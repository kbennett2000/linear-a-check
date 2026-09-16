#!/usr/bin/env python3
"""Cycle 7, Step 1.  Build four root lists, plus the paper's own stated roots.

  1  Hebrew          cycle 6's list: Strong's primitive roots + final-h-as-y
  2  Hebrew+Ugaritic add the verb roots of the Copenhagen Ugaritic Corpus
  3  made-up roots   same size, lengths and letter mix as Hebrew, no real words
  4  English         consonant skeletons of common English words
  5  paper roots     every root the paper states (Step 3; not a dictionary)

Writes data/derived/cycle7_lists.json.  **None of the lists is committed**: the
Ugaritic lexicon is CC BY-NC 4.0, so neither it nor anything built from it may
be redistributed here.  Running this script rebuilds everything.

Terms.  A *skeleton* is a root written as its consonants only, joined by
hyphens, the same way cycles 3-6 wrote them.  A *lexicon* is a dictionary of a
language.  *Positional letter frequency* means how often each letter turns up
as the first, second, third … letter of a root.
"""
import csv, hashlib, importlib, json, os, random, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')

RAW = os.path.join(HERE, 'data', 'raw')
HEB = os.path.join(HERE, 'data', 'derived', 'hebrew_list.json')
READ = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
OUT = os.path.join(HERE, 'data', 'derived', 'cycle7_lists.json')
SEED = 20260916

DOWNLOADS = {
    'ugaritic_lexicon.txt': (
        'https://raw.githubusercontent.com/DT-UCPH/cuc/main/lexicon_and_grammar/'
        'ugaritic_lexicon.txt',
        168731, 'e6e599bec99fb1e91e3d3282c254585004216ef9890edbe7a8d731cca5984931'),
    'google-10000-english-no-swears.txt': (
        'https://raw.githubusercontent.com/first20hours/google-10000-english/'
        'master/google-10000-english-no-swears.txt',
        75153, 'd6b3e04f1ac30be6525d41474166c0bff28486ecd8c48dcb0ab9c7c9cc05ed86'),
    'cmudict.dict': (
        'https://raw.githubusercontent.com/cmusphinx/cmudict/master/cmudict.dict',
        3618488, '81917843c7f44ce2b094ac63873c2c7a4cf802040792c455ba3ca406891c3d22'),
}

# --------------------------------------------------------------------------
# 1.  Hebrew
# --------------------------------------------------------------------------
def hebrew_list():
    out = set()
    for e in json.load(open(HEB, encoding='utf-8')):
        if e['aramaic'] or not e['primitive_root']:
            continue
        out.add(e['skeleton'])
        if 'skeleton_final_h_as_y' in e:
            out.add(e['skeleton_final_h_as_y'])
    return out


# --------------------------------------------------------------------------
# 2.  Ugaritic verb roots
# --------------------------------------------------------------------------
# Column 1 of the lexicon writes a regular root as /x-y-z/, with ʔ for aleph and
# ʕ for ayin (rewritten below as ʾ and ʿ, the letters the matcher uses).  Roman
# numeral tags marking homonyms -- (I), (II) -- are dropped, as the brief
# directs.  69 verb entries do not fit that pattern.  Each is expanded by hand
# below into the root or roots it names, using the lexicon's own conventions:
#
#   *          a reconstructed form               -> keep the root, drop the star
#   (?)        uncertain                          -> keep the root, drop the mark
#   (-k)       an optional extra radical          -> both the short and the long root
#   x/y        alternative letters in one slot    -> one root for each letter
#   x:y        the same, written with a colon     -> one root for each letter
#   hkr        written unsegmented                -> one root, letter by letter
#   d-k(-k)/   a missing opening or closing slash -> read as if the slash were there
#
UG_HAND = {
    '/ʔ-ḫ-d(/ḏ)/': ['ʔ-ḫ-d', 'ʔ-ḫ-ḏ'],
    '/ʕ-d(-d)/': ['ʕ-d', 'ʕ-d-d'],
    '/ʕ-g-d/ (?)': ['ʕ-g-d'],
    '/ʕ-p(-p)/': ['ʕ-p', 'ʕ-p-p'],
    '/ʕ-s-y:s/ (?)': ['ʕ-s-y', 'ʕ-s-s'],
    '/ʕ-z(-z)/': ['ʕ-z', 'ʕ-z-z'],
    '/b-r(-r)/': ['b-r', 'b-r-r'],
    '/b-t(-t)/': ['b-t', 'b-t-t'],
    'd-k(-k)/': ['d-k', 'd-k-k'],
    '/d-r(-r)/': ['d-r', 'd-r-r'],
    '*/g-h(-h/y)/': ['g-h', 'g-h-h', 'g-h-y'],
    '*/g-p-r/': ['g-p-r'],
    '/g-r(-y)/': ['g-r', 'g-r-y'],
    '/h-b-ṭ/ẓ/': ['h-b-ṭ', 'h-b-ẓ'],
    'hkr': ['h-k-r'],
    '/ḥ-s/ (?)': ['ḥ-s'],
    '/ḥ-w/y-y/ (I)': ['ḥ-w-y', 'ḥ-y-y'],
    '/ḫ-r(-r)/': ['ḫ-r', 'ḫ-r-r'],
    '/ḫ-t(-t)/': ['ḫ-t', 'ḫ-t-t'],
    '/l-ʔ-y/w/ (I)': ['l-ʔ-y', 'l-ʔ-w'],
    '/l-ʔ-y/w/ (II)': ['l-ʔ-y', 'l-ʔ-w'],
    '/l-ḥ(-ḥ)/': ['l-ḥ', 'l-ḥ-ḥ'],
    '/m-ḥ(-w:y)/': ['m-ḥ', 'm-ḥ-w', 'm-ḥ-y'],
    '/m-k-(k)/': ['m-k', 'm-k-k'],
    '/m-r(-r)/ (I)': ['m-r', 'm-r-r'],
    'm-r(-r)/ (II)': ['m-r', 'm-r-r'],
    '/m-s-s(/ś)/': ['m-s-s', 'm-s-ś'],
    '/n-d(-y)/': ['n-d', 'n-d-y'],
    '*/n-ḏ-r/': ['n-ḏ-r'],
    '/n-g(-y)/': ['n-g', 'n-g-y'],
    '/n-ḥ(-y/w)/': ['n-ḥ', 'n-ḥ-y', 'n-ḥ-w'],
    'n-k-m': ['n-k-m'],
    '/n-k-ṯ/(?)': ['n-k-ṯ'],
    '/n-p(-p)/': ['n-p', 'n-p-p'],
    '/n-s:ś-ʕ/ (II)': ['n-s-ʕ', 'n-ś-ʕ'],
    '/n-s(-y)/ (I)': ['n-s', 'n-s-y'],
    '/p-l(-l)/': ['p-l', 'p-l-l'],
    '/p-r(-r)/': ['p-r', 'p-r-r'],
    '*/p-r-s/': ['p-r-s'],
    'prsḥ': ['p-r-s-ḥ'],
    '/p-t(-y)/': ['p-t', 'p-t-y'],
    '*/p-ẓ-ġ/': ['p-ẓ-ġ'],
    '*/q-b-b/': ['q-b-b'],
    '*/q-l-l/': ['q-l-l'],
    '/q-n(-n)/': ['q-n', 'q-n-n'],
    '/q-ṣ(-ṣ)/': ['q-ṣ', 'q-ṣ-ṣ'],
    '*/q-ṭ-n/': ['q-ṭ-n'],
    '/q-ṭ(-ṭ)/': ['q-ṭ', 'q-ṭ-ṭ'],
    '/r-b(-b:y)/': ['r-b', 'r-b-b', 'r-b-y'],
    '/r-k(-k)/': ['r-k', 'r-k-k'],
    '/r-n(-n)/': ['r-n', 'r-n-n'],
    '*/r-q-q/': ['r-q-q'],
    '/r-š(-š)/': ['r-š', 'r-š-š'],
    '/s:ś-b-b/': ['s-b-b', 'ś-b-b'],
    '*/s-k(-k)/': ['s-k', 's-k-k'],
    '*/ṣ/ḍ-b-ṭ/': ['ṣ-b-ṭ', 'ḍ-b-ṭ'],
    '*/ṣ-d-q/': ['ṣ-d-q'],
    '*/ṣ-ḥ-r/': ['ṣ-ḥ-r'],
    '/ṣ-r(-r)/': ['ṣ-r', 'ṣ-r-r'],
    '/š-l(-l)/': ['š-l', 'š-l-l'],
    '*/š-m-ḥ/': ['š-m-ḥ'],
    '/š-r-y/w/': ['š-r-y', 'š-r-w'],
    '/š-t(-t)/': ['š-t', 'š-t-t'],
    '*/t-m(-m)/': ['t-m', 't-m-m'],
    '*/ṯ-q-l/': ['ṯ-q-l'],
    '*/ṯ-r-w/y/': ['ṯ-r-w', 'ṯ-r-y'],
    '/y-h(-y)/': ['y-h', 'y-h-y'],
    '/y/w-ḥ-l/': ['y-ḥ-l', 'w-ḥ-l'],
    '/z-ġ(-y)/': ['z-ġ', 'z-ġ-y'],
}
UG_LETTERS = 'ʔʕbdḏgġhḫḥklmnpqrsśšṣtṯṭwyzẓḍ'
UG_CLEAN = re.compile('^/[%s]+(?:-[%s]+)*/$' % (UG_LETTERS, UG_LETTERS))
TO_MATCHER = str.maketrans({'ʔ': 'ʾ', 'ʕ': 'ʿ'})


def ugaritic_roots():
    text = open(os.path.join(RAW, 'ugaritic_lexicon.txt'), encoding='utf-8').read()
    lines = [l for l in text.split('\n') if l and not l.startswith('#')]
    n_entries = len(lines)
    vb = [l.split('\t')[0].strip() for l in lines
          if len(l.split('\t')) > 3 and l.split('\t')[3] == 'vb']
    roots, odd = set(), []
    for s in vb:
        s2 = re.sub(r'\s*\((?:I|II|III|IV|V|VI)\)\s*$', '', s).strip()
        if UG_CLEAN.fullmatch(s2):
            roots.add(s2.strip('/'))
        else:
            odd.append(s)
    unknown = [o for o in odd if o not in UG_HAND]
    for o in odd:
        roots.update(UG_HAND.get(o, []))
    return ({r.translate(TO_MATCHER) for r in roots}, n_entries, len(vb), odd,
            unknown, {r.translate(TO_MATCHER) for r in roots
                      for _ in [0] if True})


# --------------------------------------------------------------------------
# 3.  Made-up roots
# --------------------------------------------------------------------------
def madeup_roots(heb, rng):
    """Same size, same lengths, same letter-by-position mix; no real words."""
    by_pos = defaultdict(Counter)
    for s in heb:
        for i, c in enumerate(s.split('-')):
            by_pos[i][c] += 1
    draw = {i: (list(c), [c[k] for k in c]) for i, c in by_pos.items()}
    out = set()
    for s in sorted(heb):                       # one new root per real one
        n = s.count('-') + 1
        for _ in range(10000):
            new = '-'.join(rng.choices(draw[i][0], weights=draw[i][1], k=1)[0]
                           for i in range(n))
            if new not in heb and new not in out:
                out.add(new)
                break
    return out, by_pos


# --------------------------------------------------------------------------
# 4.  English
# --------------------------------------------------------------------------
# Rough by design.  English sounds are mapped onto the nearest letter the
# matcher knows; f and v have no counterpart at all and are folded onto p and b,
# and the three affricates/fricatives CH, JH, ZH onto š, g and z.
CMU_MAP = {'B': 'b', 'CH': 'š', 'D': 'd', 'DH': 'ḏ', 'F': 'p', 'G': 'g',
           'HH': 'h', 'JH': 'g', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n',
           'NG': 'n', 'P': 'p', 'R': 'r', 'S': 's', 'SH': 'š', 'T': 't',
           'TH': 'ṯ', 'V': 'b', 'W': 'w', 'Y': 'y', 'Z': 'z', 'ZH': 'z',
           'ER': 'r'}


def cmudict():
    first = {}
    for line in open(os.path.join(RAW, 'cmudict.dict'), encoding='utf-8'):
        line = line.split('#')[0].strip()
        if not line:
            continue
        p = line.split()
        w = p[0]
        if '(' in w and w.endswith(')'):        # an alternative pronunciation
            continue
        first.setdefault(w, p[1:])
    return first


def english_skeleton(phones):
    out = []
    for x in phones:
        c = CMU_MAP.get(x.rstrip('012'))
        if c and (not out or out[-1] != c):     # merge identical neighbours
            out.append(c)
    return '-'.join(out)


def english_list(want3, want4, rng):
    first = cmudict()
    words = [w.strip() for w in
             open(os.path.join(RAW, 'google-10000-english-no-swears.txt'),
                  encoding='utf-8') if w.strip()]
    common, seen, missing = [], set(), 0
    for w in words:
        ph = first.get(w)
        if ph is None:
            missing += 1
            continue
        k = english_skeleton(ph)
        if k.count('-') == 2 and k not in seen:
            seen.add(k)
            common.append(k)
    rest3, rest4 = set(), set()
    known = set(words)
    for w, ph in first.items():
        if w in known:
            continue
        k = english_skeleton(ph)
        if k.count('-') == 2 and k not in seen:
            rest3.add(k)
        elif k.count('-') == 3:
            rest4.add(k)
    fill3 = rng.sample(sorted(rest3), want3 - len(common))
    fill4 = rng.sample(sorted(rest4), want4)
    return set(common) | set(fill3) | set(fill4), len(common), missing, len(first)


# --------------------------------------------------------------------------
# 5.  The paper's stated roots
# --------------------------------------------------------------------------
def paper_stated_roots():
    out = set()
    for r in csv.DictReader(open(READ, encoding='utf-8')):
        if r['root_kind'] != 'stated':
            continue
        for x in r['root'].split('|'):
            x = x.strip()
            if x:
                out.add(x)
    return out


def matcher_letters():
    """Every consonant the matcher can put into a skeleton, under the full set."""
    a = M.Alphabet().replace('*319', ('h',), ['R32'])
    out = set(M.THROAT)
    for v in a.values.values():
        out |= set(v)
    out |= set(M.SOUND_MATCH.values())          # ṯ=š etc. can be produced too
    out |= {'s', 'r', 'w', 'n', 'y'}            # R22, R24, N04, N05, R62/R63
    return out


def main():
    print('DOWNLOADS')
    for name, (url, size, sha) in DOWNLOADS.items():
        p = os.path.join(RAW, name)
        b = open(p, 'rb').read()
        got = hashlib.sha256(b).hexdigest()
        print('  %s' % name)
        print('    %s' % url)
        print('    %d bytes (brief said %d: %s), sha256 %s (%s)'
              % (len(b), size, 'MATCH' if len(b) == size else 'DIFFERS', got,
                 'MATCH' if got == sha else 'DIFFERS'))

    rng_roots = random.Random(SEED)
    rng_eng = random.Random(SEED)

    # ---- 1 Hebrew
    heb = hebrew_list()
    lens = Counter(s.count('-') + 1 for s in heb)
    print('\n1. HEBREW  (Strong\'s primitive roots + final-h-as-y forms)')
    print('   distinct skeletons: %d   expected 1501  %s'
          % (len(heb), 'PASS' if len(heb) == 1501 else 'DIFFERS'))
    print('   by length: %s   expected 3->1498, 4->3  %s'
          % (dict(sorted(lens.items())),
             'PASS' if lens[3] == 1498 and lens[4] == 3 else 'DIFFERS'))

    # ---- 2 Hebrew + Ugaritic
    ug, n_entries, n_vb, odd, unknown, _ = ugaritic_roots()
    print('\n2. HEBREW + UGARITIC  (Copenhagen Ugaritic Corpus verb roots)')
    print('   lexicon entries: %d   expected 4996  %s'
          % (n_entries, 'PASS' if n_entries == 4996 else 'DIFFERS'))
    print('   entries marked "vb": %d   expected 570  %s'
          % (n_vb, 'PASS' if n_vb == 570 else 'DIFFERS'))
    print('   entries already in plain /x-y-z/ form: %d' % (n_vb - len(odd)))
    print('   entries needing hand treatment: %d  (all covered: %s)'
          % (len(odd), 'yes' if not unknown else 'NO -- %s' % unknown))
    print('   distinct Ugaritic verb roots: %d' % len(ug))
    ul = Counter(r.count('-') + 1 for r in ug)
    print('   by length: %s' % dict(sorted(ul.items())))
    for k, want in (('y-t-n', True), ('p-n-y', True),
                    ('n-w-y', False), ('k-n-s', False)):
        got = k in ug
        print('   %-6s expected %-7s got %-7s %s'
              % (k, 'in list' if want else 'absent', 'in list' if got else 'absent',
                 'PASS' if got == want else 'FAIL'))
    heb_ug = heb | ug
    print('   Ugaritic roots already in the Hebrew list: %d' % len(heb & ug))
    print('   combined list: %d skeletons' % len(heb_ug))

    print('\n   THE %d HAND-EXPANDED ENTRIES' % len(odd))
    for o in sorted(odd):
        print('     %-22s -> %s' % (o, ', '.join(UG_HAND[o])))

    # ---- 3 made-up roots
    made, by_pos = madeup_roots(heb, rng_roots)
    ml = Counter(s.count('-') + 1 for s in made)
    print('\n3. MADE-UP ROOTS  (seed %d)' % SEED)
    print('   skeletons: %d   by length: %s' % (len(made), dict(sorted(ml.items()))))
    print('   overlap with the real Hebrew list: %d  %s'
          % (len(made & heb), 'PASS' if not (made & heb) else 'FAIL'))
    print('   letter mix, position 1, top 8 (real vs made-up):')
    r1 = Counter(s.split('-')[0] for s in heb)
    m1 = Counter(s.split('-')[0] for s in made)
    for c, n in r1.most_common(8):
        print('     %-3s real %4d (%4.1f%%)   made-up %4d (%4.1f%%)'
              % (c, n, 100 * n / len(heb), m1[c], 100 * m1[c] / len(made)))

    # ---- 4 English
    eng, n_common, missing, n_cmu = english_list(lens[3], lens[4], rng_eng)
    el = Counter(s.count('-') + 1 for s in eng)
    print('\n4. ENGLISH  (google-10000 + CMU Pronouncing Dictionary)')
    print('   CMU head words: %d' % n_cmu)
    print('   English words not in the CMU dictionary: %d' % missing)
    print('   distinct 3-letter skeletons from the common words: %d   '
          'expected 1041  %s' % (n_common, 'PASS' if n_common == 1041 else 'DIFFERS'))
    print('   filled from the rest of the CMU dictionary: %d three-letter, '
          '%d four-letter' % (lens[3] - n_common, lens[4]))
    print('   skeletons: %d   by length: %s' % (len(eng), dict(sorted(el.items()))))
    print('   overlap with the Hebrew list: %d' % len(eng & heb))
    throat = set('ʾʿhḥ')
    for nm, L in (('Hebrew', heb), ('English', eng)):
        n = sum(1 for s in L if throat & set(s.split('-')))
        print('   %-8s skeletons containing a throat consonant (ʾ ʿ h ḥ): '
              '%4d of %4d  (%.1f%%)' % (nm, n, len(L), 100 * n / len(L)))
    print('   English can never produce ʾ, ʿ or ḥ at all: the CMU sound set has '
          'no counterpart for them.')

    # ---- 5 the paper's stated roots
    paper = paper_stated_roots()
    can = matcher_letters()
    bad = sorted(r for r in paper if set(r.split('-')) - can)
    pl = Counter(r.count('-') + 1 for r in paper)
    print('\n5. THE PAPER\'S STATED ROOTS  (root_kind "stated")')
    print('   distinct roots: %d   by length: %s' % (len(paper), dict(sorted(pl.items()))))
    print('   roots using a letter the matcher can never produce: %d' % len(bad))
    for r in bad:
        print('     %-12s unusable letters: %s'
              % (r, ' '.join(sorted(set(r.split('-')) - can))))
    print('   These are kept in the list but can never match.  They are left in '
          'so the\n   denominator is the paper\'s own root inventory, not a '
          'filtered version of it.')

    json.dump({'seed': SEED, 'hebrew': sorted(heb), 'hebrew_ugaritic': sorted(heb_ug),
               'made_up': sorted(made), 'english': sorted(eng),
               'paper_stated': sorted(paper), 'paper_unusable': bad,
               'ugaritic_only': sorted(ug)},
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('\nwrote %s  (not committed: the Ugaritic lexicon is CC BY-NC 4.0)'
          % os.path.relpath(OUT, HERE))


if __name__ == '__main__':
    main()
