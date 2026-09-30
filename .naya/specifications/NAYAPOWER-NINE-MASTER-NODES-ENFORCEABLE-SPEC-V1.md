# 🔱 NayaPOWER — Nine Master Nodes Enforceable Specification V1

**Status:** RATIFIED OPERATIONAL SPECIFICATION  
**Effective:** 2026-09-26  
**Authority:** NayaPOWER System North Star + NayaNET Constitutional Contract Law  
**Machine manifest:** `.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json`  
**Machine schema:** `.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.schema.json`  
**Static gate:** `scripts/verify-nine-master-nodes.py`

## 1. Purpose

This document converts the ratified nine-node architecture into a normative, testable kernel contract.

The 27 contracts remain the law layer. The nine Master Nodes are the semantic operating layer compiled from that law. Runtime enforcement remains subject to the contracts, the canonical Receiver, live state, evidence, safety requirements, and human authority.

**The kernel is conforming only when the model, manifest, validator, tests, and runtime behavior agree.**

## 2. Normative language

**MUST / REQUIRED** = mandatory.  
**MUST NOT** = prohibited.  
**SHOULD** = recommended unless a higher-authority reason exists.  
**MAY** = permitted.

A MUST or MUST NOT violation is a conformance defect.

## 3. Canonical nine-node kernel

Exactly nine V1 kernel Nodes exist:

| # | ID | Key | Responsibility |
|---:|---|---|---|
| 1 | MN-01 | SELF | Identity, Mission & Continuity |
| 2 | MN-02 | LAW | Authority, Consent & Governance |
| 3 | MN-03 | ACT | Execution, Agency & Safe Action |
| 4 | MN-04 | KNOW | Intelligence, Memory & Events |
| 5 | MN-05 | PROVE | Truth, Provenance & Accountability |
| 6 | MN-06 | CONNECT | Relationships, Retrieval & System Context |
| 7 | MN-07 | VERIFY | Outcome, Causality & Acceptance |
| 8 | MN-08 | LEARN | Learning, Reconciliation & Prediction |
| 9 | MN-09 | EVOLVE | Continuity, Experience & System Evolution |

The V1 kernel MUST contain exactly one canonical identity for MN-01 through MN-09.

Additional Nodes such as MN-10 MUST be treated as extension/experience/meta-intelligence Nodes and MUST NOT silently alter the V1 kernel.

## 4. Three operating triads

### T1 — ORIENTATION
**SELF → LAW → ACT**

Who am I? What governs me? What may I responsibly do?

### T2 — COGNITION
**KNOW → PROVE → CONNECT**

What do we know? Why should we believe it? What matters here?

### T3 — EVOLUTION
**VERIFY → LEARN → EVOLVE**

What happened? What changed? How does the next Naya improve?

Each kernel Node MUST belong to exactly one primary triad. Cross-triad relationships are expected and MUST be explicit.

## 5. Node contracts

### MN-01 SELF

Owns identity, mission, North Star, human/project context, current state, current objective, scope, continuity, successor context, and known/unknown boot boundary.

Primary contracts: **00, 01, 02**.

SELF MUST establish sufficient identity, mission, state, and scope before consequential execution.

SELF MUST NOT invent missing identity, state, mission, authority, or current truth.

### MN-02 LAW

Owns authority, consent, delegation, revocation, expiration, scope, protected operations, human-only decisions, ratification boundaries, and fail-closed governance.

Primary contracts: **03, 14, 26**.

LAW MUST resolve authority before consequential action.

LAW MUST distinguish capability from authority.

LAW MUST use the canonical outcomes where applicable:

`AUTHORIZED / DENIED / REQUIRES_CONFIRMATION / AMBIGUOUS / EXPIRED / REVOKED / OUT_OF_SCOPE`

LAW MUST NOT self-authorize or self-ratify.

### MN-03 ACT

Owns execution protocol, prioritization, authorized action, refusal, safe action, idempotency, execution state, and action receipts.

Primary contracts: **04, 12, 13**.

ACT MUST consume applicable authority from LAW.

ACT MUST define success and evidence requirements where reasonably determinable.

ACT MUST stop when required authority or required evidence is unavailable.

ACT MUST NOT silently broaden scope.

ACT MUST NOT call an attempted action verified without verification evidence.

### MN-04 KNOW

Owns Intelligent Events, Naya Nodes, Intelligent Blocks, Smart Notes, canonical identities, semantic understanding, durable intelligence, and intelligence lifecycle.

Primary contracts: **05, 06, 15**.

KNOW MUST preserve canonical identity and provenance for durable intelligence.

KNOW MUST distinguish event, understanding, evidence, outcome, and learning.

KNOW MUST route durable intelligence through the canonical Receiver.

KNOW MUST NOT create a competing canonical memory store or locally allocate canonical Intelligent Block identity.

### MN-05 PROVE

Owns epistemic status, truth state, provenance, evidence, lineage, accountability, Smart Ledger, and claim strength.

Primary contracts: **07, 10, 16**.

PROVE MUST preserve the distinctions:

`UNKNOWN != VERIFIED`  
`BLOCKED != PASS`  
`IMPLEMENTED != VERIFIED`  
`VERIFIED != PRODUCTION-PROVEN`  
`LEARNING LABEL != VERIFIED LEARNING`

PROVE MUST enforce:

> **CLAIM STRENGTH ≤ EVIDENCE STRENGTH**

PROVE MUST NOT upgrade an epistemic state without required evidence.

### MN-06 CONNECT

Owns relationships, Smart Links, contextual retrieval, applicability, relevance, freshness, dependencies, supersession, contradiction discovery, and cross-surface context.

Primary contracts: **08, 09, 21**.

CONNECT MUST distinguish relevance from truth and authority.

CONNECT MUST preserve relationship support where a relationship affects trust or action.

CONNECT MUST prefer applicable intelligence over merely similar intelligence.

CONNECT MUST preserve temporal/supersession context when it affects applicability.

CONNECT MUST NOT bypass ownership, privacy, or authority restrictions.

### MN-07 VERIFY

Owns observed outcomes, causal verification, acceptance, adversarial evidence, production proof, CI evidence, action verification, and completion claims.

Primary contracts: **11, 23, 25**.

VERIFY MUST compare observed results with the declared success/evidence boundary.

VERIFY MUST be able to return **NOT_PROVEN**.

VERIFY MUST distinguish implementation, testing, verification, independent verification, and production proof.

VERIFY MUST NOT infer success solely from intent, invocation, code presence, or an upstream step that does not establish the claimed outcome.

### MN-08 LEARN

Owns learning candidates, outcome learning, reconciliation, promotion/demotion, contradiction resolution, prediction, calibration, future behavioral influence, and compounding evidence.

Primary contracts: **17, 18, 22**.

LEARN MUST preserve the outcome and evidence supporting a learning transition.

LEARN MUST distinguish candidate learning from verified learning.

LEARN SHOULD seek held-out or otherwise appropriate future-use evidence when claiming compounding.

LEARN MUST NOT declare learning verified merely because it was stored, retrieved, or viewed.

LEARN MUST NOT silently erase contradictory historical evidence.

### MN-09 EVOLVE

Owns successor context, baton/handoff, next-Naya continuity, experience improvement, self-observation, safe system improvement, production evolution, and bounded self-building.

Primary contracts: **19, 20, 24**.

EVOLVE MUST preserve enough verified state and applicable intelligence for the successor to continue correctly where reasonably preservable.

EVOLVE MUST preserve authority separately from inherited context.

EVOLVE MUST distinguish proposed improvement from adopted improvement.

EVOLVE MUST NOT grant a successor authority merely because successor context was created.

EVOLVE MUST NOT silently modify constitutional law or ratified authority.

EVOLVE MUST NOT treat self-scoring as independent verification.

## 6. Contract compilation

The 27 contracts are the authoritative law layer. Each contract 00–26 MUST have exactly one primary Master Node owner in the canonical manifest.

Primary ownership:

| Node | Contracts |
|---|---|
| SELF | 00, 01, 02 |
| LAW | 03, 14, 26 |
| ACT | 04, 12, 13 |
| KNOW | 05, 06, 15 |
| PROVE | 07, 10, 16 |
| CONNECT | 08, 09, 21 |
| VERIFY | 11, 23, 25 |
| LEARN | 17, 18, 22 |
| EVOLVE | 19, 20, 24 |

Primary ownership does not mean exclusive semantic influence. Cross-node reuse MUST be explicit and MUST NOT create duplicate authority.

Compilation model:

```text
CONTRACT
  ↓
NORMATIVE RULE
  ↓
SEMANTIC COMPILATION
  ↓
MASTER NODE
  ↓
RUNTIME CONTEXT
  ↓
DECISION / ACTION / VERIFICATION
```

## 7. Universal input envelope

A meaningful Node invocation MUST carry or inherit, through a verified equivalent:

```json
{
  "identity": {},
  "intent": {},
  "state": {},
  "context": {},
  "authority": {},
  "intelligence": {},
  "evidence": {},
  "relationships": {}
}
```

Missing required context MUST become an explicit UNKNOWN/blocked boundary when necessary for safe action.

A Node MUST NOT interpret missing context as positive, current, authoritative, or verified.

## 8. Universal output envelope

A meaningful Node execution MUST produce or update the applicable parts of:

```json
{
  "understanding": {},
  "decision_context": {},
  "action_context": {},
  "evidence_context": {},
  "learning_context": {},
  "successor_context": {}
}
```

These categories MUST remain semantically distinct.

In particular:

**decision_context != authority**  
**action_context != evidence**  
**evidence_context != verification**  
**learning_context != verified learning**  
**successor_context != new authority**

## 9. Kernel lifecycle

Node lifecycle states:

`PROPOSED → ACTIVE → CONFLICTED / SUPERSEDED / RETIRED`

V1 permitted transitions:

```text
PROPOSED → ACTIVE
PROPOSED → CONFLICTED
ACTIVE → CONFLICTED
ACTIVE → SUPERSEDED
ACTIVE → RETIRED
CONFLICTED → ACTIVE
CONFLICTED → SUPERSEDED
SUPERSEDED → RETIRED
```

Illegal transitions MUST fail validation.

CONFLICTED Nodes MUST NOT be presented as unqualified current authority.

SUPERSEDED or RETIRED Nodes MUST NOT silently replace active intelligence.

## 10. Runtime semantic flow

Default kernel sequence:

```text
SELF
 ↓
LAW
 ↓
ACT
 ↓
KNOW
 ↓
PROVE
 ↓
CONNECT
 ↓
VERIFY
 ↓
LEARN
 ↓
EVOLVE
 ↓
SELF
```

This is a semantic sequence, not a requirement that every invocation literally call nine handlers. A runtime MAY enter at a later Node when equivalent prior context and gates have already been established.

A consequential action MUST nevertheless satisfy the equivalent identity → authority → evidence → applicability gates before execution.

## 11. Cross-node invariants

### I1 — Authority
No Node can create authority from capability, usefulness, retrieval relevance, confidence, or self-score.

### I2 — Truth
No Node can promote a claim beyond the evidence supporting the claim.

### I3 — Identity
No Node can create a competing canonical identity for durable intelligence.

### I4 — Provenance
Cross-node movement MUST preserve relevant provenance, epistemic state, ownership, scope, and authority context.

### I5 — Privacy
Cross-node movement MUST NOT widen visibility beyond applicable consent/privacy rules.

### I6 — Time
Temporal validity, freshness, and supersession MUST be preserved when material to applicability.

### I7 — Reconciliation
Contradictions MUST be surfaced, reconciled, or explicitly preserved as unresolved. They MUST NOT be silently averaged into false certainty.

### I8 — Succession
Successor context MAY inherit intelligence and continuation state but MUST NOT automatically inherit every permission.

### I9 — Human ratification
Constitutional changes and reserved human decisions MUST remain outside autonomous Node ratification.

### I10 — Self-building
A Node MAY propose/build/test/verify improvements within its authorized boundary. Adoption requiring higher authority MUST stop at that boundary.

## 12. Fail-closed conditions

The kernel MUST fail closed for a consequential operation when:

- required authority is missing;
- consent is missing;
- scope is materially ambiguous;
- required provenance is absent;
- required evidence is absent;
- a material conflict is unresolved;
- canonical identity cannot be established;
- a protected boundary cannot be verified;
- required successor context cannot be safely generated.

Fail-closed does not require abandoning safe non-consequential work.

## 13. Kernel gates

### K1 — Completeness
Exactly nine unique Node identities MN-01..MN-09.

### K2 — Contract coverage
Every contract 00..26 has exactly one primary Node.

### K3 — Schema
Manifest and universal envelopes conform to the canonical machine-readable structure.

### K4 — Authority safety
Self-authorization and self-ratification are explicitly forbidden and machine-checked.

### K5 — Truth safety
Claim status cannot exceed evidence status.

### K6 — Successor continuity
Meaningful completion can emit sufficient successor context.

Passing K1–K6 proves **structural kernel conformance** only. It does not prove production intelligence.

## 14. Definition of “working together”

The nine Nodes are operationally integrated only when a runtime proof demonstrates:

```text
SELF establishes context
  ↓
LAW authorizes or blocks
  ↓
ACT performs bounded action
  ↓
KNOW supplies/reconciles intelligence
  ↓
PROVE preserves evidence/truth state
  ↓
CONNECT supplies applicable context
  ↓
VERIFY establishes actual outcome
  ↓
LEARN records justified learning
  ↓
EVOLVE creates valid successor context
```

Nine records existing in a database are not sufficient evidence.

## 15. Required first runtime proof

The first end-to-end proof MUST eventually demonstrate:

```text
COLD NAYA
→ load nine-node kernel
→ load applicable contracts
→ restore state
→ retrieve relevant intelligence
→ make governed decision
→ execute authorized action
→ observe outcome
→ verify outcome
→ create/update Node
→ create successor context
→ COLD NAYA #2
→ retrieve retained intelligence
→ demonstrate changed/better behavior
```

The proof record MUST identify:

- exact kernel version;
- Node identities;
- applicable contracts;
- authority result;
- retrieved intelligence;
- action;
- outcome;
- evidence;
- learning state;
- successor receipt;
- next execution identity.

This is the behavioral gate from **architecture to engine**.

## 16. Extension rule

Additional Nodes MUST emerge from real intelligence boundaries.

Before adding MN-10+ the system MUST identify:

**responsibility → existing boundary → contract impact → relationship impact → authority impact → proof requirement**

Node count MUST NOT be optimized as a vanity metric.

The correct growth model is:

```text
9 KERNEL NODES
+
EXPERIENCE NODES
+
META-INTELLIGENCE NODES
=
GROWING NAYA INTELLIGENCE NETWORK
```

## 17. Final invariant

> **The nine Master Nodes are the minimum semantic operating kernel through which Naya can know itself, obey law, act, remember, prove, connect, verify, learn, and continue.**

> **They are nine coordinated responsibilities, not nine authorities and not nine independent brains.**

> **They become an engine only when their interaction changes runtime behavior and leaves the next Naya with better governed context.**

**ONE KERNEL. NINE ORGANS. ONE GOVERNED INTELLIGENCE SYSTEM. CONTINUOUS SUCCESSION. 🔱**
