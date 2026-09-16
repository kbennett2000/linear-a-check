# Cycle 4 — the matcher, and whether it finds the paper's own readings

**Date run:** 16 September 2026
**Scope:** build the matcher — code that takes a Linear A word and lists every
Hebrew root it could match under the paper's own rules — and check that it finds
the readings the paper itself prints. **No conclusions about the language are
drawn in this cycle**, and none should be read into it. The test with made-up
words belongs to a later cycle.

Files written:

| file | what it is |
|---|---|
| `scripts/21_matcher.py` | the matcher, and the six Step 1 tests |
| `scripts/22_selftest.py` | Step 2, and `reports/cycle-04-selftest.csv` |
| `scripts/23_rules_added.py` | `reports/cycle-04-rules-added.csv`, with its quotes checked |
| `scripts/24_freedom.py` | Step 3, and `reports/cycle-04-formula-matches.csv` |

**Terms used below, defined on first use.** A **root** is the set of consonants
a Semitic word family is built on; the paper writes them after a √ sign. A
**skeleton** is a Hebrew dictionary word with its vowel marks stripped out,
which is how cycle 3 stored Strong's. A **primitive root** is Strong's own label
for an entry that is a bare verb root rather than a word built from one. A
**throat consonant** — linguists say *laryngeal* or *pharyngeal* — is one of
ʾ ʿ h ḥ. A **stop** is a consonant made by closing the mouth completely: p b t d
ṭ k g q. A **geminate** consonant is a doubled one. A **compound** is a word made
of two words joined together. Terms defined in cycles 1–3 are not redefined.

---

## 1. Step 0 — correcting the Zenodo note

**Done. Both links were opened and read before the notes were written.**

Cycle 1 §1.3 said the 504 errors were "our network reaching Zenodo, not
something about this particular record", and cycle 2 §2 repeated it. That was a
guess and it was wrong. The evidence that it is Zenodo's own problem:

- The project owner's own web browser, on a different network, got the same 504
  from Zenodo on 16 September 2026.
- Plazi run an automatic uptime monitor. It logged
  `https://zenodo.org/communities/biosyslit/` returning **HTTP 504** after about
  30 seconds on **14 September 2026** —
  [plazi/monitoring#4101](https://github.com/plazi/monitoring/issues/4101),
  "🛑 Biosyslit is down", response time **30,316 ms** — and again on
  **16 September 2026** —
  [plazi/monitoring#4114](https://github.com/plazi/monitoring/issues/4114),
  response time **30,303 ms**.

A dated correction note has been added to the top of
[reports/cycle-01.md](cycle-01.md) and [reports/cycle-02.md](cycle-02.md).
Nothing else in either report was changed. The practical result is unchanged:
the record's file list is still **unknown**. Only the reason has changed, from
"this machine cannot reach Zenodo" to "Zenodo was down".

---

## 2. Step 1 — the matcher

### What each sign may stand for

Only rules from `reports/cycle-03-rules.csv` are used, going by the `allows`
column. `scripts/21_matcher.py` prints this table when run.

| signs | may stand for | rule |
|---|---|---|
| A E I O U AU | nothing, or one of ʾ ʿ h ḥ | R02, R07, R30 |
| PA PE PI PO PU PA₃ PU₂ | p b | R05, R15 |
| TA TE TI TO TU TA₂ | t d ṭ ṣ ṯ | R05, R11 |
| DA DE DI DO DU | d t ṭ | R05, R12 |
| KA KE KI KO KU | k g q ḫ | R05, R13 |
| QA QE QI QA₂ | q k g | R05, R14 |
| SA SE SI SO SU | š s ṣ ś | R06 |
| ZA ZE ZO | ḏ ṯ | R16 |
| RA RE RI RO RU RA₂ | r l | R09 |
| MA ME MI MO MU | m | R01 |
| NA NE NI NO NU | n | R01 |
| WA WE WI WO | w | R01 |
| JA JE JO JU | y | R01 |
| ZU, *79, TH (all AB79) | ṯ | R27 |
| *301 | n | R25 |
| *314 | ḥ | R29 |

Anything else — other starred sign numbers, word signs, numbers, fractions —
has no sound value in the rules table. A word containing one is skipped and
counted.

### Signs settled one at a time

The paper gives no general rule for the signs whose transcription carries a
small number, or for the two-consonant signs. Each was settled on its own and
written down in the script:

| sign | what was done, and why |
|---|---|
| **PA₃** | Put in the P-series (p, b). The paper reads KU-PA₃-NU as Kubaba + -ānu and KU-PA₃-PA₃ as Kubaba itself (p.38), so it uses PA₃ for /ba/. |
| **PU₂** | Put in the P-series. The paper writes "the nearest analog to DU-PU₂-RE, or DU-BU-RE" (p.19), so it uses PU₂ for /bu/. |
| **ZU** | The corpus transcribes AB79 as ZU, so ZU is read ṯ (R27) and *not* as a member of the Z-series. The paper writes the same sign *79 or TH. |
| **AU** | AB85, which R30 calls a two-vowel sign. Treated as a plain vowel sign. |
| **RA₂, TA₂** | Linear B ra₂ is /rya/ and ta₂ is /tya/. Only the first consonant is kept, so they sit in the R- and T-series. The y is dropped rather than invented as a second consonant, because no rule lets one sign give two *different* consonants. Neither occurs in any word tested. |
| **NWA, TWE** | Two-consonant signs. Same treatment: only the n and the t are kept. Neither occurs in any word tested. |
| **QA₂** | Q-series. Does not occur in any word tested. |

### Word pieces

The matcher may take prefixes off the front and suffixes off the end, using the
pieces in R37–R61, plus the indicative U that R61 allows inside a verb.

**How long a chain is allowed.** The brief asked for the longest chain the paper
itself uses. Reading the readings table:

- **Three prefixes**, in A-TA-I-*301-WA-JA. The §4.1 table (p.4) lists A as the
  1cs prefix, TA as the tG stem marker and I as the stem vowel — three separate
  pieces before the root begins.
- **Two suffixes**, in TA-NA-RA-TE-U-TI-NU: -TI then -NU (§6.1, pp.12–13).

So the matcher allows up to 3 prefixes and up to 2 suffixes. Nothing longer.

### How a match is made

After the pieces are taken off, what is left must spell the whole root.

- Each consonant sign gives exactly one root consonant from its list, in order,
  or — because length is never written (R08) — the same consonant twice in a row.
- Each plain vowel sign gives nothing, or one throat consonant.
- Two identical signs in a row may give one consonant (R17), with R18 naming
  SA-SA = š and R19 naming TE-TE and TI-TI = ṯ.
- A root consonant may go unwritten only where the rules allow it: throat
  consonants (R07, R21), an /s/ before a stop (R22), an /r/ before a consonant
  (R24).
- On the Hebrew side, the four sound matches recorded in cycle 3 apply while
  comparing: ṯ counts as Hebrew š, ḏ as z, ḫ as ḥ, ġ as ʿ. Every match records
  which of them it needed.

The Hebrew side is the **1,390 non-Aramaic entries Strong's marks "primitive
root"**, plus their 188 final-h-as-y forms. A second, separate result compares
against **all 7,999 non-Aramaic entries**; the two are kept apart throughout.

### Two choices the paper does not settle, recorded here

1. **R17 is applied generally, not narrowly.** At first the matcher restricted a
   doubled sign to the value R18 or R19 names — SA-SA to š, TE-TE and TI-TI to
   ṯ. That had to be widened: the paper's own Appendix B entry for TI-TI-KU
   reads TI-TI as /tt/, an ordinary t ("Nun → geminate /tt/", p.40). R17 is
   general in the rules table, so a doubled sign may give one consonant from
   that sign's own series; R18 and R19 are cited when the value is the one they
   name. This widening is the paper's, not an invention, but it does make the
   matcher looser and it is recorded here because it was a judgement call.
2. **R62 is applied without checking the site.** R62 says an initial JA- is
   dropped at Palaikastro, and R63 adds that the same may hold at Zakros. The
   matcher lets a root-initial y go unwritten anywhere, because it has no
   reliable site for every word. This is more generous than the paper, which
   names two sites. Switching R62 off costs 5 rows of the self-test (§4 below).

### Step 1 tests — all six pass

| test | result |
|---|---|
| a word containing `*118` returns no matches and is counted as skipped | **PASS** |
| KA-NA-SI matches k-n-s (H3664) with nothing removed | **PASS** |
| SI-RU-TE matches š-r-t (H8334) | **PASS** |
| U-NA-KA-NA-SI matches k-n-s with U-NA- removed (R42) | **PASS** |
| DI-KI matches d-q-q (H1854), and the match disappears without R08 | **PASS** |
| MA-NA-SI does **not** match k-n-s | **PASS** |

---

## 3. Step 2 — the self-test

Every row of `reports/cycle-03-readings.csv` whose `root_kind` is "stated",
using the word as the paper prints it, with *79 and TH read as AB79. A row that
gives two roots produces one test per root, so the unit is a
(word, root, place) triple: **111 of them, over 71 distinct words**. The five
non-Semitic consonant strings cycle 3 flagged are all `root_kind`
"from comparison word", so they never entered the self-test; the script excludes
them explicitly as well.

Full results: [reports/cycle-04-selftest.csv](cycle-04-selftest.csv).

### Result

| | rows | |
|---|---|---|
| **found** | **86** | |
| not found | 3 | each explained below |
| root not in the Hebrew list | 18 | cannot be found; 12 distinct roots |
| skipped — a sign with no sound value | 4 | |
| | | |
| **found, of the 89 that could be tested** | **86** | **96.6 %** |

Against all 7,999 non-Aramaic entries instead of just the primitive roots:
93 found, 2 not found, 12 not in the list, 4 skipped — **97.9 %** of 95.

### The seven formula words: all seven find their root

| word | root | Strong's | pieces removed | rules used |
|---|---|---|---|---|
| A-TA-I-*301-WA-JA | n-w-y | H5115 | A- (R37) + TA- (R39) | R01 R02 R25 R37 R39 |
| JA-DI-KI-TU | d-q-q | H1854 | -TU (N01) + JA- (R38) | N01 R01 R05 R08 R12 R13 R38 |
| JA-SA-SA-RA-ME | y-š-r | H3474 | -ME (R47) | R01 R06 R09 R17 R18 R47 |
| U-NA-KA-NA-SI | k-n-s | H3664 | U-NA- (R42) | R01 R05 R06 R13 R42 |
| I-PI-NA-MA | p-n-y | H6437 | -MA (R47) | R01 R02 R05 R07 R15 R47 |
| SI-RU-TE | š-r-t | H8334 | (nothing) | R01 R05 R06 R09 R11 |
| TA-NA-RA-TE-U-TI-NU | r-ṣ-y | H7521 | -NU (R50) + -TI (R49) + TA-NA- (R40) | R01 R05 R07 R09 R11 R40 R49 R50 |

### The two gaps the brief expected

**The first one did not turn out to be a gap.** The brief expected trouble with
I-PI-NA-MA and TA-NA-RA-TE-U-TI-NU, whose roots end in y that no sign writes.
Both were found without any new rule, because Hebrew spells those two roots with
a **final h**, not a final y: H6437 is p-n-h and H7521 is r-ṣ-h. An h is a
throat consonant, and R07 already lets a throat consonant go unwritten. So the
match runs through the Hebrew spelling, not through a rule about final y.
Cycle 3's final-h-as-y forms were not needed for these two.

Searching the paper for a statement about a root's last y or w going unwritten
turned up nothing: the words "hollow", "weak root" and "third root consonant"
do not occur anywhere in it, and "Root C₃" appears only four times, always where
the consonant *is* written.

**The second one was a real gap, and the rule is stated.** JA-DI-KI-TU could not
be matched because -TU was not among the word pieces. The paper's §4.2 table
(p.6) reads "TU AB69 B69 𐀶 /tu/ Feminine nominal ending". Added as N01.

### The three rows that stay unmatched

None of the three is a gap in the rules. Each is something internal to the
paper, and each is recorded in the `reason` column of the CSV.

1. **A-TA-I-*301-WA-JA → √n-b-ʾ.** Not reproducible, and correctly so. Cycle 3
   already recorded that the paper prints √n-b-ʾ in this Appendix B entry as the
   root of its *Hebrew comparison word* **hitnabbēʾ**, not of the Linear A word,
   whose root is √n-w-y. That one is found.
2. **KU-MI-NA-QE → √q-b-b.** Not reproducible from the word as printed. The
   paper assigns √q-b-b to **QE alone**, which it says sits on side b of the
   roundel before the CAP logogram — so it is not part of this sign-group at
   all. The word's other root, √k-m-n, is not in the Hebrew list.
3. **I-NA-JA-PA-QA → √ʾ-n-n.** Not reproducible. The entry reads the word as
   *ʾinna* (√ʾ-n-n) plus *pāqaḥ* (√p-q-ḥ) but never says what the **JA** in the
   middle writes, so the ʾ-n-n half cannot be closed off. The √p-q-ḥ half is
   found.

### The four skipped rows

`*307` (the logogram for *dubur*), `*312-TA` (the logogram KITNU), and the two
words containing `*319`. The first two are word signs, so they cannot spell a
root consonant by consonant.

`*319` is a different case, and it cost something. The brief's design says any
other starred sign number cannot be matched. But R32 in the cycle 3 table does
give *319 a value — /hū/, put forward conditionally by the paper. Switching R32
on was run as a clearly separate check: **both *319 rows go from "skipped" to
"found"**. So following the brief here costs two rows. The rule is in the table;
the brief's sign list leaves it out; this note records the difference rather
than quietly choosing.

### The 18 rows whose root is not in the Hebrew list

Twelve distinct roots: d-m-t, d-r-r, e-š-r, g-p-n, k-m-n, k-t-n, m-k-s, t-r-s,
t-ʾ-n, w-t-ʾ, y-t-n, ʾ-r-ṣ. Cycle 3 already explained most of them: the check
looks only at entries Strong's labels "primitive root", and several of these are
noun roots (ʾ-r-ṣ "earth", k-t-n "linen", k-m-n "cummin") that Strong's lists as
nouns. They are not matcher failures and are counted apart from the found /
not-found tally.

---

## 4. The rules added, and what they are doing

Seven rules were added, each because a self-test row could not otherwise be
reproduced, and each tied to a passage in the paper. Two are things the paper
**states**; five are things it **does without saying so**. All seven quotes were
checked against the extracted paper text and all seven match.

Full table: [reports/cycle-04-rules-added.csv](cycle-04-rules-added.csv).

| id | rule | stated or used | where |
|---|---|---|---|
| N01 | -TU at the end of a word is the feminine nominal ending, so it can be taken off | stated | §4.2 table, p.6 |
| N02 | -TA at the end of a word can write a feminine -at / -āt | used | §8 p.16; Appendix B p.38 |
| N03 | RU can be taken out as the separate particle *lū* | stated | §5.1, p.9 |
| N04 | the middle consonant of a three-letter root can go unwritten when it is w | used | Appendix B pp.38, 39, 40 |
| N05 | a root-initial n can go unwritten when it runs into the next consonant, written as a doubled sign | used | Appendix B, p.40 |
| N06 | a U sign can write the root consonant w | used | Appendix B, p.39 |
| N07 | a word can be a compound of two Semitic words, each with its own root | used | Appendix B pp.37, 38 |

Two further changes were **not** new rules:

- **R22 was widened, because my first version of it was too narrow.** R22 says a
  syllable-final /s/ is unwritten before a stop. I had only allowed the stop to
  be the next letter *of the root*. In U-NA-RU-KA-NA-TI, read *hunna lu
  kanasiti*, the stop is the **t of the ending that was taken off**. The
  matcher now looks there too. That is R22 as written, not an addition.
- **R62 was implemented** (a root-initial y may go unwritten). It was already in
  the cycle 3 table; cycle 4 is the first time anything used it.

### N07 is by far the loosest thing here, and it had to be tightened

N07 lets a word be a compound. My first version only required **one** half to
spell a root — which in practice let any leftover signs be ignored. That was
caught by the *319 check, where a word matched simply by ignoring its tail. It
was tightened so that **both halves must spell a root**, which is what a
compound is and what all of the paper's compounds look like: in A-MI-DA-O,
*ʿAmmī* is √ʿ-m-m and *daʿ* is √y-d-ʿ.

Even tightened, N07 is responsible for about three quarters of everything the
matcher finds (§5). It is the single biggest source of freedom in the whole
system, and it rests on the paper *doing* this in four Appendix B entries rather
than stating it.

### Leave-one-out: which added rules are actually holding something up

| switched off | rows lost | which |
|---|---|---|
| N07 | 11 | A-MI-DA-O ×2, A-MI-DA-U ×2, A-PA-RA-NE, I-NA-JA-PA-QA, I-NA-JA-RE-TA, I-PI-NA-MI-NA, JA-SA-SA-RA-MA-NA, NA-TU-*301-NE, PA-RA-NE |
| R62 | 5 | A-MI-DA-O, A-MI-DA-U, A-SA-SA-RA, A-SA-SA-RA-ME, SA-SA-RA-ME |
| N04 | 4 | I-ZU-RI-NI-TA, RU-MA-TA, RU-MA-TA-SE, ZU-RI-NI-MA |
| N05 | 2 | I-TI-TI-KU-NI, TI-TI-KU |
| N02 | 1 | I-NA-JA-RE-TA |
| **N01** | **0** | — |
| **N03** | **0** | — |
| **N06** | **0** | — |

**Three of the seven added rules turn out not to be load-bearing.** Each was
added for a row that could not be reached at the time, but by the end another
rule covers that row:

- Without **N01**, JA-DI-KI-TU still reaches d-q-q — by treating DI-KI as the
  first half of a compound (N07) instead of taking -TU off.
- Without **N03**, U-NA-RU-KA-NA-SI still reaches k-n-s, again through N07.
- Without **N06**, JA-TA-I-*301-U-JA still reaches n-w-y, because N04 lets the
  middle w go unwritten instead of U writing it.

All three are kept, because in each case they give **the paper's own analysis**
of the word rather than an accidental route to the same answer. But they are not
what makes the self-test pass, and saying otherwise would overstate the result.

---

## 5. Step 3 — how much choice the rules give

For each of the 67 matchable self-test words, how many different Hebrew
primitive roots does the matcher find?

| | roots matched |
|---|---|
| smallest | **32** (I-NA-JA-PA-QA) |
| middle (median) | **188** |
| largest | **322** (I-TI-TI-KU-NI) |
| average | 183.9 |
| total across the 67 words | 12,322 |

Fewest: I-NA-JA-PA-QA (32), KU-MI-NA-QE (35), A-JA (46), A-NA-NE (50),
NA-TU-*301-NE (52). Most: I-TI-TI-KU-NI (322), JA-DI-KI-TE-TE (299),
U-NA-RU-KA-NA-TI (296), A-DI-KI-TE-TE (294), KI-TA-NA-SI-JA-SE (294).

**This is the number that matters most in this cycle.** A typical word in the
paper's own list can be read as any of roughly **190 different Hebrew verb
roots** under the paper's own rules. Finding the paper's root among them is
therefore not, on its own, evidence that the reading is right. What that means
for the argument is a question for a later cycle, with made-up words as a
control. This cycle only measures the freedom.

### Every match for the seven formula words

Written out in full, one row per match, in
[reports/cycle-04-formula-matches.csv](cycle-04-formula-matches.csv) — 1,506
rows, with the Strong's number, gloss, pieces removed, rules used and sound
matches for each. Counts:

| word | the paper's root | roots the matcher finds |
|---|---|---|
| A-TA-I-*301-WA-JA | n-w-y | 184 |
| JA-DI-KI-TU | d-q-q | 242 |
| JA-SA-SA-RA-ME | y-š-r | 234 |
| U-NA-KA-NA-SI | k-n-s | 198 |
| I-PI-NA-MA | p-n-y | 147 |
| SI-RU-TE | š-r-t | 230 |
| TA-NA-RA-TE-U-TI-NU | r-ṣ-y | 271 |

### Turning off one group of rules at a time

| group switched off | min | median | max | total | change |
|---|---|---|---|---|---|
| *(nothing — the full matcher)* | 32 | 188 | 322 | 12,322 | — |
| unwritten throat sounds (R07, R21) | 0 | 29 | 106 | 2,377 | **−80.7 %** |
| prefixes and suffixes (R37–R61, and N01–N03) | 0 | 132 | 269 | 7,904 | **−35.9 %** |
| the different ways of writing ṯ (R11, R16, R19, R27) | 0 | 163 | 274 | 10,895 | −11.6 % |
| one sign giving two consonants (R08) | 31 | 175 | 304 | 11,324 | −8.1 % |
| two signs giving one consonant (R17–R19) | 32 | 183 | 300 | 12,017 | −2.5 % |

And, for context, the rules cycle 4 itself added:

| switched off | min | median | max | total | change |
|---|---|---|---|---|---|
| N07 alone (compounds) | 0 | 46 | 203 | 3,176 | **−74.2 %** |
| N04 alone (unwritten middle w) | 28 | 156 | 262 | 10,182 | −17.4 % |
| R62 alone (unwritten initial y) | 31 | 168 | 290 | 11,035 | −10.4 % |
| N06 alone (U writing w) | 32 | 188 | 322 | 12,322 | 0.0 % |
| all seven added rules N01–N07 | 0 | 19 | 132 | 2,192 | −82.2 % |
| N01–N07 and R62 together | 0 | 18 | 114 | 1,973 | −84.0 % |

**What this says.** Two things dominate. **Unwritten throat sounds** (R07, R21)
account for four fifths of all matches: because a plain vowel sign may stand for
ʾ ʿ h or ḥ *and* a throat consonant may be left out of the spelling altogether,
any of the four throat consonants can be slotted into a root almost anywhere.
**Compounds** (N07) account for about three quarters. The two overlap, which is
why the figures do not add to 100 %.

By contrast, the three rules most often pointed at as the loose ones — doubling
a sign (R08), collapsing two signs into one (R17–R19), and the several ways of
writing ṯ — together account for only about a fifth. They are not where the
freedom mostly comes from.

Note that switching off the prefixes and suffixes also switches off N01–N03,
which are the word pieces cycle 4 added; they cannot be separated.

---

## 6. Things worth noting

1. **The matcher reproduces the paper on its own terms.** 86 of the 89 testable
   rows, and all seven formula words. The three that do not come out are
   explained by the paper's own text, not by missing rules. Taken on its own
   this says the rules cycle 3 wrote down are a fair record of what the paper
   does.

2. **But a typical word matches about 190 roots.** So reproducing the paper's
   own readings is a check that the rules were recorded correctly, not evidence
   that the readings are right. Both of these are true at once and neither
   cancels the other.

3. **The single loosest rule is one the paper never states.** N07, compounds,
   drives roughly three quarters of the matches and rests on four Appendix B
   entries doing it. The next loosest, unwritten throat sounds, *is* stated
   (p.19) and drives about four fifths.

4. **Three of the seven added rules turn out to be redundant** once the others
   are in (§4). They are kept because they carry the paper's own analysis, but
   they are not doing the work.

5. **Following the brief's sign list costs two rows.** R32 gives *319 a
   conditional value that the brief's "any other starred sign number" excludes.
   Switching it on finds both rows.

## 7. Open items

Carried forward, not acted on:

- Zenodo: still no file list. The reason is now known (outage), so retrying
  later is worth doing.
- Whether *319 should be given its conditional value in the next cycle.
- Whether R62 should be restricted to Palaikastro and Zakros, as the paper has
  it, rather than applied everywhere. That would cost 5 self-test rows.
- Whether N07 should require the two halves of a compound to be *different*
  roots, or to meet any other condition. As it stands both halves must spell a
  root, and nothing more.
- The control test with made-up words, which is what will show whether matching
  190 roots per word makes the paper's hits unremarkable or not.

## 8. Reproducing this cycle

```
bash scripts/run_all.sh          # scripts 01-24, in order
```

Cycle 4 is scripts 21 to 24:

| script | what it does |
|---|---|
| `scripts/21_matcher.py` | the matcher; prints the sign table and runs the six Step 1 tests |
| `scripts/22_selftest.py` | Step 2; writes `reports/cycle-04-selftest.csv`; runs the leave-one-out and the *319 check |
| `scripts/23_rules_added.py` | writes `reports/cycle-04-rules-added.csv` and checks every quote against the paper |
| `scripts/24_freedom.py` | Step 3; writes `reports/cycle-04-formula-matches.csv` |

## Credit

Tom di Mino, *Ya Diktu: Grammar of the Minoan Peak Sanctuary Libation Formula*
(September 2026), DOI [10.5281/zenodo.22730321](https://doi.org/10.5281/zenodo.22730321),
CC BY 4.0. Quotations and readings are used under that licence.

Linear A corpus: [lineara.xyz](https://lineara.xyz) (Hogan 2019–).

Strong's Hebrew dictionary: James Strong (1894), public domain; JSON edition by
[Open Scriptures](https://github.com/openscriptures/strongs), CC BY-SA. The
derived word list is not committed.
