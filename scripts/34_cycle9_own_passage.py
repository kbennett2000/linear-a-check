#!/usr/bin/env python3
"""Cycle 9.  Do the tight readings survive without the rules written for them?

Cycle 8 found that under the stated-only rule set some readings are very tight.
But a rule the paper first states in the very passage that reads a word will
naturally fit that word.  This script finds, for each reading, the rules the
paper states *only* in the passage where it reads that word -- its "own-passage"
rules -- switches those off, and measures the reading again.

Writes reports/cycle-09-own-passage.csv.

Terms.  A *passage* is one numbered section of the paper, including its
footnotes and tables, or one entry of Appendix B.  An *own-passage rule* for a
reading is a rule that the paper states nowhere except in that reading's own
passage.  *Options* and *chance* are cycle 8's measures: how many Hebrew roots
the word matches at all, and the share of 1,000 made-up words of the same length
that can be read as the same root.
"""
import csv, importlib, json, os, random, statistics, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'scripts'))
M = importlib.import_module('21_matcher')
S5 = importlib.import_module('25_cycle5_setup')
S6 = importlib.import_module('28_cycle6_sets')

SELFTEST = os.path.join(HERE, 'reports', 'cycle-04-selftest.csv')
READINGS = os.path.join(HERE, 'reports', 'cycle-03-readings.csv')
C3RULES = os.path.join(HERE, 'reports', 'cycle-03-rules.csv')
C4RULES = os.path.join(HERE, 'reports', 'cycle-04-rules-added.csv')
INSCR = os.path.join(HERE, 'data', 'derived', 'inscriptions.json')
OUT = os.path.join(HERE, 'reports', 'cycle-09-own-passage.csv')
SEED = 20260916
BATCH = 1000

# Section start pages, read off the "§n." headings in the paper's own text
# (scripts/03_extract_pdf.py output).  Used only to say which numbered section a
# bare footnote citation such as "n.30, p.17" belongs to.
SECTION_START = [('§1', 1), ('§2', 1), ('§3', 2), ('§4', 4), ('§4.1', 4),
                 ('§4.2', 6), ('§4.3', 7), ('§5', 8), ('§5.1', 8), ('§5.2', 10),
                 ('§5.3', 10), ('§6', 11), ('§6.1', 11), ('§7', 14), ('§8', 16),
                 ('§9', 18), ('§10', 20), ('§11', 23)]

# The brief's two standing exclusions: the general sound rules on p.19 and the
# base Linear B values are never own-passage for anybody.
NEVER_OWN = {'R01', 'R05', 'R06', 'R07', 'R08'}

# R11 states two different things in two different places: the T-series also
# writes ṣ (§6.1, p.12) and it also writes ṯ (Appendix B, pp.36-40).  It is
# treated below as two sub-rules, because otherwise a reading in §6.1 whose root
# contains ṣ would count as independent when its sound value is stated exactly
# where the word is read.  See the report.
R11_SPLIT = {'R11ṣ': {'§6.1'}, 'R11ṯ': set()}   # R11ṯ: see note in main()

# Rules that give a sign its sound value.  Switching one off has to take the
# value away from the sign, not just drop a switch.
VALUE_RULES = {'R25': '*301', 'R29': '*314', 'R27': 'ZU', 'R32': '*319'}


def section_for_page(p):
    best = None
    for name, start in SECTION_START:
        if start <= p:
            best = name
    return best


def passages(where):
    """A rule's or reading's 'where' string -> the set of passages it names."""
    out = set()
    for part in where.split(';'):
        s = part.strip()
        if not s:
            continue
        s = s.split('(')[0].strip()
        if s.startswith('§'):
            num = ''
            for ch in s[1:]:
                if ch.isdigit() or ch == '.':
                    num += ch
                else:
                    break
            out.add('§' + num.rstrip('.'))
        elif s.lower().startswith('n.'):
            pg = None
            for tok in s.replace(',', ' ').split():
                if tok.startswith('p.'):
                    pg = int(''.join(c for c in tok[2:] if c.isdigit()))
            out.add(section_for_page(pg) if pg else 'unknown footnote')
        elif 'Appendix' in s:
            out.add('Appendix ' + s.split('Appendix')[1].strip()[0])
        elif s.startswith('throughout'):
            out.add('throughout')
        else:
            out.add(s)
    return out


def main():
    rule_where = {}
    for path in (C3RULES, C4RULES):
        for r in csv.DictReader(open(path, encoding='utf-8')):
            rule_where[r['rule_id']] = (r['where'], r['stated_or_used'],
                                        r['rule'])
    rule_pass = {k: passages(v[0]) for k, v in rule_where.items()}
    rule_pass['R11ṣ'] = {'§6.1'}
    rule_pass['R11ṯ'] = {'Appendix B (many entries)'}

    rows = [r for r in csv.DictReader(open(SELFTEST, encoding='utf-8'))
            if r['result'] == 'found']
    ins = json.load(open(INSCR, encoding='utf-8'))
    site_of = {}
    for r in csv.DictReader(open(READINGS, encoding='utf-8')):
        site_of[(r['word'], r['where'])] = (
            (ins.get(r['corpus_id'], {}).get('site') or '')
            if r['corpus_id'] else '')

    # ---- the same made-up batches as cycle 8
    pool, _, _ = S5.word_pool(S5.rule_sets()['full'][1])
    allt = {t for e in ins.values() for t in (e.get('transliteratedWords') or [])
            if isinstance(t, str) and t.strip()}
    model = S6.BigramModel(pool)
    rng = random.Random(SEED)
    lengths = sorted({len(M.word_signs(r['word'])) for r in rows})
    batches = {n: model.batch(n, BATCH, allt, rng, distinct=False)
               for n in lengths}

    trie, _ = M.load_hebrew('primitive')
    base_on, base_alpha = S5.rule_sets()['stated only']

    def alphabet_for(off):
        a = base_alpha
        for rid, sign in VALUE_RULES.items():
            if rid in off:
                a = a.replace(sign, None, [])
        if 'R11ṣ' in off:
            vals = dict(a.values)
            for nm, v in list(vals.items()):
                if 'ṣ' in v and nm.startswith(('TA', 'TE', 'TI', 'TO', 'TU',
                                               'TWE')):
                    vals[nm] = tuple(x for x in v if x != 'ṣ')
            a = M.Alphabet(vals, a.rules, a.vowels)
        return a

    def measure(word, want, bag, n, st, on, alpha):
        res, _ = M.match_word(word, trie, on=on, alpha=alpha, sites=st)
        hit = [k for k in want if k in res]
        if not hit:
            return None, None, None
        best = min(hit, key=lambda k: M.rank(res[k]['rules'], res[k]['sound']))
        keep = M.SOUND_MATCH
        M.SOUND_MATCH = {}
        try:
            t1 = M.Trie()
            for s in bag:
                t1.add(s, s)
            t1.finish()
            if not (want & set(M.match_word(word, t1, on=on, alpha=alpha,
                                            sites=st)[0])):
                share = None
            else:
                share = sum(1 for w in batches[n]
                            if want & set(M.match_word(w, t1, on=on, alpha=alpha,
                                                       sites=st)[0])) \
                    / len(batches[n])
        finally:
            M.SOUND_MATCH = keep
        return len(res), sorted(res[best]['rules']), share

    bag = defaultdict(set)
    for r in rows:
        bag[r['word']] |= {r['paper_root']} | {
            x.strip() for x in r['hebrew_spelling'].split(' or ')}

    out, seen = [], set()
    print('STEP 1 — each reading\'s own-passage rules\n')
    for r in rows:
        word, where, root = r['word'], r['where'], r['paper_root']
        if (word, root) in seen:
            continue
        n = len(M.word_signs(word))
        s = site_of[(word, where)]
        st = frozenset([s]) if s else frozenset()
        want = {root} | {x.strip() for x in r['hebrew_spelling'].split(' or ')}
        opts, used, chance = measure(word, want, bag[word], n, st, base_on,
                                     base_alpha)
        if opts is None:
            continue                       # not reachable under stated-only
        seen.add((word, root))
        rp = passages(where)
        # R11 is recorded by the matcher whenever a T-series sign is used at
        # all, so the ṣ half is only credited when the root actually has ṣ.
        used_x = [u for u in used if u != 'R11']
        if 'R11' in used:
            used_x += ['R11ṣ'] if 'ṣ' in root.split('-') else ['R11ṯ']
        own = sorted(u for u in used_x
                     if u not in NEVER_OWN and rule_pass.get(u)
                     and rule_pass[u] <= rp)
        out.append(dict(word=word, where=where, root=root, n_signs=n, site=s,
                        passage=' '.join(sorted(rp)), rules_used=' '.join(used_x),
                        own_passage_rules=' '.join(own) or '(none)',
                        base_options=opts, base_chance=round(chance, 4)))
        print('%-22s %-8s %-18s own-passage: %s'
              % (word, root, ' '.join(sorted(rp)), ' '.join(own) or '(none)'))

    print('\nSTEP 2 — switch the own-passage rules off\n')
    print('%-22s %-8s %-14s %-9s %8s %8s'
          % ('word', 'root', 'switched off', 'survives', 'options', 'chance'))
    for x in out:
        off = set(x['own_passage_rules'].split()) - {'(none)'}
        if not off:
            x.update(survives='yes (nothing to switch off)',
                     new_options=x['base_options'], new_chance=x['base_chance'],
                     blocker='')
        else:
            on = frozenset(base_on - off)
            alpha = alphabet_for(off)
            n = x['n_signs']
            st = frozenset([x['site']]) if x['site'] else frozenset()
            want = _spellings(x['word'], x['root'], rows)
            opts, used, chance = measure(x['word'], want, bag[x['word']], n, st,
                                         on, alpha)
            if opts is None:
                # which single rule can the reading not do without?  Switch
                # off just that one and see whether the reading still stands.
                blockers = []
                for rid in sorted(off):
                    o2 = frozenset(base_on - {rid})
                    a2 = alphabet_for({rid})
                    if measure(x['word'], want, bag[x['word']], n, st, o2,
                               a2)[0] is None:
                        blockers.append(rid)
                x.update(survives='no', new_options='', new_chance='',
                         blocker=' '.join(blockers) or ' '.join(sorted(off)))
            else:
                x.update(survives='yes', new_options=opts,
                         new_chance=round(chance, 4), blocker='')
        print('%-22s %-8s %-14s %-9s %8s %8s'
              % (x['word'], x['root'], x['own_passage_rules'][:14],
                 x['survives'][:9], x['new_options'],
                 ('%.1f%%' % (100 * x['new_chance'])) if x['new_chance'] != ''
                 else '-'))

    COLS = ['word', 'root', 'where', 'passage', 'n_signs', 'site', 'rules_used',
            'own_passage_rules', 'survives', 'base_options', 'base_chance',
            'new_options', 'new_chance', 'blocker']
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for x in out:
            w.writerow({k: x.get(k, '') for k in COLS})
    print('\nwrote %s  (%d rows)' % (os.path.relpath(OUT, HERE), len(out)))

    surv = [x for x in out if x['survives'].startswith('yes')]
    print('\nreadings reachable under the stated-only set: %d' % len(out))
    print('readings with at least one own-passage rule:    %d'
          % sum(1 for x in out if x['own_passage_rules'] != '(none)'))
    print('readings that survive their own-passage rules being off: %d of %d'
          % (len(surv), len(out)))
    tight = [x for x in surv
             if x['new_options'] != '' and int(x['new_options']) <= 10
             and float(x['new_chance']) <= 0.005]
    print('\nSURVIVE WITH 10 OR FEWER OPTIONS AND A CHANCE OF 0.5%% OR LESS: %d'
          % len(tight))
    for x in sorted(tight, key=lambda y: (float(y['new_chance']),
                                          int(y['new_options']))):
        print('  %-22s %-8s %-20s options %-3s chance %.1f%%'
              % (x['word'], x['root'], x['where'][:20], x['new_options'],
                 100 * float(x['new_chance'])))
    print('\nREADINGS THAT DO NOT SURVIVE, AND WHAT THEY CANNOT DO WITHOUT')
    for x in out:
        if x['survives'] == 'no':
            print('  %-22s %-8s needs %s' % (x['word'], x['root'], x['blocker']))


def _spellings(word, root, rows):
    out = set()
    for r in rows:
        if r['word'] == word and r['paper_root'] == root:
            out |= {r['paper_root']} | {y.strip()
                                        for y in r['hebrew_spelling'].split(' or ')}
    return out


if __name__ == '__main__':
    main()
