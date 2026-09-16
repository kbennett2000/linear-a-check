#!/usr/bin/env python3
"""Cycle 4, Step 3.  How much choice the rules give.

For every word in the self-test, count how many different Hebrew primitive
roots the matcher finds.  Then switch off one group of rules at a time and
count again, to see how much freedom each group is adding.
"""
import csv, importlib, os, statistics, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S = importlib.import_module('22_selftest')

FORMULA_ORDER = ['A-TA-I-*301-WA-JA', 'JA-DI-KI-TU', 'JA-SA-SA-RA-ME',
                 'U-NA-KA-NA-SI', 'I-PI-NA-MA', 'SI-RU-TE',
                 'TA-NA-RA-TE-U-TI-NU']

# Each group is a set of rule switches to take away.  Turning off the affixes
# also turns off N01-N03, which are the affixes cycle 4 added.
GROUPS = [
    ('one sign giving two consonants (R08)', {'R08'}),
    ('two signs giving one consonant (R17-R19)', {'R17', 'R18', 'R19'}),
    ('the different ways of writing ṯ (R11, R16, R19, R27)',
     {'TH', 'R19', 'R27'}),
    ('unwritten throat sounds (R07, R21)', {'R07', 'R21'}),
    ('prefixes and suffixes (R37-R61, and N01-N03)',
     {'AFFIX', 'R61', 'N01', 'N02', 'N03'}),
]


def counts(words, trie, on):
    out = {}
    for w in words:
        res, skip = M.match_word(w, trie, on=on)
        out[w] = len(res)
    return out


def stats(c):
    v = sorted(c.values())
    return min(v), int(statistics.median(v)), max(v), sum(v)


def main():
    trie, n = M.load_hebrew('primitive')
    tests = S.load_rows()
    words = sorted({w for w, _, _ in tests})
    matchable = [w for w in words if not M.unmatchable_signs(M.word_signs(w))]
    skipped = [w for w in words if w not in matchable]
    print('distinct self-test words: %d' % len(words))
    print('  of those, matchable:    %d' % len(matchable))
    print('  of those, skipped:      %d  (%s)'
          % (len(skipped), ', '.join(skipped)))
    print('Hebrew side: %d non-Aramaic primitive roots, plus their '
          'final-h-as-y forms' % n)

    base = counts(matchable, trie, M.DEFAULT_ON)
    lo, mid, hi, tot = stats(base)
    print('\nHOW MANY HEBREW ROOTS EACH WORD MATCHES (full matcher)')
    print('  smallest %d   middle (median) %d   largest %d   total %d'
          % (lo, mid, hi, tot))
    print('  average per word: %.1f' % (tot / len(matchable)))
    lowest = sorted(base.items(), key=lambda kv: kv[1])[:5]
    highest = sorted(base.items(), key=lambda kv: -kv[1])[:5]
    print('  fewest: %s' % ', '.join('%s (%d)' % kv for kv in lowest))
    print('  most:   %s' % ', '.join('%s (%d)' % kv for kv in highest))

    print('\nEVERY MATCH FOR THE SEVEN FORMULA WORDS')
    print('  written in full to reports/cycle-04-formula-matches.csv')
    out = os.path.join(HERE, 'reports', 'cycle-04-formula-matches.csv')
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        w_ = csv.writer(fh)
        w_.writerow(['word', 'paper_root', 'matched_root', 'strongs', 'gloss',
                     'pieces_removed', 'rules_used', 'sound_matches'])
        for w in FORMULA_ORDER:
            res, _ = M.match_word(w, trie)
            items = sorted(res.items(),
                           key=lambda kv: int(kv[1]['entry']['id'][1:]))
            print('  %-22s %3d roots' % (w, len(items)))
            for sk, d in items:
                w_.writerow([w, S.FORMULA[w], sk, d['entry']['id'],
                             d['entry']['gloss'], d['removed'],
                             ' '.join(sorted(d['rules'])),
                             ' '.join(sorted(d['sound']))])

    print('\nTURNING OFF ONE GROUP OF RULES AT A TIME')
    print('  %-52s %5s %6s %6s %8s %8s'
          % ('group switched off', 'min', 'median', 'max', 'total', 'change'))
    print('  %-52s %5d %6d %6d %8d %8s'
          % ('(nothing — the full matcher)', lo, mid, hi, tot, '—'))
    rows = []
    for label, off in GROUPS:
        on = M.DEFAULT_ON - off
        c = counts(matchable, trie, on)
        a, b, cc, t = stats(c)
        pct = 100.0 * (t - tot) / tot
        print('  %-52s %5d %6d %6d %8d %7.1f%%' % (label, a, b, cc, t, pct))
        rows.append((label, a, b, cc, t, pct))

    print('\nTHE SAME, FOR THE RULES CYCLE 4 ADDED (not asked for; for context)')
    print('  %-52s %5s %6s %6s %8s %8s'
          % ('switched off', 'min', 'median', 'max', 'total', 'change'))
    extra = [('N07 alone (compounds)', {'N07'}),
             ('N04 alone (unwritten middle w)', {'N04'}),
             ('N06 alone (U writing w)', {'N06'}),
             ('R62 alone (unwritten initial y)', {'R62'}),
             ('all seven added rules N01-N07', {'N01', 'N02', 'N03', 'N04',
                                                'N05', 'N06', 'N07'}),
             ('N01-N07 and R62 together',
              {'N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07', 'R62'})]
    for label, off in extra:
        c = counts(matchable, trie, M.DEFAULT_ON - off)
        a, b, cc, t = stats(c)
        print('  %-52s %5d %6d %6d %8d %7.1f%%'
              % (label, a, b, cc, t, 100.0 * (t - tot) / tot))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
