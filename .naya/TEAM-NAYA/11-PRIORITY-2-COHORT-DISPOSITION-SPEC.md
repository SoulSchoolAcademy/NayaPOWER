# Priority 2 — Legacy Cognition-Event Cohort Disposition Specification

Status: VERIFIED (read-only census re-derived live on 2026-09-23). RPC migration applied 2026-09-23 under explicit production authorization (default DENY satisfied). No data mutation. Cohort = 88, stable, membership confirmed by fingerprint + exact group match.

## 1. The cohort (exact predicate)

```
nayanet_cognition_events.id has NO Smart Ledger row where
  source_table = 'nayanet_cognition_events'
  AND source_id = cognition_event.id::text
```

Recorded census (2026-09-23, live production DB) and live re-derivation via RPC:

| Metric | Recorded | Live RPC re-derived (2026-09-23T21:50:29Z) |
|---|---|---|
| Cognition events (total) | 4,561 | **4,653** (grew +92; new events added since census) |
| Cognition events with Smart Ledger linkage | 4,473 | **4,565** (grew +92; all new events ledgered) |
| Unlinked cohort | **88** | **88 (exact match)** |
| Group breakdown | 45/22/12/4/4/1 | **45/22/12/4/4/1 (exact match)** |
| Cohort fingerprint (sha256) | (not recorded) | `58fc76519416537537a4fd6ffaf051041ab90164aecbe60410223222cb90ec8e` |
| First ledgered cognition `event_at` | `2026-09-19 01:53:49 UTC` (ledger `created_at`) | `2026-09-17T20:00:00+00:00` (uses source `event_at`) |

Both totals rising by exactly +92 means since the originally recorded census every new cognition
event has carried Smart Ledger lineage — the going-forward gate is already working. The cohort
(unlinked) count is byte-for-byte stable at 88 with an identical composition.

Independent reproduction of these numbers requires the read-only aggregate RPC
(`nayanet_smart_ledger_coverage_audit()`), which is server-side (SECURITY DEFINER) because
Smart Ledger RLS is strictly owner-scoped — no ordinary session can census another owner's rows.

## 2. Cohort composition (reasoned groups, lineage-anchored)

| Count | type | classification | source | repo-side anchor |
|---|---|---|---|---|
| 45 | communication | observation | nayanet-smart-mail | Wave-A Smart Mail proofs (STATE known: `35409875337`, `35472129371`; `.naya/activity/2026/09/19/*WAVE-A-SMART-MAIL-BOUNDARY-REPAIRED*`) |
| 22 | intelligence | observation | nayanet-name-first-runtime-proof | Name-First corrected run `35470526689` |
| 12 | intelligence | observation | nayanet-authenticated-assistant-proof | Authenticated lifecycle run `35470519946` |
| 4 | intelligence | observation | dream-learning-decision-proof | `.github/workflows/verify-dream-learning-decision.yml` (source literal; run `35470535019`) |
| 4 | intelligence | decision_context_test | dream-learning-decision-proof | same workflow |
| 1 | verification | authenticated_lifecycle | NayaNET 10/10 readiness gate | 10/10 readiness gate run |

All 88 are pre-ledger records: Smart Ledger foundation migration
`20260919021000_smart_ledger_foundation_v1.sql` postdates them; STATE records the first
ledgered cognition event at `2026-09-19 01:53:49 UTC`.

## 3. Disposition semantics (non-destructive default)

- **Class:** `HISTORICAL_PRE_LEDGER`. Rows immutable. No backfill. No deletion. No fabricated linkage.
- **Obligation boundary:** Smart Ledger coverage obligation begins at the first ledgered
  cognition event. Ledger rows first appear at `2026-09-17 20:00 UTC` by source `event_at`
  (laeder `created_at` boundary previously stated as `2026-09-19 01:53:49 UTC`); events before
  ledger scope are outside ledger coverage by policy.
- **Going-forward mechanic:** a ledger-completeness gate requires NEW cognition events to carry
  ledger lineage, so the gap class cannot recur (this is already enforced by the canonical
  ingress chain: provenance → validation → integration → ledger → indexing).
- **Audit:** the read-only aggregate census (`nayanet_smart_ledger_coverage_audit()`) emits
  counts + cohort fingerprint (sha256, no content) to prove the cohort is stable and shrinkable,
  without exposing any row data.
- **Watch:** if `unlinked_cognition` grows after ledger-scope date, treat as a NEW defect, not
  legacy history.

## 4. Authorization model

- Migration (add RPC) = DB mutation → requires explicit production authorization (default DENY).
  **APPLIED 2026-09-23** under explicit human authorization (SQL Editor run).
- Running the audit workflow = read-only verification → authorized once the RPC exists.
  **RUN 2026-09-23T21:50:29Z (local harness mirroring the workflow): VERIFIED.**
- This session performed NO mutation beyond the authorized RPC creation. The cohort census is now
  independently re-derived (88; fingerprint `58fc7651…c90ec8e`).

## 5. Delivered / open

- DELIVERED: exact predicate, group composition with lineage anchors, non-destructive disposition policy.
- DELIVERED: read-only aggregate RPC definition + audit verification workflow + reusable script.
- DONE: RPC applied; independent census re-derived live → cohort = 88 stable, exact composition match.
- DONE: fingerprint baseline `58fc76519416537537a4fd6ffaf051041ab90164aecbe60410223222cb90ec8e` captured
  for future stability comparison.
- OPEN: CI run of the verify workflow via GitHub Actions once PR #542 merges (workflow file only
  dispatchable from default branch).