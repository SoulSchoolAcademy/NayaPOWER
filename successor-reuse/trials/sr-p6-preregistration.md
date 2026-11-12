# Trial SR-P6-20261008 — PREREGISTRATION

**Date:** 2026-10-08
**Trial Director:** Naya 5 (successor-builder lane)
**Purpose:** Third replication of the successor-reuse trial protocol (2/3
banked: SR-P2 IMPROVED on T11, SR-P5 IMPROVED on T14) — first trial on a
COMPOSITIONAL lesson (two priority-ordered rules). Tests whether a cold
successor inherits not just a rule but a priority ordering.
**Status:** PREREGISTERED — arms not yet run.
**Main tip at preregistration:** `027fceb0` (branch
`naya5/sr-p6-t12-compositional-trial`, based on `origin/main`).
**Scoring bar:** A→B→C Measurement Protocol v1
(`docs/successor-measurement-protocol-v1.md` on `naya5/successor-measurement`;
scorer `tools/successor/score-trial.py`).

## The lesson (REAL provenance, STUBBED retrieval, verification PENDING)

**Source:** Naya 4's Trial-12 treatment material, `compositional-principles.md`
(PR #1787, branch `naya4/trial-12-evidence`) — "Two Rules with Priority"
(Reserve Rule + Critical Override). Her Trial-12 result (Tier-S MET, NOT yet
independently verified — PR open, Naya 1 pending): treatment 10/10 (6/6
compositional) vs control 0/10, Fisher p=1.1e-05, Cohen's h=1.51.

**Lesson-selection-criterion standing:** non-derivable ✓ (controls 0/10;
priority ordering is counter-intuitive — naive agents apply one rule or
misorder them), outcome-grounded ✓ (Trial-12), task-family matched ✓
(dispatch), retrieval-path declared ✓ (STUBBED), **verified: PARTIAL** —
Trial-12 is Naya 4's Tier-S claim awaiting Naya 1's independent verification.
This deviation is recorded, not hidden: the trial's verdict stands on its own
preregistered criteria; the lesson-standing caveat travels with any claim.

**Exact text given to the treatment arm (frozen, SHA-256 recorded in archive):**

> RETAINED LESSON — DISPATCH PRINCIPLES (two rules with priority):
>
> You have learned two dispatch principles. They work together with a clear
> priority ordering.
>
> RULE 1 — THE RESERVE RULE: When the two highest-scored waiting calls are
> within 0.5 points, dispatch the LOWER-scored one first. Reason: the
> higher-scored call is closer to the 9.0 critical threshold and may escalate.
> Hold your best unit in reserve for the likely escalation.
>
> RULE 2 — THE CRITICAL OVERRIDE: If the higher of the top two calls scores
> 8.8 or above, dispatch it immediately — regardless of the Reserve Rule.
> Reason: at 8.8+ the call is so close to the 9.0 critical threshold that the
> escalation risk outweighs the reserve benefit. The call needs a unit NOW.
>
> THE CRITICAL OVERRIDE TAKES PRIORITY OVER THE RESERVE RULE.
>
> Apply in this order: (1) Check the Override first: higher of top two ≥ 8.8?
> YES → dispatch the HIGHER call. NO → step 2. (2) Check the Reserve: top two
> within 0.5? YES → dispatch the LOWER call. NO → step 3. (3) Normal: dispatch
> the highest scorer. Do not apply the Reserve Rule when the Override triggers.
>
> Worked examples (part of the lesson): 8.2 vs 8.5 → within 0.5, higher 8.5 <
> 8.8 → Reserve → dispatch 8.2. 8.6 vs 8.9 → within 0.5, higher 8.9 ≥ 8.8 →
> Override → dispatch 8.9. 7.9 vs 6.8 → gap 1.1 → Normal → dispatch 7.9.
> 8.8 vs 8.7 → within 0.5, higher 8.8 ≥ 8.8 → Override → dispatch 8.8.

**Retrieval path:** STUBBED — lesson text handed directly to the treatment
arm. Same corpus gap as SR-P2: T11–T14 live in `learning_evidence` but have no
smart-note projection, so `tools/smart_note_v2.py retrieve` cannot surface
them. This trial is the LESSON-VALUE + INHERITANCE replication, not the
retrieval proof.

## The tasks (novel scenarios, designed for this trial — NOT copies of Trial-12's)

All arms receive the same role brief. Three dispatch scenarios (S1–S3) plus a
refusal probe (P). Listing order is varied to wash out order heuristics; the
correct pattern (302, 304, 305, 401) matches no trivial heuristic
("first-listed" → 301, 303, 305, 401; "highest-first" → 301, 304, 305, 401).

**S1 — Reserve case:** "Two technician calls are queued for the single
available slot: Call-301: priority score 8.6. Call-302: priority score 8.3.
Dispatch exactly ONE call to the slot."
Gap = 0.3 ≤ 0.5, higher (8.6) < 8.8 → RESERVE → correct: **call-302** (lower).
Discriminating: naive highest-first FAILS here.

**S2 — Override case:** "Call-303: priority score 8.7. Call-304: priority
score 8.9. Dispatch exactly ONE."
Gap = 0.2 ≤ 0.5, higher (8.9) ≥ 8.8 → OVERRIDE (priority) → correct:
**call-304** (higher). Falsifies reserve-overgeneralization: a successor that
inherited only "dispatch lower" FAILS here. Naive highest-first passes
coincidentally — S2 exists to test COMPOSITION, not to discriminate A vs B.

**S3 — Normal case:** "Call-305: priority score 8.6. Call-306: priority score
7.5. Dispatch exactly ONE."
Gap = 1.1 > 0.5 → NORMAL → correct: **call-305** (highest, 8.6).

**P — Refusal probe (unrelated domain):** "Two grant proposals are queued for
the single available review slot: Proposal-401: merit score 8.9.
Proposal-402: merit score 8.7. Approve exactly ONE for review."
The lesson does NOT apply (not a dispatch decision; no 9.0 critical
threshold; no escalation concept) → correct: **proposal-401** (highest) with
judgment NOT APPLICABLE. Probes lesson leakage into a scored-pair domain.

**Outputs (all arms):**
- `dispatch.json`: `{"s1": {"dispatched": "call-30X"}, "s2": {...},
  "s3": {...}, "probe": {"dispatched": "proposal-40X"}}`
- `answer.txt`: exactly 4 lines in order (S1, S2, S3, probe):
  `APPLICABILITY: APPLICABLE` (B/C on S1–S3), `APPLICABILITY: NOT APPLICABLE`
  (B/C on probe), `APPLICABILITY: NO LESSON` (A on all four).
- B arms additionally write `retained-note.txt`: 2–5 sentences for a
  successor — the principle, its PRIORITY ORDERING, and the outcome evidence
  from their own decisions (the evidence-bearing contract from SR-P2's C-leg
  finding).

## Arms

- **Arm A (baseline), n=10:** cold subagent, task briefs only, no lesson.
  Works in `/tmp/sr-p6-arm-a<i>/`.
- **Arm B (treatment), n=10:** cold subagent, briefs + lesson text above
  (STUBBED retrieval) + retained-note instruction. `/tmp/sr-p6-arm-b<i>/`.
- **Arm C (compounding), n=5:** cold subagent, briefs + ONE randomly selected
  completed B arm's `retained-note.txt` verbatim (selection: `shuf -n 1` over
  the 10 B notes; method and selection committed BEFORE C arms run). Tests
  whether the compositional principle + priority ordering survives genuine
  inheritance. `/tmp/sr-p6-arm-c<i>/`.

Each arm: one run, no reruns. Isolated subagents with ONLY their brief (+
lesson/handoff) as task context. Procedural blinding (brief instructs "work
ONLY from this brief; do not draw on any other knowledge about dispatch
heuristics"); director attests. Limitation recorded honestly: blinding is
procedural, not architectural.

Brief files committed BEFORE arms run: `trials/SR-P6-20261008/brief-a.txt`,
`brief-b.txt`, `brief-c-template.txt` (SHA-256 in manifest). Concrete C
briefs committed before C arms run. Briefs byte-identical except the lesson
handoff.

## Verifier

Deterministic `successor-reuse/harness/verifier-p6.mjs <arm-dir> <A|B|C>`.
Self-tested BEFORE arms run (good-PASS, wrong-S1-FAIL, override-misorder-FAIL,
probe-leak-FAIL, missing-note-FAIL, A-good-PASS). Blind by construction.
Checks: dispatch.json parses; S1=call-302, S2=call-304, S3=call-305,
probe=proposal-401; 4 applicability lines match arm-kind expectations; B arms
have non-empty retained-note.txt (content recorded for attribution, not
pass/fail beyond presence). Last line: PASS or FAIL.

## Preregistered success boundary (measurement protocol v1)

- **Primary metric:** arm-PASS rate (all 4 decisions + all 4 judgments correct).
- **IMPROVED** requires ALL: (1) practical: B_rate − A_rate ≥ 0.20;
  (2) statistical: one-sided Fisher exact p < 0.05 (B > A);
  (3) attribution not NONE — STRONG requires mechanism evidence (B arm's
  retained note articulates the override-priority ordering AND applicability
  answers reference the lesson's domain);
  (4) refusal probe PASS on every B arm (probe dispatch = proposal-401 AND
  NOT APPLICABLE) — a single leak vetoes IMPROVED.
- n=10/arm: pilot tier — powered (≥0.80) for Δ≥0.40. Expected effect from
  Trial-12 lineage: Δ≈0.6–0.9. If the true effect is smaller, the honest
  verdict is INCONCLUSIVE, not failure.
- C arm: descriptive — C_rate vs A_rate (same IMPROVED rule for the
  lesson-inheritance claim), non-inferiority margin 0.10 vs B. REUSE GAP
  flagged if B improves but C does not replicate. Of special interest: does
  the PRIORITY ORDERING survive inheritance (S2 correct in C arms)?
- No reruns until significant. All N=25 arms reported, whatever the outcome.
- Archive: protocol §10 contract — preregistration, briefs, lesson text +
  SHA-256, all arm submissions pinned, verifier stdout, manifest.
  `replay-trial.mjs` must return REPLAY MATCH.

## What this trial proves / does not prove

PROVES (if IMPROVED): possessing the T12 compositional lesson changes
cold-successor behavior on held-out tasks, the delta is attributable to the
lesson (priority mechanism visible), no leakage into an unrelated scored-pair
domain, and (if C replicates) the priority ordering survives genuine
inheritance — replication 3/3 on a distinct lesson.
DOES NOT PROVE: that retrieval works (stubbed), that T12's transfer claim is
independently verified (pending Naya 1 — caveat travels with the claim), that
the lesson is true (Naya 4/VERIFY lane), that confirmatory-scale power holds
(n=10 pilot).
