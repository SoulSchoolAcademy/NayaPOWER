# Naya Power Runtime

## Purpose

This directory is the first executable layer for the canonical Naya Power operating model:

`RESTORE → UNDERSTAND → LEAD → AUTHORIZE → EXECUTE → VERIFY → SCORE → OSCAR → IMPROVE → UPDATE STATE → CONTINUE`

It turns Mission State, Lead Mode, verification boundaries, quality promotion, host execution, and continuity from documentation into a machine-checkable runtime contract.

## Components

- `naya_power_runtime.py` — constitutional decision kernel: Mission State, evidence states, candidate eligibility, next-action ranking, result recording, cold start, and activation checks.
- `mission_state_store.py` — atomic JSON persistence and Lead Mode orchestration around the kernel.
- `quality_gate.py` — post-execution Scorecard + OSCAR promotion gate. A score cannot override a hard constitutional or evidence failure.
- `host_executor.py` — Host Executor Bridge. It closes the operational loop by restoring state, selecting one authorized action, invoking an explicitly supplied executor, requiring an ExecutionReceipt, applying Scorecard + OSCAR, persisting state, and returning the next action.
- `test_naya_power_runtime.py` — core conformance tests.
- `test_mission_state_store.py` — persistence/orchestration tests.
- `test_quality_gate.py` — scorecard/OSCAR promotion tests.
- `test_host_executor.py` — closed-loop bridge tests, including human/external handoff behavior.

## Deliberate boundary

The runtime does **not** grant authority or invent arbitrary tool access. It determines the highest-value authorized next action and hands that action to an executor explicitly supplied by the host. The executor must return observed evidence. Human-required actions become a handoff rather than being bypassed.

That preserves:

`CAPABILITY ≠ AUTHORITY`

`HUMAN AUTHORITY > RUNTIME AUTONOMY`

and:

`SOURCE INTENT ≠ RUNTIME TRUTH`

## Host integration contract

A host agent should:

1. Load Mission State through `MissionStateStore`.
2. Restore the operational context with `LeadModeEngine.restore()`.
3. Generate candidate actions from current mission state, source-of-truth material, available tools, dependencies, and authority boundaries.
4. Call the bridge's `cycle()` to restore, choose, and execute one action.
5. Execute the selected action through the host's already-authorized executor.
6. Observe the actual result independently.
7. Return an `ExecutionReceipt` with the evidence state and exact observation.
8. Let the bridge persist the result.
9. Run Scorecard + OSCAR and apply the promotion gate.
10. Continue automatically when promoted; repair blocking defects when not promoted.
11. Stop and surface a human/external handoff when no eligible authorized action exists.

## Copy-paste continuation model

Naya Power execution mode is designed so the human does not need to invent the next prompt. At the end of an execution cycle, the host/UI should render a concise copy-paste continuation prompt derived from persisted Mission State. The prompt is a control-transfer convenience, not a second source of truth; Mission State remains authoritative.

## Verification

The repository CI workflow is:

`.github/workflows/naya-power-runtime-tests.yml`

It runs the complete runtime conformance suite on pushes to `main` and via manual dispatch.
