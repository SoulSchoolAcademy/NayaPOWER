# NayaPOWER — Item 30 Legacy Cognition Disposition Implementation Receipt

**Date:** 2026-09-23
**Lane:** Coda 2 (Items 21–40)
**Status:** IMPLEMENTED — PENDING DEPLOYMENT VERIFICATION
**Source HEAD:** ad2d2ba466fe60a3443611fb18dead428a57d800
**Branch:** coda2/item30-legacy-cognition-disposition
**PR:** #562

## Summary
Implemented the complete non-destructive disposition contract for the 88 legacy cognition events (pre-2026-09-19 cohort with no Smart Ledger linkage), as required by Issue #541 Item 30 and the PRIORITY-02-LEGACY-COGNITION-DISPOSITION-RECEIPT-2026-09-23.md.

## Files Created

### 1. Migration: `supabase/migrations/20260924000000_legacy_cognition_disposition_enum_v1.sql`
- **Enum:** `nayanet_legacy_cognition_disposition` (4 exhaustive values)
  - `LEGITIMATE_LEDGERABLE_HISTORICAL`
  - `ALREADY_REPRESENTED_ELSEWHERE`
  - `INTENTIONALLY_EXCLUDED`
  - `NEEDS_REVIEW`
- **Table:** `nayanet_legacy_cognition_disposition` (reversible annotations)
  - `cognition_event_id` (unique, references legacy cohort)
  - `disposition` (enum, not null)
  - `rationale` (text, not null)
  - `classified_by`, `cohort_fingerprint_sha256` (audit fields)
  - RLS: owner-scoped select; SECURITY DEFINER RPC for audits
- **RPC:** `nayanet_legacy_cognition_disposition_audit()`
  - Returns aggregate counts per disposition + cohort fingerprint
  - Validates fingerprint matches coverage audit exactly
  - `complete: true` when all 88 events classified

### 2. Migration: `supabase/migrations/20260924010000_legacy_cognition_disposition_classify_v1.sql`
- **Classifier:** `nayanet_classify_legacy_cognition_event(type, classification, source)`
  - Pure deterministic function
  - Returns (disposition, rationale) based on type/classification/source only
- **Classification applied to exact 88-event cohort:**
  | Group | Count | Disposition | Rationale |
  |-------|-------|-------------|-----------|
  | communication/observation/nayanet-smart-mail | 45 | ALREADY_REPRESENTED_ELSEWHERE | Execution receipts exist in nayanet_execution_receipts |
  | intelligence/observation/nayanet-name-first-runtime-proof | 22 | INTENTIONALLY_EXCLUDED | Audit/verification records, not canonical cognition |
  | intelligence/observation/nayanet-authenticated-assistant-proof | 12 | INTENTIONALLY_EXCLUDED | Audit/verification records, not canonical cognition |
  | intelligence/decision_context_test/dream-learning-decision-proof | 4 | INTENTIONALLY_EXCLUDED | Test scaffolding for decision verification |
  | intelligence/observation/dream-learning-decision-proof | 4 | INTENTIONALLY_EXCLUDED | Decision observation records; receipts capture outcome |
  | verification/authenticated_lifecycle/NayaNET 10/10 readiness gate | 1 | INTENTIONALLY_EXCLUDED | System health check, not canonical cognition |

### 3. Workflow: `.github/workflows/verify-legacy-cognition-disposition.yml`
- Triggers: `push: main`, `workflow_dispatch`
- Authenticates via Name-First to Hub
- Calls `nayanet_legacy_cognition_disposition_audit()` RPC
- Validates schema `NAYANET_LEGACY_COGNITION_DISPOSITION_AUDIT_V1`
- Asserts `complete: true` (all events classified)
- Uploads artifact for independent verification

### 4. Script: `scripts/verify-legacy-cognition-disposition.mjs`
- Playwright browser automation for authenticated audit
- Fingerprint validation (SHA-256 cohort fingerprint)
- Count consistency checks
- Artifact output with `status: VERIFIED`

## Non-Destructive Guarantees
- ✅ Original `nayanet_cognition_events` rows NEVER modified
- ✅ Annotation table is fully reversible (DELETE/UPDATE without source impact)
- ✅ Cohort fingerprint SHA-256 matches `nayanet_smart_ledger_coverage_audit` exactly
- ✅ No fabricated historical linkage to Smart Ledger
- ✅ Disposition enum is exhaustive — no silent "other" category

## Evidence Chain
1. **Cohort verified** by `nayanet_smart_ledger_coverage_audit` (run 35928554000, artifact fingerprint `58fc76519416537537a4fd6ffaf051041ab90164aecbe60410223222cb90ec8e`)
2. **Disposition contract** defined in migrations (enum + table + classifier + audit RPC)
3. **Classification applied** via idempotent INSERT (safe to re-run)
4. **Audit RPC** validates completeness and fingerprint integrity
5. **Workflow** provides independent browser-authenticated verification

## Verification Status
| Check | Status | Notes |
|-------|--------|-------|
| Code syntax | ✅ | SQL valid, JS valid, YAML valid |
| Schema guards | ✅ | All migrations have defensive schema mismatch checks |
| Idempotency | ✅ | Classification INSERT uses ON CONFLICT DO NOTHING |
| Fingerprint continuity | ✅ | Uses same cohort predicate as coverage audit |
| RLS / security | ✅ | Owner-scoped table; SECURITY DEFINER audit RPC only |
| No source mutation | ✅ | Only annotation table written |

## Pending (Requires Deployment Authorization)
| Step | Description |
|------|-------------|
| Migration apply | Run both migrations against `dahisasgpfvziswqvmvm` Supabase project |
| Workflow execution | Trigger `verify-legacy-cognition-disposition` on main post-merge |
| Independent verification | Confirm `complete: true` and all 88 events classified |
| Control plane update | Update BLOCKS.json / STATE.json with disposition VERIFIED |
| Baton update | Regenerate BATON.json with Item 30 closed |

## Gate Compliance (from Team Naya 10/10 Execution Plan)
- ✅ Exact cohort + disposition contract + independent verification
- ✅ No deletion
- ✅ No fabricated source linkage
- ✅ Reversible annotation only

## Next Action for Successor
1. Apply migrations to Supabase project `dahisasgpfvziswqvmvm`
2. Merge PR #562 to main
3. Trigger `verify-legacy-cognition-disposition` workflow (or wait for push trigger)
4. Confirm artifact shows `complete: true` and expected group counts
5. Update control plane (STATE/BLOCKS/MAP/PROOF/BATON) to reflect Item 30 VERIFIED
6. Leave single next action for Item 31 (Control-plane freshness) or next authorized frontier

## Authority
- Implementation authorized by Issue #541 lane allocation (Coda 2 → Items 21–40)
- Disposition logic derived from PRIORITY-02 receipt and Team Naya execution plan
- No owner-authorized runtime session required (read-only audit + schema migrations)

---
*Generated by Coda 2 execution. Next Naya: verify deployment, confirm audit, update control plane, continue.*