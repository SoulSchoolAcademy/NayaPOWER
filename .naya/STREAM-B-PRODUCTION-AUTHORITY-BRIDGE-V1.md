# 🔱 Stream B — Production Authority Bridge V1

**Status:** SOURCE REPAIR PREPARED + FAIL-FIRST CONTRACT — 2026-09-24  
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

A **read-only production Supabase inspection** materially improved the caller graph.

The live database currently has exactly these two `nayanet_record_cognition_event` signatures:

- 6 arguments: `p_project_id, p_event, p_action, p_expected_result, p_observed_result, p_learning`
- 7 arguments: the same six plus `p_execution_authorization jsonb`

`pg_stat_statements` shows observed PostgREST execution traffic of **2,519 calls through the 6-argument signature and 54 calls through the 7-argument signature** in the retained statistics window. This is usage evidence, not a claim that every one of those calls was `intelligence.capture`.

The live `pg_proc.prosrc` dependency scan identifies these database functions as callers of the 6-argument boundary:

- `nayanet_add_connection_to_list`
- `nayanet_create_smart_list`
- `nayanet_join_space`
- `nayanet_leave_space`
- `nayanet_prepare_smart_mail_authorization`
- `nayanet_remove_connection_from_list`
- `nayanet_revoke_connection`
- `nayanet_save_connection`
- `nayanet_smart_note_receipt_to_execution_receipt`

The live `nayanet-compound-intelligence` Edge Function is confirmed as a caller of the **7-argument** RPC and passes `p_execution_authorization` after separately calling `nayanet_validate_authority_grant`.

Recent live `intelligence.capture` receipts also show two distinct historical/runtime shapes:

1. recent governed proof receipts contain an `execution_authorization` object with `authority_id`, `decision_id`, `action_id`, `binding_hash`, `permission`, `governance_state`, and embedded grant data;
2. older `intelligence.capture` receipts in the retained window exist with **null authority lineage**. Those records predate/reflect earlier implementation states and must not be used as proof of the current contract.

Therefore the exact verified production graph is now:

**PostgREST / DB callers → one of two SQL overloads → DB grant validation and persistence**

with **`nayanet-compound-intelligence` → 7-arg overload** explicitly verified as an active Edge Function path.

Application/Hub callers outside the database and the complete Edge Function caller set remain unverified; the GitHub code-search index did not return usable call-site matches. That gap must be closed before destructive overload removal.

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
- Front #3: PARTIAL — legacy six-argument `intelligence.capture` path is now source-repaired to fail closed; seven-argument gate/portable provenance remains NOT VERIFIED
- Front #4: **PARTIAL → substantially reconstructed** — live SQL callers and the active `nayanet-compound-intelligence` 7-arg caller are verified; complete Edge Function/Hub caller inventory remains incomplete

No live mutation, grant issuance, revocation, deployment, or credential provisioning occurred.


### Source repair prepared in this session

Migration `20260924230000_converge_intelligence_capture_authority_v1.sql` changes only the six-argument overload's `intelligence.capture` branch: because that overload has no ExecutionAuthorization input, it now fails closed with `CANONICAL_EXECUTION_AUTHORIZATION_REQUIRED` instead of authorizing from caller metadata. Existing non-capture actions retain their established grant validation behavior. This is a source-level repair only; production application is NOT claimed. The seven-argument overload remains the canonical candidate but still requires provenance verification before the bridge can be considered converged.
