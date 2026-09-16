# Cycle 3 — the paper's spelling rules, and a Hebrew word list

This cycle prepares inputs for a later cycle. It does no matching between
Linear A and Semitic words, and it draws no conclusions about the language.

Three things were built:

| file | what it is |
|---|---|
| `reports/cycle-03-readings.csv` | cycle 2's readings table with three new columns: `root`, `root_kind`, `languages` |
| `reports/cycle-03-rules.csv` | 66 rules the paper states or relies on for turning Linear A signs into Semitic sounds and words |
| `data/derived/hebrew_list.json` | 8,674 Strong's Hebrew entries reduced to consonant skeletons (not committed — share-alike licence) |

`reports/cycle-02-readings.csv` is unchanged.

**Terms used below.** A *root* is the set of consonants a family of Semitic
words is built on; the paper writes roots after a √ sign, for example √k-n-s
"to gather". A *skeleton* here means the same idea applied mechanically to a
Hebrew dictionary word: its consonant letters with the vowel marks stripped
out. A *lemma* is the headword form a dictionary prints. A *primitive root* is
Strong's own label for an entry that is a bare verb root rather than a word
built from one. A *syllabogram* is a sign standing for one syllable; a
*logogram* is a sign standing for a whole word. A *prosthetic* vowel is an
extra vowel added at the front of a word without changing its meaning. A
*mater lectionis* is a consonant letter (in Hebrew ו or י) used to write a
vowel.

---

## Part A — the paper's roots, added to the readings table

`reports/cycle-03-readings.csv` is `reports/cycle-02-readings.csv` with three
columns added at the end. 167 rows, 114 distinct words, unchanged from cycle 2.

| column | what goes in it |
|---|---|
| `root` | the root the paper gives for that word, letters exactly as printed. Several roots joined with ` \| ` |
| `root_kind` | `stated` (printed with √), `from comparison word` (only a word in another language is given, so its consonants are copied), or `none` |
| `languages` | the language or languages the paper compares the word to, using the paper's own labels |

### The seven known answers

All seven came out as the brief describes.

| word | expected | found | |
|---|---|---|---|
| A-TA-I-*301-WA-JA | n-w-y | n-w-y (§4.1, pp.4-6) | PASS |
| JA-DI-KI-TU | d-q-q | d-q-q (§4.2, pp.6-7) | PASS |
| JA-SA-SA-RA-ME | y-š-r | y-š-r (§4.3, pp.7-8) | PASS |
| U-NA-KA-NA-SI | k-n-s | k-n-s (§5.1, p.9) | PASS |
| I-PI-NA-MA | p-n-y | p-n-y (§5.2, p.10) | PASS |
| SI-RU-TE | š-r-t | š-r-t (§5.3, pp.10-11) | PASS |
| TA-NA-RA-TE-U-TI-NU | r-ṣ-y | r-ṣ-y (§6.1, pp.12-13) | PASS |

Run `scripts/15_add_roots.py` to reproduce the check.

### Where the three columns came from

The 67 Appendix B rows are machine-read. `scripts/15_add_roots.py` pulls the
roots and the language labels straight out of the stored entry bodies in
`data/derived/appendix_b.json` (built in cycle 2), so nothing was retyped for
them. The other 100 rows were hand-transcribed from the paper and are listed
in the script with the page each was read from.

### Counts

**`root_kind`**

| value | rows |
|---|---|
| stated | 117 |
| from comparison word | 21 |
| none | 29 |

138 of the 167 rows carry a root; 89 of the 114 distinct words do. 59 distinct
roots appear in the column.

**Rows per comparison language.** A row can name several, so these add to more
than 167. 53 rows name none.

| language | rows | | language | rows |
|---|---|---|---|---|
| Hebrew | 82 | | Egyptian | 8 |
| Ugaritic | 43 | | Aramaic | 6 |
| Akkadian | 38 | | Punic | 6 |
| Arabic | 25 | | Hurrian | 4 |
| Mycenaean Greek | 19 | | Amarna Canaanite | 3 |
| Phoenician | 19 | | Berber | 3 |
| Greek | 15 | | Anatolian | 3 |
| Proto-Semitic | 10 | | Lydian | 1 |
| Geʿez | 10 | | | |
| Amorite | 9 | | | |

Hebrew is named on just under half the rows. The next four — Ugaritic,
Akkadian, Arabic and Phoenician — are the languages the paper leans on after
that. Berber, Lydian and Amarna Canaanite each appear in a single passage.

### Choices made, so the next cycle knows what it is reading

1. **Roots are recorded per row, not per word.** A word discussed in §4 and
   then repeated in a table gets the root at the §4 row. That is why the known
   answers check against specific pages.

2. **Table cells carry the root across.** The §7 translation table (p.14) and
   the §8 cross-site table (p.16) print no roots and no comparison languages.
   For 31 of those rows the root and languages of the same word's own
   discussion were carried across, and the `note` column on each such row says
   which section it came from. Four forms that appear only in the §8 table and
   are never given a reading anywhere — SE-KA-NA-SI, U-NA-KA-NA, SI-RU and the
   final I — were left at `none`.

3. **Root hyphenation was normalised.** The paper prints roots hyphenated
   almost everywhere (√n-w-y). Twice it prints one without hyphens (√ntk,
   p.39). Those are written n-t-k. Only the separator changed; no letter was
   touched.

4. **Language abbreviations were expanded.** Appendix B abbreviates: Heb., Ug.,
   Akk., Ar., Aram., Hurr., Anat., Eg., LB, PS. These became Hebrew, Ugaritic,
   Akkadian, Arabic, Aramaic, Hurrian, Anatolian, Egyptian, Mycenaean Greek,
   Proto-Semitic — the names the paper itself uses in its main text. No label
   was invented. Two traps were guarded against: "PS Za 2" is the site code for
   Praisos, not the abbreviation for Proto-Semitic, and "pre-Greek" is a
   statement about substrate rather than a comparison.

5. **Five consonant strings in the `root` column are not Semitic roots.** They
   were copied from non-Semitic comparison words, as the brief asks: d-k-š-n-n
   (Hurrian Daku-šenni), k-b-b (Hurrian/Anatolian Kubaba), m-k-t (Egyptian
   mk.t), p-ꜣ-y-r-ʿ (Egyptian pꜣ-y-Rʿ), r-r-j (Egyptian rrj). The `languages`
   column says which language each came from, and the `note` column says
   plainly that they are not Semitic roots.

6. **English was not counted as a comparison language.** On p.8 the paper
   compares SA-SA to English "ss" in *mission* and *tissue*. That is an
   analogy about spelling, not a word being compared, so it is not in the
   `languages` column. It is in the rules table instead (R18).

7. **Two rows record a root the paper attaches to a comparison word, not to the
   Linear A word.** The Appendix B entry for A-TA-I-*301-WA-JA prints both
   √n-w-y and √n-b-ʾ, the second being the root of the Hebrew comparandum
   *hitnabbēʾ*. Both are in the column and the `note` says which is which.
   The Appendix B entry for KU-PA₃-NU prints √g-p-n against the *rival*
   Ugaritic reading Gupanu, not against the entry's own preferred Hurrian
   reading; that row is set to `none` with a note.

8. **Three rows record a root the paper states a sentence away rather than
   against the word itself.** I-MI-SA-RA (√e-š-r, stated in the preceding
   sentence for Akkadian Išartu and Mīšaru), SI-KI-NE (√š-k-n, stated in n.22
   for Hebrew *šĕkīnā*), and *307 (√d-b-r, stated in the same sentence that
   reads *307 as *dubur*). Each `note` says so.

---

## Part B — the spelling rules table

`reports/cycle-03-rules.csv` holds 66 rules, read out of the whole paper: main
text, footnotes, the §7 and §8 tables, and Appendices A, B and C.

| kind | rules | | stated or used | rules |
|---|---|---|---|---|
| prefix or suffix | 25 | | stated | 47 |
| sound | 12 | | used | 19 |
| sign value | 12 | | | |
| spelling habit | 9 | | | |
| other | 6 | | | |
| word breaks | 2 | | | |

"Stated" means the paper puts it forward as a general rule. "Used" means it
only shows up inside particular readings. Just over two thirds are stated.

### Every quote was checked against the paper

`scripts/17_check_quotes.py` compares each of the 66 quotes against the
extracted text of the PDF. All 66 match. 57 matched with spaces removed; the
other 9 matched once the typesetter's line-break hyphens were also removed
("repre-sented", "syl-labary", "adjec-tive"). The space removal is needed
because the PDF's text layer drops most spaces between words — this was
recorded in cycle 1. Quotes in the CSV have the spaces restored and nothing
else changed.

### What the rules cover

**The four sound rules the paper states in one sentence on p.19** are R05 to
R08: stops are not told apart as voiced, voiceless or emphatic; all s-type
sounds share one series; throat sounds are often unwritten or written with a
plain vowel sign; and length is never written.

**The l/r merger.** The brief asked whether the paper itself states one, since
the author's web page lists it. It does. Appendix C, p.40, describing what
Egyptian group-writing preserves: "the liquid merger of /l/ and /r/—which the
Linear A syllabary collapses". That is R09.

**Per-series values.** R11 to R16 record which sounds each series of signs
actually writes in the paper's own readings: T-series t, ṭ, ṣ, ṯ; D-series d;
K-series k, g, q, ḫ; Q-series q and k; P-series p and b; Z-series ḏ and ṯ. The
`allows` column keeps these separate from what the general stop rule R05 would
additionally permit.

**Sign values** (R25 to R36) cover *301 = na and *301 alone = *nawā*; AB79 =
ṯ with no fixed vowel, plus the paper's own observation that scribes usually
wrote that sound with the T-series instead; *314 = ḥ; AB85 as a two-vowel
sign; *307 = *dubur*; *319 = hū (put conditionally); *312 = KITNU; RU = lū;
DU = dū; and the final I of IO Za 2 left untranslated.

**Spelling habits** (R02, and R17 to R24) cover doubled signs for doubled consonants,
SA-SA for š, TE-TE and TI-TI for ṯ, dead final vowels, ḥ dropping, coda /s/
unwritten before a stop, U-NA for *hunna* because /hu/ cannot be written, and
pre-consonantal /r/ dropped.

**Prefixes and suffixes** (R37 to R61) list each piece once with every meaning
the paper gives it: A-, JA-, TA-, TA-NA-, I-, U-NA-, WI-, RA-, O-, DU-,
-ME/-MA, -JA, -TI, -NU, -NI, -TE, -NA, -KA, -DE-KA, -SE, -A, -I, -NI-TA,
-TE-I-JA, and the indicative U inside a verb. Several carry more than one
meaning: A- is at once the 1cs verb prefix "I", a prosthetic vowel, and the
Palaikastro replacement for *ya-*; I- is a stem vowel, the preposition "in", a
prothetic vowel and a locative.

**Word breaks** (R65, R66) record as a "used" rule that the paper sometimes
divides a run of signs into words differently from the corpus. Cycle 2 counted
16 of 167 rows where this happens. R66 records separately that the paper twice
rejects a published transcription and substitutes its own division.

### Two places where the paper's rules pull against each other

Flagging these because the next cycle turns this table into code and will have
to choose.

1. **Length versus doubling.** R08, from p.19, says length is *never* written.
   R17, from n.13 on p.8, says doubled signs *may* represent doubled
   consonants, with QA-QA-RU = *qaqqaru*. Both are the paper's. A program that
   applies both will let a doubled sign mean either one consonant or two, which
   is weaker than either rule alone.

2. **Two ways to write ṯ.** R27 makes AB79 the only dedicated sign for ṯ; R28,
   from the same footnote, says scribes usually used the T-series instead; R19
   says a doubled TE or TI writes ṯ. So a ṯ may be written with AB79, with a
   single T-series sign, or with a doubled one. Nothing in the paper says when
   each applies.

---

## Part C — the Hebrew word list

### The download

| | |
|---|---|
| URL | `https://raw.githubusercontent.com/openscriptures/strongs/master/hebrew/strongs-hebrew-dictionary.js` |
| downloaded | 16 September 2026 |
| bytes | 2,003,130 — **matches** the brief |
| SHA-256 | `5ce6aeed551c709f49bcfa341cadf2f34bc7599b85d9de9e6ac2ecbf60fc3739` — **matches** the brief |
| saved as | `data/raw/strongs-hebrew-dictionary.js` (not committed) |

Strong's Hebrew dictionary (James Strong, 1894, public domain) as prepared by
Open Scriptures under CC BY-SA. The file ends in `module.exports`, so
`scripts/18_dump_hebrew.js` loads it with Node's `require`. No regular
expression was used to read it. `data/derived/hebrew_list.json` is not
committed, because of the share-alike licence.

### How the skeletons were built

From the `lemma` field of each entry: keep only the 22 Hebrew consonant
letters, fold the five final forms (ך ם ן ף ץ) into the ordinary letters, drop
every vowel point and accent, and write the letters in Latin joined with
hyphens — א ʾ, ב b, ג g, ד d, ה h, ו w, ז z, ח ḥ, ט ṭ, י y, כ k, ל l, מ m,
נ n, ס s, ע ʿ, פ p, צ ṣ, ק q, ר r, ש š or ś, ת t. ש takes š when it carries
the shin dot and ś when it carries the sin dot.

Two flags: `aramaic` when the `derivation` field contains "(Aramaic)", and
`primitive_root` when it contains "primitive root". For a primitive root whose
skeleton ends in h, a second skeleton is recorded with y in place of that final
h. 188 entries got one.

### The known answers

All came out as the brief describes.

| check | expected | got | |
|---|---|---|---|
| entries in total | 8,674 | 8,674 | PASS |
| flagged Aramaic | 675 | 675 | PASS |
| not flagged Aramaic | 7,999 | 7,999 | PASS |
| primitive roots among those 7,999 | 1,390 | 1,390 | PASS |
| H3664 | k-n-s | k-n-s | PASS |
| H3474 | y-š-r | y-š-r | PASS |
| H8334 | š-r-t | š-r-t | PASS |
| H1854 | d-q-q | d-q-q | PASS |
| H7521 | r-ṣ-h | r-ṣ-h | PASS |
| H6437 | p-n-h | p-n-h | PASS |
| H5115 | n-w-h | n-w-h | PASS |
| H6030 | ʿ-n-h | ʿ-n-h | PASS |

One thing worth recording: exactly one lemma in the whole dictionary contains a
ש with neither dot — H3485, Issachar. It was written š, and that is the only
place the shin/sin choice had to be guessed.

### Coverage: the paper's roots against the list

**The seven Part A known-answer roots: all seven found**, as expected, counting
the final-h-as-y skeletons.

| root | Strong's | skeleton |
|---|---|---|
| n-w-y | H5115 | n-w-h (matched on the final-h-as-y form) |
| d-q-q | H1854 | d-q-q |
| y-š-r | H3474 | y-š-r |
| k-n-s | H3664 | k-n-s |
| p-n-y | H6437 | p-n-h (matched on the final-h-as-y form) |
| š-r-t | H8334 | š-r-t |
| r-ṣ-y | H7521 | r-ṣ-h (matched on the final-h-as-y form) |

**Every other root in the Part A column: 26 of 52 found, 26 not found.**
Over all 59 distinct roots, 33 found and 26 not.

The 26 not found, with the languages the paper compared them to:

| root | compared to |
|---|---|
| d-k-š-n-n | Hurrian |
| d-m-t | Akkadian, Ugaritic |
| d-r-r | (none given) |
| e-š-r | Akkadian |
| g-p-n | Anatolian, Hurrian |
| k-b-b | Anatolian, Hurrian |
| k-m-n | Akkadian, Hebrew, Mycenaean Greek |
| k-t-n | Akkadian, Aramaic, Hebrew, Mycenaean Greek, Ugaritic |
| m-k-s | Akkadian, Hebrew, Proto-Semitic |
| m-k-t | Egyptian |
| p-ꜣ-y-r-ʿ | Egyptian |
| q-q-r | (none given) |
| r-r-j | Egyptian |
| t-m | Hebrew |
| t-n-t | Phoenician |
| t-r-s | Egyptian |
| t-ʾ-n | (none given) |
| w-t-ʾ | (none given) |
| y-d | Akkadian, Greek, Hebrew |
| y-t-n | Greek, Mycenaean Greek, Phoenician |
| ʾ-g-n | Aramaic, Hebrew |
| ʾ-r-ṣ | Akkadian, Hebrew, Ugaritic |
| ṯ-d | Ugaritic |
| ṯ-k-m-n | Ugaritic |
| ṯ-n-n | (none given) |
| ṯ-w-r | Hebrew, Proto-Semitic, Ugaritic |

**That number needs reading carefully, and it is not a mark against the paper.**
The check only looks at entries Strong's labels "primitive root", which means
verb roots. Many of the paper's roots are noun roots, which Strong's lists as
nouns instead. Looking the same 26 up among *all* 8,674 entries, 8 of them turn
up straight away: g-p-n (H1612 *gephen* "vine"), k-m-n (H3646 *kammôn*
"cummin"), m-k-s (H4371 *mekes* "assessment"), t-m (H8535 *tām* "complete"),
t-ʾ-n (H8383), y-d (H3027 *yād* "hand"), ʾ-g-n (H101 *ʾaggān* "bowl"), and
ʾ-r-ṣ (H776 *ʾereṣ* "earth"). Those eight are exactly the words the paper
names. 18 are absent from the dictionary altogether, and most of those are
Egyptian, Hurrian, Ugaritic or Phoenician forms that there is no reason to
expect in a Hebrew dictionary.

One case is worth a sentence on its own. **y-t-n is absent from Hebrew but
n-t-n is present** (H5414, "to give"). The paper says exactly this: it reads
A-TA-NA as the feminine of √y-t-n and points to Phoenician Baʿal-Yaton, noting
that Hebrew has the *n*-initial form. So the miss here reproduces something the
paper itself says, rather than contradicting it.

### Sound matches between older Semitic spelling and Hebrew spelling

**This list is not from the paper.** It is the standard set of correspondences,
recorded here because the paper writes its roots in the older style and the
next cycle will need them to compare those roots with Hebrew words.

| older Semitic | Hebrew |
|---|---|
| ṯ | š |
| ḏ | z |
| ḫ | ḥ |
| ġ | ʿ |

Applied as a clearly separate second pass, these rescue 2 of the 26: ṯ-n-n
matches š-n-n (H8150) and ṯ-w-r matches š-w-r (H7788). 24 remain unmatched.
That pass is in `scripts/20_root_coverage.py`, kept apart from the main count
so the two are never confused.

### Vowel letters, not handled this cycle

Hebrew sometimes writes a vowel with ו or י rather than a consonant (a *mater
lectionis*). As the brief directs, this cycle does not handle that. To say
roughly how many entries could be affected: of the 7,279 entries not flagged as
primitive roots, **3,641 have a w or a y somewhere in the skeleton**, and 3,440
have one in a position other than the first letter. So the upper bound is a
little under half the non-root entries. The true number is far smaller, since
in most of those the letter really is a consonant — but 3,440 is the set a
later cycle would have to look at.

---

## Things worth noting

1. **The paper's rule set is loose in two specific places**, set out under Part
   B above: length versus doubling, and the three different ways of writing ṯ.
   Both make the rules easier to satisfy, and the next cycle should count how
   much freedom each one adds rather than just applying it.

2. **A quarter of the readings name no comparison language at all.** 53 of 167
   rows. Most are §8 table cells and short Appendix A entries. 29 rows carry no
   root either. These are the readings that a Hebrew-word check cannot reach.

3. **Hebrew carries most of the weight.** 82 of 167 rows name Hebrew, against
   43 for Ugaritic and 38 for Akkadian. Building the Hebrew list first is
   therefore the right order of work, but a Hebrew-only check will not reach
   the roughly one row in five whose only comparison is Ugaritic, Akkadian,
   Egyptian, Hurrian or Anatolian.

4. **The seven formula roots are all ordinary, well-attested Hebrew verb
   roots.** Every one is a Strong's primitive root with a plain gloss:
   k-n-s "to collect", y-š-r "to be straight", š-r-t "to attend as a menial or
   worshipper", d-q-q "to crush", r-ṣ-h "to be pleased with", p-n-h "to turn,
   to face", n-w-h "to rest as at home". That is a fact about the roots, not
   about whether the Linear A words carry them.

## Open items

Carried forward, not acted on this cycle:

- Whether √*319 and the corpus's *904 are the same sign (cycle 2 open item).
- Which of the two Palaikastro readings of PK Za 11 the paper intends (cycle 2
  open item).
- Zenodo has not answered on any attempt across three cycles, so the record's
  file list is still unknown.
- Whether the four sound matches in the list above should be applied
  automatically in the next cycle, or only offered as an alternative. Applying
  them changes 2 of 59 roots here, so the decision is small in effect but
  should be made deliberately.
- ו and י as vowel letters: up to 3,440 non-root entries could be affected.

## Reproducing this cycle

```
python3 -m venv venv && ./venv/bin/pip install pdfplumber
# downloads into data/raw/ (see cycle 1 and the Part C table above for URLs)
bash scripts/run_all.sh
```

Cycle 3 is scripts 15 to 20:

| script | what it does |
|---|---|
| `scripts/15_add_roots.py` | Part A — builds `reports/cycle-03-readings.csv`, runs the seven known answers |
| `scripts/16_build_rules.py` | Part B — builds `reports/cycle-03-rules.csv` |
| `scripts/17_check_quotes.py` | checks all 66 quotes against the extracted paper text |
| `scripts/18_dump_hebrew.js` | Part C — loads Strong's with Node's `require`, records size and hash |
| `scripts/19_build_hebrew_list.py` | Part C — builds `data/derived/hebrew_list.json`, runs the known answers |
| `scripts/20_root_coverage.py` | Part C — coverage of the paper's roots against the list |

## Credit

Tom di Mino, *Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula*
(September 2026), DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321),
CC BY 4.0. Quotations and the readings table are used under that licence.

Linear A corpus: [lineara.xyz](https://lineara.xyz) (Hogan 2019–).

Strong's Hebrew dictionary: James Strong, *A Concise Dictionary of the Words in
the Hebrew Bible* (1894), public domain; JSON edition by
[Open Scriptures](https://github.com/openscriptures/strongs), CC BY-SA. The
derived word list is not committed.
