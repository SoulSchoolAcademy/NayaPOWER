# NayaNET Contract Law Library

**Status:** V1 STRUCTURE — Constitutional Contract Law RATIFIED 2026-09-26
**Canonical home:** `.naya/contracts/`

This directory is the **single navigational home for NayaNET Contract Law**.

## MANDATORY AI LAW

Before substantive work, every Naya MUST:
1. Read `00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md`.
2. Identify the applicable specialized contracts.
3. Read the applicable contracts before acting.
4. Reconcile contract requirements with live authoritative system state.
5. Never guess when the contract or evidence is silent.

For system-wide contract-library work, the Naya SHOULD read **all active contracts**.

## Current library structure

```
.naya/contracts/
├── README.md
├── 00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md
├── 01-INTELLIGENCE/
│   └── README.md
├── 02-GOVERNANCE-AND-FLOW/
│   └── README.md
├── 03-HUB/
│   └── README.md
└── 04-CONTINUITY/
    └── README.md
```

## Planned specialized boundaries

**01 — Intelligence:** Smart Note + Smart Link; Intelligence Organization; Adaptive Learning; Naya Playback / Dream.

**02 — Governance and Flow:** Smart Ledger; Receiver / Canonical Intelligence Engine; Sender; Backend / Sync / Projection.

**03 — Hub:** Smart Feed; Intelligence Today; Reports; Intelligent Library; SmartConnect; Connections; Smart Lists; Smart Mail; Smart Spaces; Settings.

**04 — Continuity:** Cold Naya Continuity / Successor.

These are discovery candidates, not yet ratified specialized contracts. The final number MUST emerge from actual boundaries after reconciliation with current documentation, implementation, runtime, and user experience.

## Contract design rule

A capability gets its own contract when it has a materially distinct combination of purpose, responsibility, authority, lifecycle, interface, failure behavior, or acceptance behavior.

If two proposed contracts cannot be meaningfully separated, merge them. If one contract contains multiple independently governed capabilities, split it. Do not optimize for a predetermined contract count.

## Contract anatomy

Each specialized contract must cover the dimensions applicable to its boundary:

**identity → purpose → boundary → actors → authority → inputs → outputs → state → transitions → data → canonical truth → intelligence → relationships → human experience/design → engineering → integrations → synchronization → privacy/security → failure → UNKNOWN/conflict → proof/receipts → acceptance → MUST/MUST NOT/MAY → anti-patterns → dependencies → change control → cold-Naya behavior.**

## Constitutional precedence

`00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md` governs this library. A specialized contract cannot override constitutional law.

If two applicable contracts materially conflict:

**STOP → IDENTIFY AUTHORITY → RECONCILE → RECORD → RESUME.**

Do not invent a compromise.

## Transition from Contract Stack V1

The former 10-contract stack is preserved as historical/scaffold context while this library is reconciled. It is **not** the final contract topology merely because those files already exist.

The new law deliberately begins with **Contract 00: Constitution**, then discovers and ratifies the true specialized boundaries.
