#!/usr/bin/env python3
"""Parse Appendix B (pp. 36-40) into structured entries.

Appendix B has a regular shape:  WORD: <inscription ref> (<citation>). Cf. ...
Every real entry's body opens with an inscription reference (a two/three-letter
site code followed by a number, e.g. "PK Za 11", "KH 11.1", "HTZb159"), which is
what distinguishes a genuine head word from a colon inside the prose. Two quirks
of the PDF text layer have to be handled: the space after the head's colon is
often lost, and entries are hard-wrapped mid-word.
"""
import json, re

PAGES = json.load(open('data/derived/paper_pages.json'))

text = '\n'.join(PAGES[n] for n in ('36', '37', '38', '39', '40'))
text = text.split('Appendix B: Index of Linear A Sign-Groups Cited in Davis 2026')[1]
text = text.split('Appendix C: Keftiu Incantations')[0]
text = re.sub(r'\n?YaDiktu diMino\n?', '\n', text)
text = re.sub(r'\n\s*\d{1,2}\s*\n', '\n', text)
text = re.sub(r'-\n', '-', text)          # rejoin hyphen-broken wraps
flat = re.sub(r'\s*\n\s*', ' ', text)

WORD = r"(?:\*\d{2,3}[A-Za-z]?|[A-Z]{1,3}[₂₃₄]?)"
# head word, colon, then an inscription reference
REF = r"[A-Z]{2,3}(?:\(\?\))?\s*(?:Z[a-g]|W[a-c])?\s*\d"
HEAD = re.compile(rf'(?<![A-Z0-9\-*])((?:{WORD})(?:-(?:{WORD}))+)\s*:\s*(?={REF})')

kept = [(m.start(), m.group(1), m.end()) for m in HEAD.finditer(flat)]
entries = []
for i, (s, w, e) in enumerate(kept):
    end = kept[i + 1][0] if i + 1 < len(kept) else len(flat)
    entries.append({'word': w, 'body': flat[e:end].strip()})

print(f'Appendix B entries parsed: {len(entries)}   (paper says 67)')

# sanity check: the appendix is alphabetical
def sortkey(w):
    return w.replace('*', '~')
bad = [(a['word'], b['word']) for a, b in zip(entries, entries[1:])
       if sortkey(a['word']) > sortkey(b['word'])]
print(f'out-of-alphabetical-order pairs: {len(bad)} {bad if bad else ""}')

json.dump(entries, open('data/derived/appendix_b.json', 'w'), indent=1)
for en in entries:
    print(f'  {en["word"]:24} | {en["body"][:74]}')
