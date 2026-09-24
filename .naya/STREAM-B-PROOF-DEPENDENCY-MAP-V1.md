# 🔱 Stream B Proof Dependency Map V1

**Date:** 2026-09-24

This is an evidence map, not a claim that the entire governance system is verified.

## Node B1 — Canonical authority registry
Source: `.naya/governance/authority-registry.json`

Required for: gate authorization.

## Node B2 — UniversalExecutionGate
Source: `.naya/runtime/universal_execution_gate.py`

Required for: gate-issued `ExecutionAuthorization`.

## Node B3 — Gate authorization binding
Contract: authority + decision + exact action type + target + actor + scope + permission.

Required for: execution.

## Node B4 — Portable intelligence-commit credential
Source: `.naya/runtime/portable_authorization.py`

Required proof:
B2 → B3 → signed artifact → independent verifier.

Current evidence:
`tests/test_stream_b_cross_process_intelligence_authorization.py` — 10/10 PASS in GitHub Actions run 36048265954.

## Node B5 — Production intelligence-commit authority
Sources:
- `supabase/migrations/20260924100000_wire_authority_grant_into_intelligence_commit_v1.sql`
- `supabase/migrations/20260924110000_reconcile_execution_authorization_cognition_overload_v1.sql`

Requires:
authenticated actor + production authority grant + `intelligence_commit` permission + actor match + AUTHORIZED state.

This is a separate production mechanism from B2.

## Node B6 — Cognition event persistence
Source: `nayanet_cognition_events`

## Node B7 — Execution receipt persistence
Source: `nayanet_execution_receipts`

Required lineage:
B5 → B6 → B7.

The cognition/receipt migration binds the resulting receipt ID back onto the cognition event.

## Node B8 — Smart Ledger
Source:
`supabase/migrations/20260919021000_smart_ledger_foundation_v1.sql`

Required lineage:
execution receipt/cognition event → ledger source reference.

Ledger is an accountability projection, not an authority issuer.

## Node B9 — Independent adversarial proof
Sources:
- `tests/test_universal_execution_gate.py`
- Attack #4 live proof workflow/artifact

Required for acceptance:
the proof must establish a specific boundary and may not be generalized beyond its evidence scope.

## Node B10 — Hub projection
Source:
`NAYANET/HUB/index.html`

Depends on:
B7/B8 and actual runtime retrieval.

UI state cannot promote NOT VERIFIED into VERIFIED.

## Open dependency

**B2 → B5 convergence remains unresolved.**

The portable proof demonstrates gate-issued provenance in a fresh process.

It does not establish that every production intelligence commit is issued through that same gate.

Therefore:

**portable provenance VERIFIED ≠ universal production authority convergence VERIFIED.**
