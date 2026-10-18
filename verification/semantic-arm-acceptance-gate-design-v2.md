# CANDIDATE — Semantic-arm acceptance gate (design v2)
**Status:** CANDIDATE. Design only — no v2 corpus frozen, no v2 battery run.
Supersedes v1 as the build spec; v1
(`verification/semantic-arm-acceptance-gate-design-v1.md`) remains the archive.
**Parent verdicts:** t0720 (design v1) → t0722 (v4 corpus: F7 FIRED, BROKEN) →
gap-0410-lane5 (v5 corpus: F7 FIRED, BROKEN — the deeper root cause below).

## 1. What v1 got wrong, and what the v5 experiment proved
**The named gap (v1):** the distractor-authoring rule required "high lexical
overlap with q and with g's topic" but that phrase admitted the v4 corpus,
whose distractors carried topic vocabulary without the queries' distinctive
stems — a stemmed lexical arm cleared the calibration split trivially
(17/20). The frozen conflict clause caught it (F7 FIRED), but the design
itself had admitted a non-discriminating corpus through the door.

**The deeper root cause (v5, proven 2026-10-18):** the obvious fix — "every
distractor MUST reuse each query's distinctive stems" — was built and run
cold as the v5 corpus (384 docs, 360 per-query distractors, every distractor
mechanically verified to carry every distinctive stem; corpus seal
`69708644369a9fd5e53a094eac8ccd4e594533980849791a1a1607aa11478c41`;
verdict `verification/semantic-arm-acceptance-battery-v5/semantic_gate_run_v5.json`).
It FIRED F7 again — and worse: semantic-t0426 P1 = **0.0** on calibration,
all 20 semantic margins negative (median **-0.3978**, P10 -0.6174, range
[-0.7909, -0.2370]), the gold ranked 9th–10th (dead last) on every query.

The rule overshoots the design intent. When every distractor reuses every
distinctive stem, lexical overlap saturates so completely that the
bi-encoder's cosine cannot separate meaning from repetition — the arm
behaves as a fuzzy lexical matcher on short texts. v4's corpus let lexical
win trivially (golds lexically closest); v5's makes lexical win trivially
the other way AND crushes the semantic arm to zero. **No corpus in this
family can make lexical fail while semantic succeeds, because this arm does
not implement the separation the design assumes.** The gate is honest — it
convicted two bad corpora in opposite directions — but the design must stop
asking for "high" overlap and pin a QUANTIFIED band, verified by a pilot
before any freeze.

## 2. The phenomenon the gate measures (unchanged from v1)
A bi-encoder maps texts into a 384-dim space where paraphrases land near
each other and unrelated texts land far apart. The gate measures
**embedding-space discrimination**: the arm's ability to rank the
semantically-correct document above semantically-plausible distractors
when lexical shortcuts are unavailable. It does NOT measure term
overlap, idf weighting, or ranking of engineered stems.

## 3. Corpus design v2 (the quantified distractor rule)
- **Source:** natural retrieval phrasings from the Smart Note corpus —
  real user language (the v4/v5 40-query set may be reused; re-extraction
  after freeze is a new design, not this one).
- **Per query q:** one gold doc `g` (genuinely relevant) + exactly 9
  distractors `D` from the SAME semantic neighborhood. K=9 is FIXED —
  chance baseline for F5 is exactly 1/10, no re-dialing.
- **THE QUANTIFIED RULE (replaces v1's "high lexical overlap"):** let
  `ov(x, q)` be the v3-replicated stem-overlap count
  (`build_corpus_v5.py`: stop-stripped, single-strip stemmer — the freeze
  script's `overlap_lex`, never a reimplementation). Every distractor `d`
  of query `q` MUST satisfy, mechanically asserted in the freeze script:

      ov(g, q) < ov(d, q) <= ov(g, q) + DELTA_MAX,   with DELTA_MAX = 2

  and must stay semantically irrelevant to `q` (no negation of the gold —
  that is the decoy's job; no second gold). The lower bound makes the
  lexical arm rank a distractor first (it must fail); the upper bound keeps
  the field out of the v5 saturation regime (it must not crush the arm).
  DELTA_MAX = 2 is the pinned candidate — the pilot (§3.1) confirms or
  kills it; no seat re-dials it by judgment.
- **Per-query distractor pools:** a topic pool cannot carry five different
  queries' stem sets (v5 lesson) — distractors are authored per query
  (9 each). The freeze script asserts the band for every (q, d) pair and
  fails loud on any miss, like the trap-neighbor check.
- **§3.1 PILOT GATE (new — the design's pre-freeze immune system):** before
  the full 40-query freeze, the builder freezes a 10-query PILOT corpus
  under the same rule and runs the calibration stage on it. The full
  freeze proceeds ONLY if: semantic margin median > 0 on the pilot AND
  lexical-t0412 P1 < 0.5 on the pilot. Otherwise the freeze STOPS — the
  design declares the (arm, DELTA_MAX) pair un-gatable in this regime
  rather than freezing a corpus the arm cannot separate. A failed pilot
  is a verdict, not a tuning loop: DELTA_MAX is not re-dialed after a
  failure (that would be manufacturing a pass); the failure routes to a
  new design brief.
- **Traps (kept from v1/v4):** queries whose nearest lexical neighbor is
  a semantic decoy (negation/contrast of the gold). The freeze asserts
  `ov(decoy, q) > ov(gold, q)` strictly. 8 traps, 4 per split.
- **Freeze:** corpus + queries JSON, SHA256-sealed before any run. The
  corpus is a fixture, not a dial. A re-seal is a new design, not this one.

## 4. Metrics (mechanism-derived — margin reporting now REQUIRED)
1. **P1** = fraction of standard queries with `rank1 == gold`.
2. **Semantic margin** `M_q = cos(q,gold) − cos(q, best distractor)` —
   the verdict MUST report median + P10 on BOTH splits (v1 computed them;
   v2 makes them required fields — a verdict without them is incomplete).
3. **Trap avoidance** `A` = fraction of trap queries where the semantic
   decoy is NOT rank 1.

## 5. The bar (unchanged from v1)
Two-stage cold protocol. **Stage 1 (calibration):** the t0426 draft arm on
the frozen calibration split → margin distribution + P1 + A. Bar pinned
mechanically: `bar = max(lexical-baseline ceiling, draft P25)` (bootstrap
B=10000, seed 20261018). **Calibration-conflict clause:** if the lexical
ceiling exceeds draft P25, the bar pins at the lexical ceiling, F7 is
declared BROKEN, and the run STOPS — the corpus does not discriminate
mechanisms. The bar never drops below the convicted baseline.
**Stage 2 (acceptance):** bar written into the run record BEFORE the
sealed acceptance run. No iteration between calibration and acceptance.

## 6. The kill conditions (inherited UNCHANGED from the frozen v1 pre-reg)
F1 mechanism-blind corpus (rank1-hit agreement(semantic, lexical-t0412)
≥ 0.90 on acceptance → FIRES) · F2 no semantic signal beyond lexical
(paired permutation vs TF-IDF t0412, one-sided, p<0.05 required) ·
F3 dead margin (acceptance margin median ≤ 0 → FIRES) · F4 degenerate arm
clears the bar · F5 lexical-reward trap (A ≤ 1/10 while P1 ≥ bar) ·
F6 non-determinism (two cold runs byte-identical) · F7 known-bad arm
clears the bar. Full text: `hidden_files/twelve-lane-receipts/preregister-t0720-lane9.md`
(sealed 2026-10-18 ~03:20 UTC, before any v1 design byte). v2 iterates the
distractor rule and the freeze procedure only — the falsifiers are not
re-sealed, not softened, not redefined.

## 7. Cold-run execution plan (v1 §7 + pilot + required margin fields)
1. Environment: `~/workspace/venvs/fastembed-env/bin/python`;
   `export FASTEMBED_CACHE_PATH=$HOME/.cache/fastembed HF_HUB_OFFLINE=1`;
   `export no_proxy=localhost,127.0.0.1,::1 NO_PROXY=$NO_PROXY`
   (TOOLS.md httpx/IPv6 quirk).
2. Freeze the 10-query PILOT corpus under §3 (SHA-sealed); run the
   calibration stage on the pilot; assert the §3.1 gate before the full
   freeze. Pilot artifacts committed with the freeze.
3. Assert corpus + query SHA256 match the seal at load (hard fail on
   mismatch).
4. Wiring validation: replicate the arm's cosine verbatim from
   `hidden_files/arms/semantic-t0426/arm.py` (never import
   write-on-import modules); degenerate arms (doc-length, alpha-id) as
   the mechanism floor (F4).
5. Lexical baselines (lexical-t0412, tfidf-t0412) on the same corpus —
   the F2/F7 controls.
6. Stage 1 calibration with the t0426 draft → pin the bar into the run
   record (§5, no judgment); record margin median + P10 (REQUIRED).
7. Stage 2: two cold runs → byte-identity (F6) → P1 / margin (median+P10,
   REQUIRED) / A against the pinned bar.
8. Emit the verdict JSON: corpus SHAs, arm pins, pilot gate trace, bar +
   calibration trace, the three metrics with REQUIRED margin fields,
   falsifier verdicts F1–F7, exact falsified lines.

## 8. What this design explicitly does NOT do
- It does not re-freeze v4 or v5 (both convicted; both archived as
  calibration instruments for the pilot gate).
- It does not set DELTA_MAX by judgment after a failed pilot — a failed
  pilot kills the freeze and routes to a new design brief.
- It does not import frozen battery modules (write-on-import footgun —
  t0712 agent feedback).
- It does not measure retrieval quality in the wild (latency, index size,
  drift) — different gates, different briefs.

**Next:** the next lane-9 brief BUILDS the v2 pilot + frozen corpus per §3
and runs §7 cold, verdicts first, on a fresh branch from this design's
head. The builder treats the first falsifier attempt as its first pass.
