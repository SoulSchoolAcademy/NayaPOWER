# NayaNET — ACTIVITY

**BLUEPRINT STATUS:** VERIFIED
**BLUEPRINT VERSION:** V2 — 2026-09-18
**ROLE:** Human-facing projection of canonical operational events and meaningful system activity.

## 1. WHAT IT IS
Human-facing projection of canonical operational events and meaningful system activity.

## 2. PRIMARY JOB
Show what actually happened, when, by whom, with links to evidence and resulting state; never become the canonical event store.

## 3. SYSTEM BOUNDARY
Inputs: canonical event substrate and verified execution/evidence. Outputs: Activity projections by main system, project and Hub context.

## 4. HUMAN EXPERIENCE / PRESENTATION
Chronological/time-aware, filterable by project/subproject/type/status, with clear distinction between event, intelligence, verification and next action.

## 5. CONNECTIONS
Connects Execution, Events, PIS, Notes, Hub, Reports, Today and continuity/handoff.

## 6. 01–58 DEEP-DIVE SOURCES
This blueprint is distilled from the corresponding NayaPOWER 01–58 intelligence/contracts and the current repository implementation. Relevant 01–58 areas: **Connects Execution, Events, PIS, Notes, Hub, Reports, Today and continuity/handoff.**.

## 7. ENGINEERING RULES
- Inspect current repository/runtime before changing implementation.
- Reuse canonical NayaPOWER primitives; do not create a competing store, event system, memory system, queue, or authority system.
- Preserve stable identity, timestamps, provenance, privacy and truth state.
- Separate **canonical source → event → projection → presentation → interaction**.
- Capability never creates authority.
- Activity is a projection; Smart Notes are intelligence; the Hub is presentation; the Ledger is evidence/integrity.
- Unknown remains UNKNOWN. Documentation is not runtime proof.
- Builder ≠ Judge: the implementer does not certify its own work.
- Preserve valuable existing Hub behavior and evolve surgically unless evidence requires reconstruction.

## 8. ACCEPTANCE CONTRACT
A production-ready implementation must demonstrate:
1. Real source/data ownership is identified.
2. The feature has a single clear boundary and does not duplicate another system.
3. Identity, permissions and visibility are enforced at the appropriate boundary.
4. Timestamps and stable IDs survive every projection.
5. The human can understand what the feature is, why it exists, and what action is available.
6. Actions are real, not decorative.
7. Failure is visible and recoverable.
8. Source → execution → observed behavior → verification is proven.
9. Evidence and the next action are recorded.
10. A cold Naya can continue without conversational archaeology.

## 9. CURRENT GAP
**8,15,28,39,43,44,45,49,54,57,58**

## 10. ONE NEXT ACTION
**8,15,28,39,43,44,45,49,54,57,58**

## 11. SYSTEM POSITION
NayaNET is one connected product, not 19 independent applications:

**NayaPOWER → canonical intelligence/events/state → NayaNET Intelligent Hub → human/Naya action → verified outcome → new intelligence → continuation.**

This area is therefore a **capability/view within that system**, not an independent authority or database.

## 12. DO NOT BUILD
- A second source of truth.
- A parallel event store.
- A parallel Smart Note or memory system.
- A new authority ladder.
- A feature that only looks complete in the UI.
- A duplicate copy of canonical intelligence merely for presentation.

## 13. DEFINITION OF DONE
**IMPLEMENTED → TESTED → OBSERVED → INDEPENDENTLY VERIFIED → CONNECTED → RECORDED → STATE UPDATED → SUCCESSOR READY.**

Where the area is human-facing, add **LIVE VERIFIED** before calling the runtime complete.
