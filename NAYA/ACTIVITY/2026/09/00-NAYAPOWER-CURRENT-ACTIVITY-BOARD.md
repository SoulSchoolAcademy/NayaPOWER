## 2026-09-26 — CONTRACT_RECONCILIATION

**Actor:** NAYA  
**Objective:** Reconcile the next specialized contract boundary after EP-001: Smart Note + Smart Link.  
**Status:** PROPOSED CONTRACT CREATED — NOT RATIFIED.

**What was inspected**
- CC-000 Constitutional Contract Law.
- Contract Library README.
- Canonical Smart Note / Intelligent Block System V1.
- Naya Link Identity & Evidence Contract V1.
- EP-001 NayaNET Execution Protocol.
- Canonical Smart Note registry.
- Canonical Smart Note path resolver.
- Current control-plane next-action / continuity sources.

**Finding**
Smart Note + Smart Link form one coherent intelligence-facing boundary: the Smart Note is the human-readable projection of the canonical IB, and the Smart Link is the exact navigable GitHub link to that projection. They should not become separate stores or identities.

**Changed**
- Added `.naya/contracts/01-INTELLIGENCE/01-SMART-NOTE-AND-SMART-LINK.md`
- Updated `.naya/contracts/01-INTELLIGENCE/README.md`

**Important truth**
INT-001 is **PROPOSED**, not RATIFIED. The existing canonical Smart Note and Smart Link contracts remain authoritative until specialized-contract ratification occurs.

**Evidence**
- Contract commit: `841f63b60a6c990cc070b79ac43ce92f085ebd3a`
- Index commit: `5ec348edd9fc16dd5b49c941cf46bba131999bca`

**UNKNOWN / OPEN**
- INT-001 behavioral acceptance is not yet proven.
- Deterministic Smart Link enforcement has not yet been added.
- Human-director ratification is still required before INT-001 becomes binding specialized law.

**NEXT**
Run the INT-001 boundary/acceptance reconciliation against representative canonical Smart Notes, then prepare ratification + machine-checkable enforcement only where the existing implementation does not already prove the contract.
