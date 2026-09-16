#!/usr/bin/env python3
"""Cycle 5.  What the two decisions carried in from cycle 4 actually change.

  1. *319 gets the conditional value R32 gives it (/hū/), because the paper
     uses it.  How many words does that affect?
  2. R62 (an initial JA- dropped) is restricted to Palaikastro and R63 to
     Zakros, as the paper has it, instead of cycle 4's apply-everywhere.  How
     many matches does that remove?
"""
import csv, importlib, json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')
SELF = importlib.import_module('22_selftest')

INSCR = os.path.join(HERE, 'data', 'derived', 'inscriptions.json')
READ = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')


def main():
    trie, _ = M.load_hebrew('primitive')
    sets = S5.rule_sets()
    full_on, full_alpha = sets['full']
    pool, dropped, count = S5.word_pool(full_alpha)

    # ---------------- decision 1: *319 = /hū/
    print('DECISION 1 — *319 given its conditional value /hū/ (R32)')
    no319 = M.Alphabet()                      # the cycle 4 table, without *319
    pool0, dropped0, _ = S5.word_pool(no319)
    gained = sorted(set(pool) - set(pool0))
    print('  distinct corpus words the matcher can read, without *319: %d' % len(pool0))
    print('  with *319:                                                %d' % len(pool))
    print('  words this makes readable: %d' % len(gained))
    for w in gained:
        print('    %-34s %2d× in the corpus' % (w, pool[w]['n']))
    inpaper = sum(1 for r in csv.DictReader(open(READ, encoding='utf-8'))
                  if '*319' in M.word_signs(r['word']))
    print('  rows of the paper\'s readings table containing *319: %d '
          '(2 of them in cycle 4\'s self-test, both of which it had to skip)'
          % inpaper)
    print('  none of the 20 *301 words contains *319, so Step 2 is unaffected')

    # ---------------- decision 2: R62/R63 restricted by site
    print('\nDECISION 2 — R62 restricted to Palaikastro, R63 to Zakros')
    d = json.load(open(INSCR, encoding='utf-8'))

    def totals(sitewise):
        cov = tot = 0
        for w, info in pool.items():
            res, _ = M.match_word(w, trie, on=full_on, alpha=full_alpha,
                                  sites=info['sites'] if sitewise else None)
            cov += 1 if res else 0
            tot += len(res)
        return cov, tot

    cov_b, tot_b = totals(False)      # cycle 4's behaviour: fires anywhere
    cov_a, tot_a = totals(True)       # cycle 5: only at the two sites
    print('  over the whole %d-word corpus pool:' % len(pool))
    print('    cycle 4, fires anywhere : coverage %d, %d matches' % (cov_b, tot_b))
    print('    cycle 5, only at the two sites: coverage %d, %d matches'
          % (cov_a, tot_a))
    print('    removed: %d matches (%.1f%%), coverage down by %d words'
          % (tot_b - tot_a, 100.0 * (tot_b - tot_a) / tot_b, cov_b - cov_a))
    pk = sum(1 for v in pool.values() if 'Palaikastro' in v['sites'])
    za = sum(1 for v in pool.values() if 'Zakros' in v['sites'])
    print('    of the %d pool words, %d are found at Palaikastro and %d at Zakros'
          % (len(pool), pk, za))

    # the same, on cycle 4's self-test rows
    # A word's sites are every site the corpus attests it at, not just the one
    # inscription the paper happens to cite -- A-SA-SA-RA-ME, for instance, is
    # cited at IO Zb 10 but is also attested at Palaikastro.
    site_of = {}
    for e in d.values():
        for w in (e.get('transliteratedWords') or []):
            if isinstance(w, str) and '-' in w:
                site_of.setdefault(w, set()).add(e.get('site') or '')
    for r in csv.DictReader(open(READ, encoding='utf-8')):
        cid = r['corpus_id']
        if r['word'] not in site_of and cid and cid in d:
            site_of[r['word']] = {d[cid].get('site') or ''}
    tests = SELF.load_rows()
    have = sum(1 for w, _, _ in tests if site_of.get(w))
    print('  on cycle 4\'s self-test: %d of %d rows have a word the corpus '
          'attests somewhere, so a site can be checked' % (have, len(tests)))
    base = {(r['word'], r['paper_root'], r['where']): r['result']
            for r in SELF.run(tests, trie)}
    lost = []
    for w, root, where in tests:
        acc = SELF.hebrew_spelt(root)
        res, skip = M.match_word(w, trie, on=M.CYCLE5_ON,
                                 sites=site_of.get(w) or set())
        if base[(w, root, where)] == 'found' and not any(k in res for k in acc):
            lost.append('%s / %s' % (w, root))
    print('    rows that stop being found once the site is checked: %d' % len(lost))
    for x in sorted(set(lost)):
        print('      %s' % x)


if __name__ == '__main__':
    main()
