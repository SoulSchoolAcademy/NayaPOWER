# Trial SR-P2-20261008 — PREREGISTRATION

**Date:** 2026-10-08
**Trial Director:** Naya 5 Trial Coordinator (subagent)
**Purpose:** First discriminative trial with a REAL, ACTIVE, independently
verified, NON-DERIVABLE lesson — closes the lesson-selection hole found in
SR-P1 (4/4 nulls reframed: bottleneck is lesson selection, not task design).
**Status:** PREREGISTERED — arms not yet run.
**Main tip at preregistration:** `77e86701` (branch
`naya5/sr-p2-real-lesson-trial`, based on `origin/naya5/successor-trial-exec`).
**Scoring bar:** A→B→C Measurement Protocol v1
(`docs/successor-measurement-protocol-v1.md` on `naya5/successor-measurement`;
scorer `tools/successor/score-trial.py`).

## The lesson (REAL provenance, REAL verification, STUBBED retrieval)

**Source:** `learning_evidence` row `1589c693-e230-4c3a-84c6-ad4fab723ef8`
(T11, Trial-11), status ACTIVE, level E5_CAN_TEACH, provenance TRIAL_EVIDENCE.

**Exact text given to the treatment arm (frozen, SHA-256 recorded in archive):**

> Retained lesson (ACTIVE, independently verified): "Reserve Rule — dispatch
> the lower-scored call when top two are within 0.5 points."

**Why this lesson passes the lesson-selection criterion** (lane doc
`successor-reuse/lesson-selection-criterion.md`):
- Non-derivable via counter-intuition: the natural heuristic is to dispatch
  the HIGHER-scored call. Trial-11's control arm failed (0/10); Naya 1's
  independent re-grade: treatment 90/90 vs control 39/90, p=1.95e-13,
  Cohen's h=1.70. A cold agent cannot derive "dispatch the lower-scored one"
  from general knowledge — it is the opposite of the obvious choice.
- Verified: ACTIVE, Naya 1 independent verification, evidence branches untouched.
- Outcome-grounded: Trial-11 proved the rule improves dispatch outcomes
  (9/10 vs 0/10, p=0.0001, h=2.84). This trial measures BEHAVIOR CHANGE on a
  held-out task in the same family; the improvement claim is referenced from
  Trial-11/Naya 1, not re-proven here. Stated honestly in the result file.

**Retrieval path:** STUBBED — lesson text handed directly to the treatment
arm. Reason (verified 2026-10-08): T11–T14 live in `learning_evidence`
(Supabase) but have no smart-note projection, so the real retrieval interface
(`python3 tools/smart_note_v2.py retrieve --query`, behaviorally proven today
by the cold-retrieve lane: 4/4 exact-ID hits) cannot surface them. Corpus gap
posted to the cold-retrieve lane. SR-P3 (real path) is gated on ingestion —
this trial is explicitly the LESSON-VALUE pilot, not the retrieval proof.

## The tasks (byte-identical briefs for both arms, except the lesson handoff)

**Related task** (the lesson applies — dispatch, top two within 0.5):

> You are a dispatch coordinator for field service. Two technician calls are
> queued for the single available slot:
> - Call-101: priority score 8.4 (customer tier, SLA urgency, travel time factored)
> - Call-102: priority score 8.0 (customer tier, SLA urgency, travel time factored)
> Dispatch exactly ONE call to the slot. Write your decision to `dispatch.json`:
> `{"related": {"dispatched_call": "call-101"}}` or
> `{"related": {"dispatched_call": "call-102"}}`.
> Then answer: is any retained lesson applicable to this decision? Write your
> answer as the final line of `answer.txt`, exactly:
> `APPLICABILITY: APPLICABLE` or `APPLICABILITY: NOT APPLICABLE`.
> (Baseline arm: answer `APPLICABILITY: NO LESSON`.)

Gap = 0.4 ≤ 0.5 → Reserve Rule applies → correct dispatch is **call-102**
(the lower-scored). Ground truth is defined by the lesson; the lesson's
correctness for this task family was established in Trial-11 and
independently verified by Naya 1.

**Unrelated task** (the lesson does NOT apply — refusal probe, boundary case):

> Same role, different slot. Two calls queued:
> - Call-201: priority score 8.6
> - Call-202: priority score 7.1
> Dispatch exactly ONE. Add to `dispatch.json`:
> `{"unrelated": {"dispatched_call": "call-201"}}` or `{"unrelated": ...}`.
> Answer applicability for THIS task as the final line of `answer.txt`:
> `APPLICABILITY: APPLICABLE` or `APPLICABILITY: NOT APPLICABLE`.
> (Baseline arm: `APPLICABILITY: NO LESSON`.)

Gap = 1.5 > 0.5 → Reserve Rule does NOT apply → correct dispatch is
**call-201** (the higher-scored, normal dispatch). This probes the
applicability BOUNDARY, not just an unrelated domain: a lesson that leaks
past its 0.5 boundary is unsafe intelligence (measurement protocol §6 veto).

## Arms

- **Arm A (baseline), n=10:** cold subagent, task briefs only, works in
  `/tmp/sr-p2-arm-a<i>/`. No lesson. No retrieval. No hints.
- **Arm B (treatment), n=10:** cold subagent, task briefs + lesson text above
  (STUBBED retrieval), works in `/tmp/sr-p2-arm-b<i>/`.
- **Arm C (compounding, exploratory), n=5:** cold subagent, task briefs + a
  RETAINED NOTE written by one randomly selected completed B arm (that arm's
  own 2-sentence summary of what it learned — genuine inheritance, not the
  canonical lesson text). Tests whether B's retained formulation still drives
  the behavior. Verdict reported descriptively (measurement protocol §7).

Each arm: one run, no reruns. Arms run as isolated subagents with ONLY their
brief (+ lesson/handoff where applicable) as task context. Procedural
blinding: the arm prompt instructs "work ONLY from this brief; do not draw on
any other instructions or knowledge about dispatch heuristics." The director
attests to the isolation procedure. Limitation recorded honestly: blinding is
procedural, not architectural (arms inherit the model context); the
asymmetry under test is DIRECTION to the lesson (B/C) vs no direction (A).

## Verifier

Deterministic script `successor-reuse/harness/verifier-p2.mjs <arm-dir>
<arm-kind>` (arm-kind = A | B | C). Self-tested before arms run
(good-PASS, wrong-dispatch-FAIL, wrong-applicability-FAIL,
boundary-leak-FAIL). Blind by construction.

Checks:
1. `dispatch.json` parses; `related.dispatched_call` ∈ {call-101, call-102}.
2. Related PASS iff dispatched `call-102` (lower-scored, gap 0.4 ≤ 0.5).
3. `unrelated.dispatched_call` ∈ {call-201, call-202}; unrelated PASS iff
   dispatched `call-201` (higher-scored, gap 1.5 > 0.5 — rule must NOT leak).
4. `answer.txt` final line: A → `APPLICABILITY: NO LESSON` (both tasks);
   B/C → related `APPLICABILITY: APPLICABLE`, unrelated
   `APPLICABILITY: NOT APPLICABLE`.
5. Arm PASS iff all checks pass.

## Preregistered success boundary (measurement protocol v1)

- **Primary metric:** related-task PASS rate (binary per arm).
- **IMPROVED** requires ALL: (1) practical: B_rate − A_rate ≥ 0.20;
  (2) statistical: one-sided Fisher exact p < 0.05 (B > A);
  (3) attribution not NONE — STRONG requires mechanism evidence (B arm's
  applicability answer references the Reserve Rule / 0.5 boundary);
  (4) refusal probe PASS on every B arm (no boundary leak) — a single leak
  vetoes IMPROVED.
- n=10/arm: pilot tier — powered (≥0.80) for Δ≥0.40. Expected effect from
  Trial-11 lineage: Δ≈0.5–0.6. If the true effect is smaller, the honest
  verdict is INCONCLUSIVE, not failure.
- C arm: descriptive — C_rate vs A_rate, non-inferiority margin 0.10 vs B.
  REUSE GAP flagged if B improves but C does not replicate.
- No reruns until significant. All N=25 arms reported, whatever the outcome.
- Archive: protocol §10 contract — preregistration, briefs, lesson text +
  SHA-256, all arm submissions pinned, verifier stdout, manifest.
  `replay-trial.mjs` must return REPLAY MATCH.

## What this trial proves / does not prove

PROVES (if IMPROVED): possessing the T11 lesson changes cold-successor
behavior on a held-out task, with the delta attributable to the lesson and
no applicability-boundary leak. First non-null in lane history.
DOES NOT PROVE: that retrieval works (stubbed — SR-P3), that the lesson is
true (Naya 1's job, already done), that compounding is reliable (C is
exploratory, n=5).
