# Node Orchestrator

**The machine Naya 1 described:** "each completed stage emits a durable result, the next stage consumes that result, and failures become explicit, recoverable states. A saved note must not silently stop at the filing stage."

This is Naya 1's assembly-plan step 3, built against the wiring manifest (2026-10-09: 6/27 bindings, zero wired into production).

## What it is

A durable state machine that takes a committed capture and executes the nine-node pipeline against the REAL implementations — not specs, not mocks:

| Stage | Implementation executed |
|-------|------------------------|
| SELF | `kernel/self_node.py::SelfNode.cold_boot` (in-process) |
| LAW | `nayanet-law-runtime/law.ts::evaluateLaw` (node bridge) |
| ACT | `nayanet-act-runtime/act.ts::buildActPlan` (node bridge) |
| KNOW | `nayanet-know-runtime/know.ts::selectKnowContext` (node bridge) |
| PROVE | `nayanet-prove-runtime/prove.ts::assessKnowProof` (node bridge) |
| CONNECT | **NOT_IMPLEMENTED** — no implementation exists anywhere |
| VERIFY | `tools/learning_admission_gate.py::admit_candidate` — the pinned behavioral twin of the WO3 TS gate (38/38 fixtures verdict-identical). NOT reimplemented here. Production binds the TS gate endpoint once merged/deployed. |
| LEARN | `orchestrator/learn_node.py::LearnNode` (in-process) — the inheritance mechanism: admits VERIFY-passed lessons, freezes them with provenance, serves by intent to fresh decision contexts, records every serving |
| EVOLVE | **NOT_IMPLEMENTED** — no implementation exists anywhere |

## The laws it enforces

1. **Durable obligation.** `commit_capture()` derives the event ID deterministically from the capture — the same capture committed twice yields one event. Retries are safe; duplicates are impossible. The append-only JSONL log is the obligation.
2. **Stage results chain.** Every stage record carries the shared correlation ID. Each stage consumes the previous stages' recorded outputs.
3. **Resume, never redo.** Completed stages are skipped on resume. A stage left RUNNING by a crash is retried (stages must be idempotent — a recorded contract requirement).
4. **No silent PASS.** CONNECT/EVOLVE report NOT_IMPLEMENTED with named reasons. A run with missing stages is INCOMPLETE, never SUCCESS.
5. **Failures are explicit.** Stage errors become named FAILED states with the error captured; the run halts and resume retries the failed stage.
6. **Governed halts.** LAW BLOCKED → BLOCKED. LAW NEEDS_HUMAN_AUTHORIZATION → BLOCKED (protected gate). VERIFY rejected → REJECTED. These are rules, not errors.

## Queryable state

```python
orch = NodeOrchestrator(LocalExecutor(), store_root=".naya/orchestrator")
event_id = orch.commit_capture(lesson_id, capture_fingerprint)
record = orch.run(event_id, capture)          # execute or resume
orch.get_run(event_id)                        # full run record
orch.query(status="FAILED")                   # what's stuck
orch.runs.pending_stages(event_id)            # what's left
orch.runs.missing_stages(event_id)            # what's unimplemented
```

Run records live at `.naya/orchestrator/runs/<event_id>.json` (atomic writes). Events at `.naya/orchestrator/events.jsonl` (append-only).

## Production executor

`HttpExecutor` binds each stage to its edge-function endpoint (`PRODUCTION_ENDPOINTS`). It is defined and reviewable but NOT live-proven by this package's tests — live invocation needs deployed functions + credentials (the wiring manifest records deployed versions as GAP/STALE; deploys are Shawn's protected gate).

## Proof

`tests/test_node_orchestrator.py` (8 tests):
- Event obligation is idempotent.
- Seven implemented stages execute in order with chained correlation IDs.
- Kill-and-resume: completed stages are never re-executed (execution counts asserted).
- Interrupted RUNNING stages retry exactly once.
- Missing stages are loud; the run is INCOMPLETE, never SUCCESS; no silent PASS.
- Stage failure → explicit FAILED with named error; resume recovers.
- VERIFY rejection → REJECTED (governed halt, not failure); downstream stages SKIPPED.
- Every stage has a defined contract.

`tests/test_learn_node.py` (12 tests) — the inheritance proof:
- Admit through the orchestrator → fresh LearnNode process (never saw the admission) inherits the lesson from the durable store.
- Fresh decision context (situation described, no lesson ID) → lesson served by intent overlap with full provenance; the serving is recorded.
- Unrelated situations get nothing (intent matching is real, not ID lookup).
- Smuggled candidates (no admission proof) are quarantined on load, never served.
- Rejected, NOT_VERIFIED, and non-VERIFY results are refused loudly at admit().
- Admit is idempotent; lessons are frozen with checksums (tampering detected); supersession retires old versions without rewriting history.
- LEARN fails closed (not silently) when the capture carries no lesson.

## What this does NOT prove

- Production HTTP invocation (needs deploy + credentials).
- CONNECT/EVOLVE behavior (nothing exists to execute).
- That a decision APPLIED a served lesson (WO4/WO5b territory — LEARN records the serving; the application proof is downstream).
- Semantic understanding (intent matching is structured keyword/domain overlap, honestly bounded).
