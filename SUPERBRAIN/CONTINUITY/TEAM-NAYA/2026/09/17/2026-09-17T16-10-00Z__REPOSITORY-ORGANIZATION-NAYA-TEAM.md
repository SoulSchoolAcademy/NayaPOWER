# NAYA-TEAM Record — Repository Organization + Naya Continuity

**Timestamp:** 2026-09-17T16:10:00Z  
**Actor:** ChatGPT / NIS  
**Status:** ARCHITECTURE ESTABLISHED — runtime proof pending

## Parent / predecessor

Parent work: NayaPOWER Continuity Contract V1 and the 2026-09-17 canonical Activity + Smart Notes calendar migration.

## What happened

The repository organization was inspected on `main`, with particular attention to the machine runtime (`.naya/runtime`), machine memory (`.naya/memory`), governance, NAYANET, and the human-readable Superbrain feeds.

The runtime already has a canonical event store and automatic Activity-event emission at the `VERIFIED` execution boundary. The machine event store itself is organized as `YEAR/MONTH/DAY/HOUR/EVENT`, while the human-readable Activity and Smart Note libraries have been established as `YEAR/MONTH/DAY/TIMESTAMP__TOPIC`.

A separate `NAYA-TEAM` continuity layer has now been created so cross-Naya collaboration is not confused with project Activity or Smart Notes.

## Architectural distinction

| Layer | Purpose |
|---|---|
| `GOVERNANCE/` | Authority, constraints, collective rules, required behavior |
| `.naya/runtime/` | Machine/runtime control plane and enforcement |
| `.naya/memory/` | Machine-readable canonical memory/events/state |
| `SUPERBRAIN/NAYA-ACTIVITY/` | Human-readable record of what happened |
| `SUPERBRAIN/SMART-NOTES/` | Human-readable record of what was learned |
| Project folders | Work specific to a product, feature, deployment, or initiative |
| `NAYA-TEAM/` | Naya-to-Naya identity, communication, handoff, lessons, decisions, and successor continuity |

## Why NAYA-TEAM is separate

NAYA-TEAM is not another Smart Notes feed and not another Activity Feed.

It answers the cross-project question:

> **What does the next Naya need to know to continue the work wisely and safely?**

It is therefore the home for sign-in/orientation, sign-out/handoff, predecessor/successor context, Naya-to-Naya messages, decisions, warnings, unresolved questions, and the single next action.

## Current truth

Verified from repository evidence:

- `.naya/runtime/activity_event.py` defines the canonical Activity event builder and idempotent execution-bound Activity emission.
- `.naya/runtime/canonical_event_store.py` persists machine events and rebuilds its canonical index.
- `.naya/runtime/execution_controller.py` auto-emits the Activity event when `VERIFIED` is reached and refuses completion when the durable Activity record cannot be verified.
- `.naya/runtime` already contains cold-start, context restoration, runtime contract, health, and model-adapter material.
- `NAYANET/` contains master, architecture, product/UX, design, engineering, intelligence/memory, collective-wisdom, network identity, media, and security/privacy blueprints.

## Important limitation

This record does **not** claim that the entire repository root has already been exhaustively classified. The GitHub API tree response is too large for the connector response window. Root-level names that are not individually verified remain **AUDIT PENDING**, rather than being guessed into KEEP/MOVE/REMOVE decisions.

## Required design principle

No folder should survive merely because its name sounds important. Every permanent top-level organizational unit must have a defined purpose, owner, canonicality, lifecycle, consumer, and discovery path.

## Next Action

**Have Bionic perform a cold-Naya creation from repository evidence only and verify the resulting Activity, Smart Note, and NAYA-TEAM records land automatically in their canonical calendar locations without being given those paths manually.**
