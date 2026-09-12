# CCT / NayaNet — Machine Specification v0.1

**Specification ID:** CCT-NAYANET-MACHINE-v0.1  
**Authority:** Derived from `CCT-NAYANET-ARCH-v0.1`  
**Status:** CANONICAL DERIVED SPECIFICATION  
**Audience:** validators, schemas, services, storage, transport, algorithms, test harnesses, and other machine implementations

## 0. Precedence

This specification is derived from the canonical CCT/NayaNet Architecture Specification. It MUST NOT create competing semantics. Where this document conflicts with the architecture, the architecture wins.

The machine objective is **maximum verified useful value per action** (MPA) while preserving evidence, provenance, permissions, privacy, continuity, and reproducibility.

## 1. Core model

Machine implementations MUST distinguish:

`generated → structured → supported → verified → promoted → permitted → consumed → derived`

These states are not interchangeable. AI generation alone MUST NOT establish verification.

## 2. Smart Note Triad

A Smart Note is one canonical learning event represented by three synchronized layers:

1. **Human Note** — human meaning, observation, decision, or experience.
2. **Naya Note** — AI interpretation, learning, reasoning outcome, and actionable intelligence.
3. **Machine Note** — deterministic machine-readable representation used for validation, provenance, permissions, storage, retrieval, CIS/PIS processing, and CCT exchange.

All three share one immutable Smart Note identity and MUST remain traceably linked. A Smart Note is fully formed only when all three representations exist OR each unavailable representation has an explicit machine-readable reason.

The machine MUST NOT silently substitute one representation for another.

## 3. Intelligent Block schema contract

An Intelligent Block MUST contain these semantic groups:

```yaml
identity:
  block_id: required
  schema_version: required
  created_at: required
  source_system_id: required
  content_hash: required
intelligence:
  type: required
  claim: required
  learning: optional
  context: required
  applicability: optional
evidence:
  references: required
  verification_method: required
  verifier: required
  verified_at: required
  confidence: required
  reproducibility: required
provenance:
  parents: required
  lineage: required
  derivation: required
  transformations: required
  revision: required
permissions:
  owner: required
  authorization: required
  visibility: required
  permitted_consumers: required
  derivation_rights: required
  redistribution_rights: required
  retention: required
  revocation: required
value:
  problem_solved: required
  value_class: required
  expected_reuse: optional
  demonstrated_reuse: optional
  impact: optional
lifecycle:
  state: required
  status_reason: required
  updated_at: required
```

## 4. Deterministic identity

`block_id` and `content_hash` MUST be deterministically derived from a canonical serialization of the block content, excluding self-referential identity fields as defined by the implementation contract.

Equivalent content MUST produce equivalent identity. Any modification to hashed content MUST be detectable.

## 5. Validation

A validator MUST reject an Intelligent Block when any required semantic contract is absent, malformed, contradictory, unauthorized, or unverifiable.

Minimum validation sequence:

1. parse;
2. schema validate;
3. canonicalize;
4. recompute hash;
5. validate evidence references;
6. validate verification state;
7. validate provenance;
8. validate permissions for the requesting actor;
9. validate lifecycle state;
10. return machine-readable result.

Validation results MUST identify failure class and field/path where practical.

## 6. Provenance and lineage

A root block has no parent. A derived block MUST record its parent block identifier and parent hash, plus the transformation/derivation that produced it.

The canonical relation is:

`A → B → C`

but the protocol permits branches and multiple parents, producing a DAG rather than requiring one global chain.

Lineage verification MUST independently recompute and compare parent identity/hash references.

## 7. Permissions

Existence never implies propagation permission.

Permission checks MUST occur before consumption and before derivation/redistribution. The implementation MUST support explicit denial and MUST NOT treat missing authorization as consent.

Minimum states include private, personal, project, organization, selected-network, collective, and public where the governing deployment enables them.

## 8. Independent consumption

A receiving Naya MUST be able to consume a permitted block from the durable artifact plus permitted evidence without access to the originating conversation.

A test that succeeds only because hidden conversational context was supplied is invalid proof.

## 9. Evidence

Every verified block MUST identify its evidence references, verification method, verifier, verification time, confidence, and reproducibility information.

Machine-readable proof MUST distinguish:

- specified;
- implemented;
- locally verified;
- remotely verified;
- blocked externally;
- unknown.

No machine state may infer GREEN from file existence or configuration alone.

## 10. CIS/PIS integration boundary

Smart Notes feed CIS as learning events. CIS deduplicates, correlates, detects contradiction, evaluates evidence, promotes durable intelligence, and updates PIS.

PIS is the current operational intelligence state. CCT exchange MUST consume promoted, permissioned intelligence rather than indiscriminately exporting raw memory.

The MVP MUST prove the block protocol independently before making CIS/PIS federation a prerequisite.

## 11. Mandatory negative tests

The implementation MUST test rejection of:

- malformed block;
- missing evidence;
- forged/mismatched hash;
- missing provenance;
- forged parent hash;
- denied permission;
- revoked block where consumption is prohibited;
- missing required triad representation without an explicit unavailability reason;
- conversation-dependent consumption;
- successor without parent lineage;
- undeclared contradiction;
- tampered proof artifact.

## 12. Two-Naya MVP

The minimum empirical proof is:

`Naya A → Block A → independent durable handoff → Naya B → Block B → lineage verification`

The proof passes only when A and B are independently valid, permitted, evidence-backed, and traceably linked, and when the machine-readable proof survives a second independent verification pass.

## 13. MPA machine rule

Before an expensive action, implementations SHOULD determine:

`expected verified value / resource cost / risk`

Prefer one high-value deterministic batch over repeated speculative actions. Remote CI is reserved for confidence that local execution cannot provide.

## 14. Compatibility

Schema versions MUST be explicit. New versions MUST preserve the ability to interpret historical lineage. Breaking changes require a new schema version and migration/compatibility rules rather than silent reinterpretation.

## 15. Machine acceptance

A compliant implementation can demonstrate:

- deterministic block creation;
- deterministic validation;
- tamper detection;
- evidence/provenance enforcement;
- permission enforcement;
- conversation-independent consumption;
- parent lineage preservation;
- machine-readable proof;
- independent second-pass verification.
