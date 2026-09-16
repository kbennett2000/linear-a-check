#!/usr/bin/env python3
"""Cycle 3.  Check every quote in reports/cycle-03-rules.csv against the paper.

The PDF text layer drops most spaces between words, so the comparison is made
with every space removed from both sides, and with curly quotes, apostrophes
and the several dash characters folded to plain ones.

The text layer also keeps the soft hyphens the typesetter used to break words
at the end of a line ("repre-sented", "syl-labary").  A quote that does not
match on the first pass is therefore tried again with every hyphen removed
from both sides, and the pass it matched on is reported.  Anything that still
does not match is printed so it can be fixed; nothing is corrected
automatically.
"""
import csv, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = os.path.join(HERE, 'reports', 'cycle-03-rules.csv')
TEXT = os.path.join(HERE, 'data', 'derived', 'paper_text.txt')

FOLD = {'‘': "'", '’': "'", '“': '"', '”': '"',
        '–': '-', '—': '-', '−': '-', '‐': '-',
        '‑': '-', '­': '', 'ﬁ': 'fi', 'ﬂ': 'fl'}


def norm(s):
    s = unicodedata.normalize('NFC', s)
    for a, b in FOLD.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', '', s)


def main():
    paper = norm(open(TEXT, encoding='utf-8').read())
    rows = list(csv.DictReader(open(RULES, encoding='utf-8')))
    nohy = paper.replace('-', '')
    bad, exact, dehyphenated = [], 0, []
    for r in rows:
        q = r['quote']
        if not q:
            bad.append((r['rule_id'], 'empty quote'))
        elif norm(q) in paper:
            exact += 1
        elif norm(q).replace('-', '') in nohy:
            dehyphenated.append(r['rule_id'])
        else:
            bad.append((r['rule_id'], q))
    print('rules checked: %d' % len(rows))
    print('quotes matched with spaces removed: %d' % exact)
    print('quotes matched once the typesetter\'s line-break hyphens were removed too: %d  %s'
          % (len(dehyphenated), ' '.join(dehyphenated)))
    if bad:
        print('NOT FOUND:')
        for rid, q in bad:
            print('  %s  %s' % (rid, q))
        sys.exit(1)
    print('every quote matches the paper text')


if __name__ == '__main__':
    main()
