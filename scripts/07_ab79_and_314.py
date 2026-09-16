#!/usr/bin/env python3
"""Item 6: sign AB79. The paper (p.36) says it "appears in 25 distinct Linear A
word-forms". This corpus writes AB79 with its Linear B value ZU; the paper
writes it *79 (and vocalises it TH).

Item 7: sign *314. The paper (p.17 n.30) says it "is attested six times in the
Linear A corpus (Hagia Triada, Kophinas, Phaistos, Arkhalokhori)".
"""
import json, re
from collections import defaultdict

INS = json.load(open('data/derived/inscriptions.json'))

def tokens():
    for iid, v in INS.items():
        for t in (v.get('transliteratedWords') or []):
            yield iid, v.get('site', ''), t

def report(label, pred):
    forms = defaultdict(list)
    n = 0
    for iid, site, t in tokens():
        if pred(t):
            forms[t].append((iid, site))
            n += 1
    print(f'{label}: {n} tokens, {len(forms)} distinct word-forms, '
          f'{len({s for l in forms.values() for _, s in l})} sites')
    for w in sorted(forms):
        ids = ', '.join(f'{i}' for i, _ in sorted(forms[w]))
        print(f'   {w:34} x{len(forms[w]):<3} {ids}')
    print()
    return forms

print('=' * 70)
print('ITEM 6: AB79, written ZU in this corpus')
print('=' * 70)
# A sign name in these transliterations is a token segment: word-forms are
# hyphen-joined sign names, some with + (ligature) or bare. Match ZU as a whole
# sign, not as part of another name.
SEP = re.compile(r'[-+\[\]]')
def has_sign(t, name):
    return name in [p for p in SEP.split(t) if p]

report('ZU as a whole sign', lambda t: has_sign(t, 'ZU'))
report('any "ZU" substring (looser)', lambda t: 'ZU' in t)
# is *79 ever written literally?
report('literal "*79"', lambda t: has_sign(t, '*79'))

print('=' * 70)
print('ITEM 7: *314')
print('=' * 70)
report('*314 as a whole sign', lambda t: has_sign(t, '*314'))
report('any "*314" substring', lambda t: '*314' in t)
