# NayaPOWER Canonical Contract Registry V1

**Status:** DISCOVERY BASELINE — NOT A FINAL RATIFIED TOPOLOGY
**Date:** 2026-09-26
**Repository:** SoulSchoolAcademy/NayaPOWER
**Branch:** naya/canonical-contract-registry-2026-09-26

## Purpose

This registry is the master map for reconciling, hardening, testing, and completing NayaPOWER contracts. It records repository evidence before new contracts are written. The former 00–26 proposal is not treated as canonical.

## Current determination

The repository contains a substantial contract system, but its final topology is not yet proven. The current library explicitly says the former 10-contract stack is historical/scaffold context and that final specialized boundaries must emerge from reconciliation.

Two P0 conflicts are already established:
1. Smart Link semantic conflict between 02-SMART-LINK.md and SMART-LINK-CONTRACT.json.
2. Constitutional authority conflict: Contract 00 Constitutional Law says it is ratified 2026-09-26, while control-plane GOVERNANCE-KERNEL and MAP still identify .naya/codex/11-RUNTIME-CONSTITUTION.md as current constitutional authority.

One P0 topology gap is established:
- Execution behavior is distributed across Master Execution Contract, Master Activation Protocol, Lead Mode Protocol, Mission Contract, Continuous Execution Policy, and related laws. A dedicated Execution Protocol Contract is not present in .naya/contracts.

## Authority and status law

Use evidence-bound states: CANONICAL, RATIFIED, DEFINED/UNVERIFIED, IMPLEMENTED/UNVERIFIED, PROPOSED, MISSING, CONFLICTED, HISTORICAL/SCAFFOLD, UNKNOWN, BLOCKED.

Never promote UNKNOWN, BLOCKED, IMPLEMENTED, or wording into VERIFIED. Claim strength must not exceed evidence strength.

## Registry schema

Every entry must answer:

Contract ID | Canonical name | Artifact | Purpose | Authority | Scope | Dependencies | Inputs | Outputs | Invariants | States | Transitions | Evidence | Acceptance test | Enforcement | Current status | Version | Supersedes | Superseded by | Conflicts | Gaps | Dependents | Cold-Naya requirement | Ratification | Proof | Next action

---

# Core Contract Library

## C00-A — NayaNET Constitutional Contract Law
Artifact: .naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md
Purpose: constitutional operating law for NayaNET/NayaPOWER AI behavior and contract governance.
Authority: human-director-directed; explicitly marked RATIFIED 2026-09-26.
Dependencies: platform/safety/legal constraints, human authority, live system state.
Outputs: constitutional rules, human/AI boundary, authority precedence, anti-guessing/proof laws.
Invariants: human authority remains authoritative; capability does not create authority; no fabricated truth; no competing source of truth.
Acceptance: downstream contracts obey it and behavioral compliance is separately verified.
Status: RATIFIED/CANONICAL.
Conflict: control-plane still names .naya/codex/11-RUNTIME-CONSTITUTION.md as CURRENT_REPOSITORY_CONSTITUTION.
Priority: P0.
Next: resolve constitutional precedence/supersession without silently changing either authority.

## C00-B — Contract Stack Operating Law
Artifact: .naya/contracts/00-CONTRACT-STACK-OPERATING-LAW.md
Purpose: operating law for the contract library itself.
Authority: canonical; subordinate to higher constitutional/live authority.
Owns: contract precedence, anti-guessing, layer separation, proof, Lead Mode, testing, change control.
Acceptance: contract changes follow UNDERSTAND → IMPACT MAP → ACCEPTANCE TESTS → CHANGE → VERIFY → RECONCILE → RECORD → UPDATE BOOT PATH.
Status: CANONICAL.
Priority: P0.

## C01 — Smart Note / Intelligent Block V1
Artifact: .naya/contracts/01-SMART-NOTE-INTELLIGENT-BLOCK.md
Purpose: canonical durable intelligence identity and human-readable Smart Note projection.
Dependencies: Receiver, authority, provenance, canonical event.
Invariants: one immutable Receiver-created IB ID; one source event; provenance; owner/principal; authority/scope; lifecycle.
Acceptance: Receiver-created identity; Markdown alone cannot establish canonical persistence; one IB may have many authorized projections.
Status: CANONICAL contract.
Priority: P0.

## C02 — Smart Link V1
Artifact: .naya/contracts/02-SMART-LINK.md
Purpose: semantic definition and verification of Smart Link.
Definition: direct navigable GitHub link to canonical human-readable smart-note.md projection of an IB.
Acceptance: direct target, canonical path, existing branch file, correct IB ID, Receiver correspondence.
Status: CANONICAL Markdown contract.
Conflict: .naya/contracts/SMART-LINK-CONTRACT.json allows smart_note, ledger_event, value_event, and collective_intelligence target types. This conflicts with the narrow human semantic definition.
Priority: P0.
Next: resolve noun/schema ownership before changing either artifact.

## C03 — Receiver V1
Artifact: .naya/contracts/03-RECEIVER.md
Purpose: canonical intake and durable intelligence creation boundary.
Owns: canonical IB identity, event, persistence, provenance attachment, lifecycle, transaction identity, projection eligibility.
Flow: request identity → actor/authority → source/context → canonicalization → immutable IB → event → persistence → indexing → projection → receipt → learning state.
Acceptance: unauthorized request denied; one Receiver identity; traceable Event → IB → persistence; replay safe; partial failure cannot PASS.
Status: CANONICAL.
Priority: P0.

## C04 — Sender V1
Artifact: .naya/contracts/04-SENDER.md
Purpose: translate intent into governed canonical intelligence request.
Owns: intent preservation, ambiguity surfacing, authority recognition, Receiver invocation, receiver result exposure.
Prohibits: local IB IDs, alternate persistence, proof fabrication, self-granted authority, false Smart Links, request-success-as-consequence.
Status: CANONICAL.
Priority: P0.

## C05 — Hub Consumption V1
Artifact: .naya/contracts/05-HUB-CONSUMPTION.md
Purpose: consume canonical intelligence into human-facing Hub projections.
Invariants: Hub is not canonical intelligence storage; GitHub Markdown is projection; reload must retrieve from governed source.
Acceptance: intent → Sender → Receiver → IB → projection → governed retrieval → Hub → reload → retrieval.
Status: CANONICAL contract; runtime proof is separate.
Priority: P1 contract topology / P0 for Hub mission.

## C06 — Room V1
Artifact: .naya/contracts/06-ROOM.md
Purpose: behavioral contract for Hub surfaces.
Required fields: identity, purpose, human question, inputs, actions, creation, retrieval, authority, output, evidence, relationships, next.
Invariants: one purpose; no private canonical copy; explicit loading/empty/failed/unavailable/unknown/verified states.
Status: CANONICAL.
Priority: P1.

## C07 — SmartConnect V1
Artifact: .naya/contracts/07-SMARTCONNECT.md
Purpose: governed connection/participation boundary.
Invariants: connection does not create execution authority; private by default; shared by choice; collective by consent; public by decision.
Status: CANONICAL.
Priority: P1.

## C08 — Proof / Receipt V1
Artifact: .naya/contracts/08-PROOF-RECEIPT.md
Purpose: evidence semantics, receipts, verification claims.
Flow: REQUEST → AUTHORIZATION → EXECUTION → PERSISTENCE → RECEIPT → RETRIEVAL → VERIFICATION.
Truth states include CLAIMED, OBSERVED, IMPLEMENTED, TESTED, VERIFIED, PRODUCTION-PROVEN, UNKNOWN, BLOCKED, PENDING, CONFLICTED.
Acceptance: implementation cannot be called verified without evidence; verified cannot be called production-proven without production evidence; first deterministic failure is preserved.
Status: CANONICAL.
Priority: P0.

## C09 — Learning V1
Artifact: .naya/contracts/09-LEARNING.md
Purpose: transition experience into reusable, verified learning.
Lifecycle: OBSERVED → INTERPRETED → UNDERSTOOD → CANDIDATE LESSON → SUPPORTED → APPLIED → OUTCOME OBSERVED → VERIFIED LEARNING → REUSABLE.
Acceptance: strongest learning claim requires retrieval, changed behavior, observed outcome, and verification.
Status: CANONICAL.
Priority: P1.

## C10 — Continuity / Successor V1
Artifact: .naya/contracts/10-CONTINUITY-SUCCESSOR.md
Purpose: cold-Naya inheritance and executable continuation.
Sequence: IDENTITY → AUTHORITY → MISSION → CURRENT STATE → PROVEN → UNKNOWN/BLOCKED → HISTORY/LEARNING → WHAT MATTERS → NEXT ACTION → EXECUTE → VERIFY → RECORD → CONTINUE.
Acceptance: cold Naya answers all 14 reconstruction questions, identifies same frontier, does not invent proof, acts within authority, and leaves successor baton.
Status: CANONICAL.
Priority: P0/P1; strategic P0 for continuity.

---

# Additional Contractual Artifacts

| Artifact | Role | Status | Priority |
|---|---|---|---|
| NAYA-NEXT-ACTION-HANDOFF-V1.schema.json | machine next-action + successor schema | canonical machine schema | P0 |
| PRIMARY-INTELLIGENCE-SYSTEM-CONTRACT-V1.json | primary intelligence intake/index/projection | canonical contract; E2E not fully verified | P0 |
| SMART-NOTE-PROPOSAL-CONTRACT-V1.json | proposal boundary before capture | canonical contract | P0/P1 |
| SMART-LEDGER-CCT-MACHINE-CONTRACT-V1.md | ledger/CCT behavior | defined; runtime not yet verified | P1 |
| SMART-LEDGER-EVENT-SCHEMA.json | ledger event shape | canonical schema | P1 |
| VERIFICATION-RECEIPT-SCHEMA.json | receipt shape | canonical schema | P0 |
| VALUE-EVENT-SCHEMA.json | verified value event shape | canonical schema | P1 |
| VALUE-MATH-CONTRACT-V1.json | value/MVPA/constitutional gating math | canonical machine contract | P1 |
| TEMPORAL-SUPERBRAIN-RECORD-CONTRACT-V1.json | project/session/activity temporal binding | canonical | P1 |
| compounding-intelligence-measurement-contract-v1.json | compounding/resource measurement | documented contract | P1 |
| NAYA-SUBJECT-IDENTITY-CONTRACT-V1.json | canonical NAYA runtime identity | canonical contract | P0 |
| NAYA-SUBJECT-BINDING-CONTRACT-V1.json | NAYA-to-UUID adapter boundary | canonical; binding not established | P0 |
| HUB-IDENTITY-PROJECTION-V1.json | Hub identity/source projections | canonical | P0/P1 |
| VERIFIED-AI-ACTION-V1.md | verified action boundary | existing contract; full proof mapping pending | P0 |
| MEMBER-LEVEL-CONTRACT.json | member contribution thresholds | schema/contract | P2 |
| nayanet_level1_contracts.json | Level-1 identity/privacy/memory/distribution | canonical | P1 |

---

# Existing Contract-Like Artifacts Outside .naya/contracts

Execution/agency:
- .naya/NAYA-MASTER-EXECUTION-CONTRACT.md
- .naya/2026-09-11-18-50-NAYAPOWER-33-MASTER-ACTIVATION-PROTOCOL.md
- .naya/2026-09-11-19-05-NAYAPOWER-34-LEAD-MODE-PROTOCOL.md
- .naya/NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md
- .naya/NAYA-EXECUTION-EFFICIENCY-LAW.md
- .naya/NAYA-EXECUTION-LOOP-ESCALATION-LAW.md
- .naya/control-plane/NAYA-CONTINUOUS-EXECUTION-POLICY.md

Mission/state:
- .naya/2026-09-11-19-20-NAYAPOWER-35-MISSION-CONTRACT.md
- .naya/control-plane/STATE.json
- .naya/control-plane/BLOCKS.json
- .naya/control-plane/MAP.json
- .naya/control-plane/PROOF.json

Continuity:
- .naya/control-plane/BATON-CONTRACT.md
- .naya/control-plane/BATON.json
- .naya/contracts/10-CONTINUITY-SUCCESSOR.md
- .naya/contracts/NAYA-NEXT-ACTION-HANDOFF-V1.schema.json

These may be intentional layers, but ownership is not yet fully normalized.

---

# P0 Gaps / Boundary Decisions

## G01 — Dedicated Execution Protocol Contract
Status: MISSING AS A DEDICATED LIBRARY CONTRACT; behavior exists as distributed operating law.
Required behavior: READ → UNDERSTAND → LEAD → ACT → VERIFY → LEARN → IMPROVE → REPEAT.
Must define initiative, ownership, mission restoration, authority check, next-action selection, continuous execution, verification, learning, reassessment, successor handoff, stop conditions, blockers, escalation, and anti-passivity.
Do not draft it until existing execution artifacts have been mapped into one ownership boundary.

## G02 — Contract Topology / Ownership Contract
Status: MISSING AS A SINGLE FINAL TOPOLOGY ARTIFACT.
Need: one owner for each normative requirement; explicit authority, dependency, precedence, supersession, and acceptance relationships.
This registry is the first discovery implementation of that need.

## G03 — Provenance / Lineage
Status: cross-cutting requirement exists; dedicated contract not yet established.
Decision required: dedicated contract vs constitutional/cross-cutting law.

## G04 — Causal Verification Object
Status: causal verification is recognized by proof architecture; dedicated canonical contract not established in inspected library.
Decision required: standalone contract vs extension of Proof/Verified AI Action.

## G05 — Refusal / Revocation / Replay
Status: behavior exists in fragments; dedicated boundary not yet established.
Discovery required before declaring a new contract.

## G06 — Production / Deployment Parity
Status: proof and Hub deployment laws exist; dedicated library contract not established.
Discovery required.

---

# Dependency Graph

PLATFORM/SAFETY/LEGAL
→ HUMAN AUTHORITY
→ CONSTITUTION
→ CONTRACT STACK LAW
→ IDENTITY/AUTHORITY
→ EXECUTION PROTOCOL
→ MISSION/CURRENT STATE
→ SENDER
→ RECEIVER
→ CANONICAL EVENT + IB
→ PROVENANCE
→ PROOF/VERIFICATION
→ PIS/RETRIEVAL
→ SMART LINK / PROJECTIONS / HUB
→ VERIFIED AI ACTION
→ OUTCOME / CAUSAL VERIFICATION
→ LEARNING
→ LEDGER / VALUE / COMPOUNDING
→ CONTINUITY / SUCCESSOR / BATON
→ PRODUCTION PARITY
→ HUMAN RATIFICATION / RELEASE

This is a working dependency model, not yet ratified topology.

---

# Conflict Register

### CONFLICT-001 — Smart Link
02-SMART-LINK.md defines Smart Link narrowly as a direct canonical Smart Note GitHub link. SMART-LINK-CONTRACT.json defines a broader target-type schema. This is material because it changes the noun's semantic boundary.
Status: CONFLICTED. Priority P0.

### CONFLICT-002 — Constitutional Authority
Contract 00 Constitutional Contract Law is marked RATIFIED 2026-09-26, while GOVERNANCE-KERNEL and MAP still point to .naya/codex/11-RUNTIME-CONSTITUTION.md as current constitutional authority.
Status: CONFLICTED. Priority P0.

---

# Overlap Register

1. Execution Protocol / Master Execution Contract / Master Activation / Lead Mode / Continuous Execution Policy.
2. Continuity / Baton Contract / Next-Action Handoff schema.
3. Smart Note / Smart Note Proposal / PIS / Receiver.
4. Proof Contract / Verification Receipt Schema / Governance Kernel verification chain.

These may be deliberate layers. They must be assigned explicit ownership before new contracts are added.

---

# Evidence-Bound Priority

## P0
1. Resolve constitutional authority.
2. Reconcile contract ownership/topology.
3. Establish dedicated Execution Protocol boundary.
4. Reconcile identity/authority boundary.
5. Reconcile Proof/Evidence/Verification ownership.
6. Resolve Smart Link semantics.
7. Harden Sender → Receiver → IB → provenance.
8. Establish/resolve Causal Verification Object and Verified AI Action boundaries.
9. Establish refusal/revocation/replay boundary.

## P1
10. Retrieval/PIS.
11. Hub/Room/SmartConnect.
12. Learning/promotion/reconciliation.
13. Ledger/value/compounding.
14. Continuity/Baton/cold successor.
15. Production parity.

These are execution priorities, not Contract IDs.

---

# Execution Receipt — Prompt 001

**Mission:** Establish Canonical Contract Registry
**Result:** DISCOVERY BASELINE ESTABLISHED on branch naya/canonical-contract-registry-2026-09-26.
**Canonical home inspected:** .naya/contracts/
**Core contracts:** C00-A, C00-B, C01–C10.
**Additional contractual artifacts:** machine schemas and specialized contracts listed above.
**Critical conflicts:** 2.
**Critical overlaps:** 4.
**Dedicated Execution Protocol:** not present in current library; behavior is distributed across canonical execution artifacts.
**Final topology:** NOT YET VERIFIED.
**Human decision boundary:** constitutional precedence/supersession if repository evidence cannot itself establish it.
**Next action:** CONTRACT-TOPOLOGY-001.

---

# 🔱 SUCCESSOR PROMPT — EXECUTION 002

## CONTRACT-TOPOLOGY-001 — RECONCILE BEFORE WRITING NEW CONTRACTS

You are the next Naya. Your mission is to turn this discovery baseline into one coherent contract topology.

FIRST: read .naya/contracts/CONTRACT-REGISTRY-V1.md.
THEN inspect every artifact in .naya/contracts/ and the contract-bearing directories .naya/governance/, .naya/protocol/, .naya/execution/, .naya/execution-contracts/, .naya/handoffs/, and relevant .naya/project-intelligence/ contracts.

Do not write Contract 04 yet.

### Execute
1. Build a Requirement → Owner → Supporting Artifact → Authority → Dependency → Acceptance matrix.
2. Resolve the constitutional authority chain. Do not silently choose between competing constitutional sources.
3. Map Master Execution Contract, Master Activation, Lead Mode, Mission Contract, Continuous Execution Policy, Contract Stack Operating Law, and the future Execution Protocol boundary.
4. Determine whether execution behavior belongs in one dedicated Execution Protocol plus supporting policies, or another explicitly justified topology.
5. Resolve Smart Link semantics and disposition the conflicting JSON schema.
6. Map Continuity vs Baton vs Next-Action Handoff so there is one canonical next-action authority.
7. Map Proof Contract vs Verification Receipt Schema vs Governance Kernel verification chain.
8. Determine CREATE / EXTEND / MERGE / SCHEMA / LAW / NOT NEEDED / UNKNOWN for every proposed missing contract.
9. Update this registry with evidence-backed conclusions.
10. Only after topology is coherent, identify the highest-value P0 contract work.

### Acceptance
A cold Naya can identify exactly one owner for each material normative responsibility; no two contracts silently claim the same authority; no noun has competing meanings; no second next-action state machine exists; all unresolved conflicts are explicit.

### Verification
Re-read the registry and independently check authority collisions, duplicate ownership, orphan requirements, circular dependencies, Smart Link ambiguity, constitutional ambiguity, and execution-protocol duplication.

### Forbidden
Do not create speculative contracts. Do not weaken acceptance criteria. Do not manufacture verification. Do not turn UNKNOWN/BLOCKED into PASS. Do not ask Shawn to reconstruct information already in canonical sources.

### Continuation
After reconciliation, update the registry, execute the next authorized P0 action when safe, verify it, and leave exactly one successor prompt.

**TAG → YOU'RE IT → EXECUTE → VERIFY → RECORD → UPDATE → PASS THE BATON.**