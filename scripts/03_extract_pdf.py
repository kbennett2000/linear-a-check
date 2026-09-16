#!/usr/bin/env python3
"""Extract the paper's text, one file per page, so later scripts can quote
page numbers accurately."""
import os, json
import pdfplumber

PDF = 'data/raw/ya-diktu.pdf'
OUT = 'data/derived/paper_text.txt'
pages = []
with pdfplumber.open(PDF) as pdf:
    for i, p in enumerate(pdf.pages, start=1):
        pages.append((i, p.extract_text() or ''))

with open(OUT, 'w') as f:
    for i, t in pages:
        f.write(f'\n===== PAGE {i} =====\n{t}\n')
json.dump({str(i): t for i, t in pages}, open('data/derived/paper_pages.json', 'w'))
print(f'pages: {len(pages)}  chars: {sum(len(t) for _, t in pages)}')
