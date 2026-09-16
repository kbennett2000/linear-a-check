#!/usr/bin/env python3
"""Items 3 and 4: the formula's first word (the "invocation verb") and the
formula as a whole.

Item 3 - the paper (p.4 table, p.5) says the verb has 15 attestations with an
invariant I sign. We list every corpus word containing "TA-I-*301", then add the
other forms the paper explicitly treats as the same verb or the same paradigm.

Item 4 - the paper (p.4) says the formula "occurs at least 15 times across 7
sites"; section 8 (p.16) tabulates six inscriptions. We check what the corpus has
for the paper's table cells.
"""
import json
from collections import defaultdict

INS = json.load(open('data/derived/inscriptions.json'))

def toks(v):
    return v.get('transliteratedWords') or []

# ---------- item 3 ----------
print('=' * 70)
print('ITEM 3: words containing "TA-I-*301"')
print('=' * 70)
hits = defaultdict(list)
for iid, v in INS.items():
    for t in toks(v):
        if 'TA-I-*301' in t:
            hits[t].append((iid, v.get('site', '')))

total = 0
for w in sorted(hits):
    for iid, site in sorted(hits[w]):
        print(f'  {w:22} {iid:10} {site}')
        total += 1
print(f'  -> {total} tokens, {len(hits)} distinct word-forms, '
      f'{len({s for l in hits.values() for _, s in l})} sites')
print()

# Other forms the paper attaches to the same verb/paradigm. Page refs:
#   TA-NA-I-*301-U-TI-NU  p.16 sec.8 table, position 1 for IO Za 6
#   JA-TA-I-*301-U-JA     p.39 lexicon, "same paradigm as A-TA-I-*301-WA-JA"
#                          (already caught above by the substring)
#   A-TA-I-*301-DE-KA     p.18/p.37, "a variant of the formula's usual opening
#                          term" (also caught above)
RELATED = ['TA-NA-I-*301-U-TI-NU', 'TA-NA-I-*301-TI', 'A-NA-TI-*301-WA-JA']
print('OTHER FORMS THE PAPER LINKS TO THE SAME VERB / PARADIGM')
extra = 0
for form in RELATED:
    for iid, v in INS.items():
        if form in toks(v):
            print(f'  {form:22} {iid:10} {v.get("site","")}')
            extra += 1
print()
print(f'  strict "TA-I-*301" substring          : {total}')
print(f'  + TA-NA-I-*301-U-TI-NU (sec.8 pos. 1) : {total + 1}')
print(f'  + all three related forms above       : {total + extra}')
print()

# ---------- item 4 ----------
print('=' * 70)
print('ITEM 4: the formula across sites')
print('=' * 70)
# The cells of the paper's section 8 table (p.16), position 1-7.
TABLE = {
    'IO Za 2':  ['A-TA-I-*301-WA-JA', 'JA-DI-KI-TU', 'JA-SA-SA-RA-ME',
                 'U-NA-KA-NA-SI', 'I-PI-NA-MA', 'SI-RU-TE', 'TA-NA-RA-TE-U-TI-NU'],
    'IO Za 6':  ['TA-NA-I-*301-U-TI-NU', 'I-NA-TA', 'I-*79-DI-SI-KA',
                 'JA-SA-SA-RA-ME'],
    'TL Za 1':  ['A-TA-I-*301-WA-JA', 'O-SU-QA-RE', 'JA-SA-SA-RA-ME',
                 'U-NA-KA-NA', 'I-PI-NA-MA', 'SI-RU-TE'],
    'KO Za 1':  ['A-TA-I-*301-WA-JA', 'TU-RU-SA', 'DU-*314-RE', 'I-DA-A',
                 'U-NA-KA-NA-SI', 'I-PI-NA-MA', 'SI-RU-TE'],
    'PK Za 11': ['A-TA-I-*301-WA-E', 'A-DI-KI-TE-TE', 'SA-SA-RA-ME',
                 'U-NA-RU-KA-NA-TI', 'I-PI-NA-MI-NA', 'SI-RU'],
    'SY Za 3':  ['A-TA-I-*301-WA-JA', 'SE-KA-NA-SI', 'SI-RU-TE'],
}
IDMAP = {'IO Za 2': 'IOZa2', 'IO Za 6': 'IOZa6', 'TL Za 1': 'TLZa1',
         'KO Za 1': 'KOZa1', 'PK Za 11': 'PKZa11', 'SY Za 3': 'SYZa3'}

for paper_id, cells in TABLE.items():
    cid = IDMAP[paper_id]
    v = INS.get(cid)
    if v is None:
        print(f'{paper_id} ({cid}): NOT IN CORPUS')
        continue
    ct = toks(v)
    print(f'{paper_id}  -> corpus id {cid}  site={v.get("site")}  '
          f'support={v.get("support")}')
    print(f'   corpus transliteratedWords: {[t for t in ct if t.strip()]}')
    for c in cells:
        mark = 'present' if c in ct else 'NOT as its own word'
        print(f'     {c:22} {mark}')
    print()

# Every inscription that carries any position-1 verb form of the formula
VERB_FORMS = set()
for iid, v in INS.items():
    for t in toks(v):
        if 'TA-I-*301' in t or t in RELATED:
            VERB_FORMS.add((iid, v.get('site', ''), t))
print('ALL INSCRIPTIONS CARRYING A POSITION-1 VERB FORM')
by_site = defaultdict(list)
for iid, site, t in sorted(VERB_FORMS):
    by_site[site].append(f'{iid}({t})')
for s in sorted(by_site):
    print(f'  {s:14} {len(by_site[s])}  {", ".join(by_site[s])}')
print(f'  -> {len(VERB_FORMS)} attestations across {len(by_site)} sites')
