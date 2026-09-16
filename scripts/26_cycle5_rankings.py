#!/usr/bin/env python3
"""Cycle 5, Steps 1-3.  Try every sound in place of *301, and of three signs
whose sounds are already known.

Writes reports/cycle-05-rankings.csv.

"Fit" here only ever means "the word matches at least one Hebrew primitive
root".  The paper's own sense of fit also takes in meaning, which code cannot
judge.  Nothing below is a judgement about meaning.
"""
import csv, importlib, json, os, statistics, sys
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')

OUT = os.path.join(HERE, 'reports', 'cycle-05-rankings.csv')

# every consonant the matcher uses, plus "no consonant" (a plain vowel sign)
CONSONANTS = ['ʾ', 'ʿ', 'h', 'ḥ', 'p', 'b', 't', 'd', 'ṭ', 'ṣ', 'ṯ',
              'k', 'g', 'q', 'ḫ', 'š', 's', 'ś', 'ḏ', 'z', 'r', 'l',
              'm', 'n', 'w', 'y']
VOWEL = '(no consonant)'
CANDIDATES = CONSONANTS + [VOWEL]

# the second view: whole sign groups, with all their options
GROUPS = [
    ('P-series', ('p', 'b')),
    ('T-series', ('t', 'd', 'ṭ', 'ṣ', 'ṯ')),
    ('D-series', ('d', 't', 'ṭ')),
    ('K-series', ('k', 'g', 'q', 'ḫ')),
    ('Q-series', ('q', 'k', 'g')),
    ('S-series', ('š', 's', 'ṣ', 'ś')),
    ('Z-series', ('ḏ', 'ṯ')),
    ('R-series', ('r', 'l')),
    ('M-series', ('m',)),
    ('N-series', ('n',)),
    ('W-series', ('w',)),
    ('J-series', ('y',)),
    ('plain vowel', None),
]

FORMULA = 'A-TA-I-*301-WA-JA'
NWY = ('n-w-y', 'n-w-h')


def run_one(sign, sounds, as_vowel, words, trie, on, alpha):
    """Give `sign` this value and match every word.  -> (coverage, total, median,
    per-word dict)."""
    a = alpha.replace(sign, sounds, ['R25'], as_vowel=as_vowel)
    per = {}
    for w, info in words.items():
        res, skip = M.match_word(w, trie, on=on, alpha=a, sites=info['sites'])
        per[w] = res
    counts = [len(v) for v in per.values()]
    cov = sum(1 for c in counts if c)
    return cov, sum(counts), statistics.median(counts) if counts else 0, per


def ranked(rows):
    """Competition ranking on (coverage, total) descending; ties share a rank."""
    order = sorted(rows, key=lambda r: (-r['coverage'], -r['total_matches']))
    out, prev, rank = [], None, 0
    for i, r in enumerate(order, 1):
        key = (r['coverage'], r['total_matches'])
        if key != prev:
            rank, prev = i, key
        r = dict(r)
        r['rank'] = rank
        out.append(r)
    return out


def test_sign(sign, words, trie, on, alpha, setname, note_formula=False):
    rows = []
    for c in CANDIDATES:
        as_vowel = (c == VOWEL)
        cov, tot, med, per = run_one(sign, None if as_vowel else (c,),
                                     as_vowel, words, trie, on, alpha)
        row = dict(view='single consonant', sign=sign, rule_set=setname,
                   candidate=c, coverage=cov, words_tested=len(words),
                   total_matches=tot, median_per_word=med)
        if note_formula and FORMULA in per:
            res = per[FORMULA]
            row['formula_roots'] = len(res)
            row['formula_has_n_w_y'] = 'yes' if any(k in res for k in NWY) else 'no'
        rows.append(row)
    return ranked(rows)


def test_groups(sign, words, trie, on, alpha, setname):
    rows = []
    for name, sounds in GROUPS:
        as_vowel = sounds is None
        cov, tot, med, _ = run_one(sign, sounds, as_vowel, words, trie, on, alpha)
        rows.append(dict(view='sign group', sign=sign, rule_set=setname,
                         candidate=name, coverage=cov, words_tested=len(words),
                         total_matches=tot, median_per_word=med,
                         options=1 if as_vowel else len(sounds)))
    return ranked(rows)


def show(rows, title, real=None, plain=None, limit=None):
    print('\n%s' % title)
    print('  %-4s %-16s %9s %9s %8s' % ('rank', 'candidate', 'coverage',
                                        'total', 'median'))
    for i, r in enumerate(rows):
        if limit and i >= limit:
            print('  ... %d more' % (len(rows) - limit))
            break
        mark = ''
        if real and r['candidate'] in real:
            mark = '  <-- a real value of this sign'
        if plain and r['candidate'] == plain:
            mark = '  <-- its plain Linear B consonant'
        extra = ''
        if 'formula_roots' in r:
            extra = '   %s: %3d roots, n-w-y %s' % (
                FORMULA, r['formula_roots'], r['formula_has_n_w_y'])
        print('  %-4d %-16s %4d/%-4d %9d %8.0f%s%s'
              % (r['rank'], r['candidate'], r['coverage'], r['words_tested'],
                 r['total_matches'], r['median_per_word'], extra, mark))


def main():
    trie, nheb = M.load_hebrew('primitive')
    sets = S5.rule_sets()
    full_on, full_alpha = sets['full']
    pool, dropped, count = S5.word_pool(full_alpha)
    counts = S5.sign_counts(pool)

    # ---- Step 1
    star = {w: v for w, v in pool.items() if '*301' in M.word_signs(w)}
    print('STEP 1 — the words')
    print('  distinct hyphenated corpus words with *301 as one of their signs, kept: %d'
          % len(star))
    print('  they occur %d times in the corpus' % sum(v['n'] for v in star.values()))
    for w in sorted(star):
        print('    %-46s %2d×  %s' % (w, star[w]['n'],
                                      ', '.join(sorted(star[w]['sites'])) or '(no site)'))
    left = {w: r for w, r in dropped.items() if '*301' in M.word_signs(w)}
    print('  left out, and why:')
    for w in sorted(left):
        print('    %-46s %s' % (w, left[w]))
    print('    %-46s %s' % ('*301 standing alone',
                            'read by the paper as a word sign; this test cannot '
                            'check a word sign'))

    # ---- the paper's own first filter, on p.5
    # "searching for three consonant systems containing waw and yod as their
    # second and third consonants".  How many of the 26 consonants give a real
    # Hebrew root of that shape?
    heb = [e for e in json.load(open(os.path.join(HERE, 'data', 'derived',
                                                  'hebrew_list.json'),
                                     encoding='utf-8'))
           if e['primitive_root'] and not e['aramaic']]
    forms = {}
    for e in heb:
        for k in (e['skeleton'], e.get('skeleton_final_h_as_y')):
            if k:
                forms.setdefault(k, e)
    print('\nTHE PAPER\'S OWN FIRST FILTER (p.5): a root of the shape C-w-y')
    hits = []
    for c in CONSONANTS:
        hc = M.SOUND_MATCH.get(c, c)
        for pat in (hc + '-w-y', hc + '-w-h'):
            if pat in forms:
                hits.append((c, pat, forms[pat]['id'], forms[pat]['gloss']))
                break
    print('  consonants that give one: %d of %d' % (len(hits), len(CONSONANTS)))
    for c, pat, sid, gl in hits:
        print('    %-3s %-8s %-6s %s' % (c, pat, sid, gl[:52]))

    # ---- Step 3 choice of signs
    ords = S5.ordinary_signs(counts)
    target = len(star)
    near = sorted(ords.items(),
                  key=lambda kv: (abs(kv[1] - target), -kv[1], kv[0]))[:3]
    print('\nSTEP 3 — signs with known sounds, chosen by closeness of word count')
    for s, n in near:
        print('  %-5s %3d words (*301 has %d)' % (s, n, target))

    REAL = {'JU': (('y',), 'y'), 'RA₂': (('r', 'l'), 'r'), 'WI': (('w',), 'w'),
            'JE': (('y',), 'y'), 'PA₃': (('p', 'b'), 'p'), 'QA': (('q', 'k', 'g'), 'q'),
            'ME': (('m',), 'm'), 'ZA': (('ḏ', 'ṯ'), 'z'), 'QE': (('q', 'k', 'g'), 'q')}

    allrows = []
    for setname in ('full', 'stated only'):
        on, alpha = sets[setname]
        print('\n' + '=' * 72)
        print('RULE SET: %s' % setname.upper())
        print('=' * 72)

        rows = test_sign('*301', star, trie, on, alpha, setname, note_formula=True)
        allrows += rows
        show(rows, 'STEP 2, main view — one consonant at a time, in place of *301',
             real=('n',))
        nrow = next(r for r in rows if r['candidate'] == 'n')
        tied = [r['candidate'] for r in rows if r['rank'] == nrow['rank']]
        print('\n  "na" is candidate n: rank %d of %d, %s'
              % (nrow['rank'], len(rows),
                 'alone at that rank' if len(tied) == 1
                 else 'tied with ' + ', '.join(c for c in tied if c != 'n')))
        print('  candidates ranked above n: %d'
              % sum(1 for r in rows if r['rank'] < nrow['rank']))

        grows = test_groups('*301', star, trie, on, alpha, setname)
        allrows += grows
        show(grows, 'STEP 2, second view — whole sign groups in place of *301',
             real=('N-series',))

        for sign, _n in near:
            words = {w: v for w, v in pool.items() if sign in M.word_signs(w)}
            real, plain = REAL[sign]
            rws = test_sign(sign, words, trie, on, alpha, setname)
            allrows += rws
            show(rws, 'STEP 3 — %s (%d words), real value %s'
                 % (sign, len(words), ' or '.join(real)), real=real)
            best = min(r['rank'] for r in rws if r['candidate'] in real)
            pl = next(r['rank'] for r in rws if r['candidate'] == plain)
            print('\n  best real consonant ranks %d of %d; plain Linear B '
                  'consonant %s ranks %d' % (best, len(rws), plain, pl))

    fields = ['view', 'sign', 'rule_set', 'candidate', 'rank', 'coverage',
              'words_tested', 'total_matches', 'median_per_word', 'options',
              'formula_roots', 'formula_has_n_w_y']
    with open(OUT, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in allrows:
            w.writerow({k: r.get(k, '') for k in fields})
    print('\nwrote reports/cycle-05-rankings.csv  (%d rows)' % len(allrows))


if __name__ == '__main__':
    main()
