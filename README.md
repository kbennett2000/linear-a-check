# linear-a-check

A fair, staged test of the claims in Tom di Mino's September 2026 pre-print
*"Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula"*, which argues
that Linear A — the undeciphered script of Bronze Age Crete — records a Semitic
language.

Linguists have not confirmed that claim. This project neither assumes it is right
nor assumes it is wrong. It works in small cycles, each with a written report, and
reports matches as plainly as mismatches.

**Cycle 1 ([reports/cycle-01.md](reports/cycle-01.md))** — gather the sources and
re-count the numbers the paper states about the corpus.

**Cycle 2 ([reports/cycle-02.md](reports/cycle-02.md))** — list every reading the
paper prints and check each word is in the inscription the paper cites. The table
itself is [reports/cycle-02-readings.csv](reports/cycle-02-readings.csv).

Neither cycle draws any conclusion about the language.

## Credit

The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan Peak
Sanctuary Libation Formula"* (pre-print, September 2026),
DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321), released
under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Words, readings
and page references quoted in this repository are drawn from that paper and are
reused under that licence.

The corpus is the Linear A Explorer data (Hogan 2019–),
[mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz).

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
