# NAYA AUTHORITY GRANT PRIMITIVE — CANONICAL SPECIFICATION V1

**Status:** CANONICAL GOVERNANCE CONTRACT / NOT YET IMPLEMENTED  
**Effective:** 2026-09-18  
**Domain:** Human authority → consequential execution authorization  
**Authority tier:** Governance / authority primitive  
**Canonical owner:** Naya Power Governance  
**Runtime status:** SPECIFICATION ONLY — NO RUNTIME IMPLEMENTATION

## 1. PURPOSE

Naya Law and Naya Nitro require legitimate authority before consequential execution.

Existing governance establishes that authority is required, but the current system does not define a concrete runtime primitive for representing, validating, granting, expiring, or revoking that authority.

This specification closes that governance-definition gap without creating or changing runtime infrastructure.

> **AUTHORITY MUST BE EXPLICIT, VALID, SCOPED, TRACEABLE, AND SEPARATE FROM INTELLIGENCE, LEARNING, CONSENT, OR CAPABILITY.**

## 2. NON-NEGOTIABLE BOUNDARIES

1. Capability is not authority.
2. Authentication is not authority.
3. Ownership is not authority for every consequential action.
4. Consent is not automatically execution authority.
5. Connection, membership, discoverability, or access is not authority.
6. Dream output never creates authority.
7. Learning evidence never creates authority.
8. A decision never creates authority merely by declaring that authority exists.
9. A caller-supplied authority.granted=true claim is never sufficient evidence of a grant.
10. No component may grant itself authority.
11. Authority cannot exceed the grant's scope, action, subject, resource, or constraints.
12. Missing, invalid, expired, revoked, ambiguous, or unverifiable authority fails closed.
13. A grant cannot override constitutional, safety, legal, platform, or higher-priority constraints.
14. Every consequential execution must be traceable to the authority that permitted it.

## 3. AUTHORITY MODEL

Minimum conceptual chain:

LEGITIMATE AUTHORITY SOURCE → AUTHORITY GRANT → GRANT VALIDATION → ACTION ELIGIBILITY → EXECUTION → EXECUTION RECEIPT

The execution boundary MUST NOT infer authority from authentication, Dream, learning, consent, connection, a decision claim, or capability.

## 4. MINIMUM GRANT OBJECT

| Field | Meaning |
|---|---|
| grant_id | Unique immutable identifier for the authorization |
| issuer | Legitimate authority source that issued the grant |
| subject | Human/agent/system receiving the authority |
| scope | Resources, projects, domains, or objects covered |
| actions | Exact action(s) permitted |
| constraints | Conditions/limits attached to the permission |
| issued_at | Time authority became valid |
| expires_at | Optional hard expiration |
| status | ACTIVE / EXPIRED / REVOKED / INVALID |
| revoked_at | Revocation time when applicable |
| evidence | Evidence establishing issuance and applicable authority |
| parent_authority | Higher-level authority from which delegation derives, when applicable |

The implementation MAY use a different physical schema, but it MUST preserve these semantic properties.

## 5. VALID GRANT

A grant is valid only when all applicable conditions are true:

1. The issuer possesses legitimate authority to grant the requested authority.
2. The grant is attributable to that issuer.
3. The subject is unambiguous.
4. The action is explicitly covered.
5. The target/resource is within scope.
6. All constraints are satisfied.
7. The grant is currently active.
8. The grant has not expired.
9. The grant has not been revoked.
10. The grant does not violate a higher-priority constitutional, safety, legal, platform, or permission boundary.
11. The grant can be independently verified by the execution boundary.
12. The grant is traceable for the resulting execution receipt.

If any required condition cannot be established:

> **AUTHORITY = BLOCKED**

No inference may convert UNKNOWN into AUTHORIZED.

## 6. DELEGATION

Delegation is permitted only when the governing authority explicitly allows it.

A delegated grant MUST NOT exceed the authority of its parent grant/source.

Delegated scope must be a subset of parent scope; delegated actions must be a subset of parent actions; delegated constraints must be at least as restrictive as parent constraints.

A subject cannot delegate authority it does not possess.

## 7. CONSENT IS DISTINCT FROM AUTHORITY

The existing nayanet_consents concept represents consent/sharing relationships.

Consent MAY be relevant evidence for a policy decision, but:

> **CONSENT ≠ AUTOMATIC EXECUTION AUTHORITY**

A future implementation must not silently reinterpret existing consent records as authority grants unless this contract is explicitly amended to make that relationship authoritative.

## 8. LEARNING / DREAM SEPARATION

Dream, learning evidence, learner state, cognition, and decision context may influence what Naya understands or decides.

They MUST NOT issue, imply, inherit, or escalate authority.

Required invariant:

**DREAM → LEARNING → DECISION; AUTHORITY: NO**

Only an independently valid authority grant can cross the execution-authority boundary.

## 9. EXECUTION GATE

Before a consequential execution transition, the future execution boundary MUST evaluate:

1. authenticated subject;
2. constitutional eligibility;
3. valid authority grant;
4. action within grant scope;
5. target within grant scope;
6. constraints satisfied;
7. execution permitted.

The result MUST be one of:

### BLOCKED
No valid grant exists or one of the required checks fails.

### AUTHORIZED
A valid grant independently proves that this subject may perform this exact action on this exact target under the applicable constraints.

Only AUTHORIZED may permit the consequential transition.

## 10. RECEIPT REQUIREMENT

When a consequential action is authorized and executed, the execution receipt MUST preserve authority provenance sufficient to answer:

- Who/what authorized this action?
- What grant authorized it?
- What scope covered it?
- What action was permitted?
- What constraints applied?
- Was the grant active at execution time?
- Was the grant expired or revoked?
- What evidence supported authorization?

An execution receipt without sufficient authority provenance MUST NOT be treated as proof that the action was legitimately authorized.

## 11. NEGATIVE TEST CONTRACT

| Scenario | Required result |
|---|---|
| No grant | BLOCKED |
| Caller claims grant in request body | BLOCKED |
| Dream-derived learning only | BLOCKED |
| Valid authentication only | BLOCKED for actions requiring separate consequential authority |
| Consent only | BLOCKED unless an explicitly defined policy later establishes authority equivalence |
| Expired grant | BLOCKED |
| Revoked grant | BLOCKED |
| Wrong subject | BLOCKED |
| Wrong action | BLOCKED |
| Wrong scope/resource | BLOCKED |
| Invalid/unverifiable grant | BLOCKED |
| Valid grant within scope | AUTHORIZED |
| Valid grant outside scope | BLOCKED |
| Valid delegated grant exceeding parent scope | BLOCKED |

## 12. POSITIVE TEST CONTRACT

A future positive authorization proof MUST use an independently established valid grant.

It MUST NOT manufacture authorization by posting an authority.granted=true claim.

The proof MUST demonstrate:

LEGITIMATE ISSUER → VALID GRANT → SAME AUTHENTICATED SUBJECT → ACTION WITHIN SCOPE → EXECUTION ALLOWED → RECEIPT CONTAINS AUTHORITY PROVENANCE

## 13. CURRENT IMPLEMENTATION BOUNDARY

This specification intentionally creates no database table, Edge Function, RPC, RLS policy, authentication mechanism, identity system, consent-system reinterpretation, execution code, or authority-grant record.

Those are implementation decisions for a later, separately authorized execution cycle.

Until a grant issuance/representation mechanism is implemented and verified, the runtime must treat consequential authority as unavailable unless an existing platform/governance mechanism independently proves otherwise.

## 14. REQUIRED FUTURE WORK

Before modifying nayanet_commit_cognition():

1. Define the legitimate grant issuer/issuance mechanism.
2. Define the authoritative grant storage/representation.
3. Define grant validation.
4. Define expiration and revocation semantics.
5. Define delegation semantics if delegation is required.
6. Define authority provenance in execution receipts.
7. Add constitutional negative tests.
8. Add a positive valid-grant test.
9. Test the exact Dream → Learning lineage: replay afd1383-5e18-4732-8938-52e7aedc5a6f → evidence a9e40bbc-ce65-4d1b-b34d-4840e2e68dc8, proving learning influence remains distinct from authority.
10. Only then wire the execution gate into the canonical execution boundary.

## 15. GOVERNANCE DECISION

The existing canonical governance establishes the requirement for legitimate authority but does not define a runtime Authority Grant Primitive.

Therefore:

> **THE AUTHORITY-GRANT PRIMITIVE IS NOW DEFINED AS A GOVERNANCE CONTRACT, NOT AS A RUNTIME IMPLEMENTATION.**

This specification does not itself grant authority to any user, agent, system, decision, learning state, Dream replay, or execution path.

> **NO GRANT → NO CONSEQUENTIAL AUTHORIZATION.**

## 16. CANONICAL INVARIANT

**INTELLIGENCE MAY INFORM ACTION. AUTHORITY MUST AUTHORIZE ACTION. EXECUTION MUST PROVE AUTHORIZATION.**

**DREAM DOES NOT GRANT. LEARNING DOES NOT GRANT. DECISION DOES NOT GRANT. CAPABILITY DOES NOT GRANT. AUTHENTICATION DOES NOT AUTOMATICALLY GRANT. CONSENT DOES NOT AUTOMATICALLY GRANT.**

**ONLY A VALID, TRACEABLE, IN-SCOPE AUTHORITY GRANT MAY CROSS THE CONSEQUENTIAL EXECUTION GATE.**

---

**STATUS:** CANONICAL CONTRACT / NOT YET IMPLEMENTED  
**RUNTIME CHANGE:** NONE