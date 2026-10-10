# Source Precedence and Cold-Naya Navigation Reconciliation — 2026-09-29

**Status:** CURRENT PROCEDURAL PRECEDENCE — IMPLEMENTATION STATE MUST BE RE-RESOLVED AT BOOT

**Last precedence reconciliation:** 2026-09-29, based on `main` @ `2c89cadbee7b6d71f54d8d6538161a0dd2169487` (historical procedure basis only; this SHA is NOT current repository truth).
**Purpose:** Give a cold Naya one deterministic way to distinguish governing architecture, dated snapshots, live work, and evidence without inventing a missing control plane.
**Supersedes:** `SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-2026-09-28.md` (retained for provenance; do not use as current truth).

## Freshness correction

> **The embedded implementation SHA is historical.** This document defines the precedence procedure, not the live implementation state. A cold Naya MUST resolve current `main` and active GitHub work again before making a current-state claim.

## Source precedence

Use this order when sources disagree:

1. **Human authority and ratified constitutional/governance contracts**
   - `CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md`
   - `GOVERNANCE/0000-NAYAPOWER-GOVERNANCE-CONTRACT-V1.md`
   - explicit current Human Director instruction
2. **Current `main` repository state** for what is actually present in code/contracts.
3. **Current GitHub issues and pull requests** for active work and unresolved coordination, reconciled against current `main`.
4. **Current, claim-matched proof artifacts and workflow/runtime evidence** for verification status.
5. **Dated current-state or operations documents** as snapshots only; they do not override newer repository/work evidence.
6. **Activation-kit projections** as navigation instructions only; they are never a second brain or current-state authority.
7. **Historical/design discussion** as lineage only.

## Reconciliation table

| Source | Classification | Use |
|---|---|---|
| `AGENTS.md` | CURRENT | Repository boot gate. |
| `NAYA-ACTIVATION/PORTABLE-ACTIVATION-PROTOCOL-V1.md` | CURRENT | Activation procedure; does not itself define live project reality. |
| `NAYA-ACTIVATION/00-ACTIVATION-KIT-MAP-V1.md` | DERIVED | Portable navigation map over canonical repository sources. |
| `README.md` | CURRENT | Human-readable project orientation and proven-vs-unproven framing; not the live work queue. |
| `CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md` | CURRENT | Constitutional law. |
| `GOVERNANCE/0000-NAYAPOWER-GOVERNANCE-CONTRACT-V1.md` | CURRENT | Authority/governance contract. |
| `0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md` | CURRENT | Master design contract. |
| `ARCHITECTURE/0000-NAYAPOWER-SUPERBRAIN-MASTER-SPEC-V1.md` | CURRENT | Superbrain architecture. |
| `BRAIN/MASTER-MAP.md` | DERIVED | Brain navigation map; its filesystem paths must resolve to real repository paths. |
| `BRAIN/NAYAPOWER-BRAIN-INDEX.json` | DERIVED | Machine-readable brain index; not a live-status oracle. |
| `NAYANODE/0000-CANONICAL-TREE.md` | CURRENT | Canonical semantic/system tree. |
| `.naya/project-intelligence/NAYAPOWER-SYSTEM-NORTH-STAR-RATIFICATION-2026-09-26.md` | CURRENT | Ratified strategic model and authority boundary; not a live work queue. |
| `BRAIN/90-OPERATIONS/0001-MAX-10-EXECUTION-QUEUE-V1.md` | CURRENT | Canonical maximum-value execution queue (V8 as of 2026-09-29); live evidence outranks it. |
| `KNOWLEDGE/NAYAPOWER-CURRENT-STATE-V1.md` | STALE | Dated 2026-09-27 snapshot. Retain as evidence; reconcile with newer commits/issues/PRs before using current-state claims. |
| `BRAIN/90-OPERATIONS/0002-AAA-BRAIN-EXECUTION-PROMPT-V1.md` | DERIVED | Execution doctrine, not live state. |
| `ACTIVATION SYSTEM PROTOCOL.md` | HISTORICAL | Design discussion that motivated portable activation; not the canonical boot contract. |
| current open GitHub issues/PRs | CURRENT | Active work/coordination evidence; must be reconciled with `main` and proof. |
| matching workflow runs / proof receipts | CURRENT | Evidence for the specific claim/run/version they actually prove. |
| `.naya/control-plane/*` | STALE | Referenced by draft activation text but absent from current `main`; do not restore or invent it. |

## Deterministic cold-Naya path

A cold Naya enters the repository in this order:

1. `AGENTS.md`
2. `NAYA-ACTIVATION/PORTABLE-ACTIVATION-PROTOCOL-V1.md`
3. `NAYA-ACTIVATION/PORTABLE-ACTIVATION-MANIFEST-V1.json`
4. `NAYA-ACTIVATION/00-ACTIVATION-KIT-MAP-V1.md`
5. `CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md`
6. `GOVERNANCE/0000-NAYAPOWER-GOVERNANCE-CONTRACT-V1.md`
7. `0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md`
8. `ARCHITECTURE/0000-NAYAPOWER-SUPERBRAIN-MASTER-SPEC-V1.md`
9. `BRAIN/MASTER-MAP.md` and `BRAIN/NAYAPOWER-BRAIN-INDEX.json`
10. `NAYANODE/0000-CANONICAL-TREE.md` plus only the relevant deeper node/brain contracts
11. `.naya/project-intelligence/`
12. current `main` HEAD, current open issues/PRs, recent commits, and claim-matched proof/workflow evidence
13. classify current truth as IMPLEMENTED / VERIFIED / PRODUCTION_PROVEN / BLOCKED / UNKNOWN
14. select exactly one next executable action
15. leave a durable handoff/activation receipt

## Refresh receipt — 2026-09-29

**WHAT CHANGED:** Refreshed this reconciliation at PR #915 (Option A) merge time against current `main` @ `2c89cadbee7b6d71f54d8d6538161a0dd2169487`. Superseded the 2026-09-28 version. Stamped the CURRENT-REALITY locators with their verification base.

**CURRENT TRUTH (verified read-only, 2026-09-29):**
- Test suite: 303 passed / 3 skipped / 0 failed @ `2c89cad` (local run; VERIFIED-LOCAL).
- #975 CLOSED on live evidence (recovery run `36632538416` SUCCESS; North-Star audit V3 ACCEPTED; 2/2 outcome rows).
- #810 CLOSED (nine-node behavioral acceptance artifact `11063875114`, digest-verified).
- Current Truth Resolver: SUCCESS on current main (run `36633934942`).
- Channel Contract: PROPOSED, awaiting Human Director ratification.
- Canonical execution queue: `BRAIN/90-OPERATIONS/0001-MAX-10-EXECUTION-QUEUE-V1.md` (V8).

**WHY:** Dated activation text must lose to live evidence, always. A cold Naya reading a stale reconciliation would reconstruct a stale world.

**AUTHORITY:** PR #915 Option A, decided by Shawn (Human Director); merge executed by Naya under the continuous execution directive.

**BLOCKERS / UNKNOWNS:** Channel Contract ratification pending. Genuinely independent cold-bootstrap acceptance of the merged kit: NOT YET VERIFIED — see next action.

## Exactly one next action

**Run one genuinely cold Naya against the merged activation package with no hidden conversation context, require a durable activation receipt answering the ten cold-start questions, then have a second cold Naya independently reconstruct that receipt and current state.**
