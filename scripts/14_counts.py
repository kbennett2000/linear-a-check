#!/usr/bin/env python3
"""Step 4: counts over the readings table, and a re-count of footnote 36.

Footnote 36 (p.20): "I have included a comprehensive appendix of 67 Linear A
sign-groups matching his own. Of these, 39 (58.2%) are hapax legomena."
A HAPAX LEGOMENON (plural hapax legomena) is a word that occurs exactly once in
the whole surviving corpus.
"""
import json, re
from collections import Counter, defaultdict

INS = json.load(open('data/derived/inscriptions.json'))
CHK = json.load(open('data/derived/readings_checked.json'))
APPB = json.load(open('data/derived/appendix_b.json'))

# ---------- corpus word frequency ----------
FREQ = Counter()
for v in INS.values():
    for t in (v.get('transliteratedWords') or []):
        if t.strip():
            FREQ[t] += 1

CANON = {'*79': 'ZU', 'TH': 'ZU', '*301': 'NA', '*319': '*904'}
def canon_key(w):
    return '-'.join(CANON.get(s, s) for s in w.split('-') if s)

CANON_FREQ = Counter()
for w, n in FREQ.items():
    CANON_FREQ[canon_key(w)] += n

def corpus_count(word):
    """How many times this word occurs in the whole corpus, as printed and after
    the sign-spelling allowances."""
    return FREQ.get(word, 0), CANON_FREQ.get(canon_key(word), 0)

print('=' * 72)
print('TABLE COUNTS')
print('=' * 72)
print(f'total rows      : {len(CHK)}')
print(f'distinct words  : {len({r["word"] for r in CHK})}')
print()

def part(where):
    if where.startswith('Appendix A (AB79'): return 'Appendix A (AB79 note)'
    if where.startswith('Appendix A'):       return 'Appendix A'
    if where.startswith('Appendix B'):       return 'Appendix B'
    if 'n.' in where:                        return 'footnotes'
    if where.startswith('§8 table'):         return '§8 cross-site table'
    if where.startswith('§7 table'):         return '§7 translation table'
    return 'main text'

print('ROWS BY PART OF THE PAPER')
by_part = Counter(part(r['where']) for r in CHK)
for k, n in by_part.most_common():
    print(f'  {k:26} {n}')
print(f'  {"TOTAL":26} {sum(by_part.values())}')
print()

print('ROWS BY CONFIDENCE LABEL')
cc = Counter(r['confidence'] or '(none given)' for r in CHK)
for k, n in cc.most_common():
    print(f'  {k:26} {n}')
print()

print('ROWS BY GROUP')
for k, n in Counter(r['group'] for r in CHK).most_common():
    print(f'  {k:32} {n}')
print()

print('=' * 72)
print('CORPUS FREQUENCY OF EACH DISTINCT WORD')
print('=' * 72)
words = sorted({r['word'] for r in CHK})
rows = []
for w in words:
    asprinted, allowed = corpus_count(w)
    rows.append((w, asprinted, allowed))
print(f'{"word":26} {"as printed":>11} {"with allowances":>16}')
for w, a, b in rows:
    print(f'{w:26} {a:>11} {b:>16}')
freq_json = {w: {'as_printed': a, 'with_allowances': b} for w, a, b in rows}
json.dump(freq_json, open('data/derived/word_frequency.json', 'w'),
          ensure_ascii=False, indent=1)
print()
print('distribution of corpus counts (with allowances):')
for n, c in sorted(Counter(b for _, _, b in rows).items()):
    print(f'  occurs {n:>3}x in the corpus : {c} of the {len(rows)} distinct words')

print()
print('=' * 72)
print('FOOTNOTE 36 RE-COUNT: hapax legomena among the 67 Appendix B words')
print('=' * 72)
print('paper (p.20 n.36): 39 of 67 (58.2%) are hapax legomena')
appb_words = [e['word'] for e in APPB]
print(f'Appendix B entries in our parse: {len(appb_words)}')

for label, use_allow in (('as the paper prints them', False),
                         ('with the sign-spelling allowances applied', True)):
    counts = {}
    for w in appb_words:
        a, b = corpus_count(w)
        counts[w] = b if use_allow else a
    hap = [w for w, n in counts.items() if n == 1]
    absent = [w for w, n in counts.items() if n == 0]
    more = [w for w, n in counts.items() if n > 1]
    pct = 100 * len(hap) / len(appb_words)
    print()
    print(f'  {label}:')
    print(f'    occur exactly once (hapax) : {len(hap)}  ({pct:.1f}%)   '
          f'paper: 39 (58.2%)  difference {len(hap)-39:+d}')
    print(f'    occur more than once       : {len(more)}')
    print(f'    not found in the corpus    : {len(absent)}')
    if absent:
        print(f'      -> {", ".join(sorted(absent))}')

# a hapax count that treats "not in this corpus" as "would be a hapax in the
# paper's larger corpus" - an upper bound
counts = {w: corpus_count(w)[1] for w in appb_words}
upper = sum(1 for n in counts.values() if n <= 1)
print()
print(f'  upper bound, counting the not-found words as hapaxes too: '
      f'{upper} ({100*upper/len(appb_words):.1f}%)')
