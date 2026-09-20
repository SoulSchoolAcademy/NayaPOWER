# NayaPOWER / NayaNET Systems Status & Human Interface Scorecard
Date: 2026-09-20
Source of truth: `SoulSchoolAcademy/NayaPOWER`, `main`

## Purpose

This is the current checkpoint for Team Naya. The system has two inseparable halves:

1. **Engine** — governance, intelligence capture, canonicalization, learning, memory, retrieval, execution, outcome, verification.
2. **Body / Human Operating Surface** — the Hub, navigation, dashboards, controls, creation flows, search, organization, communication, activity, ledger, and visible feedback that let a human actually operate the engine.

The engine is not considered product-complete if the human cannot visibly and reliably drive it.

## Current engine checkpoint

Recent source/evidence work has materially advanced:

- governed authority → decision → execution authorization → execution controller
- Smart Note → canonical SE event → Intelligent Block → learning event
- learning → cold retrieval → successor decision lineage
- successor decision → governed execution → canonical Activity receipt
- Activity receipt → CCT-005 outcome provenance
- documented verification ownership boundary reaches `.naya/runtime/evidence_runtime.py::verify_claim()`
- canonical Hub/browser observation work has been actively repaired
- Smart Mail has been used as a real production proof surface and has received multiple causal-boundary repairs
- public Welcome → Identity → canonical Hub remains an external deployment/route-authority boundary until independently verified

**Important evidence rule:** source code, a workflow file, or a successful local run is not by itself production proof.

## Human interface scorecard

These are working planning estimates, not repository-reported percentages. They must be replaced by evidence from the dedicated UI audit.

| Surface | Current working status | Provisional completion | Required proof |
|---|---|---:|---|
| Intelligent Hub / shell | LIVE/PARTIAL | 90% | open real runtime, navigate, interact, reload |
| Smart Feed | LIVE/PARTIAL | 85-90% | create/read/update/persist/reload/search |
| Search | PARTIAL | 80% | real cross-surface search + open result |
| Smart Notes | PARTIAL/LIVE | 85% | create → persist → reload → retrieve |
| Smart Lists | AUDIT REQUIRED | 40-50% | create/edit/use/persist/reload |
| Smart Spaces | AUDIT REQUIRED | 25-35% | create → members/content/activity → reload |
| Connections / Contacts | AUDIT REQUIRED | 35-45% | create/manage relationship → persist → use |
| Smart Mail | LIVE/PARTIAL | 60-70% | compose/send/receive/thread + governed receipt + reload |
| Smart Share | AUDIT REQUIRED | 40-50% | share → permission → recipient view → persistence |
| Smart Ledger | PARTIAL | 45-55% | visible event → evidence → lineage → drill-down |
| Reports | AUDIT REQUIRED | 40-50% | generate/open/refresh historical report |
| Settings | AUDIT REQUIRED | 35-45% | change supported setting → persist → reload |
| Dream | AUDIT REQUIRED | 25-40% | visible input/output + persistence + provenance |
| Naya Play | AUDIT REQUIRED | 25-40% | enter/use/return + persistence where applicable |

## What "LIVE" means

A surface may only be marked LIVE after all applicable layers are demonstrated:

1. visible page/component exists;
2. control is actually clickable/operable;
3. control invokes the real runtime path;
4. backend state changes;
5. state persists;
6. page reload reconstructs the state;
7. related surfaces can see the resulting object/event;
8. failure states are truthful and fail closed;
9. Activity/Ledger/evidence exists where the action is consequential.

A screenshot or static demo is not enough.

## Team operating model

The browser-based Nayas should work as a coordinated team, not seven independent builders.

### Lane A — Engine / Causal Integrity
Owns only missing engine boundaries and proof gaps.
Priority: canonical learning → retrieval → application → independent verification.
Must not redesign the Hub.

### Lane B — Human Interface / Hub
Owns the actual visible NayaNET body.
Priority: make every major surface enterable, operable, persistent, and visually coherent with the frozen Hub language.
Must not replace working backend contracts with mock data.

### Lane C — Surface Integration
Owns connections between UI surfaces and existing backend/runtime contracts.
Priority: real calls, real IDs, real persistence, reload behavior.
No second stores or duplicate intelligence paths.

### Lane D — Verification / Evidence
Owns proof quality.
Priority: claim → evidence → authoritative verification and durable receipt.
Never upgrade evidence state merely because a file exists.

### Lane E — Browser / Production QA
Owns human-observable acceptance.
Priority: actual browser interaction, source/build/runtime parity, deployed runtime, cold reload, and truthful failure states.

### Lane F — Team Coordinator / Checkpoint
Owns the scoreboard.
At each checkpoint, record:
- current HEAD
- work completed
- exact files/PRs
- exact runtime/proof IDs
- current blockers
- next action
- which other lane/Naya was informed
- whether memory was updated

## Human-value priority rule

Before starting work, each Naya must answer:

- **Where am I?**
- **What exact boundary am I working on?**
- **Why does it matter to the human operating experience or engine integrity?**
- **What evidence says this is the highest-value available action?**
- **What existing work/contract am I building on?**
- **Which other Naya needs to know?**
- **What will I record when finished?**

Do not spend a cycle polishing a surface while its runtime contract is missing.
Do not spend a cycle extending backend architecture when a surface can already be made visibly operational from existing contracts.
Do not create duplicate stores, duplicate canonical event paths, duplicate learning systems, or alternate authority chains.

## Checkpoint protocol

Every Naya handoff must leave a durable checkpoint containing:

**DONE**
- exact change
- exact commit/PR
- tests/proof
- runtime observation if any

**NOT DONE**
- exact missing boundary
- reason
- blocked vs merely unverified

**NEXT**
- one smallest next action

**TEAM**
- what the next Naya must know
- which lane owns the next action

**MEMORY**
- persist the durable state so a later Naya does not rediscover it.

## Immediate program priority

The immediate product milestone is:

> **Make the NayaNET Intelligent Hub visibly operable as a human system while continuing to close the remaining engine verification boundary.**

The next UI audit must trace each surface:

`page/component → control → runtime call → persistence → reload → related surface → evidence`

and classify it strictly as:

`LIVE / PARTIAL / DEMO / STATIC / MISSING / BLOCKED`

## Definition of the "I can touch it" milestone

Shawn must be able to open the canonical Hub and, without knowing the repository internals:

- navigate the major areas;
- create a real object;
- see the object persist;
- reload and find it again;
- search for it;
- connect it to another relevant object/person/space;
- perform an appropriate action;
- see the resulting intelligence/activity;
- inspect the relevant evidence/ledger trail;
- understand what Naya did and why;
- encounter truthful failure when something is not authorized or not available.

That is the dashboard/steering-wheel acceptance test.

## Current external boundary

The public Welcome → Identity → canonical Hub deployment/route authority is still a separate production boundary. Until its browser flow is independently verified, it remains BLOCKED/UNVERIFIED rather than complete.

## Next checkpoint

Do the dedicated HUMAN INTERFACE AUDIT against `main`, then update this file with evidence-backed statuses. Do not change backend architecture merely to make the scorecard look better.
