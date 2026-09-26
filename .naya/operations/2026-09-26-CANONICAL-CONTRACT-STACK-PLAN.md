# 2026-09-26 — Canonical Contract Stack Build Plan

**Status:** CANONICAL PLAN — HUMAN-DIRECTOR DIRECTED 2026-09-26

## Objective

Turn the agreed NayaPOWER architecture into one deterministic Contract Stack so independent Nayas converge on the same behavior instead of implementing the same mission in incompatible ways.

## Today’s execution order

1. Establish one contract tree at `.naya/contracts/`.
2. Establish the stack operating law and precedence rules.
3. Define Contracts 01–10 with explicit ownership, non-ownership, MUST/MUST NOT behavior, boundaries, and acceptance tests.
4. Wire the tree into `README.md` and `SUPERBRAIN/AI-BOOT/START-HERE.md` so every Naya is told to read the contracts.
5. Register the tree in the canonical source map.
6. Reconcile each contract against the Constitution, current control plane, existing Smart Note/Smart Link/participation sources, and Hub alignment.
7. Identify and eliminate semantic overlaps or contradictory current contracts before implementation expands.
8. Convert the contracts into executable acceptance tests and enforcement where implementation exists.
9. Build the first complete vertical slice: human intent → Sender → Receiver → Event → IB → projection → Smart Link → retrieval → Hub → reload → proof → learning → cold successor.
10. Only after that slice is verified, expand the same contract family across the remaining Hub surfaces.

## Contract set

- 00 — Contract Stack Operating Law
- 01 — Smart Note / Intelligent Block
- 02 — Smart Link
- 03 — Receiver
- 04 — Sender
- 05 — Hub Consumption
- 06 — Room
- 07 — SmartConnect
- 08 — Proof / Receipt
- 09 — Learning
- 10 — Continuity / Successor

**Promotion is governed inside Contract 09 (Learning); no separate Contract 11 is created in V1.**

## Definition of done for today

The documentation phase is complete only when the tree is discoverable from the boot path, each contract has a declared boundary and acceptance tests, and conflicting current terminology has been reconciled rather than papered over.

The engineering phase is complete only when the first vertical slice passes its own acceptance criteria with evidence at each boundary.

## Non-negotiable stop conditions

- Do not guess missing semantics.
- Do not create a second source of truth.
- Do not call documentation proof.
- Do not create a Smart Link from a predicted path.
- Do not mark learning from a field label alone.
- Do not expand to ten rooms before the first vertical slice is proven.
- Do not weaken a contract to make an implementation pass; amend it explicitly if the contract itself is wrong.
