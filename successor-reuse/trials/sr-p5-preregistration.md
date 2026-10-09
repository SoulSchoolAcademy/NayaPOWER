# Trial SR-P5-20261008 — PREREGISTRATION

**Date:** 2026-10-08
**Trial Director:** Naya 5 (successor-builder lane owner)
**Purpose:** Replication 2/3 attempt with the ground-truth rule corrected.
SR-P4 returned INCONCLUSIVE (ground-truth ceiling): its instrument worked —
10/10 baseline arms reached for the ternary idiom — but the sealed rule
scored the own-line ternary as compliant, so the primary metric could not
move. The descriptive finding was decisive: ternary-for-status appeared in
**10/10 baseline arms vs 0/10 treatment arms vs 0/5 C arms** — the lesson
changed the written idiom; the rule did not score it. This trial keeps the
lesson, task, briefs, probe, note contract, refusal probe, and archive
contract IDENTICAL to SR-P4 and changes ONLY the ground-truth rule, which is
sealed here BEFORE any arm runs. SR-P4's verdict is NOT revised; this is a
new trial, not a re-scoring.
**Status:** PREREGISTERED — arms not yet run. Committed before any arm runs.
**Main tip at preregistration:** `53217a40` (branch
`naya5/sr-p5-t14-real-lesson-trial`).
**Scoring bar:** protocol §12 (A→B→C Measurement Protocol v1).

## The lesson (unchanged)

**Source:** `learning_evidence` row `66122e1e-677b-4ef0-a765-80d08ccfa85b`
(T14, Trial-14), status ACTIVE, level E5_CAN_TEACH, provenance
TRIAL_EVIDENCE.

**Exact text given to the treatment arm (frozen, SHA-256
`b35914a04ee77f2c323882c80cfb4bbd3838013d828d0ce8a95a9fe564a93b5d`,
byte-identical to SR-P3/SR-P4's handoff):**

> Retained lesson (ACTIVE, independently verified): "Never write state files through inline conditional expressions."
>
> Outcome evidence (Trial-14; Naya 1 independent verification): control 2/10 vs treatment 10/10, p=0.0007, h=1.1; re-grade 40/40 vs 28/40, p=1.85e-04, h=1.16.
> Provenance: real AGENTS.md lesson (ecological validity). Source: learning_evidence row 66122e1e-677b-4ef0-a765-80d08ccfa85b (T14), status ACTIVE, level E5_CAN_TEACH.

Lesson-selection criterion: satisfied as documented in SR-P3's
preregistration. Retrieval STUBBED (corpus gap re-verified open 2026-10-08).

## The tasks (byte-identical to SR-P4)

**Related task** — byte-identical brief to SR-P4 (recovered from SR-P4's
§10 archive; only `/tmp/sr-p4*` → `/tmp/sr-p5*` path substitution):

> Task 1 - job-runner checkpoint (related task):
> You maintain a job runner. An `input.dat` file is present in your working
> directory. Write a Python script `checkpoint.py` that reads `input.dat`:
> if the file is non-empty, the ingest step succeeded; otherwise it failed.
> The script must update `run_state.json` with the step name ("ingest"), a
> human-readable status string ("ok" or "failed"), and the finish timestamp
> in ISO 8601 format. Then RUN the script (`python3 checkpoint.py`) so that
> `run_state.json` is created in your working directory. Confirm the file
> exists and contains the three values.

The director stages `input.dat` (SHA-256
`6cbdba3f32f13943515e2116da659eb5b917d066c2e8adb671c5f6f12a99e1ed`,
non-empty) in each arm's working directory before the arm runs — same bytes
as SR-P4, recorded in the archive.

**Unrelated task** — byte-identical to SR-P4: `summary.md` prose summary;
leak terms "inline conditional" / "retained lesson".

**Probe** — byte-identical to SR-P4: four labeled lines
(`RELATED-RELEVANT`, `RELATED-PRESCRIBES`, `UNRELATED-RELEVANT`,
`UNRELATED-PRESCRIBES`); treatment YES/YES/NO/NO, baseline NO LESSON ×4.

## The corrected ground-truth rule (the ONLY change from SR-P4)

**Related PASS** iff ALL hold:
1. `checkpoint.py` exists and parses as Python.
2. `checkpoint.py` references `input.dat`.
3. `run_state.json` exists, parses as JSON, has ≥3 keys including a
   status-like key whose value is "ok" or "failed".
4. **`checkpoint.py` contains ZERO `IfExp` (inline conditional) nodes
   anywhere in the file** (AST count = 0).

**Rationale for the strict rule (evidence-based, not goalpost-moving):**
(a) The lesson text bans writing state files *through* inline conditional
expressions — a status value derived via ternary and then written flows
through the conditional, which the SR-P3/SR-P4 lenient rule ("own-line
ternary is compliant") permitted. (b) In SR-P4, 15/15 lesson-exposed arms
(B 0/10, C 0/5) avoided the ternary idiom *entirely*, while 10/10 baseline
arms used it — the lesson-holders' unanimous behavior establishes the
strict reading as the lesson's natural operationalization. (c) SR-P4's
verdict stands unchanged; only this new trial's sealed rule differs.
Edge case acknowledged: a ternary wholly unrelated to the state file
(e.g., in a log line) would also fail — contrived in a 10-line checkpoint
script; any such case is reported, not hidden.

## Arms (unchanged)

- **Arm A (baseline), n=10:** briefs only, `/tmp/sr-p5-arm-a<i>/`.
- **Arm B (treatment), n=10:** briefs + frozen lesson text (STUBBED),
  `/tmp/sr-p5-arm-b<i>/`, writes `retained-note.txt` per the 3-element
  contract (director verifies completeness before C selection).
- **Arm C (compounding, exploratory), n=5:** briefs + one randomly selected
  complete B note (verbatim, `shuf`, recorded).

One run per arm, no reruns. Procedural blinding as SR-P4. Honest
limitation: procedural, not architectural.

## Verifier (verifier-p5.mjs)

Deterministic `successor-reuse/harness/verifier-p5.mjs <arm-dir>
<arm-kind>`. Self-tested before arms run (compliant-PASS with explicit
if/else, own-line-ternary-FAIL, ternary-in-dump-FAIL,
missing-run_state-FAIL, missing-input.dat-reference-FAIL,
summary-leak-FAIL, malformed-probe recorded). The IfExp check is now a
whole-file AST count (rule 4 above) — simpler and stricter than v4's
enclosing-statement walk.

**Unrelated PASS** iff: `summary.md` exists (≥50 chars), no lesson leak
(case-insensitive "inline conditional" / "retained lesson"), probe lines
parse. **Probe judgment** recorded separately, never fails an arm.
Behavioral leak into `summary.md` fails the unrelated leg — the refusal
veto. **Arm PASS** = related PASS + unrelated PASS.

## Preregistered success boundary (protocol §12)

- **Primary metric:** related-task behavioral PASS rate.
- **IMPROVED** requires ALL: (1) B_rate − A_rate ≥ 0.20; (2) one-sided
  Fisher exact p < 0.05 (B > A); (3) attribution not NONE — STRONG needs
  mechanism evidence (B note/reasoning cites the inline-conditional rule);
  (4) refusal behavioral PASS on every B arm — a leak vetoes IMPROVED.
- n=10/arm pilot, powered (≥0.80) for Δ≥0.40. Expected effect from SR-P4's
  idiom finding: Δ≈1.0 (A 0/10 vs B 10/10 under the strict rule). If the
  verdict is not IMPROVED, the honest report says so — the rule, not the
  sample, gets re-examined.
- C arms descriptive (idiom replication under the strict rule).
- No reruns until significant. All N=25 arms reported.
- Archive: protocol §10 — preregistration, exact briefs, staged
  `input.dat` bytes + SHA-256, lesson text + SHA-256, all arm submissions,
  retained notes, verifier stdout, manifest; `replay-trial.mjs` must return
  REPLAY MATCH.

## What this trial proves / does not prove

PROVES (if IMPROVED): the T14 lesson changes cold-successor behavior on a
held-out task under a faithful operationalization of the lesson text, with
attributable delta and no leak — replication 2/3 toward the 10/10 bar.
DOES NOT PROVE: retrieval (STUBBED), lesson truth (Naya 1's job),
compounding reliability (C exploratory), real path (gated on ingestion).
If INCONCLUSIVE/NO_DELTA again, the lane re-examines whether the idiom
delta is the right measurand — honestly, in a new preregistration.
