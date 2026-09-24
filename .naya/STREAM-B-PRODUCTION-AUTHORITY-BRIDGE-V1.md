# 🔱 Stream B — Production Authority Bridge V1

**Status:** DESIGN + FAIL-FIRST CONTRACT — 2026-09-24  
**Scope:** Fronts #1–#4 only  
**Production mutation:** NONE

## 1. Current caller/authorization graph

The repository source currently exposes these production database boundaries:

```
authenticated caller
  |
  +--> nayanet_record_cognition_event(
         project_id,
         event,
         action,
         expected,
         observed,
         learning
       )
       |
       +--> if action = intelligence.capture
       |      require event.metadata.authority_grant_id
       |      |
       |      +--> nayanet_validate_authority_grant(
       |             grant_id,
       |             intelligence_commit,
       |             project_id
       |          )
       |      |
       |      +--> cognition event
       |      +--> execution receipt
       |
       +--> overload:
            nayanet_record_cognition_event(..., p_execution_authorization)
            |
            +--> authority_id is cast to UUID
            +--> nayanet_validate_authority_grant(
            |      authority_id,
            |      intelligence_commit,
            |      project_id
            |   )
            +--> actor_id / permission / governance_state checks
            +--> cognition event
            +--> execution receipt
```

The first route is the legacy bypass candidate: it can authorize `intelligence.capture` from a database grant without any proof that a UniversalExecutionGate-issued credential exists.

The second route is closer to the intended contract, but it still does not verify gate provenance. Its `p_execution_authorization` is caller-supplied JSON; the SQL function checks selected fields but does not verify the portable signature, binding hash, gate issuer provenance, or canonical gate decision/action relationship.

### Front #4 caller inventory result

Repository-wide source inspection confirms the **database execution boundary is the two overloaded SQL signatures above**. The current GitHub connector code-search index did not return source-call-site matches for the function name, so application-level callers cannot honestly be declared exhaustively inventoried from the indexed source. That is a remaining prerequisite, not a guessed success.

Therefore the exact verified caller graph is:

**caller(s) not exhaustively indexed → one of two SQL overloads → authority validation → cognition → receipt**

The unresolved caller inventory must be closed before deleting the legacy overload.

## 2. Smallest canonical bridge

The bridge should have exactly one production authority object at execution time:

```
nayanet_authority_grants
        |
        | canonical grant snapshot
        v
production authority adapter
        |
        v
UniversalExecutionGate
        |
        v
ExecutionAuthorization
        |
        | process boundary, if needed
        v
portable signed authorization
        |
        v
single production intelligence_commit verifier
        |
        v
cognition event + execution receipt
```

### Canonical identity mapping

The production grant UUID must remain the runtime authority identity.

The gate authorization must carry a deterministic binding to that grant UUID, for example through the existing `authority_id` field after defining a canonical mapping contract. The mapping MUST NOT silently reinterpret an unrelated repository authority ID as a production grant.

Required invariant:

```
execution_authorization.authority_id
    == canonical production grant identity
```

or, if the existing `authority_id` field cannot safely carry the UUID contract, introduce a separately named immutable `production_grant_id` binding field in the canonical authorization schema. Do not overload semantics silently.

## 3. Exact overload convergence point

The two current signatures must converge on one internal function:

```
nayanet_record_cognition_event(...)
        |
        +--> canonical_intelligence_commit_authorize(...)
        |
        +--> canonical_cognition_persist(...)
        |
        +--> canonical_receipt_persist(...)
```

For `p_action = 'intelligence.capture'`, **no overload may independently authorize the action**.

The 6-argument overload must eventually either:

- become a compatibility wrapper that requires a canonical credential supplied through the event contract, or
- be removed after verified caller migration.

It must NOT retain the current behavior:

```
metadata.authority_grant_id
    -> nayanet_validate_authority_grant()
    -> SUCCESS
```

The 7-argument overload must stop treating arbitrary caller JSON as sufficient provenance. It must pass through the same canonical verifier.

## 4. Fail-first contract vectors

The implementation is not complete until these vectors pass against the unified production seam:

| Vector | Required result |
|---|---|
| valid gate-issued credential + exact active grant | ALLOW |
| caller-constructed JSON with matching fields but no gate signature | BLOCK |
| changed actor_id | BLOCK |
| changed authority/grant identity | BLOCK |
| changed permission | BLOCK |
| changed target/project | BLOCK |
| changed decision_id | BLOCK |
| changed action_id | BLOCK |
| changed binding_hash | BLOCK |
| expired credential | BLOCK |
| revoked grant after issuance | BLOCK |
| wrong grant for same actor | BLOCK |
| legacy 6-arg path without canonical credential | BLOCK |
| legacy metadata grant alone | BLOCK |
| successful execution | receipt contains same authority lineage |
| blocked execution | no SUCCESS receipt |
| cognition event | points to resulting receipt |
| receipt | cannot claim authority not verified at execution |

## 5. Front #1 — production grant → canonical authority adapter

Prerequisite:
- define the production grant UUID as the runtime authority identity;
- define the exact adapter fields: issuer, subject, mission, scope, actions, constraints, status, source_event_id, issued_at, expires_at, grant_id;
- make the adapter read current grant state at issuance/use rather than trusting caller JSON.

Implementation:
- one adapter;
- no second grant table;
- no UI permission;
- no authority minted from participation or model output.

Proof:
- same grant produces deterministic canonical authority;
- changed/revoked grant cannot produce an authorized credential.

## 6. Front #2 — production signed-credential verifier

Use the existing portable verification machinery rather than creating a new signature protocol.

Required checks:
- schema;
- Ed25519 signature;
- binding hash;
- gate authorization state;
- issuance/expiry;
- canonical authority fingerprint;
- current production grant validity;
- actor;
- action/permission;
- exact target/project.

The verifier must be fail-closed.

## 7. Front #3 — single intelligence_commit seam

There must be one function responsible for the authorization decision.

The persistence function must never manufacture a SUCCESS receipt before that authorization returns ALLOW.

All overloads delegate to it.

## 8. Front #4 — caller inventory

Before destructive overload removal:
1. enumerate SQL/RPC callers;
2. enumerate Edge Functions;
3. enumerate Hub/runtime application calls;
4. enumerate tests/fixtures;
5. enumerate workflows/scripts;
6. identify production versus test-only callers;
7. migrate every production caller;
8. then remove or permanently block the legacy authorization route.

## 9. Non-negotiable boundary

This document intentionally does **not** claim the bridge is implemented.

Current status:
- Front #1: DESIGN COMPLETE / IMPLEMENTATION NOT VERIFIED
- Front #2: EXISTING PORTABLE VERIFIER AVAILABLE / PRODUCTION WIRING NOT VERIFIED
- Front #3: NOT CONVERGED
- Front #4: PARTIAL — SQL boundary known, application caller inventory incomplete

No live mutation, grant issuance, revocation, deployment, or credential provisioning occurred.
