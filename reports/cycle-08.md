# Cycle 8 — how tight is each reading, and the write-up

**Date run:** 16 September 2026
**Scope:** the last planned cycle. It does two things: it measures how tight each
of the paper's readings is, and it writes the whole project up in plain English
as [`reports/SUMMARY.md`](SUMMARY.md). **No claim is made here about whether
Linear A is or is not a Semitic language.**

Files written: `reports/cycle-08-readings.csv`, `reports/SUMMARY.md`,
`scripts/33_cycle8_tightness.py`. `reports/cycle-07.md` and `README.md` were
corrected (§1).

**Settings.** Both rule sets, prefixes and suffixes on, R32 on in the full set,
R62 and R63 limited to Palaikastro and Zakros as in cycle 5, seed **20260916**.

**Terms used below, defined on first use.** **Chance** is the share of made-up
words of the same length that can also be read as a given root; a **low** chance
means the reading is **tight**, because most words that length cannot be read
that way. **Options** is the opposite measure: how many Hebrew primitive roots
the word matches at all, which is how much freedom the rules left when the root
was picked. A **batch** is one shared set of 1,000 made-up words, drawn once per
word length so that every reading of that length is judged against the same
words. Terms from cycles 1–7 — root, skeleton, primitive root, throat consonant,
rule set, coverage, median, Linear A-like — are not redefined.

---

## 1. Step 0 — the licence correction

`README.md` and `reports/cycle-07.md` both said the English word list
([first20hours/google-10000-english](https://github.com/first20hours/google-10000-english))
was under an "MIT licence". That was wrong. Its `LICENSE.md` was downloaded and
read (723 bytes, SHA-256
`28a336d4f14838b169fda9c4c26ede12ebe79abee9ae3e890bfa3ade865735c6`). It says:

* the data is derived from the **Google Web Trillion Word Corpus** (Thorsten
  Brants and Alex Franz), distributed by the **Linguistic Data Consortium**,
  with subsets released by Peter Norvig and corpus editing by Josh Kaufman;
* educational and personal/research use is permitted under the LDC licence,
  Norvig's MIT licence **for his own contributions only**, and US fair use;
* commercial use is **not recommended** without licensing the data from the LDC.

Both credit lines now say that. A dated correction note has been added to the top
of `reports/cycle-07.md`. Nothing else in either file was changed. This project
uses the list for research only.

---

## 2. Step 1 — how tight is each reading?

### What was measured

Cycle 4's self-test (`reports/cycle-04-selftest.csv`) has 111 rows. **86 are
readings the matcher found.** Those 86 rows cover **55 distinct word-and-root
readings** across **52 distinct words** — the paper prints some readings more
than once, in the main text and again in a table or in Appendix B, and each
printing is its own row. `reports/cycle-08-readings.csv` keeps all 86 rows for
each rule set (172 rows); the tables below count **distinct readings**, since a
reading printed twice is not two pieces of evidence.

For each reading, under each rule set:

1. **Reachable** — does the word still match its root with these rules?
2. **Options** — how many Hebrew primitive roots the word matches at all.
3. **Chance** — the share of 1,000 made-up Linear A-like words of the same
   length that can also be read as that root.

Each reading was given **the site of the inscription the paper cites for it**, so
R62 and R63 apply to the made-up words exactly as they do to the real one. Every
one of the 86 rows has a site.

### Choices this step had to make

* **The batches are drawn with repeats allowed**, so each is exactly 1,000 draws.
  A batch is a sample used to estimate a share, so a word drawn twice should
  count twice. It also matters at two signs, where there are not 1,000 distinct
  made-up words to be had: that batch has 1,000 draws over 418 distinct words.
  The longer batches are nearly all distinct (3 signs: 920; 5 signs and up: 1,000).
* **What counts as "this reading's root".** As cycle 7's Step 3 did, the chance
  test uses no dictionary and no sound correspondences: the target is the root as
  the paper writes it. Where cycle 3 recorded a second spelling of the *same*
  root — Hebrew writes p-n-h where the paper writes p-n-y — **both** spellings
  count. Without that, the real word would fail its own test, and the chance
  would be measuring something no word in the corpus does. This affects 27 of the
  86 rows.
* **Seven readings could not be scored** and are marked as such rather than
  guessed at. In each, the paper reads only *part* of the word as that root —
  rule N07, compounds — and a test against one root cannot express "some run of
  signs inside this word spells this root" without also saying what the rest of
  the word is. They are: A-MI-DA-O/ʿ-m-m, A-PA-RA-NE/ʿ-b-r, I-NA-JA-PA-QA/p-q-ḥ,
  I-NA-JA-RE-TA/y-r-ʾ, I-PI-NA-MI-NA/p-n-y, NA-TU-*301-NE/n-t-n and
  PA-RA-NE/ʿ-b-r. Where the paper records roots for **both** halves — A-MI-DA-U
  and JA-SA-SA-RA-MA-NA — the test works and those readings are scored.

### How many readings survive with only the stated rules

| | full rule set | stated only |
|---|---|---|
| distinct readings | 55 | 55 |
| **reachable** | **53** (96%) | **31** (56%) |
| scored | 46 | 31 |
| chance — median | 0.35% | 0.30% |
| chance — range | 0.0% – 7.8% | 0.0% – 4.2% |
| readings no made-up word could match | 5 | 10 |
| **options — median** | **189** | **12** |
| options — range | 43 – 299 | 1 – 101 |

Two readings are lost under the full rule set once each reading is held to its
own site: **A-MI-DA-O** (Phaistos, so the Palaikastro rule R62 cannot apply) and
**A-SA-SA-RA-ME** (the corpus attests that spelling only at Iouktas). Cycle 5
already reported both.

**Just over half the readings — 31 of 55 — survive on the paper's stated rules
alone.** The other 24 need at least one rule the paper uses without stating it.

### The ten tightest and the ten loosest

**Full rule set** (46 scored readings):

| | word | root | signs | chance | options |
|---|---|---|---|---|---|
| tightest | A-NA-NU-SI-JA-SE | ʿ-n-n | 6 | 0.0% | 138 |
| | A-TA-I-\*301-DE-KA | ʿ-n-y | 6 | 0.0% | 251 |
| | JA-SA-SA-RA-MA-NA | y-š-r | 6 | 0.0% | 248 |
| | TA-NA-I-\*301-U-TI-NU | ʿ-n-y | 7 | 0.0% | 171 |
| | TA-NA-I-NA-U-TI-NU | ʿ-n-y | 7 | 0.0% | 171 |
| | A-TA-I-\*301-WA-E | n-w-y | 6 | 0.1% | 162 |
| | A-TA-I-\*301-WA-JA | n-w-y | 6 | 0.1% | 163 |
| | A-TA-I-NA-WA-JA | n-w-y | 6 | 0.1% | 163 |
| | I-TI-TI-KU-NI | n-t-k | 5 | 0.1% | 290 |
| | JA-SA-SA-RA-MA-NA | m-n-y | 6 | 0.1% | 248 |
| loosest | A-MI-DA-U | y-d-ʿ | 4 | 7.8% | 111 |
| | DU-\*314-RE | ḥ-r-r | 3 | 6.0% | 94 |
| | TA-NA-TE | ṯ-n-n | 3 | 4.2% | 163 |
| | I-NA-TA | ʿ-n-y | 3 | 4.2% | 150 |
| | A-NA-NE | ḥ-n-n | 3 | 4.2% | 43 |
| | RU-MA-TA | r-w-m | 3 | 3.9% | 189 |
| | A-MI-DA-U | ʿ-m-m | 4 | 3.7% | 111 |
| | A-RI-NI-TA | ʾ-r-y | 4 | 3.1% | 189 |
| | I-ZU-RI-NI-TA | ṯ-w-r | 5 | 2.4% | 140 |
| | ZU-RI-NI-MA | ṯ-w-r | 4 | 2.3% | 113 |

**Stated-only rule set** (31 scored readings):

| | word | root | signs | chance | options |
|---|---|---|---|---|---|
| tightest | A-TA-I-\*301-WA-E | n-w-y | 6 | 0.0% | 4 |
| | A-TA-I-\*301-WA-JA | n-w-y | 6 | 0.0% | 5 |
| | A-TA-I-NA-WA-JA | n-w-y | 6 | 0.0% | 5 |
| | SI-KI-RA | š-k-r | 3 | 0.0% | 11 |
| | SI-RU-TE | š-r-t | 3 | 0.0% | 52 |
| | TA-NA-I-\*301-U-TI-NU | ʿ-n-y | 7 | 0.0% | 38 |
| | TA-NA-I-NA-U-TI-NU | ʿ-n-y | 7 | 0.0% | 38 |
| | TA-NA-RA-TE-U-TI-NU | r-ṣ-y | 7 | 0.0% | 90 |
| | U-NA-RU-KA-NA-SI | k-n-s | 6 | 0.0% | **1** |
| | U-NA-RU-KA-NA-TI | k-n-s | 6 | 0.0% | 12 |
| loosest | DU-\*314-RE | ḥ-r-r | 3 | 4.2% | 9 |
| | TA-NA-TE | ṯ-n-n | 3 | 3.8% | 101 |
| | A-NA-NE | ḥ-n-n | 3 | 3.8% | 3 |
| | SA-SA-RA-ME | y-š-r | 4 | 0.9% | 47 |
| | JA-DI-KI-TU | d-q-q | 4 | 0.9% | 12 |
| | A-SA-SA-RA | y-š-r | 4 | 0.9% | 46 |
| | A-JA | ḥ-y-y | 2 | 0.8% | 12 |
| | I-PI-NA-MA | p-n-y | 4 | 0.7% | 4 |
| | RA-KI-NI-SE | k-n-s | 4 | 0.6% | **1** |
| | KI-DA-RO | q-d-r | 3 | 0.4% | 6 |

Under the stated-only set the "loosest" end is not loose at all: seventeen of the
31 readings sit below 1%.

### Where the seven formula words fall

| word | root | full: chance / options / place | stated only: chance / options / place |
|---|---|---|---|
| A-TA-I-\*301-WA-JA | n-w-y | 0.1% / 163 / **7th of 46** | 0.0% / 5 / **2nd of 31** |
| JA-DI-KI-TU | d-q-q | 1.2% / 224 / 32nd | 0.9% / 12 / 27th |
| JA-SA-SA-RA-ME | y-š-r | 0.3% / 224 / 21st | 0.2% / 47 / 12th |
| U-NA-KA-NA-SI | k-n-s | 0.2% / 182 / 16th | 0.1% / **1** / 11th |
| I-PI-NA-MA | p-n-y | 0.9% / 131 / 29th | 0.7% / 4 / 24th |
| SI-RU-TE | š-r-t | 1.2% / 201 / 34th | 0.0% / 52 / **5th** |
| TA-NA-RA-TE-U-TI-NU | r-ṣ-y | 0.5% / 238 / 27th | 0.0% / 90 / **8th** |

The seven are **spread through the range, not clustered at the tight end**. Under
the full rule set their median place is 27th of 46 — the middle. Under the
stated-only set they do better, median 11th of 31, with three in the top eight.
The formula words are not the paper's tightest readings on this measure; several
words outside the formula fit more tightly than they do.

### The three readings with no freedom at all

This is the strongest result in the cycle, and it runs in the paper's favour.

Under the **stated-only** rule set, three readings match **exactly one** Hebrew
primitive root — and in each case it is the root the paper gives:

| word | root | options | chance |
|---|---|---|---|
| U-NA-RU-KA-NA-SI | k-n-s | 1 | 0.0% |
| U-NA-KA-NA-SI | k-n-s | 1 | 0.1% |
| RA-KI-NI-SE | k-n-s | 1 | 0.6% |

Seven readings in all have a chance of 0.5% or less **and** ten options or fewer:
the three above plus A-TA-I-\*301-WA-JA, A-TA-I-\*301-WA-E, A-TA-I-NA-WA-JA
(n-w-y, 4–5 options) and KI-DA-RO (q-d-r, 6 options). For those seven, there was
almost nothing to choose from and almost no made-up word could have produced the
same reading.

Under the full rule set **no reading has fewer than 43 options**, and 71 of the 76
scored rows have 100 or more. The extra rules the paper uses without stating
them are what destroy the tightness.

---

## 3. What these numbers mean, and what they do not

**A low chance means the fit is tight.** If 0.1% of made-up six-sign words can be
read as n-w-y, then reading A-TA-I-\*301-WA-JA that way is not something any word
would give you. That is a real observation and it is worth having.

**But a tight fit is not proof, because the root was chosen after the word was
seen.** Under the full rule set the median reading's word matches **189** Hebrew
primitive roots. The paper did not have to predict n-w-y in advance; it could
look at the word, see what the rules allowed, and pick the one that made sense.
Picking one outcome out of 189 and then observing that this particular outcome is
rare is not surprising — it is what choosing from 189 candidates looks like. The
rarity is in the naming, not in the fit.

**This is exactly why the stated-only column matters.** There the median is **12**
options, not 189, and for three readings it is **1**. When there is only one root
the word can be read as, the choice was not free, and the tightness means
something. The measurement therefore says something fairly precise: **the paper's
readings carry real evidential weight where they rest on its stated rules, and
very little where they need the unstated ones.**

### Why the chances must not be multiplied together

It is tempting to multiply the 46 chances into one number. That number would be
around 10⁻¹²⁰ and it would be meaningless. Four reasons, any one of which is
fatal:

1. **The readings are not independent.** Seven of them use the root ʿ-n-y, four
   use k-n-s, five use y-š-r. Several are the same word with a different ending.
   Multiplying assumes each is a fresh, unrelated draw. They are not.
2. **The roots were chosen after the words were seen.** A product is the right
   tool for predictions made in advance. These are not predictions.
3. **The set of readings is itself selected.** The paper prints the readings that
   worked. Multiplying over a sample chosen for success measures the selection,
   not the language.
4. **Five of the chances are exactly zero**, so the product is zero — which
   would only reveal that the batch size of 1,000 sets a floor, not that the odds
   are nil.

A single number would look like overwhelming proof while measuring none of the
things that would make it proof. The table is the result; there is no summary
statistic behind it.

---

## 4. Open items

Carried into [`reports/SUMMARY.md`](SUMMARY.md) §10: the full 508-entry word list
once it is released, a test that judges meaning, and a closer copy of Linear A's
sign patterns for the made-up words.

## 5. Reproducing this cycle

```
bash scripts/run_all.sh        # scripts 01-33, in order
```

`scripts/33_cycle8_tightness.py` writes `reports/cycle-08-readings.csv`: one row
per reading per rule set, 172 rows. Columns: `word`, `where`, `root`,
`rule_set`, `n_signs`, `site`, `reachable`, `options`, `chance`, `rank`, `note`.

## Credit

The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan Peak
Sanctuary Libation Formula"* (pre-print, September 2026),
DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321), CC BY 4.0.
Full credits for every data source are in [`reports/SUMMARY.md`](SUMMARY.md) §2.
