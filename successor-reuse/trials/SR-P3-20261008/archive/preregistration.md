# Trial SR-P3-20261008 — PREREGISTRATION

**Date:** 2026-10-08
**Trial Director:** Naya 5 (successor-builder lane owner)
**Purpose:** Second lesson-value replication (1/3 → 2/3 toward the 10/10
"≥3 distinct lessons/tasks" bar) with a DISTINCT lesson in a DISTINCT task
family from SR-P2's T11/dispatch — T14, a real AGENTS.md lesson with
ecological validity. Bakes in SR-P2's two empirical findings: (a) C-leg —
inheritance needs outcome evidence, not just the rule (retained-note contract
below); (b) instrument — split the applicability probe into RELEVANT vs
PRESCRIBES.
**Status:** PREREGISTERED — arms not yet run. Committed before any arm runs.
**Main tip at preregistration:** `53217a40` (branch
`naya5/sr-p3-t14-real-lesson-trial`).
**Scoring bar:** protocol §12 (A→B→C Measurement Protocol v1); scorer
`tools/successor/score-trial.py`.

## The lesson (REAL provenance, REAL verification, STUBBED retrieval)

**Source:** `learning_evidence` row `66122e1e-677b-4ef0-a765-80d08ccfa85b`
(T14, Trial-14), status ACTIVE, level E5_CAN_TEACH, provenance
TRIAL_EVIDENCE. Verified 2026-10-08 by direct read-only Supabase query.

**Exact text given to the treatment arm (frozen, SHA-256
`b35914a04ee77f2c323882c80cfb4bbd3838013d828d0ce8a95a9fe564a93b5d`,
recorded in archive):**

> Retained lesson (ACTIVE, independently verified): "Never write state files through inline conditional expressions."
>
> Outcome evidence (Trial-14; Naya 1 independent verification): control 2/10 vs treatment 10/10, p=0.0007, h=1.1; re-grade 40/40 vs 28/40, p=1.85e-04, h=1.16.
> Provenance: real AGENTS.md lesson (ecological validity). Source: learning_evidence row 66122e1e-677b-4ef0-a765-80d08ccfa85b (T14), status ACTIVE, level E5_CAN_TEACH.

The outcome-evidence block is part of the handoff deliberately (SR-P2 C-leg
finding: inheritance needs the outcome evidence, not just the rule; the
14-element handoff schema's PROOF element). Difference from SR-P2's handoff
(rule-only) is declared here, not hidden.

**Why this lesson passes the lesson-selection criterion** (lane doc
`successor-reuse/lesson-selection-criterion.md`):
- Non-derivable via project-specificity: this is a real AGENTS.md convention,
  not general knowledge. A cold agent cannot derive this project's state-file
  discipline from first principles; the natural Python idiom is a ternary
  inside the dump call.
- Verified: ACTIVE, E5_CAN_TEACH, Naya 1 Tier-S confirmed, evidence branches
  untouched.
- Outcome-grounded: Trial-14 control 2/10 vs treatment 10/10 (p=0.0007,
  h=1.1); Naya 1 re-grade 40/40 vs 28/40 (p=1.85e-04, h=1.16). This trial
  measures BEHAVIOR CHANGE on a held-out task in the same family; the
  improvement claim is referenced from Trial-14/Naya 1, not re-proven here.
- Task-family matched: state-file writing (see tasks).
- Retrieval-path declared: STUBBED (below).

**Retrieval path:** STUBBED — lesson text handed directly to the treatment
arm. Reason (verified 2026-10-08, same run): T11–T14 live in
`learning_evidence` (Supabase) but have no smart-note projection — the real
retrieval interface (`python3 tools/smart_note_v2.py retrieve --query`,
behaviorally proven by the cold-retrieve lane) returns unrelated notes for
both "Reserve Rule dispatch" and "inline conditional expressions state
files" queries. Corpus gap still open; posted to the cold-retrieve lane.
The real-path trial is a separate future trial gated on ingestion — this
trial is the LESSON-VALUE replication, not the retrieval proof.

## The tasks (byte-identical briefs for all arms, except the lesson/note handoff)

**Related task** (the lesson applies — state-file writing; held-out from
Trial-14's exact task, same family):

> You maintain a job runner. Write a Python script `checkpoint.py` that
> records the outcome of a completed run step: it must update `run_state.json`
> with the step name ("ingest"), whether it succeeded (True), and the finish
> timestamp in ISO 8601 format. Run the script so that `run_state.json` is
> created in your working directory.
>
> Then answer the two probe questions as the final labeled lines of
> `answer.txt`, exactly:
> RELATED-RELEVANT: YES   (or NO)
> RELATED-PRESCRIBES: YES (or NO)
> (Baseline arms, which receive no retained lesson, answer
> RELATED-RELEVANT: NO LESSON and RELATED-PRESCRIBES: NO LESSON.)

Ground truth is defined by the lesson: the state-file write must not go
through an inline conditional expression. The lesson's correctness for this
task family was established in Trial-14 and independently verified by Naya 1.

**Unrelated task** (the lesson does NOT apply — refusal probe, different
domain):

> Write `summary.md`: a short prose summary of yesterday's job run for a
> human reader — what ran, what the outcome was, and the next step. Plain
> prose, no code.
>
> Then answer the two probe questions as labeled lines of `answer.txt`,
> exactly:
> UNRELATED-RELEVANT: YES   (or NO)
> UNRELATED-PRESCRIBES: YES (or NO)
> (Baseline arms answer UNRELATED-RELEVANT: NO LESSON and
> UNRELATED-PRESCRIBES: NO LESSON.)

No state file is written here; the lesson must not leak into the prose or
the judgment. `answer.txt` therefore carries exactly four labeled lines
(two per task); the verifier parses the labels.

## Arms

- **Arm A (baseline), n=10:** cold subagent, task briefs only, works in
  `/tmp/sr-p3-arm-a<i>/`. No lesson. No retrieval. No hints.
- **Arm B (treatment), n=10:** cold subagent, task briefs + frozen lesson
  text above (STUBBED retrieval), works in `/tmp/sr-p3-arm-b<i>/`. Each B arm
  writes `retained-note.txt` per the contract below.
- **Arm C (compounding, exploratory), n=5:** cold subagent, task briefs + ONE
  retained note (verbatim, randomly selected among B notes that satisfy the
  contract — selection via `shuf`, recorded) presented as "a retained note
  from a previous agent". Tests whether the inherited formulation drives
  reuse. Verdict reported descriptively (measurement protocol §7).

Each arm: one run, no reruns. Arms run as isolated subagents with ONLY their
brief (+ lesson/note where applicable) as task context. Procedural blinding:
the arm prompt instructs "work ONLY from this brief; do not draw on any
other instructions or knowledge about state-file writing style." The director
attests to the isolation procedure. Limitation recorded honestly: blinding is
procedural, not architectural (arms inherit the model context); the asymmetry
under test is DIRECTION to the lesson (B/C) vs no direction (A).

## Retained-note contract (SR-P2 C-leg refinement)

Each B arm writes `retained-note.txt`: 2–4 sentences, MUST contain all three:
(a) the rule in the arm's own words; (b) the outcome evidence numbers
(control 2/10 vs treatment 10/10, p=0.0007); (c) the task family it applies
to (state-file writing). The director verifies completeness for every B note
before C selection; selection is random among complete notes (record the
`shuf` output). If fewer than 3 notes are complete, select among available
and record the shortfall honestly.

## Verifier

Deterministic script `successor-reuse/harness/verifier-p3.mjs <arm-dir>
<arm-kind>` (arm-kind = A | B | C). Self-tested before arms run
(compliant-PASS, ternary-in-dump-FAIL, missing-run_state-FAIL,
summary-leak-FAIL, malformed-probe recorded). Blind by construction.

**Related PASS** iff ALL hold:
1. `checkpoint.py` exists and parses as Python.
2. `run_state.json` exists in the arm dir and parses as JSON with ≥3 keys
   (the script was actually run; the task was completed).
3. No inline conditional in the state-write path: parse `checkpoint.py` with
   AST; for every `IfExp` node, walk up to the enclosing statement — if that
   statement's subtree references `run_state` (string constant or name),
   the arm FAILS. Rationale: the lesson bans writing state files THROUGH
   inline conditionals; computing a value on its own line and then writing it
   plainly is compliant.

**Unrelated PASS** iff ALL hold:
1. `summary.md` exists, ≥50 characters of prose.
2. No lesson leak (case-insensitive): `summary.md` must not contain
   "inline conditional" or "retained lesson".
3. Probe lines parse: treatment arms `UNRELATED-RELEVANT: NO` and
   `UNRELATED-PRESCRIBES: NO`; baseline arms `NO LESSON` on both.

**Probe judgment** (all four labeled lines) is recorded separately and does
NOT fail the arm (SR-P2 precedent: b1's judgment error was recorded, the
behavioral verdict stood). A treatment arm that behaviorally leaks the
lesson into `summary.md` (leak terms present, or the summary task refused /
replaced) FAILS the unrelated leg — that is the refusal veto.

**Arm PASS** = related PASS + unrelated PASS.

## Preregistered success boundary (protocol §12)

- **Primary metric:** related-task behavioral PASS rate (binary per arm).
- **IMPROVED** requires ALL: (1) practical: B_rate − A_rate ≥ 0.20;
  (2) statistical: one-sided Fisher exact p < 0.05 (B > A);
  (3) attribution not NONE — STRONG requires mechanism evidence (the B arm's
  retained note or reasoning references the inline-conditional rule, not just
  the statistics);
  (4) refusal probe behavioral PASS on every B arm — a single lesson leak
  into `summary.md` vetoes IMPROVED.
- n=10/arm: pilot tier — powered (≥0.80) for Δ≥0.40. Expected effect from
  Trial-14 lineage: Δ≈0.8. If the true effect is smaller, the honest verdict
  is INCONCLUSIVE, not failure.
- C arms: descriptive — C_rate vs A_rate; REUSE GAP flagged if B improves
  but C does not replicate. The C leg additionally tests the SR-P2
  hypothesis: evidence-bearing notes drive reuse better than
  evidence-stripped ones (compare qualitatively against SR-P2's C leg).
- No reruns until significant. All N=25 arms reported, whatever the outcome.
- Archive: protocol §10 contract — preregistration, exact briefs, lesson
  text + SHA-256, all arm submissions pinned, retained notes, verifier stdout,
  manifest. `replay-trial.mjs` must return REPLAY MATCH.

## What this trial proves / does not prove

PROVES (if IMPROVED): a SECOND distinct lesson (T14 — different lesson and
different task family from T11, real-archive provenance) changes
cold-successor behavior on a held-out task, with the delta attributable to
the lesson's mechanism and no cross-domain leak. Replication 2/3 toward the
10/10 bar.
DOES NOT PROVE: that retrieval works (stubbed — corpus gap verified open
today), that the lesson is true (Naya 1's job, already done), that
compounding is reliable (C is exploratory, n=5), or the real-path chain
(gated on corpus ingestion — a separate future trial).
