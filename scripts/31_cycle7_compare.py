#!/usr/bin/env python3
"""Cycle 7, Steps 2 and 3.  Match cycle 6's words against each root list.

Writes reports/cycle-07-lists.csv.

Settings are cycle 6's: both rule sets, prefixes and suffixes on, R62 and R63
off so real and made-up words are judged alike.  The word sets are cycle 6's
real words and Linear A-like words, rebuilt from seed 20260916; the shuffled
set is dropped, as the brief directs.

Terms.  *Coverage* is the share of words matching at least one root in the list.
*Matches per 1,000 roots* is the average number of roots a word matches divided
by the size of the list, times a thousand: it lets lists of different sizes be
compared, since a longer list gives more chances to match.
"""
import csv, importlib, json, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')

SETS = os.path.join(HERE, 'data', 'derived', 'cycle6_sets.json')
LISTS = os.path.join(HERE, 'data', 'derived', 'cycle7_lists.json')
OUT = os.path.join(HERE, 'reports', 'cycle-07-lists.csv')
NOSITE = frozenset()

LIST_ORDER = [('Hebrew', 'hebrew'), ('Hebrew + Ugaritic', 'hebrew_ugaritic'),
              ('made-up roots', 'made_up'), ('English', 'english'),
              ("the paper's stated roots", 'paper_stated')]


def trie_of(skels):
    t = M.Trie()
    for s in skels:
        t.add(s, s)
    t.finish()
    return t


def main():
    d = json.load(open(SETS, encoding='utf-8'))
    L = json.load(open(LISTS, encoding='utf-8'))
    real = d['real']
    like_draws = [x for v in d['like'].values() for x in v]
    word_sets = {
        'real (read by the paper)': [w for w, v in real.items() if v['read_by_paper']],
        'real (never read)': [w for w, v in real.items() if not v['read_by_paper']],
        'Linear A-like': like_draws,
    }
    print('WORD SETS (cycle 6, seed %d; R62 and R63 off throughout)' % d['seed'])
    for k, v in word_sets.items():
        print('  %-26s %5d words (%d distinct)' % (k, len(v), len(set(v))))

    sets = S5.rule_sets()
    rows = []

    def run(list_name, key, setname, on, alpha, trie, size, no_sound):
        # The four sound matches (ṯ=š …) are switched off for the paper's own
        # roots: the brief asks for the root as the paper writes it, with no
        # dictionary and no correspondence in between.
        keep = M.SOUND_MATCH
        if no_sound:
            M.SOUND_MATCH = {}
        try:
            cache = {}
            for ws, words in word_sets.items():
                by_len = defaultdict(list)
                for w in words:
                    if w not in cache:
                        res, _ = M.match_word(w, trie, on=on, alpha=alpha,
                                              sites=NOSITE)
                        cache[w] = len(res)
                    by_len[len(M.word_signs(w))].append(cache[w])
                allv = [v for vs in by_len.values() for v in vs]
                for length in list(sorted(by_len)) + ['all']:
                    vs = allv if length == 'all' else by_len[length]
                    mean = statistics.mean(vs)
                    rows.append(dict(
                        root_list=list_name, roots_in_list=size, word_set=ws,
                        rule_set=setname, n_signs=length, word_count=len(vs),
                        coverage=round(sum(1 for v in vs if v) / len(vs), 4),
                        median_roots=statistics.median(vs),
                        mean_roots=round(mean, 2),
                        matches_per_1000_roots=round(1000 * mean / size, 2)))
        finally:
            M.SOUND_MATCH = keep

    for list_name, key in LIST_ORDER:
        skels = L[key]
        trie = trie_of(skels)
        for setname, (on, alpha) in sets.items():
            run(list_name, key, setname, on - {'R62', 'R63'}, alpha, trie,
                len(skels), no_sound=(key == 'paper_stated'))
        print('  done: %s (%d roots)' % (list_name, len(skels)))

    COLS = ['root_list', 'roots_in_list', 'word_set', 'rule_set', 'n_signs',
            'word_count', 'coverage', 'median_roots', 'mean_roots',
            'matches_per_1000_roots']
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print('\nwrote %s  (%d rows)' % (os.path.relpath(OUT, HERE), len(rows)))

    # ------------------------------------------------------------------
    # known-answer check: the Hebrew column must reproduce cycle 6
    # ------------------------------------------------------------------
    print('\nKNOWN-ANSWER CHECK against reports/cycle-06-sets.csv')
    c6 = {(r['word_set'], r['rule_set'], r['n_signs']): r
          for r in csv.DictReader(open(os.path.join(HERE, 'reports',
                                                    'cycle-06-sets.csv'),
                                       encoding='utf-8'))
          if r['affixes'] == 'on' and r['r62_r63'] == 'off'}
    ok = True
    for r in rows:
        if r['root_list'] != 'Hebrew':
            continue
        k = (r['word_set'], r['rule_set'], str(r['n_signs']))
        o = c6.get(k)
        if not o:
            continue
        same = (o['share_any_root'] == str(r['coverage'])
                and float(o['median_roots']) == float(r['median_roots']))
        if r['n_signs'] == 'all':
            print('  %-26s %-12s cycle 6: cover %s median %-6s | cycle 7: %s %-6s  %s'
                  % (r['word_set'], r['rule_set'], o['share_any_root'],
                     o['median_roots'], r['coverage'], r['median_roots'],
                     'PASS' if same else 'FAIL'))
        ok &= same
    print('  every Hebrew row reproduces cycle 6 exactly: %s'
          % ('PASS' if ok else 'FAIL'))

    # ------------------------------------------------------------------
    # what the brief's "work them out once per word" shortcut would cost
    # ------------------------------------------------------------------
    print('\nWHY THE SKELETONS ARE WORKED OUT ONCE PER LIST, NOT ONCE PER WORD')
    heb = set(L['hebrew'])
    own = trie_of(heb)
    union = trie_of(set().union(*(set(L[k]) for _, k in LIST_ORDER)))
    on, alpha = sets['full']
    on = on - {'R62', 'R63'}
    a = b = diff = 0
    for w in real:
        ra, _ = M.match_word(w, own, on=on, alpha=alpha, sites=NOSITE)
        rb, _ = M.match_word(w, union, on=on, alpha=alpha, sites=NOSITE)
        rbh = {k for k in rb if k in heb}
        a += len(ra)
        b += len(rbh)
        diff += (set(ra) != rbh)
    print('  Hebrew matches over all %d real words, own trie:   %d' % (len(real), a))
    print('  the same, via one shared trie over all five lists: %d  (+%.2f%%)'
          % (b, 100 * (b - a) / a))
    print('  real words where the two disagree: %d of %d' % (diff, len(real)))
    print('  Three rules -- R22 (unwritten s before a stop), R24 (unwritten r) and')
    print('  N04 (unwritten middle w) -- look ahead into the list to decide whether')
    print('  they may fire, so a word\'s possible skeletons are not quite')
    print('  list-independent.  Every list below is therefore matched against its')
    print('  own trie, which is what cycles 4-6 did and what keeps the Hebrew')
    print('  column identical to cycle 6.')


if __name__ == '__main__':
    main()
