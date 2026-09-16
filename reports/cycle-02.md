# Cycle 2 — every reading the paper prints, checked against the corpus

**Date run:** 17 September 2026
**Scope:** build a table of every Linear A word the paper gives a reading or a
meaning for, then check each one against the corpus file from cycle 1. Plus a fix
to a mistake in cycle 1's report. **No conclusions about the language are drawn in
this cycle**, and none should be read into it.

The table itself is [reports/cycle-02-readings.csv](cycle-02-readings.csv)
(167 rows, UTF-8).

**Credit.** The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan
Peak Sanctuary Libation Formula"* (pre-print, September 2026), DOI
`10.5281/zenodo.22730321`, released under CC BY 4.0. The words, readings and page
references quoted here are drawn from that paper and reused under that licence.
The corpus is the Linear A Explorer data (Hogan 2019–).

Terms used below, defined on first use. A **sign-group** is what Linear A scholars
call a written word: a run of signs between two dividers. A **word divider** is the
little upright stroke (𐄁) Minoan scribes put between words. A **hapax legomenon**
(plural *hapax legomena*) is a word that occurs exactly once in the whole surviving
corpus. An **allograph** is a second sign writing the same sound as an existing one.
Terms defined in cycle 1 — syllabogram, logogram, transliteration, ligature,
attestation — are not redefined here.

---

## 1. Step 0 — correcting cycle 1

**The correction has been made, and a dated note added at the top of
`reports/cycle-01.md`. Nothing else in that report was changed.**

Cycle 1, section 1.3, said the paper "contains a 508-entry lexicon as **Appendix B,
inside the PDF** (pp. 36–40), not as a separate data file." That was wrong on both
counts. Both passages were checked:

> "…welcome his input on a 508-entry lexicon, 42 resolved signs, and 443 full
> translations that I have tested and amassed in the authoring of this paper."
> — end of §9, p. 20

That is the only mention of the 508-entry lexicon in the paper, and it is a
*mention*: the lexicon is never printed.

> "In formal response to Davis (2026), I have included a comprehensive appendix of
> **67 Linear A sign-groups** matching his own. Of these, 39 (58.2%) are hapax
> legomena." — footnote 36, p. 20

> "**Appendix B: Index of Linear A Sign-Groups Cited in Davis 2026.** The list below
> corresponds to the **66 sign-groups in Davis's appendix** (2026, 58–60) and **one
> word in his body**, with signs transliterated using Linear B homomorph values."
> — opening paragraph of Appendix B, p. 36

So Appendix B is 66 + 1 = 67 sign-groups from Davis 2026, not a 508-entry lexicon.
Our own parse of Appendix B recovers **exactly 67 entries** (section 3 below),
which independently confirms the paper's count.

Why the error mattered: it wrongly implied the 508-entry lexicon was already in
hand. It is not, and as far as we can see it remains unpublished — which makes it
a live candidate for whatever the Zenodo record holds.

## 2. Step 1 — Zenodo, tried once more

**Still no answer.** Both records were tried once each, as instructed:

| Record | URL | Result |
|---|---|---|
| The paper | `https://zenodo.org/api/records/22730321` | HTTP 504 Gateway Timeout |
| Earlier version (from DataCite's `IsVersionOf`) | `https://zenodo.org/api/records/21903481` | HTTP 504 Gateway Timeout |

Same failure as cycle 1, where it was established that zenodo.org is unreachable
from this machine over both IPv4 and IPv6, inside and outside the sandbox, while
other hosts respond normally. No files were downloaded. **No file addresses were
guessed.** The file list for both records remains **unknown**, and one successful
fetch of either API URL from a machine that can reach Zenodo would settle it.

## 3. Step 2 — the readings table

**167 rows, 114 distinct words.** One row for each word in each place the paper
gives it a reading or a meaning, so a word read in both the main text and Appendix
B gets two rows; the distinct-word count handles the overlap.

| Part of the paper | rows |
|---|---|
| Appendix B (pp. 36–40) | 67 |
| Main text (§4–§10) | 38 |
| §8 cross-site table (p. 16) | 33 |
| Footnotes | 10 |
| §7 translation table (p. 14) | 8 |
| Appendix A (p. 36) | 7 |
| Appendix A, the AB79 note (p. 36) | 4 |
| **Total** | **167** |

Appendix B's 67 entries were parsed automatically (`scripts/10_parse_appendix_b.py`);
everything else was transcribed by hand, because the main text and footnotes give
readings in running prose rather than in a fixed format.

**Confidence labels.** The paper uses its four labels in exactly one place —
Appendix A's table for KN Zc 7 (p. 36). Nowhere else in the paper does any of the
four words appear.

| Label | rows |
|---|---|
| CONFIRMED | 1 |
| PROBABLE | 3 |
| CANDIDATE | 2 |
| SPECULATIVE | 1 |
| *(none given)* | 160 |

**What was left out, and why.**

- **Appendix C (pp. 40–42).** Its two spells are Egyptian group-writing from the
  London Medical Papyrus, not Linear A. The paper is explicit about this.
- **Linear B forms quoted for comparison** — `da-pu2-ri-to`, `po-ti-ni-ja`,
  `a-ka-wi-ja`, `su-ki-ri-to`, `ta-na-to` and others. The paper marks them as
  Linear B: "Were it Linear A, we would read ʾa-ḫa-wi-ya" (p. 21).
- **Forms quoted only to illustrate a sign or a sound change, with no reading
  attached** — e.g. "WA-JA → WA-E" (p. 22), and the fragment `]U-TI-NU·I-NA-I-DA[`
  at p. 14 n. 20, which is shown to prove the prayer could continue rather than to
  be read.
- **Hebrew and Arabic script**, per the brief.

One parsing limit worth recording: where an Appendix B entry cites a second
inscription *after* a line-number dot — as `KU-PA₃-NA-TU: HT 47a.1–2 (…), HT 119`
does — our reference extractor keeps only the first (`HT 47a`). Where the second
reference comes before any dot, as with `A-SA-SA-RA-ME`, both are kept and both are
checked. This affects the reference column only, not the word list.

## 4. Step 3 — checking each row against the corpus

| Group | rows | share |
|---|---|---|
| **exact** — the word is in that inscription as printed | **138** | 82.6% |
| different word breaks | 16 | 9.6% |
| same word, different spelling | 9 | 5.4% |
| not found | 3 | 1.8% |
| no inscription given | 1 | 0.6% |

### 4.1 The allowances we needed

Four, and only four. Both spellings are mapped onto a common alphabet before the
second and third passes, and **every substitution actually used is recorded in the
`allowance` column of the CSV**, so no match is quietly smoothed over.

| Paper writes | Corpus writes | Why |
|---|---|---|
| `*79` | `ZU` | The paper numbers AB79; the corpus uses its Linear B value. Flagged in the brief. |
| `TH` | `ZU` | The same sign, written with the paper's proposed value /ṯ/ (pp. 15, 17). Flagged in the brief. |
| `NA` | `*301` | The paper writes `NA` for `*301` in §7 and §8 prose, having argued `*301` is an allograph of `NA`. Flagged in the brief. |
| `*319` | `*904` | **Not flagged in the brief, and new here.** The paper numbers a sign `*319` in two Appendix B entries; the corpus numbers the sign in that slot `*904`. See 4.4. |

### 4.2 Rows with a different spelling (9)

All nine are the allowances above doing exactly what they were meant to do.

| Word as printed | Where | Inscription | Corpus has | Allowance |
|---|---|---|---|---|
| `A-*79-RA` | Appendix A, p.36 | KN Zc 7 | `A-ZU-RA` | *79 = ZU |
| `A-TH-RA` | §7, p.15 | KN Zc 7 | `A-ZU-RA` | TH = ZU |
| `*79-DU` | Appendix A, p.36 | HT 51b | `ZU-DU` | *79 = ZU |
| `*79-DU` | Appendix A, p.36 | HT 99b | `ZU-DU` | *79 = ZU |
| `MA-*79` | Appendix A, p.36 | HT 102 | `MA-ZU` | *79 = ZU |
| `*79-RI-NI-MA` | Appendix A, p.36 | KN Zb 52 | `ZU-RI-NI-MA` | *79 = ZU |
| `A-TA-I-NA-WA-JA` | §7 table, p.14 | IO Za 2 | `A-TA-I-*301-WA-JA` | NA = *301 |
| `TA-NA-I-NA-U-TI-NU` | §8, p.16 | IO Za 6 | `TA-NA-I-*301-U-TI-NU` | NA = *301 |
| `NA-MA-MA-TI-TI-*319` | Appendix B | HT Zd 155 | `NA-MA-MA-TI-TI-*904` | *319 = *904 |

The paper is consistent about `A-*79-RA` / `A-TH-RA`: it prints `A-*79-RA` in
Appendix A's table and `A-TH-RA` in the §7 prose, and says plainly that `TH` is its
transliteration of AB79 (p. 36). Both reach the corpus's `A-ZU-RA`.

### 4.3 Rows with different word breaks (16)

These are the cases where the signs are in the corpus in the same order, but the
paper and the corpus divide them into words differently. This is the largest
non-exact group, and it clusters in three inscriptions.

**KN Zc 7 — the paper reads 7 words, the corpus 5 (6 rows affected).**
The corpus reads:

> `A-KA-NU-ZA-TI` 𐄁 `DU-RA-RE` 𐄁 `A-ZU-RA` 𐄁 `JA-SA-RA-A-NA-NE` 𐄁 `WI-PI` 𐄁

Appendix A splits two of those into two words each:

| Paper's word | Corpus | Group |
|---|---|---|
| `A-KA-NU` | inside `A-KA-NU-ZA-TI` | different word breaks |
| `ZA-TI` | inside `A-KA-NU-ZA-TI` | different word breaks |
| `JA-SA-RA` | inside `JA-SA-RA-A-NA-NE` | different word breaks (3 rows: Appendix A, §4.3, §7) |
| `A-NA-NE` | inside `JA-SA-RA-A-NA-NE` | different word breaks |
| `DU-RA-RE`, `WI-PI` | as printed | exact |
| `A-*79-RA` | `A-ZU-RA` | same word, different spelling |

This one deserves a flag. KN Zc 7 is the only place in the paper that carries
confidence labels, and the word labelled **CONFIRMED** — `A-KA-NU`, read *ʾagānu*
"bowl" — is one of the four that the corpus does not write as a separate word. The
corpus has no divider inside `A-KA-NU-ZA-TI`. We are not saying the paper is wrong;
word divisions in Linear A are genuinely contested and a corpus is not automatically
right. We are saying the division is the paper's, not the corpus's, and that the
paper's highest-confidence reading rests on it.

**IO Za 6 — 4 rows affected.** The corpus reads:

> `TA-NA-I-*301-U-TI-NU` 𐄁 `I-NA-TA-I-ZU-DI-SI-KA` 𐄁 `JA-SA-SA-RA-ME` 𐄁

The paper's `I-NA-TA` and `I-*79-DI-SI-KA` (also printed `I-TH-DI-SI-KA` on p. 17)
are both inside the corpus's single unbroken `I-NA-TA-I-ZU-DI-SI-KA`. This was
already flagged in cycle 1 as the difference most worth a careful later look, since
the split is what lets the paper read `I-NA-TA` as the goddess Anat.

**Six more, one each.**

| Word | Inscription | What the corpus has |
|---|---|---|
| `JA-DI-KI-TE-TE` | PK Za 15 | inside `JA-DI-KI-TE-TE-DU-PU₂-RE` |
| `DU-PU₂-RE` | PK Za 15 | inside the same word |
| `JA-SA-SA-RA-MA-NA` | KN Za 10 | split as `JA-SA-SA-RA-MA` + `NA`, no divider between |
| `JA-SU-MA-TU` | SY Za 2 | inside `JA-SU-MA-TU-OLIV` — the corpus joins the commodity sign OLIV to the word |
| `KI-TA-NA-SI-JA-SE` | PE Zb 3 | inside `A-KA-RA-KI-TA-NA-SI-JA-SE-VIR+[?]-ZA` |
| `WI-JA-SU-MA-TI-TI-*319` | HT Zd 157+156 | split as `WI-JA-SU-MA-TI-TI` + `*904`, no divider between |

The `JA-SU-MA-TU-OLIV` case is arguably a corpus quirk rather than a real
disagreement: gluing a commodity sign onto the preceding word is a transcription
convention, not a scribal word division.

### 4.4 Rows not found (3)

| Word | Where | Inscription | What the corpus has instead |
|---|---|---|---|
| `DU-PU₂-RE` | §9, p.19 | PK Za 11 | `A-TA-I-*301-WA-E` 𐄁 `A-DI-KI-TE-TE` 𐄁 𐄁 `RE` 𐄁 `PI-TE-RI` 𐄁 `A-KO-A-NE` 𐄁 `A` `SA-SA-RA-ME` 𐄁 `U-NA-RU-KA-NA-TI` 𐄁 `I-PI-NA-MI-NA` `SI-RU` 𐄁 … — no `DU-PU₂-RE` |
| `DU-PU₂-RE` | §9, p.19 | PK Za 12 | `A-TA-I-*301-WA-JA` 𐄁 `A-DI-KI-TE` `SI` 𐄁 𐄁 `RA-ME` `A-NE` `U-NA-RU-KA-JA-SI` `A-PA-DU-PA` `JA` `JA-PA-QA` — no `DU-PU₂-RE` |
| `A-DU-RE-ZA` | Appendix B | KH 11 | `A-DU` 𐄁 `ZA` `CYP` ¹⁄₁₆ `SU` 3 … — see known case 4, where this is the expected result |

On the two `DU-PU₂-RE` rows: the paper writes that Davis "settles on the peak
sanctuary of Petsofas and the sequence `A-DI-KI-TE-TE` `DU-PU₂-RE` (PK Za 11, 12,
15)" (p. 19). In this corpus the sequence is at **PK Za 15 only**, where it is one
unbroken word `JA-DI-KI-TE-TE-DU-PU₂-RE`. PK Za 11 has `A-DI-KI-TE-TE` but no
`DU-PU₂-RE`; PK Za 12 has a damaged `A-DI-KI-TE` and no `DU-PU₂-RE`. PK Za 12 is
visibly broken in this corpus, so damage is a plausible explanation there; PK Za 11
is well preserved and simply does not have the word. Note also that the citation is
a report of *Davis's* claim, not the paper's own reading, so this is a mismatch with
a cited third party rather than with the paper's own decipherment.

We also note a possible slip in the same sentence: the inscriptions cited are PK
(Palaikastro) but the site named is Petsofas. Those are different places, though
Petsofas is the peak sanctuary above Palaikastro, so this may be shorthand rather
than an error. **Unknown**; the paper does not say.

`*319` vs `*904` (4.1) is worth one more line. In `NA-MA-MA-TI-TI-*319` the
allowance resolves it cleanly to the corpus's `NA-MA-MA-TI-TI-*904`. But nothing in
the paper explains the different sign number, and we could not establish from the
files we have whether `*319` and `*904` are two numbering systems for one sign or
two different signs. **Unknown.** GORILA's own sign list, or the paper's sign
table, would settle it. Until then the two rows using `*319` should be read as
provisional.

### 4.5 No inscription given (1)

`JE-DI` (§8 n. 31, p. 17), read *yedī* "the Idaean". The paper says only "four
attestations at Hagia Triada" and names no tablet, so there is nothing to check
against. For what it is worth, `JE-DI` does occur in the corpus — but since the
paper does not say which inscriptions it means, we did not try to guess.

## 5. The four known cases

**All four came out as described. The checker was not adjusted to make them pass;
the one failure during development was a faulty assertion in our own test, noted
below.** Run by `scripts/13_known_cases.py`.

**1. IO Za 2 — PASS.** All seven words of the prayer as printed in §4–§6 come out
**exact**: `A-TA-I-*301-WA-JA`, `JA-DI-KI-TU`, `JA-SA-SA-RA-ME`, `U-NA-KA-NA-SI`,
`I-PI-NA-MA`, `SI-RU-TE`, `TA-NA-RA-TE-U-TI-NU`. The §7 translation table's
`A-TA-I-NA-WA-JA` comes out **same word, different spelling**, on the `NA` = `*301`
allowance.

**2. IO Za 6 — PASS.** `I-NA-TA` and `I-*79-DI-SI-KA` both come out **different word
breaks**; the corpus has the single word `I-NA-TA-I-ZU-DI-SI-KA`.

**3. PK Za 11 — PASS, and the paper does read this spot two different ways.** Said
plainly, as the brief asks:

- §4.3 (p. 8), the §8 table (p. 16) and the §8 discussion (p. 18) all print
  **`SA-SA-RA-ME`**, and p. 18 states the reason: at Palaikastro "the initial JA is
  consistently dropped: SA-SA-RA-ME for JA-SA-SA-RA-ME". All three rows come out
  **exact** — `SA-SA-RA-ME` is a word in the corpus's PK Za 11.
- Appendix B (p. 37) instead lists **`A-SA-SA-RA-ME`** for "IO Zb 10, PK Za 11a–b",
  and explains it the other way round: a "Palaikastro prefix variant of
  JA-SA-SA-RA-ME (ʾa- for ya-)" — an `A-` prefix rather than a dropped `JA-`.
- The corpus supports the *signs* of the Appendix B reading: PK Za 11 has a bare
  `A` immediately before `SA-SA-RA-ME`, with **no word divider between them** (they
  sit on either side of a line break, which is not a divider). Checked against the
  raw token stream: `… 'A-KO-A-NE', '𐄁', 'A', '\n', 'SA-SA-RA-ME', '𐄁' …`.
- So at PK Za 11 the Appendix B row comes out **different word breaks** (corpus
  splits it as `A` + `SA-SA-RA-ME`), while at the other inscription the same entry
  cites, IO Zb 10, `A-SA-SA-RA-ME` is **exact** — it is the whole inscription there.

The two readings are not compatible with each other: one takes the `A` as the start
of the word, the other does not take it at all. Both cannot be right about the same
spot. The paper does not acknowledge the difference, and we are not adjudicating it
here.

**4. KH 11 — PASS: the paper's correction is supported by the corpus.** Appendix B
says of Davis's `A-DU-RE-ZA`: "Mis-transcribed by Davis: the tablet reads A-DU 𐄁 ZA,
with a word divider; RE is absent. A-DU-RE-ZA is not an attested word." The corpus
opens KH 11 with exactly `['A-DU', '𐄁', 'ZA', 'CYP', …]` — `A-DU`, a word divider,
then `ZA`, and no `RE`. The row is recorded as **not found**, which is the correct
and expected outcome, with a note that the paper itself predicted it.

*On the development failure:* our first version of the known-case test asserted
that `A` was the token immediately preceding `SA-SA-RA-ME` in PK Za 11. It is not —
a line-break token sits between them. The brief's claim was about a *word divider*,
and there is none. The test was corrected to check what the brief actually claims.
No change was made to the checker.

## 6. Step 4 — counts

### 6.1 Rows and words

Given in section 3 (167 rows, 114 distinct words, by part of the paper) and section
4 (by group).

### 6.2 How often each word occurs in the whole corpus

Full per-word figures are in the CSV and in `data/derived/word_frequency.json`.
Counted with the sign-spelling allowances applied, over the 114 distinct words:

| Occurrences in the corpus | distinct words |
|---|---|
| 0 | 14 |
| 1 | 66 |
| 2 | 19 |
| 3 | 3 |
| 4 | 3 |
| 6 | 3 |
| 7 | 2 |
| 8 | 1 |
| 11 | 2 |
| 39 | 1 |

**66 of 114 (57.9%) occur exactly once.** The 14 that do not occur at all are not a
separate mystery — every one of them is a row already accounted for in section 4 as
a word-break difference or a not-found. The most frequent are the single sign `I`
(39), `A-TA-I-*301-WA-JA` (11), `KU-PA₃-NU` (8), then `JA-SA-SA-RA-ME` and
`SI-RU-TE` (7 each).

### 6.3 Footnote 36 re-counted

> "In formal response to Davis (2026), I have included a comprehensive appendix of
> 67 Linear A sign-groups matching his own. **Of these, 39 (58.2%) are hapax
> legomena.**" — p. 20, footnote 36

| | Paper | Ours | Match? |
|---|---|---|---|
| Appendix B sign-groups | 67 | **67** | **yes, exact** |
| — of which hapax legomena | 39 (58.2%) | **39 (58.2%)** | **yes, exact** |

Counting the 67 words exactly as the paper prints them, 39 occur exactly once in
this corpus. That is the paper's number to the unit and to the tenth of a percent.

**The caveat, stated plainly, because this match is more fragile than it looks.**
Of the 67 words, 7 do not appear in this corpus at all as printed: `A-DU-RE-ZA`
(which the paper itself says is not a word), `JA-DI-KI-TE-TE`, `JA-SA-SA-RA-MA-NA`,
`JA-SU-MA-TU`, `KI-TA-NA-SI-JA-SE`, `NA-MA-MA-TI-TI-*319` and
`WI-JA-SU-MA-TI-TI-*319`. Six of those seven are the word-break and sign-numbering
cases from section 4 — under the paper's own divisions each would occur once, and
so would count as a hapax. Counting them that way gives **46 of 67 (68.7%)**, not
39. The exact agreement at 39 therefore depends on treating a word-division
mismatch as "not attested" rather than "attested once". We report the match because
it is real on the strictest reading, and the caveat because the number moves nearly
ten points under a defensible alternative. Applying only the sign-spelling
allowances (which rescues `NA-MA-MA-TI-TI-*319`) gives 40 of 67, 59.7%.

## 7. Things worth noting

1. **Four out of five rows check out exactly.** 138 of 167 rows put the word in the
   inscription the paper cites, spelled as the paper prints it. Of the 29 that do
   not, 9 are the sign-spelling conventions the paper itself declares, and 16 are
   word-division differences. Only 3 are genuine absences, and one of those is a
   mismatch the paper predicted. This is a statement about the paper's bookkeeping —
   whether a word is where it is said to be — and nothing else.

2. **Appendix B's count of itself is exact.** 67 entries claimed, 67 parsed, and
   the hapax figure inside it reproduces at 39 (58.2%) — with the caveat in 6.3.

3. **The paper's highest-confidence reading depends on a word division the corpus
   does not share.** `A-KA-NU` is the only word in the paper labelled CONFIRMED, and
   the corpus writes `A-KA-NU-ZA-TI` as one word. Four of Appendix A's seven words
   are affected by the same two joins in KN Zc 7.

4. **PK Za 11 is read two incompatible ways** — `SA-SA-RA-ME` with a dropped `JA-`
   in the main text, `A-SA-SA-RA-ME` with an added `A-` in Appendix B. The paper
   does not note the difference.

5. **A sign-numbering difference nobody flagged.** The paper writes `*319` where
   this corpus writes `*904`, in two Appendix B entries. Whether these are two
   numberings of one sign or two different signs is **unknown** from the files we
   have.

6. **`DU-PU₂-RE` is cited for three inscriptions and found in one.** The citation
   reports Davis's claim rather than the paper's own reading, which softens it, but
   PK Za 11 is well preserved and does not contain the word.

7. **Zenodo has now failed twice.** The DOI is real and verified through DataCite;
   only the attached-file list is missing, and the 508-entry lexicon (section 1) is
   the obvious thing it might contain.

## 8. Open items carried forward

| Question | What would settle it |
|---|---|
| What files are attached to either Zenodo record? | One successful fetch of `https://zenodo.org/api/records/22730321` or `/21903481` |
| Is the 508-entry lexicon published anywhere? | The Zenodo file list, or the author |
| Are `*319` and `*904` the same sign? | GORILA's sign list, or the paper's sign table |
| Which four Hagia Triada inscriptions have `JE-DI`? | The paper's underlying data |
| Which reading of PK Za 11 does the paper intend? | The paper, or the author |
| Is "Petsofas" (p. 19) shorthand for the PK inscriptions, or a slip? | The paper |
| Which 59 entries does the paper's corpus have that this file lacks? | Carried over from cycle 1 |

## 9. How to reproduce

`data/` is not committed. Cycle 1's report records the download URLs with sizes and
SHA-256 hashes. Then:

```
node scripts/01_dump_corpus.js
python3 -m venv venv && ./venv/bin/pip install pdfplumber
bash scripts/run_all.sh
```

| Script | Does |
|---|---|
| `scripts/10_parse_appendix_b.py` | Parses Appendix B into 67 structured entries |
| `scripts/11_build_readings.py` | Builds the 167-row readings table |
| `scripts/12_check_readings.py` | Checks every row against the corpus; writes the CSV |
| `scripts/13_known_cases.py` | Verifies the four known cases; fails loudly if any differs |
| `scripts/14_counts.py` | Step 4 counts and the footnote 36 re-count |

Scripts 01–09 are from cycle 1 and are documented in `reports/cycle-01.md`.
