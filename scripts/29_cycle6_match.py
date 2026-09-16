#!/usr/bin/env python3
"""Cycle 6, Steps 2 and 3.  Match the real and made-up word sets.

Writes reports/cycle-06-sets.csv.

Terms.  The *median* is the middle value when the numbers are put in order:
half the words match more roots than this, half match fewer.  *Coverage* here
is the share of words that match at least one Hebrew primitive root.  "Match"
never means anything about meaning; it means only that the word's signs can be
read as that root's consonants under the rules being applied.
"""
import csv, importlib, json, os, statistics, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')

SETS = os.path.join(HERE, 'data', 'derived', 'cycle6_sets.json')
READ = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
HEB = os.path.join(HERE, 'data', 'derived', 'hebrew_list.json')
OUT = os.path.join(HERE, 'reports', 'cycle-06-sets.csv')

TO_HEBREW = {'ṯ': 'š', 'ḏ': 'z', 'ḫ': 'ḥ', 'ġ': 'ʿ'}   # not from the paper
FORMULA = ['A-TA-I-*301-WA-JA', 'JA-DI-KI-TU', 'JA-SA-SA-RA-ME',
           'U-NA-KA-NA-SI', 'I-PI-NA-MA', 'SI-RU-TE', 'TA-NA-RA-TE-U-TI-NU']
NOSITE = frozenset()


def paper_roots():
    """The paper's roots that are in the Hebrew primitive-root list.

    -> (set of skeletons, straight count, sound-match count)
    """
    heb = json.load(open(HEB, encoding='utf-8'))
    index = set()
    for e in heb:
        if e['primitive_root']:
            index.add(e['skeleton'])
            if 'skeleton_final_h_as_y' in e:
                index.add(e['skeleton_final_h_as_y'])
    roots = set()
    for r in csv.DictReader(open(READ, encoding='utf-8')):
        for x in r['root'].split('|'):
            x = x.strip()
            if x:
                roots.add(x)
    straight = {x for x in roots if x in index}
    shifted = set()
    for x in roots - straight:
        y = '-'.join(TO_HEBREW.get(c, c) for c in x.split('-'))
        if y in index:
            shifted.add(y)
    return straight | shifted, straight, shifted, len(roots)


def stats(vals):
    if not vals:
        return dict(word_count=0, share_any_root='', min_roots='',
                    median_roots='', max_roots='', mean_roots='')
    return dict(word_count=len(vals),
                share_any_root=round(sum(1 for v in vals if v) / len(vals), 4),
                min_roots=min(vals), median_roots=statistics.median(vals),
                max_roots=max(vals), mean_roots=round(statistics.mean(vals), 2))


def main():
    target, straight, shifted, n_roots = paper_roots()
    print("THE PAPER'S ROOTS IN THE HEBREW PRIMITIVE-ROOT LIST")
    print('  distinct roots in reports/cycle-03-readings.csv: %d' % n_roots)
    print('  found as a Strong\'s primitive root:              %d' % len(straight))
    print('  found only after the four sound matches:         %d  (%s)'
          % (len(shifted), ' '.join(sorted(shifted))))
    print('  target set used in Step 3:                       %d' % len(target))
    print('  the four sound matches are not from the paper, but the matcher has')
    print('  applied them since cycle 4, so the target set matches what it returns.')

    d = json.load(open(SETS, encoding='utf-8'))
    print('\nseed recorded in the sets file: %d' % d['seed'])
    real = d['real']
    trie, n_prim = M.load_hebrew('primitive')
    sets = S5.rule_sets()

    # ---- the word lists.  Made-up sets are kept as the full list of draws,
    # so the length mix stays the one Step 1 checked; matching is cached per
    # distinct spelling, so repeats cost nothing.
    shuf_draws = [x for v in d['shuffled'].values() for x in v]
    like_draws = [x for v in d['like'].values() for x in v]
    print('\nWORD SETS')
    print('  real                       %5d words' % len(real))
    print('    read by the paper        %5d' % sum(1 for v in real.values()
                                                   if v['read_by_paper']))
    print('    never read               %5d' % sum(1 for v in real.values()
                                                   if not v['read_by_paper']))
    print('  shuffled                   %5d draws, %d distinct'
          % (len(shuf_draws), len(set(shuf_draws))))
    print('  Linear A-like              %5d draws, %d distinct'
          % (len(like_draws), len(set(like_draws))))

    rows = []
    cache = {}

    def counts(word, sites, key, on, alpha):
        ck = (word, sites, key)
        if ck not in cache:
            res, _ = M.match_word(word, trie, on=on, alpha=alpha, sites=sites)
            cache[ck] = (len(res), len(target & set(res)))
        return cache[ck]

    def add(word_set, setname, affix, r62, words_and_sites, on, alpha):
        by_len = defaultdict(list)
        for w, sites in words_and_sites:
            n_all, n_pap = counts(w, sites, (setname, affix, r62), on, alpha)
            by_len[len(M.word_signs(w))].append((n_all, n_pap))
        allv = [v for vs in by_len.values() for v in vs]
        for length in list(sorted(by_len)) + ['all']:
            vs = allv if length == 'all' else by_len[length]
            base = stats([a for a, _ in vs])
            pap = [b for _, b in vs]
            rows.append(dict(word_set=word_set, rule_set=setname, affixes=affix,
                             r62_r63=r62, n_signs=length, **base,
                             share_paper_root=round(
                                 sum(1 for b in pap if b) / len(pap), 4) if pap else '',
                             mean_paper_roots=round(
                                 statistics.mean(pap), 3) if pap else ''))

    for setname, (on, alpha) in sets.items():
        for affix in ('on', 'off'):
            base_on = on if affix == 'on' else (on - {'AFFIX'})
            no62 = base_on - {'R62', 'R63'}
            real_sited = [(w, frozenset(v['sites'])) for w, v in real.items()]
            real_flat = [(w, NOSITE) for w in real]
            read_flat = [(w, NOSITE) for w, v in real.items() if v['read_by_paper']]
            never_flat = [(w, NOSITE) for w, v in real.items()
                          if not v['read_by_paper']]
            add('real (all)', setname, affix, 'on', real_sited, base_on, alpha)
            add('real (all)', setname, affix, 'off', real_flat, no62, alpha)
            add('real (read by the paper)', setname, affix, 'off', read_flat,
                no62, alpha)
            add('real (never read)', setname, affix, 'off', never_flat, no62, alpha)
            add('shuffled', setname, affix, 'off',
                [(w, NOSITE) for w in shuf_draws], no62, alpha)
            add('Linear A-like', setname, affix, 'off',
                [(w, NOSITE) for w in like_draws], no62, alpha)
            print('  done: %-12s affixes %s' % (setname, affix))

    COLS = ['word_set', 'rule_set', 'affixes', 'r62_r63', 'n_signs', 'word_count',
            'share_any_root', 'min_roots', 'median_roots', 'max_roots',
            'mean_roots', 'share_paper_root', 'mean_paper_roots']
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print('\nwrote %s  (%d rows)' % (os.path.relpath(OUT, HERE), len(rows)))

    # ------------------------------------------------------------------
    # the seven formula words against 1,000 Linear A-like words each
    # ------------------------------------------------------------------
    print('\nEACH FORMULA WORD AGAINST 1,000 MADE-UP WORDS OF THE SAME LENGTH')
    print('  (R62 and R63 off on both sides, so the comparison is even)')
    fl = d['formula_like']
    for setname, (on, alpha) in sets.items():
        no62 = on - {'R62', 'R63'}
        print('\n  %s rule set' % setname)
        print('  %-22s %6s %8s %8s %10s' % ('word', 'roots', 'made-up',
                                            'beats', 'ties'))
        for w in FORMULA:
            real_n, _ = counts(w, NOSITE, (setname, 'on', 'f'), no62, alpha)
            made = [counts(x, NOSITE, (setname, 'on', 'f'), no62, alpha)[0]
                    for x in fl[w]]
            fewer = sum(1 for m in made if m < real_n)
            same = sum(1 for m in made if m == real_n)
            print('  %-22s %6d %8d %7.1f%% %9.1f%%'
                  % (w, real_n, len(made), 100 * fewer / len(made),
                     100 * same / len(made)))
    print('\n"beats" is the share of the 1,000 made-up words that match fewer '
          'roots than the real word does.')


if __name__ == '__main__':
    main()
