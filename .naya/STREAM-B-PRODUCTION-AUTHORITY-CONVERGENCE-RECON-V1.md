# 🔱 Stream B — Production Authority Convergence Reconnaissance V1

**Date:** 2026-09-24  
**Status:** RECONNAISSANCE COMPLETE — NO LIVE PRODUCTION MUTATION  
**Scope:** `nayanet_authority_grants → nayanet_validate_authority_grant → intelligence_commit` versus the repository's gate-issued `ExecutionAuthorization`.

## Executive finding

The repository currently contains **two authority representations that are related but not one canonical execution chain**:

1. **UniversalExecutionGate / portable authorization**
   - Canonical governance kernel + repository `.naya/governance/authority-registry.json`.
   - Gate issues immutable `ExecutionAuthorization`.
   - Portable boundary adds Ed25519 provenance and exact action binding.
   - Current intelligence-commit portable contract is `action_type ∈ {INTELLIGENCE_COMMIT, intelligence_commit}`, `permission=intelligence_commit`, `target=NayaNET`.

2. **Production Supabase authority grant**
   - `public.nayanet_authority_grants` is a database-backed grant model.
   - `nayanet_validate_authority_grant(grant_id, action, target)` checks authenticated subject, status, expiry, action membership, and target/project scope.
   - `nayanet_record_cognition_event` has **two overloads** relevant to this boundary:
     - 6-argument overload: accepts `metadata.authority_grant_id` and validates the database grant.
     - 7-argument overload: accepts `p_execution_authorization`, validates its `authority_id` against the database grant, then checks actor/permission/governance-state fields.
   - The 7-argument overload does **not** establish that the supplied JSON authorization was issued by `UniversalExecutionGate`, nor does it verify the portable Ed25519 signature/binding contract.

Therefore:

> **A database-authorized intelligence commit is not yet proven to be a gate-authorized intelligence commit.**

And conversely, the current gate registry uses human-controlled repository authority IDs such as `HUMAN-SOULSCHOOLACADEMY-REPO-WRITE`; the production grant table uses UUID `grant_id` values. There is no verified canonical adapter that makes those the same authority-of-record.

## Exact current chain

### A. Database production path

`authenticated actor`
→ `nayanet_authority_grants`
→ `nayanet_validate_authority_grant(grant_id, action, target)`
→ `nayanet_record_cognition_event(...)`
→ `nayanet_cognition_events`
→ `nayanet_project_cognition_state`
→ `nayanet_execution_receipts`

For `intelligence.capture`, the SQL boundary requires an active in-scope database grant.

### B. Gate / portable path

`canonical AuthorityRegistry`
→ `UniversalExecutionGate.authorize()`
→ canonical governance kernel evaluation
→ immutable `ExecutionAuthorization`
→ optional portable Ed25519 artifact
→ independent verifier

The gate is explicitly isolated from production today; its module states that nothing imports it except its test suite.

## Minimum bridge

The smallest bridge that makes the two models one canonical chain is **not another authority table, not another approval object, and not a new UI permission flow**.

It is a single governed production boundary with these properties:

1. **One authority-of-record**
   - Production `nayanet_authority_grants` becomes the authoritative runtime grant source for the production intelligence path.
   - The gate must consume a canonical representation of that exact grant rather than a separately invented/static grant.

2. **One gate-issued execution credential**
   - The production intelligence path may execute only from a gate-issued `ExecutionAuthorization` for:
     - exact actor/subject;
     - exact production grant identity;
     - exact `intelligence_commit` permission;
     - exact `NayaNET` target;
     - exact decision/action binding;
     - current validity.

3. **One cross-process verification boundary**
   - If the issuer and Supabase execution boundary are separate processes, the existing portable Ed25519 contract is the appropriate bridge.
   - The production verifier must verify signature, binding hash, artifact lifetime, and current production grant state.
   - The credential's authority identity must map unambiguously to the production grant identity.

4. **One canonical intelligence-commit function**
   - Collapse the two relevant `nayanet_record_cognition_event` execution surfaces into one canonical production path, or make every overload delegate to one internal canonical function.
   - There must be no legacy 6-argument route that can authorize `intelligence.capture` without the canonical gate credential.

5. **Receipt lineage**
   - The receipt must persist the same authority identity and execution credential lineage used at the execution boundary.
   - A successful receipt must be impossible when the canonical authorization verification did not pass.

## Exact prerequisite / implementation / proof boundary

### Prerequisites

- Decide and document the production authority-of-record identity mapping.
- Provide a production verifier public-key pin through the existing human-controlled secret/configuration boundary; **do not commit private signing material**.
- Confirm the exact production runtime that calls `nayanet_record_cognition_event`.
- Confirm whether the current production Supabase schema has both overloads deployed and which callers use each.

### Implementation boundary

- Add the minimum adapter from production grant → canonical gate authority representation.
- Issue the existing `ExecutionAuthorization` from the canonical gate for `intelligence_commit`.
- Convert it to the existing portable artifact only when a process boundary requires portability.
- Make the production intelligence-commit boundary verify that artifact and current production grant state.
- Remove/bypass no governance checks; do not introduce a second authority system.
- Make all intelligence-capture overloads converge on the same canonical verification function.

### Proof boundary

The closure proof must demonstrate all of the following independently:

1. **Positive:** a valid gate-issued credential for the exact active production grant permits the commit.
2. **Forgery:** caller-constructed JSON with the same fields but no valid gate provenance is blocked.
3. **Tampering:** changing actor, grant identity, permission, target, decision, or action causes rejection.
4. **Revocation:** revoking the production grant after issuance blocks execution.
5. **Expiry:** expired credentials block execution.
6. **Wrong grant:** a credential for another grant cannot execute this commit.
7. **Legacy bypass:** the old 6-argument path cannot authorize `intelligence.capture` independently.
8. **Receipt:** successful execution persists the same authority/credential lineage.
9. **Cognition binding:** the cognition event points to the resulting receipt.
10. **No false success:** no blocked execution emits a successful receipt.

## Holes in the current job

1. **Production authority ↔ UniversalExecutionGate convergence:** NOT VERIFIED.
2. **Portable artifact ↔ production grant identity mapping:** NOT VERIFIED.
3. **Production signature verification at the SQL/runtime boundary:** NOT VERIFIED.
4. **Two-overload intelligence-capture convergence:** NOT VERIFIED.
5. **Production caller inventory:** NOT VERIFIED.
6. **Production verifier key provisioning:** NOT VERIFIED.
7. **Independent live positive intelligence commit through the unified gate path:** NOT VERIFIED.
8. **Independent revocation/expiry proof through the unified path:** NOT VERIFIED.
9. **Receipt proof from the unified gate path:** PARTIAL.
10. **Single machine-enforced contract registry:** NOT VERIFIED.

## Next 10 highest-value execution fronts

| # | Frontier | Status | Why it matters |
|---|---|---|---|
| 1 | Canonical production grant → gate authority adapter | BLOCKED | Establishes one authority-of-record. |
| 2 | Canonical signed credential verifier at production boundary | BLOCKED | Closes cross-process provenance. |
| 3 | Collapse intelligence-capture overloads to one verification seam | BLOCKED | Removes the legacy authorization bypass. |
| 4 | Exact production caller inventory | NOT VERIFIED | Prevents an unseen caller from retaining the old path. |
| 5 | Grant identity mapping contract + tests | NOT VERIFIED | Prevents cross-system identity substitution. |
| 6 | Revocation/expiry adversarial suite on unified path | NOT VERIFIED | Proves time-of-use authority. |
| 7 | Receipt/receipt-lineage proof on unified path | PARTIAL | Completes accountability chain. |
| 8 | No-false-success regression on unified path | PARTIAL | Prevents success claims after blocked execution. |
| 9 | Human-controlled verifier-key provisioning contract | BLOCKED | Required for real cross-process signature verification. |
| 10 | Live authorized intelligence commit + independent reconstruction | BLOCKED | Final live proof of Actor → Authority → Decision → Execution → Intelligence Commit → Persistence → Receipt. |

## Explicit non-actions

This reconnaissance did **not**:
- mutate production Supabase;
- issue/revoke any live authority grant;
- deploy a Worker;
- change Cloudflare routes;
- provision or expose credentials;
- claim that the portable gate proof is already production authority proof.

**Conclusion:** the minimum bridge is a **single production gate-verification seam** that binds a gate-issued execution credential to the exact database authority grant, with all intelligence-capture entry points converging on it. The existing portable authorization machinery is reusable; a second authority model is not.
