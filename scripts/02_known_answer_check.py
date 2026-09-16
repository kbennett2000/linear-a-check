#!/usr/bin/env python3
"""Known-answer check: reproduce four numbers the user measured from the
same corpus file before doing any other analysis."""
import json
from collections import Counter

INS = json.load(open('data/derived/inscriptions.json'))

EXPECTED = {
    'entries in inscriptions Map': 1721,
    'distinct hyphen-containing transliteratedWords strings': 995,
    'transliteratedWords tokens exactly "KU-RO"': 37,
    'transliteratedWords tokens exactly "*301"': 238,
}

tokens = []           # every transliteratedWords token, across all inscriptions
for k, v in INS.items():
    tokens.extend(v.get('transliteratedWords') or [])

got = {
    'entries in inscriptions Map': len(INS),
    'distinct hyphen-containing transliteratedWords strings':
        len({t for t in tokens if '-' in t}),
    'transliteratedWords tokens exactly "KU-RO"': sum(1 for t in tokens if t == 'KU-RO'),
    'transliteratedWords tokens exactly "*301"': sum(1 for t in tokens if t == '*301'),
}

ok = True
for label, exp in EXPECTED.items():
    g = got[label]
    mark = 'MATCH' if g == exp else 'MISMATCH'
    if g != exp:
        ok = False
    print(f'{mark:9} {label}: expected {exp}, got {g}')

print()
print(f'total transliteratedWords tokens: {len(tokens)}')
print(f'inscriptions lacking transliteratedWords: '
      f'{sum(1 for v in INS.values() if not v.get("transliteratedWords"))}')
print()
print('ALL FOUR REPRODUCED' if ok else 'STOP: at least one number differs')
