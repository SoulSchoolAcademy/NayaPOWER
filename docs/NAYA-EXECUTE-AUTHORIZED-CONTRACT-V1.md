# Naya `execute_authorized()` Contract V1

**Status:** CANONICAL EXECUTION CONTRACT  
**Effective:** 2026-09-19  
**Domain:** Human authority → consequential execution

## 1. Contract

Every consequential adapter follows:

**PRE-ISSUED AUTHORITY GRANT → VALIDATE AT USE → EXECUTE → RECEIPT → REVOKE/REVALIDATE**

The adapter MUST NOT mint authority as a side effect of execution.

## 2. Required input

- authenticated subject
- pre-issued `authority_grant_id`
- exact action
- exact target/resource
- idempotency key
- action payload

## 3. Gate

`execute_authorized()` calls the canonical independent Authority Grant validator immediately before execution.

Validation MUST fail closed for missing, invalid, expired, revoked, wrong-subject, wrong-action, or wrong-target authority.

Only `AUTHORIZED` validation may cross the consequential external-action boundary.

## 4. Execution

The adapter passes the exact validated grant into the action transaction. Execution MUST NOT infer authority from authentication, Dream, learning, decision claims, consent, connection, membership, or capability.

## 5. Receipt

A successful consequential action MUST preserve:

- authority grant ID
- issuer/subject
- scope
- actions
- constraints
- authority status at execution
- source authorization event
- validation timestamp
- external/action correlation identifiers

## 6. Revocation-at-use

After revocation, the same grant MUST fail at the execution boundary and produce no new external side effect. Historical receipts remain evidence.

## 7. Separation laws

Authentication identifies the caller.  
Dream informs.  
Learning informs.  
Decision informs.  
Consent remains consent.  
Capability provides the mechanism.  
**Authority authorizes consequential action.**

## 8. Proven production implementation

Smart Mail is the first production adapter implementing this pattern.

Production proof run **35415669855** verified:

`issue → pre-validate → real execution → receipt provenance → revoke → same execution blocked → original receipt preserved`.

## 9. Migration rule

Consequential production adapters are migrated one at a time. Each migration requires an independent production proof of pre-issued grant, validation-at-use, execution, receipt lineage, revocation-at-use, and blocked replay.

**No synthetic PASS. No caller-supplied authority claim. No internal grant minting at execution. No consequential execution without validated authority.**
