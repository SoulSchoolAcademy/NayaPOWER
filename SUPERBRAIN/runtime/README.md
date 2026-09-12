# Naya Power Runtime

## Purpose

This directory is the first executable layer for the canonical Naya Power operating model:

`RESTORE → UNDERSTAND → LEAD → EXECUTE → VERIFY → SCORE → OSCAR → IMPROVE → UPDATE STATE → CONTINUE`

It turns Mission State, Lead Mode, verification boundaries, quality promotion, and continuity from documentation into a machine-checkable runtime contract.

## Components

- `naya_power_runtime.py` — constitutional decision kernel: Mission State, evidence states, candidate eligibility, next-action ranking, result recording, cold start, and activation checks.
- `mission_state_store.py` — atomic JSON persistence and Lead Mode orchestration around the kernel.
- `quality_gate.py` — post-execution Scorecard + OSCAR promotion gate. A score cannot override a hard constitutional or evidence failure.
- `test_naya_power_runtime.py` — core conformance tests.
- `test_mission_state_store.py` — persistence/orchestration tests.
- `test_quality_gate.py` — scorecard/OSCAR promotion tests.

## Deliberate boundary

The runtime does **not** invent or silently execute arbitrary tools. It determines the highest-value authorized next action, hands that action to the existing execution/tool layer, then requires an observed result and evidence before promoting state.

That preserves the constitutional distinction:

`CAPABILITY ≠ AUTHORITY`

and the integrity rule:

`SOURCE INTENT ≠ RUNTIME TRUTH`

## Host integration contract

A host agent should:

1. Load Mission State through `MissionStateStore`.
2. Restore the operational context with `LeadModeEngine.restore()`.
3. Generate candidate actions from the current mission, source-of-truth material, available tools, dependencies, and authority boundaries.
4. Call `LeadModeEngine.choose(candidates)`.
5. Execute the selected action through the host's already-authorized tool layer.
6. Observe the actual result independently.
7. Create an `ExecutionReceipt` with the evidence state and exact observation.
8. Call `LeadModeEngine.accept_execution(plan, receipt)`.
9. Run `evaluate_quality(...)` with the scorecard and OSCAR review.
10. Apply the quality decision; repair blocking defects before promotion, otherwise continue with the derived `next_action`.

If no eligible action exists, the runtime stops pretending and reports the missing authority, evidence, dependency, or human decision required.

## Verification

The repository CI workflow is:

`.github/workflows/naya-power-runtime-tests.yml`

It runs the complete runtime conformance suite on pushes to `main` and via manual dispatch.
