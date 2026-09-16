# Cycle 5 — testing the paper's reading of *301 as "na"

**Date run:** 16 September 2026
**Scope:** one claim only. On p.5 the paper says the value for *301 had to
complete the formula's verb and "fit into every other occurrence of *301 within
the Linear A corpus", and that under those conditions "only /na/ stood its
ground". This cycle tries every other sound in place of *301 and sees whether
"na" really is the only one that fits — and then runs the same test on three
signs whose sounds are already known, to see whether this kind of test can pick
out a right answer at all. **No conclusions about the language as a whole.**

Files written: `reports/cycle-05-rankings.csv`, `scripts/25_cycle5_setup.py`,
`scripts/26_cycle5_rankings.py`, `scripts/27_cycle5_decisions.py`.

**Terms used below, defined on first use.** A **rule set** here is a pair: which
rule switches are on, and what each sign may stand for. A **site** is the place
an inscription was dug up; the corpus records one per inscription. A **control**
is a test run on a case whose answer is already known, to check that the test
itself works. **Coverage** below means how many of the words being tested match
at least one Hebrew root. Terms from cycles 1–4 — root, skeleton, primitive
root, throat consonant, stop, compound, syllabogram, word divider — are not
redefined.

**What "fit" means here, and what it does not.** In this cycle "fit" only ever
means *the word matches at least one Hebrew primitive root*. The paper's own
sense of fit also takes in **meaning** — footnote 10 on p.5 rejects √d-w-y
"to be ill" not because it fails mechanically but because it gives no
"contextually viable reading". Code cannot judge that. So nothing below shows
the paper's reading is wrong. What it can show is whether this kind of
mechanical test supports the claim, and whether it can be trusted at all.

---

## 1. Step 0 — the header date

`reports/cycle-02.md` said **"Date run: 17 September 2026"**. The machine's date
for cycles 2, 3 and 4 was **16 September 2026**, the same day as cycle 1. The
header now reads 16 September 2026, and a dated note saying so has been added
under the existing correction note. Nothing else in that report was changed.

---

## 2. The decisions carried in from cycle 4, and what they change

### *319 gets its conditional value /hū/ (R32)

**This affects two words, both of them the paper's, and none of the corpus words
in this cycle.**

The corpus contains **no** hyphenated word with `*319` in it. Cycle 2 found why:
the paper writes `*319` where this corpus writes `*904`. So giving `*319` a value
makes **0** of the 787 readable corpus words newly readable — the count is 787
either way.

Where it does matter is the paper's own readings table: 2 rows contain `*319`
(NA-MA-MA-TI-TI-*319 and WI-JA-SU-MA-TI-TI-*319), and cycle 4 had to skip both.
With R32 on, both are found. None of the 20 *301 words contains `*319`, so
Step 2 below is unaffected either way.

### R62 restricted to Palaikastro, R63 to Zakros

Cycle 4 let "an initial JA- is dropped" fire anywhere, and flagged that as more
generous than the paper. Every corpus word has a site, so from this cycle the
rule only fires where the paper says it applies.

Over the whole 787-word corpus pool:

| | coverage | total matches |
|---|---|---|
| cycle 4 — fires anywhere | 781 / 787 | 109,292 |
| cycle 5 — only at Palaikastro (R62) and Zakros (R63) | 781 / 787 | 99,624 |

**It removes 9,668 matches, 8.8 %, and costs no coverage at all.** 52 of the 787
pool words are attested at Palaikastro and 97 at Zakros.

On cycle 4's own self-test (111 rows), **2 rows stop being found**:

- **A-MI-DA-O / √y-d-ʿ** — the corpus has it at Phaistos, which is neither site.
  (A-MI-DA-U survives, because it is at Zakros and R63 covers that.)
- **A-SA-SA-RA-ME / √y-š-r** — the corpus attests this spelling only at IO Zb 10,
  Iouktas. The paper cites PK Za 11a–b for it too, but cycle 2 found that the
  corpus writes **SA-SA-RA-ME** there, not A-SA-SA-RA-ME. So on the corpus's own
  evidence this is an Iouktas word, and the Palaikastro rule does not reach it.
  That is a consequence of taking the paper's site restriction seriously, and it
  works against the paper's Palaikastro argument at exactly this word.

A word's sites here are **every** site the corpus attests it at, not just the one
inscription the paper cites. That is the more generous of the two readings.

### N07 (compounds) is kept exactly as cycle 4 built it

Both halves must spell a root.

---

## 3. The two rule sets

Everything below is run twice.

- **full** — every rule in `reports/cycle-03-rules.csv` and
  `reports/cycle-04-rules-added.csv`. 58 switches on.
- **stated only** — only the rules marked "stated". 40 switches on.

The 20 switches "stated only" drops: N02 N04 N05 N06 N07 R12 R13 R14 R15 R16 R24
R32 R43 R51 R53 R54 R55 R56 R59 R60.

The sign table under the two sets:

| signs | full | stated only | |
|---|---|---|---|
| P-series | p b | p b | |
| T-series | t d ṭ ṣ ṯ | t d ṭ ṣ ṯ | |
| D-series | d t ṭ | d t ṭ | |
| K-series | k g q ḫ | k g q | **differs** |
| Q-series | q k g | q | **differs** |
| S-series | š s ṣ ś | š s ṣ ś | |
| Z-series | ḏ ṯ | z | **differs** |
| R-series | r l | r l | |
| M / N / W / J | m / n / w / y | m / n / w / y | |
| AB79 (ZU, *79, TH) | ṯ | ṯ | |
| *301 | n | n | *(replaced in the test)* |
| *314 | ḥ | ḥ | |
| *319 | h | cannot be read | **differs** |
| A E I O U AU | nothing, or ʾ ʿ h ḥ | nothing, or ʾ ʿ h ḥ | |

**A choice the paper does not settle, recorded here.** R05 ("stops are not told
apart as voiced, voiceless or emphatic") is marked *stated*, and its `allows`
column names the P-, T- and K-series explicitly. So under "stated only" those
three keep their sets, and the T-series keeps ṣ and ṯ as well because R11 is
stated. The **Q-series and the Z-series are named by no stated rule** — R14 and
R16 are both marked "used" — so, following the cycle 5 brief, they fall back to
their plain Linear B value: q, and z. A different reading of R05 could have given
the Q-series k and g as well. That would make the stated-only set more generous,
not less.

---

## 4. Step 1 — the words

Of the corpus's **995** distinct hyphenated words, **22** have `*301` as one of
their signs. **20 are kept**, and they occur **32 times** in the corpus.

| word | occurrences | site(s) |
|---|---|---|
| *301-*301 | 2 | Haghia Triada |
| *301-NA | 1 | Khania |
| *301-SI | 1 | Tiryns |
| *301-U-RA | 1 | Haghia Triada |
| *301-WA | 1 | Iouktas |
| A-*301 | 1 | Khania |
| A-*301-KI-TA-A | 1 | Tylissos |
| A-NA-TI-*301-WA-JA | 1 | Iouktas |
| A-RE-NE-SI-DI-*301-PI-KE-PA-JA-TA-RI-SE-TE-RI-MU-A-JA-KU | 1 | Knossos |
| A-TA-I-*301-DE-KA | 1 | Zakros |
| A-TA-I-*301-WA-E | 1 | Palaikastro |
| **A-TA-I-*301-WA-JA** | **11** | Iouktas, Kophinas, Palaikastro, Syme, Troullos |
| DA-DU-*301 | 1 | (none recorded) |
| E-*301 | 1 | Haghia Triada |
| JA-TA-I-*301-U-JA | 1 | Apodoulou |
| NA-TU-*301-NE | 1 | Skoteino Cave |
| SA-*301-RI | 1 | Zakros |
| TA-NA-I-*301-TI | 1 | Psykhro |
| TA-NA-I-*301-U-TI-NU | 1 | Iouktas |
| TE-*301 | 2 | Haghia Triada |

**Left out, and why:**

| left out | why |
|---|---|
| `*301` standing alone — **238 occurrences** | the paper reads it as a word sign; this test cannot check a word sign |
| combined signs written with `+` — `*301+*311` (10), `I+*301` (2), `MI+*301` (2), `DA+*301` (1), `*307+*301[` (1); **16 occurrences** | excluded by the brief. As it happens none of them occurs inside a hyphenated word, so none was in the 22 to begin with |
| `*905-*301` | contains `*905`, which the matcher cannot read |
| `ZU-*301-SE-DE-*21F-*118` | contains `*21F` and `*118`, which the matcher cannot read |

---

## 5. Step 2 — every sound in place of *301

27 candidates: the 26 consonants the matcher uses, plus "no consonant" (the sign
treated as a plain vowel). "na" is candidate **n**. Candidates are ranked by
coverage first, then by total matches; tied candidates share a rank.

### Full rule set

| rank | candidate | coverage | total | median | A-TA-I-*301-WA-JA |
|---|---|---|---|---|---|
| 1 | p | 19/20 | 2435 | 100 | 204 roots, n-w-y no |
| 2 | b | 19/20 | 2376 | 93 | 206 roots, n-w-y no |
| 3 | l | 19/20 | 2203 | 85 | 198 roots, n-w-y no |
| 4 | q | 19/20 | 2122 | 82 | 188 roots, n-w-y no |
| **5** | **n — "na"** | **19/20** | **2120** | **88** | **184 roots, n-w-y yes** |
| 6 | r | 19/20 | 2084 | 84 | 191 roots, n-w-y no |
| 7 | k | 19/20 | 2021 | 78 | 180 roots, n-w-y no |
| 8 | g | 19/20 | 1983 | 80 | 177 roots |
| 8 | m | 19/20 | 1983 | 68 | 57 roots |
| 10 | y | 19/20 | 1961 | 72 | 64 roots |
| 11 | ṯ | 19/20 | 1932 | 78 | 152 roots |
| 11 | š | 19/20 | 1932 | 78 | 152 roots |
| 13 | (no consonant) | 19/20 | 1931 | 74 | 154 roots |
| 14 | d | 19/20 | 1906 | 82 | 161 roots |
| 15 | ṣ | 19/20 | 1840 | 75 | 148 roots |
| 16 | t | 19/20 | 1824 | 72 | 159 roots |
| 17 | ḏ | 19/20 | 1743 | 71 | 158 roots |
| 17 | z | 19/20 | 1743 | 71 | 158 roots |
| 19 | ṭ | 19/20 | 1711 | 68 | 156 roots |
| 20 | ś | 19/20 | 1701 | 60 | 152 roots |
| 21 | h | 19/20 | 1684 | 64 | 144 roots |
| 22 | ḥ | 19/20 | 1644 | 58 | 144 roots |
| 22 | ḫ | 19/20 | 1644 | 58 | 144 roots |
| 24 | ʿ | 19/20 | 1636 | 58 | 144 roots |
| 25 | ʾ | 19/20 | 1627 | 58 | 144 roots |
| 26 | s | 19/20 | 1402 | 38 | 24 roots |
| 27 | w | 18/20 | 1366 | 39 | 22 roots |

**n is 5th of 27, alone at that rank. Four candidates rank above it: p, b, l, q.**

*(Medians are rounded to whole numbers in these tables; `reports/cycle-05-rankings.csv`
has them exactly.)*

And the headline number is not the rank, it is the coverage column:
**26 of the 27 candidates fit 19 of the 20 words.** Only w falls to 18. The one
word nothing ever fits is the 19-sign
A-RE-NE-SI-DI-*301-PI-KE-PA-JA-TA-RI-SE-TE-RI-MU-A-JA-KU, which is far too long
to spell a two-to-five-letter root. So on the "fits every other occurrence of
*301" test, **/na/ is not picked out at all — nearly every sound fits, and by
the same margin.**

### Stated-only rule set

| rank | candidate | coverage | total | median | A-TA-I-*301-WA-JA |
|---|---|---|---|---|---|
| 1 | (no consonant) | 18/20 | 510 | 15 | 23 roots, n-w-y no |
| 2 | r | 16/20 | 278 | 4 | 4 roots |
| 3 | b | 16/20 | 188 | 3 | 1 root |
| 4 | ʿ | 16/20 | 69 | 2 | 2 roots |
| **5** | **n — "na"** | **15/20** | **218** | **4** | **5 roots, n-w-y yes** |
| 6 | p | 15/20 | 210 | 3 | 1 root |
| 7 | ṯ | 15/20 | 146 | 4 | 4 roots |
| 7 | š | 15/20 | 146 | 4 | 4 roots |
| 9 | ḥ | 15/20 | 87 | 2 | 2 roots |
| 9 | ḫ | 15/20 | 87 | 2 | 2 roots |
| 11 | l | 14/20 | 221 | 4 | 4 roots |
| 12 | q | 14/20 | 127 | 3 | 3 roots |
| 13 | k | 14/20 | 118 | 5 | 2 roots |
| 14 | g | 14/20 | 101 | 2 | 1 root |
| 15 | h | 14/20 | 95 | 1 | 1 root |
| 16 | ṣ | 14/20 | 77 | 2 | 3 roots |
| 17 | d | 13/20 | 107 | 2 | 3 roots |
| 18 | t | 13/20 | 88 | 2 | 2 roots |
| 19 | ḏ | 13/20 | 53 | 1 | 1 root |
| 19 | z | 13/20 | 53 | 1 | 1 root |
| 21 | m | 12/20 | 184 | 4 | 0 roots |
| 22 | y | 12/20 | 173 | 3 | 0 roots |
| 23 | ṭ | 12/20 | 58 | 2 | 4 roots |
| 24 | ś | 12/20 | 34 | 1 | 1 root |
| 25 | w | 11/20 | 104 | 2 | 0 roots |
| 26 | s | 11/20 | 73 | 2 | 0 roots |
| 27 | ʾ | 10/20 | 42 | 0 | 2 roots |

**n is again 5th of 27, alone at that rank.** Above it: "no consonant", r, b, ʿ.
The tighter rule set does spread the coverage out — from 10/20 to 18/20 instead
of a flat 19/20 — but it does not move n to the top. **The result that n is not
first holds under both rule sets.**

### Second view — whole sign groups

The same test, giving *301 a whole sign group with all its options, as the
paper's rules would treat any ordinary sign.

| rank | full set | coverage | total | | rank | stated only | coverage | total |
|---|---|---|---|---|---|---|---|---|
| 1 | P-series | 19/20 | 3173 | | 1 | plain vowel | 18/20 | 510 |
| 2 | K-series | 19/20 | 2939 | | 2 | R-series | 16/20 | 501 |
| 3 | Q-series | 19/20 | 2881 | | 3 | T-series | 16/20 | 490 |
| 4 | T-series | 19/20 | 2837 | | 4 | P-series | 16/20 | 398 |
| 5 | R-series | 19/20 | 2703 | | 5 | Z-series | 16/20 | 199 |
| 6 | S-series | 19/20 | 2452 | | 6 | K-series | 15/20 | 433 |
| 7 | D-series | 19/20 | 2225 | | 7 | S-series | 15/20 | 329 |
| 8 | Z-series | 19/20 | 2184 | | **8** | **N-series** | **15/20** | **218** |
| **9** | **N-series** | **19/20** | **2120** | | 9 | Q-series | 14/20 | 346 |
| 10 | M-series | 19/20 | 1983 | | 10 | D-series | 14/20 | 254 |
| 11 | J-series | 19/20 | 1961 | | 11 | M-series | 12/20 | 184 |
| 12 | plain vowel | 19/20 | 1931 | | 12 | J-series | 12/20 | 173 |
| 13 | W-series | 18/20 | 1366 | | 13 | W-series | 11/20 | 104 |

**Read this table with care.** A group with more options matches more words for
no reason except that it has more options: the P-series has two sounds, the
T-series five, the N-series one. The N-series lands 9th of 13 in the full set and
8th of 13 in the stated-only set, but that is mostly a count of options, not a
measure of fit. The single-consonant view above is the fair comparison, because
there every candidate competes on equal terms.

### The paper's own first filter

P.5 describes the search as "searching for three consonant systems containing
waw and yod as their second and third consonants". That filter can be applied
directly. Of the 26 consonants, **15 give a real Hebrew primitive root of the
shape C-w-y**: ʾ, ʿ, ḥ, t, d, ṭ, ṣ, ṯ, k, q, ḫ, š, r, l, n — for instance
ʾ-w-y "to wish for" (H183), d-w-y "to be ill" (H1738), r-w-y "to slake the
thirst" (H7301), l-w-y "to twine, to join" (H3867), q-w-y "to bind together, to
wait for" (H6960).

So the paper's first filter narrows 26 candidates to 15, not to one. What does
the rest of the narrowing is **meaning** — and the paper says so itself, in
footnote 10 on p.5, where √d-w-y is set aside because "none produce a
contextually viable reading at this position". That is a judgement about sense,
not about mechanical fit, and it is precisely the part this cycle's code cannot
test.

---

## 6. Step 3 — the control: the same test on signs whose sounds are known

If the ranking in Step 2 means anything, then running the same test on a sign
whose sound is already known should put the right answer at or near the top.

**Choosing the signs.** Counting how many words of the readable pool contain each
ordinary syllable sign (leaving out plain vowels, AB79/ZU and numbered signs),
*301 appears in 20. The three closest are **JU (20 words)**, **RA₂ (20 words)**
and **WI (19 words)**.

Each was then treated as if its sound were unknown and put through the same 27
candidates. Full rankings for all three, under both rule sets, are in
`reports/cycle-05-rankings.csv`.

### Where the real answer landed

| sign | real value | plain Linear B consonant | full set: best real rank | stated only: best real rank |
|---|---|---|---|---|
| JU | y | y | **1 of 27** (tied with p) | **5 of 27** |
| RA₂ | r or l | r | **10 of 27** (l; r is 16th) | **9 of 27** (r; l is 10th) |
| WI | w | w | **26 of 27** | **19 of 27** |

### JU — full rule set (top of the table)

| rank | candidate | coverage | total |
|---|---|---|---|
| 1 | p | 19/20 | 1982 |
| **1** | **y — the real value** | **19/20** | **1982** |
| 3 | n | 19/20 | 1931 |
| 4 | (no consonant) | 19/20 | 1927 |
| 5 | l | 19/20 | 1914 |
| … | (22 more, down to ʿ at 27) | | |

### RA₂ — full rule set (top of the table)

| rank | candidate | coverage | total |
|---|---|---|---|
| 1 | (no consonant) | 20/20 | 1670 |
| 2 | y | 20/20 | 1614 |
| 3 | n | 20/20 | 1564 |
| 4 | m | 20/20 | 1513 |
| 5 | h | 20/20 | 1302 |
| … | | | |
| **10** | **l — a real value** | **19/20** | **1613** |
| … | | | |
| **16** | **r — the plain Linear B consonant** | **18/20** | **1527** |

### WI — full rule set (the bottom matters here)

| rank | candidate | coverage | total |
|---|---|---|---|
| 1 | p | 19/19 | 2242 |
| 2 | (no consonant) | 19/19 | 2185 |
| 3 | y | 19/19 | 2168 |
| … | | | |
| **26** | **w — the real value** | **19/19** | **1719** |
| 27 | s | 19/19 | 1698 |

Every one of the 27 candidates covers all 19 WI words. The real answer comes
second from last on total matches.

### What the control says

**The method cannot pick out a right answer.** One of the three known signs
comes first, one lands in the middle, and one comes 26th of 27. Under the
stated-only set the spread is 5th, 9th and 19th — better, but still nowhere near
a test that finds the truth.

That is the decisive result of this cycle. Because the same test cannot find the
known value of WI, its verdict on *301 carries no weight in either direction. It
cannot be used to support "only /na/ stood its ground", and it cannot be used to
argue against /na/ either.

---

## 7. What the tests show, and what they do not

**What they show.**

1. On the test the paper describes — a value for *301 that "fits into every other
   occurrence of *301" — **fit does not pick out /na/**. Under the full rule set,
   26 of 27 possible sounds fit 19 of the 20 words, the same 19. Ranking them by
   how many roots they produce puts n **5th of 27**, behind p, b, l and q. Under
   the stated-only rule set n is again 5th of 27. The result is the same under
   both.
2. The paper's own first filter — a root shaped C-w-y — leaves **15 of 26**
   consonants standing, not one.
3. **The test itself cannot be trusted.** Run on three signs whose sounds are
   known, it put the right answer 1st, 10th and 26th of 27. A test that ranks the
   true value of WI 26th of 27 cannot certify anything about *301.

**What they do not show.**

4. **They do not show that /na/ is wrong.** Two things this cycle cannot do are
   exactly the two things the paper leans on. It cannot judge **meaning**, and the
   paper's own footnote 10 shows meaning doing the narrowing work. And it cannot
   check the **logographic** use of *301 — the 238 standalone occurrences the
   paper reads as *nawā* — because a word sign has no consonant skeleton to match.
   That is most of the evidence the paper cites for *301, and it is untouched here.
5. They do not say anything about the language as a whole. One sign, one kind of
   test.

**The fair summary.** The claim on p.5 is presented as a narrowing: strict
conditions leave only /na/ standing. The mechanical half of those conditions does
not narrow much — 15 candidates survive the root-shape filter, and 26 survive the
corpus-fit filter. The narrowing is being done by the author's judgement of
meaning. That may well be sound; it is simply not the kind of claim the phrase
"only /na/ stood its ground" suggests, and it is not something this code can check.

---

## 8. Choices this cycle had to make that the paper does not settle

1. **The Q-series and Z-series under the stated-only set** fall back to their
   plain Linear B value, because no stated rule names them (§3). A different
   reading of R05 would give the Q-series k and g too.
2. **A word's sites** are every site the corpus attests it at, not just the one
   inscription the paper cites. This is the more generous reading, and it still
   costs two rows of cycle 4's self-test (§2).
3. **RA₂ is put in the R-series**, keeping only the r of Linear B /rya/, as
   cycle 4 decided. Its "real value" in the control is therefore r or l.
4. **Ranking is by coverage first, then total matches.** Ranking by total matches
   alone would put n 5th in the full set as well, so this choice does not change
   the headline.
5. **"No consonant"** is treated as the sign behaving like a plain vowel — it can
   still stand for a throat consonant under R07, exactly as A, E, I, O and U do.

## 9. Open items

- The 238 standalone occurrences of `*301`, which the paper reads as the word
  *nawā*. Testing a word sign needs a different method from this one.
- Whether a test that scored candidates on **meaning** as well as fit could be
  built at all, and what it would rest on.
- Zenodo: still no file list; the outage is on Zenodo's side (cycle 4).
- The made-up-word control from cycle 4's open items is still not done. This
  cycle's Step 3 is a control of a different kind — known signs rather than
  invented words.

## 10. Reproducing this cycle

```
bash scripts/run_all.sh          # scripts 01-27, in order
```

| script | what it does |
|---|---|
| `scripts/25_cycle5_setup.py` | the word pool, the two rule sets, the sign counts |
| `scripts/26_cycle5_rankings.py` | Steps 1–3; writes `reports/cycle-05-rankings.csv` |
| `scripts/27_cycle5_decisions.py` | what the two cycle 4 decisions change |

`scripts/21_matcher.py` was refactored so a sign can be handed a different sound
and a word can carry its sites. Cycle 4's own outputs were re-run afterwards and
are byte-identical, so nothing older changed.

## Credit

Tom di Mino, *Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula*
(September 2026), DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321),
CC BY 4.0. Quotations and readings are used under that licence.

Linear A corpus: [lineara.xyz](https://lineara.xyz) (Hogan 2019–).

Strong's Hebrew dictionary: James Strong (1894), public domain; JSON edition by
[Open Scriptures](https://github.com/openscriptures/strongs), CC BY-SA. The
derived word list is not committed.
