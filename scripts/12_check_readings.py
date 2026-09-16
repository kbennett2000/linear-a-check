#!/usr/bin/env python3
"""Step 3: check every readings-table row against the corpus.

Each row is put in one of five groups:

  exact                          the word appears in that inscription as printed
  same word, different spelling  matches once a sign-spelling allowance is
                                 applied (see CANON below)
  different word breaks          the signs are present in the same order, but
                                 the paper and the corpus divide them into words
                                 differently
  not found                      neither of the above; we report what the
                                 inscription has instead
  no inscription given           the paper gives no inscription for the word

SIGN-SPELLING ALLOWANCES. Both the paper's spelling and the corpus's are mapped
onto a common alphabet before the second and third passes. Every substitution
actually used is recorded per row, so no match is silently smoothed over.
"""
import json, re, csv
from collections import Counter

INS = json.load(open('data/derived/inscriptions.json'))
ROWS = json.load(open('data/derived/readings_rows.json'))
IDS = set(INS)

CANON = {
    '*79': 'ZU',      # paper writes AB79 as *79; corpus writes its Linear B value ZU
    'TH':  'ZU',      # paper also writes AB79 as TH (its proposed value /ṯ/)
    '*301': 'NA',     # paper sometimes writes *301 as NA (its proposed value /na/)
    '*319': '*904',   # paper numbers this sign *319; corpus numbers it *904
}
WHY = {
    ('*79', 'ZU'):   'AB79: paper writes *79, corpus writes ZU',
    ('TH', 'ZU'):    'AB79: paper writes TH, corpus writes ZU',
    ('*301', 'NA'):  'paper writes NA where the corpus writes *301',
    ('NA', '*301'):  'paper writes NA where the corpus writes *301',
    ('*319', '*904'): 'paper numbers the sign *319, corpus numbers it *904',
}

def signs(word):
    return [s for s in word.split('-') if s]

def canon(sq):
    return [CANON.get(s, s) for s in sq]

# ---------- resolving printed references to corpus ids ----------
def split_refs(ref):
    """Printed reference string -> list of individual reference strings."""
    if not ref or re.search(r'attestation', ref, re.I):
        return []
    r = ref.replace('(?)', '\x01')                 # protect the "(?)" marker
    r = re.sub(r'\([^)]*\)', ' ', r)               # drop citation parentheses
    r = r.split('.')[0]                            # stop at the first sentence end
    r = r.replace('\x01', '(?)')
    return [p.strip() for p in r.split(',') if p.strip()]

def candidates(one):
    r = one.replace('–', '-').replace('—', '-')
    r = re.sub(r'\s+', '', r)
    r = re.sub(r'\.\d+(-\d+)?$', '', r)            # drop line numbers
    out = []
    def add(x):
        if x and x not in out:
            out.append(x)
    add(r)
    m = re.match(r'^(.*?)([a-e])-([a-e])$', r)     # 11a-b
    if m:
        stem, lo, hi = m.groups()
        for c in (chr(o) for o in range(ord(lo), ord(hi) + 1)):
            add(stem + c)
        add(stem)
    m = re.match(r'^(.*?)(\d+)-(\d+)$', r)         # Zf 1-2
    if m:
        stem, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        for n in range(lo, hi + 1):
            add(f'{stem}{n}')
    m = re.match(r'^(.*\d)([a-e])$', r)
    if m:
        add(m.group(1))
    for c in 'abcd':
        add(r + c)
    return out

def toks(cid):
    return [t for t in (INS[cid].get('transliteratedWords') or []) if t.strip()]

# ---------- the three passes ----------
def try_one(word, cid):
    """Return (rank, group, allowance, note) for this word in this inscription.
    Lower rank is a better outcome."""
    cw = toks(cid)
    if word in cw:
        return 0, 'exact', '', ''
    pc = canon(signs(word))
    for t in cw:
        if canon(signs(t)) == pc:
            diffs = {WHY.get((a, b), f'{a} vs {b}')
                     for a, b in zip(signs(word), signs(t)) if a != b}
            return 1, 'same word, different spelling', '; '.join(sorted(diffs)), \
                   f'corpus has {t}'
    # word-break pass: does the canonical sign run appear across word boundaries?
    stream, owner = [], []
    for t in cw:
        if t in ('𐄁',) or not re.match(r'^[A-Z*]', t):
            stream.append('\x02'); owner.append(t)     # a barrier we may cross
            continue
        for s in canon(signs(t)):
            stream.append(s); owner.append(t)
    joined = '\x00'.join(stream)
    needle = '\x00'.join(pc)
    if needle and needle in joined:
        idx = joined[:joined.index(needle)].count('\x00')
        hosts = []
        for o in owner[idx:idx + len(pc)]:
            if o not in hosts:
                hosts.append(o)
        # compare the paper's signs against the exact stream slice they matched,
        # so the reported allowance is aligned rather than guessed
        raw = []
        for o in owner[idx:idx + len(pc)]:
            pass
        matched_raw = []
        k = 0
        for t in cw:
            if t in ('\u3000',) or not re.match(r'^[A-Z*]', t):
                continue
            for s_ in signs(t):
                matched_raw.append(s_)
        # rebuild the un-canonicalised stream in the same order as `stream`
        raw_stream = []
        for t in cw:
            if t in ('\U0001d101',) or not re.match(r'^[A-Z*]', t):
                raw_stream.append('\x02')
                continue
            raw_stream.extend(signs(t))
        slice_raw = raw_stream[idx:idx + len(pc)]
        diffs = {WHY.get((a, b), f'{a} vs {b}')
                 for a, b in zip(signs(word), slice_raw) if a != b}
        if len(hosts) == 1:
            note = f'corpus writes it inside the longer word {hosts[0]}'
        else:
            note = ('corpus splits it as ' + ' + '.join(hosts) +
                    ' (no word divider between them)')
        return 2, 'different word breaks', '; '.join(sorted(diffs)), note
    return 3, 'not found', '', 'corpus has: ' + ' '.join(cw[:16])

def check(word, ref):
    """Evaluate the word against every corpus id the printed reference can
    resolve to, and return the best outcome plus a note when the references
    disagree with one another."""
    results = []
    for one in split_refs(ref):
        for c in candidates(one):
            if c in IDS:
                rank, group, allow, note = try_one(word, c)
                results.append((rank, c, group, allow, note))
    if not results:
        return None
    results.sort(key=lambda x: x[0])
    best = results[0]
    # if the paper cited more than one inscription and they do not agree, say so
    others = [r for r in results[1:] if r[1] != best[1]]
    if others:
        extra = '; '.join(f'{r[1]}: {r[2]}' + (f' ({r[4]})' if r[4] and r[0] < 3 else '')
                          for r in others)
        note = (best[4] + ' | ' if best[4] else '') + 'other cited inscription(s) -> ' + extra
        best = (best[0], best[1], best[2], best[3], note)
    return best

out = []
for r in ROWS:
    res = check(r['word'], r['inscription'])
    if res is None:
        cid, group, allow, note = '', 'no inscription given', '', ''
        if r['inscription']:
            note = f'paper cites "{r["inscription"]}" but gives no inscription id'
    else:
        _, cid, group, allow, note = res
    if r.get('paper_note'):
        note = (note + ' | ' if note else '') + r['paper_note']
    out.append({**r, 'corpus_id': cid, 'group': group,
                'allowance': allow, 'note': note})

json.dump(out, open('data/derived/readings_checked.json', 'w'),
          ensure_ascii=False, indent=1)

COLS = ['word', 'where', 'inscription', 'corpus_id', 'reading', 'meaning',
        'confidence', 'group', 'allowance', 'note']
with open('reports/cycle-02-readings.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    for r in out:
        w.writerow({k: r.get(k, '') for k in COLS})

print('ROWS BY GROUP')
for g, n in Counter(r['group'] for r in out).most_common():
    print(f'  {g:32} {n}')
print(f'  {"TOTAL":32} {len(out)}')
print()
print('EVERY ROW THAT IS NOT "exact":')
for r in out:
    if r['group'] != 'exact':
        print(f'  [{r["group"]}] {r["word"]}  ({r["where"]}; "{r["inscription"]}"'
              f' -> {r["corpus_id"] or "unresolved"})')
        if r['allowance']:
            print(f'        allowance: {r["allowance"]}')
        if r['note']:
            print(f'        {r["note"][:160]}')
