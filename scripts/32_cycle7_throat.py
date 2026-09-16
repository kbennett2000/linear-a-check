#!/usr/bin/env python3
"""Cycle 7, Step 2, question (c).  English against Hebrew with the throat
consonants taken out of the comparison.

R07 lets a throat consonant (ʾ ʿ h ḥ) go unwritten, so a root containing one is
far easier to match than one that does not.  53.8% of the Hebrew list's
skeletons contain a throat consonant against 7.9% of the English list's, so some
of English's lower score is that difference and not the language.  This script
re-runs both lists restricted to the skeletons that contain **no** throat
consonant at all, which removes the advantage from both sides at once.
"""
import importlib, json, os, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')

THROAT = set('ʾʿhḥ')
NOSITE = frozenset()


def main():
    d = json.load(open(os.path.join(HERE, 'data', 'derived', 'cycle6_sets.json'),
                       encoding='utf-8'))
    L = json.load(open(os.path.join(HERE, 'data', 'derived', 'cycle7_lists.json'),
                       encoding='utf-8'))
    real = [w for w, v in d['real'].items() if not v['read_by_paper']]
    like = [x for v in d['like'].values() for x in v]

    print('WHICH MATCHER LETTERS EACH LIST CAN CONTAIN')
    letters = {}
    for nm, key in (('Hebrew', 'hebrew'), ('English', 'english')):
        letters[nm] = {c for s in L[key] for c in s.split('-')}
    print('  in Hebrew but never in English: %s'
          % ' '.join(sorted(letters['Hebrew'] - letters['English'])))
    print('  in English but never in Hebrew: %s'
          % (' '.join(sorted(letters['English'] - letters['Hebrew'])) or '(none)'))

    sets = S5.rule_sets()
    print('\nMATCHES PER 1,000 ROOTS, WHOLE LIST vs THROAT-FREE PART OF IT')
    print('  %-8s %-12s %-22s %7s %9s %9s'
          % ('list', 'rule set', 'word set', 'roots', 'per 1000', 'coverage'))
    for nm, key in (('Hebrew', 'hebrew'), ('English', 'english')):
        whole = set(L[key])
        free = {s for s in whole if not THROAT & set(s.split('-'))}
        for label, skels in (('whole', whole), ('no throat', free)):
            t = M.Trie()
            for s in skels:
                t.add(s, s)
            t.finish()
            for setname, (on, alpha) in sets.items():
                on = on - {'R62', 'R63'}
                cache = {}
                for ws, words in (('real (never read)', real),
                                  ('Linear A-like', like)):
                    vals = []
                    for w in words:
                        if w not in cache:
                            res, _ = M.match_word(w, t, on=on, alpha=alpha,
                                                  sites=NOSITE)
                            cache[w] = len(res)
                        vals.append(cache[w])
                    mean = statistics.mean(vals)
                    print('  %-8s %-12s %-22s %7d %9.2f %9.4f'
                          % ('%s, %s' % (nm, label) if ws.startswith('real') else '',
                             setname if ws.startswith('real') else '', ws,
                             len(skels), 1000 * mean / len(skels),
                             sum(1 for v in vals if v) / len(vals)))


if __name__ == '__main__':
    main()
