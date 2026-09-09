# Priority 2 — Legacy Cognition-Event Cohort Disposition Specification

Status: ACTIVE (read-only investigation). No DB mutation authorized unless separately granted.

## 1. The cohort (exact predicate)

```
nayanet_cognition_events.id has NO Smart Ledger row where
  source_table = 'nayanet_cognition_events'
  AND source_id = cognition_event.id::text
```

Recorded census (2026-09-23, live production DB):

| Metric | Value |
|---|---|
| Cognition events (total) | 4,561 |
| Cognition events with Smart Ledger linkage | 4,473 |
| Unlinked cohort | **88** |

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
  cognition event (`2026-09-19 01:53:49 UTC`); events before it are outside ledger scope by policy.
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
- Running the audit workflow = read-only verification → authorized once the RPC exists.
- This session performed NO mutation. The cohort census numbers (4,561 / 4,473 / 88) are recorded
  from the prior coordinated session and remain pending independent re-derivation via the RPC.

## 5. Delivered / open

- DELIVERED: exact predicate, group composition with lineage anchors, non-destructive disposition policy.
- DELIVERED: read-only aggregate RPC definition + audit verification workflow + reusable script.
- OPEN: production application of the RPC migration + independent census run (authorization-gated).
- OPEN: confirmation that the 88 membership is stable (fingerprint comparison across runs).