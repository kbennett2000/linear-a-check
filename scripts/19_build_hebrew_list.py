#!/usr/bin/env python3
"""Cycle 3, Part C.  Build data/derived/hebrew_list.json from Strong's Hebrew.

Source: Strong's Hebrew dictionary (James Strong, 1894, public domain) as
prepared by Open Scriptures, CC BY-SA.  Downloaded to data/raw/ and dumped to
JSON by scripts/18_dump_hebrew.js.  The result is NOT committed: the licence is
share-alike, and this repository commits no data files.

For every entry the "lemma" field is reduced to a consonant skeleton:

  * only the 22 Hebrew consonant letters are kept; the five final forms
    (ך ם ן ף ץ) are folded into the ordinary letters (כ מ נ פ צ)
  * every vowel point, accent and cantillation mark is dropped
  * the letters are written in Latin and joined with hyphens

    א ʾ   ב b   ג g   ד d   ה h   ו w   ז z   ח ḥ   ט ṭ   י y   כ k   ל l
    מ m   נ n   ס s   ע ʿ   פ p   צ ṣ   ק q   ר r   ש š/ś   ת t

  ש takes š when it carries the shin dot (U+05C1) and ś when it carries the
  sin dot (U+05C2).  Entries whose ש carries neither are counted and reported;
  they are written š.

Two flags are recorded:

  aramaic          the "derivation" field contains "(Aramaic)"
  primitive_root   the "derivation" field contains "primitive root"

For a primitive root whose skeleton ends in h, a second skeleton is recorded
with y in place of that final h, because Hebrew writes many roots that
originally ended in y or w with a final ה.
"""
import json, os, sys, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, 'data', 'derived', 'strongs_hebrew.json')
DST = os.path.join(HERE, 'data', 'derived', 'hebrew_list.json')

SHIN_DOT = 'ׁ'
SIN_DOT = 'ׂ'

LETTER = {
    'א': 'ʾ', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h',
    'ו': 'w', 'ז': 'z', 'ח': 'ḥ', 'ט': 'ṭ', 'י': 'y',
    'ך': 'k', 'כ': 'k', 'ל': 'l', 'ם': 'm', 'מ': 'm',
    'ן': 'n', 'נ': 'n', 'ס': 's', 'ע': 'ʿ', 'ף': 'p',
    'פ': 'p', 'ץ': 'ṣ', 'צ': 'ṣ', 'ק': 'q', 'ר': 'r',
    'ת': 't',
}
SHIN = 'ש'


def skeleton(lemma):
    """Return (skeleton, number of undotted shins seen)."""
    s = unicodedata.normalize('NFD', lemma)
    out, undotted = [], 0
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == SHIN:
            j = i + 1
            dot = None
            while j < n and s[j] not in LETTER and s[j] != SHIN:
                if s[j] in (SHIN_DOT, SIN_DOT):
                    dot = s[j]
                    break
                j += 1
            if dot == SIN_DOT:
                out.append('ś')
            else:
                out.append('š')
                if dot is None:
                    undotted += 1
        elif ch in LETTER:
            out.append(LETTER[ch])
        i += 1
    return '-'.join(out), undotted


def main():
    dict_ = json.load(open(SRC, encoding='utf-8'))
    entries = []
    undotted_total = 0
    undotted_ids = []
    empty = []
    for sid, e in dict_.items():
        lemma = e.get('lemma', '')
        deriv = e.get('derivation') or ''
        sk, und = skeleton(lemma)
        if und:
            undotted_total += und
            undotted_ids.append(sid)
        if not sk:
            empty.append(sid)
        prim = 'primitive root' in deriv
        rec = {
            'id': sid,
            'lemma': lemma,
            'xlit': e.get('xlit', ''),
            'skeleton': sk,
            'aramaic': '(Aramaic)' in deriv,
            'primitive_root': prim,
            'gloss': e.get('strongs_def', ''),
        }
        # a primitive root written with a final he is very often a root whose
        # third consonant was originally y (or w)
        if prim and sk.endswith('-h'):
            rec['skeleton_final_h_as_y'] = sk[:-1] + 'y'
        entries.append(rec)

    entries.sort(key=lambda r: int(r['id'][1:]))
    json.dump(entries, open(DST, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('wrote data/derived/hebrew_list.json  (%d entries)' % len(entries))

    total = len(entries)
    aram = sum(1 for r in entries if r['aramaic'])
    nonaram = total - aram
    prim_nonaram = sum(1 for r in entries
                       if r['primitive_root'] and not r['aramaic'])
    alt = sum(1 for r in entries if 'skeleton_final_h_as_y' in r)

    print('\nKNOWN-ANSWER CHECK (Part C, counts)')
    checks = [('entries in total', total, 8674),
              ('flagged Aramaic', aram, 675),
              ('not flagged Aramaic', nonaram, 7999),
              ('primitive roots among those %d' % nonaram, prim_nonaram, 1390)]
    ok = True
    for label, got, want in checks:
        good = got == want
        ok &= good
        print('  %-38s expected %5d  got %5d  %s'
              % (label, want, got, 'PASS' if good else 'FAIL'))

    print('\nKNOWN-ANSWER CHECK (Part C, skeletons)')
    by_id = {r['id']: r for r in entries}
    want_sk = {'H3664': 'k-n-s', 'H3474': 'y-š-r', 'H8334': 'š-r-t',
               'H1854': 'd-q-q', 'H7521': 'r-ṣ-h', 'H6437': 'p-n-h',
               'H5115': 'n-w-h', 'H6030': 'ʿ-n-h'}
    for sid in sorted(want_sk, key=lambda s: int(s[1:])):
        got = by_id[sid]['skeleton']
        good = got == want_sk[sid]
        ok &= good
        print('  %-6s expected %-7s got %-7s  %s'
              % (sid, want_sk[sid], got, 'PASS' if good else 'FAIL'))

    print('\n  ALL PART C KNOWN ANSWERS AS DESCRIBED' if ok
          else '\n  STOP: a Part C known answer did not come out as described')

    print('\nnotes on the build')
    print('  primitive roots given a second, final-h-as-y skeleton: %d' % alt)
    print('  entries whose lemma contains a shin with neither dot: %d  (written š)'
          % len(undotted_ids))
    if undotted_ids:
        print('    %s' % ' '.join(undotted_ids[:20])
              + (' ...' if len(undotted_ids) > 20 else ''))
    print('  entries whose lemma yields an empty skeleton: %d  %s'
          % (len(empty), ' '.join(empty)))
    lens = Counter(len(r['skeleton'].split('-')) for r in entries if r['skeleton'])
    print('  skeleton lengths (letters -> entries): %s'
          % ', '.join('%d->%d' % kv for kv in sorted(lens.items())))

    # how many non-root entries could be affected by mater lectionis spelling
    nonroot = [r for r in entries if not r['primitive_root']]
    with_wy = [r for r in nonroot
               if any(c in ('w', 'y') for c in r['skeleton'].split('-'))]
    med_fin = [r for r in nonroot
               if any(c in ('w', 'y') for c in r['skeleton'].split('-')[1:])]
    print('  entries not flagged as primitive roots: %d' % len(nonroot))
    print('    of those, skeleton contains w or y anywhere:        %d' % len(with_wy))
    print('    of those, w or y other than as the first letter:    %d' % len(med_fin))

    if not ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
