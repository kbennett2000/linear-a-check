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

**Cycle 3 ([reports/cycle-03.md](reports/cycle-03.md))** — write down the paper's
own spelling rules, record the Semitic root it gives for each reading, and build a
Hebrew word list to compare against later. The two tables are
[reports/cycle-03-readings.csv](reports/cycle-03-readings.csv) (cycle 2's table
plus `root`, `root_kind` and `languages`) and
[reports/cycle-03-rules.csv](reports/cycle-03-rules.csv) (66 rules).

**Cycle 4 ([reports/cycle-04.md](reports/cycle-04.md))** — build the matcher: code
that takes a Linear A word and lists every Hebrew root it could match under the
paper's own rules, then check it finds the paper's own readings.
[reports/cycle-04-selftest.csv](reports/cycle-04-selftest.csv) has one row per
reading tested, [reports/cycle-04-rules-added.csv](reports/cycle-04-rules-added.csv)
the seven rules that had to be added, and
[reports/cycle-04-formula-matches.csv](reports/cycle-04-formula-matches.csv) every
root the seven formula words can match.

No cycle so far draws any conclusion about the language.

## Credit

The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan Peak
Sanctuary Libation Formula"* (pre-print, September 2026),
DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321), released
under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Words, readings
and page references quoted in this repository are drawn from that paper and are
reused under that licence.

The corpus is the Linear A Explorer data (Hogan 2019–),
[mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz).

The Hebrew word list used from cycle 3 on is built from Strong's Hebrew dictionary
(James Strong, 1894, public domain), JSON edition by
[Open Scriptures](https://github.com/openscriptures/strongs), released under
CC BY-SA. The derived list is not committed.

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
