# PROOF PACKET A — DB Prerequisites for Persistence Promotion
**Status:** IN-FLIGHT (evidence complete; 2 human-gated items open)
**Generated:** 2026-10-01 · **Owner:** Naya 2 (Muse)

## 1. Claim
The database prerequisites for promoting the persistence seam are enumerated
with each item's verified state: what is applied in production, what exists
only as source, and what is blocked on a human or a disposable environment.

## 2. Authority
Shawn's second master execution directive (2026-10-01): close the persistence
interface. Standing prohibitions: no production DB writes/migrations by any
seat (human-only); no self-merge; read-only production inspection authorized
and used throughout.

## 3. Source binding
- Repo main pinned at `a726a8376559609a3620f948ec7bfcabdba50abb` for migration
  inventory (161 files in `supabase/migrations/`). Main has since moved to
  `694f62cd6b8dae8a6f9ce802be58ac4ae4488188` (2026-10-01); the inventory
  must be re-pinned before any promotion decision.
- Persistence branch `naya2/persistence-integration-package` @ `2a7851a8`.

## 4. Production ground truth (read-only, 2026-10-01)
| Item | Observed state | How verified |
|---|---|---|
| `nayanet_smart_ledger` table | live, 23 columns | `information_schema` via sb-mgmt |
| RLS on ledger | enabled (`relrowsecurity=true`) | `pg_class` |
| SELECT policy | 1 policy: `auth.uid() = owner_id` for `authenticated` | `pg_policy` expr read |
| INSERT/UPDATE/DELETE for `authenticated` | none (writes via service_role / security-definer) | `pg_policies` count = 1 |
| `nayanet_record_ledger_event` | live | `pg_proc` |
| V2.1 functions (`..._v2_1_state`, `..._projection_v2_1`, `..._attach_v2_1`) | **NOT present** | `pg_proc` — only the base writer found |
| Latest applied migration | `20260930233137` | `supabase_migrations.schema_migrations` |
| V2.1 migration file `20261001032000` | present in repo, **not applied** | file vs `schema_migrations` diff |

## 5. Reconciliation
SOURCE PRESENT ≠ MIGRATION APPLIED (standing law, confirmed again): the V2.1
typed-receipt functions exist at main `a726a837` but are absent from
production. No drift in the ledger table itself (23 columns as expected).

## 6. Material findings
- Owner isolation is a **real policy**, not a column: `auth.uid() = owner_id`,
  verified in `pg_policy`. An `owner_id` column alone would not prove this —
  the policy does.
- The V2.1 attach path's conflict semantics (`VALUE_RECEIPT_ALREADY_ATTACHED`
  on conflicting payload, idempotent return on identical replay) are
  specified in the migration but **not executable** until a human applies it.
- 12-field reconstruction proven against a real retrieved row
  (`375f74e7…`, 0 violations) with explicit rules for derived fields
  (`owner_scope` ← vocabulary mapping, `updated_at` := `created_at` for
  append-only events, `truth_state` ← `verification.assessment_state`,
  `superseded_by` ← reverse query, proven empty).

## 7. Execution record
Read-only SQL via `sb-mgmt` (Management API), 2026-10-01 ~09:20–09:45 PDT.
No writes attempted. Reconstruction script: `/tmp/reconstruct-12field.py`
(exit 0, 0 violations).

## 8. Acceptance chain
ENUMERATED ✓ → READ-ONLY VERIFIED ✓ → HUMAN-GATED ITEMS IDENTIFIED ✓ →
APPLIED ⏳ (human) → ISOLATED ROUND TRIP ⏳ (disposable DB)

## 9. What this packet did and did not establish
Established: exact prerequisite inventory with verified applied/present
states; owner-isolation policy reality; reconstruction rules. Did NOT
establish: V2.1 functions applied (human step); isolated round trip executed
(blocked: no disposable Postgres available to this seat).

## 10. Receipts
- Isolated-DB handoff: `~/workspace/naya/isolated-db-handoff/` (README +
  `roundtrip.py`, syntax-checked, refuses production URLs)
- Reconstruction: `/tmp/reconstruct-12field.py`, `/tmp/v21-connect.py`
- V2.1 migration: `supabase/migrations/20261001032000_decision_value_smart_ledger_v2_1.sql`
  @ `a726a837`

## Open human-gated items
1. **Apply migration `20261001032000`** to production (migration-application
   law: human step; verify post-apply per runbook).
2. **Provide a disposable Postgres** (or authorize a throwaway Supabase
   project) so `roundtrip.py` can execute the isolated round trip.
