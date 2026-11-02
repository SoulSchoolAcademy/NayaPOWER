# AUTO-MATCH ELITE HARDENING — V2 (2026-10-24)

**Lane:** Resolve (builder) · **Base:** engine as landed on main at
`05f209aed3829edeb44f27dd1cf88fa0fda16` (PR #3041, VERIFY 9.0) ·
**Branch:** `resolve/auto-match-elite-v2` · **Review:** parent seat
(different-seat scorecard still owed before any landing).

**Engine version:** `tools/welcome-engine/smart_match.py` is now **v1.5**.
The published contract is unchanged: weights topics .40 / goals .25 /
offers_needs .20 / wants .15, surface rule ≥2 channels, every existing
`score()` key untouched. Everything below either extends the contract or
fixes a proven defect behind a regression gate.

**Regression gates (run after every change):** the 23 landed tests stay
green · the golden-set printout stays **byte-identical** to the pristine
engine · the first-population (FP-12) table changes only where a fix
predicts it. Both extra fixes in §11 passed all three gates.

**Full suite at this head: 69 passed** under pytest
(9 smart-match + 14 welcome-engine + 12 golden + 15 hardening + 19 holdout).

---

## 1. STOPWORD FIX — DONE

`family_score`'s word tier had no stopwords: `"the"` (length 3 > 2) leaked
as a shared goal — observed live in FP-12 reasons ("shared goals: the").

- ONE unified `STOPWORDS` set (79 words: standard English glue + the v1.4
  cross-tier list; `CROSS_STOPWORDS` kept as an alias) now serves the
  family word tier, the cross-tier signature, and phrase-content checks.
  Filtering applies to the **raw word, pre-stem**, in every tier.
- A declared phrase made only of glue ("the and of") no longer counts as a
  phrase match (`_content_phrases` — a phrase needs ≥1 content word).
- **Evidence (FP-12, before → after):** the phantom goals signal between
  Power and Resolve ("connect **the** parts" × "clear **the** path") is
  gone — that pair drops 16 → 14 and now surfaces on topics+wants only.
  Pairs scoring 0 rise 33 → 36 (stopword-only phantom signals removed).
  All 15 true pairs still surface; top-2 unchanged (62, 57).
- **Tests:** stopwords never appear as reason tokens; a stopword-only
  overlap scores 0; one set used everywhere (test_hardening).

## 2. GOLDEN SET INTO PYTEST — DONE

`test_golden_set.py` wraps `golden_set.py`'s 12 cases (9 pair expectations
+ 3 top-1 rankings) as pytest tests, reading the golden data itself — CI
now pins the calibration set, not just two test scripts.

## 3. OUTPUT CONTRACT — DONE (extend-only)

`score()` output gains two keys; no key renamed or removed:

- `signal_coverage_percent` — weighted share of the 4 channels carrying
  any signal (topics-only match = 40; full match = 100).
- `calibrated: true` — the weights are the evidence-checked published
  weights (calibration re-run at this head: **12 right / 0 wrong, mean
  top-1 margin 36.7** — identical verdict to the pristine engine).

Tests pin the old contract: same keys, Power↔NayaPOWER still **57**,
surface flags unchanged.

## 4. SELF-MATCH + ROBUSTNESS — DONE

- `rank_matches()` excludes the entity itself — by `self_name`, by a
  `name`/`_name` key on the vector, and by object identity.
  `welcome_engine.activate()` passes `self_name=alias`, so a citizen
  never matches themselves.
- Malformed-vector battery (test_hardening, all graceful, never a crash):
  `None` fields · bare numbers as fields · non-string entries · a bare
  string treated as ONE term, not characters · empty everything ·
  duplicate candidates (both rank) · unicode/emoji text · repeated terms.

## 5. POPULATION-FREQUENCY WEIGHTING (IDF) — DONE as a mode, default OFF

`compute_idf(population, threshold=0.5, factor=0.25)`: tokens present in
>50% of the population are down-weighted ×0.25 (never zeroed — a
ubiquitous token can still be a pair's only real signal). `score(...,
idf=...)` and `rank_matches(..., idf=...)` accept it; **default OFF** —
the published contract is unchanged.

**Evidence:**

- On FP-12 the shipped >50% rule is a **no-op** (`compute_idf` → `{}`):
  "builder"/"builders" sit at exactly 6/12 = 50%, not above it.
- Sensitivity at ≥50% (down-weighted: `builder`, `builders`): **all 15
  true pairs survive**; builder-inflated pairs deflate most
  (Power↔Team Nitro 14→6, NayaPOWER↔Team Nitro 12→6, Nitro↔NayaPOWER
  15→8, Power↔Nitro 18→10, Team Nitro↔Smart Factory 7→4);
  builder-independent pairs are untouched (27→27, 25→25, 14→14, 6→6,
  4→4); the top-2 stay the top-2 (62→54, 57→53).
- On the synthetic bench population (n=200), IDF changes percents, not
  surface decisions (precision/recall identical OFF vs ON) — because
  surfacing is a ≥2-channel rule and ×0.25 ≠ 0. Labeled honestly: that
  generator is too promiscuous to discriminate (see §6).

**Recommendation: ADOPT as an available mode, default OFF.** The mechanism
demonstrably discriminates exactly where the inflation is, and harms
nothing. Whether production flips the default (or the threshold to ≥50%)
is a wiring-step calibration decision to make with real citizen data —
the golden set + identity tests are its gate.

## 6. SCALE BENCHMARK — DONE, with the honest limits named

Scripts: `bench_smart_match.py`, `bench2_smart_match.py`,
`bench3_disjoint.py` (seeded, deterministic).

| measure | result |
|---|---|
| per-score cost, v1.5 | 0.260–0.300 ms (v1.4 baseline 0.070 ms — the input sanitizers cost ~4×; still sub-ms) |
| n=100, naive full pairwise | 2.97 s |
| n=1,000, naive full pairwise | 259.9 s |
| n=10,000, naive full pairwise | ~433 min (extrapolated from measured per-score cost) |
| **1 s budget — full pairwise** | **crosses at ~62 entities** (n·(n−1) scores) |
| **1 s budget — one citizen's ranking** (the actual product operation) | crosses at ~3,800 candidates, naive |
| inverted index, n=1,000, templated population | 259.6 s — **1.0×** (see below) |
| **identity proof, n=1,000** | **1000/1000 rankings identical, 0 mismatches** |
| inverted index, n=10,000 | candidate set for citizen-00000 = **10,000 of 10,000**; 2.836 s/entity (25-entity sample) → ~473 min extrapolated |
| disjoint-vocabulary scenario, n=300 | naive 12.7 s → indexed 1.53 s = **8.3×**; mean candidate set **37 of 299**; identity 300/300 |

**Why the pre-filter degenerates on the templated populations:** the
index is built over the full signature (phrases + stemmed words +
concepts), and templated text carries *universal stems* — every entity
offers "{theme} **coaching**", wants "{theme} **people**", goals begin
"**grow** / **master** / **share**" — so every signature intersects every
other. A sound pre-filter cannot drop those tokens (a pair whose only
shared token is a universal stem still scores >0). Where tokens are
selective — the disjoint-vocabulary scenario, and real free-text citizen
declarations — the same index cuts candidates to ~12% and runs 8.3×
faster, with identical output.

**Production implication (wiring-lane decision, not silently taken
here):** candidate generation should pair this index with the §5
ubiquity table (require ≥1 shared sub-ubiquity token, or ≥2 shared
tokens overall). Any such rule must pass the identity test on a real
population snapshot before it ships — the test is in this branch.

## 7. SQL ↔ PYTHON EQUIVALENCE — STATIC AUDIT + SQL REWRITE

**Runtime limit, stated plainly:** this environment has no Postgres and
no jsonb-capable SQLite, so an execution diff was **not possible**. What
follows is a line-by-line static audit; plain divergences are fixed in
`tools/smart-match/smart_match_v1_4.sql` (file change only — **not
deployed**; deployment rides the production gate).

**Matched (verified in both):** weights · two-tier family formula
(phrase tier, then word tier) · concept-silence rule · surface ≥2 rule ·
wants-field concatenation · ies/s/ss stemming guards.

**Fixed in the SQL rewrite** (now 10,023 bytes, 11 functions, generated
from the Python source's own tables where they must agree):

- stopwords: `sm_stopwords()` generated from Python's exact `STOPWORDS`
  set — the SQL previously had its own drifting list;
- `sm_stem` rewritten plural-first, matching the §11 stemmer fix;
- `sm_words` filters on the raw word (length > 2, not a stopword),
  split on commas/whitespace like Python;
- new `sm_sig_words` (length > 3 + raw-word stopword filter) — the old
  SQL let every length-3 word into cross signatures;
- new `sm_terms_content` — glue-only phrases carry no signal (§1);
- `sm_coeff` deduplicates inputs (concatenated signature arrays could
  double-count and push a coefficient above 1); `sm_cross` uses
  deduplicated distinct unions;
- output parity: `parts` (2 dp) and `signals` as channel **names in
  Python's order** (was: a count), plus `signal_coverage_percent` and
  `calibrated: true` (§3).

**Named remaining divergences (not fixed — decisions, not oversights):**

1. `value_b` is still a bare numeric in SQL; Python v1.5 requires a
   verified-value **record** (§9). Changing the SQL signature is a
   wiring-lane API decision.
2. Postgres `round()` is half-away-from-zero; Python rounds banker's —
   an exact-.5 weighted sum can differ by 1 point.
3. SQL does not produce `reasons` (would need shared-element returns
   from every helper).
4. Non-array jsonb inputs error in SQL; Python degrades gracefully (§4).

## 8. INDEPENDENT HOLDOUT — DONE: 20/20 (synthetic, labeled)

`holdout_set.py` + `test_holdout.py`: 20 hand-written citizen-like cases
**not derived from the declared population** — 18 pair expectations
(clear matches: baker↔café, swim coach↔triathlon club, beekeeper↔
orchard, tutor↔homeschool co-op, photographer↔wedding venue, yoga
teacher↔wellness studio, accountant↔freelancers, electrician↔
makerspace, dog trainer↔shelter, translator↔book club, carpenter↔
furniture store, astronomer↔stargazing club; borderline-true:
meal-prep cook↔gym; clear non-matches: chess↔garden, physicist↔
plumbers, poet↔tax firm, surfer↔chess club; borderline-false: violin
teacher↔luthier, held below the surface bar at exactly 1 signal) +
2 ordering checks (Rosa → Bakery Cafe 47% top; Dev → Data Bootcamp 35%
top). **Result: 20 passed, 0 failed.**

First run was 19/20 — the one failure (photographer↔wedding venue
scoring 0 on every channel) exposed a real engine bug, fixed in §11 —
the test was not adjusted to fit. This set is **synthetic**: it probes
generalization beyond the golden set's population; it is not citizen
data, and calibration on real Welcome answers is still owed.

## 9. VALUE-RECORD CONTRACT — DONE

`score()`'s `value_b` now passes through `_verified_value`: only a
record (dict) carrying `state` ∈ {VERIFIED, FINAL} and a numeric
`value` in [0, 1] influences ranking. A bare float, a PENDING record, or
anything else is **neutral** — per the points profile (points are
PENDING at observed, FINAL at verified; unverified value must not move
matches). Tests pin the arithmetic truth: rank = relevance × (0.9 +
0.1·v), so VERIFIED 1.0 equals the plain baseline, VERIFIED 0.0 scores
below it, and the match **percent never moves** — only ranking weight.

## 10. ALIAS SAFETY — DONE

`welcome_engine.issue_link_sql` validates the alias against
`^[a-z0-9][a-z0-9_-]{1,31}$` and raises `ValueError` on anything else —
the alias is interpolated into SQL, so this closes an injection-shaped
hole at the door. Tests cover 10 bad aliases: quotes, spaces, uppercase,
overlong, leading dash, single char, empty, non-string.

## 11. TWO FURTHER FIXES THE NEW TESTS FOUND (beyond the work order)

Both gated: golden printout byte-identical, FP-12 stable, 23 old tests
green after each.

- **Stemmer lemma/plural asymmetry (v1.4 elif chain):** "wedding"
  stemmed to "wed" but "weddings" to "wedding" — the same word in two
  forms never met (this was the holdout's one failure). Plural stripping
  now applies **before** the -ing rule: 'weddings' → 'wedding' → 'wed',
  exactly like 'wedding'; 'buildings' → 'building' → 'build'.
- **Glue-only phrase matching:** covered in §1 (`_content_phrases`).

## 12. FIRST POPULATION — BEFORE / AFTER (FP-12, IDF OFF)

Same 15 surfaced pairs before and after; only stopword-inflated numbers
move. Full tables in the run logs; the deltas:

| pair | before | after | why |
|---|---|---|---|
| Nitro ↔ Team Nitro | 62 | 62 | — |
| Power ↔ NayaPOWER | 57 | 57 | — |
| Power ↔ Smart Factory | 32 | 32 | — |
| Power ↔ One Hub | 26 | **27** | stopword dilution removed |
| NayaPOWER ↔ One Hub | 24 | **25** | stopword dilution removed |
| NayaPOWER ↔ Smart Factory | 18 | 18 | — |
| Power ↔ Nitro | 18 | 18 | — |
| Power ↔ Resolve | 16 | **14** | goals signal was stopword-only ("the") — correctly gone; surfaces on topics+wants |
| Nitro ↔ NayaPOWER | 15 | 15 | — |
| Power ↔ Team Nitro | 14 | 14 | — |
| Nitro ↔ One Hub | 14 | 14 | — |
| NayaPOWER ↔ Team Nitro | 12 | 12 | — |
| Ask Naya ↔ One Hub | 8 | **6** | stopword dilution removed |
| Team Nitro ↔ Smart Factory | 7 | 7 | — |
| Nitro ↔ Ask Naya | 4 | 4 | — |
| pairs scoring 0 | 33 | **36** | phantom stopword signals removed |

## 13. WHAT DID NOT CHANGE / NOT DONE HERE

- No PR opened, nothing posted, SQL **not deployed**, production
  untouched — per the run's constraints. Landing needs a different-seat
  scorecard at this head + the L659 reconcile rule if any other cure
  touches the same files first.
- Calibration circularity stands (golden set authored from the declared
  population); the holdout mitigates, real citizen data cures.
- Island spaces (Smart Mail, Mirror Program, One Flow, Voice) still
  surface no matches — their vectors are thin; the cure is Welcome
  answers filling every space, a wiring-step item.

*Evidence: run logs + before/after tables retained in the lane's
hardening scratch (`hidden_files/automatch-hardening/logs/`).*
