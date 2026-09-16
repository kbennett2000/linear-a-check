# Cycle 9 — do the tight readings survive without the rules written for them?

**Date run:** 16 September 2026
**Scope:** one check, aimed at this project's own conclusion. Cycle 8 found that
under the stated-only rule set some readings are very tight, and
`reports/SUMMARY.md` called that "the clearest single conclusion of the project"
and a point in the paper's favour. **That was overstated, and this cycle shows
why.** Some of the stated rules those readings use are introduced in the very
passage that reads the word, so part of the tightness is built in. **No claim is
made here about whether Linear A is or is not a Semitic language.**

Files written: `reports/cycle-09-own-passage.csv`,
`scripts/34_cycle9_own_passage.py`. `reports/SUMMARY.md`,
`reports/cycle-08.md`, `reports/cycle-01.md` and `README.md` were updated (§4).

**Settings.** The stated-only rule set exactly as in cycle 8, the same batches of
made-up words (seed **20260916**), and the same site handling.

**Terms used below, defined on first use.** A **passage** is one numbered section
of the paper, including its footnotes and tables, or one entry of Appendix B. An
**own-passage rule** for a reading is a rule the paper states **nowhere except**
in that reading's own passage. A rule the paper also states somewhere else is
not own-passage, however often it appears in the reading's own passage. Terms
from cycles 1–8 — root, options, chance, rule set, stated-only, site — are not
redefined.

**Known-answer check.** Before anything was switched off, all 31 readings were
re-measured with every stated rule on. All 31 reproduce cycle 8's options and
chance **exactly**, to four decimal places.

---

## 1. Step 1 — finding each reading's own-passage rules

The `where` column of `reports/cycle-03-rules.csv` and
`reports/cycle-04-rules-added.csv` lists every place the paper states each rule.
Those strings were turned into sets of passages, and a rule counts as
own-passage for a reading when that set has exactly one member and it is the
reading's own passage.

### Judgment calls

The brief asked for these to be written down. Six had to be made.

**1. Bare footnote citations.** Some rules are cited as "n.30, p.17" with no
section. Which section that is was settled from the paper's own `§n.` headings:
§7 starts on p.14, §8 on p.16, §9 on p.18. So n.29 and n.30 (p.17) fall inside
**§8**, n.23 (p.15) inside §7, n.18 (p.12) inside §6.1, and n.41 (p.21) inside
§10. Only n.30 matters here: it is the sole statement of **R29**, that `*314`
writes ḥ, and it lands in the same section as the reading DU-\*314-RE.

**2. R01 and R05–R08 are never own-passage**, as the brief directs. R05–R08 are
the general sound rules stated together on p.19, which is §9. Exactly one
reading — DU-PU₂-RE — sits in §9, so this exclusion changes that one reading's
outcome and nobody else's.

**3. R11 had to be split in two.** R11 states two different things in two
different places: the T-series also writes **ṣ** (§6.1, p.12) and it also writes
**ṯ** (Appendix B, pp.36–40). Treated as one rule it would never be
own-passage, and TA-NA-RA-TE-U-TI-NU — read in §6.1, with ṣ in its root — would
count as independent although its sound value is stated exactly where the word
is read. So R11 is treated as **R11ṣ** (§6.1 only) and **R11ṯ** (Appendix B). This
is the one place where the mechanical test was overridden, and it was overridden
in the direction that is harder on the paper.

**4. R11 is credited only when its extra value was actually needed.** The
matcher records the whole T-series rule set whenever any T-sign is used, so R11
appears in the rule list of readings that never needed it. R11ṣ is counted only
when the root contains ṣ, R11ṯ only when it contains ṯ.

**5. Appendix B statements that span the whole appendix are not "the same
entry".** R11ṯ is cited at Appendix B pp.36, 38, 39 and 40 — many entries, not
one — so it is not own-passage for any single entry. This is the only place the
entry-level definition of a passage could have bitten. It does not bite
elsewhere: every other stated rule used by an Appendix B reading is also stated
outside Appendix B, so no entry-level attribution was needed. Note that the
self-test's `where` column gives Appendix B readings as "Appendix B, pp.36–40",
the whole appendix, so entry-level comparison was not available from the data as
recorded.

**6. Rules stated in several places are not own-passage even when one of those
places is the reading's own.** This is the brief's definition and it matters. The
prefixes behind A-TA-I-\*301-WA-JA are a case in point: **R37** (A-) is stated at
§4.1 *and* in Appendix B; **R39** (TA-) at §4.1 *and* §6.1; **R41** (I-) at §4.1,
§5.2 *and* Appendix B. All three are first stated in §4.1, the section that reads
the verb — but because the paper also states them elsewhere, none counts as
own-passage. That is the generous reading, and it is the one used.

### The result

**11 of the 31 readings use at least one own-passage rule.**

| reading | root | passage | own-passage rules |
|---|---|---|---|
| A-TA-I-\*301-WA-JA | n-w-y | §4.1 | **R25** (`*301` = na) |
| \*301-SI | n-ś-ʾ | §4.1 | **R25** |
| JA-DI-KI-TU | d-q-q | §4.2 | **N01** (-TU is the feminine ending) |
| JA-SA-SA-RA-ME | y-š-r | §4.3 | **R17**, **R18** (a doubled sign; a doubled SA = š) |
| SA-SA-RA-ME | y-š-r | §4.3 | **R17**, **R18** |
| A-SA-SA-RA | y-š-r | §4.3 | **R17**, **R18** |
| U-NA-KA-NA-SI | k-n-s | §5.1 | **R42** (U-NA- = hunna) |
| U-NA-RU-KA-NA-SI | k-n-s | §5.1 | **N03** (RU = lū), **R42** |
| RA-KI-NI-SE | k-n-s | §5.1 | **R44** (RA- = la-) |
| TA-NA-RA-TE-U-TI-NU | r-ṣ-y | §6.1 | **R11ṣ** (the T-series also writes ṣ) |
| DU-\*314-RE | ḥ-r-r | §8 | **R29** (`*314` = ḥ), **R46** (DU- = dū) |

The brief's examples come out as it expected for §5.1 — R42, R44 and the RU
rule are stated only there — and differently for §4.1, where the prefixes turn
out to be stated elsewhere as well, but the **sign value R25** is not.

---

## 2. Step 2 — switching them off

For each reading, only its own-passage rules were switched off. Every other
stated rule stayed on. Then cycle 8's measurements were run again.

**The result is uniform: none of the 11 survives.**

| reading | root | switched off | survives | options | chance |
|---|---|---|---|---|---|
| A-TA-I-\*301-WA-JA | n-w-y | R25 | **no** — needs R25 | — | — |
| \*301-SI | n-ś-ʾ | R25 | **no** — needs R25 | — | — |
| JA-DI-KI-TU | d-q-q | N01 | **no** — needs N01 | — | — |
| JA-SA-SA-RA-ME | y-š-r | R17 R18 | **no** — needs R17 | — | — |
| SA-SA-RA-ME | y-š-r | R17 R18 | **no** — needs R17 | — | — |
| A-SA-SA-RA | y-š-r | R17 R18 | **no** — needs R17 | — | — |
| U-NA-KA-NA-SI | k-n-s | R42 | **no** — needs R42 | — | — |
| U-NA-RU-KA-NA-SI | k-n-s | N03 R42 | **no** — needs both | — | — |
| RA-KI-NI-SE | k-n-s | R44 | **no** — needs R44 | — | — |
| TA-NA-RA-TE-U-TI-NU | r-ṣ-y | R11ṣ | **no** — needs R11ṣ | — | — |
| DU-\*314-RE | ḥ-r-r | R29 R46 | **no** — needs both | — | — |
| A-TA-I-\*301-WA-E | n-w-y | (none) | yes | 4 | 0.0% |
| A-TA-I-NA-WA-JA | n-w-y | (none) | yes | 5 | 0.0% |
| SI-KI-NE | š-k-n | (none) | yes | 2 | 0.3% |
| KI-DA-RO | q-d-r | (none) | yes | 6 | 0.4% |
| A-SI-KI-RA | š-k-r | (none) | yes | 11 | 0.3% |
| SI-KI-RA | š-k-r | (none) | yes | 11 | 0.0% |
| A-DI-KI-TE-TE | d-q-q | (none) | yes | 12 | 0.3% |
| JA-DI-KI-TE-TE | d-q-q | (none) | yes | 12 | 0.3% |
| U-NA-RU-KA-NA-TI | k-n-s | (none) | yes | 12 | 0.0% |
| A-JA | ḥ-y-y | (none) | yes | 12 | 0.8% |
| TA-NA-I-\*301-TI | ʿ-n-y | (none) | yes | 37 | 0.3% |
| TA-NA-I-\*301-U-TI-NU | ʿ-n-y | (none) | yes | 38 | 0.0% |
| TA-NA-I-NA-U-TI-NU | ʿ-n-y | (none) | yes | 38 | 0.0% |
| JA-SU-MA-TU | š-m-ṭ | (none) | yes | 42 | 0.3% |
| DU-PU₂-RE | d-b-r | (none) | yes | 43 | 0.3% |
| JA-SA-RA | y-š-r | (none) | yes | 46 | 0.3% |
| SI-RU-TE | š-r-t | (none) | yes | 52 | 0.0% |
| TA-NA-TE | ṯ-n-n | (none) | yes | 101 | 3.8% |
| A-NA-NE | ḥ-n-n | (none) | yes | 3 | 3.8% |
| I-PI-NA-MA | p-n-y | (none) | yes | 4 | 0.7% |

**20 of 31 survive — and they are exactly the 20 that had nothing to switch off.
Every reading that used a rule stated only in its own passage depended on that
rule.** Not one of the eleven had a second route to its root.

### The readings that pass the independent check

These survive with **10 or fewer options and a chance of 0.5% or less**: they
rest only on rules the paper states somewhere other than where it reads them.

| word | root | meaning given | where read | options | chance |
|---|---|---|---|---|---|
| A-TA-I-\*301-WA-E | n-w-y | the invocation verb | §8 table, p.16 | 4 | 0.0% |
| A-TA-I-NA-WA-JA | n-w-y | "I make myself a dwelling" | §7 table, p.14 | 5 | 0.0% |
| SI-KI-NE | š-k-n | *šikinēt*, a recipient title | §7, p.14 | 2 | 0.3% |
| KI-DA-RO | q-d-r | "pot" | Appendix B | 6 | 0.4% |

**Four readings, and they need reading carefully.** Two of the four are the same
invocation verb, restated in the paper's own translation table (§7) and
cross-site table (§8). Those tables summarise the readings argued in §4–§6, so
calling them a different passage is true by the mechanical test but thin as
independent evidence. What is genuinely independent about them is narrower and
still worth something: **A-TA-I-NA-WA-JA spells the fourth sign `NA` rather than
`*301`**, so it does not need R25 at all, and A-TA-I-\*301-WA-E is read in a
section that is not where `*301`'s value is established. On the corpus's own
spellings the verb can be reached without the rule that was written for it.

That leaves **two readings outside the formula** — SI-KI-NE and KI-DA-RO — as the
clean cases: ordinary words, read elsewhere in the paper, reachable on rules
stated for other words, matching 2 and 6 Hebrew roots respectively, and matched
by 0.3% and 0.4% of made-up words of their length.

---

## 3. What this means, in plain words

**A reading that survives rests on rules the paper stated for other words.** The
fit was not written into the rule, so its tightness is evidence of something
outside itself. That is the closest thing this project has to an independent
check, and four readings pass it.

**A reading that does not survive may still be perfectly right.** Nothing here
says R42 is wrong, or that *hunna* is not the reading of U-NA-. What it says is
narrower: **the tightness of that reading cannot be counted as independent
support**, because the rule that makes it tight was introduced to read that word.
The reading and the rule are one claim, not two.

**This changes cycle 8's headline.** Cycle 8 highlighted three readings —
U-NA-RU-KA-NA-SI, U-NA-KA-NA-SI and RA-KI-NI-SE — that match exactly one Hebrew
root, k-n-s, and `reports/SUMMARY.md` called that the clearest conclusion of the
project and a point in the paper's favour. **All three depend on rules stated
only in §5.1, the section that reads them.** R42 (U-NA- = *hunna*), N03 (RU =
*lū*) and R44 (RA- = *la-*) are all introduced there. Their tightness is partly
built in, and the write-up should not have leaned on it. It has been corrected.

Two things should be said on the other side, to be fair.

* **The fourth k-n-s reading does survive.** U-NA-RU-KA-NA-TI is read in the §8
  table, so for that reading R42 and N03 are stated elsewhere. It survives with
  12 options and a chance of 0.0%. The k-n-s family is not left with nothing.
* **Eleven failures out of 31 is not a general indictment.** Twenty readings use
  no own-passage rule at all. The paper mostly does state its rules in more than
  one place, and where it does, the readings stand on their own.

---

## 4. Step 3 — what was changed in the write-up

Only the items the brief lists.

* **`reports/SUMMARY.md` §6** — the own-passage result added; "the clearest
  single conclusion of the project" and "runs in the paper's favour" replaced
  with what Step 2 supports.
* **`reports/SUMMARY.md` "A last word"** — adjusted to match.
* **`reports/SUMMARY.md` §9, suggestion 2** — adjusted, with the addition that
  the strongest version of this evidence would be rules stated in one place that
  correctly predict readings somewhere else.
* **`reports/SUMMARY.md` §5, cycle 4** — "about 190 Hebrew roots" applied to the
  words the paper reads (median 188). Across all 787 readable corpus words cycle
  6 found a median of about 120. Both figures are now given.
* **`reports/SUMMARY.md` §8 rows 1 and 2** — dated 17 September 2026; cycle 2 ran
  on 16 September. Corrected. The same wrong date inside the cycle 2 correction
  note at the top of `reports/cycle-01.md` is corrected too.
* **`reports/SUMMARY.md` §8** — a row added for this cycle, recording that the
  write-up overstated the stated-only result.
* **`reports/cycle-08.md` §2** — a dated note added next to "This is the
  strongest result in the cycle."
* **`reports/SUMMARY.md`** cycle table and **`README.md`** — cycle 9 added.

## 5. Reproducing this cycle

```
bash scripts/run_all.sh        # scripts 01-34, in order
```

`scripts/34_cycle9_own_passage.py` writes `reports/cycle-09-own-passage.csv`, one
row per reading, 31 rows. Columns: `word`, `root`, `where`, `passage`,
`n_signs`, `site`, `rules_used`, `own_passage_rules`, `survives`,
`base_options`, `base_chance`, `new_options`, `new_chance`, `blocker`.

## Credit

The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan Peak
Sanctuary Libation Formula"* (pre-print, September 2026),
DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321), CC BY 4.0.
Full credits for every data source are in [`reports/SUMMARY.md`](SUMMARY.md) §2.
