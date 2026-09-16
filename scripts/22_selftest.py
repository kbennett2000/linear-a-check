#!/usr/bin/env python3
"""Cycle 4, Step 2.  Run the matcher on the paper's own readings.

Every row of reports/cycle-03-readings.csv whose root_kind is "stated" is put
through the matcher, using the word as the paper prints it.  A row that gives
more than one root produces one test per root, so the unit here is a
(row, root) pair.

Writes reports/cycle-04-selftest.csv.
"""
import csv, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
import importlib
M = importlib.import_module('21_matcher')

READ = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
OUT = os.path.join(HERE, 'reports', 'cycle-04-selftest.csv')

# the five consonant strings cycle 3 flagged as not being Semitic roots
NON_SEMITIC = {'d-k-š-n-n', 'k-b-b', 'm-k-t', 'p-ꜣ-y-r-ʿ', 'r-r-j'}

FORMULA = {
    'A-TA-I-*301-WA-JA': 'n-w-y', 'JA-DI-KI-TU': 'd-q-q',
    'JA-SA-SA-RA-ME': 'y-š-r', 'U-NA-KA-NA-SI': 'k-n-s',
    'I-PI-NA-MA': 'p-n-y', 'SI-RU-TE': 'š-r-t',
    'TA-NA-RA-TE-U-TI-NU': 'r-ṣ-y',
}


# The two rows that stay unmatched.  Neither is a failure of the rules; the
# reason in each case is recorded in reports/cycle-04.md.
MISS_REASON = {
    ('A-TA-I-*301-WA-JA', 'n-b-ʾ'):
        'not reproducible, and correctly so: cycle 3 recorded that the paper '
        'prints √n-b-ʾ in this entry as the root of its Hebrew comparison word '
        'hitnabbēʾ, not of the Linear A word, whose root is √n-w-y',
    ('I-NA-JA-PA-QA', 'ʾ-n-n'):
        'not reproducible: the paper\'s entry reads the word as ʾinna (√ʾ-n-n) '
        'plus pāqaḥ (√p-q-ḥ) but never says what the JA in the middle writes, '
        'so the ʾ-n-n half cannot be closed off.  The √p-q-ḥ half is found',
    ('KU-MI-NA-QE', 'q-b-b'):
        'not reproducible from the word as printed: the paper assigns √q-b-b to '
        'QE alone, which it says sits on side b of the roundel before the CAP '
        'logogram, so it is not part of this sign-group',
}


def hebrew_spelt(root):
    """The paper's root written the way Hebrew spells it, plus the h/y variant."""
    heb = '-'.join(M.SOUND_MATCH.get(c, c) for c in root.split('-'))
    acc = {heb}
    if heb.endswith('-y'):
        acc.add(heb[:-1] + 'h')
    if heb.endswith('-h'):
        acc.add(heb[:-1] + 'y')
    return acc


def in_list(acc, trie):
    n = trie
    for key in acc:
        n = trie
        ok = True
        for ch in key.split('-'):
            n = n.kids.get(ch)
            if n is None:
                ok = False
                break
        if ok and n.ends:
            return True
    return False


def load_rows():
    rows = list(csv.DictReader(open(READ, encoding='utf-8')))
    tests = []
    seen = set()
    for r in rows:
        if r['root_kind'] != 'stated':
            continue
        for root in [x.strip() for x in r['root'].split('|') if x.strip()]:
            if root in NON_SEMITIC:
                continue
            key = (r['word'], root, r['where'])
            if key in seen:
                continue
            seen.add(key)
            tests.append((r['word'], root, r['where']))
    return tests


def run(tests, trie, on=M.DEFAULT_ON, label=''):
    out = []
    for word, root, where in tests:
        acc = hebrew_spelt(root)
        res, skip = M.match_word(word, trie, on=on)
        rec = {'word': word, 'where': where, 'paper_root': root,
               'hebrew_spelling': ' or '.join(sorted(acc)),
               'in_hebrew_list': 'yes' if in_list(acc, trie) else 'no',
               'result': '', 'strongs': '', 'rules_used': '',
               'sound_matches': '', 'pieces_removed': '', 'reason': '',
               'total_roots_matched': len(res)}
        if skip:
            rec['result'] = 'skipped'
            rec['reason'] = skip
        else:
            # a root may be in the list under both its -h and its -y spelling;
            # report whichever of them the matcher reached most simply
            cands = [k for k in sorted(acc) if k in res]
            hit = min(cands, key=lambda k: M.rank(res[k]['rules'],
                                                  res[k]['sound'])) if cands else None
            if hit:
                d = res[hit]
                rec['result'] = 'found'
                rec['strongs'] = d['entry']['id']
                rec['rules_used'] = ' '.join(sorted(d['rules']))
                rec['sound_matches'] = ' '.join(sorted(d['sound']))
                rec['pieces_removed'] = d['removed']
            elif rec['in_hebrew_list'] == 'no':
                rec['result'] = 'root not in the Hebrew list'
                rec['reason'] = ('the paper\'s root is not a Strong\'s primitive '
                                 'root, so the matcher cannot find it')
            else:
                rec['result'] = 'not found'
                rec['reason'] = MISS_REASON.get((word, root), '')
        out.append(rec)
    return out


def summarise(recs, title):
    c = Counter(r['result'] for r in recs)
    print('\n%s' % title)
    for k in ('found', 'not found', 'root not in the Hebrew list', 'skipped'):
        print('  %-32s %3d' % (k, c.get(k, 0)))
    testable = c.get('found', 0) + c.get('not found', 0)
    if testable:
        print('  found, of the %d testable: %.1f%%'
              % (testable, 100.0 * c.get('found', 0) / testable))
    return c


def main():
    trie, n = M.load_hebrew('primitive')
    tests = load_rows()
    print('self-test rows (word, root pairs from root_kind="stated"): %d' % len(tests))
    print('distinct words: %d' % len({t[0] for t in tests}))

    recs = run(tests, trie)
    summarise(recs, 'MAIN RESULT — against %d non-Aramaic primitive roots' % n)

    print('\nTHE SEVEN FORMULA WORDS')
    ok = True
    for w, root in FORMULA.items():
        r = next((x for x in recs if x['word'] == w and x['paper_root'] == root), None)
        good = r is not None and r['result'] == 'found'
        ok &= good
        print('  %-22s -> %-6s  %-10s %s'
              % (w, root, r['result'] if r else '(no row)',
                 'PASS' if good else 'FAIL'))
        if r and r['result'] == 'found':
            print('      %s | removed: %s | rules: %s%s'
                  % (r['strongs'], r['pieces_removed'], r['rules_used'],
                     ' | sound: ' + r['sound_matches'] if r['sound_matches'] else ''))
    print('  ALL SEVEN FORMULA WORDS FIND THEIR ROOT' if ok
          else '  STOP: a formula word did not find its root')

    print('\nMISSES (root is in the Hebrew list, matcher did not find it)')
    misses = [r for r in recs if r['result'] == 'not found']
    for r in sorted(misses, key=lambda x: (x['paper_root'], x['word'])):
        print('  %-24s %-8s %s' % (r['word'], r['paper_root'], r['where']))
    print('  total: %d' % len(misses))

    print('\nSKIPPED (a sign with no sound value in the rules table)')
    for r in [x for x in recs if x['result'] == 'skipped']:
        print('  %-24s %-8s %s' % (r['word'], r['paper_root'], r['reason'][:60]))

    print('\nROOTS NOT IN THE HEBREW LIST')
    nl = sorted({r['paper_root'] for r in recs
                 if r['result'] == 'root not in the Hebrew list'})
    print('  %d rows, %d distinct roots: %s'
          % (sum(1 for r in recs if r['result'] == 'root not in the Hebrew list'),
             len(nl), ', '.join(nl)))

    # secondary: every non-Aramaic entry, not just the primitive roots
    trie2, n2 = M.load_hebrew('all')
    recs2 = run(tests, trie2)
    summarise(recs2, 'SECONDARY RESULT — against all %d non-Aramaic entries' % n2)

    # A clearly separate check: R32 gives *319 the conditional value /hū/.
    # The matcher leaves *319 out, following the cycle 4 brief, which says any
    # other starred sign number cannot be matched.  This shows what changes.
    print('\nEXTRA CHECK — what happens if R32 (*319 = /hū/) is switched on')
    M.VALUES['*319'] = ('h',)
    M.VALUE_RULES['*319'] = frozenset(['R32'])
    M._DEFAULT_ALPHA = None          # rebuild the sign table with *319 in it
    recs319 = run([t for t in tests if '*319' in t[0]], trie)
    for r in recs319:
        print('  %-24s %-8s %-8s %s | %s'
              % (r['word'], r['paper_root'], r['result'],
                 r['pieces_removed'], r['rules_used']))
    print('  Both rows go from "skipped" to "found".  So leaving *319 out, as '
          'the cycle 4 brief directs, costs two rows.')
    del M.VALUES['*319'], M.VALUE_RULES['*319']
    M._DEFAULT_ALPHA = None

    # Leave-one-out: which of the seven rules cycle 4 added is actually doing
    # work?  A rule that loses no rows when it is switched off is not holding
    # anything up on its own, even though it was added for a row that the
    # matcher could not otherwise reach at the time.
    print('\nLEAVE-ONE-OUT ON THE RULES CYCLE 4 ADDED')
    base_f = {(r['word'], r['paper_root']): r['result'] for r in recs}
    for rid in ['N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07', 'R62']:
        alt = run(tests, trie, on=M.DEFAULT_ON - {rid})
        lost = sorted({'%s / %s' % (r['word'], r['paper_root']) for r in alt
                       if r['result'] != 'found'
                       and base_f.get((r['word'], r['paper_root'])) == 'found'})
        print('  %-4s switched off -> %2d rows lost%s'
              % (rid, len(lost), (': ' + '; '.join(lost)) if lost else ''))

    fields = ['word', 'where', 'paper_root', 'hebrew_spelling', 'in_hebrew_list',
              'result', 'strongs', 'pieces_removed', 'rules_used',
              'sound_matches', 'total_roots_matched', 'reason']
    with open(OUT, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in recs:
            w.writerow({k: r.get(k, '') for k in fields})
    print('\nwrote reports/cycle-04-selftest.csv  (%d rows)' % len(recs))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
