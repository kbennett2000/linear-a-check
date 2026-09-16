# A fair test of "Ya Diktu": what we checked, and what we found

**Written 16 September 2026; revised after cycle 9, same day. This is the
place to start.**

---

## 1. What we tested, why, and who did it

In September 2026 Tom di Mino released a pre-print called *"Ya Diktu: Grammar of
the Minoan Peak Sanctuary Libation Formula"*. It argues that **Linear A** records
a **Semitic** language.

Some terms, before anything else.

* **Linear A** is the writing system of Bronze Age Crete. It has never been
  deciphered. We can read the signs — we know roughly what sounds most of them
  stood for, because a later script, Linear B, reused many of them — but nobody
  knows what language the words are in.
* A **Semitic** language is one of a family that includes Hebrew, Arabic,
  Aramaic, Akkadian, Phoenician and Ugaritic.
* A **transliteration** is the standard way of writing Linear A signs in Latin
  letters, like `A-TA-I-*301-WA-JA`. It records *which signs are written*, not
  what they meant. Signs whose sound is unknown are written with a star and a
  number, like `*301`.
* A **root** is the idea at the heart of a Semitic word. Semitic words are built
  on a skeleton of usually three consonants: Hebrew *k-n-s* is the root behind
  "to gather", and the vowels change as the grammar changes.

The paper's method is to read a Linear A word's signs as consonants, and then to
find a Semitic root with those consonants and a meaning that suits the
inscription. Linguists have not confirmed the claim.

**This project set out to test the claim fairly.** It did not assume the paper
was right and did not assume it was wrong. It worked in eight small cycles, each
with a written report, each finishing before the next was designed. Matches were
reported as plainly as mismatches.

**Who did the work.** The project is **Kris Bennett's**. Claude, in chat,
designed the tests and wrote the brief for each cycle. Claude Code wrote and ran
the scripts and wrote the reports. Every number below comes from code in
`scripts/`, and every cycle can be re-run.

**The single most important thing to understand about what follows.** Every test
here measures one thing only: **how easily the paper's spelling rules let a
Linear A word be read as some Semitic root.** None of them judges **meaning** —
whether a reading makes sense in the inscription it is written on. The paper's
case rests on meaning as well as on spelling. **Nothing in this project shows
whether Linear A is or is not a Semitic language, and nothing below should be
read as saying so.**

---

## 2. The data

Everything was downloaded, its size and **SHA-256** recorded — a SHA-256 is a
fingerprint of a file's exact contents, so anyone can confirm they have the same
file — and checked against known answers before use.

### The paper

| | |
|---|---|
| Title | *Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula* |
| Author | Tom di Mino |
| Version | Pre-print version 1.0, publicly released 12 August 2026; DOI record issued 12 September 2026; it supersedes an earlier DOI, `10.5281/zenodo.21903481` |
| Source | `https://www.minoanmystery.org/linear-a/ya-diktu-grammar-tom-di-mino.pdf` |
| Size | 446,199 bytes, 42 pages |
| SHA-256 | `2204ea0e6d1a0c09957b962bad8feb058a9e7275cdb1380699ec926beb93dc2b` |
| DOI | [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321) |
| Licence | CC BY 4.0. Words, readings and page references quoted here are reused under it. |

### The Linear A corpus

| | |
|---|---|
| Source | Linear A Explorer (Hogan, 2019–), [mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz) |
| Size | 1,609,137 bytes |
| SHA-256 | `4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c` |
| Contents | 1,721 inscriptions, 8,601 word tokens, 995 distinct hyphenated words |

The paper worked from **1,780** inscriptions; this file has **1,721**. The whole
shortfall sits in material added after GORILA, the standard printed corpus. That
is a property of the file, not a fault in the paper, and small gaps below are
expected because of it.

### The word lists

| list | source | size / fingerprint | licence |
|---|---|---|---|
| **Hebrew** | Strong's Hebrew dictionary (James Strong, 1894, public domain), JSON edition by [Open Scriptures](https://github.com/openscriptures/strongs) | 2,003,130 bytes, SHA-256 `5ce6aeed…fc3739`; 8,674 entries → **1,501** root skeletons | CC BY-SA |
| **Ugaritic** | [Copenhagen Ugaritic Corpus](https://github.com/DT-UCPH/cuc), University of Copenhagen — the project the paper itself cites for Ugaritic | 168,731 bytes, SHA-256 `e6e599be…984931`; 4,996 entries, 570 verbs → **595** roots | **CC BY-NC 4.0.** Used for research only; neither it nor anything built from it is redistributed here |
| **English words** | [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english) | 75,153 bytes, SHA-256 `d6b3e04f…05ed86`; 9,894 words | Data from the Google Web Trillion Word Corpus (Brants and Franz), distributed by the **Linguistic Data Consortium**; educational and research use permitted under the LDC licence, Norvig's MIT licence for his own contributions, and US fair use. Commercial use not recommended without an LDC licence |
| **English sounds** | [CMU Pronouncing Dictionary](https://github.com/cmusphinx/cmudict), Carnegie Mellon University | 3,618,488 bytes, SHA-256 `81917843…1c3d22`; 126,052 words | BSD-style |

**None of the derived word lists is committed to this repository.** Each report
records the download URL, size and fingerprint so anyone can rebuild them.

---

## 3. What held up

A good deal did, and it should be said first and plainly.

**The corpus file is the right one.** Four counts stated in advance were
reproduced exactly: 1,721 inscriptions, 995 distinct hyphenated words, 37
occurrences of `KU-RO`, and 238 standalone `*301` signs.

**The paper's own counts are careful.** Seven numbers the paper states were
re-counted from the corpus:

| what the paper says | what we counted | |
|---|---|---|
| 1,468 inscriptions from GORILA | **1,468** | exact |
| `*301` stands alone 238 times | **238** | exact |
| at four sites: Hagia Triada (mostly), Khania, Knossos, Zakros | **the same four**, 230 / 5 / 2 / 1 | exact |
| `*314` occurs 6 times | **6** | exact |
| at Hagia Triada, Kophinas, Phaistos, Arkhalokhori | **the same four** | exact |
| the formula's first verb occurs 15 times | **15** (including the paper's own §8 variant) | exact |
| the vowels a, i, u are 80.8% of syllable signs | **81.1%** | close |
| `*301` occurs 291 times in all | **290** | one short |
| AB79 appears in 25 distinct words | **24** | one short |

The two one-short results are exactly what 59 missing inscriptions would cause.
Recovering the GORILA figure to the unit — from a part of the file that exists
for an unrelated reason — is a stronger check than the headline number would have
been.

**A correction the paper makes to another scholar is right.** Appendix B says
that Davis mis-transcribed a word as `A-DU-RE-ZA`, and that the tablet KH 11
actually reads `A-DU`, a word divider, then `ZA`, with no `RE`. The corpus opens
KH 11 with exactly `A-DU 𐄁 ZA`. The paper predicted this mismatch and the corpus
confirms it.

**Nearly every reading is where the paper says it is.** Every word the paper
reads was listed — 167 rows, 114 distinct words — and each was looked for in the
inscription the paper cites. **138 of the 167 came out exactly as printed.** Of
the remaining 29, nine differ only by spelling conventions the paper itself
declares, and sixteen differ only in where the word boundaries fall. **Only three
were genuinely absent, and one of those three is the Davis mismatch the paper
itself predicted.**

**Appendix B counts itself correctly.** It claims 67 sign-group entries; 67 were
parsed. Its internal figure for words attested only once reproduces at 39
(58.2%).

**The paper's spelling rules can be written down, and they work.** Cycle 3 turned
the paper into a table of **66 rules** — 47 that the paper states outright, 19
that it uses without stating. Cycle 4 turned that table into code. Running it on
the paper's own readings, **86 of 89 were reproduced**, using only rules from the
table. Seven more rules had to be added along the way, and each was tied to a
page and a quotation showing the paper uses it.

---

## 4. Where the paper and the corpus disagree

These are not accusations. Word division in Linear A is genuinely contested, and
the corpus is not automatically right. But each is specific, and each does work
in the paper's argument.

**1. IO Za 6 — one word or two.** The corpus has `I-NA-TA-I-ZU-DI-SI-KA` as a
single unbroken word. The paper reads it as two, `I-NA-TA · I-*79-DI-SI-KA`, and
identifies `I-NA-TA` as the goddess Anat. That split carries weight in the
paper's cross-site argument.

**2. KN Zc 7 — the paper's most confident reading.** `A-KA-NU` is the only word
in the paper marked CONFIRMED. The corpus writes `A-KA-NU-ZA-TI` as one word.
`JA-SA-RA` is likewise inside the corpus's `JA-SA-RA-A-NA-NE`. Four of Appendix
A's seven words are affected by these two joins.

**3. PK Za 11 is read two incompatible ways.** In the main text (§4.3, the §8
table and the §8 discussion) the paper prints **`SA-SA-RA-ME`** and explains that
at Palaikastro "the initial JA is consistently dropped". In Appendix B it prints
**`A-SA-SA-RA-ME`** for the same spot and explains it the other way round, as a
Palaikastro variant with an added `ʾa-` prefix. One reading takes the preceding
`A` as part of the word; the other does not take it at all. Both cannot be right
about the same place. The paper does not note the difference.

**4. Where `A-SA-SA-RA-ME` actually appears.** The corpus attests that spelling at
**IO Zb 10 (Iouktas)**, where it is the whole inscription. At PK Za 11 the corpus
writes `A` and `SA-SA-RA-ME` with no word divider between them. This matters
because the Palaikastro rule is the paper's explanation for the form, and on the
corpus's evidence the spelling is attested at Iouktas instead.

**5. `*319` against `*904`.** In two Appendix B entries the paper writes a sign as
`*319` where this corpus numbers it `*904`. Whether these are two numberings of
one sign or two different signs is **unknown** from the files we have. The
practical effect: no word in the corpus contains the sign the paper calls `*319`.

**6. Nodules against roundels.** The paper says the 238 standalone `*301` signs
stand on **roundels**, a particular kind of clay document. In this corpus's own
labelling, **not one of the 151 roundels carries a standalone `*301`**. The 225
Hagia Triada documents concerned are labelled **Nodule**. This is a terminology
difference rather than a counting error, but it touches what kind of document the
sign is claimed to abbreviate on.

---

## 5. What the tests found about the matching method

### Cycle 4 — building the matcher, and how much choice the rules give

The 66-rule table was turned into code that takes a Linear A word and lists every
Hebrew root it could be read as. It reproduced **86 of 89** of the paper's own
readings.

Then the same code was pointed at the corpus, and the question became how much
choice the rules leave. **Among the words the paper reads, a typical word matches
about 190 Hebrew roots** — the median is 188, the range 32 to 322, out of roughly
1,390 roots in the whole dictionary. **Across all 787 readable corpus words the
median is about 120.** The paper's own words are longer than average, and longer
words match more.

### Cycle 5 — testing one specific claim

On p. 5 the paper says the value of the unknown sign `*301` had to fit "every
other occurrence of `*301` within the Linear A corpus", and that "only /na/ stood
its ground". So every other consonant was tried in its place, on the 20 corpus
words that contain the sign.

**26 of the 27 candidate sounds fit 19 of the same 20 words.** Ranked by how many
roots they produce, **"na" comes 5th of 27**, behind p, b, l and q. The paper's
own first filter — that the root must be shaped C-w-y — leaves **15** of the 26
consonants standing, not one.

The control matters more than the result. The same test was run on three signs
whose sounds are already known. The true value of **JU** ranked 1st of 27; for
**RA₂**, which the rules read as r or l, the better of the two ranked 10th and r
itself 16th; and **WI** ranked **26th of 27**. A test that ranks a known-correct answer
second from last cannot certify anything — which cuts both ways. **It does not
show /na/ is wrong.**

### Cycle 6 — the made-up-word test

If real Linear A words really spell Semitic words, they should match Semitic
roots more easily than invented words do. Three sets were compared: the 787
readable corpus words; the same words with their own signs shuffled into a new
order; and invented words built from the corpus's own sign patterns.

**They match equally well.** Median roots matched: real 119, shuffled 127,
invented 117. Coverage — the share of words matching at least one root — 99.3%,
97.9%, 98.2%. For words of 2 to 4 signs, which is 646 of the 691 real words the
paper never read, the three sets are indistinguishable.

And the paper's own roots showed no preference for real Linear A. They appear in
**77%** of real words the paper never looked at, **84%** of shuffled words and
**74%** of invented ones.

### Cycle 7 — does the word list matter?

The author raised a fair objection: Strong's is built from the Bible, and
Biblical Hebrew is not the whole of the language. A root that existed in Bronze
Age West Semitic might simply be missing from it.

That was tested on its own terms. Four lists were compared: Hebrew; Hebrew plus
the Ugaritic verb roots of the project the paper itself cites; 1,501 **invented**
roots with Hebrew's exact size, lengths and letter mix; and 1,501 skeletons built
from common **English** words.

* **Adding Ugaritic raises everything equally.** Real words go from 119 to 141
  roots, invented words from 117 to 137 — both about 18%. Per root added, the
  Ugaritic entries are slightly *harder* to match than the Hebrew ones. The gap
  between real and invented words does not widen.
* **Real Linear A words show no special liking for real Semitic roots.** Given
  two lists of identical shape, one real and one invented, real Linear A words
  prefer the real roots by 5.7% — and **invented Linear A words prefer them by
  4.6%**. The leftover is about 1%, and it changes sign depending on word length.
* **Even English nearly saturates the test. 98.8%** of real corpus words match an
  English "root". English scores lower on the *number* of roots matched, but most
  of that is one rule: the paper's rules let a throat consonant (ʾ ʿ h ḥ) go
  unwritten, 53.8% of Hebrew roots contain one, and only 7.9% of English ones do.
  Remove throat consonants from both lists and Hebrew's advantage falls from 3.5×
  to 1.5×.
* **The same holds with no dictionary at all.** Matching straight against the 46
  roots the paper *states*: real words it never read score **54.7%**, invented
  words **52.9%**.

---

## 6. How tight is each individual reading? (cycle 8)

The tests above are about the method in bulk. This one is about each reading on
its own.

For each of the paper's 55 distinct readings, two numbers were measured:

* **Options** — how many Hebrew roots that word matches at all. This is how much
  freedom the rules left when the root was chosen.
* **Chance** — the share of 1,000 invented words of the same length that can also
  be read as that root. A **low** chance means a **tight** fit.

The results split sharply depending on which rules are allowed.

| | all the paper's rules | only the rules it states |
|---|---|---|
| readings that still work | **53 of 55** | **31 of 55** |
| median chance | 0.35% | 0.30% |
| **median options** | **189** | **12** |
| smallest number of options | 43 | **1** |

**With all the rules, the tight fits prove little.** The median reading's word
matches 189 roots. Choosing one of 189 candidates and then noting that this
particular one is rare is not surprising — that is what choosing from 189 looks
like. The rarity is in the naming, not in the fit.

**With only the stated rules, some readings look genuinely tight.** The median
word matches 12 roots, not 189. Three readings — `U-NA-RU-KA-NA-SI`,
`U-NA-KA-NA-SI` and `RA-KI-NI-SE` — match **exactly one** Hebrew root, and in
each case it is the root the paper gives: *k-n-s*. Seven readings in all have
both a chance of 0.5% or less and ten options or fewer.

### But some of that tightness is built in (cycle 9)

A rule the paper states **only in the passage that reads a word** will naturally
fit that word. The rule and the reading are then one claim, not two, and the
tightness cannot count as support.

Cycle 9 tested that. For each of the 31 readings, it found the rules the paper
states nowhere except in that reading's own section (or Appendix B entry),
switched off **only** those, kept every other stated rule on, and measured again.

* **11 of the 31 readings use at least one such rule.**
* **None of the 11 survives.** Every one of them depended on it; not one had a
  second route to its root.
* **The three `k-n-s` readings are among the eleven.** R42 (U-NA- = *hunna*),
  N03 (RU = *lū*) and R44 (RA- = *la-*) are all introduced in §5.1, the section
  that reads those words. So is R25, the value `*301` = /na/ that
  `A-TA-I-*301-WA-JA` needs, stated only in §4.1 where that verb is read.
* **20 readings survive**, and they are exactly the 20 that had nothing to switch
  off. Four of them stay tight — ten options or fewer, chance 0.5% or less:
  `A-TA-I-*301-WA-E` and `A-TA-I-NA-WA-JA` (the invocation verb, n-w-y),
  `SI-KI-NE` (š-k-n) and `KI-DA-RO` (q-d-r).

Two of those four are the same invocation verb restated in the paper's own
translation and cross-site tables, which is a different passage by the test but
thin as independent evidence. What is solid about them is narrower:
`A-TA-I-NA-WA-JA` spells its fourth sign `NA` rather than `*301`, so it never
needs the rule written for `*301`. That leaves `SI-KI-NE` and `KI-DA-RO` as the
clean cases — ordinary words, read elsewhere in the paper, reachable on rules
stated for other words.

**So the honest version is narrower than cycle 8 first put it.** Where a reading
rests on rules the paper states for *other* words, its tightness is real evidence
— and about twenty readings are in that position, four of them tight. Where a
reading needs a rule introduced to read it, the tightness is partly built in and
cannot be counted twice. The readings that most caught the eye — the three
matching only *k-n-s* — are in the second group. They may still be right; they
just cannot be their own evidence.

Two further notes. The seven words of the libation formula are **not** the
paper's tightest readings: with all rules on, their median place is 27th of 46.
And the individual chances must **not** be multiplied into one number — the
readings are not independent, the roots were chosen after the words were seen,
and the set of printed readings is itself selected for success. A product would
look like overwhelming proof while measuring none of those things.

---

## 7. What these tests cannot judge

Three large things sit outside everything above.

**1. Meaning.** This is the big one. Every test here asks whether signs *can* be
read as a root. None asks whether the result makes sense on a libation table at a
mountain shrine. The paper's own footnote 10 on p. 5 shows that judgement doing
real work: it rejects a root that fits mechanically because it gives no
"contextually viable reading". Code cannot weigh that. So nothing here shows any
individual reading is wrong.

**2. The 238 standalone `*301` signs.** The sign stands alone on 238 documents,
and the paper reads it there as a whole word, *nawā*. A word sign has no
consonant skeleton to match, so this method cannot touch it — and it is most of
the evidence the paper cites for that sign.

**3. The 508-entry word list.** The paper mentions a 508-entry lexicon once, at
the end of §9 (p. 20), and never prints it. As far as we can see it is
unpublished. It may be attached to the Zenodo record; Zenodo returned server
errors on every attempt across the whole project, so its file list is still
unknown. That word list is the single thing most likely to change the picture.

---

## 8. Every correction made along the way

Including our own. Several of the mistakes were in the briefs Claude wrote, not
in the paper or in the code.

| # | cycle | date | what was wrong | how it was fixed |
|---|---|---|---|---|
| 1 | 2 | 16 Sep 2026 | **Our brief's error.** Cycle 1 §1.3 said the paper "contains a 508-entry lexicon as Appendix B, inside the PDF". Wrong on both counts: the 508-entry lexicon is mentioned once and never printed, and Appendix B is a different thing — an index of 67 sign-groups from Davis 2026. It wrongly implied the word list was already in hand. | §1.3 rewritten, dated note added at the top of `reports/cycle-01.md` |
| 2 | 2 | 16 Sep 2026 | **Our own test's error.** The first version of the PK Za 11 check asserted that `A` was the token immediately before `SA-SA-RA-ME`. It is not — a line-break token sits between them. | The test was corrected to check what was actually claimed. The checker itself was not changed |
| 3 | 4 | 16 Sep 2026 | **Our brief's error.** Cycles 1 and 2 said the Zenodo 504 errors were "our network reaching Zenodo, not something about this particular record". That was a guess and it was wrong: the owner's own browser on a different network got the same 504, and Plazi's uptime monitor logged Zenodo 504s on 14 and 16 September 2026. | Dated notes added to the top of `reports/cycle-01.md` and `reports/cycle-02.md`. The conclusion — file list unknown — is unchanged; the reason is not |
| 4 | 5 | 16 Sep 2026 | `reports/cycle-02.md` was headed "Date run: 17 September 2026". The machine's date for cycles 2, 3 and 4 was 16 September. | Header corrected, dated note added. One line inside `reports/cycle-01.md` — the cycle 2 correction note — carried the same wrong date and was left as written at the time; it was corrected in cycle 9, row 9 below |
| 5 | 7 | 16 Sep 2026 | **Our brief's error, twice over.** It said about 22 Ugaritic entries use irregular notation and that the regular ones give 531 roots. In fact **69** entries need hand treatment (54 of them structurally irregular), and the clean entries give 485 roots, or 500 once `*` and `(?)` are stripped. 531 could not be reproduced by any reading. | All 69 expanded by hand and listed in `reports/cycle-07.md`; the final count, **595**, is the one used |
| 6 | 7 | 16 Sep 2026 | **Our brief's error.** It said a word's possible roots "don't depend on the list", so they could be worked out once and checked against every list. Three rules — R22, R24 and N04 — look ahead into the list before deciding whether they may fire. The shortcut would have inflated the Hebrew figures by 2.88% and changed the answer for 234 of 787 words. | Each list matched against its own list instead, which also keeps cycle 7's Hebrew column identical to cycle 6's. The deviation and its measured cost are recorded in `reports/cycle-07.md` §1 |
| 7 | 8 | 16 Sep 2026 | **Our error.** The README and `reports/cycle-07.md` described the English word list as being under an "MIT licence". Its `LICENSE.md` says the data comes from the Google Web Trillion Word Corpus via the Linguistic Data Consortium; research use is permitted under the LDC licence, Norvig's MIT licence for his own contributions, and US fair use; commercial use is not recommended without an LDC licence. | Both credit lines corrected, dated note added to `reports/cycle-07.md` |

| 8 | 9 | 16 Sep 2026 | **Our error, in this write-up.** §6 called the stated-only tightness "the clearest single conclusion of the project" and said it "runs in the paper's favour". That overstated it: 11 of the 31 readings — including all three `k-n-s` readings it singled out — depend on a rule the paper states only in the passage that reads the word, and none of them survives without it. | §6, §9 and "A last word" rewritten to what cycle 9 supports; a dated note added to `reports/cycle-08.md` §2 |
| 9 | 9 | 16 Sep 2026 | **Our error.** Rows 1 and 2 of this table were dated 17 September 2026. Cycle 2 ran on 16 September — the same clock error cycle 5 fixed in `reports/cycle-02.md`'s header. | Both rows corrected, and the same wrong date inside the cycle 2 correction note at the top of `reports/cycle-01.md` |
| 10 | 9 | 16 Sep 2026 | **Imprecision in this write-up.** §5 said "a typical Linear A word matches about 190 Hebrew roots". That is the median for the words the paper reads (188), not for the corpus: across all 787 readable corpus words the median is about 120. | Both figures now given |

Code faults caught before publication are recorded in the cycle reports where
they occurred — among them a character class that silently truncated roots ending
in *s*, a site code read as a language label, a compound rule loose enough to let
leftover signs be ignored, and three rule switches that could not be turned off.
Each was found by a check that failed, and each is described where it happened.

---

## 9. What would make the matching evidence stronger

Offered as constructive suggestions, in the order we would try them.

1. **State every rule in advance, in one place.** 19 of the 66 rules we could
   reconstruct are used but never stated, and cycle 4 had to add seven more from
   worked examples. A single numbered table — each rule saying exactly what it
   permits — would let any reader check a reading without reverse-engineering it.
2. **Show the readings still work with only the stated rules — and with rules
   stated somewhere other than where the word is read.** 31 of 55 readings
   survive on the stated rules alone, which is a real strength worth presenting
   first. But cycle 9 found that 11 of those 31 depend on a rule the paper states
   only in the passage that reads the word, and none of the 11 survives without
   it. The strongest version of this evidence is a rule stated in one place that
   then **correctly predicts a reading somewhere else** — as `SI-KI-NE` and
   `KI-DA-RO` do. Marking, for each reading, which rules it needs and where each
   of those rules is first stated would let a reader see that at a glance.
3. **Predict readings before checking them.** Choose a set of inscriptions, fix
   the rules, publish the predicted readings, and only then compare. This removes
   the single biggest objection to everything in §5 and §6 — that the root was
   chosen after the word was seen. Even a handful of pre-registered predictions
   would be worth more than many after-the-fact readings.
4. **Quote the tightness alongside each reading.** How many roots could this word
   have been? How many other words could have been read this way? A reading with
   one option is a far stronger claim than one with 189, and the difference is
   invisible unless it is stated.
5. **Publish the 508-entry word list.** It is the largest body of evidence
   mentioned but not shown, and it would let the tests in cycles 5 to 8 be run
   against the paper's full claim rather than the readings that happen to be
   printed.
6. **Settle the two PK Za 11 readings**, and say which word divisions the argument
   depends on. Where the corpus and the paper split words differently, saying so
   openly costs little and pre-empts the obvious objection.

---

## 10. Open items

* **The 508-entry word list, once it is released.** Everything in cycles 5 to 8
  could be re-run against it.
* **A test that judges meaning.** This is the missing piece in every cycle. Every
  test here measures spelling only, and meaning is where the paper's argument
  actually lives. Whether such a test can be built fairly is an open question;
  nothing here has tried.
* **A closer copy of Linear A's sign patterns.** The invented words in cycles 6
  to 8 are drawn from a model that copies which sign follows which, one pair at a
  time. A model using three-sign runs would be a closer imitation and would test
  whether the small real-word advantage in longer words survives.
* **Zenodo's file list.** Still unread. The outage is on Zenodo's side, so this is
  worth simply retrying.

---

## The eight cycles

| | report | what it did |
|---|---|---|
| 1 | [cycle-01.md](cycle-01.md) | Gather the sources; re-count seven numbers the paper states |
| 2 | [cycle-02.md](cycle-02.md) | List every reading the paper prints; check each against the corpus |
| 3 | [cycle-03.md](cycle-03.md) | Write down the paper's spelling rules; build the Hebrew word list |
| 4 | [cycle-04.md](cycle-04.md) | Build the matcher; check it finds the paper's own readings |
| 5 | [cycle-05.md](cycle-05.md) | Test the reading of `*301` as "na", with a control |
| 6 | [cycle-06.md](cycle-06.md) | The made-up-word test |
| 7 | [cycle-07.md](cycle-07.md) | Does the choice of word list change the answer? |
| 8 | [cycle-08.md](cycle-08.md) | How tight is each reading; this write-up |
| 9 | [cycle-09.md](cycle-09.md) | Do the tight readings survive without the rules written for them? |

Supporting tables: [cycle-02-readings.csv](cycle-02-readings.csv),
[cycle-03-readings.csv](cycle-03-readings.csv),
[cycle-03-rules.csv](cycle-03-rules.csv),
[cycle-04-selftest.csv](cycle-04-selftest.csv),
[cycle-04-rules-added.csv](cycle-04-rules-added.csv),
[cycle-04-formula-matches.csv](cycle-04-formula-matches.csv),
[cycle-05-rankings.csv](cycle-05-rankings.csv),
[cycle-06-sets.csv](cycle-06-sets.csv),
[cycle-07-lists.csv](cycle-07-lists.csv),
[cycle-08-readings.csv](cycle-08-readings.csv),
[cycle-09-own-passage.csv](cycle-09-own-passage.csv).

---

## A last word

The paper is careful where it can be checked. Its counts hold up, its readings
are where it says they are, its correction to another scholar is right, and its
spelling rules can be written down and made to reproduce its own results. Those
are real things and they should not be lost in what follows.

What the tests show is that the **mechanical** half of the method does not narrow
the field. It says yes to nearly every word, whatever word list you give it, and
whatever the word actually is — including words we invented. Where the paper
leans only on the rules it states outright, that changes, and some readings
become genuinely tight. Where it needs the unstated rules, it does not.

One further qualification, found last and worth keeping in view. Some of the
tightest readings rest on rules the paper introduces in the same passage that
reads the word. There the rule and the reading are a single claim, and the
tightness cannot be counted as separate support. About twenty readings are not
in that position, and four of those are tight — they are reached by rules the
paper stated for other words, and they are the sturdiest thing this project
found.

The rest of the argument rests on meaning, and on the fit of the whole formula —
and those we could not test. **Whether Linear A is a Semitic language is not
something this project can answer, and it has not tried to.**
