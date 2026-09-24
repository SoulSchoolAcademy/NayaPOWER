# 🔱 Stream B Contract Inventory V1

**Date:** 2026-09-24

## Authority / execution

| Contract | Source | Status |
|---|---|---|
| Governance kernel | `.naya/governance/governance_kernel.py` | VERIFIED |
| UniversalExecutionGate | `.naya/runtime/universal_execution_gate.py` | VERIFIED as implemented/tested |
| ExecutionAuthorization | same gate module | VERIFIED as implemented/tested |
| Production authority grant | `supabase/migrations/20260918170000_authority_grant_runtime_v1.sql` | VERIFIED as implemented |
| Portable authorization | `.naya/runtime/portable_authorization.py` | VERIFIED by fresh-process regression |

## Receipt / evidence

| Contract | Source | Status |
|---|---|---|
| Cognition event → execution receipt | `20260920030000_repair_cognition_event_receipt_lineage.sql` | VERIFIED as implemented |
| Execution authorization → receipt lineage | `20260924110000_reconcile_execution_authorization_cognition_overload_v1.sql` | VERIFIED as implemented |
| Smart Ledger | `20260919021000_smart_ledger_foundation_v1.sql` | VERIFIED as implemented |
| Receipt → Ledger trigger | same Smart Ledger migration | VERIFIED as implemented |
| Independent live Attack #4 | workflow + durable artifact | VERIFIED for its bounded claim |

## Product boundary contracts

| Contract | Source | Status |
|---|---|---|
| Smart Connect seven-door model | `NAYANET/HUB-ROOM-SYSTEM/04-SMART-CONNECT.md` | VERIFIED as documented |
| Participation/privacy protocol | `.naya/protocol/NAYANET-INTELLIGENCE-PARTICIPATION-PRIVACY-PROTOCOL-V1.md` | VERIFIED as documented |
| Hub room taxonomy | Master Objective + Gap Register | VERIFIED as current intended architecture |
| Dream process boundary | Master Objective + Gap Register | VERIFIED as current intended architecture |
| Naya Play capability boundary | Master Objective + Gap Register | VERIFIED as current intended architecture |

## Missing universal registry

There is not yet one machine-enforced registry containing:

`contract_id → owner → version → schema → invariants → authority → failure states → proof dependencies → implementation`

Therefore the **Universal Contract Registry** remains:

**NOT VERIFIED.**

This inventory must not be mistaken for that missing machine registry.
