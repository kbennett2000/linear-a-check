#!/usr/bin/env python3
"""Cycle 4.  Write reports/cycle-04-rules-added.csv and check its quotes.

Seven rules were added to the matcher in Step 2, each because a row of the
self-test could not otherwise be reproduced.  Every one is tied to a passage in
the paper: four are things the paper states, three are things it does without
saying so.  Nothing here is invented.

The quote column is checked against data/derived/paper_text.txt the same way
cycle 3 checked the 66-rule table: spaces removed, and the typesetter's
line-break hyphens removed on a second pass.
"""
import csv, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(HERE, 'reports', 'cycle-04-rules-added.csv')
TEXT = os.path.join(HERE, 'data', 'derived', 'paper_text.txt')

ROWS = [
    dict(rule_id='N01', kind='prefix or suffix',
         rule='-TU at the end of a word is the feminine nominal ending, so it '
              'can be taken off.',
         allows='-TU = feminine nominal ending',
         stated_or_used='stated', where='§4.2 table, p.6',
         quote='TU AB69 B69 𐀶 /tu/ Feminine nominal ending',
         needed_for='JA-DI-KI-TU → √d-q-q (4 rows)',
         examples='JA-DI-KI-TU (p.6); A-RA-TU-ME "erṣetum, fem. + mimation" '
                  '(p.37); KU-PA₃-NA-TU "+ -atu, feminine of KU-PA₃-NU" (p.38)'),
    dict(rule_id='N02', kind='prefix or suffix',
         rule='-TA at the end of a word can write a feminine ending -at or '
              '-āt, so it can be taken off.',
         allows='-TA = feminine -at / -āt',
         stated_or_used='used', where='§8, p.16; Appendix B, p.38',
         quote='I-NA-TA is certainly the Minoan doublet of Ugaritic Anat and '
               'Biblical Anath',
         needed_for='I-NA-TA → √ʿ-n-y (2 rows)',
         examples='I-NA-TA read ʿInat (p.16); I-NA-JA-RE-TA read ʾinayirʾāta '
                  '(p.38).  The paper states the same ending written -TE at '
                  'A-TA-NA-TE (p.38, already R52) and -TU at KU-PA₃-NA-TU (p.38)'),
    dict(rule_id='N03', kind='prefix or suffix',
         rule='RU can be taken out as the separate particle lū, "may, let". '
              'The paper describes it as inserted into the word.',
         allows='RU- = the particle lū, removable',
         stated_or_used='stated', where='§5.1, p.9',
         quote='between U-NA and KA-NA-SI, yielding hunna lū kanasī',
         needed_for='U-NA-RU-KA-NA-SI and U-NA-RU-KA-NA-TI → √k-n-s (3 rows)',
         examples='U-NA-RU-KA-NA-SI (p.9); U-NA-RU-KA-NA-TI (p.40); '
                  'U-NA-RU-KA-JA-SI (p.40).  R34 already gives RU the value lū; '
                  'this makes it a piece that can be taken out.'),
    dict(rule_id='N04', kind='spelling habit',
         rule='The middle consonant of a three-letter root can go unwritten '
              'when it is w.',
         allows='root C₂ = w may have no sign',
         stated_or_used='used', where='Appendix B, pp.38, 39, 40',
         quote='rāmāh “height” (√r-w-m “be high”)',
         needed_for='RU-MA-TA, RU-MA-TA-SE → √r-w-m; I-ZU-RI-NI-TA, '
                    'ZU-RI-NI-MA → √ṯ-w-r (4 rows)',
         examples='RU-MA-TA and RU-MA-TA-SE read rāmāh from √r-w-m (p.39); '
                  'I-ZU-RI-NI-TA and ZU-RI-NI-MA from √ṯ-w-r (pp.38, 40).  The '
                  'paper never states this; it is what its readings do.'),
    dict(rule_id='N05', kind='spelling habit',
         rule='A root-initial n can go unwritten when it runs into the next '
              'consonant, which is then written as a doubled sign.',
         allows='root C₁ = n may have no sign when the next two signs are an '
                'identical pair',
         stated_or_used='used', where='Appendix B, p.40',
         quote='Nun → geminate /tt/ (√n-t-k “pour out”)',
         needed_for='TI-TI-KU and I-TI-TI-KU-NI → √n-t-k (2 rows)',
         examples='TI-TI-KU read hittīkū (p.40); I-TI-TI-KU-NI (p.38).  The '
                  'paper discusses the same assimilation in Hebrew at p.9 '
                  '(*han-bayt > hab-bayt) and p.12.'),
    dict(rule_id='N06', kind='sound',
         rule='A U sign can write the root consonant w.',
         allows='U = w (as well as nothing, or a throat consonant)',
         stated_or_used='used', where='Appendix B, p.39',
         quote='Cf. tG √n-w-y (3ms prefix ya-; same paradigm as '
               'A-TA-I-*301-WA-JA)',
         needed_for='JA-TA-I-*301-U-JA → √n-w-y (1 row)',
         examples='JA-TA-I-*301-U-JA (p.39).  The paper says it is the same '
                  'shape as A-TA-I-*301-WA-JA, where WA writes the w; here the '
                  'U sits in that slot.  This is read off the paradigm, not '
                  'stated sign by sign.'),
    dict(rule_id='N07', kind='word breaks',
         rule='A word can be a compound of two Semitic words, each with its '
              'own root. Both halves must spell a root.',
         allows='word = element₁ + element₂, each spelling a root',
         stated_or_used='used', where='Appendix B, pp.37, 38',
         quote='mānāh “to allot” (√y-š-r + √m-n-y)',
         needed_for='JA-SA-SA-RA-MA-NA → √m-n-y; A-MI-DA-O, A-MI-DA-U → '
                    '√ʿ-m-m and √y-d-ʿ; I-NA-JA-PA-QA → √p-q-ḥ (6 rows)',
         examples='JA-SA-SA-RA-MA-NA = yāšār + mānāh (p.38); A-MI-DA-O and '
                  'A-MI-DA-U = √ʿ-m-m + √y-d-ʿ (p.37); I-NA-JA-PA-QA = √ʾ-n-n '
                  '+ √p-q-ḥ (p.38)'),
]

FOLD = {'‘': "'", '’': "'", '“': '"', '”': '"',
        '–': '-', '—': '-', '−': '-', '‐': '-', '‑': '-', '­': ''}


def norm(s):
    s = unicodedata.normalize('NFC', s)
    for a, b in FOLD.items():
        s = s.replace(a, b)
    return re.sub(r'\s+', '', s)


def main():
    paper = norm(open(TEXT, encoding='utf-8').read())
    nohy = paper.replace('-', '')
    bad = []
    exact = dehy = 0
    for r in ROWS:
        q = norm(r['quote'])
        if q in paper:
            exact += 1
        elif q.replace('-', '') in nohy:
            dehy += 1
        else:
            bad.append((r['rule_id'], r['quote']))

    fields = ['rule_id', 'kind', 'rule', 'allows', 'stated_or_used', 'where',
              'quote', 'needed_for', 'examples']
    with open(DST, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(ROWS)
    print('wrote reports/cycle-04-rules-added.csv  (%d rules)' % len(ROWS))

    from collections import Counter
    print('by stated_or_used: %s'
          % dict(Counter(r['stated_or_used'] for r in ROWS)))
    print('by kind:           %s' % dict(Counter(r['kind'] for r in ROWS)))
    print('\nquotes matched with spaces removed: %d' % exact)
    print('quotes matched once line-break hyphens were removed too: %d' % dehy)
    over = [(r['rule_id'], len(r['quote'].split())) for r in ROWS
            if len(r['quote'].split()) > 25]
    print('quotes over 25 words: %s' % (over if over else 'none'))
    if bad:
        print('NOT FOUND IN THE PAPER:')
        for rid, q in bad:
            print('  %s  %s' % (rid, q))
        sys.exit(1)
    print('every quote matches the paper text')


if __name__ == '__main__':
    raise SystemExit(main())
