#!/usr/bin/env python3
"""Cycle 3, Part C, coverage check.

Take every root in the `root` column of reports/cycle-03-readings.csv and look
for it in data/derived/hebrew_list.json among the entries Strong's marks as a
primitive root, counting the second final-h-as-y skeleton as a match.

The four sound matches between older Semitic spelling and Hebrew spelling
(ṯ = š, ḏ = z, ḫ = ḥ, ġ = ʿ) are NOT part of the paper.  They are applied here
only as a clearly separate second pass, to show what difference they make.
"""
import csv, json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READ = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
HEB = os.path.join(HERE, 'data', 'derived', 'hebrew_list.json')

# not from the paper: the standard correspondences between the older Semitic
# consonants the paper writes and the letters Hebrew spelling uses
TO_HEBREW = {'ṯ': 'š', 'ḏ': 'z', 'ḫ': 'ḥ', 'ġ': 'ʿ'}

SEVEN = ['n-w-y', 'd-q-q', 'y-š-r', 'k-n-s', 'p-n-y', 'š-r-t', 'r-ṣ-y']


def shift(root):
    return '-'.join(TO_HEBREW.get(c, c) for c in root.split('-'))


def main():
    heb = json.load(open(HEB, encoding='utf-8'))
    roots_index = defaultdict(list)          # skeleton -> primitive-root entries
    for e in heb:
        if not e['primitive_root']:
            continue
        roots_index[e['skeleton']].append(e)
        if 'skeleton_final_h_as_y' in e:
            roots_index[e['skeleton_final_h_as_y']].append(e)

    rows = list(csv.DictReader(open(READ, encoding='utf-8')))
    langs = defaultdict(set)
    order = []
    for r in rows:
        for root in [x.strip() for x in r['root'].split('|') if x.strip()]:
            if root not in langs:
                order.append(root)
            for l in [y.strip() for y in r['languages'].split('|') if y.strip()]:
                langs[root].add(l)
            langs[root]                      # make sure the key exists
    order = sorted(set(order))

    def report(title, roots):
        found, missing = [], []
        for root in roots:
            hits = roots_index.get(root, [])
            (found if hits else missing).append((root, hits))
        print('\n%s  (%d roots)' % (title, len(roots)))
        print('  found as a Strong\'s primitive root: %d' % len(found))
        print('  not found:                          %d' % len(missing))
        for root, hits in found:
            e = hits[0]
            extra = ' (+%d more)' % (len(hits) - 1) if len(hits) > 1 else ''
            print('    %-12s %-6s %-9s %s%s'
                  % (root, e['id'], e['skeleton'], e['gloss'][:46], extra))
        for root, _ in missing:
            l = ' | '.join(sorted(langs[root])) or '(no comparison language given)'
            print('    %-12s NOT FOUND   compared to: %s' % (root, l))
        return found, missing

    f7, m7 = report('The seven Part A known-answer roots', SEVEN)
    others = [r for r in order if r not in SEVEN]
    fo, mo = report('Every other root in the Part A column', others)

    print('\nTOTAL over all %d distinct roots: %d found, %d not found'
          % (len(order), len(f7) + len(fo), len(m7) + len(mo)))

    # second pass, clearly separate: apply the four sound matches
    still, rescued = [], []
    for root, _ in m7 + mo:
        s = shift(root)
        (rescued if (s != root and s in roots_index) else still).append((root, s))
    print('\nSecond pass, NOT part of the paper: applying ṯ=š, ḏ=z, ḫ=ḥ, ġ=ʿ')
    print('  roots that then match a primitive root: %d' % len(rescued))
    for root, s in rescued:
        print('    %-12s -> %-12s %s' % (root, s, roots_index[s][0]['id']))
    print('  roots still not found: %d' % len(still))

    # context: the check above only looks at entries Strong's marks "primitive
    # root".  Many of the paper's roots are noun roots, which Strong's lists as
    # nouns instead.  This shows how many turn up anywhere in the dictionary.
    any_index = defaultdict(list)
    for e in heb:
        any_index[e['skeleton']].append(e)
    print('\nContext: the same %d not-found roots looked up among ALL Strong\'s entries,'
          % (len(m7) + len(mo)))
    print('not just the primitive-root ones (still no sound matches applied)')
    seen_any, seen_none = [], []
    for root, _ in m7 + mo:
        (seen_any if root in any_index else seen_none).append(root)
    print('  present as some entry\'s skeleton: %d' % len(seen_any))
    for root in seen_any:
        e = any_index[root][0]
        print('    %-12s %-6s %-9s %s' % (root, e['id'], e['xlit'], e['gloss'][:46]))
    print('  absent from the dictionary altogether: %d' % len(seen_none))
    for root in seen_none:
        l = ' | '.join(sorted(langs[root])) or '(no comparison language given)'
        print('    %-12s compared to: %s' % (root, l))


if __name__ == '__main__':
    main()
