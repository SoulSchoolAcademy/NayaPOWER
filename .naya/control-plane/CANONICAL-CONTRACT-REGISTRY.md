# CANONICAL CONTRACT REGISTRY

**Status:** LIVE  
**Version:** 1.1-V2-GOVERNANCE-CANDIDATE  
**Authority:** NayaPOWER Control Plane  
**Purpose:** Map every contract in the NayaPOWER contract stack to its canonical source, authority, dependencies, and current status. This registry is the single navigational home for the contract system.

---

## 0. HOW TO USE THIS REGISTRY

Each entry maps:
- **Contract ID** → unique identifier
- **Canonical Name** → official contract name
- **Purpose** → what the contract governs
- **Authority** → what higher authority governs this contract
- **Source** → canonical file path(s)
- **Dependencies** → other contracts this depends on
- **Inputs** → what the contract consumes
- **Outputs** → what the contract produces
- **Invariants** → key normative rules
- **Acceptance** → how the contract is verified
- **Status** → PROVEN / PARTIAL / UNPROVEN / BLOCKED / MISSING
- **Conflicts** → contradictions with other contracts
- **Gaps** → what's missing from the 24-point checklist

---

## WAVE 1 — CONSTITUTIONAL CORE

### CC-000: NayaNET Constitutional Contract Law

| Field | Value |
|---|---|
| **Contract ID** | CC-000 |
| **Canonical Name** | NayaNET Constitutional Contract Law |
| **Purpose** | Supreme governing contract law from which all subsequent NayaNET contracts derive their operating discipline |
| **Authority** | Human-director constitutional authority; ratified 1.0 baseline remains in force while V2 is reviewed |
| **Source** | `.naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md` |
| **Dependencies** | None as normative law; machine governance depends on schema, registry, enforcement registry, decision procedure, and acceptance suite |
| **Inputs** | Human authority, platform/safety/legal constraints, live control-plane state |
| **Outputs** | Constitutional law, deterministic decision procedure, action classes, enforcement model, cold-Naya reachability requirements |
| **Invariants** | CAPABILITY DOES NOT CREATE AUTHORITY; UNKNOWN ≠ PASS; ONE SYSTEM ONE LAW; Receiver-centric durable intelligence; Privacy by default; claim strength MUST NOT exceed evidence |
| **Acceptance** | V2 self-governance suite, machine-schema validation, enforcement registry, boot reachability, cold-Naya tests, runtime/production evidence |
| **Status** | **CANDIDATE** — V2 specification and machine governance artifacts added; operational ratification is blocked pending self-governance and reachability evidence |
| **Conflicts** | Constitutional identity/authority audit remains **CONFLICTED** until all self-declared constitutional artifacts are mapped and supersession is explicit |
| **Gaps** | Cold-Naya boot enforcement, executable self-governance suite, runtime enforcement receipts, final constitutional supersession decision |

---

### CC-001: Contract Stack Operating Law

| Field | Value |
|---|---|
| **Contract ID** | CC-001 |
| **Canonical Name** | Contract Stack Operating Law V1 |
| **Purpose** | Meta-governance framework ensuring all contracts are treated as binding subsystem law |
| **Authority** | CC-000 (Constitutional Contract Law; V2 candidate under review) |
| **Source** | `.naya/contracts/00-CONTRACT-STACK-OPERATING-LAW.md` |
| **Dependencies** | CC-000 |
| **Inputs** | All contracts in `.naya/contracts/` |
| **Outputs** | 9-level authority precedence, anti-guessing law, layer separation, proof law |
| **Invariants** | Lower authority MUST NOT silently override higher authority; UNKNOWN/BLOCKED/PENDING/CONFLICTED may never be rewritten as PASS; Anti-guessing law; Layer separation |
| **Acceptance** | Every contract MUST define acceptance tests; positive and adversarial tests for critical MUSTs |
| **Status** | **PARTIAL** — Well-defined meta-law but no acceptance tests for the operating law itself |
| **Conflicts** | None |
| **Gaps** | No contract ID; no explicit inputs/outputs; no state machine; no receipt format |

---

### CC-002: Mission / Purpose / Success

| Field | Value |
|---|---|
| **Contract ID** | CC-002 |
| **Canonical Name** | Mission, Purpose, and Success Contract |
| **Purpose** | Defines why NayaPOWER exists, what problem it solves, the North Star, and genuine success |
| **Authority** | CC-000 |
| **Source** | Distributed across: `STATE.json` (mission/north_star), `.naya/codex/NAYA-POWER-MASTER-CONSTITUTIONAL-CHARTER-V1.md`, `.naya/codex/NAYA-FUTURE-SELF-MASTER-DIRECTIVE.md` |
| **Dependencies** | CC-000, CC-001 |
| **Inputs** | Human vision, constitutional principles |
| **Outputs** | Mission statement, North Star, success criteria |
| **Invariants** | Working governed intelligence system ≠ documentation/features/tests/deployments/activity |
| **Acceptance** | Cold Naya can state mission without conversation; success is measurable |
| **Status** | **PARTIAL** — Mission is defined in STATE.json but no single canonical contract file exists |
| **Conflicts** | Mission is distributed across multiple files without a single canonical source |
| **Gaps** | No single canonical file; no formal acceptance tests; no machine-readable schema |

---

### CC-003: Identity & Continuity (14-Question Interface)

| Field | Value |
|---|---|
| **Contract ID** | CC-003 |
| **Canonical Name** | Identity & Continuity Contract (14-Question Cold-Successor Interface) |
| **Purpose** | Defines how Naya establishes WHO am I, WHO is the human, WHAT system, WHAT authority, WHAT is true, WHAT is unknown, WHAT is next, HOW does another Naya inherit |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/10-CONTINUITY-SUCCESSOR.md`, `.naya/control-plane/BATON.json`, `.naya/control-plane/BATON-CONTRACT.md` |
| **Dependencies** | CC-000, CC-001 |
| **Inputs** | Canonical sources (STATE/BLOCKS/MAP/PROOF/BATON) |
| **Outputs** | 14-question reconstruction, cold-successor sequence, handoff law |
| **Invariants** | Naya must not require Shawn to reconstruct current reality; Baton is pointer to canonical truth, not competing truth store |
| **Acceptance** | Cold Naya answers all 14 questions from canonical sources; identifies same active frontier |
| **Status** | **PARTIAL** — Well-defined but acceptance tests not implemented as executable tests |
| **Conflicts** | Overlap with EP-001 (Execution Protocol) on handoff format |
| **Gaps** | No formal acceptance tests; no machine-readable schema; no explicit dependency declarations |

---

### CC-004: Authority / Consent / Scope

| Field | Value |
|---|---|
| **Contract ID** | CC-004 |
| **Canonical Name** | Authority, Consent, and Scope Contract |
| **Purpose** | Defines who can authorize what, scope, delegation, inheritance, consent, expiration, revocation, capability boundaries |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/07-SMARTCONNECT.md`, `.naya/codex/11-RUNTIME-CONSTITUTION.md` (L0-L3 authority model), `supabase/migrations/20260924110000_wire_authority_grant_into_intelligence_commit_v1.sql` |
| **Dependencies** | CC-000, CC-001 |
| **Inputs** | Human authority, constitutional principles |
| **Outputs** | Authority model (L0-L3), consent boundaries, revocation protocol |
| **Invariants** | CAPABILITY DOES NOT CREATE AUTHORITY; Private by default; Shared by choice; Collective by consent; Public by decision |
| **Acceptance** | Connection establishes only intended participation state; cannot manufacture execution authority |
| **Status** | **PARTIAL** — Well-defined principles but distributed across multiple files |
| **Conflicts** | SmartConnect vs Smart Share terminology inconsistency |
| **Gaps** | No single canonical file; no formal acceptance tests; no machine-readable schema |

---

### CC-005: Execution Protocol

| Field | Value |
|---|---|
| **Contract ID** | EP-001 |
| **Canonical Name** | NayaNET Execution Protocol Contract |
| **Purpose** | Turns Naya from passive responder into proactive, outcome-oriented execution partner |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/02-GOVERNANCE-AND-FLOW/01-EXECUTION-PROTOCOL.md` |
| **Dependencies** | CC-000, CC-001, CC-003 |
| **Inputs** | Authorized objective, canonical sources |
| **Outputs** | Continuous action loop, evidence preservation, continuation handoff |
| **Invariants** | Execution Prime Directive; Continuous verified progress ≠ continuous activity; Outcome before output; Tune in before executing |
| **Acceptance** | 11 behavioral tests (A-K); 20 adversarial questions |
| **Status** | **PARTIAL** — Comprehensive but status is PROPOSED (not RATIFIED); acceptance tests not implemented |
| **Conflicts** | Overlap with CC-003 (Continuity/Successor) on handoff format; overlap with Runtime Constitution on proactive execution |
| **Gaps** | No formal implementation of acceptance tests; no state machine; no machine-readable schema |

---

## WAVE 2 — INTELLIGENCE CORE

### CC-006: Intelligent Block / Intelligence Object

| Field | Value |
|---|---|
| **Contract ID** | CC-006 |
| **Canonical Name** | Smart Note / Intelligent Block V1 |
| **Purpose** | Defines the canonical durable intelligence identity (Intelligent Block) and its human-readable projection (Smart Note) |
| **Authority** | CC-000, CC-001 |
| **Source** | `.naya/contracts/01-SMART-NOTE-INTELLIGENT-BLOCK.md`, `.naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md` |
| **Dependencies** | CC-000, CC-001, CC-003 |
| **Inputs** | Source intelligence event, receiver-allocated IB identity |
| **Outputs** | Canonical IB identity, Smart Note projection |
| **Invariants** | ONE IB → MANY AUTHORIZED PROJECTIONS; Receiver owns canonical IB identity; No local agent may invent IB IDs |
| **Acceptance** | Smart Note creation uses Receiver-created identity; Markdown without receiver event is not canonical proof |
| **Status** | **PARTIAL** — Well-defined but no explicit status, no contract ID, acceptance tests not implemented |
| **Conflicts** | Potential overlap with INT-001 on Smart Link boundary |
| **Gaps** | No formal acceptance tests; no state machine; no explicit dependency declarations |

---

### CC-007: Smart Note Projection

| Field | Value |
|---|---|
| **Contract ID** | INT-001 |
| **Canonical Name** | NayaNET Smart Note + Smart Link Contract |
| **Purpose** | Makes durable intelligence understandable and navigable without semantic ambiguity |
| **Authority** | CC-000, CC-001, CC-006 |
| **Source** | `.naya/contracts/01-INTELLIGENCE/01-SMART-NOTE-AND-SMART-LINK.md` |
| **Dependencies** | CC-000, CC-006 |
| **Inputs** | Canonical IB, repository projection |
| **Outputs** | Smart Note projection, Smart Link |
| **Invariants** | ONE CANONICAL IB → ONE HUMAN-READABLE SMART NOTE → ONE EXACT SMART LINK; Smart Link ≠ Hub Deep Link ≠ Evidence Link |
| **Acceptance** | 8 acceptance tests (A-H); 6 evidence requirements for VERIFIED Smart Link |
| **Status** | **PARTIAL** — Most comprehensive Smart Note/Smart Link contract but status is PROPOSED |
| **Conflicts** | Overlap with CC-006 on IB identity boundary |
| **Gaps** | No formal implementation of acceptance tests; no state transition rules |

---

### CC-008: Provenance / Lineage

| Field | Value |
|---|---|
| **Contract ID** | CC-008 |
| **Canonical Name** | Provenance and Lineage Contract |
| **Purpose** | Preserves ACTOR → AUTHORITY → ACTION → EVENT → EVIDENCE → INTELLIGENCE → PROJECTION → RETRIEVAL → APPLICATION → OUTCOME |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/08-PROOF-RECEIPT.md`, `.naya/contracts/schemas/CAUSAL-VERIFICATION-OBJECT-SCHEMA.json` |
| **Dependencies** | CC-000, CC-006 |
| **Inputs** | Execution receipts, cognition events, evidence |
| **Outputs** | Provenance chain, lineage verification |
| **Invariants** | Where did this come from? Who authorized it? What happened? What evidence proves it? |
| **Acceptance** | Causal claims require explicit causal-evidence boundary |
| **Status** | **PARTIAL** — Well-defined framework but no runtime evidence references |
| **Conflicts** | None |
| **Gaps** | No formal acceptance tests; no machine-readable schema; no receipt format |

---

### CC-009: Intelligent Event / Event Lifecycle

| Field | Value |
|---|---|
| **Contract ID** | CC-009 |
| **Canonical Name** | Intelligent Event / Event Lifecycle Contract |
| **Purpose** | Defines the event substrate: CAPTURE → CANONICALIZE → STRUCTURE → PRESERVE → INDEX → RETRIEVE → APPLY |
| **Authority** | CC-000 |
| **Source** | `SUPERBRAIN/INTELLIGENCE/COLLECTIVE-INTELLIGENCE-EVENT-SCHEMA.md`, `.naya/contracts/SMART-LEDGER-EVENT-SCHEMA.json` |
| **Dependencies** | CC-000, CC-006, CC-008 |
| **Inputs** | Source events from senders |
| **Outputs** | Canonical events, indexed events |
| **Invariants** | Event ≠ IB; IB ≠ Learning; Learning label ≠ Verified Learning |
| **Acceptance** | Event → IB → persistence is traceable |
| **Status** | **PARTIAL** — Defined but distributed across multiple files |
| **Conflicts** | None |
| **Gaps** | No single canonical file; no formal acceptance tests; no state machine |

---

### CC-010: Smart Ledger

| Field | Value |
|---|---|
| **Contract ID** | CC-010 |
| **Canonical Name** | Smart Ledger / CCT Machine Contract V1 |
| **Purpose** | Lineage and accountability — not intelligence itself. Records what happened and how intelligence relates to those events |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/SMART-LEDGER-CCT-MACHINE-CONTRACT-V1.md`, `.naya/contracts/SMART-LEDGER-EVENT-SCHEMA.json` |
| **Dependencies** | CC-000, CC-008, CC-009 |
| **Inputs** | Ledger events, evidence, verification receipts |
| **Outputs** | Integrity-chained durable event record |
| **Invariants** | Ledger event records that an event occurred; it does not claim that the event is valuable or true; CCT is not blockchain technology |
| **Acceptance** | No component is considered implemented merely because its source exists |
| **Status** | **UNPROVEN** — Explicitly states "CONTRACT DEFINED — RUNTIME NOT YET VERIFIED" |
| **Conflicts** | None |
| **Gaps** | No runtime evidence; no test run IDs; no evidence registry |

---

## WAVE 3 — RETRIEVAL & TRUTH

### CC-011: Smart Link

| Field | Value |
|---|---|
| **Contract ID** | CC-011 |
| **Canonical Name** | Smart Link V1 |
| **Purpose** | Defines the exact semantic meaning and verification of the canonical human-readable Smart Link |
| **Authority** | CC-000, CC-006 |
| **Source** | `.naya/contracts/02-SMART-LINK.md`, `.naya/contracts/schemas/SMART-LINK-CONTRACT.json` |
| **Dependencies** | CC-000, CC-006, CC-007 |
| **Inputs** | Canonical IB, repository projection |
| **Outputs** | Verified Smart Link |
| **Invariants** | SMART LINK = direct navigable GitHub link to canonical smart-note.md; Smart Link ≠ Hub Deep Link ≠ Evidence Link |
| **Acceptance** | 5-condition verification gate |
| **Status** | **PARTIAL** — Clear definition but acceptance tests not implemented |
| **Conflicts** | Duplication with INT-001 (both define Smart Link) |
| **Gaps** | No formal acceptance tests; no state machine; no explicit dependency declarations |

---

### CC-012: Retrieval / Applicability

| Field | Value |
|---|---|
| **Contract ID** | CC-012 |
| **Canonical Name** | Retrieval and Applicability Contract |
| **Purpose** | Retrieval must mean: Retrieve the right intelligence for this situation, with sufficient provenance, authority, status, scope, freshness, and applicability |
| **Authority** | CC-000 |
| **Source** | Distributed across: `.naya/contracts/09-LEARNING.md`, `.naya/contracts/05-HUB-CONSUMPTION.md`, `supabase/functions/nayanet-compound-intelligence/index.ts` |
| **Dependencies** | CC-000, CC-006, CC-008 |
| **Inputs** | Query, context, applicability scope |
| **Outputs** | Retrieved intelligence with provenance |
| **Invariants** | Retrieval ≠ "Find something similar"; must have sufficient provenance, authority, status, scope, freshness |
| **Acceptance** | Retrieved intelligence has complete provenance chain |
| **Status** | **PARTIAL** — No single canonical contract file exists |
| **Conflicts** | Distributed across multiple files without canonical source |
| **Gaps** | No single canonical file; no formal acceptance tests; no machine-readable schema |

---

### CC-013: Truth-State / Evidence

| Field | Value |
|---|---|
| **Contract ID** | CC-013 |
| **Canonical Name** | Truth-State and Evidence Contract |
| **Purpose** | Defines the canonical truth state machine: VERIFIED, PENDING, MISSING, CONFLICTED, UNKNOWN |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/08-PROOF-RECEIPT.md`, `.naya/control-plane/PROOF.json` |
| **Dependencies** | CC-000 |
| **Inputs** | Evidence, verification results |
| **Outputs** | Truth state classification |
| **Invariants** | UNKNOWN ≠ VERIFIED; BLOCKED ≠ PASS; IMPLEMENTED ≠ VERIFIED; VERIFIED ≠ PRODUCTION_PROVEN |
| **Acceptance** | Truth states are distinguishable and enforceable |
| **Status** | **PARTIAL** — Well-defined in PROOF.json but no single canonical contract file |
| **Conflicts** | None |
| **Gaps** | No single canonical file; no formal acceptance tests; no state transition rules |

---

### CC-014: Causal Verification Object

| Field | Value |
|---|---|
| **Contract ID** | CC-014 |
| **Canonical Name** | Causal Verification Object Contract |
| **Purpose** | Connects CLAIM → INTENDED ACTION → ACTUAL EXECUTION → OBSERVED RESULT → CAUSAL EVIDENCE → DECISION |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/schemas/CAUSAL-VERIFICATION-OBJECT-SCHEMA.json` |
| **Dependencies** | CC-000, CC-008 |
| **Inputs** | Intent, authority, action, observation, evidence |
| **Outputs** | Causal verification object with status |
| **Invariants** | A green test alone is not automatically causal proof; causal_status enum: VERIFIED, PARTIAL, REJECTED, BLOCKED |
| **Acceptance** | Causal claims require explicit causal-evidence boundary |
| **Status** | **PARTIAL** — Schema exists but learning.refs items lack type constraints |
| **Conflicts** | None |
| **Gaps** | No acceptance criteria; no dependency declarations; no temporal/ordering constraints |

---

### CC-015: Verified AI Action

| Field | Value |
|---|---|
| **Contract ID** | CC-015 |
| **Canonical Name** | Verified AI Action Contract V1 |
| **Purpose** | Defines when Naya may truthfully state: I performed this action and verified the result |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/VERIFIED-AI-ACTION-V1.md`, `.naya/contracts/schemas/VERIFIED-AI-ACTION-V1-SCHEMA.json` |
| **Dependencies** | CC-000, CC-008, CC-014 |
| **Inputs** | Intent, authority, permission, action, observation, evidence |
| **Outputs** | Verified action claim with 10 proof conditions |
| **Invariants** | REQUESTED → AUTHORIZED → ATTEMPTED → EXECUTED → OBSERVED → VERIFIED → PRODUCTION-PROVEN; No step may silently be promoted |
| **Acceptance** | All 10 proof conditions satisfied for VERIFIED status |
| **Status** | **PARTIAL** — Well-defined proof chain but no formal acceptance tests |
| **Conflicts** | None |
| **Gaps** | No formal acceptance tests; no state machine; no explicit dependency declarations |

---

## WAVE 4 — SAFETY & RATIFICATION

### CC-016: Refusal / Revocation / Replay

| Field | Value |
|---|---|
| **Contract ID** | CC-016 |
| **Canonical Name** | Refusal, Revocation, and Replay Contract |
| **Purpose** | Defines what Naya must do when authority is absent, revoked, conflicting, stale, duplicated, or unsafe |
| **Authority** | CC-000 |
| **Source** | Distributed across: `.naya/contracts/07-SMARTCONNECT.md`, `supabase/migrations/20260924200000_harden_cognition_event_replay_idempotency_v1.sql`, `.naya/contracts/08-PROOF-RECEIPT.md` |
| **Dependencies** | CC-000, CC-004 |
| **Inputs** | Authority state, replay detection |
| **Outputs** | Fail-safe behavior, revocation enforcement |
| **Invariants** | Naya must never fill a missing authority boundary with imagination; replay is idempotent |
| **Acceptance** | Unauthorized request denied before canonical persistence |
| **Status** | **PARTIAL** — Defined but distributed across multiple files |
| **Conflicts** | No single canonical file |
| **Gaps** | No single canonical file; no formal acceptance tests; no state machine |

---

### CC-017: Portable Authorization / Cryptographic Authority

| Field | Value |
|---|---|
| **Contract ID** | CC-017 |
| **Canonical Name** | Portable Authorization Workflow Contract |
| **Purpose** | Defines authorization artifacts, signing, verification, issuer custody, verifier identity, public-key trust |
| **Authority** | CC-000 |
| **Source** | `.naya/control-plane/PORTABLE-AUTHORIZATION-WORKFLOW-CONTRACT.md` |
| **Dependencies** | CC-000, CC-004, CC-005 |
| **Inputs** | Workflow tokens, registry, governance kernel |
| **Outputs** | Portable authorization artifact |
| **Invariants** | Capability does not create authority; runner holds ONLY the pinned public key; no step may be skipped |
| **Acceptance** | 12-step verification sequence must complete before any side effect |
| **Status** | **UNPROVEN** — Explicitly states "CONTRACT ONLY — NOT WIRED" |
| **Conflicts** | None |
| **Gaps** | No implementation; no evidence; no machine-readable schema for the artifact |

---

### CC-018: Verification & Acceptance

| Field | Value |
|---|---|
| **Contract ID** | CC-018 |
| **Canonical Name** | Verification and Acceptance Contract |
| **Purpose** | Defines: SPECIFIED → IMPLEMENTED → TESTED → VERIFIED → INDEPENDENTLY VERIFIED → PRODUCTION PROVEN → RATIFIED |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/08-PROOF-RECEIPT.md`, `.naya/control-plane/PROOF.json` |
| **Dependencies** | CC-000, CC-013 |
| **Inputs** | Evidence, test results, runtime observations |
| **Outputs** | Verification status, acceptance determination |
| **Invariants** | No status inflation; evidence determines the tier |
| **Acceptance** | Untested implementation cannot be reported verified |
| **Status** | **PARTIAL** — Well-defined framework but no single canonical contract file |
| **Conflicts** | None |
| **Gaps** | No single canonical file; no formal acceptance tests |

---

### CC-019: Ratification / Release Authority

| Field | Value |
|---|---|
| **Contract ID** | CC-019 |
| **Canonical Name** | Ratification and Release Authority Contract |
| **Purpose** | Naya can prove. Naya can prepare. Naya can recommend. Human authority ratifies. |
| **Authority** | CC-000 |
| **Source** | `.naya/codex/11-RUNTIME-CONSTITUTION.md` (L3 authority), `.naya/control-plane/RELEASE-AUTHORIZATION.json` |
| **Dependencies** | CC-000, CC-004 |
| **Inputs** | Human decision, technical evidence |
| **Outputs** | Ratified release |
| **Invariants** | Technical evidence must never silently become human approval |
| **Acceptance** | Human ratification required for release |
| **Status** | **PARTIAL** — Defined but no single canonical contract file |
| **Conflicts** | None |
| **Gaps** | No single canonical file; no formal acceptance tests; no machine-readable schema |

---

## WAVE 5 — LEARNING & CONTINUITY

### CC-020: Learning Loop

| Field | Value |
|---|---|
| **Contract ID** | CC-020 |
| **Canonical Name** | Learning Loop Contract |
| **Purpose** | Defines: OUTCOME → OBSERVATION → LESSON CANDIDATE → VALIDATION → PROMOTION → INTELLIGENCE → FUTURE APPLICATION |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/09-LEARNING.md` |
| **Dependencies** | CC-000, CC-006 |
| **Inputs** | Observed outcomes, evidence |
| **Outputs** | Verified learning, promoted intelligence |
| **Invariants** | CANDIDATE ≠ VERIFIED INTELLIGENCE; Behavior-change law: RETRIEVE → UNDERSTAND → APPLY DIFFERENTLY → OBSERVE OUTCOME → VERIFY |
| **Acceptance** | Event alone is not verified learning; learning label alone is not behavior-change proof |
| **Status** | **PARTIAL** — Clear conceptual framework but acceptance tests not implemented |
| **Conflicts** | None |
| **Gaps** | No formal acceptance tests; no state machine; no explicit dependency declarations |

---

### CC-021: Promotion / Reconciliation

| Field | Value |
|---|---|
| **Contract ID** | CC-021 |
| **Canonical Name** | Promotion and Reconciliation Contract |
| **Purpose** | Defines how the system handles candidate intelligence, corroboration, conflicts, supersession, reconciliation, promotion, demotion, retirement |
| **Authority** | CC-000 |
| **Source** | Distributed across: `.naya/contracts/09-LEARNING.md`, `supabase/functions/nayanet-compound-intelligence/index.ts` (reconcile action) |
| **Dependencies** | CC-000, CC-020 |
| **Inputs** | Learning candidates, conflicts |
| **Outputs** | Promoted/demoted/retired intelligence |
| **Invariants** | The system cannot simply accumulate contradictory assertions forever |
| **Acceptance** | Conflicting evidence keeps the candidate appropriately qualified |
| **Status** | **PARTIAL** — No single canonical contract file exists |
| **Conflicts** | Distributed without canonical source |
| **Gaps** | No single canonical file; no formal acceptance tests; no state machine |

---

### CC-022: Cold Successor / Intelligence Inheritance

| Field | Value |
|---|---|
| **Contract ID** | CC-022 |
| **Canonical Name** | Cold Successor / Intelligence Inheritance Contract |
| **Purpose** | Ensures inheritance of current understanding and executable continuation by a cold Naya |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/10-CONTINUITY-SUCCESSOR.md`, `.naya/control-plane/BATON.json` |
| **Dependencies** | CC-000, CC-003, CC-005 |
| **Inputs** | Canonical sources, baton |
| **Outputs** | Restored understanding, continued execution |
| **Invariants** | RETRIEVE → UNDERSTAND → DECIDE → ACT DIFFERENTLY/CORRECTLY without inherited conversation context |
| **Acceptance** | Cold Naya can restore relevant state from canonical sources and continue |
| **Status** | **PARTIAL** — Well-defined but acceptance tests not implemented |
| **Conflicts** | Overlap with EP-001 on handoff format |
| **Gaps** | No formal acceptance tests; no machine-readable schema |

---

### CC-023: Handoff / Baton / Next-Naya

| Field | Value |
|---|---|
| **Contract ID** | CC-023 |
| **Canonical Name** | Handoff / Baton / Next-Naya Contract |
| **Purpose** | Defines the machine-readable continuation state |
| **Authority** | CC-000 |
| **Source** | `.naya/control-plane/BATON-CONTRACT.md`, `.naya/control-plane/NAYA-CONTINUOUS-EXECUTION-POLICY.md` |
| **Dependencies** | CC-000, CC-003, CC-005 |
| **Inputs** | Current state, evidence, authority |
| **Outputs** | Baton with one next action |
| **Invariants** | Baton binds: CURRENT STATE, CURRENT INTELLIGENCE, PROVEN/UNKNOWN, ACTIVE BLOCK, ONE NEXT ACTION, EVIDENCE, SUCCESSOR PROMPT, PLAYBACK POINTER |
| **Acceptance** | Cold Naya can load baton, resolve sources, understand state, execute one next action |
| **Status** | **PARTIAL** — Well-defined but automation target not complete |
| **Conflicts** | None |
| **Gaps** | No formal acceptance tests; no machine-readable schema; automation not complete |

---

## WAVE 6 — SYSTEM & PRODUCTION

### CC-024: NayaNET Architecture

| Field | Value |
|---|---|
| **Contract ID** | CC-024 |
| **Canonical Name** | NayaNET Architecture Contract |
| **Purpose** | Defines the topology: NayaPOWER → NayaNET → Intelligence Substrate → Receivers → Hub → Human |
| **Authority** | CC-000 |
| **Source** | `.naya/codex/NAYA-POWER-SYSTEM-ARCHITECTURE-WHITE-PAPER-V1.md`, `SUPERBRAIN/MASTER-NOTES/NAYAPOWER-CANONICAL-SOURCE-MAP.md` |
| **Dependencies** | CC-000, CC-001 |
| **Inputs** | Architectural principles |
| **Outputs** | Topology, boundaries, prevent architectural drift |
| **Invariants** | NayaPOWER → NayaNET → Intelligence Substrate → Receivers → Hub → Human |
| **Acceptance** | Architecture prevents drift |
| **Status** | **PARTIAL** — Defined but distributed across multiple files |
| **Conflicts** | No single canonical file |
| **Gaps** | No single canonical file; no formal acceptance tests |

---

### CC-025: Hub Master Design / Experience

| Field | Value |
|---|---|
| **Contract ID** | CC-025 |
| **Canonical Name** | NayaNET Hub Visual & Structural Contract |
| **Purpose** | The Hub is the human cockpit / receiver / visual brain — not the source of truth |
| **Authority** | CC-000 |
| **Source** | `.naya/contracts/NAYANET-HUB-VISUAL-STRUCTURAL-CONTRACT.md`, `.naya/contracts/05-HUB-CONSUMPTION.md`, `.naya/contracts/06-ROOM.md` |
| **Dependencies** | CC-000, CC-006, CC-007 |
| **Inputs** | Canonical intelligence, Hub surfaces |
| **Outputs** | Human-facing projections |
| **Invariants** | Hub is a projection surface, not a second brain; NAYANET/HUB/index.html is the protected reference |
| **Acceptance** | Per-surface evidence; OPEN → UNDERSTAND → NAVIGATE → SEARCH → CREATE → SAVE → SEE → RELOAD → FIND → UNDERSTAND EVIDENCE → CONTINUE |
| **Status** | **PARTIAL** — Per-surface evidence provided; most surfaces browser-proven only |
| **Conflicts** | None |
| **Gaps** | No formal acceptance tests; no state machine; no machine-readable schema |

---

### CC-026: Production / Deployment Parity

| Field | Value |
|---|---|
| **Contract ID** | CC-026 |
| **Canonical Name** | Production and Deployment Parity Contract |
| **Purpose** | Defines SOURCE → BUILD → ARTIFACT → DEPLOYMENT → RUNTIME and proves correspondence |
| **Authority** | CC-000 |
| **Source** | `.naya/control-plane/DEPLOYMENT-GOVERNANCE.json`, `.naya/runtime/deployment_verification.py` |
| **Dependencies** | CC-000, CC-018 |
| **Inputs** | Source code, build artifacts, deployment |
| **Outputs** | Parity proof |
| **Invariants** | Production runtime evidence cannot be substituted with source-level evidence |
| **Acceptance** | Source identity, deployment identity, runtime identity all correspond |
| **Status** | **PARTIAL** — Deployment verification script exists but no single canonical contract file |
| **Conflicts** | No single canonical file |
| **Gaps** | No single canonical file; no formal acceptance tests |

---

### CC-027: CI / Full-Suite Evidence

| Field | Value |
|---|---|
| **Contract ID** | CC-027 |
| **Canonical Name** | CI / Full-Suite Evidence Contract |
| **Purpose** | Defines what constitutes genuine repository-wide execution evidence |
| **Authority** | CC-000 |
| **Source** | Distributed across: `.naya/codex/NAYA-POWER-UNIVERSAL-OPERATING-PROTOCOL-V1.md`, `.naya/control-plane/GOVERNANCE-KERNEL.json` |
| **Dependencies** | CC-000, CC-018 |
| **Inputs** | CI runs, workflow evidence |
| **Outputs** | Full-suite evidence |
| **Invariants** | Until a genuine runner/workflow produces the required evidence: CI = UNKNOWN, not PASS |
| **Acceptance** | Genuine runner/workflow produces required evidence |
| **Status** | **PARTIAL** — Defined but no single canonical contract file |
| **Conflicts** | No single canonical file |
| **Gaps** | No single canonical file; no formal acceptance tests |

---

## SUMMARY STATUS TABLE

| Contract ID | Name | Status | Wave |
|---|---|---|---|
| CC-000 | Constitutional Contract Law | PARTIAL | 1 |
| CC-001 | Contract Stack Operating Law | PARTIAL | 1 |
| CC-002 | Mission / Purpose / Success | PARTIAL | 1 |
| CC-003 | Identity & Continuity (14Q) | PARTIAL | 1 |
| CC-004 | Authority / Consent / Scope | PARTIAL | 1 |
| EP-001 | Execution Protocol | PARTIAL | 1 |
| CC-006 | Intelligent Block / IB | PARTIAL | 2 |
| INT-001 | Smart Note + Smart Link | PARTIAL | 2 |
| CC-008 | Provenance / Lineage | PARTIAL | 2 |
| CC-009 | Intelligent Event Lifecycle | PARTIAL | 2 |
| CC-010 | Smart Ledger / CCT | UNPROVEN | 2 |
| CC-011 | Smart Link | PARTIAL | 3 |
| CC-012 | Retrieval / Applicability | PARTIAL | 3 |
| CC-013 | Truth-State / Evidence | PARTIAL | 3 |
| CC-014 | Causal Verification Object | PARTIAL | 3 |
| CC-015 | Verified AI Action | PARTIAL | 3 |
| CC-016 | Refusal / Revocation / Replay | PARTIAL | 4 |
| CC-017 | Portable Authorization | UNPROVEN | 4 |
| CC-018 | Verification & Acceptance | PARTIAL | 4 |
| CC-019 | Ratification / Release Authority | PARTIAL | 4 |
| CC-020 | Learning Loop | PARTIAL | 5 |
| CC-021 | Promotion / Reconciliation | PARTIAL | 5 |
| CC-022 | Cold Successor | PARTIAL | 5 |
| CC-023 | Handoff / Baton | PARTIAL | 5 |
| CC-024 | NayaNET Architecture | PARTIAL | 6 |
| CC-025 | Hub Master Design | PARTIAL | 6 |
| CC-026 | Production / Deployment Parity | PARTIAL | 6 |
| CC-027 | CI / Full-Suite Evidence | PARTIAL | 6 |

---

## CRITICAL CONFLICTS

1. **CC-002 (Mission) is distributed** — No single canonical file. Mission is scattered across STATE.json, codex files, and master notes.
2. **CC-011 (Smart Link) duplicates INT-001** — Two contracts define Smart Link without explicit reconciliation.
3. **CC-003 (Continuity) overlaps EP-001** — Both define handoff format and successor preparation.
4. **CC-012 (Retrieval) has no canonical file** — Distributed across Learning, Hub Consumption, and compound runtime.
5. **CC-021 (Promotion) has no canonical file** — Distributed across Learning and compound runtime.

---

## CRITICAL GAPS

1. **No contract has a complete 24-point checklist** — Most contracts lack formal acceptance tests, machine-readable schemas, state machines, and explicit dependency declarations.
2. **Only 2 of 27 contracts have evidence registries** — Sender-Receiver Readiness Contract and Hub Visual Structural Contract.
3. **No contract defines state transitions** — Multiple contracts define status enums but none define valid transitions.
4. **No contract has temporal constraints** — No ordering or timing enforcement between events, states, or transitions.
5. **Automation targets not complete** — Continuous Execution Policy and Baton Contract describe automation that is not yet implemented.

---

## DEPENDENCY GRAPH

```
CC-000 (Constitutional Law)
  ├─ CC-001 (Operating Law)
  │   ├─ CC-002 (Mission)
  │   ├─ CC-003 (Identity & Continuity)
  │   ├─ CC-004 (Authority)
  │   └─ EP-001 (Execution Protocol)
  │       ├─ CC-005 (not yet created)
  │       └─ CC-022 (Cold Successor)
  ├─ CC-006 (Intelligent Block)
  │   ├─ INT-001 (Smart Note + Link)
  │   │   └─ CC-011 (Smart Link)
  │   └─ CC-008 (Provenance)
  │       └─ CC-009 (Event Lifecycle)
  │           └─ CC-010 (Smart Ledger)
  ├─ CC-013 (Truth-State)
  │   └─ CC-014 (Causal Verification)
  │       └─ CC-015 (Verified AI Action)
  ├─ CC-016 (Refusal/Revocation)
  ├─ CC-017 (Portable Auth) [UNPROVEN]
  ├─ CC-018 (Verification)
  │   └─ CC-019 (Ratification)
  ├─ CC-020 (Learning)
  │   └─ CC-021 (Promotion)
  └─ CC-024 (Architecture)
      └─ CC-025 (Hub)
          └─ CC-026 (Production Parity)
              └─ CC-027 (CI Evidence)
```

---

## NEXT ACTIONS (Priority Order)

1. **Create CC-002 (Mission) as a single canonical contract file**
2. **Reconcile CC-011 (Smart Link) and INT-001** — supersede one with the other
3. **Create CC-012 (Retrieval) as a single canonical contract file**
4. **Create CC-021 (Promotion) as a single canonical contract file**
5. **Implement acceptance tests for EP-001 (Execution Protocol)**
6. **Wire CC-017 (Portable Authorization) into production workflow**
7. **Implement automation targets for CC-023 (Baton) and CC-018 (Continuous Execution)**
8. **Add machine-readable schemas to all contracts**
9. **Define state transitions for all status enums**
10. **Add temporal constraints to event and verification contracts**

---

[CONTROL PLACE][CONTRACT]
CANONICAL-CONTRACT-REGISTRY-V1
Status: ACTIVE
Next Review: After each contract completion


---

## CONTRACT 00 V2 GOVERNANCE GATE

As of this registry version, CC-000 V2 is the constitutional specification candidate and **must not be treated as operationally ratified merely because its Markdown exists**.

The ratified 1.0 baseline remains the governing baseline until the V2 acceptance gates pass and the Human Director explicitly ratifies V2.

The following are mandatory before Contracts 01–10 may declare themselves fully governed:

1. Constitutional identity conflict resolved and registry-mapped.
2. Contract 00 V2 schema validated.
3. Deterministic decision procedure validated.
4. Enforcement registry present and every critical rule classified.
5. Constitutional self-governance tests pass, including mutation coverage where applicable.
6. Cold-Naya boot reachability is proven.
7. Runtime enforcement evidence exists for claims marked ENFORCED.
8. No specialized contract claims a stronger governance status than its evidence supports.

Until then, downstream contracts remain developable but governance status is limited to the evidence actually established.
