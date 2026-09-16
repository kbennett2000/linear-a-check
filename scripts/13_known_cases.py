#!/usr/bin/env python3
"""Verify the four known cases the brief says must come out a particular way.
If any of these fails, the checker is wrong and the cycle should stop."""
import json
INS = json.load(open('data/derived/inscriptions.json'))
CHK = json.load(open('data/derived/readings_checked.json'))

def rows(word=None, where=None, ins=None):
    out = CHK
    if word: out = [r for r in out if r['word'] == word]
    if where: out = [r for r in out if where in r['where']]
    if ins: out = [r for r in out if ins in r['inscription']]
    return out

ok = True
def check(label, cond, detail=''):
    global ok
    print(f'{"PASS" if cond else "FAIL"}  {label}')
    if detail:
        print(f'        {detail}')
    if not cond:
        ok = False

print('=' * 72)
print('KNOWN CASE 1: IO Za 2')
print('=' * 72)
SEVEN = ['A-TA-I-*301-WA-JA', 'JA-DI-KI-TU', 'JA-SA-SA-RA-ME', 'U-NA-KA-NA-SI',
         'I-PI-NA-MA', 'SI-RU-TE', 'TA-NA-RA-TE-U-TI-NU']
main = [r for r in CHK if r['word'] in SEVEN and r['where'].startswith('§4')
        or (r['word'] in SEVEN and r['where'].startswith('§5'))
        or (r['word'] in SEVEN and r['where'].startswith('§6'))]
check('all seven §4-§6 words of the prayer are "exact"',
      all(r['group'] == 'exact' for r in main) and len(main) == 7,
      f'{len(main)} rows, groups: {sorted({r["group"] for r in main})}')
s7 = rows('A-TA-I-NA-WA-JA', '§7')
check('§7 prints A-TA-I-NA-WA-JA -> "same word, different spelling"',
      len(s7) == 1 and s7[0]['group'] == 'same word, different spelling',
      s7[0]['group'] + ' | ' + s7[0]['allowance'] if s7 else 'row missing')

print()
print('=' * 72)
print('KNOWN CASE 2: IO Za 6')
print('=' * 72)
for w in ('I-NA-TA', 'I-*79-DI-SI-KA'):
    rs = rows(w, ins='IO Za 6')
    check(f'{w} -> "different word breaks"',
          bool(rs) and all(r['group'] == 'different word breaks' for r in rs),
          '; '.join(f'{r["where"]}: {r["group"]} ({r["note"]})' for r in rs))
print(f'   corpus IOZa6: {[t for t in INS["IOZa6"]["transliteratedWords"] if t.strip()]}')

print()
print('=' * 72)
print('KNOWN CASE 3: PK Za 11 - the paper reads this spot two ways')
print('=' * 72)
ss = [r for r in CHK if r['word'] == 'SA-SA-RA-ME']
for r in ss:
    print(f'   SA-SA-RA-ME   {r["where"]:22} -> {r["corpus_id"]:8} {r["group"]}')
asr = [r for r in CHK if r['word'] == 'A-SA-SA-RA-ME']
for r in asr:
    print(f'   A-SA-SA-RA-ME {r["where"]:22} -> {r["corpus_id"]:8} {r["group"]}')
    print(f'                 ref as printed: "{r["inscription"]}"')
    print(f'                 note: {r["note"]}')
raw = INS['PKZa11']['transliteratedWords']
i = raw.index('SA-SA-RA-ME')
# walk back over whitespace-only tokens (line breaks); the claim to test is that
# nothing but a line break separates A from SA-SA-RA-ME - in particular, no
# word divider.
j = i - 1
between = []
while j >= 0 and not raw[j].strip():
    between.append(raw[j]); j -= 1
check('corpus PK Za 11 has a bare A before SA-SA-RA-ME with no word divider '
      'between them',
      raw[j] == 'A' and '\U0001d101' not in between and
      not any(b.strip() for b in between),
      f'preceding token {raw[j]!r}; separated only by {between!r} '
      f'(a line break, not the word divider)')
check('the paper reads this spot two different ways '
      '(SA-SA-RA-ME in §4.3/§8; A-SA-SA-RA-ME in Appendix B)',
      any('PK Za 11' in r['inscription'] for r in ss) and
      any('PKZa11' in r['inscription'].replace(' ', '') for r in asr),
      'both printings present in the table')

print()
print('=' * 72)
print('KNOWN CASE 4: KH 11 - the paper corrects Davis')
print('=' * 72)
adr = rows('A-DU-RE-ZA')[0]
t = [x for x in INS['KH11']['transliteratedWords'] if x.strip()]
check('A-DU-RE-ZA is "not found" in the corpus', adr['group'] == 'not found')
check('the corpus reads A-DU, then a word divider, then ZA',
      t[0] == 'A-DU' and t[1] == '𐄁' and t[2] == 'ZA',
      f'corpus KH11 opens: {t[:4]}')
check("the paper's correction is supported by the corpus",
      adr['group'] == 'not found' and t[:3] == ['A-DU', '𐄁', 'ZA'],
      'paper says Davis mis-transcribed A-DU-RE-ZA and the tablet reads '
      'A-DU | ZA with REST absent; the corpus shows exactly that')

print()
print('ALL FOUR KNOWN CASES AS DESCRIBED' if ok else
      'STOP: a known case did not come out as described')
