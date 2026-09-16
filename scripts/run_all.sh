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


# --- cycle 2 ---
./venv/bin/python scripts/10_parse_appendix_b.py  | tee data/derived/out_10.txt
./venv/bin/python scripts/11_build_readings.py    | tee data/derived/out_11.txt
./venv/bin/python scripts/12_check_readings.py    | tee data/derived/out_12.txt
./venv/bin/python scripts/13_known_cases.py       | tee data/derived/out_13.txt
./venv/bin/python scripts/14_counts.py            | tee data/derived/out_14.txt

# --- cycle 3 ---
# Part C needs a third download: data/raw/strongs-hebrew-dictionary.js
# (see reports/cycle-03.md for the URL and hash).
./venv/bin/python scripts/15_add_roots.py         | tee data/derived/out_15.txt
./venv/bin/python scripts/16_build_rules.py       | tee data/derived/out_16.txt
./venv/bin/python scripts/17_check_quotes.py      | tee data/derived/out_17.txt
node    scripts/18_dump_hebrew.js                 | tee data/derived/out_18.txt
./venv/bin/python scripts/19_build_hebrew_list.py | tee data/derived/out_19.txt
./venv/bin/python scripts/20_root_coverage.py     | tee data/derived/out_20.txt

# --- cycle 4 ---
./venv/bin/python scripts/21_matcher.py           | tee data/derived/out_21.txt
./venv/bin/python scripts/22_selftest.py          | tee data/derived/out_22.txt
./venv/bin/python scripts/23_rules_added.py       | tee data/derived/out_23.txt
./venv/bin/python scripts/24_freedom.py           | tee data/derived/out_24.txt

# --- cycle 5 ---
./venv/bin/python scripts/25_cycle5_setup.py      | tee data/derived/out_25.txt
./venv/bin/python scripts/26_cycle5_rankings.py   | tee data/derived/out_26.txt
./venv/bin/python scripts/27_cycle5_decisions.py  | tee data/derived/out_27.txt

# --- cycle 6 ---
./venv/bin/python scripts/28_cycle6_sets.py       | tee data/derived/out_28.txt
./venv/bin/python scripts/29_cycle6_match.py      | tee data/derived/out_29.txt

# --- cycle 7 ---
# Needs three more downloads into data/raw/ (see reports/cycle-07.md for URLs
# and hashes): ugaritic_lexicon.txt, google-10000-english-no-swears.txt, cmudict.dict
./venv/bin/python scripts/30_cycle7_lists.py      | tee data/derived/out_30.txt
./venv/bin/python scripts/31_cycle7_compare.py    | tee data/derived/out_31.txt
./venv/bin/python scripts/32_cycle7_throat.py     | tee data/derived/out_32.txt

# --- cycle 8 ---
./venv/bin/python scripts/33_cycle8_tightness.py  | tee data/derived/out_33.txt
echo "done"
