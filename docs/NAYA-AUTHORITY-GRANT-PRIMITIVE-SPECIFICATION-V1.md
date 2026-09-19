# NAYA AUTHORITY GRANT PRIMITIVE — CANONICAL SPECIFICATION V1

**Status:** CANONICAL GOVERNANCE + RUNTIME CONTRACT  
**Effective:** 2026-09-18  
**Domain:** Human authority → consequential execution authorization  
**Runtime status:** V1 IMPLEMENTED — CONSEQUENTIAL COGNITION COMMIT GATE WIRED

## 1. Purpose

Naya Law and Naya Nitro require legitimate authority before consequential execution. This primitive defines the minimum machine-verifiable representation and validation boundary without creating a parallel identity or sovereign authority hierarchy.

> **AUTHORITY MUST BE EXPLICIT, VALID, SCOPED, TRACEABLE, AND SEPARATE FROM INTELLIGENCE, LEARNING, CONSENT, OR CAPABILITY.**

## 2. Non-negotiable boundaries

1. Capability is not authority.
2. Authentication is not authority.
3. Ownership is not authority for every consequential action.
4. Consent is not automatically execution authority.
5. Connection, membership, discoverability, or access is not authority.
6. Dream output never creates authority.
7. Learning evidence never creates authority.
8. A decision never creates authority by assertion.
9. `authority.granted=true` in a caller request is never sufficient evidence.
10. No component may grant itself authority.
11. Authority cannot exceed scope, action, subject, resource, or constraints.
12. Missing, invalid, expired, revoked, ambiguous, or unverifiable authority fails closed.
13. A grant cannot override constitutional, safety, legal, platform, or higher-priority constraints.
14. Every consequential execution must be traceable to the authority that permitted it.

## 3. Canonical chain

**LEGITIMATE HUMAN AUTHORITY → AUTHORIZATION EVENT → AUTHORITY GRANT → INDEPENDENT VALIDATOR → ACTION ELIGIBILITY → EXECUTION → EXECUTION RECEIPT**

The execution boundary must not infer authority from authentication, Dream, learning, consent, connection, decision claims, or capability.

## 4. Minimum grant object

The authoritative runtime record is `public.nayanet_authority_grants` and preserves:

- `grant_id`
- `issuer_id`
- `subject_id`
- `source_event_id`
- `mission_id`
- `scope`
- `actions`
- `constraints`
- `issued_at`
- `expires_at`
- `status`
- `revoked_at`
- `evidence`
- `parent_authority`
- `schema_version`
- `created_at`

`issuer_id` and `subject_id` reference the existing Supabase Auth identity. No parallel identity system exists.

## 5. Issuance transaction

`public.nayanet_issue_authority_grant(...)` is the V1 authoritative issuance transaction.

The issuer is derived from `auth.uid()`; it cannot be supplied by the caller. The transaction requires subject, source event, mission, scope, actions, constraints, and valid time semantics, then atomically creates an `ACTIVE` grant.

The grant is not executable merely because issuance succeeded; the independent validator must still authorize the exact action and target.

## 6. Independent validator

`public.nayanet_validate_authority_grant(grant_id, action, target)` is read-only and independently evaluates authenticated subject, grant lifecycle, expiration, exact action, and target/project scope.

It returns `AUTHORIZED` only when the stored grant independently proves the exact in-scope action for the authenticated subject; otherwise it returns `BLOCKED` with a deterministic reason.

## 7. Expiration and revocation

`expires_at` is evaluated against the database clock at validation time. Expired grants are blocked without requiring a background mutation.

`public.nayanet_revoke_authority_grant(...)` is the controlled revocation path. Authority-defining fields are immutable after issuance. Revocation preserves historical evidence and prevents subsequent authorization.

## 8. Mission / Authorized Actions

The runtime does not currently expose a separate durable Mission Contract table. V1 therefore materializes the existing Mission + Authorized-Actions semantics directly into `mission_id`, `scope`, `actions`, and `constraints` at human issuance time.

This is an adapter to existing governance semantics, not a replacement Mission system or universal authority source.

## 9. Consent separation

`nayanet_consents` remains a consent/sharing mechanism. Consent may be evidence but is not automatically execution authority.

## 10. Dream / Learning separation

**DREAM → LEARNING → DECISION; AUTHORITY: NO**

The verified lineage:

- Dream replay: `fafd1383-5e18-4732-8938-52e7aedc5a6f`
- Learning evidence: `a9e40bbc-ce65-4d1b-b34d-4840e2e68dc8`

is intelligence provenance only. It cannot issue or inherit authority.

## 11. Execution receipt provenance

`public.nayanet_execution_receipts` now has nullable V1 authority provenance fields:

- `authority_grant_id`
- `authority_issuer_id`
- `authority_scope`
- `authority_actions`
- `authority_constraints`
- `authority_status_at_execution`
- `authority_source_event_id`
- `authority_validated_at`

They remain nullable for backward schema compatibility, but consequential `nayanet_commit_cognition()` writes populate them only from successful validator output. The caller cannot supply authoritative provenance through `evidence`.

## 12. Required proof contract

Negative cases must return `BLOCKED`: no grant; authentication only; Dream-derived learning only; caller-supplied authority claim; expired grant; revoked grant; wrong subject; wrong action; wrong target/scope; invalid or unverifiable grant.

Positive case must return `AUTHORIZED` only from an independently established human-issued grant whose stored issuer is the authenticated `auth.uid()` and whose action/target are in scope.

## 13. Runtime implementation boundary

Implemented V1:

- authoritative grant table;
- existing-identity issuer/subject references;
- authenticated issuance transaction;
- independent validator;
- expiration evaluation;
- controlled revocation;
- immutable authority-defining fields;
- execution-receipt provenance columns;
- runtime proof harness.

Not yet implemented:

- automatic lookup/validation of a separate Mission Contract runtime object;
- full delegation enforcement;
- wiring the authority validator into `nayanet_commit_cognition()`;
- populating receipt provenance from successful validation during consequential execution.

## 14. Constitutional invariant

**INTELLIGENCE MAY INFORM ACTION. AUTHORITY MUST AUTHORIZE ACTION. EXECUTION MUST PROVE AUTHORIZATION.**

**DREAM DOES NOT GRANT. LEARNING DOES NOT GRANT. DECISION DOES NOT GRANT. CAPABILITY DOES NOT GRANT. AUTHENTICATION DOES NOT AUTOMATICALLY GRANT. CONSENT DOES NOT AUTOMATICALLY GRANT.**

**ONLY A VALID, TRACEABLE, IN-SCOPE AUTHORITY GRANT MAY CROSS THE CONSEQUENTIAL EXECUTION GATE.**

**NO GRANT → NO CONSEQUENTIAL AUTHORIZATION.**
