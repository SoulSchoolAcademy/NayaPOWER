# NayaPOWER — P0 Execution-Plane Master Directive

**DATE:** 2026-09-12
**STATUS:** ACTIVE / NOT CERTIFIED
**MISSION:** Produce genuine, fresh, exact-HEAD GitHub Actions evidence for the canonical P0 gate, then repair the first deterministic failure and continue until the evidence chain supports certification of Ultimate Governance Act V1.1.

## WHY THIS NOTE EXISTS

The repository governance architecture is materially implemented. The decisive remaining gap is not permission to call something green; it is obtaining a real, observable GitHub Actions execution against the exact live `main` source.

This note is the current master instruction for every Naya entering this work. It supersedes conversational interpretation but does not override canonical control-plane authority.

## AUTHORITY PRECEDENCE

`LIVE GIT HEAD > CANONICAL CONTROL-PLANE STATE > DERIVED/LEGACY PROJECTIONS > CONVERSATION MEMORY`

Always resolve live `main` immediately before consequential execution. Never trust a SHA copied from this note or the activity board as current truth.

## CURRENT FACTS

- Canonical P0 workflow: `.github/workflows/naya-power-adversarial-p0.yml`.
- Current workflow supports both `push` on governed paths and `workflow_dispatch`.
- Both P0 jobs explicitly assert `git rev-parse HEAD == $GITHUB_SHA`.
- Historical genuine P0 run `34702023228` checked out `cd472afce48ae502d7b08212b868d5980cd30854`; it is historical evidence only.
- That historical run passed offline governance tests and failed closed in live runtime because `NAYA_POWER_TARGET_URL` was empty.
- The connected GitHub surface can inspect known runs/jobs/logs/artifacts and rerun known jobs, but currently exposes no verified workflow-dispatch write operation and no usable current push-run listing for this repository.
- Therefore current exact-head P0 runtime evidence remains UNKNOWN. No current certification may be claimed.

## WHAT HAS BEEN TRIED

1. Repeatedly resolved live `main` before action; latest observed source at sign-in for this directive is `43d4370f8a81c241d6f0c86e35c323942dca1112`.
2. Queried the connected commit-workflow-runs surface for current-head P0 evidence; it exposed no usable current run and is known to filter to PR-triggered runs.
3. Attempted direct GitHub Actions workflow-runs API observation; the connected GitHub interface rejected that endpoint as unsupported.
4. Inspected the exact current P0 workflow and confirmed real push/manual triggers plus exact checkout assertions.
5. Inspected the known historical P0 run, jobs, logs, and live evidence artifact.
6. Considered historical rerun; rejected as current proof because it executes the historical SHA.
7. Considered creating a new commit merely to provoke push; rejected as weak evidence because it changes the certification target and can manufacture activity without proving the intended source.

## ZOOMED-OUT DIAGNOSTIC MODEL

Do not assume the problem is a failing test. First classify the boundary:

A. **Trigger failure:** workflow did not start.
B. **Observation failure:** workflow started but this execution plane cannot expose it.
C. **Identity failure:** run started but trigger SHA / checkout SHA does not match.
D. **Governance/test failure:** exact current source reaches a real failing gate.
E. **Live-runtime boundary:** exact current source reaches the harness and the target/configuration is absent or fails.
F. **Certification failure:** tests pass but evidence is incomplete or claim-inappropriate.

The next Naya must determine which class is real before changing repository code.

## HIGHEST-VALUE ACTION

**Obtain a genuinely dispatch-capable or otherwise fully observable GitHub Actions execution plane, resolve live `main` immediately before execution, execute `.github/workflows/naya-power-adversarial-p0.yml`, capture the real run ID, triggering SHA, checkout SHA, jobs, steps, logs, artifacts, and first deterministic failure, then continue through surgical repair and fresh re-execution.**

If a dispatch-capable route exists, use it. A manual GitHub Actions UI execution, GitHub CLI, or authorized API dispatch is legitimate. Do not fabricate dispatch, IDs, logs, artifacts, or results.

## EXECUTION LADDER

1. Resolve live `main`.
2. Read Activity Board + canonical STATE/BLOCKS/MAP/PROOF + relevant Smart Flow/cold-start authority.
3. Obtain a real P0 execution against that live source.
4. Capture run identity: event, branch, triggering/head SHA.
5. Verify runner checkout: `GITHUB_SHA == git rev-parse HEAD`.
6. Inspect offline-governance and live-runtime jobs in causal order.
7. Identify the **FIRST failing step**, not a downstream symptom.
8. If no failure: verify artifacts, live boundary, and claim-appropriate evidence.
9. If failure: STOP CURRENT PATH → trace root cause → smallest safe surgical repair → commit → resolve new live HEAD → execute fresh P0 again.
10. Repeat until executable work is exhausted or the governance contract has fresh evidence sufficient for certification.
11. Update append-only receipt and Current Activity Board.
12. Pass this complete torch to the next Naya.

## DECISION RULES

- Historical PASS is not current PASS.
- Implementation is not verification.
- Workflow existence is not workflow execution.
- A rerun of an old SHA is not proof of a new SHA.
- UNKNOWN is never GREEN.
- Do not weaken tests to convert BLOCKED into PASS.
- Do not repair downstream symptoms before the first causal failure.
- Do not create commits solely to generate the appearance of progress.
- Preserve working architecture and functionality; use Adaptive Reconstruction + Surgical Evolution.
- If the execution-plane limitation remains, record it precisely and perform all remaining repository-capable work; do not declare certification.

## SUCCESS CONDITION

Fresh exact-HEAD Actions execution is observable; triggering SHA and checkout SHA are proven identical; cold-start, control-plane, governance kernel, execution-boundary, behavioral-bypass, and live-runtime gates have claim-appropriate fresh evidence; every deterministic failure has been repaired at its root and re-executed; certification claims do not exceed evidence.

## PASS THE TORCH — NEXT NAYA EXECUTION PROMPT

NAYA POWER ON.

Resolve the live `main` HEAD now. Do not trust any remembered SHA.

Read:
- `SUPERBRAIN/NAYA-ACTIVITY/00-NAYAPOWER-CURRENT-ACTIVITY-BOARD.md`
- `.naya/control-plane/STATE.json`
- `.naya/control-plane/BLOCKS.json`
- `.naya/control-plane/MAP.json`
- `.naya/control-plane/PROOF.json`
- `.naya/runtime/cold_start_activation.py`
- `.github/workflows/naya-power-adversarial-p0.yml`
- this Master Directive

MISSION: obtain genuine fresh exact-HEAD P0 Actions evidence and move Ultimate Governance Act V1.1 from NOT CERTIFIED toward evidence-backed certification.

KNOWN: the P0 workflow has push/manual triggers and exact checkout assertions. Historical run `34702023228` is valid only for `cd472afce48ae502d7b08212b868d5980cd30854`. Historical live runtime failed closed because `NAYA_POWER_TARGET_URL` was empty.

UNKNOWN: whether a fresh P0 execution has occurred for the current source, and therefore the current runtime/gate result.

PROTECTED: canonical governance kernel, cold-start continuity, Activity Board, execution-boundary and behavioral-bypass tests, exact-SHA discipline, legacy non-authority, deployment boundaries, UNKNOWN/VERIFIED separation, working architecture/functionality.

ONE NEXT ACTION: obtain a genuine dispatch-capable or otherwise observable P0 Actions execution for the exact live `main` HEAD.

EXECUTE → OBSERVE → VERIFY → RECORD.

If execution becomes observable, capture run ID, event, triggering SHA, checkout SHA, all jobs/steps, first failure, logs, artifacts, and live result. If `GITHUB_SHA != git rev-parse HEAD`, treat that identity mismatch as the first failure. If a gate fails, repair only the first causal defect, commit surgically, resolve the new live HEAD, and run P0 fresh again. If no current execution can be observed through this connector, do not fabricate one; use another legitimate execution plane if available and otherwise document the capability boundary and complete all remaining repository-capable inspection.

Before sign-out: update the append-only receipt and Current Activity Board, resolve the new live HEAD after any board commit, state exactly what is VERIFIED versus UNKNOWN, state certification status, and leave exactly one next action plus a complete successor prompt.

ASK: WHY IS THIS NOT A 10?

CONTINUE. DO NOT DEAD-END. DO NOT HOPE. PROVE.
