#!/usr/bin/env python3
"""Item 5: vowel share.

The paper, p.24 n.53: "Counting recognized syllabogram tokens, and excluding
logograms, quantities, dividers, unknown signs, damaged tokens, and compounds,
/a, i, u/ account for 3,823 of 4,733 tokens (80.8%)."

A syllabogram is a sign standing for a whole syllable (KA, TI, ...), as opposed
to a logogram, a sign standing for a whole word or commodity (VIN "wine",
GRA "grain").

COUNTING CHOICES, all made explicit because small choices move the total:
 C1  Unit of counting = the SIGN token, not the word. We split each
     transliteratedWords word on "-" and count the pieces.
 C2  We count only signs on an explicit whitelist of recognized syllabograms
     (below). Anything not on it is excluded; that implements "recognized
     syllabogram tokens" and all six of the paper's exclusions at once.
 C3  Excluded as QUANTITIES: digits, fractions, "double mina", weight marks.
 C4  Excluded as DIVIDERS: the Aegean word separator and newlines.
 C5  Excluded as LOGOGRAMS: VIN GRA CYP OLE OLIV AROM CAP VIR HIDE VS GAL VAS L.
 C6  Excluded as UNKNOWN SIGNS: anything written *NNN (e.g. *301, *118).
 C7  Excluded as COMPOUNDS: any segment containing "+" (ligatures such as
     OLE+DI, *301+*311). The paper's word for these is "compounds".
 C8  Excluded as DAMAGED: any segment containing "[", "]" or "?".
 C9  Vowel of a syllabogram = the vowel letter of its transliterated value;
     the Linear A "complex" signs keep their base vowel (RA2 -> a, PA3 -> a,
     TA2 -> a, PU2 -> u, NWA -> a, TWE -> e).
 C10 AU (AB85) is a VV sign the paper itself calls a diphthong (p.17 n.29),
     not a plain CV syllabogram. Main count EXCLUDES it; a variant is reported.
 C11 Pure-vowel signs A, E, I, O, U are counted as syllabograms (they are
     syllables). A variant excluding them is reported.
"""
import json, re
from collections import Counter

INS = json.load(open('data/derived/inscriptions.json'))

VOWEL_OF = {}
for v, group in [
    ('a', 'A DA JA KA MA NA PA QA RA SA TA WA ZA RA₂ PA₃ TA₂ NWA'),
    ('e', 'E DE JE KE ME NE QE RE SE TE ZE TWE'),
    ('i', 'I DI KI MI NI PI QI RI SI TI WI'),
    ('o', 'O KO PO RO TO ZO'),
    ('u', 'U DU JU KU MU NU PU RU SU TU ZU PU₂'),
]:
    for s in group.split():
        VOWEL_OF[s] = v

PURE_VOWEL = set('A E I O U'.split())

def sign_tokens():
    for iid, v in INS.items():
        for word in (v.get('transliteratedWords') or []):
            for seg in word.split('-'):
                if seg:
                    yield seg

segs = list(sign_tokens())

def count(include_au, include_pure_vowels):
    c = Counter()
    for s in segs:
        if s == 'AU':
            if include_au:
                c['u_diphthong'] += 1      # AU ends in u
            continue
        v = VOWEL_OF.get(s)
        if v is None:
            continue
        if s in PURE_VOWEL and not include_pure_vowels:
            continue
        c[v] += 1
    total = sum(c.values())
    aiu = c['a'] + c['i'] + c['u'] + c.get('u_diphthong', 0)
    return c, total, aiu

print('PAPER (p.24 n.53): /a,i,u/ = 3,823 of 4,733 syllabogram tokens = 80.8%')
print()
variants = [
    ('MAIN: AU excluded, pure-vowel signs included', False, True),
    ('AU included as /u/',                            True,  True),
    ('pure-vowel signs A,E,I,O,U excluded',           False, False),
    ('AU included, pure-vowel signs excluded',        True,  False),
]
for label, au, pv in variants:
    c, total, aiu = count(au, pv)
    pct = 100 * aiu / total if total else 0
    print(f'{label}')
    print(f'   a={c["a"]}  e={c["e"]}  i={c["i"]}  o={c["o"]}  u={c["u"]}'
          f'{"  au=" + str(c["u_diphthong"]) if au else ""}')
    print(f'   /a,i,u/ = {aiu} of {total} = {pct:.1f}%   '
          f'(paper: 3823 of 4733 = 80.8%)')
    print(f'   difference vs paper: total {total - 4733:+d}, '
          f'a/i/u {aiu - 3823:+d}, percentage {pct - 80.8:+.1f} points')
    print()

# What the excluded classes cost us
c, total, _ = count(False, True)
excluded = Counter()
for s in segs:
    if s in VOWEL_OF or s == 'AU':
        continue
    if re.fullmatch(r'\*\S+', s):            excluded['unknown sign *NNN'] += 1
    elif '+' in s:                           excluded['compound/ligature'] += 1
    elif '[' in s or ']' in s or '?' in s:   excluded['damaged'] += 1
    elif re.fullmatch(r'[\d.,]+', s):        excluded['number'] += 1
    elif s in ('\n',):                       excluded['newline'] += 1
    elif s.isascii() and s.isalpha():        excluded['logogram (letters)'] += 1
    else:                                    excluded['divider/fraction/other'] += 1
print('EXCLUDED SIGN TOKENS BY CLASS')
for k, n in excluded.most_common():
    print(f'   {k:26} {n}')
print(f'   {"TOTAL excluded":26} {sum(excluded.values())}')
print(f'   {"TOTAL counted (main)":26} {total}')
print(f'   {"grand total segments":26} {len(segs)}')
