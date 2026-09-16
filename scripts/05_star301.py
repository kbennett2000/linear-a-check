#!/usr/bin/env python3
"""Item 2: sign *301.

The paper (p.5) says *301 has 291 attestations, of which 238 stand alone,
"predominantly on Hagia Triada roundels, with additional examples at Khania,
Knossos, and Zakros."

"Standing alone" = a transliteratedWords token that is exactly "*301" (the sign
is the whole word). "Total attestations" = every token in which the substring
"*301" appears, i.e. standalone plus *301 inside longer words.
"""
import json
from collections import Counter

INS = json.load(open('data/derived/inscriptions.json'))

standalone = []   # (inscription id, site, support)
inword = []       # (id, token)
for iid, v in INS.items():
    for t in (v.get('transliteratedWords') or []):
        if t == '*301':
            standalone.append((iid, v.get('site', ''), v.get('support', '')))
        elif '*301' in t:
            inword.append((iid, t))

print(f'standalone "*301" tokens          : {len(standalone)}')
print(f'*301 inside a longer word (tokens): {len(inword)}')
print(f'total tokens containing "*301"    : {len(standalone) + len(inword)}')
print()

print('STANDALONE *301 BY SITE')
for s, c in Counter(s for _, s, _ in standalone).most_common():
    print(f'  {s or "<blank>":20} {c}')
print()
print('STANDALONE *301 BY SUPPORT (corpus field)')
for s, c in Counter(sup for _, _, sup in standalone).most_common():
    print(f'  {s or "<blank>":20} {c}')
print()
print('STANDALONE *301 BY SITE x SUPPORT')
for (s, sup), c in Counter((s, sup) for _, s, sup in standalone).most_common():
    print(f'  {s or "<blank>":20} {sup or "<blank>":20} {c}')
print()

# The user notes: at Hagia Triada, ids starting HTWa are labelled "Nodule" and
# ids starting HTWc are labelled "Roundel" in this file.
print('HAGIA TRIADA STANDALONE *301 BY ID PREFIX')
pref = Counter()
for iid, s, sup in standalone:
    if s == 'Haghia Triada':
        p = iid[:4] if iid[:3] == 'HTW' else iid[:2]
        pref[(p, sup)] += 1
for (p, sup), c in sorted(pref.items()):
    print(f'  {p:6} {sup:10} {c}')
print()
print(f'distinct inscriptions with >=1 standalone *301: '
      f'{len({i for i, _, _ in standalone})}')
print()
print('WORDS CONTAINING *301 (not standalone), by form')
for w, c in Counter(t for _, t in inword).most_common():
    ids = sorted({i for i, t in inword if t == w})
    print(f'  {w:26} x{c:<3} {", ".join(ids)}')
