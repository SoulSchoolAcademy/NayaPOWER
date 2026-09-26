# NayaPOWER Canonical Contract Registry V1

**Status:** DISCOVERY BASELINE — NOT A FINAL RATIFIED TOPOLOGY
**Date:** 2026-09-26
**Repository:** SoulSchoolAcademy/NayaPOWER
**Branch:** naya/canonical-contract-registry-2026-09-26

## Purpose

This registry is the master map for reconciling, hardening, testing, and completing NayaPOWER contracts. It records repository evidence before new contracts are written. The former 00–26 proposal is not treated as canonical.

## Current determination

The repository contains a substantial contract system, but its final topology is not yet proven. The current library explicitly says the former 10-contract stack is historical/scaffold context and that final specialized boundaries must emerge from reconciliation. Topology reconciliation has now confirmed an important correction: a dedicated Execution Protocol already exists as EP-001 under `.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md`; it is PROPOSED, so the problem is hardening/integration and ownership reconciliation, not absence.

Two P0 conflicts are already established:
1. Smart Link semantic conflict between 02-SMART-LINK.md and SMART-LINK-CONTRACT.json.
2. Constitutional authority conflict: Contract 00 Constitutional Law says it is ratified 2026-09-26, while control-plane GOVERNANCE-KERNEL and MAP still identify .naya/codex/11-RUNTIME-CONSTITUTION.md as current constitutional authority.

One P0 topology gap is established:
- Execution behavior has a dedicated proposed owner, EP-001, but its relationship to Master Execution Contract, Master Activation Protocol, Lead Mode Protocol, Mission Contract, Continuous Execution Policy, and related laws is not yet fully normalized. The required action is EXTEND/HARDEN EP-001 and reconcile supporting layers; do not create a second Execution Protocol.

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

## G01 — Execution Protocol Boundary
Status: EXISTING / PROPOSED — EXTEND/HARDEN REQUIRED.
Canonical candidate: `.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md` (EP-001, V1.0, PROPOSED).
EP-001 already defines initiative, ownership, mission advancement, authority boundaries, next-action selection, continuous verified progress, verification, evidence preservation, successor handoff, blockers, stop conditions, and anti-passivity.
Required action: reconcile EP-001 against the legacy/supporting execution stack and establish one normative owner with explicit supporting-layer boundaries. Do not create a second Execution Protocol.

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
3. Reconcile and harden EP-001 as the single normative Execution Protocol boundary.
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
**Execution Protocol:** EP-001 exists in `.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md`; status PROPOSED; topology action is EXTEND/HARDEN and reconcile supporting execution artifacts.
**Final topology:** NOT YET VERIFIED.
**Human decision boundary:** constitutional precedence/supersession if repository evidence cannot itself establish it.
**Next action:** CONTRACT-TOPOLOGY-002 — reconcile constitutional authority and execution ownership.

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
10. Only after topology is coherent, identify the highest-value P0 contract work; if a boundary is already owned by a proposed contract, harden/reconcile it instead of creating a duplicate.

### Acceptance
A cold Naya can identify exactly one owner for each material normative responsibility; no two contracts silently claim the same authority; no noun has competing meanings; no second next-action state machine exists; all unresolved conflicts are explicit.

### Verification
Re-read the registry and independently check authority collisions, duplicate ownership, orphan requirements, circular dependencies, Smart Link ambiguity, constitutional ambiguity, and execution-protocol duplication.

### Forbidden
Do not create speculative contracts. Do not weaken acceptance criteria. Do not manufacture verification. Do not turn UNKNOWN/BLOCKED into PASS. Do not ask Shawn to reconstruct information already in canonical sources.

### Continuation
After reconciliation, update the registry, execute the next authorized P0 action when safe, verify it, and leave exactly one successor prompt.

**TAG → YOU'RE IT → EXECUTE → VERIFY → RECORD → UPDATE → PASS THE BATON.**

## CONTRACT-TOPOLOGY-002 — CONSTITUTION + EXECUTION OWNERSHIP RECEIPT

**Date:** 2026-09-26
**Status:** VERIFIED DISCOVERY / RATIFICATION BLOCKED AT CONSTITUTIONAL PRECEDENCE

### Constitutional authority comparison

| Artifact | Version | Date/effective evidence | Authority claim | Current references | Supersession evidence | Disposition |
|---|---|---|---|---|---|---|
| `.naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md` | Proposed V1.0 | Human-director-directed 2026-09-26; explicitly marked ratified | NayaNET Constitutional Contract Law; applies to every Naya, agent, contract, capability and governed execution | New contract itself; not yet the sole control-plane pointer | **NONE FOUND in inspected repository evidence** | RATIFIED BY DOCUMENTED HUMAN DIRECTION, but repository authority chain remains conflicted |
| `.naya/codex/11-RUNTIME-CONSTITUTION.md` | V1.0 | No effective date stated in inspected header | Canonical / Constitutional; Document 11 of 20 | `.naya/control-plane/MAP.json`, `.naya/control-plane/STATE.json` still identify it as current constitutional authority | **NONE FOUND in inspected repository evidence** | CANONICAL/CONSTITUTIONAL POINTER REMAINS ACTIVE; conflict unresolved |

**Precedence finding:** the repository does **not** currently establish explicit supersession or amendment precedence between these two constitutional artifacts. The new law contains a human-directed ratification statement, but that statement does not by itself rewrite the older control-plane authority pointers. Therefore the constitutional chain remains **CONFLICTED / HUMAN DECISION REQUIRED**. No constitutional pointer was silently changed.

### Execution ownership finding

**EP-001 is the single normative execution-owner candidate and should be treated as the only normative Execution Protocol boundary.** It explicitly owns execution behavior: proactive ownership, authorized objective advancement, next-value action selection, continuous execution, dependency ordering, execution waves, verification, evidence preservation, blocker handling, safe stops, continuation, and anti-passivity.

The surrounding execution artifacts are classified as follows:

| Artifact | Classification | Relationship to EP-001 |
|---|---|---|
| `.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md` (EP-001) | **NORMATIVE OWNER** | One bounded normative execution contract; PROPOSED; harden/integrate, do not duplicate |
| `.naya/NAYA-MASTER-EXECUTION-CONTRACT.md` | **SUPPORTING POLICY / LEGACY NORMATIVE OVERLAP** | Broad operational contract predating EP-001; its execution-behavior claims must be subordinated/reconciled rather than left as a competing owner |
| `.naya/2026-09-11-18-50-NAYAPOWER-33-MASTER-ACTIVATION-PROTOCOL.md` | **SUPPORTING POLICY** | Entry/activation procedure; restores context and mission before execution; does not own execution loop semantics |
| `.naya/2026-09-11-19-05-NAYAPOWER-34-LEAD-MODE-PROTOCOL.md` | **SUPPORTING POLICY** | Human/Naya lead-mode behavior; should defer execution mechanics to EP-001 |
| `.naya/2026-09-11-19-20-NAYAPOWER-35-MISSION-CONTRACT.md` | **SUPPORTING POLICY / MISSION BOUNDARY** | Defines mission/objective framing; not the execution engine |
| `.naya/control-plane/NAYA-CONTINUOUS-EXECUTION-POLICY.md` | **SUPPORTING POLICY + ENFORCEMENT BINDING** | Operationalizes continuous execution and lifecycle gating; it must not define a competing execution protocol |
| `.naya/NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md` | **SUPPORTING CROSS-CUTTING LAW** | Governs continuity/learning relationship; EP-001 consumes its constraints |
| `.naya/NAYA-EXECUTION-EFFICIENCY-LAW.md` | **SUPPORTING POLICY** | Efficiency/optimization constraints; not normative ownership of execution behavior |
| `.naya/NAYA-EXECUTION-LOOP-ESCALATION-LAW.md` | **SUPPORTING CROSS-CUTTING LAW** | Escalation/repetition boundary; EP-001 incorporates it as an execution constraint |
| `.naya/control-plane/BATON-CONTRACT.md` | **SUPPORTING CONTINUATION CONTRACT** | Owns continuation boundary, not execution behavior |
| `.naya/contracts/NAYA-NEXT-ACTION-HANDOFF-V1.schema.json` | **MACHINE SCHEMA** | Projects one next action/handoff; subordinate to BLOCKS + EP-001 + Baton relationship |
| `.naya/control-plane/BLOCKS.json` | **CURRENT STATE / NEXT-ACTION AUTHORITY** | Owns active block and exactly one project-level next action; not a second execution protocol |
| `.naya/control-plane/BATON.json` | **CONTINUATION PROJECTION** | Assembles continuation from STATE/BLOCKS/MAP/PROOF; does not override them |
| `.naya/control-plane/STATE.json` | **CURRENT STATE AUTHORITY** | Owns current operational state; does not select execution semantics |
| `.naya/control-plane/MAP.json` | **NAVIGATION / AUTHORITY MAP** | Owns mission/system/authority navigation; its constitutional pointer is currently conflicted |

### One-next-action authority

The topology is now explicit at the execution/continuity boundary:

**BLOCKS.json owns the single project-level next action.**

**EP-001 owns the normative rule for how Naya selects and executes that authorized action.**

**BATON.json owns the continuation handoff projection.**

**NAYA-NEXT-ACTION-HANDOFF-V1.schema.json owns only machine shape.**

**STATE.json owns current operational state; MAP.json owns navigation; PROOF.json owns proof claims/evidence rules.**

This is one next-action authority, not competing state machines.

### Contract topology acceptance status

| Acceptance condition | Result |
|---|---|
| One normative execution owner | **PASS — EP-001** |
| No second Execution Protocol created | **PASS** |
| Supporting execution artifacts classified | **PASS — evidence-backed classification above** |
| One project-level next-action authority | **PASS — BLOCKS.json** |
| Baton preserved as continuation boundary | **PASS** |
| Machine handoff schema subordinate | **PASS** |
| Constitutional precedence explicit | **BLOCKED — repository cannot establish supersession** |
| Final topology ratification-ready | **BLOCKED by constitutional conflict** |

### Safe authorized P0 frontier after reconciliation

Because constitutional precedence remains unresolved, do **not** ratify or rewrite constitutional authority. The next safe P0 work is **EP-001 hardening/integration analysis** that does not alter constitutional authority: identify exact overlapping MUST rules with the Master Execution Contract, Lead Mode, Activation, and Continuous Execution Policy; define subordinate/supporting boundaries; and produce acceptance tests proving EP-001 is the sole normative execution owner.

This work may proceed without resolving the constitutional conflict because it is repository analysis/reconciliation, not constitutional amendment. Any action that would change which constitutional artifact is authoritative remains **HUMAN DECISION REQUIRED**.

### Evidence receipt

- EP-001 exists at the exact canonical path and is V1.0 / PROPOSED.
- New Constitutional Contract Law exists and is explicitly marked RATIFIED — HUMAN-DIRECTOR DIRECTED — 2026-09-26.
- Runtime Constitution exists as V1.0 / CANONICAL / CONSTITUTIONAL.
- MAP.json and STATE.json still point to Runtime Constitution as canonical current constitution.
- No inspected repository evidence established explicit supersession/amendment of Runtime Constitution by Contract 00.
- BATON-CONTRACT explicitly says Baton is not a second project state machine.
- NAYA-NEXT-ACTION-HANDOFF schema explicitly says it is not a competing mission state machine.

### Result

**CONTRACT-TOPOLOGY-002: EXECUTED.** Constitutional authority remains **CONFLICTED / HUMAN DECISION REQUIRED**. Execution ownership is reconciled to **EP-001 as the single normative execution owner**, with existing execution artifacts retained as subordinate/supporting layers until explicit hardening is completed.


## CONTRACT-TOPOLOGY-002B — SMART LINK SEMANTIC RECONCILIATION

**Status:** VERIFIED SEMANTIC FINDING / SCHEMA CHANGE NOT YET APPLIED

The P0 Smart Link boundary was inspected after execution ownership was hardened.

**Normative semantic owner:** INT-001 / `.naya/contracts/01-INTELLIGENCE/01-SMART-NOTE-AND-SMART-LINK.md`, reinforced by `.naya/contracts/02-SMART-LINK.md`.

Both normative Markdown artifacts agree: **Smart Link means only the direct GitHub link to the canonical human-readable `smart-note.md` projection of one Receiver-created IB.** Hub Deep Link and Evidence Link are explicitly different nouns.

**Conflict:** `.naya/contracts/SMART-LINK-CONTRACT.json` currently permits `target_type = smart_note | ledger_event | value_event | collective_intelligence`. That machine schema therefore exposes multiple meanings for the same noun and violates the repository's Exact-Noun Law.

**Disposition:** `SMART-LINK-CONTRACT.json` = **MACHINE SCHEMA / MERGE-NARROW CANDIDATE**, not a competing semantic contract. The schema should be narrowed to the single normative Smart Link meaning only after a reference audit establishes whether any live implementation depends on the broad enum. No schema mutation was made in this wave because the reference/dependent surface was not yet established; guessing a compatibility impact would violate the anti-guessing law.

**Next P0 action:** audit all repository references to `SMART-LINK-CONTRACT.json` and its `target_type` values; then, if no distinct canonical generic-link owner exists, narrow the schema to `smart_note` and preserve ledger/value/collective links under their own nouns/schemas rather than calling them Smart Links.

**EP-001 hardening receipt:** EP-001 now contains an explicit normative ownership boundary and acceptance tests; status remains PROPOSED because hardening does not equal ratification/verification.


## SMART-LINK-REFERENCE-AUDIT-001 — RECEIPT

**Date:** 2026-09-26
**Result:** REFERENCE AUDIT LIMITED BY GITHUB CODE-SEARCH INDEX RESPONSE; SCHEMA NOT MODIFIED

### Findings

- The repository contains `.naya/contracts/SMART-LINK-CONTRACT.json` with a broad `target_type` enum.
- The repository also contains dedicated canonical machine schemas for `ledger_event` (`SMART-LEDGER-EVENT-SCHEMA.json`) and `value_event` (`VALUE-EVENT-SCHEMA.json`).
- The inspected PIS contract separately models primary intelligence events and does not establish `collective_intelligence` as a Smart Link semantic.
- GitHub code-search queries for the schema filename and each target type returned no indexed matches. This is **not sufficient evidence of zero dependencies**, because the connected search surface returned no indexed code matches even for known repository artifacts. Therefore live/historical/test/unused classification cannot safely be asserted from this search result alone.
- No schema narrowing was performed. This preserves compatibility and avoids guessing.

### Disposition

`SMART-LINK-CONTRACT.json` remains **CONFLICTED / MACHINE SCHEMA / NARROW-MERGE CANDIDATE**. Dedicated ledger and value-event schemas exist, supporting separation of those nouns. `collective_intelligence` still lacks a verified distinct Smart Link consumer/owner in the inspected evidence.

### Next authorized P0

Use repository-tree/commit/diff inspection or another authoritative reference mechanism to establish all dependencies of `SMART-LINK-CONTRACT.json` and its enum values. Only after that evidence is complete may the schema be narrowed or retired. Constitutional authority remains untouched.

**Acceptance:** no Smart Link schema mutation without dependency evidence; no competing Smart Link noun; unresolved dependency search limitation remains explicitly UNKNOWN rather than PASS.


## SMART-LINK-DEPENDENCY-001 — FINAL RECEIPT

**Date:** 2026-09-26
**Result:** PARTIAL / SAFE RECONCILIATION APPLIED; DEPENDENCY PROOF REMAINS INCOMPLETE

### Authoritative evidence discovered

1. `.naya/contracts/SMART-LINK-CONTRACT.json` was introduced by commit `6611a3fe52dd0b353277c5e763b9e4b6c02b214f` on 2026-09-11. The commit creates the schema from scratch and is the direct provenance of the broad `target_type` enum.
2. The older prose `.naya/2026-09-12-NAYAPOWER-48-SMART-LINK-CONTRACT.md` was introduced by commit `03a1831b633aabf06d199c6c5929b2c3c920b591`. It defines a broader identity/intelligence-link concept, including canonical intelligence object/event links.
3. The newer canonical `.naya/codex/NAYA-LINK-IDENTITY-AND-EVIDENCE-CONTRACT-V1.md` is explicitly **CANONICAL — RATIFIED 2026-09-25** and defines Smart Link narrowly as the direct GitHub canonical `smart-note.md` link. Its enforcement test is `.naya/tests/test_smart_link_identity_contract.py`, executed by `.github/workflows/verify-smart-link-identity.yml`.
4. The current INT-001 and Contract 02 prose independently agree with that narrow definition.
5. Dedicated schemas exist for `ledger_event` and `value_event`, so those nouns already have separate machine boundaries.

### Dependency classification

| Surface | Finding |
|---|---|
| Current code/schema references to `SMART-LINK-CONTRACT.json` | **UNKNOWN** — GitHub code-search index returned no matches and cannot be treated as exhaustive |
| Current `target_type` consumers | **UNKNOWN** — no authoritative indexed consumer evidence |
| Historical provenance | **CONFIRMED** — schema created in commit 6611a3f; broad prose contract created in commit 03a1831 |
| Smart Note target | **CANONICAL / LIVE SEMANTIC OWNER** via NAYA LINK IDENTITY + INT-001 + Contract 02 |
| Ledger event target | **SEPARATE CANONICAL NOUN/SCHEMA**, not Smart Link |
| Value event target | **SEPARATE CANONICAL NOUN/SCHEMA**, not Smart Link |
| Collective intelligence target | **NO verified Smart Link consumer found; separate Collective Intelligence artifacts exist** |
| Generic-link concept | **EXISTED HISTORICALLY** in Contract 48, but newer canonical law explicitly narrows the Smart Link noun; historical broader meaning requires supersession/reconciliation, not silent coexistence |

### Safety determination

**Narrowing `target_type` is NOT yet proven safe.** There is insufficient authoritative dependency evidence to claim that no implementation, fixture, generated artifact, or historical compatibility path consumes the broad enum.

Therefore **NO schema mutation was made**.

The smallest safe reconciliation is documentation/topology-level classification: the broad JSON is now treated as a **MACHINE SCHEMA / NARROW-MERGE CANDIDATE**, while the canonical Smart Link semantic owner is the newer narrow contract family. This does not break any demonstrated live consumer because no live consumer was demonstrated; it also avoids claiming that absence from search proves safety.

### Disposition of broad schema

**MERGE / NARROW CANDIDATE — NOT RETIRED YET.**

Do not create a replacement Smart Link contract. If dependency evidence later proves the broad enum unused, narrow this existing schema in place to the canonical `smart_note` target (or retire the redundant machine schema only if the canonical machine representation is explicitly established elsewhere). If a live consumer is discovered, reconcile that consumer first.

### Validation

The existing Smart Link identity test suite is structurally consistent with the narrow definition: Hub Deep Links, wrong-IB links, and generic GitHub pages are rejected; a canonical Smart Note URL is accepted. However, this audit did not execute GitHub Actions or local test runtime, so **test execution status = UNKNOWN**, not PASS.

### Hard stops preserved

- Constitutional authority untouched.
- No replacement Smart Link contract created.
- No schema narrowing performed without dependency proof.
- UNKNOWN was not converted to PASS.
- BLOCKS / EP-001 / BATON topology preserved.

### Next authorized P0

**SMART-LINK-DEPENDENCY-002 — AUTHORITATIVE REFERENCE SWEEP:** obtain complete repository bytes through a source that permits whole-tree materialization (local clone/authorized workspace or equivalent), then run exact literal-reference scans for `SMART-LINK-CONTRACT.json`, `nayanet://contracts/smart-link-v1`, `target_type`, and each enum value across source, tests, workflows, fixtures, generated artifacts, and historical compatibility surfaces. Reconcile any discovered consumer before changing the schema.


## SMART-LINK-DEPENDENCY-002 — AUTHORITATIVE WHOLE-TREE SWEEP RECEIPT

**Date:** 2026-09-26
**Authoritative source:** authorized local Git clone at `C:\\Users\\Admin\\NayaPOWER`, inspected with exact `git grep` and `git log --all -S` against repository HEAD/history. Local working tree has unrelated uncommitted changes; no local changes were used as dependency evidence except the generated sweep artifact, which was excluded from the tracked grep target.

### Proven live dependencies

1. **Live implementation dependency:** `.naya/runtime/smart_ledger_engine.py:138-145` defines `generate_smart_link(target_type, target_ref,...)` and accepts all four broad targets: `smart_note`, `ledger_event`, `value_event`, `collective_intelligence`.
2. **Live vertical-slice dependency:** `.naya/runtime/smart_ledger_engine.py:192` generates a Smart Link with `target_type=ledger_event`.
3. **Executable test dependency:** `.naya/runtime/test_smart_ledger_engine.py:27,61` asserts and invokes `ledger_event` Smart Links.
4. **Duplicate machine schema:** `.naya/contracts/schemas/SMART-LINK-CONTRACT.json` independently defines Smart Link V1 with targets `ledger_event`, `smart_note`, `verification_receipt`, `value_event`, `collective_intelligence`.
5. **Canonical primary machine schema:** `.naya/contracts/SMART-LINK-CONTRACT.json` defines `nayanet://contracts/smart-link-v1` and the four-target enum.
6. **Relationship registry:** `.naya/control-plane/RELATIONSHIP-INDEX.json` references both Smart Link schema paths.

### Target-type classification

- `smart_note`: LIVE/CANONICAL. It is the newer canonical Smart Link semantic target.
- `ledger_event`: LIVE. The current Smart Ledger engine generates it and the executable unit test asserts it.
- `value_event`: LIVE AS A GENERATED DATA TYPE; no direct Smart Link test was found beyond the engine's accepted enum. A dedicated Value Event schema exists.
- `collective_intelligence`: LIVE AS A DOMAIN/PROJECTION; no direct Smart Link generation/test consumer was found. It must not be called an actual Smart Link consumer solely from domain references.
- `verification_receipt`: LIVE only in the duplicate schema's enum; no corresponding consumer was established in this sweep.

### Generic-link finding

A generic link concept is **real and executable in the current repository**, not merely historical: `generate_smart_link` is a live function parameterized by `target_type`. The older Contract 48 broad concept also exists historically. Therefore the earlier assumption that the broad enum might be unused is disproven.

### Safety decision

**NARROWING `.naya/contracts/SMART-LINK-CONTRACT.json` to `smart_note` is NOT SAFE at this time.** Doing so without first reconciling the live `generate_smart_link(...)` behavior and its test would create a schema/runtime contradiction and break the current vertical slice. No schema mutation was made.

The correct next architectural action is **reconcile the existing generic Smart Link implementation and duplicate schema against the newer canonical Smart Link semantic**, without creating a replacement contract. This requires deciding whether the generic runtime function should be retired/renamed/re-scoped and whether the duplicate schema is historical, supporting, or a merge candidate. That decision must preserve the one-noun/one-owner boundary and avoid silently breaking existing ledger/value projections.

### History evidence

`git log --all -S` confirms `target_type` and `generate_smart_link` entered with the Smart Link/Smart Ledger vertical slice and persisted through subsequent repository restoration/runtime work. This is therefore not an orphaned documentation-only artifact.

### Verification

- Whole-tree authoritative scan: **PASS** for the accessible local clone scope.
- Historical search across reachable refs: **PASS** for the inspected paths/terms.
- Live generic Smart Link dependency: **CONFIRMED**.
- Safe narrowing: **FAIL / NOT SAFE**.
- Schema mutation: **NONE**.
- Runtime/test reconciliation: **PENDING**.
- JSON validation after mutation: **N/A — no mutation**.
- Full repository test execution: **UNKNOWN** (not run in this wave).
- Constitutional authority: **UNCHANGED**.
- BLOCKS/EP-001/BATON topology: **PRESERVED**.

### Exact next action

**SMART-LINK-RECONCILIATION-001:** reconcile the existing `generate_smart_link` runtime/test path and both existing Smart Link schemas against the canonical narrow Smart Link law. Establish one canonical machine owner, one semantic owner, and an explicit disposition for generic ledger/value/collective targets. Do not create a replacement Smart Link contract; do not change constitutional authority; do not delete a live dependency until its callers/tests are migrated or explicitly retired with evidence.
