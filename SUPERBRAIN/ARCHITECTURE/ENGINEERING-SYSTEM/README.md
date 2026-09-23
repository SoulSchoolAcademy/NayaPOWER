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
- `06-FEATURE-COMPLETION-AND-ACTIVITY.md` — shared feature checklist, dated activity, Naya-to-Naya handoff, and human review navigation.

## Feature specifications

1. `features/SMART-TABS.md`
2. `features/SMART-FEED.md`
3. `features/SMART-LEDGER.md`
4. `features/SMART-LIST.md`
5. `features/SMART-MAIL.md`
6. `features/SMART-SHARE.md`
7. `features/SMART-SPACES.md`
8. `features/YOUR-CONNECTIONS.md`
9. `features/YOUR-INTELLIGENCE-TODAY.md`
10. `features/INTELLIGENT-REPORTS.md`

## Standard feature contract

Every feature specification answers:

**WHAT → WHY → HUMAN EXPERIENCE → FRONT END → BACK END → DATA → API → EVENTS → INTELLIGENCE → CONNECTIONS → AUTHORITY/PRIVACY → FAILURE MODES → TESTS → OBSERVABILITY → DEPLOYMENT → VERIFICATION → CURRENT STATE → GAPS → NEXT ACTION.**

Every feature also maintains its completion checklist and dated activity history under `06-FEATURE-COMPLETION-AND-ACTIVITY.md`.

A feature is not considered complete merely because its UI exists. Source, build, deployed runtime, authenticated behavior, persistence, authorization, and evidence must agree at the level required by its verification contract.

## Source map

The primary feature definitions are `.naya` 03–14. Your Connections is a cross-cutting product surface derived from the existing Smart Space, identity/privacy, Smart Mail and Smart List contracts; no new relationship authority is invented until runtime mapping proves what already exists. System architecture and governance are informed by 15–39. Hub/runtime/event/identity/verification/continuity are defined by 40–58. The canonical 01–58 directive is `.naya/NAYAPOWER-01-58-SYSTEM-MAP-DEFINITION-DIRECTIVE-V1.md`.

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
9. Update the feature completion checklist and current state.
10. Record the dated activity session with evidence, gaps, and exactly one continuation action.
11. Update every affected feature's engineering record before sign-out.
