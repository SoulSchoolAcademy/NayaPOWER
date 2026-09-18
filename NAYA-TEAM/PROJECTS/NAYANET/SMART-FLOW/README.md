# NayaNET — SMART FLOW

**STATUS:** PARTIAL  
**RECONCILED:** 2026-09-17

## Definition
Official NayaNET sub-project boundary for **SMART FLOW**.

## Current repository truth
Governed execution primitives are real: authorization, preflight, execution state, observation, verification, Activity receipt, and handoff. Complete human-facing Smart Flow is not live-proven as one journey.

## Canonical implementation / evidence
`.naya/runtime/canonical_event_store.py`; `.naya/runtime/execution_controller.py`; `.naya/runtime/universal_execution_gate.py`; control plane

## Dependencies
Depends on canonical NayaPOWER identity/authorization, intelligence/events, governance, evidence/verification, continuity, and Hub projection as applicable. No competing source of truth may be created.

## Activity
Activity here is a scoped projection of canonical NayaPOWER Main Activity. It is not a second event store.

## Evidence boundary
Repository evidence establishes implementation state only where stated. Live production behavior must be independently observed and verified. **PARTIAL** is the current reconciliation classification, not a universal production claim.

## Exactly one next action
> Connect the existing governed execution spine to one real Hub-facing Smart Flow journey and verify every boundary.

## Operating rule
**ONE EVENT → MANY USEFUL VIEWS → ONE TRUTH.**
