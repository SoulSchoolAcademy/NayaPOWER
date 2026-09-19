# NayaNET Engineering System

**Purpose:** canonical engineering map for NayaNET capabilities. This directory is the NIS build source for the NayaNET experience and its connected intelligence engine.

## Authority and method

This system is derived from the canonical `.naya` 01–58 source set plus current NayaNET architecture/contracts. Repository evidence outranks memory. Current implementation must be inspected before declaring a capability implemented or verified.

The 01–58 directive requires every area to define meaning, function, ownership/boundary, upstream/downstream dependencies, explicit connections, evidence, current state, gaps, and one next action. `UNKNOWN` is preferred to invention.

## Engineering map

- `00-SYSTEM-ARCHITECTURE.md` — what NayaNET is and how the systems fit together.
- `01-ENGINE-AND-DATA-FLOW.md` — the end-to-end intelligence/event/control flow.
- `02-IDENTITY-AUTHORIZATION-PRIVACY.md` — identity, authority, privacy, publication and access boundaries.
- `03-INTELLIGENCE-EVENT-DATA-CONTRACTS.md` — canonical objects, events, provenance and cross-system contracts.
- `04-VERIFICATION-GOVERNANCE-AND-DELIVERY.md` — verification, evidence, quality, deployment and definition-of-done rules.

## Feature specifications

1. `features/SMART-FEED.md`
2. `features/SMART-LEDGER.md`
3. `features/SMART-LIST.md`
4. `features/SMART-MAIL.md`
5. `features/SMART-SHARE.md`
6. `features/SMART-SPACES.md`
7. `features/YOUR-INTELLIGENCE-TODAY.md`
8. `features/INTELLIGENT-REPORTS.md`

## Standard feature contract

Every feature specification answers:

**WHAT → WHY → HUMAN EXPERIENCE → FRONT END → BACK END → DATA → API → EVENTS → INTELLIGENCE → CONNECTIONS → AUTHORITY/PRIVACY → FAILURE MODES → TESTS → OBSERVABILITY → DEPLOYMENT → VERIFICATION → CURRENT STATE → GAPS → NEXT ACTION.**

A feature is not considered complete merely because its UI exists. Source, build, deployed runtime, authenticated behavior, persistence, authorization, and evidence must agree at the level required by its verification contract.

## Source map

The primary feature definitions are `.naya` 03–14, especially 04/05/07/08/11/12/13/14. System architecture and governance are informed by 15–39. Hub/runtime/event/identity/verification/continuity are defined by 40–58. The canonical 01–58 directive is `.naya/NAYAPOWER-01-58-SYSTEM-MAP-DEFINITION-DIRECTIVE-V1.md`.

## NIS operating rule

When assigned a NayaNET feature:

1. Read this directory.
2. Read the feature specification.
3. Read every linked `.naya` authority named by the specification.
4. Inspect the actual repository/runtime before choosing implementation changes.
5. Preserve existing canonical primitives where they satisfy the contract.
6. Do not create duplicate stores or parallel concepts without explicit architectural justification.
7. Build the smallest correct change.
8. Test the complete user/data/authority path.
9. Record evidence and current state.
10. Leave one explicit continuation action.
