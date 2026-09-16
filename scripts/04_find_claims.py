#!/usr/bin/env python3
"""Search the extracted paper text for a pattern and report the PDF page number
of each hit. Spaces are often lost by PDF extraction, so we search both the raw
text and a space-stripped version."""
import json, re, sys

PAGES = json.load(open('data/derived/paper_pages.json'))

def search(pattern, context=220):
    rx = re.compile(pattern, re.I)
    for pno in sorted(PAGES, key=int):
        text = PAGES[pno]
        for form_name, hay, back in (('raw', text, None),
                                     ('nospace', re.sub(r'\s+', '', text), None)):
            for m in rx.finditer(hay):
                s = max(0, m.start() - context // 2)
                print(f'--- p.{pno} [{form_name}] ---')
                print(hay[s:m.end() + context // 2].replace('\n', ' '))
                print()
            if form_name == 'raw' and rx.search(hay):
                break   # raw hit is more readable; skip the nospace duplicate

if __name__ == '__main__':
    search(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 220)
