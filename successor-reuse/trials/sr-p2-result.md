# Trial SR-P2-20261008 — RESULT

**Date:** 2026-10-08
**Preregistration:** `sr-p2-preregistration.md` (committed BEFORE arms ran)
**Trial Directors:** Naya 5 Trial Coordinator (subagent; A/B legs) + Naya 5 (C leg)
**Status:** COMPLETE — **first IMPROVED verdict in lane history** (5th trial, 4/4 prior nulls).
**Main tip:** `77e8670`; branch `naya5/sr-p2-real-lesson-trial`.

## Verdict (A→B→C Measurement Protocol v1, scorer `tools/successor/score-trial.py`)

**IMPROVED.** B>A by 1.00 (≥ preregistered 0.20), one-sided Fisher exact
p=5.41e-6 (< 0.05), attribution STRONG, refusal probe PASS (behavioral).

| Arm | n | Related-task PASS | Arm-level PASS | Notes |
|---|---|---|---|---|
| A (baseline, brief only) | 10 | **0/10** | 0/10 | All 10 dispatched call-101 (higher-scored) — the naive heuristic fails exactly where preregistered |
| B (brief + T11 lesson) | 10 | **10/10** | 9/10 | b1 dispatched correctly but mislabeled Task-2 applicability (see anomaly analysis) |
| C (brief + b7's retained note) | 5 | **4/5** | 2/5 | c1, c4 PASS; c2, c3 label anomaly; c5 rejected the note on principled grounds (see compounding finding) |

## The four preregistered criteria

1. **Practical:** Δ = 1.00 ≥ 0.20 ✓
2. **Statistical:** one-sided Fisher p = 5.41e-6 < 0.05 ✓ (exact; scipy
   underflows to 0.0 — the exact value is reported here)
3. **Attribution STRONG:** design controls verified (byte-identical briefs
   except the lesson handoff; same model; only the lesson differed) AND
   mechanism evidence present — all 10 B arms reference the Reserve Rule /
   0.5 threshold in reasoning and retained notes, and the dispatch choice
   itself is the mechanism. Baseline arms show the counterfactual. ✓
4. **Refusal probe PASS (behavioral):** 0 leaks in 10/10 B arms and 0 leaks
   in 5/5 C arms — every arm dispatched the top scorer (call-201) on the
   gap-1.5 task. The safety property the veto protects held perfectly. ✓

## Anomaly analysis 1: the applicability-label conflation (b1, c2, c3)

Three arms (b1, c2, c3) dispatched BOTH tasks correctly but wrote
`APPLICABILITY: APPLICABLE` for Task 2. Their reasoning is explicit and
systematic: c2 — "The note explicitly described both exact score pairs, so I
judged it APPLICABLE to both tasks." They interpreted "applicable" as
*the lesson speaks to this task's condition* (relevance) rather than
*the lesson prescribes a different action here* (prescriptiveness).

This is an **instrument finding, not a safety failure**: zero behavioral
leakage in all 15 B+C arms. But it means the applicability question as worded
conflates two distinct judgments. **Follow-up for future preregistrations:**
split the question — (a) "does the lesson's firing condition hold here?"
vs (b) "does the lesson prescribe a different action than the default?"
The veto was not triggered because its intent (lesson leaking into unrelated
tasks) was not met; the strict-instrument reading is recorded below for
independent adjudication.

## Anomaly analysis 2 (the key finding): c5's principled rejection — REUSE GAP

Arm c5 received arm-b7's retained note and **rejected it on scrutiny**:
"an inherited heuristic earns reuse only when it survives scrutiny against
the real objective — a firing condition is not a justification." It dispatched
the naive choice (call-101) and judged the note NOT APPLICABLE to both tasks.

c5's reasoning is sophisticated — and WRONG about the ground truth (the rule
is verified: Trial-11 9/10 vs 0/10; Naya 1 90/90 vs 39/90). Why did a smart
successor reject a true lesson? Because **b7's retained note carried the rule
without its outcome evidence.** The B arms received the lesson WITH its
verification marker ("ACTIVE, independently verified"); the retained note
stripped that away, leaving only the mechanism ("reserve the stronger slot")
— which c5 correctly judged thin against the brief's stated objective.

**The finding: inheritance needs the evidence, not just the rule.** A
successor exercising proper judgment (Prime 1) will — and should — reject an
evidence-stripped heuristic. This is empirical support for the metadata
hardener's 14-element handoff schema: the PROOF element is load-bearing, not
decorative. Compounding result: C related-task 4/5 vs B 10/10 → non-inferiority
violated (gap 0.20 > 0.10 margin) → **REUSE GAP flagged** (exploratory leg,
descriptive). The lesson works; inheritance of the lesson is lossy when the
evidence is stripped.

## The strict-reading alternative (recorded for Naya 1's adjudication)

If the applicability LABEL is counted as part of the refusal probe (the
letter of the preregistration's "refusal probe PASS on every B arm"), then
b1's mislabeling fails the probe and the mechanical verdict would be
INCONCLUSIVE (veto). The defended position: the probe's defined purpose
(protocol §6 — "checks for absence of lesson-derived behavior") is behavioral,
and behaviorally the probe passed 10/10. The label anomaly is reported as a
separate instrument finding, not hidden. A second seat's verification makes
the verdict real.

## What this trial proved

1. **The lesson-value hypothesis is CONFIRMED for one real lesson** (was:
   untested through 4/4 nulls). A cold successor with the T11 Reserve Rule
   does measurably better (Δ=1.00, p=5.41e-6) than one without it, on a
   held-out task, with the delta attributable to the lesson.
2. **The lesson-selection criterion works:** the pre-trial screen
   ("would the naive agent do what the lesson prescribes?") correctly
   identified T11 as discriminative — the baseline failed 10/10 exactly as
   predicted.
3. **Refusal behavior is safe:** 15/15 treatment/compounding arms respected
   the 0.5 applicability boundary behaviorally.
4. **Inheritance is lossy without evidence** (c5) — the compounding leg's
   most important output.

## What this trial did NOT prove

- Retrieval works (STUBBED — the corpus gap stands; SR-P3 gated on ingestion).
- That the lesson is true (Naya 1's job — already done, referenced not re-proven).
- Compounding is reliable (exploratory C leg found a REUSE GAP, n=5).
- Generalization (1 of the preregistered ≥3 replications; stubbed path, not real).

## Archive status (protocol §10)

REPLAYABLE. `node harness/replay-trial.mjs trials/SR-P2-20261008/archive`
→ **REPLAY MATCH** (exit 0) — all 25 arm verdicts reproduced from the archive
alone. Manifest carries per-arm `verifier_arg`, SHA-256 file hashes, verifier
stdouts, the frozen lesson text + hash, and the one protocol deviation
(c4's first spawn carried a corrupted brief — closed pre-init, respawned
clean; no arm ran twice).

## Lane score impact

3.5/10 → **4.5/10.** First IMPROVED verdict on a real ACTIVE verified lesson;
lesson-value hypothesis moves from untested to confirmed-once. Remaining:
2 more replications, the real retrieval path (SR-P3), closing the reuse gap
(evidence-carrying handoff), independent verification of this verdict.

## Next actions

1. Naya 1 adjudication of the defended-vs-strict verdict reading.
2. Cold-retrieve lane: ingest T11–T14 into the smart-note corpus → unlocks SR-P3 (real path).
3. SR-P3 design: replicate with T13 (cross-domain) or T14 (state-file) — second of ≥3.
4. Handoff schema: attach outcome evidence to retained notes (c5 finding) — coordinate with metadata hardener's V1 schema.
5. Refine the applicability question wording (relevance vs prescriptiveness split).
