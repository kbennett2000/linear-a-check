# Cycle 1 — gather the data, re-count the paper's own numbers

**Date run:** 16 September 2026
**Scope:** collect the sources, verify we are reading the same files the project
owner read, and re-count seven numbers the paper states. **No conclusions about
the language are drawn in this cycle**, and none should be read into it.

> **Correction — 17 September 2026 (cycle 2).** Section 1.3 previously said the
> paper "contains a 508-entry lexicon as Appendix B, inside the PDF (pp. 36–40)".
> That was wrong on both counts. The paper mentions a 508-entry lexicon once, at
> the end of §9 (p. 20), and never prints it. Appendix B is a different thing: an
> index of **67 Linear A sign-groups** drawn from Davis 2026 (p. 36 and footnote
> 36 on p. 20). The bullet in 1.3 has been rewritten; nothing else in this report
> has been changed. The error mattered because it wrongly implied the 508-entry
> lexicon was already in hand, when in fact it remains unpublished as far as we
> can see and is a live candidate for whatever the Zenodo record holds.

> **Correction — 16 September 2026 (cycle 4).** Section 1.3 below says the 504
> errors were "our network reaching Zenodo, not something about this particular
> record". **That was a guess, and it was wrong.** The failure is on Zenodo's
> side. Two independent checks show it: the project owner's own web browser, on
> a different network, got the same 504 from Zenodo on 16 September 2026; and
> Plazi's automatic uptime monitor logged `https://zenodo.org/communities/biosyslit/`
> returning HTTP 504 after about 30 seconds on 14 September 2026
> ([plazi/monitoring#4101](https://github.com/plazi/monitoring/issues/4101),
> response time 30,316 ms) and again on 16 September 2026
> ([plazi/monitoring#4114](https://github.com/plazi/monitoring/issues/4114),
> response time 30,303 ms). Both were opened and read before this note was
> written. The practical conclusion is unchanged — the record's file list is
> still **unknown** — but the reason is Zenodo being down, not this machine.
> Nothing else in this report has been changed.

A note on words used below. *Linear A* is the undeciphered writing system of
Bronze Age Crete. A **syllabogram** is a sign standing for a whole syllable (KA,
TI). A **logogram** is a sign standing for a whole word or commodity (VIN "wine",
GRA "grain"). A **transliteration** is the conventional Latin-letter spelling of a
sign sequence — it records *which signs are written*, not what they meant. Signs
with no agreed sound value are written with a star and a number (`*301`). A
**ligature** or **compound** is two signs drawn as one (`OLE+DI`). An **attestation**
is one surviving occurrence of something.

---

## 1. What we downloaded

### 1.1 The corpus

| | |
|---|---|
| URL | `https://raw.githubusercontent.com/mwenge/lineara.xyz/master/LinearAInscriptions.js` |
| Saved as | `data/raw/LinearAInscriptions.js` |
| Size | **1,609,137 bytes** |
| SHA-256 | **`4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c`** |

**Both the size and the hash are identical to the values recorded by the project
owner on 16 Sep 2026.** We are reading exactly the same file. This is the Linear A
Explorer data the paper itself credits as "Hogan 2019–".

The file is JavaScript, not data: it defines `var inscriptions = new Map([...])`
plus four more Maps. As instructed, it was not parsed with regular expressions. It
was executed in Node's `vm` module and the Maps were serialised to JSON
(`scripts/01_dump_corpus.js`). One wrinkle worth recording: objects built inside a
`vm` context belong to that context's realm, so `map instanceof Map` is **false**
when tested from outside. The conversion therefore has to be run *inside* the
context. The five Maps and their sizes:

| Map | entries |
|---|---|
| `inscriptions` | 1,721 |
| `lexicon` | 24 |
| `sequences` | 133 |
| `wordsInCorpus` | 1,427 |
| `ligatures` | 141 |

### 1.2 The paper

| | |
|---|---|
| URL | `https://www.minoanmystery.org/linear-a/ya-diktu-grammar-tom-di-mino.pdf` |
| Saved as | `data/raw/ya-diktu.pdf` |
| Size | **446,199 bytes** |
| SHA-256 | **`2204ea0e6d1a0c09957b962bad8feb058a9e7275cdb1380699ec926beb93dc2b`** |
| Pages | 42 |

Text extracted with `pdfplumber` (`scripts/03_extract_pdf.py`). The PDF's embedded
fonts lose many inter-word spaces on extraction, so quotations below are given with
spacing restored; `scripts/04_find_claims.py` searches both the raw and a
space-stripped form so no claim is missed because of it. All page numbers cited are
PDF page numbers, which match the paper's own printed page numbers.

### 1.3 The DOI record — **file list unknown**

The DOI `10.5281/zenodo.22730321` **does exist and does resolve to this paper.**
Confirmed independently through DataCite, the registry that holds DOI metadata
(saved as `data/raw/datacite_22730321.json`):

- Title: *Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula*
- Creator: di Mino, Tom
- Publisher: Zenodo; type: Preprint; publication year 2026
- Dates: issued 2026-09-12; "Preprint version 1.0 publicly released" 2026-08-12
- Licence: CC BY 4.0
- `IsVersionOf` an earlier DOI: `10.5281/zenodo.21903481`
- `IsSupplementedBy`: `https://www.minoanmystery.org/linear-a`

**We could not list the record's attached files.** `zenodo.org` is unreachable from
this machine: every request — the API, the record page, the OAI-PMH endpoint, over
both IPv4 and IPv6, inside and outside the sandbox, and through a separate
web-fetching tool — returned a 504 Gateway Timeout or timed out. A known-good
unrelated Zenodo record failed the same way, while other hosts responded normally,
so **this is our network reaching Zenodo, not something about this particular
record.** DataCite's copy of the metadata has empty `sizes` and `formats` arrays and
no `contentUrl`, so it cannot substitute for the file list.

Per the project rules, no file URLs were guessed. Two partial signals, neither of
them authoritative:

- The paper's own web page links only the PDF. Asked to list every downloadable
  file on it, a fetch of `https://www.minoanmystery.org/linear-a` returned the PDF
  and the DOI link and nothing else — "no spreadsheets, CSV files, word lists, code
  repositories, or GitHub links".
- The paper mentions a 508-entry lexicon at the end of §9 (p. 20) but **never
  prints it**. What it does print, as **Appendix B inside the PDF** (pp. 36–40), is
  an index of **67 Linear A sign-groups** taken from Davis 2026 — "the 66
  sign-groups in Davis's appendix (2026, 58–60) and one word in his body" (p. 36),
  described in footnote 36 (p. 20) as "a comprehensive appendix of 67 Linear A
  sign-groups matching his own". So the 508-entry lexicon is not in the PDF and
  would be a genuine candidate for a separate data deposit.

**Status: unknown.** What would settle it: one successful fetch of
`https://zenodo.org/api/records/22730321` from any machine that can reach Zenodo.
Its `files[]` array lists every attached file with name, size and checksum. Worth
retrying next cycle.

---

## 2. Known-answer check — **all four reproduced exactly**

Run first, before any other analysis (`scripts/02_known_answer_check.py`).

| Check | Expected | Ours | |
|---|---|---|---|
| Entries in the `inscriptions` Map | 1,721 | **1,721** | match |
| Distinct strings in `transliteratedWords` containing a hyphen | 995 | **995** | match |
| `transliteratedWords` entries exactly `KU-RO` | 37 | **37** | match |
| `transliteratedWords` entries exactly `*301` | 238 | **238** | match |

Nothing differs, so nothing to stop for. For context: there are 8,601
`transliteratedWords` tokens in total, and 9 inscriptions carry none at all.

---

## 3. Re-count of the paper's numbers

Reminder from the brief, and it matters for reading every row: **the paper worked
from 1,780 inscriptions and this file has 1,721**, so small shortfalls are expected
and are not evidence of anything. A mismatch here is not a verdict.

| # | Item | Paper | Ours | Match? | Most likely reason for any gap |
|---|---|---|---|---|---|
| 1 | Corpus size | 1,780 | 1,721 | **No** (−59) | This file predates or omits 59 of the paper's entries. But the GORILA component matches *exactly* — see 3.1 |
| 1a | — of which from GORILA | 1,468 | **1,468** | **Yes, exact** | — |
| 1b | — of which Douros + SigLA | 261 + 51 = 312 | 253 | **No** (−59) | The entire shortfall sits in the post-GORILA additions |
| 2 | `*301` total attestations | 291 | **290** | Near-exact (−1) | One occurrence in the 59 missing inscriptions |
| 2a | `*301` standing alone | 238 | **238** | **Yes, exact** | — |
| 2b | Sites for standalone `*301` | Hagia Triada (predominant), Khania, Knossos, Zakros | Hagia Triada 230, Khania 5, Knossos 2, Zakros 1 | **Yes** | Exactly the four sites named, in the stated proportion |
| 2c | Support type | "roundels" | **Nodule** 231, Tablet 6, Sealing 1 — **Roundel 0** | **No** | Terminology, not arithmetic — see 3.2 |
| 3 | Attestations of the formula's first verb | 15 | 14 strict, **15** including the IO Za 6 form | **Yes** | Reproduces exactly once the paper's own §8 variant is included |
| 3a | The `I` sign invariant across them | invariant | **invariant in all 15** | **Yes** | — |
| 4 | Formula occurrences / sites | "at least 15 times across 7 sites" | 14 across **7 sites** strict; 17 across 8 including related forms | **Yes**, consistent | "At least" is satisfied on the wider reading; site count matches exactly on the strict one |
| 4a | §8 cross-site table inscriptions | 6 named | **all 6 present** | **Yes** | Two have different word divisions — see 3.4 |
| 5 | /a, i, u/ share of syllable signs | 3,823 of 4,733 = 80.8% | **3,867 of 4,769 = 81.1%** | **Yes, close** | +0.3 points; 0.8% difference in the base. Well inside the range our own counting choices move it |
| 6 | AB79 distinct word-forms | 25 | **24** | Near-exact (−1) | One form in the 59 missing inscriptions |
| 7 | `*314` attestations | 6 | **6** | **Yes, exact** | — |
| 7a | `*314` sites | Hagia Triada, Kophinas, Phaistos, Arkhalokhori | **the same four** | **Yes, exact** | — |

### 3.1 Corpus size (item 1)

> "As of September 2026 … the Linear A corpus has grown to 1,780 individual
> inscriptions … I have reconciled and deduplicated all 1,468 documents from the
> five volumes of GORILA (Godart & Olivier 1976–1985), 261 additional entries
> tabulated by George Douros from post-1985 publications (Hallager 1996), as well
> as 51 face-level records from the SigLA database (Salgarella & Castellan 2021)."
> — p. 3

This file has 1,721 entries, 59 fewer. The interesting part is *where* the 59 sit.

The file has no explicit "source" field, but its `imageRightsURL` field points at
the scanned GORILA volumes for entries drawn from GORILA. Counting those
(`scripts/09_corpus_size.py`):

| | entries |
|---|---|
| GORILA vol. 1 | 257 |
| GORILA vol. 2 | 868 |
| GORILA vol. 3 | 244 |
| GORILA vol. 4 | 74 |
| GORILA vol. 5 | 25 |
| **Total citing a GORILA volume** | **1,468** |
| Everything else | 253 |

**1,468 on the nose.** The paper's GORILA figure is reproduced exactly, from an
independent field of the file. The whole 59-entry gap falls in the post-GORILA
additions: 253 here against the paper's 261 + 51 = 312. That is consistent with the
paper having pulled in Douros and SigLA material that this snapshot of the Explorer
data does not carry — which is what the brief anticipated.

One caveat on `imageRightsURL` as a proxy: it records where an image came from, not
where an inscription record came from. That it lands on exactly 1,468 is good
evidence it tracks GORILA membership, but it is a proxy. The paper's own list of
the 312 non-GORILA entries would settle it.

### 3.2 Sign `*301` (item 2)

> "In 238 of its 291 attestations — predominantly on Hagia Triada roundels, with
> additional examples at Khania, Knossos, and Zakros — `*301` stands alone as a
> logographic abbreviation, plausibly for *nawā* 'dwelling, temple' itself."
> — p. 5

`scripts/05_star301.py`. Counting the sign itself (a word can contain it twice):

| | |
|---|---|
| Standing alone (token is exactly `*301`) | **238** |
| Inside a longer word | 52 |
| **Total `*301` sign occurrences** | **290** (paper: 291) |

238 is exact. 290 against 291 is one short, which the missing 59 inscriptions
easily explain.

Standalone `*301` by site, and by the file's own `support` field:

| Site | Nodule | Tablet | Sealing | total |
|---|---|---|---|---|
| Hagia Triada | 226 | 4 | — | **230** |
| Khania | 3 | 2 | — | 5 |
| Knossos | 1 | — | 1 | 2 |
| Zakros | 1 | — | — | 1 |
| **total** | **231** | **6** | **1** | **238** |

The site list is exactly right: predominantly Hagia Triada, plus Khania, Knossos
and Zakros — no fifth site, and no site named that isn't there.

**The support type is where it parts company with the paper.** As the brief notes,
in this file Hagia Triada ids beginning `HTWa` are labelled **Nodule** and those
beginning `HTWc` are labelled **Roundel**. Breaking the Hagia Triada 230 down by id:

| id prefix | label in this file | standalone `*301` |
|---|---|---|
| `HTWa` | Nodule | 225 |
| `HTWd` | Nodule | 1 |
| `HT` (tablets) | Tablet | 4 |
| `HTWc` | **Roundel** | **0** |

Checked across the whole corpus, not just Hagia Triada: there are 151 roundels in
the file (101 Khania, 24 Hagia Triada, 8 Knossos, 8 Phaistos, and a scatter
elsewhere), and **not one of them carries a standalone `*301`.**

This is a difference in what the documents are called, not in the count — the 238
is solid either way. `Wa` and `Wc` are the standard sub-classes for sealed clay
documents, and this file assigns "nodule" to the `Wa` series and "roundel" to the
`Wc` series. Under that labelling the paper's word "roundels" does not describe
these 225 documents. Whether the paper is using "roundel" loosely for sealed clay
documents in general, or is following a different classification, is **unknown**
from the files we have; the paper does not define the term. Worth flagging for a
later cycle because the document type carries an administrative meaning — it
bears on whether a standalone sign is an abbreviation in a sealing system or a word
in a text — but that is a question for a cycle that is allowed to draw conclusions.

For the record, `*301` inside longer words breaks down as: `A-TA-I-*301-WA-JA` ×11,
the ligature `*301+*311` ×10 (one at Armenoi, nine on Khania roundels), and 25
further one- or two-off forms.

### 3.3 The formula's first word (item 3)

> "**I** AB28 B28 /i/ Stem vowel (invariant across 15 attestations)" — p. 4, table

> "…the tG morpheme in this language has been vocalized as *-ta-* rather than bare
> *-t-*, with the **I** sign representing an invariant stem vowel across all 15
> attestations of this verb." — p. 5

Every corpus word containing `TA-I-*301` (`scripts/06_formula.py`):

| Word-form | Inscription | Site |
|---|---|---|
| `A-TA-I-*301-WA-JA` | IOZa2 | Iouktas |
| `A-TA-I-*301-WA-JA` | IOZa3 | Iouktas |
| `A-TA-I-*301-WA-JA` | IOZa7 | Iouktas |
| `A-TA-I-*301-WA-JA` | KOZa1 | Kophinas |
| `A-TA-I-*301-WA-JA` | PKZa12 | Palaikastro |
| `A-TA-I-*301-WA-JA` | SYZa1 | Syme |
| `A-TA-I-*301-WA-JA` | SYZa2 | Syme |
| `A-TA-I-*301-WA-JA` | SYZa3 | Syme |
| `A-TA-I-*301-WA-JA` | SYZa4 | Syme |
| `A-TA-I-*301-WA-JA` | SYZa8 | Syme |
| `A-TA-I-*301-WA-JA` | TLZa1 | Troullos |
| `A-TA-I-*301-WA-E` | PKZa11 | Palaikastro |
| `A-TA-I-*301-DE-KA` | ZAZb3 | Zakros |
| `JA-TA-I-*301-U-JA` | APZa1 | Apodoulou |

**14 tokens, 4 distinct word-forms, 7 sites.**

Now the other forms the paper itself treats as the same verb:

| Word-form | Inscription | Site | How the paper treats it |
|---|---|---|---|
| `TA-NA-I-*301-U-TI-NU` | IOZa6 | Iouktas | §8 table, p. 16: position 1, the invocation verb, "the most pronounced deviation" |
| `TA-NA-I-*301-TI` | PSZa2 | Psykhro | not discussed in the paper |
| `A-NA-TI-*301-WA-JA` | IOZa8 | Iouktas | lexicon p. 37: "fragmentary single-word inscription"; not claimed as this verb |

Adding the one form the paper explicitly puts in position 1 of its own cross-site
table — IO Za 6's `TA-NA-I-*301-U-TI-NU` — gives **exactly 15**. The paper's number
reproduces.

The invariance claim also holds on the corpus data: all 15 have an `I` immediately
before `*301`, in the 14 strict forms as part of `TA-I-*301` and in IO Za 6 as
`TA-NA-I-*301`. Note this is a statement about the *written sign*, which is what we
checked; whether it is a stem vowel of a Semitic verb is a language question and
out of scope this cycle.

(`A-NA-TI-*301-WA-JA` at IO Za 8 has `TI`, not `I`, before `*301`. It is *not*
included in the 15 — and the paper does not claim it as this verb either, so this
does not cut against it. Flagged only so the next cycle knows it exists.)

### 3.4 The formula itself (item 4)

> "The sequence itself occurs at least 15 times across 7 sites, showing minor
> variations which may be explained by dialect, verbal morphology, and the resident
> deity in question." — p. 4

Counting every inscription carrying a position-1 verb form of the formula:

| Site | count | inscriptions |
|---|---|---|
| Iouktas | 5 | IOZa2, IOZa3, IOZa6, IOZa7, IOZa8 |
| Syme | 5 | SYZa1, SYZa2, SYZa3, SYZa4, SYZa8 |
| Palaikastro | 2 | PKZa11, PKZa12 |
| Apodoulou | 1 | APZa1 |
| Kophinas | 1 | KOZa1 |
| Psykhro | 1 | PSZa2 |
| Troullos | 1 | TLZa1 |
| Zakros | 1 | ZAZb3 |
| **total** | **17** | **8 sites** |

On the strict `TA-I-*301` reading it is **14 across 7 sites** (the 7 being Iouktas,
Syme, Palaikastro, Apodoulou, Kophinas, Troullos, Zakros). On the wider reading that
includes IO Za 6 and the two other `*301` verb forms it is 17 across 8.

So "at least 15 across 7 sites" is **consistent with this corpus**: 15 is reached as
soon as IO Za 6 is included, which the paper's own §8 table does, and the site count
lands on 7 exactly on the strict reading and 8 on the wider one. Given the wording
"at least", this is a match. The paper's separate claim on p. 16 — "if we expand to
fragments, the count rises to 28 stone vessels and 11 sites" — was not tested this
cycle; it needs a definition of "fragment" the paper does not give, so it is
**unknown** for now.

**The §8 cross-site table (p. 16).** All six inscriptions it tabulates are present
in the corpus, all six on stone vessels. Checking each cell of the table against the
corpus word divisions:

- **IO Za 2** (Iouktas) — all seven positions present as separate words, exactly as
  printed. The corpus reads:
  `A-TA-I-*301-WA-JA · JA-DI-KI-TU · JA-SA-SA-RA-ME · U-NA-KA-NA-SI · I-PI-NA-MA ·
  SI-RU-TE · TA-NA-RA-TE-U-TI-NU · I ·`
  This is a clean, exact match with the paper's headline example.
- **TL Za 1** (Troullos) — all six cells present as printed.
- **KO Za 1** (Kophinas) — all seven cells present as printed, `DU-*314-RE` and
  `I-DA-A` included.
- **SY Za 3** (Syme) — all three cells present as printed.
- **IO Za 6** (Iouktas) — **word division differs.** The paper prints positions 2
  and 3 as two words, `I-NA-TA ·` and `I-*79-DI-SI-KA`. The corpus has a **single
  unbroken word**, `I-NA-TA-I-ZU-DI-SI-KA`. (`ZU` is this file's spelling of the
  sign the paper writes `*79` — see item 6.) The first and last positions,
  `TA-NA-I-*301-U-TI-NU` and `JA-SA-SA-RA-ME`, match exactly. This one matters more
  than the others, because the split is what lets the paper read `I-NA-TA` as the
  goddess Anat, and that reading is load-bearing for its §8 argument. Recorded here
  as a difference, not forced into a match, and not judged either way this cycle.
- **PK Za 11** (Palaikastro) — **word division differs, mildly.** The paper prints
  `SA-SA-RA-ME`; the corpus has a separate `A` immediately before it, i.e.
  `… A · SA-SA-RA-ME …`. All other cells match. The corpus also carries five words
  the table does not show (`RE`, `PI-TE-RI`, `A-KO-A-NE`, a damaged sign,
  `I-NA-JA-PA-QA`); the table is explicitly a selection by position, so this is not
  a discrepancy, just a note that the inscription is longer than the row.

### 3.5 Vowels (item 5)

> "My calculation is based on a corpus of approximately 1,780 Linear A inscriptions.
> Counting recognized syllabogram tokens, and excluding logograms, quantities,
> dividers, unknown signs, damaged tokens, and compounds, /a, i, u/ account for
> 3,823 of 4,733 tokens (80.8%)." — p. 24, footnote 53

> "Its core vowel set, /a, i, u/, which makes up 80.8% of the Linear A corpus's
> vowel signs…" — p. 24

**Our result: 3,867 of 4,769 = 81.1%.** Against the paper's 3,823 of 4,733 = 80.8%:
+44 on the numerator, +36 on the base, **+0.3 percentage points**.

Every counting choice, because the brief is right that small choices move the
total (`scripts/08_vowels.py`):

- **C1** The unit counted is the **sign**, not the word. Each `transliteratedWords`
  word is split on `-` and the pieces counted. This is what makes the base ~4,700
  rather than ~8,600.
- **C2** Only signs on an explicit whitelist of recognised syllabograms are counted.
  Everything else is excluded. One whitelist implements all six of the paper's
  exclusions at once, and makes the rule auditable rather than a chain of filters.
- **C3** Excluded as **quantities**: digits, fractions (`¹⁄₂`, `≈ ¹⁄₆`), weight
  marks such as "double mina" — 1,301 tokens.
- **C4** Excluded as **dividers**: the Aegean word separator and line breaks.
- **C5** Excluded as **logograms**: VIN GRA CYP OLE OLIV AROM CAP VIR HIDE VS GAL
  VAS L — 293 tokens.
- **C6** Excluded as **unknown signs**: anything written `*NNN` (`*301`, `*118`, …)
  — 822 tokens.
- **C7** Excluded as **compounds**: any sign containing `+` (`OLE+DI`, `*301+*311`)
  — 371 tokens. "Compounds" is the paper's own word for these.
- **C8** Excluded as **damaged**: anything containing `[`, `]` or `?` — 4 tokens.
  (Low, because this file mostly folds damage into `[?]` inside compounds, already
  removed by C7.)
- **C9** A sign's vowel is the vowel of its transliterated value. The Linear A
  complex signs keep their base vowel: `RA₂`→a, `PA₃`→a, `TA₂`→a, `PU₂`→u,
  `NWA`→a, `TWE`→e.
- **C10** `AU` (AB85) is excluded from the main count. The paper itself calls it a
  VV diphthong rather than a plain consonant-vowel syllabogram (p. 17 n. 29). Only
  8 tokens; including it changes nothing to one decimal place.
- **C11** The pure-vowel signs A, E, I, O, U **are counted**. They are syllables, so
  they are syllabograms. This is the single most consequential choice — see below.

Full distribution on the main count: **a 1,840 · e 644 · i 1,172 · o 258 · u 855**.
The paper's separate observation that *o* is rare holds emphatically here: 258 of
4,769, or 5.4%.

Sensitivity, so the number can be judged rather than taken on trust:

| Variant | /a,i,u/ | base | % | vs paper |
|---|---|---|---|---|
| **Main** (AU out, pure vowels in) | 3,867 | 4,769 | **81.1%** | +0.3 pts |
| AU counted as /u/ | 3,875 | 4,777 | 81.1% | +0.3 pts |
| Pure-vowel signs excluded | 3,405 | 4,246 | 80.2% | −0.6 pts |
| AU in, pure vowels out | 3,413 | 4,254 | 80.2% | −0.6 pts |

Every variant lands between 80.2% and 81.1%, bracketing the paper's 80.8%. **We
count this as a reproduction.** Note the honest limitation: the choice at C11 alone
swings the base by 487 tokens — more than the 36-token gap with the paper — so this
agreement establishes that the paper's figure is in the right region, not that its
method was identical to ours. The paper does not state its treatment of pure-vowel
signs, so the exact route to 4,733 is **unknown**. Its own workings, or a sign-level
table, would settle it.

One oddity worth recording: our base is *larger* than the paper's (4,769 vs 4,733)
even though our corpus is *smaller* (1,721 vs 1,780). So the difference cannot be a
simple corpus-size effect — it must come from differing exclusion or word-division
choices, in a direction that removed more tokens from the paper's count than from
ours. Not a problem; just not explained by corpus size, and worth saying so.

### 3.6 Sign AB79 (item 6)

> "AB79 (𐙀) attestations. The sign appears in 25 distinct Linear A word-forms, but
> only seven Linear B attestations distributed across four forms. I propose that its
> Linear A value was /ṯ/, here transliterated TH…" — p. 36

As the brief notes, this file writes AB79 as **ZU** (its Linear B value); the paper
writes it `*79` and reads it `TH`. Confirmed: the string `*79` never appears as a
sign in this file.

Counting `ZU` as a whole sign, not as a substring (`scripts/07_ab79_and_314.py`):
**32 tokens in 24 distinct word-forms across 9 sites.** Against the paper's 25
distinct word-forms, **one short.** Both a strict whole-sign match and a looser
substring match give the same 24, so the result is not an artefact of how we split.

The 24 forms: `A-RA-KO-KU-ZU-WA-SA-TO-MA-RO-AU-TA-DE-PO-NI-ZA`, `A-ZU-RA`,
`DU-ZU-WA`, `I-NA-TA-I-ZU-DI-SI-KA`, `I-ZU-RI-NI-TA`, `JU-KU-NA-PA-KU-NU-U-I-ZU`,
`KA-U-ZU-NI`, `KU-PA-ZU`, `KU-ZU-NA`, `KU-ZU-NI`, `MA-ZU`, `PI-KU-ZU`, `QE-SI-ZU-E`,
`RU-ZU-NA`, `TE-ZU`, `ZA-SI-ZU`, `ZU` (alone, ×5), `ZU-*22F-DI`,
`ZU-*301-SE-DE-*21F-*118`, `ZU-DI-RA`, `ZU-DU`, `ZU-JU-PU₂`, `ZU-RI-NI-MA`,
`ZU-SU`.

A −1 gap is exactly what 59 missing inscriptions predict. Two cross-checks that the
paper's own examples are here: it cites `*79-DU` ("*ṯudu* 'breast'") at HT 51b and
HT 99b — the corpus has `ZU-DU` at precisely HT51b and HT99b. And `I-*79-DI-SI-KA`
from the §8 table is present, though inside the longer `I-NA-TA-I-ZU-DI-SI-KA` per
3.4. Both confirm that `ZU` here and `*79` there are the same sign.

One caution on this row: "distinct word-forms" depends on word division, and we have
already found two places where the paper divides differently from the corpus. A
different division could change 24 in either direction without either side being
wrong about the sign.

### 3.7 Sign `*314` (item 7)

> "`*314` 𐙦, here read as the pharyngeal ḥ absent from Linear B, is attested six
> times in the Linear A corpus (Hagia Triada, Kophinas, Phaistos, Arkhalokhori)."
> — p. 17, footnote 30

**Exact match, on both the count and the sites.**

| Word-form | Inscription | Site |
|---|---|---|
| `*314` | PH26 | Phaistos |
| `*314-TA-MA` | PHWc38 | Phaistos |
| `KA-*314-SI` | PHWc37 | Phaistos |
| `DU-*314-RE` | KOZa1 | Kophinas |
| `PI-*314` | ARKH3b | Arkhalkhori |
| `RA-*314-RA` | HTWc3006 | Hagia Triada |

Six attestations, six distinct forms, four sites — Hagia Triada, Kophinas, Phaistos
and Arkhalokhori, exactly the four named and no others. This is the cleanest match
of the seven items, and notable because it is a *falsifiable* claim: a sign this
rare could easily have come out at four or nine.

---

## 4. Things that surprised us

1. **The GORILA sub-count reproduces exactly, at 1,468.** The headline corpus size
   does not match (1,721 vs 1,780) and was never going to. But recovering the
   paper's GORILA figure to the unit, from a field of the file that exists for an
   unrelated reason (image credits), is a stronger check than the headline number
   would have been. The paper's account of where its corpus came from survives
   contact with the data.

2. **`*301` stands alone on nodules, not roundels.** The 238 is exact and the four
   sites are exact, but in this file's own labelling not a single one of the 151
   roundels in the entire corpus carries a standalone `*301`. The 225 Hagia Triada
   documents concerned are `HTWa`, labelled "Nodule". A terminology difference
   rather than a counting error, but a specific one, and it touches what kind of
   document the sign is claimed to abbreviate on.

3. **IO Za 6 is one word in the corpus and two in the paper.** The corpus has
   `I-NA-TA-I-ZU-DI-SI-KA` unbroken; the paper reads `I-NA-TA · I-*79-DI-SI-KA` and
   identifies `I-NA-TA` as the goddess Anat. Word divisions in Linear A are genuinely
   contested and the corpus is not automatically right — but this particular split is
   doing real work in the paper's cross-site argument, so it is the one difference
   from this cycle most worth a careful look later.

4. **Five of the seven items land on or within one of the paper's figure.** `*314`
   6/6 with the right four sites; standalone `*301` 238/238; the verb 15/15; AB79
   24 against 25; total `*301` 290 against 291. Whatever one eventually concludes
   about the *language*, the paper's **counts** are, so far, careful and checkable.
   That is a finding about the paper's arithmetic and bookkeeping only. It says
   nothing about whether Linear A is Semitic, and nothing in this cycle should be
   read as bearing on that question.

5. **Our vowel base is bigger than the paper's from a smaller corpus** (4,769 from
   1,721 inscriptions vs 4,733 from 1,780). The percentages agree closely, but the
   direction of the token-count difference rules out corpus size as the explanation.

6. **Zenodo was unreachable for the entire session**, from every route tried. The
   DOI is real and verified through DataCite; only the attached-file list is
   missing.

---

## 5. Open items for a later cycle

| Question | What would settle it |
|---|---|
| What files are attached to the Zenodo record? | One successful fetch of `https://zenodo.org/api/records/22730321` |
| Which 59 entries does the paper have that this file lacks? | The paper's list of its 312 non-GORILA entries |
| Does the paper use "roundel" loosely, or follow a different classification? | A definition in the paper, or its per-inscription support labels |
| How exactly does the paper reach a base of 4,733 vowel tokens? | Its sign-level workings, or its treatment of pure-vowel signs |
| Is the p. 16 claim of "28 stone vessels and 11 sites" reproducible? | The paper's definition of "fragment" |

---

## 6. How to reproduce

`data/` is not committed, by design — no corpus file, no PDF, no derived tables. The
hashes above identify exactly which files to fetch. Then:

```
node scripts/01_dump_corpus.js
python3 -m venv venv && ./venv/bin/pip install pdfplumber
bash scripts/run_all.sh
```

| Script | Does |
|---|---|
| `scripts/01_dump_corpus.js` | Runs the corpus JS in Node's `vm`, dumps the five Maps to JSON |
| `scripts/02_known_answer_check.py` | The four known-answer numbers |
| `scripts/03_extract_pdf.py` | Extracts the paper's text, one record per page |
| `scripts/04_find_claims.py` | Page-aware search helper for locating quotations |
| `scripts/05_star301.py` | Item 2 — `*301` by site and support |
| `scripts/06_formula.py` | Items 3 and 4 — the verb and the §8 table |
| `scripts/07_ab79_and_314.py` | Items 6 and 7 — AB79/`ZU` and `*314` |
| `scripts/08_vowels.py` | Item 5 — vowel share with all four variants |
| `scripts/09_corpus_size.py` | Item 1 — corpus size and the GORILA share |
