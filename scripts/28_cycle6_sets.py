#!/usr/bin/env python3
"""Cycle 6, Step 1.  Build the three word sets.

  real           the 787 readable hyphenated corpus words of cycle 5, each
                 marked "read by the paper" or "never read"
  shuffled       each real word's own signs put in a new order
  Linear A-like  new words of the same length, drawn from the corpus's own
                 sign patterns

Writes data/derived/cycle6_sets.json (not committed -- rebuild it by running
this script; the random seed is fixed below).

Terms.  A *word type* is one distinct spelling, however many times it occurs.
A *bigram* is a pair of neighbouring signs; the Linear A-like words are drawn
from a bigram model, meaning each sign is chosen from how often it follows the
sign before it.
"""
import importlib, json, os, random, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')

INSCR = os.path.join(HERE, 'data', 'derived', 'inscriptions.json')
READ = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
OUT = os.path.join(HERE, 'data', 'derived', 'cycle6_sets.json')

SEED = 20260916
PER_WORD = 10            # made-up words per real word, in each made-up set
TRIES = 400              # how many draws before giving up on one real word

# Cycle 2's sign-spelling allowances, copied from scripts/12_check_readings.py.
# They are needed to say which corpus word a printed reading answers to.
CANON = {'*79': 'ZU', 'TH': 'ZU', '*301': 'NA', '*319': '*904'}


def signs(w):
    return [s for s in w.split('-') if s]


def canon(sq):
    return [CANON.get(s, s) for s in sq]


# --------------------------------------------------------------------------
# which corpus words the paper reads
# --------------------------------------------------------------------------
def corpus_words_read(ins, rows):
    """-> set of corpus word types that some readings row answers to.

    Repeats cycle 2's three passes (exact, same word different spelling,
    different word breaks) but records the corpus word rather than the group.
    A word-break row marks every corpus word its sign run crosses.
    """
    read = set()
    unresolved = 0
    for r in rows:
        cid = r['corpus_id']
        if not cid or cid not in ins:
            unresolved += 1
            continue
        toks = [t for t in (ins[cid].get('transliteratedWords') or []) if t.strip()]
        w = r['word']
        if w in toks:
            read.add(w)
            continue
        pc = canon(signs(w))
        hit = next((t for t in toks if canon(signs(t)) == pc), None)
        if hit is not None:
            read.add(hit)
            continue
        # word-break pass: the same sign run spread over the token stream
        stream, owner = [], []
        for t in toks:
            if not re.match(r'^[A-Z*]', t):
                stream.append('\x02')
                owner.append(t)
                continue
            for s in canon(signs(t)):
                stream.append(s)
                owner.append(t)
        joined = '\x00'.join(stream)
        needle = '\x00'.join(pc)
        if needle and needle in joined:
            idx = joined[:joined.index(needle)].count('\x00')
            for o in owner[idx:idx + len(pc)]:
                read.add(o)
            continue
        unresolved += 1
    return read, unresolved


# --------------------------------------------------------------------------
# the made-up sets
# --------------------------------------------------------------------------
def shuffled_set(pool, forbidden, rng):
    out = {}
    skipped = []
    for w in sorted(pool):
        sg = signs(w)
        if len(set(sg)) < 2:
            skipped.append(w)
            continue
        made = []
        seen = set()
        for _ in range(TRIES):
            if len(made) >= PER_WORD:
                break
            t = sg[:]
            rng.shuffle(t)
            new = '-'.join(t)
            if new == w or new in forbidden or new in seen:
                continue
            seen.add(new)
            made.append(new)
        out[w] = made
    return out, skipped


class BigramModel:
    """How real words begin, and which sign follows which."""

    def __init__(self, pool):
        self.first = Counter()
        self.nxt = defaultdict(Counter)
        self.overall = Counter()
        for w in pool:
            sg = signs(w)
            self.first[sg[0]] += 1
            for s in sg:
                self.overall[s] += 1
            for a, b in zip(sg, sg[1:]):
                self.nxt[a][b] += 1
        self._f = (list(self.first), [self.first[k] for k in self.first])
        self._o = (list(self.overall), [self.overall[k] for k in self.overall])
        self._n = {a: (list(c), [c[k] for k in c]) for a, c in self.nxt.items()}
        self.dead_ends = sorted(s for s in self.overall if s not in self.nxt)

    def draw(self, length, rng):
        keys, wts = self._f
        w = [rng.choices(keys, weights=wts, k=1)[0]]
        while len(w) < length:
            k_w = self._n.get(w[-1]) or self._o
            w.append(rng.choices(k_w[0], weights=k_w[1], k=1)[0])
        return '-'.join(w)

    def batch(self, length, n, forbidden, rng, distinct=True):
        made, seen = [], set()
        for _ in range(TRIES * max(1, n // PER_WORD)):
            if len(made) >= n:
                break
            new = self.draw(length, rng)
            if new in forbidden or (distinct and new in seen):
                continue
            seen.add(new)
            made.append(new)
        return made


def main():
    rng = random.Random(SEED)
    ins = json.load(open(INSCR, encoding='utf-8'))
    import csv
    rows = list(csv.DictReader(open(READ, encoding='utf-8')))

    sets = S5.rule_sets()
    full_on, full_alpha = sets['full']
    st_on, st_alpha = sets['stated only']
    pool, dropped, count = S5.word_pool(full_alpha)
    pool_st, _, _ = S5.word_pool(st_alpha)
    print('WORD POOL')
    print('  readable hyphenated corpus words, full rule set:        %d' % len(pool))
    print('  readable hyphenated corpus words, stated-only rule set: %d  %s'
          % (len(pool_st), 'identical' if set(pool) == set(pool_st)
             else 'DIFFERENT -- check'))

    # every corpus word type, used only to throw out made-up words that are real
    all_tokens = set()
    for e in ins.values():
        for t in (e.get('transliteratedWords') or []):
            if isinstance(t, str) and t.strip():
                all_tokens.add(t)
    print('  distinct corpus word types of every kind (the "is it real?" list): %d'
          % len(all_tokens))

    read, unresolved = corpus_words_read(ins, rows)
    read_in_pool = sorted(w for w in pool if w in read)
    never = sorted(w for w in pool if w not in read)
    print('\nREAD BY THE PAPER')
    print('  readings rows:                                     %d' % len(rows))
    print('  rows that answer to no corpus word:                %d' % unresolved)
    print('  distinct corpus word types the paper reads:        %d' % len(read))
    print('  of those, inside the readable pool:                %d' % len(read_in_pool))
    print('  readable pool words the paper never reads:         %d' % len(never))

    # ---- shuffled
    shuf_map, no_shuffle = shuffled_set(pool, all_tokens, rng)
    shuf = sorted({x for v in shuf_map.values() for x in v})
    print('\nSHUFFLED SET')
    print('  real words with at least two different signs: %d'
          % (len(pool) - len(no_shuffle)))
    print('  real words that cannot be shuffled:           %d' % len(no_shuffle))
    print('  made-up words:                                %d' % len(shuf))

    # ---- Linear A-like
    model = BigramModel(pool)
    like_map = {}
    for w in sorted(pool):
        like_map[w] = model.batch(len(signs(w)), PER_WORD, all_tokens, rng)
    like = sorted({x for v in like_map.values() for x in v})
    print('\nLINEAR A-LIKE SET')
    print('  signs that never start a word but do occur: %d'
          % len([s for s in model.overall if s not in model.first]))
    print('  signs never followed by anything (drawn from overall frequency '
          'instead): %d  %s' % (len(model.dead_ends), ' '.join(model.dead_ends[:12])))
    print('  made-up words: %d' % len(like))

    # ---- the seven formula words, 1000 each
    FORMULA = ['A-TA-I-*301-WA-JA', 'JA-DI-KI-TU', 'JA-SA-SA-RA-ME',
               'U-NA-KA-NA-SI', 'I-PI-NA-MA', 'SI-RU-TE', 'TA-NA-RA-TE-U-TI-NU']
    formula_like = {}
    for w in FORMULA:
        formula_like[w] = model.batch(len(signs(w)), 1000, all_tokens, rng)
    print('\nONE THOUSAND LINEAR A-LIKE WORDS PER FORMULA WORD')
    for w in FORMULA:
        print('  %-22s %d signs, %d made' % (w, len(signs(w)), len(formula_like[w])))

    # ------------------------------------------------------------------
    # the checks
    # ------------------------------------------------------------------
    print('\nCHECK 1: every shuffled word has the same signs as its source')
    bad = [(w, x) for w, v in shuf_map.items() for x in v
           if Counter(signs(x)) != Counter(signs(w))]
    print('  mismatches: %d   %s' % (len(bad), 'PASS' if not bad else 'FAIL'))

    print('\nCHECK 2: length distribution, real pool vs Linear A-like')
    rl = Counter(len(signs(w)) for w in pool)
    ll = Counter(len(signs(x)) for v in like_map.values() for x in v)
    print('  %-8s %10s %14s %10s' % ('signs', 'real', 'Linear A-like', 'expected'))
    okl = True
    for k in sorted(rl):
        exp = rl[k] * PER_WORD
        okl &= abs(ll.get(k, 0) - exp) == 0
        print('  %-8d %10d %14d %10d' % (k, rl[k], ll.get(k, 0), exp))
    print('  every length exactly %dx the real pool: %s'
          % (PER_WORD, 'PASS' if okl else 'no -- some draws were dropped as real'))

    print('\nCHECK 3: the 20 most common signs, real pool vs Linear A-like')
    rs = Counter(s for w in pool for s in signs(w))
    ls = Counter(s for v in like_map.values() for x in v for s in signs(x))
    rtot, ltot = sum(rs.values()), sum(ls.values())
    top_r = [s for s, _ in rs.most_common(20)]
    top_l = [s for s, _ in ls.most_common(20)]
    print('  %-4s %-22s %-22s' % ('#', 'real pool', 'Linear A-like'))
    for i in range(20):
        a, b = top_r[i], top_l[i]
        print('  %-4d %-6s %5.2f%%          %-6s %5.2f%%'
              % (i + 1, a, 100 * rs[a] / rtot, b, 100 * ls[b] / ltot))
    shared = len(set(top_r) & set(top_l))
    worst = max(abs(100 * rs[s] / rtot - 100 * ls.get(s, 0) / ltot) for s in top_r)
    print('  signs in both top-20 lists: %d of 20' % shared)
    print('  largest share difference among the real top 20: %.2f percentage points'
          % worst)

    print('\nCHECK 4: no made-up word is a real corpus word')
    clash = sorted((set(shuf) | set(like)
                    | {x for v in formula_like.values() for x in v}) & all_tokens)
    print('  clashes: %d   %s' % (len(clash), 'PASS' if not clash else 'FAIL'))

    json.dump({'seed': SEED,
               'real': {w: {'n': i['n'], 'sites': sorted(i['sites']),
                            'read_by_paper': w in read} for w, i in pool.items()},
               'shuffled': shuf_map, 'like': like_map,
               'formula_like': formula_like,
               'no_shuffle': no_shuffle},
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print('\nwrote %s' % os.path.relpath(OUT, HERE))


if __name__ == '__main__':
    main()
