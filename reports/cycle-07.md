# Cycle 7 — does the word list matter?

**Date run:** 16 September 2026
**Scope:** one objection. Cycle 6 found that made-up Linear A-like words match
Hebrew roots about as easily as real Linear A words do, and that the paper's own
roots turn up in real words it never read no more often than in made-up words.
The author's reply is a fair one: the Hebrew list comes from Strong's, which is
built from the Bible, and Biblical Hebrew does not cover the whole of the spoken
language. A root that existed in Bronze Age West Semitic may simply be missing
from it. This cycle tests whether the **choice of word list** changes cycle 6's
result. **No claim is made here about whether Linear A is or is not a Semitic
language.**

Files written: `reports/cycle-07-lists.csv`, `scripts/30_cycle7_lists.py`,
`scripts/31_cycle7_compare.py`, `scripts/32_cycle7_throat.py`.

**Settings.** Both rule sets from cycle 5 (**full**, 58 switches; **stated
only**, 40), prefixes and suffixes on, and **R62 and R63 off throughout** so
real and made-up words are judged alike. The word sets are cycle 6's, rebuilt
from **seed 20260916**: the 787 readable corpus words (96 read by the paper,
691 never read) and the 7,870 Linear A-like draws. The shuffled set is dropped,
as the brief directs.

**Terms used below, defined on first use.** A **lexicon** is a dictionary of a
language. **Positional letter frequency** is how often each letter turns up as
the first, second, third … letter of a root. **Matches per 1,000 roots** is the
average number of roots a word matches divided by the size of the list, times a
thousand — it lets lists of different sizes be compared, since a longer list
gives more chances to match. A **difference of differences** is what is left
when you take one gap away from another: here, how much more real words prefer
real roots than made-up words do. Terms from cycles 1–6 — root, skeleton,
primitive root, throat consonant, stop, rule set, coverage, median, word type,
bigram — are not redefined.

**Licence.** The Ugaritic lexicon is CC BY-NC 4.0. It is used here but
**neither it nor any list built from it is committed or redistributed**. None of
the four root lists is committed; `scripts/30_cycle7_lists.py` rebuilds them all
from the seed and the three downloads.

---

## 1. One deviation from the brief, and why

The brief says: *"Each word's possible skeletons don't depend on the list, so
work them out once per word and check them against every list."* That is very
nearly true, but not quite, and the exception matters enough to report.

Three rules **look ahead into the list** before deciding whether they may fire:

* **R22** — an unwritten /s/ is allowed only *before a stop*, so the matcher has
  to ask whether any root in the list continues with a stop at that point;
* **R24** — an unwritten /r/ is allowed only when the root continues;
* **N04** — an unwritten middle /w/ is allowed only where a three-letter root
  has /w/ as its second letter.

So a word's possible skeletons depend a little on what is in the list. Measured
over all 787 real words under the full rule set:

| | Hebrew matches |
|---|---|
| each list matched against its own trie (used below) | 97,350 |
| one shared trie over all five lists, then filtered to Hebrew | 100,156 (**+2.88%**) |
| real words where the two disagree | **234 of 787** |

The shortcut would have inflated every list by whatever the other lists happen to
contain. **Each list is therefore matched against its own trie.** That is what
cycles 4–6 did, and it means the Hebrew column below reproduces cycle 6 exactly
— which is checked in §3.

---

## 2. Step 1 — the four root lists

### Downloads

All three files matched the sizes and hashes in the brief exactly.

| file | bytes | SHA-256 |
|---|---|---|
| `ugaritic_lexicon.txt` | 168,731 ✓ | `e6e599be…5984931` ✓ |
| `google-10000-english-no-swears.txt` | 75,153 ✓ | `d6b3e04f…c05ed86` ✓ |
| `cmudict.dict` | 3,618,488 ✓ | `81917843…91c3d22` ✓ |

### List 1 — Hebrew

Cycle 6's list: the skeletons of every non-Aramaic Strong's entry marked
*primitive root*, plus the final-h-as-y form where cycle 3 recorded one.

| check | expected | got | |
|---|---|---|---|
| distinct skeletons | 1,501 | **1,501** | PASS |
| three letters | 1,498 | **1,498** | PASS |
| four letters | 3 | **3** | PASS |

The count in the brief is confirmed exactly; there is no difference to explain.

### List 2 — Hebrew plus Ugaritic

The verb roots of the Copenhagen Ugaritic Corpus lexicon — the same project the
paper cites for Ugaritic.

| check | expected | got | |
|---|---|---|---|
| lexicon entries | 4,996 | **4,996** | PASS |
| entries marked `vb` | 570 | **570** | PASS |
| `y-t-n` in the list | yes | **yes** | PASS |
| `p-n-y` in the list | yes | **yes** | PASS |
| `n-w-y` in the list | no | **absent** | PASS |
| `k-n-s` in the list | no | **absent** | PASS |

**Distinct Ugaritic verb roots: 595** — 87 of two letters, 503 of three, 5 of
four. 280 of them are already in the Hebrew list, so the **combined list is
1,816 skeletons**.

The 87 two-letter roots are worth flagging. The lexicon writes hollow and
geminate roots with two radicals — `/ʕ-d(-d)/` names both *ʕ-d* and *ʕ-d-d* —
and a two-letter root is far easier to match than a three-letter one. Part of
any rise from adding Ugaritic is therefore root *length*, not Ugaritic
vocabulary.

**The counts in the brief, and why mine differ.** The brief expected "about 22"
irregular entries and 531 distinct roots from the regular ones. I get:

| | |
|---|---|
| entries already in plain `/x-y-z/` form (only Roman-numeral tags removed) | **501** → 485 distinct roots |
| entries clean once a leading `*` or a trailing `(?)` is also removed | **516** → 500 distinct roots |
| distinct roots found by searching for any `/x-y-…/` block anywhere in the field | 507 |
| entries needing hand treatment | **69** |
| …of those, cosmetic only (`*` or `(?)`, otherwise clean) | 15 |
| …of those, structurally irregular | **54** |

So the "about 22" depends on where the line is drawn — 54 entries have genuinely
irregular structure, and 69 need some hand treatment. I could not reproduce 531
by any reading; my closest figure for "entries already in `/x-y-z/` form" is 485
(strict) or 500 (after stripping `*` and `(?)`). Since **every** irregular entry
was expanded by hand, the number that matters is the final one: **595**.

### The notation, and the 69 hand expansions

The lexicon's own conventions, read off the entries themselves:

| written | means | expanded as |
|---|---|---|
| `*` prefix | a reconstructed form | keep the root, drop the star |
| `(?)` | uncertain | keep the root, drop the mark |
| `(-k)` | an optional extra radical | both the short and the long root |
| `x/y` | alternative letters in one slot | one root for each letter |
| `x:y` | the same, written with a colon | one root for each letter |
| `hkr` | written unsegmented | one root, letter by letter |
| `d-k(-k)/` | a missing opening or closing slash | read as if the slash were there |

The entry column below is the lexicon's own spelling, which writes aleph `ʔ`
and ayin `ʕ`; the roots column uses `ʾ` and `ʿ`, the letters the matcher uses.
All 69:

| entry | roots | entry | roots |
|---|---|---|---|
| `*/g-h(-h/y)/` | g-h, g-h-h, g-h-y | `/n-s(-y)/ (I)` | n-s, n-s-y |
| `*/g-p-r/` | g-p-r | `/n-s:ś-ʕ/ (II)` | n-s-ʿ, n-ś-ʿ |
| `*/n-ḏ-r/` | n-ḏ-r | `/p-l(-l)/` | p-l, p-l-l |
| `*/p-r-s/` | p-r-s | `/p-r(-r)/` | p-r, p-r-r |
| `*/p-ẓ-ġ/` | p-ẓ-ġ | `/p-t(-y)/` | p-t, p-t-y |
| `*/q-b-b/` | q-b-b | `/q-n(-n)/` | q-n, q-n-n |
| `*/q-l-l/` | q-l-l | `/q-ṣ(-ṣ)/` | q-ṣ, q-ṣ-ṣ |
| `*/q-ṭ-n/` | q-ṭ-n | `/q-ṭ(-ṭ)/` | q-ṭ, q-ṭ-ṭ |
| `*/r-q-q/` | r-q-q | `/r-b(-b:y)/` | r-b, r-b-b, r-b-y |
| `*/s-k(-k)/` | s-k, s-k-k | `/r-k(-k)/` | r-k, r-k-k |
| `*/t-m(-m)/` | t-m, t-m-m | `/r-n(-n)/` | r-n, r-n-n |
| `*/š-m-ḥ/` | š-m-ḥ | `/r-š(-š)/` | r-š, r-š-š |
| `*/ṣ-d-q/` | ṣ-d-q | `/s:ś-b-b/` | s-b-b, ś-b-b |
| `*/ṣ-ḥ-r/` | ṣ-ḥ-r | `/y-h(-y)/` | y-h, y-h-y |
| `*/ṣ/ḍ-b-ṭ/` | ṣ-b-ṭ, ḍ-b-ṭ | `/y/w-ḥ-l/` | y-ḥ-l, w-ḥ-l |
| `*/ṯ-q-l/` | ṯ-q-l | `/z-ġ(-y)/` | z-ġ, z-ġ-y |
| `*/ṯ-r-w/y/` | ṯ-r-w, ṯ-r-y | `/š-l(-l)/` | š-l, š-l-l |
| `/b-r(-r)/` | b-r, b-r-r | `/š-r-y/w/` | š-r-y, š-r-w |
| `/b-t(-t)/` | b-t, b-t-t | `/š-t(-t)/` | š-t, š-t-t |
| `/d-r(-r)/` | d-r, d-r-r | `/ʔ-ḫ-d(/ḏ)/` | ʾ-ḫ-d, ʾ-ḫ-ḏ |
| `/g-r(-y)/` | g-r, g-r-y | `/ʕ-d(-d)/` | ʿ-d, ʿ-d-d |
| `/h-b-ṭ/ẓ/` | h-b-ṭ, h-b-ẓ | `/ʕ-g-d/ (?)` | ʿ-g-d |
| `/l-ʔ-y/w/ (I)` | l-ʾ-y, l-ʾ-w | `/ʕ-p(-p)/` | ʿ-p, ʿ-p-p |
| `/l-ʔ-y/w/ (II)` | l-ʾ-y, l-ʾ-w | `/ʕ-s-y:s/ (?)` | ʿ-s-y, ʿ-s-s |
| `/l-ḥ(-ḥ)/` | l-ḥ, l-ḥ-ḥ | `/ʕ-z(-z)/` | ʿ-z, ʿ-z-z |
| `/m-k-(k)/` | m-k, m-k-k | `/ḥ-s/ (?)` | ḥ-s |
| `/m-r(-r)/ (I)` | m-r, m-r-r | `/ḥ-w/y-y/ (I)` | ḥ-w-y, ḥ-y-y |
| `/m-s-s(/ś)/` | m-s-s, m-s-ś | `/ḫ-r(-r)/` | ḫ-r, ḫ-r-r |
| `/m-ḥ(-w:y)/` | m-ḥ, m-ḥ-w, m-ḥ-y | `/ḫ-t(-t)/` | ḫ-t, ḫ-t-t |
| `/n-d(-y)/` | n-d, n-d-y | `/ṣ-r(-r)/` | ṣ-r, ṣ-r-r |
| `/n-g(-y)/` | n-g, n-g-y | `d-k(-k)/` | d-k, d-k-k |
| `/n-k-ṯ/(?)` | n-k-ṯ | `hkr` | h-k-r |
| `/n-p(-p)/` | n-p, n-p-p | `m-r(-r)/ (II)` | m-r, m-r-r |
| `/n-ḥ(-y/w)/` | n-ḥ, n-ḥ-y, n-ḥ-w | `n-k-m` | n-k-m |
| | | `prsḥ` | p-r-s-ḥ |

Two letters in these roots — `ẓ` and `ḍ` — are outside the matcher's alphabet, so
those roots can never match. They are left in rather than quietly dropped.

### List 3 — made-up roots

For each Hebrew skeleton, a new skeleton of the same length drawn letter by
letter from the positional letter frequencies of the real Hebrew list, rejecting
anything that is already a real Hebrew skeleton or a repeat.

**1,501 skeletons, 1,498 of three letters and 3 of four, overlap with the real
Hebrew list: 0.** Same size, same lengths, same letter mix — no real words.

One limitation worth stating: rejecting real Hebrew roots **flattens** the mix
slightly, because the commonest letter combinations are the ones most likely to
be real already. The largest positional gap is final **y**: 11.4% of real Hebrew
skeletons end in y against 6.7% of the made-up ones (the final-h-as-y forms make
final y very common in Hebrew). Averaged over all positions the largest gap in
any letter's overall share is 1.5 percentage points. The made-up list is
therefore a close but not perfect copy.

### List 4 — English

Each word's first CMU pronunciation, consonants only, mapped to the matcher's
letters, identical neighbours merged.

| check | expected | got | |
|---|---|---|---|
| distinct three-letter skeletons from the 9,894 common words | 1,041 | **1,041** | PASS |

546 of the common words are not in the CMU dictionary. The list was then filled
to the Hebrew list's exact shape from the rest of the CMU dictionary (126,052
head words), picked at random with the seed: **457** more three-letter and **3**
four-letter skeletons, giving **1,501**, of which 195 are also real Hebrew
skeletons.

**These mappings are rough, and deliberately so.** English has no counterpart to
several of the letters the rules use, so F and V are folded onto p and b, and
CH, JH and ZH onto š, g and z. Nothing here claims that English *th* is Semitic
ṯ; the point is only to have a list of real words from a language nobody thinks
is related.

**English is handicapped before the test starts.** The rules let a throat
consonant (ʾ ʿ h ḥ) go unwritten — R07 — which makes a root containing one much
easier to match. **53.8%** of Hebrew skeletons contain a throat consonant
against **7.9%** of English ones, and English can never produce ʾ, ʿ or ḥ at all.
In fact seven of the matcher's letters — **q ś ʾ ʿ ḥ ṣ ṭ** — occur in the Hebrew
list and never in the English one. §4(c) takes that into account rather than
ignoring it.

---

## 3. Step 2 — the comparison

**Known-answer check.** The Hebrew column must reproduce cycle 6. Every Hebrew
row matches `reports/cycle-06-sets.csv` (affixes on, R62/R63 off) exactly:

| word set | rule set | cycle 6 | cycle 7 | |
|---|---|---|---|---|
| real (read by the paper) | full | 0.9896 / 146.0 | 0.9896 / 146.0 | PASS |
| real (never read) | full | 0.9928 / 119 | 0.9928 / 119 | PASS |
| Linear A-like | full | 0.9820 / 117.0 | 0.9820 / 117.0 | PASS |
| real (read by the paper) | stated only | 0.6771 / 4.0 | 0.6771 / 4.0 | PASS |
| real (never read) | stated only | 0.8017 / 10 | 0.8017 / 10 | PASS |
| Linear A-like | stated only | 0.7539 / 9.0 | 0.7539 / 9.0 | PASS |

### Full rule set

Coverage — the share of words matching at least one root in the list:

| root list | word set | 2 signs | 3 | 4 | 5 | all |
|---|---|---|---|---|---|---|
| Hebrew | real, never read | 100% | 100% | 100% | 96.7% | **99.3%** |
| Hebrew | Linear A-like | 100% | 100% | 99.9% | 95.5% | **98.2%** |
| Hebrew + Ugaritic | real, never read | 100% | 100% | 100% | 100% | **99.4%** |
| Hebrew + Ugaritic | Linear A-like | 100% | 100% | 99.9% | 95.9% | **98.3%** |
| made-up roots | real, never read | 100% | 100% | 100% | 96.7% | **99.3%** |
| made-up roots | Linear A-like | 100% | 100% | 99.6% | 96.8% | **98.5%** |
| English | real, never read | 99.3% | 98.9% | 100% | 100% | **98.8%** |
| English | Linear A-like | 99.2% | 99.4% | 99.2% | 98.4% | **98.3%** |

Median roots matched:

| root list | word set | 2 signs | 3 | 4 | 5 | all |
|---|---|---|---|---|---|---|
| Hebrew | real, never read | 91 | 136 | 140 | 157 | **119** |
| Hebrew | Linear A-like | 90 | 135 | 145 | 117 | **117** |
| Hebrew + Ugaritic | real, never read | 107 | 161 | 166 | 185 | **141** |
| Hebrew + Ugaritic | Linear A-like | 107 | 159 | 173 | 137.5 | **137** |
| made-up roots | real, never read | 87.5 | 123 | 139 | 164.5 | **114** |
| made-up roots | Linear A-like | 89 | 125 | 140 | 107.5 | **110** |
| English | real, never read | 22 | 38 | 46 | 61 | **32** |
| English | Linear A-like | 21 | 36 | 46 | 43 | **31** |

Matches per 1,000 roots — the size-corrected figure:

| root list | word set | 2 signs | 3 | 4 | 5 | all |
|---|---|---|---|---|---|---|
| Hebrew | real, never read | 64.65 | 89.12 | 98.52 | 95.36 | **79.99** |
| Hebrew | Linear A-like | 64.11 | 88.83 | 95.42 | 78.19 | **78.30** |
| Hebrew + Ugaritic | real, never read | 63.25 | 87.23 | 96.86 | 94.75 | **78.47** |
| Hebrew + Ugaritic | Linear A-like | 63.12 | 87.21 | 94.09 | 77.35 | **77.07** |
| made-up roots | real, never read | 60.83 | 82.18 | 96.52 | 96.49 | **75.71** |
| made-up roots | Linear A-like | 61.23 | 84.25 | 91.90 | 76.38 | **74.83** |
| English | real, never read | 14.82 | 25.81 | 34.23 | 37.93 | **23.03** |
| English | Linear A-like | 15.02 | 25.39 | 32.43 | 32.12 | **22.96** |

### Stated-only rule set

Coverage:

| root list | word set | 2 signs | 3 | 4 | 5 | all |
|---|---|---|---|---|---|---|
| Hebrew | real, never read | 99.3% | 81.1% | 53.4% | 26.7% | **80.2%** |
| Hebrew | Linear A-like | 99.1% | 81.3% | 47.7% | 20.5% | **75.4%** |
| Hebrew + Ugaritic | real, never read | 100% | 81.9% | 53.4% | 26.7% | **80.8%** |
| Hebrew + Ugaritic | Linear A-like | 99.3% | 82.5% | 48.7% | 21.4% | **76.2%** |
| made-up roots | real, never read | 97.1% | 83.4% | 57.3% | 33.3% | **81.0%** |
| made-up roots | Linear A-like | 98.6% | 85.7% | 53.9% | 25.7% | **78.3%** |
| English | real, never read | 87.4% | 84.5% | 66.0% | 33.3% | **78.9%** |
| English | Linear A-like | 85.0% | 87.5% | 57.2% | 26.8% | **74.7%** |

Median roots matched, and matches per 1,000 roots ("all" column):

| root list | median (real / made-up) | per 1,000 (real / made-up) |
|---|---|---|
| Hebrew | 10 / 9 | 10.68 / 10.10 |
| Hebrew + Ugaritic | 12 / 11 | 10.41 / 9.94 |
| made-up roots | 9 / 8 | 10.46 / 10.35 |
| English | 3 / 3 | 2.97 / 3.01 |

---

## 4. The three questions

### (a) Does adding Ugaritic change the gap, or just raise both?

**It raises both, and does not change the gap.** Adding 315 new skeletons (1,501
→ 1,816, +21%) lifts the median for real words from 119 to 141 and for Linear
A-like words from 117 to 137 — both by about 18%. Per 1,000 roots the figure
actually falls slightly, from 79.99 to 78.47 for real words and 78.30 to 77.07
for made-up ones: the added Ugaritic roots are, if anything, a little *harder* to
match than the Hebrew ones, root for root, so the rise is simply a bigger list.

The gap between real and made-up words does not widen. Per 1,000 roots it is
**1.69** with Hebrew alone and **1.40** with Ugaritic added. Under the
stated-only set, 0.58 and 0.47. Coverage for real words rises from 99.3% to
99.4%, for made-up words from 98.2% to 98.3%.

**This answers the author's objection directly.** A wider Semitic vocabulary is
exactly what the objection called for, drawn from the project the paper itself
cites, and it does not separate real Linear A from invented Linear A. It makes
everything easier to match, real and invented alike.

### (b) Real roots against made-up roots

If Linear A really spells Hebrew-like words under these rules, real Linear A
words should fit *real* Hebrew roots better than *made-up* roots, and by more
than Linear A-like words do. Both lists hold exactly 1,501 skeletons, so the
mean numbers are directly comparable. Mean roots matched, full rule set:

| signs | real word × real root | real × made-up | gap | made-up word × real root | made-up × made-up | gap | difference of differences |
|---|---|---|---|---|---|---|---|
| 2 | 97.04 | 91.31 | +5.73 | 96.23 | 91.90 | +4.33 | **+1.40** |
| 3 | 133.76 | 123.35 | +10.41 | 133.34 | 126.46 | +6.88 | **+3.53** |
| 4 | 147.88 | 144.87 | +3.01 | 143.22 | 137.94 | +5.28 | **−2.27** |
| 5 | 143.13 | 144.83 | −1.70 | 117.36 | 114.65 | +2.71 | **−4.41** |
| all | 120.07 | 113.64 | +6.43 | 117.53 | 112.33 | +5.20 | **+1.23** |

Stated-only rule set:

| signs | real × real | real × made-up | gap | made-up × real | made-up × made-up | gap | difference of differences |
|---|---|---|---|---|---|---|---|
| 2 | 23.43 | 23.08 | +0.35 | 22.07 | 23.60 | −1.53 | **+1.88** |
| 3 | 14.45 | 13.78 | +0.67 | 15.89 | 15.43 | +0.46 | **+0.21** |
| 4 | 6.65 | 6.87 | −0.22 | 6.68 | 6.69 | −0.01 | **−0.21** |
| 5 | 1.70 | 2.63 | −0.93 | 2.25 | 2.06 | +0.19 | **−1.12** |
| all | 16.03 | 15.71 | +0.32 | 15.16 | 15.54 | −0.38 | **+0.70** |

**The difference does not show up.** Real Linear A words do prefer real Hebrew
roots to made-up ones — by 6.43 roots out of about 120, or 5.7%. But **made-up
Linear A words prefer them almost exactly as much**, by 5.20 out of 117, or 4.6%.
What is left over is 1.23 roots in 120 — about 1% — and it is not consistent:
the difference of differences flips sign with word length, **+1.40, +3.53, −2.27,
−4.41**. At five signs real Linear A words match *more* made-up roots (144.83)
than real Hebrew ones (143.13). Under the stated-only set the leftover is 0.70
of 16 and flips the same way. Coverage there actually favours the made-up roots:
81.0% of real never-read words match a made-up root against 80.2% a real Hebrew
one.

The small preference for real roots that both sets share is easy to explain
without any language: real Hebrew roots are not evenly spread over the alphabet,
and the letters they favour overlap with the letters the matcher produces most
freely. That is a property of the rules and the alphabet, not of Linear A.

### (c) How does English compare?

On the raw numbers English scores far lower: a median of 32 roots against 119,
and 23.03 matches per 1,000 roots against 79.99 — 29% of the Hebrew rate. But
almost all of that is the throat-consonant handicap, and once it is taken
into account English closes most of the gap. Restricting **both** lists to the
skeletons that contain no throat consonant at all:

| list | roots | per 1,000 (real words) | coverage |
|---|---|---|---|
| Hebrew, whole list | 1,501 | 79.99 | 99.3% |
| Hebrew, throat-free part | 693 | **26.76** | 96.1% |
| English, whole list | 1,501 | 23.03 | 98.8% |
| English, throat-free part | 1,382 | **17.75** | 97.4% |

Hebrew's advantage falls from **3.47×** to **1.51×**. The rest of it is the other
six letters English can never contain — q, ś, ṣ, ṭ and, through the throat set,
ʾ and ʿ — several of which the sign table hands out freely (the T-series writes
ṣ, the S-series writes ṣ and ś, the K- and Q-series write q).

**And the headline number barely moves at all. Under the full rule set English
matches 98.8% of the real Linear A words the paper never read** — against
Hebrew's 99.3%. Under the stated-only set, 78.9% against 80.2%, and at four
signs English is *ahead*, 66.0% to 53.4%. A list of common English words,
mapped roughly onto the matcher's alphabet, finds a "root" for very nearly every
Linear A word in the corpus.

---

## 5. Step 3 — the paper's roots, without any dictionary

Cycle 6 could only use the 35 paper roots that happen to be in Strong's. Here
every root the paper **states** is used directly — `root_kind` = "stated" in
`reports/cycle-03-readings.csv` — with no dictionary in between and **with the
four sound matches (ṯ=š, ḏ=z, ḫ=ḥ, ġ=ʿ) switched off**, since the brief asks for
the root as the paper writes it.

**46 distinct stated roots, all of three letters.** One — **e-š-r** (compared to
Akkadian) — contains a letter the matcher can never produce, so it can never
match. It is kept in the list rather than dropped, so the denominator stays the
paper's own root inventory rather than a filtered version of it. The other 45
are all reachable.

Share of words matching at least one of the 46, and the average number matched:

**Full rule set**

| word set | 2 signs | 3 | 4 | 5 | all | mean matched |
|---|---|---|---|---|---|---|
| real, read by the paper | 55.6% | 87.0% | 72.7% | 78.6% | **75.0%** | 2.96 |
| real, never read | 61.2% | 54.7% | 48.5% | 40.0% | **54.7%** | 1.65 |
| Linear A-like | 57.4% | 58.2% | 47.8% | 33.4% | **52.9%** | 1.64 |

**Stated-only rule set**

| word set | 2 signs | 3 | 4 | 5 | all | mean matched |
|---|---|---|---|---|---|---|
| real, read by the paper | 33.3% | 60.9% | 30.3% | 42.9% | **41.7%** | 0.73 |
| real, never read | 36.3% | 24.2% | 12.6% | 10.0% | **26.2%** | 0.38 |
| Linear A-like | 33.5% | 28.6% | 14.1% | 4.8% | **25.5%** | 0.42 |

**Cycle 6's finding survives without a dictionary.** Real Linear A words the
paper never read match one of its stated roots 54.7% of the time; invented words
do so 52.9% of the time, and match 1.64 of them on average against 1.65. At
three signs the invented words are ahead, 58.2% to 54.7%. Under the stated-only
set the invented words match **more** of the paper's roots on average, 0.42
against 0.38.

The words the paper does read score higher — 75.0% and 2.96 — but that row is
circular: those roots were chosen for those words. It is worth noting it is only
75%, not 100%. Two reasons: the 46 are all the *stated* roots, so a word is being
asked to match a pool that mostly belongs to other words; and cycle 4 already
found three readings that the paper's own rules do not reproduce.

---

## 6. What this cycle shows

**The choice of word list does not change cycle 6's result.**

1. **The author's objection is a fair one, and it has been tested on its own
   terms.** Biblical Hebrew is not the whole of the language, so the test was
   re-run with the Ugaritic verb roots of the very project the paper cites for
   Ugaritic added. That is the right kind of fix. It does not work: adding 315
   roots lifts real and invented Linear A by the same 18%, and per root the
   Ugaritic additions are slightly harder to match than the Hebrew ones. The gap
   between real and invented words stays where it was.

2. **Real Linear A words show no special affinity for real Semitic roots.** Given
   two lists of identical size, lengths and letter mix — one of real Hebrew
   roots, one of invented ones — real Linear A words prefer the real roots by
   5.7%, and invented Linear A words prefer them by 4.6%. The leftover is about
   1%, and it changes sign with word length. If Linear A spelled Semitic words
   under these rules, this is the one measurement that should have shown it, and
   it does not.

3. **Even English nearly saturates the test.** 98.8% of real corpus words match
   an English "root" under the full rule set. English scores lower on the *number*
   of roots matched, but most of that is the throat-consonant allowance (R07)
   rather than anything about the languages: take throat consonants out of both
   lists and Hebrew's advantage falls from 3.5× to 1.5×.

4. **And the same holds for the paper's own roots with no dictionary at all.**
   Matching directly against the 46 roots the paper states, real words it never
   read score 54.7% and invented words 52.9%.

5. **What this does not show.** It does not show any individual reading is wrong,
   and it says nothing about whether Linear A is a Semitic language. Every number
   here measures one thing: how easily the rules let signs be read as consonants
   of some root. The paper's case also rests on **meaning** — on whether a reading
   makes sense in a libation formula on a libation table — and no cycle so far
   has been able to test that. What these seven cycles do show, consistently, is
   that the *mechanical* half of the method carries almost no weight on its own:
   it says yes to nearly everything, whatever the list, and whatever the word.
   The burden therefore falls on the part a reader has to judge.

---

## 7. Choices this cycle had to make that the paper does not settle

1. **Each list matched against its own trie**, not against one shared trie
   (§1). The reason and the measured cost are given there. This is a deviation
   from the brief's suggested shortcut.
2. **The 69 irregular Ugaritic entries** were expanded using the lexicon's own
   notation, read off the entries themselves; the full table is in §2 and in
   `scripts/30_cycle7_lists.py`. Where an entry names an optional radical,
   **both** the short and the long root are kept.
3. **Roman-numeral homonym tags dropped**, as the brief directs, so
   `/m-r(-r)/ (I)` and `m-r(-r)/ (II)` collapse to the same roots.
4. **`ẓ`, `ḍ` and `e` kept in their lists** although the matcher can never
   produce them, so that the denominators stay the real inventories.
5. **Positional letter frequencies for the made-up list** are pooled over every
   skeleton that has that position. The fourth position rests on only 3 real
   skeletons, which is negligible at 3 of 1,501.
6. **English four-letter skeletons come only from the CMU fill**, since the
   brief asks for three-letter skeletons from the common-word list.
7. **Separate random streams**, both seeded 20260916, for the made-up roots and
   for the English fill, so changing one does not shift the other.
8. **Prefixes and suffixes left on** throughout, matching cycle 6's main tables;
   the brief does not ask for the off variant here.

---

## 8. Open items, for a future cycle only

* A test that scores readings on **meaning** is still the missing piece, and is
  now the only place the argument has left to be tested.
* The 238 standalone occurrences of `*301` remain untestable by this method.
* A trigram model for the Linear A-like words, to close the last gap between
  invented and real sign patterns.
* Zenodo's file list for the deposit is still unread.

---

## 9. Reproducing this cycle

```
bash scripts/run_all.sh        # scripts 01-32, in order
```

`scripts/30_cycle7_lists.py` builds the four root lists plus the paper's stated
roots into `data/derived/cycle7_lists.json`; `scripts/31_cycle7_compare.py`
matches cycle 6's words against each and writes `reports/cycle-07-lists.csv`;
`scripts/32_cycle7_throat.py` runs the throat-free comparison for §4(c).

**Nothing derived from the Ugaritic lexicon is committed**, and neither are the
other lists. The three downloads are recorded above with their sizes and hashes.

`reports/cycle-07-lists.csv` has 290 rows: one per root list, word set, rule set
and word length, plus an "all" row for each combination. Columns: `root_list`,
`roots_in_list`, `word_set`, `rule_set`, `n_signs`, `word_count`, `coverage`,
`median_roots`, `mean_roots`, `matches_per_1000_roots`.

## Credit

The paper under test is Tom di Mino, *"Ya Diktu: Grammar of the Minoan Peak
Sanctuary Libation Formula"* (pre-print, September 2026),
DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321), CC BY 4.0.

The corpus is the Linear A Explorer data (Hogan 2019–).

The Hebrew list is built from Strong's Hebrew dictionary (1894, public domain),
JSON edition by [Open Scriptures](https://github.com/openscriptures/strongs),
CC BY-SA.

The Ugaritic verb roots come from the **Copenhagen Ugaritic Corpus**
([DT-UCPH/cuc](https://github.com/DT-UCPH/cuc)), University of Copenhagen,
released under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Used here for
non-commercial research; not redistributed.

English pronunciations come from the **CMU Pronouncing Dictionary**
([cmusphinx/cmudict](https://github.com/cmusphinx/cmudict)), Carnegie Mellon
University, BSD-style licence. The English word list is
[first20hours/google-10000-english](https://github.com/first20hours/google-10000-english),
derived from the Google Web Trillion Word Corpus, MIT licence.
