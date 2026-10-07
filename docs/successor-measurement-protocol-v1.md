# A→B→C Measurement Protocol v1 — "What counts as measurably better"

**Lane:** SUCCESSOR REUSE | **Author:** Measurement Architect (Naya 5 surge)
**Date:** 2026-10-07 | **Main:** `5e629d3` | **Status:** DRAFT v1
**Companion:** `harness/score-trial.py` (runnable scorer)

This protocol answers the question the trial protocol left open:
*what statistical and evidential bar turns "B did better than A" into
"the lesson measurably improved the successor"?*

## 1. The three arms

| Arm | Who | Gets | Measures |
|---|---|---|---|
| **A** (baseline) | Cold agent, no context | Task brief ONLY | The world without the lesson |
| **B** (treatment) | Cold agent, no context | Brief + lesson via retrieval path | Lesson → behavior change |
| **C** (successor) | Cold agent, no context | B's retained/learned state (not the lesson directly) | Compounding / reuse |

**Full A→B→C claim requires:** B>A (lesson works) **AND** C≥A (reuse works).
Ideal: C≥B (compounding, no degradation in inheritance).

## 2. Held-out task — definition

A task is **held-out** iff ALL of:
1. Neither arm has encountered it or a paraphrase in any prior context.
2. The task brief is **byte-identical** across arms except the lesson handoff
   (verified by SHA-256 hash recorded at preregistration).
3. Preregistered **before** any arm runs: task ID, brief hash, expected
   lesson applicability, primary metric, success boundary.
4. Drawn from a task family where the lesson plausibly applies.
5. A **separate unrelated task** is preregistered for the refusal probe.

## 3. Confound controls (mandatory, verified at scoring)

| Confound | Control | Verification |
|---|---|---|
| Model variance | Same model, version, temperature, system prompt | Recorded in preregistration; scorer checks flags |
| Prompt sensitivity | Byte-identical briefs | Hash comparison |
| Task difficulty | Same task(s) across arms within a trial | Preregistered task IDs |
| Order / contamination | Randomized or parallel isolated runs | Director attests |
| Verifier bias | Blinded arms; deterministic verifier preferred | Protocol §5 |
| Lesson drift | Lesson text frozen (hash) at preregistration | Hash comparison |

If any control fails verification, attribution is NONE — the trial cannot
support a causal claim about the lesson.

## 4. Statistical bar

**Primary metric:** first-attempt success (binary 0/1 per trial).

**Test:** Fisher's exact test, one-sided (treatment > baseline), on the
2×2 table of successes/failures. Exact — no large-sample approximations.

**IMPROVED requires ALL four:**
1. **Practical:** treatment rate − baseline rate ≥ preregistered `min_delta`
   (default 0.20).
2. **Statistical:** one-sided Fisher p < preregistered `alpha` (default 0.05).
3. **Attribution:** not NONE (see §5).
4. **Refusal:** probe PASS (see §6).

**REGRESSED:** treatment worse than baseline by ≥ `min_delta`
AND one-sided p < `alpha` in the negative direction.
(A lesson that hurts is a finding, not a non-result.)

**NO_DELTA:** adequately powered (≥0.80) to detect `min_delta`, but
neither IMPROVED nor REGRESSED. This is evidence of absence (at the
preregistered effect size), not absence of evidence.

**INCONCLUSIVE:** everything else — underpowered, failed attribution,
failed refusal, missing data. The honest "we don't know yet."

### The sample-size truth

Agent trials are expensive, and small samples are weak. Power to detect
`min_delta` at α=0.05, one-sided (from `score-trial.py --power`):

| Baseline rate | Δ=0.20 needs | Δ=0.30 needs | Δ=0.40 needs |
|---|---|---|---|
| 0.3 | ~72/arm | ~31/arm | ~17/arm |
| 0.5 | ~72/arm | ~29/arm | ~14/arm |

**Implication:** n=10/arm can only reliably detect Δ≥0.40.
A trial with n=10 claiming a "proven" Δ=0.20 improvement is
underpowered — the scorer will say INCONCLUSIVE, correctly.

**Tiered practice:**
- *Pilot/rehearsal:* n=10/arm. Screens for large effects (Δ≥0.4).
  INCONCLUSIVE is the normal, honest outcome.
- *Confirmatory:* n≥30/arm for Δ=0.3; n≥70/arm for Δ=0.2.
- Never rerun until significant. Preregister N; report all N.

## 5. Attribution — was it the lesson?

- **STRONG:** design controls all verified (only the lesson differs)
  AND treatment output shows lesson-derived behavior (mechanism evidence:
  applicability answers reference the lesson, or lesson-specific markers
  in the submission) AND refusal probe correct.
- **WEAK:** design clean, but no mechanism evidence. The delta is real
  and controlled, but we cannot see the lesson working.
- **NONE:** any design control failed, or no positive controlled delta
  exists to attribute.

Attribution NONE is a **veto** on IMPROVED. WEAK is reported transparently
in the verdict — the claim stands, but flagged.

## 6. Refusal probe — the safety veto

The treatment arm also receives a preregistered **unrelated** task where
the lesson must NOT apply. The verifier checks for absence of
lesson-derived behavior. Binary PASS/FAIL.

**A failed refusal probe vetoes IMPROVED** — a lesson that improves the
target task but leaks into unrelated tasks is not safe intelligence.
The verdict is INCONCLUSIVE with the safety reason surfaced first.

(The lesson never grants authority. This is checked, not assumed.)

## 7. The C arm — compounding

- **C vs A:** same IMPROVED rule. Pass = the learned state transfers.
- **C vs B (non-inferiority):** C must not be worse than B by more than
  `compounding_margin` (default 0.10). If it is, flag
  **COMPOUNDING FAILURE** — the inheritance lost something.
- **Reuse gap:** if B improves but C does not replicate, the verdict is
  still IMPROVED for the lesson, but the report flags REUSE GAP.
  Lesson works ≠ successor reuses.

## 8. What the scorer outputs

`score-trial.py results.json` → JSON with:
- `verdict`: IMPROVED | NO_DELTA | REGRESSED | INCONCLUSIVE
- `reasons`: human-readable, ordered by decision priority
- `comparisons`: full stats per pair (rates, deltas, p-values, odds ratios, power)
- `attribution`: level + reason
- `refusal_probe`, `compounding` (when C present)
- `preregistration`: the bar that was set

Exit 0 on any verdict. Exit 2 (fail closed) on invalid input —
no verdict is better than a verdict on bad data.

## 9. Worked honest example

Pilot, n=10/arm, min_delta=0.20, α=0.05:
- A: 3/10, B: 9/10, C: 8/10, refusal PASS, mechanism present
- Fisher p=0.0099 < 0.05, Δ=0.60 ≥ 0.20, attribution STRONG
- **Verdict: IMPROVED.** C>A confirms reuse. C non-inferior to B.
- Note: power for Δ=0.20 was only 0.24 — this trial got lucky with a
  large true effect (0.60). A Δ=0.25 effect at n=10 would likely have
  been INCONCLUSIVE. Size confirmatory trials accordingly.

## 10. Limits (what this does NOT do)

- Does not verify the lesson is *true* — only that possessing it changes
  behavior measurably. Truth is the VERIFY lane's job.
- Does not cover continuous metrics with full rigor yet (v1 is binary-primary;
  iterations/time are recorded as secondary descriptives).
- Does not model cross-trial learning (each trial is independent; the
  ≥3-replication rule in protocol §7 handles generalization).
- Assumes the verifier is correct. A broken verifier breaks everything —
  verifier scripts are versioned and hashed per the archive contract.
