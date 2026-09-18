# NayaNET — ACTIVITY

**STATUS:** VERIFIED  
**RECONCILED:** 2026-09-17

## Definition
Official NayaNET sub-project boundary for **ACTIVITY**.

## Current repository truth
Canonical events, completion-boundary Activity emission, execution binding, receipts, continuity, and projection checks are implemented. Current production proof remains separate.

## Canonical implementation / evidence
`.naya/runtime/canonical_event_store.py`; `.naya/runtime/execution_controller.py`; `.naya/runtime/activity_event.py`; `.naya/memory/events`

## Dependencies
Depends on canonical NayaPOWER identity/authorization, intelligence/events, governance, evidence/verification, continuity, and Hub projection as applicable. No competing source of truth may be created.

## Activity
Activity here is a scoped projection of canonical NayaPOWER Main Activity. It is not a second event store.

## Evidence boundary
Repository evidence establishes implementation state only where stated. Live production behavior must be independently observed and verified. **VERIFIED** is the current reconciliation classification, not a universal production claim.

## Exactly one next action
> Run fresh current-HEAD execution → automatic Activity → verification → handoff proof.

## Operating rule
**ONE EVENT → MANY USEFUL VIEWS → ONE TRUTH.**
