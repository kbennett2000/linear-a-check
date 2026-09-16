#!/usr/bin/env python3
"""Step 2: build the readings table.

One row for each Linear A word the paper gives a reading or a meaning for, in
each place it gives one. The same word read in two places (e.g. in the main text
and again in Appendix B) gets two rows; the distinct-word count in
scripts/13_counts.py handles deduplication.

Appendix B's 67 entries are parsed automatically by scripts/10_parse_appendix_b.py.
Everything else is transcribed by hand from the PDF text, because the main text
and footnotes give readings in running prose rather than in a fixed format.

EXCLUDED, with reasons:
  - Appendix C (pp. 40-42). Its five- and six-word spells are Egyptian
    group-writing from the London Medical Papyrus, not Linear A.
  - Linear B forms cited for comparison (da-pu2-ri-to, po-ti-ni-ja, a-ka-wi-ja,
    a-ta-na-po-ti-ni-ja, su-ki-ri-to, da-i-pi-ta, ta-na-to, ku-mi-no ...). The
    paper is explicit that these are Linear B: "Were it Linear A, we would read
    ʾa-ḫa-wi-ya" (p. 21).
  - Forms quoted only to show a sign or a sound change with no reading attached
    (e.g. "WA-JA -> WA-E" on p. 22; the fragment "I-NA-I-DA" on p. 14 n. 20).
  - Hebrew and Arabic script, per the brief.
"""
import csv, json, re

# word | where | inscription as printed | reading | meaning | confidence
ROWS_RAW = """
A-KA-NU|Appendix A, p.36|KN Zc 7|ʾagānu|bowl|CONFIRMED
ZA-TI|Appendix A, p.36|KN Zc 7|ḏāti|of (fs genitive relative)|PROBABLE
DU-RA-RE|Appendix A, p.36|KN Zc 7|durar|freedom, purity|PROBABLE
A-*79-RA|Appendix A, p.36|KN Zc 7|ʾAṯirat|Athirat (the Goddess)|CANDIDATE
JA-SA-RA|Appendix A, p.36|KN Zc 7|yašara|righteous|PROBABLE
A-NA-NE|Appendix A, p.36|KN Zc 7|ḥanān|grace|CANDIDATE
WI-PI|Appendix A, p.36|KN Zc 7|wīpī|and my mouth|SPECULATIVE
*79-DU|Appendix A (AB79 note), p.36|HT 51b|ṯudu|breast|
*79-DU|Appendix A (AB79 note), p.36|HT 99b|ṯudu|breast|
MA-*79|Appendix A (AB79 note), p.36|HT 102|maṯu|man|
*79-RI-NI-MA|Appendix A (AB79 note), p.36|KN Zb 52|Ṯawrinima|a "bull" name|
A-TA-I-*301-WA-JA|§4.1, pp.4-6|IO Za 2|ʾatainawaya|I make myself a dwelling|
JA-DI-KI-TU|§4.2, pp.6-7|IO Za 2|yā Diqqitu|O Diqqitu! (the mountain goddess)|
JA-SA-SA-RA-ME|§4.3, pp.7-8|IO Za 2|yašāram|in (the spirit of) righteousness|
JA-SA-RA|§4.3, p.8|KN Zc 7|yašar-|righteous (same root, single SA)|
SA-SA-RA-ME|§4.3, p.8|PK Za 11|(yašāram without JA-)|righteousness, JA-less variant|
A-SA-SA-RA|§4.3, p.8|PK Za 4|(yašāram without JA-)|righteousness, standalone inscription|
I-MI-SA-RA|§4.3, p.8|HT 27a|(Mīšaru)|divine recipient, "righteousness"|
TI-NI-TA|§4.3, p.8|HT 27a|Tinit|the Goddess Tinit|
QA-QA-RU|§4.3 n.13, p.8|HT 118|qaqqaru|ground|
QA-QA-RU|§4.3 n.13, p.8|HT 122b|qaqqaru|ground|
QA-QA-RU|§4.3 n.13, p.8|HT 93a|qaqqaru|ground|
U-NA-KA-NA-SI|§5.1, p.9|IO Za 2|hunna kanasī|behold, my assembly!|
U-NA-RU-KA-NA-SI|§5.1, p.9|IO Za 16|hunna lū kanasī|behold, may my assembly gather!|
RA-KI-NI-SE|§5.1, p.9|SY Zb 7|la-kinnisēt|for the assembly|
I-PI-NA-MA|§5.2, p.10|IO Za 2|ʾipinama|in the presence of|
SI-RU-TE|§5.3, pp.10-11|IO Za 2|šīrūt|sacred worship, ministry|
TA-NA-RA-TE-U-TI-NU|§6.1, pp.12-13|IO Za 2|tana-raṣē-ū-tī-nū|may she be accepted for you|
A-RE-TU-MI|§6.1, p.12|ZA 7a|ʾarṣ-ummī|Earth is my mother|
*301-SI|§4.1 n.10, p.5|TI Zb 1|nāśī|prince|
TE-*301|§4.1 n.10, p.5|HT 8a|tēna|fig|
NA-TU-*301-NE|§4.1 n.10, p.5|SKO Zc 1|natūnān|the dedicated one|
A-TA-I-NA-WA-JA|§7 table, p.14|IO Za 2|ʾatainawaya|I make myself a dwelling|
JA-DI-KI-TU|§7 table, p.14|IO Za 2|yā Diqqitu|O Diqqitu!|
JA-SA-SA-RA-ME|§7 table, p.14|IO Za 2|yašāram|in (the spirit of) righteousness|
U-NA-KA-NA-SI|§7 table, p.14|IO Za 2|hunna kanasī|Behold, my assembly!|
I-PI-NA-MA|§7 table, p.14|IO Za 2|ʾipinama|in the presence of|
SI-RU-TE|§7 table, p.14|IO Za 2|šīrūt|sacred worship|
TA-NA-RA-TE-U-TI-NU|§7 table, p.14|IO Za 2|tana-raṣē-ū-tī-nū|May she be accepted for you|
I|§7 table, p.14|IO Za 2|(CH008)|"hand" (left untranslated)|
SI-KI-NE|§7, p.14|HT 116a|šikinēt|recipient title, cf. Linear B potnia|
TU-ME|§7, p.15|PK Za 14|tōm|perfection (tōm wāyōšer)|
TU-ME-I|§7, p.15|PK Za 8|tōm|perfection|
DU-RA-RE|§7, p.15|KN Zc 7|(√d-r-r)|to purify, be free|
A-TH-RA|§7, p.15|KN Zc 7|ʾAṯirat|Athirat|
JA-SA-RA|§7, p.15|KN Zc 7|yašar-|righteous|
A-TA-I-*301-WA-JA|§8 table, p.16|IO Za 2||position 1, invocation|
JA-DI-KI-TU|§8 table, p.16|IO Za 2||position 2, deity/site|
JA-SA-SA-RA-ME|§8 table, p.16|IO Za 2||position 3, righteousness|
U-NA-KA-NA-SI|§8 table, p.16|IO Za 2||position 4, gathering|
I-PI-NA-MA|§8 table, p.16|IO Za 2||position 5, presence|
SI-RU-TE|§8 table, p.16|IO Za 2||position 6, sacred ministry|
TA-NA-RA-TE-U-TI-NU|§8 table, p.16|IO Za 2||position 7, petition|
TA-NA-I-*301-U-TI-NU|§8 table, p.16|IO Za 6||position 1, invocation|
I-NA-TA|§8 table, p.16|IO Za 6|ʿInat|position 2, deity; Anat|
I-*79-DI-SI-KA|§8 table, p.16|IO Za 6||position 2, deity/site (cont.)|
JA-SA-SA-RA-ME|§8 table, p.16|IO Za 6||position 3, righteousness|
A-TA-I-*301-WA-JA|§8 table, p.16|TL Za 1||position 1, invocation|
O-SU-QA-RE|§8 table, p.16|TL Za 1||position 2, deity/site|
JA-SA-SA-RA-ME|§8 table, p.16|TL Za 1||position 3, righteousness|
U-NA-KA-NA|§8 table, p.16|TL Za 1||position 4, gathering|
I-PI-NA-MA|§8 table, p.16|TL Za 1||position 5, presence|
SI-RU-TE|§8 table, p.16|TL Za 1||position 6, sacred ministry|
A-TA-I-*301-WA-JA|§8 table, p.16|KO Za 1||position 1, invocation|
TU-RU-SA|§8 table, p.16|KO Za 1||position 2, deity/site|
DU-*314-RE|§8 table, p.16|KO Za 1||position 2, deity/site (cont.)|
I-DA-A|§8 table, p.16|KO Za 1||position 2, deity/site (cont.)|
U-NA-KA-NA-SI|§8 table, p.16|KO Za 1||position 4, gathering|
I-PI-NA-MA|§8 table, p.16|KO Za 1||position 5, presence|
SI-RU-TE|§8 table, p.16|KO Za 1||position 6, sacred ministry|
A-TA-I-*301-WA-E|§8 table, p.16|PK Za 11||position 1, invocation|
A-DI-KI-TE-TE|§8 table, p.16|PK Za 11||position 2, deity/site|
SA-SA-RA-ME|§8 table, p.16|PK Za 11||position 3, righteousness|
U-NA-RU-KA-NA-TI|§8 table, p.16|PK Za 11||position 4, gathering|
I-PI-NA-MI-NA|§8 table, p.16|PK Za 11||position 5, presence|
SI-RU|§8 table, p.16|PK Za 11||position 6, sacred ministry|
A-TA-I-*301-WA-JA|§8 table, p.16|SY Za 3||position 1, invocation|
SE-KA-NA-SI|§8 table, p.16|SY Za 3||position 4, gathering|
SI-RU-TE|§8 table, p.16|SY Za 3||position 6, sacred ministry|
TA-NA-I-NA-U-TI-NU|§8, p.16|IO Za 6|tanainautīnū|may she answer for you|
I-NA-TA|§8, p.16|IO Za 6|ʿInat|Anat, "she who answers"|
I-TH-DI-SI-KA|§8, p.17|IO Za 6|I-Ṯadi Siqqa|the breast that gives drink|
O-SU-QA-RE|§8, p.17|TL Za 1|ʾO-Sukar|the Egyptian god Sokar|
TU-RU-SA|§8, p.17|KO Za 1|(√t-r-s)|to shield, protect, fortify|
DU-*314-RE|§8, p.17|KO Za 1|dū-ḥurre|the one of the noble/freeborn|
I-DA-A|§8, p.17|KO Za 1|Ida + hē locale|toward Ida|
AU-SI-RE|§8 n.29, p.17|PH(?) 31a|Ousire|Osiris|
MA-DI|§8 n.29, p.17|PH(?) 31a|mōʿēd|appointed festival|
JE-DI|§8 n.31, p.17|HT (4 attestations)|yedī|the Idaean|
A-SA-MU-NE|§8, p.18|ZA Zb 3|ʾAšmun|the god Eshmun|
A-TA-I-*301-DE-KA|§8, p.18|ZA Zb 3|ʾata-iʿnay-dēka|who answered for you|
SA-SA-RA-ME|§8, p.18|PK Za 11|(yašāram without JA-)|righteousness; initial JA dropped|
A-TA-NA|§8, p.18|ZA 9|(yatan-)|She-who-gives|
DU-PU₂-RE|§9, p.19|PK Za 11|dubur|sanctuary|
DU-PU₂-RE|§9, p.19|PK Za 12|dubur|sanctuary|
DU-PU₂-RE|§9, p.19|PK Za 15|dubur|sanctuary|
A-DI-KI-TE-TE|§9, p.19|PK Za 11|(Diqqiṯe)|Dikte (in the Petsofas sequence)|
*307|§9, p.19|HT 27a|dubur|sanctuary/debir (logographic)|
TI-NI-TA|§9, p.19|HT 27a|Tinit|the Minoan serpent goddess|
SU-KI-RI-TE-I-JA|§10 n.41, p.21|HT Zb 158b|(Sybrita + gentilic)|the Keretian|
"""

rows = []
for line in ROWS_RAW.strip().splitlines():
    w, where, ins, reading, meaning, conf = (line.split('|') + [''] * 6)[:6]
    rows.append({'word': w, 'where': where, 'inscription': ins,
                 'reading': reading, 'meaning': meaning, 'confidence': conf})

# ---- Appendix B, parsed ----
APPB = json.load(open('data/derived/appendix_b.json'))

def appb_fields(body):
    """Pull the full printed inscription reference and a short meaning out of an
    entry body. The reference is everything before the first sentence end, with
    the parenthesised GORILA/SigLA citations removed but the "(?)" site marker
    kept (PH(?) is a real corpus id prefix)."""
    r = body.replace('(?)', '\x01')
    r = re.sub(r'\([^)]*\)', ' ', r)
    r = r.split('.')[0]
    r = r.replace('\x01', '(?)')
    ref = re.sub(r'\s+', ' ', r).strip().rstrip(',;')
    gl = re.findall(r'[\u201c"]([^\u201d"]{1,60})[\u201d"]', body)
    meaning = gl[0] if gl else ''
    if 'Unknown' in body[:40]:
        meaning = 'unknown'
    if 'viablereading' in body.replace(' ', '') :
        meaning = 'no viable reading'
    # the paper's own verdict on a Davis form it rejects
    paper_note = ''
    if 'Mis-transcribed' in body or 'isnotanattestedword' in body.replace(' ', ''):
        paper_note = ("paper states Davis mis-transcribed this; "
                      "paper reads the tablet as A-DU | ZA")
    return ref, meaning, paper_note

for e in APPB:
    ref, meaning, paper_note = appb_fields(e['body'])
    rows.append({'word': e['word'], 'where': 'Appendix B, pp.36-40',
                 'inscription': ref, 'reading': '', 'meaning': meaning,
                 'confidence': '', 'paper_note': paper_note})

json.dump(rows, open('data/derived/readings_rows.json', 'w'), ensure_ascii=False, indent=1)
print(f'hand-transcribed rows : {len(rows) - len(APPB)}')
print(f'Appendix B rows       : {len(APPB)}')
print(f'TOTAL rows            : {len(rows)}')
