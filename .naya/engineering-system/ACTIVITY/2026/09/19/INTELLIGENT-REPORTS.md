# INTELLIGENT REPORTS — MASTER NAYA READINESS REVIEW — 2026-09-19

**Role:** Intelligent Reports owner  
**Mission:** Turn accumulated intelligence into longer-horizon, evidence-traceable reports without double-counting derived intelligence.

## Executive state

**Current product readiness: 3.1 / 10 — report infrastructure exists in part; complete generation, evidence, privacy and UI closure are missing.**

Fresh runtime evidence:
- `v7_intelligence_reports`: 1 row.
- `nayanet_report_to_ledger` exists.
- This proves report-related runtime infrastructure, not a complete report product.

## Readiness matrix

| Dimension | Rating |
|---|---:|
| Specification | 9.5/10 |
| Requirements completeness | 9/10 |
| Today's execution plan | 9/10 |
| Engine/backend | 3/10 |
| Interface/design | 7/10 |
| Product integration | 2/10 |
| Security/privacy | 3/10 |
| Runtime/deployment | 3/10 |
| Ship readiness | 3.1/10 |

## Core role

Reports synthesize across a defined period longer than Today:

patterns, lessons, changes, decisions, outcomes and next actions.

A report is derived intelligence, not independent evidence.

## Complete today

1. Locate report UI and route.
2. Locate generation/storage implementation.
3. Define period boundaries and scope.
4. Generate a report from known source events.
5. Trace every material conclusion to canonical sources/evidence.
6. Prove regeneration when source intelligence materially changes.
7. Prove personal/Space/collective privacy isolation.
8. Prove fresh retrieval after generation.
9. Ensure reports are not double-counted as independent evidence.
10. Verify Cloudflare source/build/runtime parity.

## Definition of COMPLETE

Human selects a period → authorized canonical sources are gathered → report is generated with provenance/version → material claims drill to evidence → privacy is enforced → source changes trigger defined regeneration/invalidation → refreshed retrieval returns the correct version/state.

**NEXT:** Map the existing report generation/storage path and prove one end-to-end evidence-linked report before expanding report types.
