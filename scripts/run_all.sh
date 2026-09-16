#!/usr/bin/env bash
# Runs the whole cycle-1 pipeline in order. Assumes data/raw/ already holds the
# two downloads (see reports/cycle-01.md for URLs and hashes) and that ./venv
# exists with pdfplumber installed.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/derived
node    scripts/01_dump_corpus.js        | tee data/derived/out_01.txt
./venv/bin/python scripts/02_known_answer_check.py | tee data/derived/out_02.txt
./venv/bin/python scripts/03_extract_pdf.py        | tee data/derived/out_03.txt
./venv/bin/python scripts/05_star301.py            | tee data/derived/out_05.txt
./venv/bin/python scripts/06_formula.py            | tee data/derived/out_06.txt
./venv/bin/python scripts/07_ab79_and_314.py       | tee data/derived/out_07.txt
./venv/bin/python scripts/08_vowels.py             | tee data/derived/out_08.txt
./venv/bin/python scripts/09_corpus_size.py        | tee data/derived/out_09.txt
echo "done"
