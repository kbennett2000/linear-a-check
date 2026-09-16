# Cycle 6 — the made-up-word test

**Date run:** 16 September 2026
**Scope:** one question. Cycle 4 showed that under the paper's own rules a
typical Linear A word matches roughly 190 Hebrew roots. Cycle 5 showed that a
fit-based test cannot pick out sign values that are already known. This cycle
asks whether real Linear A words match Hebrew roots — and the paper's own roots
— any more easily than **made-up** words do. **No claim is made here about
whether Linear A is or is not a Semitic language.** Code cannot settle that, and
the paper's case also rests on meaning, which this test does not judge.

Files written: `reports/cycle-06-sets.csv`, `scripts/28_cycle6_sets.py`,
`scripts/29_cycle6_match.py`.

**Random seed: 20260916.** Every made-up word in this cycle comes from that
seed. The word lists themselves are not committed — running
`scripts/28_cycle6_sets.py` rebuilds them exactly.

**Terms used below, defined on first use.** A **word type** is one distinct
spelling, however many times it occurs in the corpus. A **bigram** is a pair of
neighbouring signs; the Linear A-like words below are drawn from a *bigram
model*, meaning each sign is chosen according to how often it follows the sign
before it in real words. The **median** is the middle value once the numbers are
put in order: half the words match more roots than this, half fewer. The
**mean** is the ordinary average. **Coverage** (from cycle 5) is the share of
words that match at least one Hebrew primitive root. To say a word **beats** a
share of made-up words means it matches more roots than that share of them.
Terms from cycles 1–5 — root, skeleton, primitive root, throat consonant, stop,
compound, rule set, site, syllabogram — are not redefined.

**What "match" means here, and what it does not.** As in cycles 4 and 5, a
match means only that a word's signs can be read as a root's consonants under
the rules being applied. It says nothing about whether the resulting word makes
sense in its inscription. The paper's own readings are chosen on meaning as well
as spelling, and no test below judges meaning.

---

## 1. The setting carried in from cycle 5

Both rule sets are kept exactly as cycle 5 built them:

* **full** — every rule in `reports/cycle-03-rules.csv` and
  `reports/cycle-04-rules-added.csv`, with R32 on (so `*319` = /hū/), and R62
  and R63 limited to Palaikastro and Zakros. 58 switches.
* **stated only** — only the rules the paper states outright. 40 switches. A
  sign group with no stated rule of its own keeps its plain Linear B value.

Every number below is given under both. Where a result holds under only one of
them, that is said.

**Made-up words have no site**, so R62 (initial JA- dropped at Palaikastro) and
R63 (the same at Zakros) can never fire for them. To keep the comparison even,
the real words were therefore run **twice**: once with their real sites, and
once with R62 and R63 switched off entirely. The difference is small — over all
787 real words under the full rule set, mean roots matched 126.6 with the rules
on against 123.7 with them off, a 2.3% difference, and **coverage is identical
to four decimal places either way**. All comparisons against made-up words below
use the with-them-off numbers; `reports/cycle-06-sets.csv` carries both.

---

## 2. Step 1 — the word sets

### Real

The 787 readable hyphenated corpus word types from cycle 5. (The pool is the
same under either rule set: the only sign the two sign-tables disagree about is
`*319`, which the corpus never writes — it writes `*904` instead.)

Each was marked **read by the paper** if any row of
`reports/cycle-03-readings.csv` answers to it. Cycle 2's three passes were
repeated for this — the word as printed, the word after cycle 2's sign-spelling
allowances, and the word-break pass, in which a printed reading's sign run is
found spread across the corpus's own word divisions. A word-break row marks
**every** corpus word its sign run crosses, which is the generous reading.

| | |
|---|---|
| rows in the readings table | 167 |
| rows answering to no corpus word | 4 |
| distinct corpus word types the paper reads | 105 |
| …of those, inside the readable pool | **96** |
| readable pool words the paper never reads | **691** |

The 9 read words outside the pool are there for reasons cycle 5 already
recorded: four are single signs with no hyphen (`I`, `NA`, `*307`, `*904`),
four contain a sign the matcher has no value for (`*312`, `*904`, `OLIV`), and
one contains a `+` combined sign.

### Shuffled

For each real word with at least two **different** signs, up to 10 distinct new
words made by putting that word's own signs in a new order. Any result equal to
the original, or to any corpus word type of any kind, was thrown away.

* real words with at least two different signs: **781**
* real words that cannot be shuffled: **6** — `*301-*301`, `DA-DA`, `DI-DI`,
  `JA-JA`, `TA-TA`, `TE-TE`
* made-up words: **3,735 draws, 3,723 distinct**

Short words yield few shuffles — a two-sign word has exactly one — so this set
is tilted towards longer words compared with the real pool. That is why every
table below is also broken down by length.

### Linear A-like

For each real word, 10 new words of the same length, drawn from the corpus's own
sign patterns: the first sign by how often each sign starts a real word, each
later sign by how often it follows the sign before it inside real words. Only
signs the matcher can read were used — automatic here, since the model is built
from the readable pool itself. Any draw equal to a real corpus word type was
thrown away and redrawn.

* distinct signs in the pool: 57; exactly **one** (`NWA`) occurs but never
  starts a word, and **no** sign is a dead end, so the fallback to overall sign
  frequency was never needed
* made-up words: **7,870 draws, 5,062 distinct**

Draws are kept with their repeats, so the length mix stays the one checked
below; matching is cached per distinct spelling, so the repeats cost nothing.

### The checks

**Check 1 — the shuffled set has the same signs as its sources.** Every one of
the 3,735 shuffled words was compared sign-count for sign-count against the real
word it came from. **Mismatches: 0. PASS.**

**Check 2 — the Linear A-like set has the real pool's length distribution.**

| signs | real pool | Linear A-like | expected (10×) |
|---|---|---|---|
| 2 | 287 | 2,870 | 2,870 |
| 3 | 288 | 2,880 | 2,880 |
| 4 | 136 | 1,360 | 1,360 |
| 5 | 44 | 440 | 440 |
| 6 | 20 | 200 | 200 |
| 7 | 7 | 70 | 70 |
| 8 | 2 | 20 | 20 |
| 9 | 1 | 10 | 10 |
| 16 | 1 | 10 | 10 |
| 19 | 1 | 10 | 10 |

Every length is exactly ten times the real pool. **PASS.**

**Check 3 — the 20 most common signs, side by side.** Shares are of all sign
occurrences in that set.

| # | real pool | | Linear A-like | |
|---|---|---|---|---|
| 1 | A | 4.85% | TA | 4.39% |
| 2 | JA | 4.61% | JA | 4.18% |
| 3 | TA | 4.15% | A | 4.07% |
| 4 | NA | 4.07% | NA | 3.87% |
| 5 | I | 3.83% | I | 3.71% |
| 6 | DA | 3.46% | DA | 3.50% |
| 7 | RA | 3.21% | TI | 3.37% |
| 8 | RE | 3.13% | MA | 3.24% |
| 9 | MA | 3.13% | TE | 3.20% |
| 10 | SI | 3.09% | KI | 3.03% |
| 11 | TI | 3.09% | RE | 2.97% |
| 12 | SA | 3.09% | RA | 2.94% |
| 13 | KI | 3.00% | SI | 2.91% |
| 14 | KA | 2.88% | KU | 2.79% |
| 15 | TE | 2.88% | MI | 2.74% |
| 16 | KU | 2.71% | SA | 2.72% |
| 17 | MI | 2.67% | KA | 2.68% |
| 18 | DI | 2.47% | RI | 2.36% |
| 19 | RU | 2.30% | DI | 2.32% |
| 20 | PA | 2.26% | DU | 2.26% |

**18 of the 20 signs appear in both lists**, and the largest share difference
for any sign in the real top 20 is **0.78 percentage points**. Close. **PASS.**

**Check 4 — no made-up word is a real corpus word.** All 3,735 shuffled words,
all 7,870 Linear A-like words and all 7,000 formula-comparison words were
checked against every distinct corpus word type of any kind. **Clashes: 0.
PASS.**

---

## 3. Step 2 — how many Hebrew roots each set matches

Matched against the non-Aramaic entries Strong's marks as a primitive root, with
their final-h-as-y forms, exactly as in cycles 4 and 5.

### Full rule set, prefixes and suffixes on

| word set | words | coverage | min | median | max | mean |
|---|---|---|---|---|---|---|
| real (all) | 787 | 99.2% | 0 | 123 | 316 | 123.7 |
| real, read by the paper | 96 | 99.0% | 0 | 146 | 290 | 149.8 |
| real, never read | 691 | 99.3% | 0 | 119 | 316 | 120.1 |
| **shuffled** | 3,735 | 97.9% | 0 | **127** | 333 | 128.4 |
| **Linear A-like** | 7,870 | 98.2% | 0 | **117** | 357 | 117.5 |

**Made-up words match about as many Hebrew roots as real ones.** The shuffled
set's median is slightly *higher* than the real set's, the Linear A-like set's
slightly lower, and all three are within about 5% of each other.

Because the three sets have different length mixes, the breakdown by length is
the number that matters. Median roots matched:

| word set | 2 signs | 3 signs | 4 signs | 5 signs | 6 signs | 7 signs |
|---|---|---|---|---|---|---|
| real, never read | 91 (n=278) | 136 (n=265) | 140 (n=103) | 157 (n=30) | 96.5 (n=8) | 56 (n=4) |
| shuffled | 97 (n=239) | 131.5 (n=1376) | 136.5 (n=1360) | 139.5 (n=440) | 93.5 (n=200) | 48 (n=70) |
| Linear A-like | 90 (n=2870) | 135 (n=2880) | 145 (n=1360) | 117 (n=440) | 50.5 (n=200) | 0 (n=70) |

For **2, 3 and 4 signs — 646 of the 691 real words the paper never read** — the
three sets are indistinguishable: the largest gap between real and either
made-up set is 7 roots on a median of about 130.

From 5 signs up, real words do match more than Linear A-like ones, and coverage
starts to separate too (at 6 signs, 87.5% of real never-read words match
something against 80.5% of Linear A-like words; at 7 signs, 100% against 47%).
But the counts there are small — 30, 8 and 4 real words — and the **shuffled**
set, which is made of real words' own signs, stays close to the real set
throughout. That points at the length and the sign inventory of long Linear A
words, not at their order.

### Full rule set, prefixes and suffixes off

| word set | words | coverage | median | mean |
|---|---|---|---|---|
| real, never read | 691 | 99.1% | 109 | 105.5 |
| shuffled | 3,735 | 96.4% | 108 | 104.3 |
| Linear A-like | 7,870 | 97.1% | 104 | 102.4 |

Turning the word pieces off costs every set about the same. It does **not**
open a gap between real and made-up words — which answers the worry that
shuffled words lose their real beginnings and endings: with no beginnings or
endings in play at all, they still match as much as real words do.

### Stated-only rule set

Everything is far sparser here, because most of the loosening rules are among
the ones the paper only *uses* rather than states.

| word set | words | coverage | median | mean |
|---|---|---|---|---|
| real (all) | 787 | 78.7% | 10 | 16.1 |
| real, never read | 691 | 80.2% | 10 | 16.0 |
| shuffled | 3,735 | 56.9% | 2 | 9.0 |
| Linear A-like | 7,870 | 75.4% | 9 | 15.2 |

At first sight real words beat shuffled ones badly here. **They do not.** That
whole gap is the length mix: the shuffled set is tilted long, and under this
rule set long words match almost nothing. By length, the medians are:

| word set | 2 signs | 3 signs | 4 signs | 5 signs |
|---|---|---|---|---|
| real, never read | 20 | 6 | 1 | 0 |
| shuffled | 19 | 5 | 0 | 0 |
| Linear A-like | 19 | 8 | 0 | 0 |

and coverage at 2 and 3 signs is 99.3% / 81.1% for real never-read words,
99.6% / 78.8% shuffled, 99.1% / 81.3% Linear A-like. At the same length the
three sets behave the same, and at 3 signs the Linear A-like words match
**more** roots than the real ones do.

### The seven formula words against 1,000 made-up words each

For each formula word, 1,000 Linear A-like words of the same length were drawn
and matched. R62 and R63 are off on both sides. "Beats" is the share of the
1,000 that match **fewer** roots than the real word.

| word | signs | roots (full) | beats | roots (stated only) | beats |
|---|---|---|---|---|---|
| A-TA-I-\*301-WA-JA | 6 | 163 | 83.7% | 5 | 96.8% |
| JA-DI-KI-TU | 4 | 224 | 91.0% | 12 | 78.7% |
| JA-SA-SA-RA-ME | 5 | 224 | 90.8% | 47 | 99.5% |
| U-NA-KA-NA-SI | 5 | 182 | 75.8% | 1 | 79.0% |
| I-PI-NA-MA | 4 | 131 | 41.3% | 4 | 69.5% |
| SI-RU-TE | 3 | 201 | 92.5% | 52 | 95.3% |
| TA-NA-RA-TE-U-TI-NU | 7 | 238 | 97.9% | 90 | 100.0% |

Six of the seven sit high in their own comparison group. **This cuts the
opposite way from how it first reads.** Matching *more* roots is not a sign that
a word fits Hebrew better; it is a sign that the word is easier for these rules
to bend — it is more ambiguous, not more Semitic. What the table shows is that
the formula words are **not typical Linear A words**: they are unusually
tractable ones. That is what one would expect of words picked out because they
could be read. It is not, by itself, evidence for or against the readings.

---

## 4. Step 3 — the paper's own roots

The target set is the paper's roots that cycle 3 found in the Hebrew
primitive-root list: **33** of the 59 distinct roots in
`reports/cycle-03-readings.csv` outright, plus **2** more (š-n-n, š-w-r) after
the four sound matches ṯ=š, ḏ=z, ḫ=ḥ, ġ=ʿ. **Those four are not from the
paper** — cycle 3 flagged them as such — but the matcher has applied them since
cycle 4, so including the two shifted forms is what makes the target set line up
with what the matcher actually returns. **Target set: 35 roots.**

Share of words matching **at least one** of those 35, full rule set, prefixes
and suffixes on:

| word set | 2 signs | 3 signs | 4 signs | 5 signs | overall |
|---|---|---|---|---|---|
| 1. real, read by the paper | 88.9% (n=9) | 95.7% (n=23) | 90.9% (n=33) | 100% (n=14) | **92.7%** |
| 2. real, never read | 68.0% (n=278) | 85.7% (n=265) | 81.6% (n=103) | 83.3% (n=30) | **77.3%** |
| 3. shuffled | 69.9% (n=239) | 89.1% (n=1376) | 86.1% (n=1360) | 83.4% (n=440) | **83.8%** |
| 4. Linear A-like | 60.2% (n=2870) | 84.7% (n=2880) | 87.9% (n=1360) | 77.7% (n=440) | **74.3%** |

Average number of the 35 matched per word, overall: group 1 **3.42**, group 2
**2.13**, group 3 **2.41**, group 4 **2.09**.

Group 1 scores high, as the brief expected and as it must: the paper chose those
roots for those words, so this row is circular and carries no weight.

**The comparison that matters is group 2 against groups 3 and 4, and there is no
advantage.** At every length from 2 to 5 signs the shuffled words match one of
the paper's roots **at least as often as** the real words the paper never read,
and the Linear A-like words are within a few points either side. Overall, real
never-read words 77.3%, shuffled 83.8%, Linear A-like 74.3%. The averages tell
the same story: 2.13 for real never-read words against 2.41 and 2.09 for the two
made-up sets.

Under the **stated-only** rule set the shares collapse but the ordering does not
change:

| word set | 2 signs | 3 signs | 4 signs | 5 signs | overall |
|---|---|---|---|---|---|
| 1. real, read by the paper | 44.4% | 56.5% | 24.2% | 42.9% | **38.5%** |
| 2. real, never read | 34.2% | 19.6% | 10.7% | 6.7% | **23.2%** |
| 3. shuffled | 31.8% | 20.5% | 7.7% | 5.0% | **13.1%** |
| 4. Linear A-like | 28.2% | 24.6% | 12.5% | 4.6% | **21.7%** |

At 3 and 4 signs the Linear A-like words again match the paper's roots **more**
often than the real words the paper never read. The overall column favours real
words over shuffled ones only through the length mix, as in §3.

So the result is the same under both rule sets, with prefixes and suffixes on or
off: **the paper's roots turn up in Linear A words the paper never looked at no
more often than they turn up in words that were never Linear A at all.**

### The caveat this test cannot remove

A real-word advantage, had there been one, would not automatically have meant
Semitic meaning. The rules in `reports/cycle-03-rules.csv` were themselves
distilled from real Linear A words, so they are fitted to Linear A's own
spelling habits before any question of language arises. The Linear A-like set
exists to reduce that worry — it copies those habits without copying any
meaning — but it does not remove it: a bigram model catches how signs follow one
another in pairs, not longer patterns. Here the point is moot in one direction,
since no advantage appeared to explain. It matters for reading the small
real-word edge at 5+ signs in §3, which the shuffled set suggests is about
length and sign inventory rather than anything Semitic.

---

## 5. Step 4 — what the made-up-word test shows

**The matching evidence, on its own, is weak — not because the matches are
wrong, but because a match is nearly free.**

1. **Under the paper's full rule set almost every word matches, whatever it is.**
   99.3% of real Linear A words the paper never read match at least one Hebrew
   primitive root, and so do 97.9% of shuffled words and 98.2% of words invented
   from a bigram model. A test that says "yes" to 98% of nonsense cannot
   distinguish a real reading from a coincidence.

2. **The typical word matches over a hundred roots.** A median real word matches
   119 of the roughly 1,390 primitive roots in Strong's — about one in twelve of
   the whole Hebrew root inventory. Made-up words match the same number. So
   finding *a* Semitic root for a Linear A word is not a discovery; the rules
   guarantee it. The work is being done by which root is chosen, and that choice
   is made on meaning, which this test does not touch.

3. **The paper's own roots are no more at home in real Linear A than in
   invented words.** This is the sharpest result in the cycle. Those 35 roots
   were reached through the paper's readings of about a hundred words; if they
   reflected something real in the script, one would expect them to keep turning
   up in the other 691 readable words. They do — in 77% of them — but they turn
   up in 84% of scrambled words and 74% of invented ones too. Their presence in
   a Linear A word carries no information.

4. **This is not a verdict on the readings, and not a verdict on the language.**
   Everything above measures one thing: how easily the rules let signs be read
   as roots. The paper does not rest its case there. Its readings are chosen for
   sense in context — a libation formula on a libation table — and footnote 10 on
   p.5 shows that judgement doing real work, rejecting a mechanically valid root
   because it gives no "contextually viable reading". Code cannot weigh that, so
   nothing here shows any individual reading is wrong, and nothing here shows
   Linear A is or is not Semitic.

5. **What it does show is where the weight has to be carried.** Taken with
   cycle 4 (a typical word matches about 190 roots under the rules as first
   built) and cycle 5 (the same style of test ranks the known value of the sign
   WI 26th out of 27), the picture is consistent: the mechanical half of the
   paper's method does not narrow the field. Under the stated-only rule set the
   field narrows a good deal — a median real word matches 10 roots, not 119, and
   only 79% of words match anything — which says the narrowing depends heavily
   on the rules the paper uses without stating. Any weight the argument carries
   has to come from meaning, from the fit of the whole formula, and from
   evidence outside this kind of matching. Those are the parts a reader has to
   judge, and the parts a future cycle would have to find some other way to test.

---

## 6. Choices this cycle had to make that the paper does not settle

1. **What counts as "read by the paper".** Taken as: any corpus word type that
   any row of the readings table answers to, under cycle 2's three passes,
   including the word-break pass, and marking every corpus word a split reading
   crosses. This is the generous reading, and it makes group 1 larger and group 2
   smaller — that is, it works against finding a real-word advantage being
   claimed here, so it is the safe direction.
2. **Counting by word type, not by occurrence.** Every count above treats a
   distinct spelling as one word however often it occurs, matching cycles 4 and
   5. Counting by occurrence would weight common short words much more heavily.
3. **The bigram model is built over word types too**, for the same reason.
4. **Made-up words are kept with their repeats** for the statistics, so the
   length mix stays the one Check 2 verified; within any one real word's batch of
   ten they are distinct.
5. **The target set of the paper's roots includes the two forms reached through
   the four sound matches** (š-n-n, š-w-r). Those matches are not the paper's.
   They are included because the matcher applies them, so excluding them would
   have measured something the matcher cannot return.
6. **R62 and R63 off for the even comparison.** Made-up words have no site, so
   the rules cannot fire for them; the real words were run both ways and both are
   in the CSV. The difference is 2.3% of matches and no change in coverage.
7. **The "is it real?" list used to throw out made-up words** is every distinct
   corpus word type of any kind, not only the 787 readable ones.

---

## 7. Open items, for a future cycle only

* The 238 standalone occurrences of `*301` are still untested — a word sign has
  no consonant skeleton, so this method cannot reach them. That is most of the
  evidence the paper cites for that sign.
* A test that scores candidate readings on **meaning**, not just on spelling, is
  the missing piece in every cycle so far. Whether one can be built fairly is an
  open question; nothing in cycles 1–6 has tried.
* Zenodo's file list for the deposit is still unread (the 504s are on Zenodo's
  side — see the correction notes on `reports/cycle-01.md` and
  `reports/cycle-02.md`). Worth retrying.
* The bigram model could be replaced with a trigram one, to test whether the
  small real-word advantage at 5+ signs survives a closer copy of Linear A's
  sign patterns.

---

## 8. Reproducing this cycle

```
bash scripts/run_all.sh        # scripts 01-29, in order
```

`scripts/28_cycle6_sets.py` builds the word sets from seed 20260916 and writes
`data/derived/cycle6_sets.json`; `scripts/29_cycle6_match.py` matches them and
writes `reports/cycle-06-sets.csv`. Neither the word lists nor the Hebrew list
is committed — the first is rebuildable from the seed, the second is left out
for licence reasons (see `reports/cycle-03.md`).

`reports/cycle-06-sets.csv` has 248 rows: one per word set, rule set,
prefix/suffix setting, R62/R63 setting and word length, plus an "all" row for
each combination. Columns: `word_set`, `rule_set`, `affixes`, `r62_r63`,
`n_signs`, `word_count`, `share_any_root`, `min_roots`, `median_roots`,
`max_roots`, `mean_roots`, `share_paper_root`, `mean_paper_roots`.

## Credit

The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan Peak
Sanctuary Libation Formula"* (pre-print, September 2026),
DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321), CC BY 4.0.
The corpus is the Linear A Explorer data (Hogan 2019–). The Hebrew list is built
from Strong's Hebrew dictionary (1894, public domain), JSON edition by Open
Scriptures, CC BY-SA.
