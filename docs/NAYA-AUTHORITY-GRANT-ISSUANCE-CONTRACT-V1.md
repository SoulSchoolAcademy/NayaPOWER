# NAYA AUTHORITY GRANT ISSUANCE CONTRACT V1

**STATUS:** CANONICAL GOVERNANCE CONTRACT / SPECIFICATION ONLY  
**EFFECTIVE:** 2026-09-18  
**DOMAIN:** Human authority → authority-grant issuance  
**AUTHORITY TIER:** Governance / authority primitive  
**RUNTIME STATUS:** NOT YET IMPLEMENTED

## 1. PURPOSE

The Naya Authority Grant Primitive defines what a valid consequential-execution grant must contain and how it must be validated.

This contract defines only the missing **issuance mechanism**: how legitimate human authority can become a verifiable Authority Grant without creating a second authority hierarchy.

It is intentionally narrow. It does not create runtime storage, APIs, RPCs, RLS policies, identity systems, execution code, or a new authority table.

## 2. EXISTING ARCHITECTURAL BASIS

The existing canonical Naya Power architecture already establishes:

- the human as mission owner, destination setter, authority source, boundary setter, and final override;
- explicit current human authority as a Tier-2 authority source;
- human delegation of actions to Naya;
- mission contracts that state human authority and authorized actions;
- explicit human stop/change/override controls;
- higher-risk or consequential actions requiring appropriate human authority;
- uncertainty about authority as a reason to pause;
- capability as distinct from authority.

The Human Authority Smart Note explicitly models delegation as:

**GOAL + SCOPE + AUTHORITY + CONSTRAINTS + SUCCESS CONDITION + VERIFICATION METHOD**

and states that the exact permission model must be implemented by the relevant runtime systems.

Therefore the architecture contains the legitimate **authority source and delegation model**, but not yet the machine-verifiable issuance event.

## 3. ISSUER

For the current Naya Power model, the default legitimate issuer is:

**THE HUMAN AUTHORITY SOURCE WHO ACTUALLY POSSESSES THE RELEVANT AUTHORITY.**

For a person's own NayaNET workspace, authenticated human identity may identify the subject/issuer, but authentication alone does not prove that every consequential action is authorized.

The issuer must be entitled to authorize the specific action, target, scope, and constraints being granted.

An AI, Dream replay, learning record, decision context, capability, session, membership, or caller-supplied claim cannot self-issue authority.

## 4. ISSUANCE EVENT

An Authority Grant is created only from an **explicit human authorization event** that is sufficiently specific to establish:

- issuer;
- subject receiving authority;
- purpose/mission;
- target/resource;
- authorized action or action set;
- scope;
- constraints;
- success/termination conditions where material;
- effective time;
- expiry or continuing-validity rule;
- verification/evidence reference.

A vague statement such as “do whatever is necessary” must not be treated as unlimited consequential authority.

Where the human's instruction is ambiguous about a material consequential boundary, the authority state is **UNKNOWN**, not authorized.

## 5. DIRECT HUMAN INSTRUCTION

A direct human instruction may be the source event for a grant when all required grant semantics can be established from the instruction and surrounding authorized mission context.

The system must not silently widen a direct instruction beyond:

**WHAT + WHO + TARGET + ACTION + SCOPE + CONSTRAINTS + TIME**

where those dimensions are material.

A low-risk operational delegation may be broad within an already established scope.

A consequential, irreversible, externally binding, financial, security-sensitive, privacy-sensitive, or otherwise high-impact action requires sufficiently explicit authorization for that action.

## 6. MISSION CONTRACT AS AN ISSUANCE SOURCE

An existing Mission Contract may provide the structured source for an Authority Grant when it contains the required human authority and authorized-action semantics.

A Mission Contract is not automatically a universal grant.

For each consequential action, the resulting grant must still be:

- attributable to the legitimate human issuer;
- explicit about applicable scope/action;
- constrained by the mission contract;
- independently validated;
- traceable to the originating authorization.

Thus:

**MISSION CONTRACT → POSSIBLE AUTHORIZATION SOURCE → VALIDATED AUTHORITY GRANT**

not:

**MISSION CONTRACT = UNLIMITED AUTHORITY**

## 7. NO NEW AUTHORITY HIERARCHY

Issuance must not introduce a second sovereign authority.

The hierarchy remains:

**EXTERNAL HARD CONSTRAINTS → NAYA POWER CONSTITUTION → LEGITIMATE HUMAN AUTHORITY → GOVERNANCE → SYSTEM / MISSION / TOOL SCOPE**

The issuance mechanism is an adapter between legitimate human authority and the Authority Grant Primitive.

It does not become an authority source itself.

## 8. GRANT CONSTRUCTION

The issuance mechanism must transform the verified authorization source into the canonical grant fields defined by the Authority Grant Primitive specification.

At minimum:

- grant_id
- issuer
- subject
- scope
- actions
- constraints
- issued_at
- expires_at
- status
- revoked_at
- evidence
- parent_authority

The issuance process must not invent missing material fields.

If a required field cannot be established, issuance fails closed.

## 9. ISSUANCE VALIDATION

Issuance and validation are separate responsibilities.

The issuance event establishes the proposed grant.

The downstream validator independently determines whether the grant is currently valid for the requested action.

Therefore:

**ISSUER → ISSUANCE EVENT → GRANT → VALIDATOR**

not:

**ISSUER → GRANT → AUTOMATIC EXECUTION**

The issuer cannot bypass later constitutional or scope validation.

## 10. EXPIRATION

Every consequential grant must have either:

- an explicit expiry; or
- an explicitly defined continuing-validity condition that the future runtime contract can independently evaluate.

Silence must not be interpreted as perpetual authority when the action is consequential.

## 11. REVOCATION / STOP

The human remains the final override.

A human stop, withdrawal, or mission change must be capable of invalidating or superseding applicable delegated authority.

Future runtime implementation must preserve revocation provenance rather than deleting historical grant evidence.

A revoked grant cannot authorize new consequential execution.

Existing execution already performed under a previously valid grant is historical fact and must not be rewritten merely because the grant was later revoked.

## 12. DELEGATION

Delegation is permitted only when the issuer possesses authority to delegate.

Any delegated grant must satisfy:

**delegated scope ⊆ parent scope**

**delegated actions ⊆ parent actions**

**delegated constraints ≥ parent restrictions**

A delegate cannot create broader authority than its parent.

If delegation authority is not established, delegation is blocked.

## 13. CONSENT IS NOT THE ISSUER CONTRACT

nayanet_consents remains a consent/sharing mechanism.

Consent may be evidence relevant to a grant, but it must not be silently reinterpreted as consequential execution authority.

No issuance implementation may convert existing consent records into execution grants without a future explicit governance decision.

## 14. DREAM / LEARNING / DECISION SEPARATION

The verified chain:

**DREAM → LEARNING EVIDENCE → DECISION**

can inform an action.

It cannot issue authority.

For the established lineage:

Dream replay: **fafd1383-5e18-4732-8938-52e7aedc5a6f**

Learning evidence: **a9e40bbc-ce65-4d1b-b34d-4840e2e68dc8**

that lineage is evidence/intelligence provenance only.

It must not be treated as an authority grant, issuer, or permission source.

## 15. REVOCATION AND MISSION CHANGE PRECEDENCE

When a human changes or stops the mission:

**CURRENT LEGITIMATE HUMAN AUTHORITY > PRIOR DELEGATION**

subject to constitutional, legal, safety, platform, and technical constraints.

A previously issued grant must not remain effective merely because an old mission record still exists.

## 16. REQUIRED FUTURE ISSUANCE STATES

A future runtime implementation should distinguish at minimum:

- PROPOSED — authorization source identified but not yet sufficient;
- ISSUED — grant created from a valid authorization source;
- ACTIVE — grant currently valid;
- EXPIRED — grant validity ended by time/condition;
- REVOKED — human authority withdrew or superseded it;
- INVALID — required issuer, scope, evidence, or other condition cannot be established.

Only a separately validated ACTIVE grant may satisfy the Authority Grant Primitive.

## 17. FAIL-CLOSED RULE

If issuer identity, issuer authority, subject, action, target, scope, constraints, effective time, evidence, or lifecycle state cannot be established where material:

**DO NOT ISSUE / DO NOT AUTHORIZE.**

Unknown authority is not implicit permission.

## 18. REQUIRED FUTURE PROOF

Before the execution boundary is modified, the implementation must prove both:

### Negative path
No valid human-issued grant → **BLOCKED**.

This includes:

- authentication only;
- ownership only;
- consent only;
- Dream-derived learning only;
- decision-context assertion only;
- caller-supplied authority.granted=true;
- expired grant;
- revoked grant;
- wrong subject;
- wrong action;
- wrong target/scope.

### Positive path
A valid independently established human-issued grant with matching scope/action/constraints → **AUTHORIZED**.

The positive test must prove the grant came from the authoritative issuance path, not from the request body or test fixture assertion.

## 19. CURRENT ARCHITECTURAL DECISION

The smallest legitimate issuance mechanism supported by the existing Naya Power architecture is:

**EXPLICIT HUMAN AUTHORIZATION / DELEGATION, STRUCTURED BY THE EXISTING MISSION + AUTHORIZED-ACTIONS MODEL, THEN MATERIALIZED AS A VALIDATED AUTHORITY GRANT.**

This uses the existing human authority hierarchy.

It does not create:

- a new sovereign authority;
- a second permission system;
- a replacement identity system;
- a reinterpretation of consent;
- AI self-authorization.

## 20. WHAT IS STILL UNIMPLEMENTED

The following remain runtime work and are intentionally outside this contract:

1. authoritative grant storage/representation;
2. issuance API or transaction;
3. issuer verification;
4. grant validation;
5. expiry evaluation;
6. revocation/supersession recording;
7. delegation enforcement if required;
8. execution-receipt grant provenance;
9. positive/negative runtime tests;
10. integration with nayanet_commit_cognition().

No execution boundary should be changed until those semantics are implemented and independently verified.

## 21. CONSTITUTIONAL INVARIANT

> **THE HUMAN MAY DELEGATE AUTHORITY. NAYA MAY USE AUTHORITY. NAYA MAY NOT CREATE AUTHORITY.**

> **AN AUTHORIZATION SOURCE MAY PROPOSE A GRANT. ONLY VALIDATION MAY MAKE THE GRANT EXECUTABLE.**

> **INTELLIGENCE MAY INFORM ACTION. AUTHORITY MUST AUTHORIZE ACTION. EXECUTION MUST PROVE AUTHORIZATION.**

---

**RELATIONSHIP:**
- Authority Grant Primitive: defines the grant.
- Authority Grant Issuance Contract: defines how legitimate human authorization becomes the grant.
- Runtime validator: future implementation that independently validates the grant.
- Execution boundary: future consumer that permits consequential execution only after successful validation.

**RUNTIME STATUS:** GOVERNANCE SPECIFICATION ONLY. NO RUNTIME CODE CHANGED.
