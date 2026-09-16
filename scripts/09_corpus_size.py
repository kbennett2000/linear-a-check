#!/usr/bin/env python3
"""Item 1: corpus size.

The paper, p.3: "I have reconciled and deduplicated all 1,468 documents from
the five volumes of GORILA (Godart & Olivier 1976-1985), 261 additional entries
tabulated by George Douros from post-1985 publications (Hallager 1996), as well
as 51 face-level records from the SigLA database (Salgarella & Castellan 2021)."
1,468 + 261 + 51 = 1,780.

This file has no explicit "source" field, but imageRightsURL points at the
scanned GORILA volumes for entries that come from GORILA, which gives us a
usable proxy for the GORILA share.
"""
import json, re
from collections import Counter

INS = json.load(open('data/derived/inscriptions.json'))
print(f'entries in this file: {len(INS)}')
print(f"paper's corpus:       1780   (difference: {len(INS) - 1780:+d})")
print()

def bucket(u):
    if not u:
        return '<empty>'
    m = re.search(r'GORILA-Vol(\d)', u)
    if m:
        return f'GORILA vol {m.group(1)}'
    return re.sub(r'[#?].*$', '', u)[:60]

b = Counter(bucket(v.get('imageRightsURL', '')) for v in INS.values())
for k, n in b.most_common():
    print(f'  {k:34} {n}')
gor = sum(n for k, n in b.items() if k.startswith('GORILA vol'))
print()
print(f'  entries citing a GORILA volume : {gor}')
print(f"  paper's GORILA count           : 1468   "
      f"({'MATCH' if gor == 1468 else f'differs by {gor-1468:+d}'})")
print(f'  entries NOT citing GORILA      : {len(INS) - gor}')
print(f"  paper's Douros + SigLA         : 261 + 51 = 312   "
      f"(difference: {len(INS) - gor - 312:+d})")
print()
print('non-GORILA entries by site:')
for s, n in Counter(v.get('site', '') for v in INS.values()
                    if not bucket(v.get('imageRightsURL', '')).startswith('GORILA')).most_common():
    print(f'  {s or "<blank>":22} {n}')
