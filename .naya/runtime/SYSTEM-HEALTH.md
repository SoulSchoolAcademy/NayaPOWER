# NayaPOWER System Health / Master Node Contract

**Status:** CANONICAL RUNTIME ACCEPTANCE CONTRACT  
**Version:** 1.0  
**Effective:** 27 August 2026  
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## Purpose

This contract composes existing NayaPOWER boot, governance, memory, continuity, verification, and Smart Brain contracts into one deterministic current-state health receipt.

It does **not** create a second boot system, memory system, governance system, or One-Net architecture. Existing canonical contracts remain authoritative; this contract is the health/continuity composition layer.

## Health states

The receipt distinguishes:

`DOCUMENTED → REGISTERED → ACTIVATED → CONTEXT ESTABLISHED → OPERATING-METHOD ESTABLISHED → VERIFIED → NETWORK-CONNECTED → HEALTHY`

A state may not be promoted without the evidence required by the underlying contract. `UNKNOWN` is never promoted to `HEALTHY`.

## Required system surfaces

A healthy repository-level Master Node state must recognize and connect:

- canonical repository and governance branch;
- canonical boot entry and context manifest;
- Human Capability & Mastery operating policy;
- Continuous Block Execution and One-Network laws;
- memory/CIS and canonical event/index model;
- cold-start activation acceptance;
- continuity/handoff contract;
- evidence/verification runtime;
- specialized node boundaries for Naya, NayaPOWER, MAXIS, MAXESS, and Oscar;
- authority and provenance boundaries;
- human control and authorization boundaries;
- future-Naya handoff and mandatory Next Execution;
- current system status and evidence limitations.

## Reuse law

The implementation is `.naya/runtime/system_health.py`. It must reuse existing deterministic runtime contracts instead of reimplementing their internal validation logic. The health receipt is a composition of evidence, not a replacement validator.

## Network boundary

`NETWORK-CONNECTED` means that the governed architectural relationships and propagation rules are present and verified. It does **not** claim live distributed federation, external model execution, or deployment health.

Private memory remains private by default. One-Network does not authorize silent memory merging. Provenance, authority, privacy, and human control must survive propagation.

## Deployment separation

Smart Brain/system health and deployment/Vercel health are separate signals. A deployment failure must not be hidden by a healthy repository health receipt, and repository health must not be declared unhealthy merely because an unrelated deployment surface is unavailable.

## Verification

The health runtime may execute the existing cold-start, continuity, Smart Brain validation, and Smart Brain test contracts. Its exit code is `0` only when all required checks pass and the resulting receipt is `HEALTHY`.

A receipt is a point-in-time evidence object. It must include repository, HEAD, governance branch, states, individual checks, network boundaries, limitations, and the commands/evidence used.

**UNKNOWN IS NEVER SUCCESS.**
