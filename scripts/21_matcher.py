#!/usr/bin/env python3
"""Cycle 4.  The matcher.

Given a Linear A word as a list of signs, list every Hebrew root the word could
match under the rules in reports/cycle-03-rules.csv, and for each match, the
rules it used.

Only rules from that table are applied, going by the `allows` column.  Nothing
is added that the table does not have.  Run this file directly to see the sign
table and the Step 1 tests:

    ./venv/bin/python scripts/21_matcher.py

Terms.  A *root* is the set of consonants a Semitic word family is built on.  A
*skeleton* is a Hebrew dictionary word with its vowel marks stripped out, which
is how cycle 3 stored Strong's.  A *prefix* is a piece added to the front of a
word, a *suffix* a piece added to the end.  A *throat consonant* (linguists say
laryngeal or pharyngeal) is one of ʾ ʿ h ḥ.  A *stop* is a consonant made by
closing the mouth completely: p b t d ṭ k g q.
"""
import json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEB = os.path.join(HERE, 'data', 'derived', 'hebrew_list.json')

# --------------------------------------------------------------------------
# 1.  What each sign can stand for
# --------------------------------------------------------------------------
# Every entry below cites the rule in reports/cycle-03-rules.csv that allows it.
# R01 (Linear B sound values) underlies all of them and is not repeated.

THROAT = ('ʾ', 'ʿ', 'h', 'ḥ')
STOPS = set('pbtdk g q'.replace(' ', '')) | {'ṭ'}

VOWEL_SIGNS = {'A', 'E', 'I', 'O', 'U', 'AU'}

SERIES = [
    (['PA', 'PE', 'PI', 'PO', 'PU', 'PA₃', 'PU₂'], ('p', 'b'), ('R05', 'R15')),
    (['TA', 'TE', 'TI', 'TO', 'TU', 'TA₂'], ('t', 'd', 'ṭ', 'ṣ', 'ṯ'), ('R05', 'R11')),
    (['DA', 'DE', 'DI', 'DO', 'DU'], ('d', 't', 'ṭ'), ('R05', 'R12')),
    (['KA', 'KE', 'KI', 'KO', 'KU'], ('k', 'g', 'q', 'ḫ'), ('R05', 'R13')),
    (['QA', 'QE', 'QI', 'QA₂'], ('q', 'k', 'g'), ('R05', 'R14')),
    (['SA', 'SE', 'SI', 'SO', 'SU'], ('š', 's', 'ṣ', 'ś'), ('R06',)),
    (['ZA', 'ZE', 'ZO'], ('ḏ', 'ṯ'), ('R16',)),
    (['RA', 'RE', 'RI', 'RO', 'RU', 'RA₂'], ('r', 'l'), ('R09',)),
    (['MA', 'ME', 'MI', 'MO', 'MU'], ('m',), ('R01',)),
    (['NA', 'NE', 'NI', 'NO', 'NU'], ('n',), ('R01',)),
    (['WA', 'WE', 'WI', 'WO'], ('w',), ('R01',)),
    (['JA', 'JE', 'JO', 'JU'], ('y',), ('R01',)),
    # AB79.  The corpus transcribes this sign ZU; the paper writes it *79 or TH.
    (['ZU', '*79', 'TH', 'AB79'], ('ṯ',), ('R27',)),
    (['*301'], ('n',), ('R25',)),
    (['*314'], ('ḥ',), ('R29',)),
    # two-consonant signs, from their Linear B values, fitted to the lists above
    (['NWA'], ('n',), ('R01',)),
    (['TWE'], ('t', 'd', 'ṭ', 'ṣ', 'ṯ'), ('R05', 'R11')),
]

VALUES, VALUE_RULES = {}, {}
for names, vals, rules in SERIES:
    for nm in names:
        VALUES[nm] = vals
        VALUE_RULES[nm] = frozenset(rules)

# Signs whose transcription carries a small number, and the two-consonant signs.
# The paper gives no general rule for these, so each was settled one at a time
# and written down here.
SIGN_NOTES = {
    'PA₃': 'AB56.  Put in the P-series (p, b).  The paper reads KU-PA₃-NU as '
           'Kubaba + -ānu and KU-PA₃-PA₃ as Kubaba itself (p.38), so it uses '
           'PA₃ for /ba/.',
    'PU₂': 'AB29.  Put in the P-series (p, b).  The paper writes "DU-PU₂-RE, or '
           'DU-BU-RE, as Davis correctly renders it" (p.19), so it uses PU₂ for '
           '/bu/.',
    'RA₂': 'Linear B ra₂ is /rya/.  Only the r is kept, so RA₂ sits in the '
           'R-series (r, l).  The y is dropped rather than invented as a second '
           'consonant, because no rule in the table licenses one sign giving two '
           'different consonants.  Does not occur in any word tested.',
    'TA₂': 'Linear B ta₂ is /tya/.  Only the t is kept, so TA₂ sits in the '
           'T-series.  Same reasoning as RA₂.  Does not occur in any word tested.',
    'QA₂': 'Put in the Q-series (q, k, g).  Does not occur in any word tested.',
    'NWA': 'A two-consonant sign, Linear B nwa.  Only the n is kept, for the same '
           'reason as RA₂.  Does not occur in any word tested.',
    'TWE': 'A two-consonant sign, Linear B twe.  Only the t is kept, so TWE sits '
           'in the T-series.  Does not occur in any word tested.',
    'AU': 'AB85, which R30 calls a two-vowel sign.  Treated as a plain vowel '
          'sign: no consonant, or one throat consonant.',
    'ZU': 'AB79.  The corpus transcribes AB79 as ZU, so ZU is read ṯ (R27), not '
          'as a member of the Z-series.  The paper writes the same sign *79 or TH.',
}

# Signs that carry no sound value the rules give: other starred numbers, word
# signs (logograms), numbers and fractions.  A word containing one is skipped.
UNMATCHABLE_NOTE = ('no sound value in the rules table: other starred sign '
                    'numbers, word signs, numbers and fractions')


class Alphabet:
    """What each sign may stand for, for one run of the matcher.

    Cycle 5 needs to hand a sign a different sound from the one the rules give
    it, so the sign table is bundled here instead of being read straight off the
    module globals.  Built with no arguments it is exactly the table cycle 4
    used, so nothing older changes.
    """

    def __init__(self, values=None, value_rules=None, vowels=None):
        self.values = dict(VALUES) if values is None else dict(values)
        self.rules = dict(VALUE_RULES) if value_rules is None else dict(value_rules)
        self.vowels = set(VOWEL_SIGNS) if vowels is None else set(vowels)
        self.stop_signs = {nm for nm, v in self.values.items()
                           if any(x in STOPS for x in v)}

    def kind(self, s):
        if s in self.vowels:
            return 'vowel'
        if s in self.values:
            return 'consonant'
        return 'unmatchable'

    def vals(self, sign, on):
        """The sounds a sign may stand for, under the rules switched on.

        Switching off 'TH' is the "ways of writing ṯ" ablation of cycle 4's
        Step 3: it takes ṯ out of the T-series (R11) and the Z-series (R16),
        and leaves AB79 (R27) with no value at all.
        """
        v = self.values[sign]
        if 'TH' not in on:
            v = tuple(x for x in v if x != 'ṯ')
        return v

    def replace(self, sign, sounds, rules, as_vowel=False):
        """A copy with one sign given a different value."""
        a = Alphabet(self.values, self.rules, self.vowels)
        a.vowels.discard(sign)
        a.values.pop(sign, None)
        a.rules.pop(sign, None)
        if as_vowel:
            a.vowels.add(sign)
        elif sounds:
            a.values[sign] = tuple(sounds)
            a.rules[sign] = frozenset(rules)
        a.stop_signs = {nm for nm, v in a.values.items()
                        if any(x in STOPS for x in v)}
        return a


_DEFAULT_ALPHA = None


def default_alphabet():
    global _DEFAULT_ALPHA
    if _DEFAULT_ALPHA is None:
        _DEFAULT_ALPHA = Alphabet()
    return _DEFAULT_ALPHA


def sign_kind(s, alpha=None):
    return (alpha or default_alphabet()).kind(s)


def word_signs(word):
    return [p for p in word.split('-') if p]


def unmatchable_signs(signs, alpha=None):
    a = alpha or default_alphabet()
    return [s for s in signs if a.kind(s) == 'unmatchable']


# --------------------------------------------------------------------------
# 2.  Word pieces (prefixes and suffixes), R37-R61
# --------------------------------------------------------------------------
PREFIXES = [
    (('TA', 'NA'), 'R40'), (('U', 'NA'), 'R42'),
    (('A',), 'R37'), (('JA',), 'R38'), (('TA',), 'R39'), (('I',), 'R41'),
    (('WI',), 'R43'), (('RA',), 'R44'), (('O',), 'R45'), (('DU',), 'R46'),
    (('RU',), 'N03'),                      # added in cycle 4, see below
]
SUFFIXES = [
    (('TE', 'I', 'JA'), 'R60'), (('SI', 'JA', 'SE'), 'R56'),
    (('DE', 'KA'), 'R55'), (('NI', 'TA'), 'R59'),
    (('ME',), 'R47'), (('MA',), 'R47'), (('JA',), 'R48'), (('TI',), 'R49'),
    (('NU',), 'R50'), (('NI',), 'R51'), (('TE',), 'R52'), (('NA',), 'R53'),
    (('KA',), 'R54'), (('SE',), 'R56'), (('A',), 'R57'), (('I',), 'R58'),
    (('TU',), 'N01'), (('TA',), 'N02'),    # added in cycle 4, see below
]

# --------------------------------------------------------------------------
# 2b.  Rules added in cycle 4, each tied to a passage in the paper.
#      The full text, page and quote are in reports/cycle-04-rules-added.csv.
# --------------------------------------------------------------------------
ADDED = {
    'N01': '-TU is the feminine nominal ending (stated, §4.2 p.6)',
    'N02': '-TA writes a feminine -at / -āt (used, §8 p.16; Appendix B p.38)',
    'N03': 'RU may be taken out as the particle lū (stated, §5.1 p.9)',
    'N04': 'the middle w of a three-letter root may go unwritten (used, '
           'Appendix B pp.38-40)',
    'N05': 'a root-initial n may go unwritten when it assimilates into a '
           'following doubled sign (used, Appendix B p.40)',
    'N06': 'a U sign may write the root consonant w (used, Appendix B p.39)',
    'N07': 'a word may be a compound of two Semitic words, each with its own '
           'root (used, Appendix B pp.37-38)',
}

# signs that write a stop, so R22 can tell when an unwritten /s/ stands
# "before a stop"
STOP_SIGNS = {nm for nm, vals in VALUES.items() if any(v in STOPS for v in vals)}
# R61 lets an indicative U sit inside a verb.  It is handled as a removable
# middle piece; see the note printed at the bottom of this file.
MAX_PREFIX_CHAIN = 3      # A- + TA- + I- in A-TA-I-*301-WA-JA (§4.1, p.4)
MAX_SUFFIX_CHAIN = 2      # -TI + -NU in TA-NA-RA-TE-U-TI-NU (§6.1, p.12)


def splits(signs, use_affixes=True, max_pre=None, max_suf=None, on=None):
    """Every way of taking pieces off the two ends (and one middle U).

    Returns a list of (remaining signs tuple, following sign or None,
    frozenset of rules, description).  `following` is the first sign of the
    ending that was taken off, which R22 needs.
    """
    max_pre = MAX_PREFIX_CHAIN if max_pre is None else max_pre
    max_suf = MAX_SUFFIX_CHAIN if max_suf is None else max_suf
    on = DEFAULT_ON if on is None else on
    pre_list = [(p, r) for p, r in PREFIXES if r in on]
    suf_list = [(p, r) for p, r in SUFFIXES if r in on]
    if not use_affixes:
        return [(tuple(signs), None, frozenset(), '')]

    out = {}

    def add(rest, following, rules, names):
        key = (tuple(rest), following)
        if not key[0]:
            return
        desc = ' + '.join(names) if names else '(nothing)'
        cur = out.get(key)
        if cur is None or len(rules) < len(cur[0]):
            out[key] = (rules, desc)

    def strip_pre(rest, following, n, rules, names):
        add(rest, following, rules, names)
        if n >= max_pre:
            return
        for piece, rid in pre_list:
            k = len(piece)
            if len(rest) > k and tuple(rest[:k]) == piece:
                strip_pre(rest[k:], following, n + 1, rules | {rid},
                          names + ['-'.join(piece) + '- (%s)' % rid])

    def strip_suf(rest, following, n, rules, names):
        yield rest, following, rules, names
        if n >= max_suf:
            return
        for piece, rid in suf_list:
            k = len(piece)
            if len(rest) > k and tuple(rest[-k:]) == piece:
                yield from strip_suf(rest[:-k], piece[0], n + 1, rules | {rid},
                                     names + ['-' + '-'.join(piece) + ' (%s)' % rid])

    for rest, following, rules, names in strip_suf(list(signs), None, 0,
                                                  frozenset(), []):
        strip_pre(list(rest), following, 0, rules, list(names))
        # R61: an indicative U inside the word
        for i in range(1, len(rest) - 1) if 'R61' in on else []:
            if rest[i] == 'U':
                mid = list(rest[:i]) + list(rest[i + 1:])
                strip_pre(mid, following, 0, rules | {'R61'},
                          list(names) + ['middle U (R61)'])
    return [(k[0], k[1], v[0], v[1]) for k, v in out.items()]


# --------------------------------------------------------------------------
# 3.  The Hebrew side
# --------------------------------------------------------------------------
# The four standard matches between the older Semitic spelling the paper uses
# and Hebrew spelling.  Recorded in cycle 3; not from the paper.
SOUND_MATCH = {'ṯ': 'š', 'ḏ': 'z', 'ḫ': 'ḥ', 'ġ': 'ʿ'}


def hebrew_forms(c):
    """Hebrew letters a generated consonant c may match, with a flag."""
    out = [(c, None)]
    if c in SOUND_MATCH:
        out.append((SOUND_MATCH[c], '%s=%s' % (c, SOUND_MATCH[c])))
    return out


class Trie:
    __slots__ = ('kids', 'ends', 'depth', 'dists')

    def __init__(self, depth=0):
        self.kids = {}
        self.ends = []
        self.depth = depth        # how many root letters have been taken so far
        self.dists = set()        # how many letters still to come, to any end

    def add(self, skeleton, payload):
        n = self
        for ch in skeleton.split('-'):
            n = n.kids.setdefault(ch, Trie(n.depth + 1))
        n.ends.append((skeleton, payload))

    def finish(self):
        d = {0} if self.ends else set()
        for k in self.kids.values():
            k.finish()
            d |= {x + 1 for x in k.dists}
        self.dists = d

    def has_stop_child(self):
        return any(k in STOPS for k in self.kids)


def load_hebrew(which='primitive'):
    """Build the trie.

    which='primitive'  non-Aramaic entries Strong's marks "primitive root",
                       with the final-h-as-y forms included  (the main result)
    which='all'        every non-Aramaic entry                (the secondary one)
    """
    entries = json.load(open(HEB, encoding='utf-8'))
    t = Trie()
    n = 0
    for e in entries:
        if e['aramaic']:
            continue
        if which == 'primitive' and not e['primitive_root']:
            continue
        t.add(e['skeleton'], e)
        n += 1
        if 'skeleton_final_h_as_y' in e:
            t.add(e['skeleton_final_h_as_y'], e)
    t.finish()
    return t, n


# --------------------------------------------------------------------------
# 4.  The match itself
# --------------------------------------------------------------------------
def rank(rules, sound):
    """How much a match leans on the rules.  Lower is simpler.

    Rules added in cycle 4 (the N-numbers) are counted first, so a match that
    needs only cycle 3's rules is always preferred to one that does not.  N07,
    the compound rule, counts double, because it is by far the loosest of them
    and would otherwise crowd out the paper's own analysis of a word.
    """
    weight = sum((2 if r == 'N07' else 1) for r in rules if r.startswith('N'))
    return (weight, len(rules), len(sound), tuple(sorted(rules)))


DEFAULT_ON = frozenset(
    ['R05', 'R06', 'R07', 'R08', 'R09', 'R11', 'R12', 'R13', 'R14', 'R15',
     'R16', 'R17', 'R18', 'R19', 'R21', 'R22', 'R24', 'R25', 'R27', 'R29',
     'R30', 'R62', 'AFFIX', 'TH', 'R61']
    + ['R%d' % i for i in range(37, 61)]          # the word pieces
    + ['N01', 'N02', 'N03', 'N04', 'N05', 'N06', 'N07'])

# the matcher as it stood before cycle 4 added anything
BASELINE_ON = frozenset(r for r in DEFAULT_ON if not r.startswith('N')) - {'R62'}

# Cycle 5 onward.  R63 (the same initial-JA weakening, at Zakros) is only switched
# on once every word being tested has a site to check it against; cycle 4 worked
# from the paper's printed words, which do not all have one.
CYCLE5_ON = DEFAULT_ON | {'R63'}


def match_signs(signs, trie, on=DEFAULT_ON, following=None, alpha=None,
                sites=None):
    """All skeletons the sign run can spell.  -> {skeleton: (entry, rules, sm)}

    `following` is the first sign of whatever was taken off the end, if any.
    R22 needs it to see whether an unwritten /s/ stands before a stop.
    """
    alpha = alpha or default_alphabet()
    signs = tuple(signs)
    n = len(signs)
    memo = {}

    def simpler(a, b):
        return a if rank(a[1], a[2]) <= rank(b[1], b[2]) else b

    def merge(dst, src):
        for sk, val in src.items():
            dst[sk] = simpler(dst[sk], val) if sk in dst else val

    def go(i, node):
        key = (i, id(node))
        if key in memo:
            return memo[key]
        res = {}
        memo[key] = res                      # i+depth strictly increases; no cycles
        if i == n:
            for sk, e in node.ends:
                merge(res, {sk: (e, frozenset(), frozenset())})

        # (a) a root consonant that no sign writes
        for letter, child in node.kids.items():
            rules = None
            if letter in THROAT and 'R07' in on:
                rules = {'R07'} | ({'R21'} if letter == 'ḥ' else set())
            elif letter == 's' and 'R22' in on and (
                    child.has_stop_child()
                    or (i == n and following in alpha.stop_signs)):
                # R22: a syllable-final /s/ is unwritten before a stop.  The
                # stop may be the next root letter, or -- as in
                # U-NA-RU-KA-NA-TI = hunna lu kanasiti -- the first sign of the
                # ending that was taken off.
                rules = {'R22'}
            elif letter == 'r' and 'R24' in on and child.kids:
                rules = {'R24'}
            elif letter == 'y' and node.depth == 0 and (
                    'R62' in on or 'R63' in on):
                # R62: an initial JA- is dropped at Palaikastro.  R63: the same
                # weakening may extend to Zakros.  Cycle 4 applied this without
                # checking the site; from cycle 5 on, `sites` names the sites
                # the word is actually found at, and the rule only fires there.
                # sites=None keeps cycle 4's site-blind behaviour.
                rules = None
                if sites is None:
                    rules = {'R62'} if 'R62' in on else {'R63'}
                elif 'Palaikastro' in sites and 'R62' in on:
                    rules = {'R62'}
                elif 'Zakros' in sites and 'R63' in on:
                    rules = {'R63'}
            elif (letter == 'w' and node.depth == 1 and 1 in child.dists
                  and 'N04' in on):
                rules = {'N04'}
            elif (letter == 'n' and node.depth == 0 and 'N05' in on
                  and i + 1 < n and signs[i] == signs[i + 1]):
                rules = {'N05'}
            if rules is not None:
                sub = go(i, child)
                if sub:
                    merge(res, {sk: (e, rl | rules, sm)
                                for sk, (e, rl, sm) in sub.items()})

        if i < n:
            s = signs[i]
            kind = alpha.kind(s)
            if kind == 'unmatchable':
                pass
            elif kind == 'vowel':
                # gives nothing (R02: the script writes a vowel on every syllable)
                sub = go(i + 1, node)
                if sub:
                    merge(res, {sk: (e, rl | {'R02'}, sm)
                                for sk, (e, rl, sm) in sub.items()})
                # or (N06) the root consonant w, for a U sign
                if s == 'U' and 'N06' in on:
                    child = node.kids.get('w')
                    if child is not None:
                        sub = go(i + 1, child)
                        if sub:
                            merge(res, {sk: (e, rl | {'N06'}, sm)
                                        for sk, (e, rl, sm) in sub.items()})
                # or one throat consonant (R07; R30 for AU)
                if 'R07' in on:
                    extra = {'R07'} | ({'R30'} if s == 'AU' else set())
                    for c in THROAT:
                        child = node.kids.get(c)
                        if child is None:
                            continue
                        sub = go(i + 1, child)
                        if sub:
                            merge(res, {sk: (e, rl | extra, sm)
                                        for sk, (e, rl, sm) in sub.items()})
            else:
                # two identical signs in a row -> one consonant
                if i + 1 < n and signs[i + 1] == s:
                    # R17 is general: a doubled sign may mark one consonant of
                    # that sign's own series.  R18 and R19 name the particular
                    # values SA-SA = š and TE-TE / TI-TI = ṯ, and are cited when
                    # the value is that one.  R17 is not narrowed to exclude the
                    # others, because the paper reads TI-TI as /tt/ in TI-TI-KU
                    # (Appendix B, p.40) -- see reports/cycle-04.md.
                    if 'R17' in on:
                        for c in alpha.vals(s, on):
                            for h, flag in hebrew_forms(c):
                                child = node.kids.get(h)
                                if child is None:
                                    continue
                                sub = go(i + 2, child)
                                if sub:
                                    add_r = alpha.rules[s] | {'R17'}
                                    if s == 'SA' and c == 'š' and 'R18' in on:
                                        add_r = add_r | {'R18'}
                                    if s in ('TE', 'TI') and c == 'ṯ' and 'R19' in on:
                                        add_r = add_r | {'R19'}
                                    add_s = {flag} if flag else set()
                                    merge(res, {sk: (e, rl | add_r, sm | add_s)
                                                for sk, (e, rl, sm) in sub.items()})
                # one sign -> one consonant, or (R08) the same consonant twice
                for c in alpha.vals(s, on):
                    for h, flag in hebrew_forms(c):
                        child = node.kids.get(h)
                        if child is None:
                            continue
                        add_s = {flag} if flag else set()
                        sub = go(i + 1, child)
                        if sub:
                            merge(res, {sk: (e, rl | alpha.rules[s], sm | add_s)
                                        for sk, (e, rl, sm) in sub.items()})
                        if 'R08' in on:
                            gchild = child.kids.get(h)
                            if gchild is not None:
                                sub = go(i + 1, gchild)
                                if sub:
                                    merge(res, {sk: (e, rl | alpha.rules[s] | {'R08'},
                                                     sm | add_s)
                                                for sk, (e, rl, sm) in sub.items()})
        memo[key] = res
        return res

    return go(0, trie)


def match_word(word, trie, on=DEFAULT_ON, alpha=None, sites=None, **kw):
    """Match a whole word.  Returns (results, skipped_reason).

    results: {skeleton: {'entry':…, 'rules':set, 'sound':set, 'removed':str}}
    """
    alpha = alpha or default_alphabet()
    signs = word_signs(word) if isinstance(word, str) else list(word)
    bad = unmatchable_signs(signs, alpha)
    if bad:
        return {}, 'contains %s (%s)' % (', '.join(sorted(set(bad))),
                                         UNMATCHABLE_NOTE)
    use_affixes = 'AFFIX' in on
    out = {}

    def take(sk, e, rules, sm, desc):
        rec = out.get(sk)
        cand = {'entry': e, 'rules': set(rules), 'sound': set(sm),
                'removed': desc}
        if rec is None or rank(cand['rules'], cand['sound']) < rank(
                rec['rules'], rec['sound']):
            out[sk] = cand

    for rest, following, arules, desc in splits(signs, use_affixes=use_affixes,
                                                on=on, **kw):
        for sk, (e, rules, sm) in match_signs(rest, trie, on, following,
                                             alpha, sites).items():
            take(sk, e, set(rules) | set(arules) | {'R01'}, sm, desc)
        # N07: the word may be a compound of two Semitic words, each with its
        # own root.  The root may then be spelled by a run of signs at either
        # end of what is left, with at least one sign over on the other side.
        # Both halves must themselves spell a root.  That is what a compound
        # is, and it is what all four of the paper's compounds look like: in
        # A-MI-DA-O, ʿAmmī is √ʿ-m-m and daʿ is √y-d-ʿ.  Without this, N07
        # would simply let any leftover signs be ignored.
        if 'N07' in on and len(rest) > 1:
            for k in range(1, len(rest)):
                head, tail = rest[:k], rest[k:]
                hm = match_signs(head, trie, on, tail[0], alpha, sites)
                tm = match_signs(tail, trie, on, following, alpha, sites)
                if not hm or not tm:
                    continue
                pre = desc + ' + ' if desc != '(nothing)' else ''
                for sk, (e, rules, sm) in hm.items():
                    take(sk, e, set(rules) | set(arules) | {'R01', 'N07'}, sm,
                         pre + 'first part of a compound (N07)')
                for sk, (e, rules, sm) in tm.items():
                    take(sk, e, set(rules) | set(arules) | {'R01', 'N07'}, sm,
                         pre + 'second part of a compound (N07)')
    return out, None


# --------------------------------------------------------------------------
# 5.  Step 1 tests
# --------------------------------------------------------------------------
def main():
    trie, n = load_hebrew('primitive')
    print('Hebrew side: %d non-Aramaic primitive-root entries, plus their '
          'final-h-as-y forms' % n)

    print('\nSIGN TABLE')
    for names, vals, rules in SERIES:
        print('  %-28s -> %-18s %s'
              % (' '.join(names), ' '.join(vals), ' '.join(rules)))
    print('  %-28s -> %-18s %s'
          % (' '.join(sorted(VOWEL_SIGNS)), 'nothing | ʾ ʿ h ḥ', 'R02 R07 R30'))

    print('\nSIGNS SETTLED ONE AT A TIME')
    for k in sorted(SIGN_NOTES):
        print('  %-5s %s' % (k, SIGN_NOTES[k]))

    print('\nWORD-PIECE CHAINS')
    print('  longest prefix chain allowed: %d  (A- + TA- + I- in '
          'A-TA-I-*301-WA-JA, §4.1 p.4)' % MAX_PREFIX_CHAIN)
    print('  longest suffix chain allowed: %d  (-TI + -NU in '
          'TA-NA-RA-TE-U-TI-NU, §6.1 p.12)' % MAX_SUFFIX_CHAIN)

    print('\nSTEP 1 TESTS')
    ok = True

    def show(word):
        res, skip = match_word(word, trie)
        return res, skip

    # 1. a word with an unmatchable sign
    res, skip = show('A-*118-TA')
    t = (not res) and skip is not None
    ok &= t
    print('  %-24s no matches and skipped                 %s   %s'
          % ('A-*118-TA', 'PASS' if t else 'FAIL', skip))

    # 2. KA-NA-SI = k-n-s with nothing removed
    res, _ = show('KA-NA-SI')
    t = 'k-n-s' in res and res.get('k-n-s', {}).get('removed') == '(nothing)'
    ok &= t
    print('  %-24s k-n-s (%s) with nothing removed        %s'
          % ('KA-NA-SI', res.get('k-n-s', {}).get('entry', {}).get('id', '-'),
             'PASS' if t else 'FAIL'))

    # 3. SI-RU-TE = š-r-t
    res, _ = show('SI-RU-TE')
    t = 'š-r-t' in res and res['š-r-t']['entry']['id'] == 'H8334'
    ok &= t
    print('  %-24s š-r-t (H8334)                          %s'
          % ('SI-RU-TE', 'PASS' if t else 'FAIL'))

    # 4. U-NA-KA-NA-SI = k-n-s with U-NA- removed
    res, _ = show('U-NA-KA-NA-SI')
    rem = res.get('k-n-s', {}).get('removed', '')
    t = 'k-n-s' in res and 'U-NA- (R42)' in rem
    ok &= t
    print('  %-24s k-n-s with U-NA- removed (R42)         %s'
          % ('U-NA-KA-NA-SI', 'PASS' if t else 'FAIL'))

    # 5. DI-KI = d-q-q, and only by letting KI give q-q (R08)
    res, _ = show('DI-KI')
    got = 'd-q-q' in res and res['d-q-q']['entry']['id'] == 'H1854'
    res_no8, _ = match_word('DI-KI', trie, on=DEFAULT_ON - {'R08'})
    t = got and 'd-q-q' not in res_no8
    ok &= t
    print('  %-24s d-q-q (H1854), and gone without R08    %s'
          % ('DI-KI', 'PASS' if t else 'FAIL'))

    # 6. MA-NA-SI does not match k-n-s
    res, _ = show('MA-NA-SI')
    t = 'k-n-s' not in res
    ok &= t
    print('  %-24s does NOT match k-n-s                   %s'
          % ('MA-NA-SI', 'PASS' if t else 'FAIL'))

    print('\n  ALL SIX STEP 1 TESTS PASS' if ok
          else '\n  STOP: a Step 1 test failed')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
