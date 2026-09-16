# linear-a-check

A fair, staged test of the claims in Tom di Mino's September 2026 pre-print
*"Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula"*, which argues
that Linear A — the undeciphered script of Bronze Age Crete — records a Semitic
language.

Linguists have not confirmed that claim. This project neither assumes it is right
nor assumes it is wrong. It works in small cycles, each with a written report, and
reports matches as plainly as mismatches.

**Cycle 1 ([reports/cycle-01.md](reports/cycle-01.md))** — gather the sources and
re-count the numbers the paper states about the corpus. No judgements about the
language.

## Layout

- `scripts/` — analysis scripts, numbered in the order they run (`scripts/run_all.sh`
  runs the lot)
- `reports/` — one report per cycle
- `data/` — downloads and derived tables. **Not committed** (see `.gitignore`); the
  reports record every download URL with its size and SHA-256 so anyone can rebuild
  `data/` themselves.

## Reproducing

```
node scripts/01_dump_corpus.js     # needs data/raw/LinearAInscriptions.js
python3 -m venv venv && ./venv/bin/pip install pdfplumber
bash scripts/run_all.sh
```
