#!/usr/bin/env python3
"""Cycle 3, Part A.

Copy reports/cycle-02-readings.csv to reports/cycle-03-readings.csv and add
three columns: root, root_kind, languages.

  root       - the Semitic root the paper gives for that word, letters as the
               paper prints them.  Several roots are joined with " | ".
  root_kind  - "stated"              the paper writes it with a radical sign (v)
               "from comparison word" the paper gives only a word in another
                                      language; its consonants are copied
               "none"                neither
  languages  - the language(s) the paper compares the word to, " | " separated.

Two sources feed the columns:

  1. Appendix B (rows whose `where` starts "Appendix B").  Roots and language
     labels are pulled straight out of the stored entry bodies in
     data/derived/appendix_b.json, so those 67 rows are machine-read, not typed.

  2. Every other row.  Hand-transcribed below from the paper, keyed on
     (word, section).  Each entry records the page it was read from.

Two normalisations are applied and are reported in reports/cycle-03.md:

  * Root hyphenation.  The paper almost always prints roots hyphenated
    (v n-w-y).  Twice it prints one unhyphenated (v ntk, p.39).  Roots are
    written hyphenated throughout; the letters themselves are untouched.
  * Language labels.  Appendix B abbreviates (Heb., Ug., Akk., Ar., Aram.,
    Hurr., Anat., Eg., LB, PS).  These are expanded to the full names the
    paper itself uses in its main text.  No label is invented.

Rows that come from the two summary tables (section 7, p.14 and section 8,
p.16) print no roots and no comparison languages of their own.  For those the
root and languages of the same word's own discussion are carried across, and
the `note` column says so.  Rows for words that get no reading anywhere are
left at root_kind "none".
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, 'reports', 'cycle-02-readings.csv')
DST = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
APPB = os.path.join(HERE, 'data', 'derived', 'appendix_b.json')

# ---------------------------------------------------------------- language labels
LANG = [
    (r'\bHeb\.', 'Hebrew'), (r'\bHebrew\b', 'Hebrew'),
    (r'\bUg\.', 'Ugaritic'), (r'\bUgaritic\b', 'Ugaritic'),
    (r'\bAkk\.', 'Akkadian'), (r'\bAkkadian\b', 'Akkadian'),
    (r'\bAram\.', 'Aramaic'), (r'\bAramaic\b', 'Aramaic'),
    (r'\bAr\.', 'Arabic'), (r'\bArabic\b', 'Arabic'),
    (r'\bHurr\.', 'Hurrian'), (r'\bHurrian\b', 'Hurrian'),
    (r'\bAnat\.', 'Anatolian'),
    (r'\bEg\.', 'Egyptian'), (r'\bEgyptian\b', 'Egyptian'),
    (r'\bLB\b', 'Mycenaean Greek'),
    # "PS" must be followed by a reconstructed form: "PS Za 2" is the site code
    # for Praisos, not a language label.
    (r'\bPS\s*\*', 'Proto-Semitic'), (r'\bProto-Semitic\b', 'Proto-Semitic'),
    (r'\bAmorite\b', 'Amorite'),
    # "pre-Greek" is a statement about substrate, not a comparison language.
    (r'(?<!pre-)\bGreek\b', 'Greek'),
]


def langs_in(text):
    out = []
    for pat, name in LANG:
        if re.search(pat, text) and name not in out:
            out.append(name)
    return sorted(out)


# ---------------------------------------------------------------- Appendix B roots
# every letter the paper uses inside a root, plus the hyphen.  Anything else
# (a space, a comma, a "+", a quotation mark) ends the root.
ROOT_CHARS = r"ʾʿḥḫḏṣṭṯšśġbgdehjklmnpqrstwyz\-"
ROOT_RE = re.compile(r'√([' + ROOT_CHARS + r']+)')


def roots_in(text):
    """Every root printed after a radical sign, in order, de-duplicated.

    The paper glues a following morpheme onto some roots (v'ʾ-r-y+-nit'); the
    regex stops at the '+', so only the root letters are captured.  v'ntk' is
    re-hyphenated.
    """
    out = []
    for r in ROOT_RE.findall(text):
        r = r.strip('-')
        if '-' not in r:                       # v ntk  ->  n-t-k
            r = '-'.join(r)
        if r and r not in out:
            out.append(r)
    return out


# ---------------------------------------------------------------- hand table
# (word, where-prefix): (root, root_kind, languages, note)
# Page numbers in the notes are the pages the entry was read from.
H = {}


def hand(word, where, root, kind, languages, note=''):
    H[(word, where)] = (root, kind, languages, note)


# --- Appendix A, p.36 (the KN Zc 7 table and the AB79 note)
hand('A-KA-NU', 'Appendix A', 'ʾ-g-n', 'from comparison word', 'Aramaic | Hebrew',
     'root copied from the comparandum "Hebrew/Aramaic ʾaggan" (p.36); the paper prints no radical sign here')
hand('ZA-TI', 'Appendix A', '', 'none', 'Proto-Semitic',
     'the paper compares the relative d- to Proto-Semitic t-, a single consonant, not a root')
hand('DU-RA-RE', 'Appendix A', 'd-r-r', 'stated', '')
hand('A-*79-RA', 'Appendix A', '', 'none', '',
     'the paper gives the divine name ʾAthirat but no root and no comparison word')
hand('JA-SA-RA', 'Appendix A', 'y-š-r', 'stated', '')
hand('A-NA-NE', 'Appendix A', 'ḥ-n-n', 'stated', '')
hand('WI-PI', 'Appendix A', '', 'none', '',
     'the paper segments wa- + pi but gives no root and no comparison word')
hand('*79-DU', 'Appendix A (AB79 note)', '', 'none', '',
     'no root and no comparison word at this point; Ugaritic td "breast" is cited in n.28 (p.17) for I-TH-DI-SI-KA')
hand('MA-*79', 'Appendix A (AB79 note)', '', 'none', '')
hand('*79-RI-NI-MA', 'Appendix A (AB79 note)', '', 'none', '',
     'no root here; the Appendix B entry for ZU-RI-NI-MA gives v t-w-r for the parallel form')

# --- Section 4, the formula word by word
hand('A-TA-I-*301-WA-JA', '§4.1',
     'n-w-y', 'stated',
     'Akkadian | Arabic | Geʿez | Greek | Hebrew | Mycenaean Greek | Phoenician | Ugaritic',
     'n.10 (p.5) names v d-w-y as a rejected alternative')
hand('*301-SI', '§4.1 n.10', 'n-ś-ʾ', 'stated', '')
hand('TE-*301', '§4.1 n.10', 't-ʾ-n', 'stated', '')
hand('NA-TU-*301-NE', '§4.1 n.10', 'n-t-n', 'stated', '')
hand('JA-DI-KI-TU', '§4.2', 'd-q-q', 'stated',
     'Arabic | Greek | Hebrew | Mycenaean Greek | Ugaritic')
hand('JA-SA-SA-RA-ME', '§4.3', 'y-š-r', 'stated', 'Akkadian | Amorite | Hebrew',
     'the paper also reports Gordon\'s derivation from v s-l-m and cites v e-s-r for Akkadian Isartu/Misaru (p.8)')
hand('JA-SA-RA', '§4.3', 'y-š-r', 'stated', '',
     'p.8 calls it "the same root ... with a single SA", referring back to v y-s-r')
hand('SA-SA-RA-ME', '§4.3', 'y-š-r', 'stated', '',
     'p.8 gives it as the JA-less Palaikastro form of the same word')
hand('A-SA-SA-RA', '§4.3', 'y-š-r', 'stated', '',
     'p.8 gives it as the JA-less Palaikastro form of the same word')
hand('I-MI-SA-RA', '§4.3', 'e-š-r', 'stated', 'Akkadian',
     'p.8 states v e-s-r for Akkadian Isartu and Misaru in the preceding sentence and places I-MI-SA-RA beside them; it does not write the root against I-MI-SA-RA itself')
hand('TI-NI-TA', '§4.3', 't-n-t', 'from comparison word', 'Phoenician',
     'consonants copied from "the Phoenician Goddess Tinit" (p.8)')
hand('QA-QA-RU', '§4.3 n.13', 'q-q-r', 'from comparison word', '',
     'consonants copied from qaqqaru "ground" (n.13, p.8); the paper does not say which language qaqqaru belongs to')

# --- Section 5
hand('U-NA-KA-NA-SI', '§5.1', 'k-n-s', 'stated',
     'Akkadian | Arabic | Aramaic | Hebrew | Phoenician | Proto-Semitic | Ugaritic',
     'n.16 (p.9) writes the root v k-n-s/s')
hand('U-NA-RU-KA-NA-SI', '§5.1', 'k-n-s', 'stated', 'Akkadian | Hebrew | Ugaritic')
hand('RA-KI-NI-SE', '§5.1', 'k-n-s', 'stated', '',
     'read la-kinniset "for the assembly" in the sentence that states v k-n-s (p.9)')
hand('I-PI-NA-MA', '§5.2', 'p-n-y', 'stated',
     'Akkadian | Arabic | Hebrew | Phoenician | Punic | Ugaritic',
     'p.10 also prints v w-j-h, but explicitly as the root of the Arabic word wajh, not of I-PI-NA-MA')
hand('SI-RU-TE', '§5.3', 'š-r-t', 'stated', 'Hebrew')

# --- Section 6
hand('TA-NA-RA-TE-U-TI-NU', '§6.1', 'r-ṣ-y', 'stated',
     'Akkadian | Amarna Canaanite | Arabic | Berber | Hebrew | Proto-Semitic | Ugaritic')
hand('A-RE-TU-MI', '§6.1', '', 'none', 'Akkadian | Greek | Lydian | Mycenaean Greek',
     'the reading *ʾars-ummi is the paper\'s own; no root is printed at p.12 (cf. v ʾ-r-s at A-RA-TU in Appendix B)')

# --- Section 7 (prose after the translation table)
hand('SI-KI-NE', '§7', 'š-k-n', 'stated', 'Hebrew | Mycenaean Greek',
     'n.22 (p.14) states v s-k-n for sekina "divine indwelling"; the paper reads SI-KI-NE as sikinet in the same passage but does not write the root against it')
hand('TU-ME', '§7', 't-m', 'from comparison word', 'Hebrew',
     'consonants copied from Hebrew tom (Psalm 25:21, p.15)')
hand('TU-ME-I', '§7', 't-m', 'from comparison word', 'Hebrew',
     'consonants copied from Hebrew tom (Psalm 25:21, p.15)')
hand('DU-RA-RE', '§7', 'd-r-r', 'stated', '')
hand('A-TH-RA', '§7', '', 'none', '',
     'the paper gives the divine name ʾAthirat but no root and no comparison word')
hand('JA-SA-RA', '§7', 'y-š-r', 'stated', '',
     'root stated for this word in Appendix A, p.36')

# --- Section 8 prose
hand('TA-NA-I-NA-U-TI-NU', '§8', 'ʿ-n-y', 'stated', 'Hebrew | Ugaritic',
     'p.16 reads the first position as "a verb from the root v ʿ-n-y"')
hand('I-NA-TA', '§8', 'ʿ-n-y', 'stated', 'Akkadian | Amorite | Hebrew | Ugaritic',
     'n.26 (p.16) states the root; n.27 (p.17) adds the Amorite/Akkadian Hanat material')
hand('I-TH-DI-SI-KA', '§8', 'ṯ-d', 'from comparison word', 'Ugaritic',
     'consonants copied from Ugaritic td "breast" (n.28, p.17); the paper prints no radical sign')
hand('O-SU-QA-RE', '§8', '', 'none', 'Egyptian',
     'read as the Egyptian god name Sukar/Sokar (p.17); Coptic Sokar is cited for the later form')
hand('TU-RU-SA', '§8', 't-r-s', 'stated', 'Egyptian')
hand('DU-*314-RE', '§8', 'ḥ-r-r', 'stated', 'Arabic',
     'Arabic dhu is cited for the DU- element, not for the root')
hand('I-DA-A', '§8', '', 'none', 'Akkadian | Greek | Hebrew',
     'n.31 (p.17) compares Semitic *yad, Hebrew yad, Akkadian idu, and Greek daktyloi, but prints no root for I-DA-A')
hand('AU-SI-RE', '§8 n.29', '', 'none', 'Egyptian',
     'read as Osiris; Coptic Ousire is cited')
hand('MA-DI', '§8 n.29', 'm-ʿ-d', 'from comparison word', 'Hebrew',
     'consonants copied from Hebrew moʿed "appointed festival" (n.29, p.17)')
hand('JE-DI', '§8 n.31', 'y-d', 'from comparison word', 'Akkadian | Greek | Hebrew',
     'consonants copied from Hebrew yad "hand" (n.31, p.17); the paper writes the reconstruction as *yad, not as a root')
hand('A-SA-MU-NE', '§8', '', 'none', 'Greek | Phoenician | Punic',
     'read as the god name Ashmun/Eshmun (p.18); n.33 adds the Punic-Greek-Latin trilingual from Sardinia')
hand('A-TA-I-*301-DE-KA', '§8', 'ʿ-n-y', 'stated', 'Hebrew | Ugaritic')
hand('SA-SA-RA-ME', '§8', 'y-š-r', 'stated', '',
     'p.18 gives it as the Palaikastro form of JA-SA-SA-RA-ME with the initial JA dropped')
hand('A-TA-NA', '§8', 'y-t-n', 'stated', 'Greek | Mycenaean Greek | Phoenician')

# --- Section 9
hand('DU-PU₂-RE', '§9', 'd-b-r', 'stated', 'Geʿez | Hebrew | Mycenaean Greek',
     'p.19 writes "v d-b-r\'s versatility"')
hand('A-DI-KI-TE-TE', '§9', 'd-q-q', 'stated', '',
     'root stated for this word in Appendix B, p.36')
hand('*307', '§9', 'd-b-r', 'stated', 'Geʿez | Hebrew',
     'p.19 reads *307 logographically for Semitic dubur, in the sentence that states v d-b-r')
hand('TI-NI-TA', '§9', 't-n-t', 'from comparison word', 'Phoenician',
     'consonants copied from "the Phoenician Goddess Tinit" (p.8)')

# --- Section 10
hand('SU-KI-RI-TE-I-JA', '§10 n.41', '', 'none', '',
     'read as a toponym plus a gentilic ending; no root and no comparison word (n.41, p.21; Appendix B, p.39)')

# words that appear only inside the section 8 cross-site table and are given no
# reading anywhere in the paper
NO_READING = {'SE-KA-NA-SI', 'U-NA-KA-NA', 'SI-RU', 'I'}

# for rows that come from the two summary tables, carry the word's own root
CARRY = {
    'A-TA-I-NA-WA-JA': ('A-TA-I-*301-WA-JA', '§4.1', 'pp.4-6'),
    'A-TA-I-*301-WA-JA': ('A-TA-I-*301-WA-JA', '§4.1', 'pp.4-6'),
    'JA-DI-KI-TU': ('JA-DI-KI-TU', '§4.2', 'pp.6-7'),
    'JA-SA-SA-RA-ME': ('JA-SA-SA-RA-ME', '§4.3', 'pp.7-8'),
    'U-NA-KA-NA-SI': ('U-NA-KA-NA-SI', '§5.1', 'p.9'),
    'I-PI-NA-MA': ('I-PI-NA-MA', '§5.2', 'p.10'),
    'SI-RU-TE': ('SI-RU-TE', '§5.3', 'pp.10-11'),
    'TA-NA-RA-TE-U-TI-NU': ('TA-NA-RA-TE-U-TI-NU', '§6.1', 'pp.12-13'),
    'TA-NA-I-*301-U-TI-NU': ('TA-NA-I-NA-U-TI-NU', '§8', 'p.16'),
    'I-NA-TA': ('I-NA-TA', '§8', 'pp.16-17'),
    'I-*79-DI-SI-KA': ('I-TH-DI-SI-KA', '§8', 'p.17'),
    'O-SU-QA-RE': ('O-SU-QA-RE', '§8', 'p.17'),
    'TU-RU-SA': ('TU-RU-SA', '§8', 'p.17'),
    'DU-*314-RE': ('DU-*314-RE', '§8', 'p.17'),
    'I-DA-A': ('I-DA-A', '§8', 'p.17'),
    'SA-SA-RA-ME': ('SA-SA-RA-ME', '§4.3', 'p.8'),
    'A-DI-KI-TE-TE': ('A-DI-KI-TE-TE', 'Appendix B', 'p.36'),
    'A-TA-I-*301-WA-E': ('A-TA-I-*301-WA-E', 'Appendix B', 'p.37'),
    'U-NA-RU-KA-NA-TI': ('U-NA-RU-KA-NA-TI', 'Appendix B', 'p.40'),
    'I-PI-NA-MI-NA': ('I-PI-NA-MI-NA', 'Appendix B', 'p.38'),
}


# ---------------------------------------------------------------- Appendix B overrides
# Entries that print no radical sign.  Where the entry still supplies a
# comparison word, its consonants are copied, exactly as the cycle 3 brief asks.
# Where the entry instead cross-references another entry that does state a root,
# that root is carried across and the note says so.  Entries that supply neither
# are left at "none".
#
# Four of these comparison words are not Semitic (Hurrian Daku-shenni and
# Kubaba, Egyptian mk.t / pa-y-Rc / rrj).  Their consonant strings are recorded
# because the brief asks for them, but they are not Semitic roots and the
# languages column says which language each came from.
APPB_OVERRIDE = {
    'A-DU-KU-MI-NA': ('ṯ-k-m-n', 'from comparison word', None,
        'consonants copied from Ugaritic Ṯukamuna (ṯkmn); the entry itself calls the word "Unknown"'),
    'A-KU-MI-NA': (None, None, None,
        'the entry reads "Unknown; apparently related to the preceding form" (A-DU-KU-MI-NA) and gives neither a root nor a comparison word'),
    'A-NA-TI-*301-WA-JA': (None, None, None,
        'the entry reads ʿAnati nawaya but prints no root; v ʿ-n-y and v n-w-y are stated elsewhere in the appendix for the two elements'),
    'A-DU-RE-ZA': (None, None, None,
        'the entry says the word is not attested, and gives neither a root nor a comparison word'),
    'DA-I-PI-TA': (None, None, None,
        'the entry calls it a pre-Greek, non-Semitic substrate name and gives no root'),
    'DA-KU-SE-NE': ('d-k-š-n-n', 'from comparison word', None,
        'consonants copied from Hurrian Daku-šenni; Hurrian is not a Semitic language and this is not a Semitic root'),
    'DA-KU-SE-NE-TI': ('d-k-š-n-n', 'from comparison word', None,
        'consonants copied from Hurrian Daku-šenni; Hurrian is not a Semitic language and this is not a Semitic root'),
    'DU-RE-ZA-SE': (None, None, None,
        'the entry compares only the Linear A form DU-RE-ZA and a Proto-Semitic suffix; no root and no comparison word'),
    'I-DA-MA-TE': ('d-m-t', 'stated', None,
        'the entry reads it as prothetic I- before DA-MA-TE; v d-m-t is stated at the DA-MA-TE entry (p.38)'),
    'I-KU-PA₃-NA-TU-NA-TE': ('k-b-b', 'from comparison word', None,
        'consonants copied from Hurrian/Anatolian Kubaba; not a Semitic root'),
    'KU-PA₃-NA-TU': ('k-b-b', 'from comparison word', None,
        'consonants copied from Hurrian/Anatolian Kubaba; not a Semitic root'),
    'MA-KA-I-TA': ('m-k-t', 'from comparison word', None,
        'consonants copied from Egyptian mk.t "protection"; not a Semitic root'),
    'PA-JA-RE': ('p-ꜣ-y-r-ʿ', 'from comparison word', None,
        'consonants copied from Egyptian pꜣ-y-Rʿ "He-of-Re"; not a Semitic root'),
    'PA-RA-NE': ('ʿ-b-r', 'stated', None,
        'the entry reads it as the shortened form of A-PA-RA-NE; v ʿ-b-r is stated at the A-PA-RA-NE entry (p.37)'),
    'RI-RU-MA': ('r-r-j', 'from comparison word', None,
        'consonants copied from Egyptian rrj "pig"; not a Semitic root'),
    'RI-RU-MA-TI': (None, None, None,
        'the entry reads "No viable reading"'),
    'SU-KI-RI-TA': (None, None, None,
        'compared only to the Linear B toponym su-ki-ri-to / Sybrita; no root and no Semitic comparison word'),
    'SU-KI-RI-TE-I-JA': (None, None, None,
        'read as SU-KI-RI-TA plus a gentilic ending; no root and no comparison word'),
    'U-NA-RU-KA-JA-SI': (None, None, None,
        'the entry only cross-references U-NA-RU-KA-NA-SI and U-NA-RU-KA-NA-TI; no root and no comparison word'),
    'U-NA-RU-KA-NA-TI': ('k-n-s', 'stated', None,
        'the entry reads it hunna lu kanasiti; v k-n-s is stated at the U-NA-KA-NA-SI entry (p.40) and at p.9'),
    '*312-TE-TE': ('k-t-n', 'from comparison word', None,
        'consonants copied from Ugaritic ktn "tunic"; v k-t-n is stated at the *312-TA entry (p.40)'),
    'A-TA-I-*301-WA-JA': (None, None, None,
        'the second root in this entry (v n-b-ʾ) is the root of the Hebrew comparison word hitnabbeʾ, not of the Linear A word'),
    # entries that do print a root, but not for the head word itself
    'A-JA': (None, None, None,
        'the radical sign in this entry (v ḥ-y-y) is printed against the comparison form JA-JA, not against A-JA'),
    'KU-PA₃-NU': (None, None, None,
        'the radical sign in this entry (v g-p-n) belongs to the rival Ugaritic reading Gupanu; the entry\'s own preference is Hurrian/Anatolian Kubaba'),
}


def main():
    appb = {e['word']: e['body'] for e in json.load(open(APPB, encoding='utf-8'))}
    appb_cols, appb_notes = {}, {}
    for w, body in appb.items():
        rs = roots_in(body)
        root, kind, lang = (' | '.join(rs), 'stated' if rs else 'none',
                            ' | '.join(langs_in(body)))
        if w in APPB_OVERRIDE:
            o_root, o_kind, o_lang, o_note = APPB_OVERRIDE[w]
            if o_root is not None:
                root = o_root
            if o_kind is not None:
                kind = o_kind
            if o_lang is not None:
                lang = o_lang
            appb_notes[w] = o_note
        appb_cols[w] = (root, kind, lang)

    rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
    out = []
    carried = []
    for r in rows:
        word, where = r['word'], r['where']
        root = kind = languages = ''
        extra = ''

        if where.startswith('Appendix B'):
            root, kind, languages = appb_cols[word]
            extra = appb_notes.get(word, '')
        else:
            key = None
            for (w, wh) in H:
                if w == word and where.startswith(wh):
                    if key is None or len(wh) > len(key[1]):
                        key = (w, wh)
            if key:
                root, kind, languages, extra = H[key]
            elif word in NO_READING:
                root, kind, languages = '', 'none', ''
                extra = 'the paper gives this form no reading anywhere, so no root and no comparison language'
            elif word in CARRY:
                src_word, src_sec, src_pages = CARRY[word]
                if src_sec.startswith('Appendix B'):
                    root, kind, languages = appb_cols[src_word]
                else:
                    root, kind, languages, _ = H[(src_word, src_sec)]
                extra = ('this row is a table cell and prints no root; root and languages '
                         'carried from %s (%s), where the paper discusses %s'
                         % (src_sec, src_pages, src_word))
                carried.append((word, where))
            else:
                sys.exit('unannotated row: %r %r' % (word, where))

        r['root'] = root
        r['root_kind'] = kind
        r['languages'] = languages
        if extra:
            r['note'] = (r['note'] + '; ' if r['note'] else '') + extra
        out.append(r)

    fields = list(rows[0].keys())
    with open(DST, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    print('wrote %s  (%d data rows)' % (os.path.relpath(DST, HERE), len(out)))
    print('rows whose root/languages were carried from a table cell: %d' % len(carried))

    # ---- known answers from the cycle 3 brief
    print('\nKNOWN-ANSWER CHECK (Part A)')
    KNOWN = [('A-TA-I-*301-WA-JA', 'n-w-y', '§4.1'),
             ('JA-DI-KI-TU', 'd-q-q', '§4.2'),
             ('JA-SA-SA-RA-ME', 'y-š-r', '§4.3'),
             ('U-NA-KA-NA-SI', 'k-n-s', '§5.1'),
             ('I-PI-NA-MA', 'p-n-y', '§5.2'),
             ('SI-RU-TE', 'š-r-t', '§5.3'),
             ('TA-NA-RA-TE-U-TI-NU', 'r-ṣ-y', '§6.1')]
    ok = True
    for word, want, sec in KNOWN:
        got = [x['root'] for x in out if x['word'] == word and x['where'].startswith(sec)]
        good = bool(got) and all(g == want for g in got)
        ok &= good
        print('  %-22s %-8s at %-6s -> %-8s %s'
              % (word, want, sec, got[0] if got else '(no row)', 'PASS' if good else 'FAIL'))
    print('  ALL SEVEN PART A KNOWN ANSWERS AS DESCRIBED' if ok
          else '  STOP: a Part A known answer did not come out as described')

    # ---- summary counts
    from collections import Counter
    print('\nroot_kind:', dict(Counter(x['root_kind'] for x in out)))
    lc = Counter()
    for x in out:
        for l in [y.strip() for y in x['languages'].split('|') if y.strip()]:
            lc[l] += 1
    print('rows per comparison language:')
    for l, n in lc.most_common():
        print('  %-18s %3d' % (l, n))
    print('rows with no comparison language: %d'
          % sum(1 for x in out if not x['languages'].strip()))


if __name__ == '__main__':
    main()
