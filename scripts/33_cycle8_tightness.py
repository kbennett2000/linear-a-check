#!/usr/bin/env python3
"""Cycle 8, Step 1.  How tight is each of the paper's readings?

For every reading cycle 4's self-test found, under each rule set:

  reachable  does the word still match its root with these rules?
  options    how many Hebrew primitive roots the word matches at all
  chance     the share of 1,000 made-up Linear A-like words of the same length
             that can also be read as that root

Writes reports/cycle-08-readings.csv.

Terms.  *Chance* here is the share of made-up words that could be read as the
same root.  A **low** chance means the reading is *tight*: most made-up words of
that length cannot be read that way.  *Options* is the opposite measure: how
much freedom the rules left when the root was picked.  A *batch* is one shared
set of 1,000 made-up words, drawn once per word length, so every reading of that
length is judged against the same words.
"""
import csv, importlib, json, os, random, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')
S6 = importlib.import_module('28_cycle6_sets')

SELFTEST = os.path.join(HERE, 'reports', 'cycle-04-selftest.csv')
READINGS = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
INSCR = os.path.join(HERE, 'data', 'derived', 'inscriptions.json')
OUT = os.path.join(HERE, 'reports', 'cycle-08-readings.csv')
SEED = 20260916
BATCH = 1000
FORMULA = ['A-TA-I-*301-WA-JA', 'JA-DI-KI-TU', 'JA-SA-SA-RA-ME',
           'U-NA-KA-NA-SI', 'I-PI-NA-MA', 'SI-RU-TE', 'TA-NA-RA-TE-U-TI-NU']

NO_CHANCE = ('the paper reads only part of this word as this root (N07), and a '
             'test against one root cannot express that')


def trie_of(skels):
    t = M.Trie()
    for s in skels:
        t.add(s, s)
    t.finish()
    return t


def main():
    rows = [r for r in csv.DictReader(open(SELFTEST, encoding='utf-8'))
            if r['result'] == 'found']
    print('readings cycle 4 found: %d' % len(rows))

    # ---- each reading's site: the site of the inscription the paper cites
    ins = json.load(open(INSCR, encoding='utf-8'))
    site_of = {}
    for r in csv.DictReader(open(READINGS, encoding='utf-8')):
        cid = r['corpus_id']
        site_of[(r['word'], r['where'])] = (
            (ins.get(cid, {}).get('site') or '') if cid else '')
    print('readings with no row in cycle 3\'s table: %d'
          % sum(1 for r in rows if (r['word'], r['where']) not in site_of))
    sites = {}
    for r in rows:
        s = site_of.get((r['word'], r['where']), '')
        sites[(r['word'], r['where'])] = frozenset([s]) if s else frozenset()
    print('readings whose cited inscription gives no site: %d'
          % sum(1 for v in sites.values() if not v))

    # ---- what counts as "this row's root".
    # The paper's own spelling, plus the spelling cycle 4 actually matched where
    # Hebrew writes the same root differently (p-n-y / p-n-h).  No dictionary:
    # the trie below holds only the roots recorded for this one word.
    target, bag = {}, defaultdict(set)
    for r in rows:
        t = {r['paper_root']} | {x.strip()
                                 for x in r['hebrew_spelling'].split(' or ')}
        target[(r['word'], r['where'], r['paper_root'])] = t
        bag[r['word']] |= t

    # ---- the made-up batches: one per length, shared by every reading.
    # Drawn with repeats allowed: the batch is a sample used to estimate a
    # share, so a word drawn twice should count twice.  (Insisting on distinct
    # words would also have made a full batch impossible at two signs.)
    pool, _, _ = S5.word_pool(S5.rule_sets()['full'][1])
    allt = {t for e in ins.values() for t in (e.get('transliteratedWords') or [])
            if isinstance(t, str) and t.strip()}
    model = S6.BigramModel(pool)
    rng = random.Random(SEED)
    lengths = sorted({len(M.word_signs(r['word'])) for r in rows})
    batches = {n: model.batch(n, BATCH, allt, rng, distinct=False)
               for n in lengths}
    print('\nMADE-UP BATCHES (seed %d, one per length, shared by every reading)'
          % SEED)
    for n in lengths:
        b = batches[n]
        print('  %d signs: %d words (%d distinct)' % (n, len(b), len(set(b))))

    trie, _ = M.load_hebrew('primitive')
    out = []
    for setname, (on, alpha) in S5.rule_sets().items():
        cache = {}
        for r in rows:
            word, where, root = r['word'], r['where'], r['paper_root']
            n = len(M.word_signs(word))
            st = sites[(word, where)]
            want = target[(word, where, root)]
            res, _ = M.match_word(word, trie, on=on, alpha=alpha, sites=st)
            reach = bool(want & set(res))
            row = dict(word=word, where=where, root=root, rule_set=setname,
                       n_signs=n, site=(sorted(st) or [''])[0],
                       reachable='yes' if reach else 'no',
                       options=len(res) if reach else '', chance='', note='')
            if reach:
                key = (word, root, n, st, setname)
                if key not in cache:
                    keep = M.SOUND_MATCH
                    M.SOUND_MATCH = {}          # no dictionary correspondences
                    try:
                        t1 = trie_of(bag[word])
                        self_ok = bool(want & set(
                            M.match_word(word, t1, on=on, alpha=alpha,
                                         sites=st)[0]))
                        share = None
                        if self_ok:
                            hit = sum(1 for w in batches[n]
                                      if want & set(M.match_word(
                                          w, t1, on=on, alpha=alpha,
                                          sites=st)[0]))
                            share = hit / len(batches[n])
                    finally:
                        M.SOUND_MATCH = keep
                    cache[key] = share
                share = cache[key]
                if share is None:
                    row['note'] = NO_CHANCE
                else:
                    row['chance'] = share
            else:
                row['note'] = 'not reachable with stated rules only' \
                    if setname == 'stated only' else 'not reachable'
            out.append(row)
        print('  matched: %s' % setname)

    # ---- rank, tightest first, within each rule set
    for setname in S5.rule_sets():
        rs = sorted([x for x in out if x['rule_set'] == setname
                     and x['chance'] != ''], key=lambda x: x['chance'])
        prev, rank = None, 0
        for i, x in enumerate(rs, 1):
            if x['chance'] != prev:
                rank, prev = i, x['chance']
            x['rank'] = rank
    for x in out:
        x.setdefault('rank', '')
        if x['chance'] != '':
            x['chance'] = round(x['chance'], 4)

    COLS = ['word', 'where', 'root', 'rule_set', 'n_signs', 'site', 'reachable',
            'options', 'chance', 'rank', 'note']
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for x in out:
            w.writerow(x)
    print('\nwrote %s  (%d rows)' % (os.path.relpath(OUT, HERE), len(out)))

    for setname in S5.rule_sets():
        rs = [x for x in out if x['rule_set'] == setname]
        reach = [x for x in rs if x['reachable'] == 'yes']
        scored = [x for x in reach if x['chance'] != '']
        print('\n=== %s rule set ===' % setname)
        print('  readings reachable:      %d of %d' % (len(reach), len(rs)))
        if len(reach) < len(rs):
            print('  not reachable: %s' % ', '.join(
                sorted({x['word'] for x in rs if x['reachable'] == 'no'})))
        print('  reachable and scored:    %d' % len(scored))
        skipped = sorted({(x['word'], x['root']) for x in reach
                          if x['chance'] == ''})
        if skipped:
            print('  reachable but not scored: %d  (%s)'
                  % (len(reach) - len(scored), NO_CHANCE))
            for w_, r_ in skipped:
                print('      %-22s %s' % (w_, r_))
        ch = sorted(x['chance'] for x in scored)
        op = sorted(x['options'] for x in scored)
        print('  chance   median %.3f  smallest %.3f  largest %.3f'
              % (statistics.median(ch), ch[0], ch[-1]))
        print('  options  median %d  smallest %d  largest %d'
              % (statistics.median(op), op[0], op[-1]))
        print('  readings with a chance of 0 (no made-up word could be read '
              'that way): %d' % sum(1 for c in ch if c == 0))
        by = sorted(scored, key=lambda x: (x['chance'], x['word'], x['where']))
        for title, part in (('TEN TIGHTEST', by[:10]),
                            ('TEN LOOSEST', by[-10:][::-1])):
            print('\n  %s' % title)
            print('    %-4s %-24s %-9s %5s %8s %8s'
                  % ('rank', 'word', 'root', 'signs', 'chance', 'options'))
            for x in part:
                print('    %-4d %-24s %-9s %5d %7.1f%% %8d'
                      % (x['rank'], x['word'], x['root'], x['n_signs'],
                         100 * x['chance'], x['options']))
        print('\n  THE SEVEN FORMULA WORDS')
        print('    %-24s %-9s %5s %8s %8s %s'
              % ('word', 'root', 'signs', 'chance', 'options', 'rank'))
        for w_ in FORMULA:
            hits = [x for x in scored if x['word'] == w_]
            if not hits:
                print('    %-24s not scored with these rules' % w_)
                continue
            x = min(hits, key=lambda y: y['chance'])
            print('    %-24s %-9s %5d %7.1f%% %8d %d of %d'
                  % (w_, x['root'], x['n_signs'], 100 * x['chance'],
                     x['options'], x['rank'], len(scored)))
        print('\n  FULL TABLE, TIGHTEST FIRST')
        print('    %-4s %-24s %-9s %5s %8s %8s'
              % ('rank', 'word', 'root', 'signs', 'chance', 'options'))
        for x in by:
            print('    %-4d %-24s %-9s %5d %7.1f%% %8d'
                  % (x['rank'], x['word'], x['root'], x['n_signs'],
                     100 * x['chance'], x['options']))


if __name__ == '__main__':
    main()
