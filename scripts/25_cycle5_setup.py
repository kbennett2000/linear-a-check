#!/usr/bin/env python3
"""Cycle 5, shared setup.

Builds three things the cycle 5 scripts need, and prints them when run directly:

  * the word pool  - every distinct hyphenated word in the corpus that the
                     matcher can read, with how often it occurs and which sites
                     it is found at
  * the two rule sets - "full" and "stated only"
  * the sign counts - how many words of the pool contain each ordinary
                     syllable sign

Terms.  A *rule set* here is a pair: which rule switches are on, and what each
sign may stand for.  A *site* is the place an inscription was excavated; the
corpus records one per inscription.
"""
import csv, importlib, json, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')

INSCR = os.path.join(HERE, 'data', 'derived', 'inscriptions.json')
C3RULES = os.path.join(HERE, 'reports', 'cycle-03-rules.csv')
C4RULES = os.path.join(HERE, 'reports', 'cycle-04-rules-added.csv')

# --------------------------------------------------------------------------
# the two rule sets
# --------------------------------------------------------------------------
# Decision carried in from cycle 4: *319 gets the conditional value R32 gives
# it, because the paper uses it.  R32 is marked "used", so it is in the full
# set only.
STAR319 = ('h',)


def stated_ids():
    ids = set()
    for path in (C3RULES, C4RULES):
        for r in csv.DictReader(open(path, encoding='utf-8')):
            if r['stated_or_used'] == 'stated':
                ids.add(r['rule_id'])
    return ids


def rule_sets():
    """-> {'full': (on, alphabet), 'stated only': (on, alphabet)}"""
    stated = stated_ids()

    # ---- full: everything, plus R63 (Zakros) and *319 = /hū/
    full_alpha = M.Alphabet().replace('*319', STAR319, ['R32'])
    full_on = M.CYCLE5_ON | {'R32'}

    # ---- stated only
    # Every rule switch the matcher knows about, kept only if it is marked
    # "stated".  R01 and R02 are the base facts (Linear B values; every sign
    # writes an open syllable) and stay in both sets, as does the TH switch,
    # which is not a rule but the handle cycle 4 used for the ṯ ablation.
    keep = {r for r in M.CYCLE5_ON if r in stated} | {'R01', 'R02', 'AFFIX', 'TH'}
    st_on = frozenset(keep)

    # The sign table under the stated-only set.  R05 is stated and its `allows`
    # column names the P-, T- and K-series explicitly, so those keep their sets.
    # R06 (sibilants), R09 (l/r), R11 (T also writes ṣ and ṯ), R25, R27, R29 and
    # R30 are stated too.  The Q-series and the Z-series have no stated rule of
    # their own -- R14 and R16 are both marked "used" -- so, as the cycle 5
    # brief directs, they fall back to their plain Linear B value.  This is a
    # choice the paper does not settle and it is written up in reports/cycle-05.md.
    vals, rules = {}, {}

    def put(names, sounds, rs):
        for nm in names:
            vals[nm] = tuple(sounds)
            rules[nm] = frozenset(rs)

    put(['PA', 'PE', 'PI', 'PO', 'PU', 'PA₃', 'PU₂'], ('p', 'b'), ['R05'])
    put(['TA', 'TE', 'TI', 'TO', 'TU', 'TA₂', 'TWE'],
        ('t', 'd', 'ṭ', 'ṣ', 'ṯ'), ['R05', 'R11'])
    put(['DA', 'DE', 'DI', 'DO', 'DU'], ('d', 't', 'ṭ'), ['R05'])
    put(['KA', 'KE', 'KI', 'KO', 'KU'], ('k', 'g', 'q'), ['R05'])
    put(['QA', 'QE', 'QI', 'QA₂'], ('q',), ['R01'])          # no stated rule
    put(['SA', 'SE', 'SI', 'SO', 'SU'], ('š', 's', 'ṣ', 'ś'), ['R06'])
    put(['ZA', 'ZE', 'ZO'], ('z',), ['R01'])                 # no stated rule
    put(['RA', 'RE', 'RI', 'RO', 'RU', 'RA₂'], ('r', 'l'), ['R09'])
    put(['MA', 'ME', 'MI', 'MO', 'MU'], ('m',), ['R01'])
    put(['NA', 'NE', 'NI', 'NO', 'NU', 'NWA'], ('n',), ['R01'])
    put(['WA', 'WE', 'WI', 'WO'], ('w',), ['R01'])
    put(['JA', 'JE', 'JO', 'JU'], ('y',), ['R01'])
    put(['ZU', '*79', 'TH', 'AB79'], ('ṯ',), ['R27'])
    put(['*301'], ('n',), ['R25'])
    put(['*314'], ('ḥ',), ['R29'])
    # *319 is left out: R32 is marked "used"
    st_alpha = M.Alphabet(vals, rules, M.VOWEL_SIGNS)

    return {'full': (full_on, full_alpha), 'stated only': (st_on, st_alpha)}


# --------------------------------------------------------------------------
# the word pool
# --------------------------------------------------------------------------
def word_pool(alpha):
    """Distinct hyphenated corpus words the matcher can read.

    -> {word: {'n': occurrences, 'sites': set}}, plus a dict of what was left
    out and why.
    """
    d = json.load(open(INSCR, encoding='utf-8'))
    count = Counter()
    sites = defaultdict(set)
    for e in d.values():
        for w in (e.get('transliteratedWords') or []):
            if isinstance(w, str) and '-' in w:
                count[w] += 1
                sites[w].add(e.get('site') or '')
    keep, dropped = {}, {}
    for w, n in count.items():
        signs = M.word_signs(w)
        if any('+' in s for s in signs):
            dropped[w] = 'contains a combined sign written with +'
            continue
        bad = M.unmatchable_signs(signs, alpha)
        if bad:
            dropped[w] = 'contains %s, which the matcher cannot read' % ', '.join(
                sorted(set(bad)))
            continue
        keep[w] = {'n': n, 'sites': {s for s in sites[w] if s}}
    return keep, dropped, count


def sign_counts(pool):
    c = Counter()
    for w in pool:
        for s in set(M.word_signs(w)):
            c[s] += 1
    return c


# plain vowels, AB79/ZU and numbered signs are left out of the Step 3 choice
SKIP_FOR_STEP3 = set(M.VOWEL_SIGNS) | {'ZU', '*79', 'TH', 'AB79'}


def ordinary_signs(counts):
    return {s: n for s, n in counts.items()
            if s not in SKIP_FOR_STEP3 and not s.startswith('*')}


def main():
    sets = rule_sets()
    full_on, full_alpha = sets['full']
    st_on, st_alpha = sets['stated only']

    print('RULE SETS')
    print('  full:        %d switches on' % len(full_on))
    print('  stated only: %d switches on' % len(st_on))
    print('  switches dropped by "stated only": %s'
          % ' '.join(sorted(full_on - st_on)))
    print('\n  sign table, the two sets side by side')
    print('  %-8s %-24s %s' % ('signs', 'full', 'stated only'))
    for names, vals, _r in M.SERIES:
        a = ' '.join(full_alpha.values.get(names[0], ()))
        b = ' '.join(st_alpha.values.get(names[0], ())) or '(cannot be read)'
        mark = '   <-- differs' if a != b else ''
        print('  %-8s %-24s %s%s' % (names[0] + '…', a, b, mark))
    print('  %-8s %-24s %s' % ('*319', ' '.join(STAR319), '(cannot be read)'))

    pool, dropped, count = word_pool(full_alpha)
    print('\nWORD POOL (full rule set)')
    print('  distinct hyphenated words in the corpus: %d' % len(count))
    print('  the matcher can read:                    %d' % len(pool))
    print('  left out:                                %d' % len(dropped))
    why = Counter(v.split(',')[0] for v in dropped.values())
    for k, n in why.most_common(4):
        print('    %-52s %d' % (k[:52], n))

    counts = sign_counts(pool)
    print('\n*301 appears in %d words of the pool' % counts.get('*301', 0))
    ords = ordinary_signs(counts)
    target = counts.get('*301', 0)
    near = sorted(ords.items(), key=lambda kv: (abs(kv[1] - target), -kv[1], kv[0]))
    print('ordinary syllable signs closest to that count:')
    for s, n in near[:8]:
        print('  %-5s %3d words' % (s, n))


if __name__ == '__main__':
    main()
