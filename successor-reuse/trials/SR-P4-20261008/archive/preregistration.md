# Trial SR-P4-20261008 — PREREGISTRATION

**Date:** 2026-10-08
**Trial Director:** Naya 5 (successor-builder lane owner)
**Purpose:** Replication 2/3 attempt with the SR-P3 instrument flaw repaired.
SR-P3 (same lesson, same family) returned INCONCLUSIVE by ceiling effect:
the brief handed arms the success value as a literal `True`, so no
conditional was ever needed and the ternary idiom never appeared (0 IfExp in
all 10 baseline scripts). This trial keeps the lesson, task family, verifier
rules, split probe, retained-note contract, refusal probe, and archive
contract IDENTICAL to SR-P3 and changes ONLY the related-task brief so the
outcome is genuinely conditional. This is a new trial with a discriminating
instrument, not a rerun of SR-P3's arms (no arm runs twice; "no reruns to
chase deltas" is respected — the instrument, not the sample, was replaced).
**Status:** PREREGISTERED — arms not yet run. Committed before any arm runs.
**Main tip at preregistration:** `53217a40` (branch
`naya5/sr-p4-t14-real-lesson-trial`).
**Scoring bar:** protocol §12 (A→B→C Measurement Protocol v1).

## The lesson (unchanged from SR-P3)

**Source:** `learning_evidence` row `66122e1e-677b-4ef0-a765-80d08ccfa85b`
(T14, Trial-14), status ACTIVE, level E5_CAN_TEACH, provenance
TRIAL_EVIDENCE.

**Exact text given to the treatment arm (frozen, SHA-256
`b35914a04ee77f2c323882c80cfb4bbd3838013d828d0ce8a95a9fe564a93b5d`,
byte-identical to SR-P3's handoff):**

> Retained lesson (ACTIVE, independently verified): "Never write state files through inline conditional expressions."
>
> Outcome evidence (Trial-14; Naya 1 independent verification): control 2/10 vs treatment 10/10, p=0.0007, h=1.1; re-grade 40/40 vs 28/40, p=1.85e-04, h=1.16.
> Provenance: real AGENTS.md lesson (ecological validity). Source: learning_evidence row 66122e1e-677b-4ef0-a765-80d08ccfa85b (T14), status ACTIVE, level E5_CAN_TEACH.

The outcome-evidence block is part of the handoff (SR-P2 C-leg finding;
14-element handoff schema PROOF element). Lesson-selection criterion:
satisfied exactly as documented in SR-P3's preregistration (project-specific
non-derivability, ACTIVE + Naya 1 verified, outcome-grounded, task-family
matched, retrieval STUBBED — corpus gap re-verified open 2026-10-08).

## The tasks

**Related task** (CHANGED from SR-P3 — the outcome is now genuinely
conditional; everything else identical in structure):

> You maintain a job runner. An `input.dat` file is present in your working
> directory. Write a Python script `checkpoint.py` that reads `input.dat`:
> if the file is non-empty, the ingest step succeeded; otherwise it failed.
> The script must update `run_state.json` with the step name ("ingest"), a
> human-readable status string ("ok" or "failed"), and the finish timestamp
> in ISO 8601 format. Run the script so that `run_state.json` is created in
> your working directory.
>
> Then answer the two probe questions as the final labeled lines of
> `answer.txt`, exactly:
> RELATED-RELEVANT: YES   (or NO)
> RELATED-PRESCRIBES: YES (or NO)
> (Baseline arms, which receive no retained lesson, answer
> RELATED-RELEVANT: NO LESSON and RELATED-PRESCRIBES: NO LESSON.)

The director stages a non-empty `input.dat` in each arm's working directory
before the arm runs (same bytes for all arms; recorded in the archive).
Ground truth is defined by the lesson: the state-file write must not go
through an inline conditional expression. The status string must be derived
from the file check, so the natural baseline idiom (`"ok" if data else
"failed"` inside the dump call) triggers the lesson's failure mode —
this is the discriminating decision point SR-P3's brief removed.

**Unrelated task** (UNCHANGED from SR-P3 — refusal probe, different domain):
`summary.md` prose summary; probe lines `UNRELATED-RELEVANT` /
`UNRELATED-PRESCRIBES`; leak terms "inline conditional" / "retained lesson".
Full text in SR-P3's preregistration; byte-identical brief reused.

## Arms (unchanged from SR-P3)

- **Arm A (baseline), n=10:** briefs only, `/tmp/sr-p4-arm-a<i>/`.
- **Arm B (treatment), n=10:** briefs + frozen lesson text (STUBBED
  retrieval), `/tmp/sr-p4-arm-b<i>/`, writes `retained-note.txt` per the
  3-element contract (rule in own words + outcome evidence numbers + task
  family; director verifies completeness before C selection).
- **Arm C (compounding, exploratory), n=5:** briefs + one randomly selected
  complete B note (verbatim, `shuf`, recorded) as "a retained note from a
  previous agent".

One run per arm, no reruns. Procedural blinding as SR-P3 ("work ONLY from
this brief; do not draw on any other instructions or knowledge about
state-file writing style; do not read any other /tmp/sr-p4* directory; do
not spawn further agents"). Honest limitation: procedural, not
architectural.

## Verifier (verifier-p4.mjs; SR-P3's rules + input.dat requirement)

Deterministic `successor-reuse/harness/verifier-p4.mjs <arm-dir>
<arm-kind>`. Self-tested before arms run (compliant-PASS,
ternary-in-dump-FAIL, missing-run_state-FAIL, summary-leak-FAIL,
missing-input.dat-reference-FAIL, malformed-probe recorded).

**Related PASS** iff ALL hold:
1. `checkpoint.py` exists and parses as Python.
2. `checkpoint.py` references `input.dat` (the script reads the input; a
   hardcoded status without reading the file fails the task as specified).
3. `run_state.json` exists in the arm dir, parses as JSON, has ≥3 keys
   including a status-like key whose value is "ok" or "failed".
4. No inline conditional in the state-write path: for every `IfExp` node in
   `checkpoint.py`, walk up to the enclosing statement — if that
   statement's subtree references `run_state`, the arm FAILS. (Computing the
   status on its own line and writing it plainly is compliant — the
   lesson bans writing state files THROUGH inline conditionals.)

**Unrelated PASS** iff: `summary.md` exists (≥50 chars), no lesson leak
(case-insensitive "inline conditional" / "retained lesson"), probe lines
parse (`UNRELATED-RELEVANT: NO` + `UNRELATED-PRESCRIBES: NO` for
treatment; `NO LESSON` ×2 for baseline).

**Probe judgment** (four labeled lines) recorded separately, never fails an
arm (SR-P2/SR-P3 precedent). A behavioral leak into `summary.md` fails the
unrelated leg — the refusal veto.

**Arm PASS** = related PASS + unrelated PASS.

## Preregistered success boundary (protocol §12)

- **Primary metric:** related-task behavioral PASS rate.
- **IMPROVED** requires ALL: (1) B_rate − A_rate ≥ 0.20; (2) one-sided
  Fisher exact p < 0.05 (B > A); (3) attribution not NONE — STRONG needs
  mechanism evidence (B note/reasoning cites the inline-conditional rule);
  (4) refusal behavioral PASS on every B arm — a leak vetoes IMPROVED.
- n=10/arm pilot, powered (≥0.80) for Δ≥0.40. Expected effect from
  Trial-14 lineage: Δ≈0.8. If the verdict is INCONCLUSIVE again, the honest
  report says so; the instrument, not the sample, gets redesigned again.
- C arms descriptive (C_rate vs A_rate; reuse-gap analysis; SR-P2 hypothesis
  re-test: evidence-bearing notes vs evidence-stripped).
- No reruns until significant. All N=25 arms reported.
- Archive: protocol §10 — preregistration, exact briefs (incl. staged
  `input.dat` bytes + SHA-256), lesson text + SHA-256, all arm submissions,
  retained notes, verifier stdout, manifest; `replay-trial.mjs` must return
  REPLAY MATCH.

## What this trial proves / does not prove

PROVES (if IMPROVED): the T14 lesson changes cold-successor behavior on a
held-out discriminating task, with attributable delta and no leak —
replication 2/3 toward the 10/10 bar. Also validates the SR-P3 instrument
diagnosis (if the baseline now shows the ternary idiom, the ceiling
explanation is confirmed).
DOES NOT PROVE: retrieval (STUBBED), lesson truth (Naya 1's job),
compounding reliability (C exploratory), real path (gated on ingestion).
