# NAYA AUTHORITY GRANT ISSUANCE CONTRACT V1

**STATUS:** CANONICAL GOVERNANCE + RUNTIME CONTRACT  
**EFFECTIVE:** 2026-09-18  
**DOMAIN:** Human authority → authority-grant issuance  
**AUTHORITY TIER:** Governance / authority primitive  
**RUNTIME STATUS:** V1 IMPLEMENTED — CONSEQUENTIAL COGNITION COMMIT GATE WIRED

## 1. PURPOSE

This contract defines how legitimate human authority becomes a verifiable Authority Grant without creating a second authority hierarchy.

The V1 runtime implementation uses the existing authenticated `auth.uid()` identity, a single `nayanet_authority_grants` record, an authenticated issuance transaction, an independent validator, and explicit execution-receipt provenance fields. It does not replace identity, consent, Mission governance, or the execution boundary.

## 2. EXISTING ARCHITECTURAL BASIS

The existing canonical Naya Power architecture establishes the human as mission owner, destination setter, authority source, boundary setter, and final override; explicit current human authority as a Tier-2 source; human delegation; mission contracts with authority and authorized actions; stop/change/override controls; consequential actions requiring appropriate authority; and uncertainty about authority as a reason to pause.

The runtime does not currently expose a separate durable Mission Contract table. Therefore V1 treats `mission_id`, `scope`, `actions`, and `constraints` as the structured authorization terms supplied by the authenticated human issuance transaction. This is an adapter to the existing Mission/Authorized-Actions semantics, not a replacement Mission system.

## 3. ISSUER

The legitimate issuer is the human authority source possessing the relevant authority.

At runtime, `nayanet_issue_authority_grant()` derives `issuer_id` from `auth.uid()`. The caller cannot supply or override the issuer identity.

Authentication identifies the issuing session; it does not by itself authorize every consequential action.

## 4. AUTHORIZATION EVENT

V1 represents the authorization event through the immutable grant's `source_event_id` plus its stored mission, scope, action, constraint, evidence, and issuer provenance.

The issuance transaction is itself the authoritative materialization event: it runs only for an authenticated issuer, derives the issuer from `auth.uid()`, validates required authorization terms, and inserts the grant atomically.

A caller cannot turn Dream, learning, decision context, consent, or a request-body authority claim into an issuance event.

## 5. MINIMAL RUNTIME GRANT

`public.nayanet_authority_grants` contains:

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

Issuer and subject reference existing Supabase Auth users. No parallel identity table is created.

## 6. ATOMIC ISSUANCE TRANSACTION

`public.nayanet_issue_authority_grant(...)` is the sole V1 issuance path exposed to authenticated callers.

It:

1. requires an authenticated `auth.uid()`;
2. derives `issuer_id = auth.uid()`;
3. requires an unambiguous subject;
4. requires mission, scope, actions, and constraints data in structured form;
5. rejects an expiry already in the past;
6. inserts the complete grant in one database transaction;
7. creates the grant in `ACTIVE` state;
8. returns the authoritative stored record.

The grant is not executable merely because issuance succeeded; the independent validator must still authorize the exact action and target.

## 7. INDEPENDENT VALIDATOR

`public.nayanet_validate_authority_grant(grant_id, action, target)` independently evaluates:

- authenticated caller;
- grant ownership/visibility;
- exact subject match;
- lifecycle status;
- expiration;
- exact action membership;
- target/project scope.

It returns either `AUTHORIZED` with grant provenance or `BLOCKED` with a deterministic reason.

The validator does not accept `authority.granted=true` or other caller-supplied authority assertions as evidence.

## 8. EXPIRATION

Consequential grants may carry an explicit `expires_at`. The validator compares expiration against the current database clock at validation time.

An expired grant is therefore `BLOCKED` without requiring a background job to rewrite the row.

## 9. REVOCATION

`public.nayanet_revoke_authority_grant()` permits the authenticated issuer to revoke an active grant. The immutable-grant trigger prevents changes to identity, mission, scope, actions, constraints, issuance time, expiry, or parent authority after issuance.

Revocation changes only lifecycle state/provenance and preserves historical evidence.

A revoked grant cannot authorize new execution.

## 10. IMMUTABILITY

The grant's authority-defining fields are immutable after issuance.

Only a controlled transition to `REVOKED` is permitted. This prevents a valid grant from being silently widened after it has been issued.

## 11. CONSENT

`nayanet_consents` remains a consent/sharing mechanism. It is not converted into execution authority.

## 12. DREAM / LEARNING / DECISION SEPARATION

The verified lineage:

**Dream replay `fafd1383-5e18-4732-8938-52e7aedc5a6f` → learning evidence `a9e40bbc-ce65-4d1b-b34d-4840e2e68dc8`**

remains intelligence/learning provenance only.

It cannot issue, imply, inherit, or escalate authority.

## 13. RECEIPT PROVENANCE

`nayanet_execution_receipts` now has nullable V1 provenance fields:

- `authority_grant_id`
- `authority_issuer_id`
- `authority_scope`
- `authority_actions`
- `authority_constraints`
- `authority_status_at_execution`
- `authority_source_event_id`
- `authority_validated_at`

They are intentionally nullable until `nayanet_commit_cognition()` is wired to require and persist successful authority validation.

The existing execution function was not changed by this implementation cycle.

## 14. PROOF CONTRACT

The V1 runtime proof must demonstrate:

### Negative

- no grant → `BLOCKED`;
- Dream/learning lineage only → `BLOCKED`;
- authentication only → `BLOCKED` for consequential action;
- caller assertion → `BLOCKED`;
- expired grant → `BLOCKED`;
- revoked grant → `BLOCKED`;
- wrong action/target → `BLOCKED`.

### Positive

- authenticated name-first human session;
- issuer derived from that session's `auth.uid()`;
- human-issued grant persisted by the issuance transaction;
- validator independently returns `AUTHORIZED` for the exact in-scope action/target;
- grant provenance is sufficient for a future execution receipt;
- no execution boundary is changed during this proof.

## 15. CURRENT BOUNDARY

Implemented in V1:

- authoritative grant storage;
- authenticated issuance transaction;
- independent validator;
- expiry evaluation;
- revocation;
- immutable authority-defining fields;
- receipt provenance schema.

Not yet implemented:

- automatic Mission Contract lookup/validation as a separate runtime object;
- delegation enforcement beyond stored parent provenance;
- wiring `nayanet_commit_cognition()` to require validator success;
- execution-receipt population from the validator result;
- final consequential execution positive proof through the existing execution RPC.

## 16. CONSTITUTIONAL INVARIANT

> **THE HUMAN MAY DELEGATE AUTHORITY. NAYA MAY USE AUTHORITY. NAYA MAY NOT CREATE AUTHORITY.**

> **AN AUTHORIZATION SOURCE MAY PROPOSE A GRANT. ONLY VALIDATION MAY MAKE THE GRANT EXECUTABLE.**

> **INTELLIGENCE MAY INFORM ACTION. AUTHORITY MUST AUTHORIZE ACTION. EXECUTION MUST PROVE AUTHORIZATION.**

**NO GRANT → NO CONSEQUENTIAL AUTHORIZATION.**
