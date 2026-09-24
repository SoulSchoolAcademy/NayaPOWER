# NAYANET_SELF_PROOF_V1

## Purpose

NayaNET proves service integrity from evidence already produced by the canonical system. This is not a second state store, event store, ledger, or authority system.

## Required proof surface

1. Identity
2. Source
3. Build
4. Deployment
5. Runtime
6. Connectivity
7. Canonical intelligence
8. Authority
9. Execution
10. Persistence
11. Lineage
12. Retrieval
13. Integrity

## Truth rule

- PASS means explicit evidence exists.
- FAIL means explicit contradictory evidence exists.
- NOT_VERIFIED means the system does not have sufficient evidence.
- Missing evidence never becomes PASS.
- Any FAIL produces overall NOT_VERIFIED.
- No failures plus one or more NOT_VERIFIED checks produces SELF_VERIFIED_WITH_LIMITATIONS.
- All required checks passing produces SELF_VERIFIED.

## Durability

The proof report can be embedded in the existing canonical Activity event shape and persisted through .naya/runtime/canonical_event_store.py via the existing Activity writer. No second persistence authority is introduced.

## V1 boundary

V1 evaluates supplied evidence; it does not fabricate evidence, bypass authentication, mutate Supabase security policy, or silently execute consequential actions. A future Hub surface may collect the evidence from the live runtime and render the resulting proof report.

## Human boundary

A self-proof is machine evidence, not human authorization. SELF_VERIFIED does not grant authority or replace human decisions where human authority is required.
