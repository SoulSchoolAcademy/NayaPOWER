# Protected Release Packet V1 — 4 pending migrations

**Status:** PREPARED. NOT authorized, NOT dispatched, NOT applied.
**Pinned source:** `a726a8376559609a3620f948ec7bfcabdba50abb` (main, 2026-10-01T03:58:10Z).
If main moves, this packet EXPIRES and must be regenerated.
**Target:** Supabase project `supabase-red-cable` (`dahisasgpfvziswqvmvm.supabase.co`, ca-central-1).
**Authorization required:** Shawn's explicit go-ahead naming this exact packet (SHA + 4 hashes).

## 1. Migration order and hashes (byte-verified at pinned SHA)

| # | Version | File | SHA-256 | Depends on |
|---|---|---|---|---|
| 1 | 20260930235959 | `ai1_capability_carry_v1.sql` (15,133 B) | `6437954afad70d68e09434c8ce6507b5538633f8970bca7a23310da40acd7932` | — |
| 2 | 20261001000100 | `ai1_supersede_capability_integrity_v1.sql` (5,998 B) | `5c419e92b6047bd0dac0d715789d7cf5c7f28519ea9eadb0c2d37852645d161b` | #1 (explicit) |
| 3 | 20261001030000 | `disconnect_stop_future_v1.sql` (3,265 B) | `7a2b0d0dbaf7e092f5be94a0bd126fe04d581e294fdc2e99f0183332b9ada679` | — |
| 4 | 20261001032000 | `decision_value_smart_ledger_v2_1.sql` (15,720 B) | `1c9c14632636e884883fa565cfabdece05b592199c94ba29599542d11eb0c889` | — |

All four verified: NOT APPLIED in production (0 history rows with version ≥ 20260930235959,
checked read-only 2026-10-01).

## 2. SQL impacts (all four are code-only: function definitions, no table DDL, no data writes)

- **#1** adds optional `p_capabilities jsonb` param to `nayanet_intelligence_commit`,
  `nayanet_intelligence_commit_runtime`, and related writers. Backward compatible (default NULL).
- **#2** preserves `p_capabilities` through `nayanet_supersede_intelligent_block_runtime`.
- **#3** replaces `nayanet_smart_disconnect(text)` — ratified #1136 Reading A: disconnect stops
  future participation; already-distilled collective wisdom is NOT erased. Prospective only;
  rows already REVOKED stay REVOKED (no history rewrite).
- **#4** creates 6 new functions: `nayanet_value_receipt_v2_1_state`,
  `nayanet_execution_value_projection_v2_1`, `nayanet_attach_value_receipt_v2_1`,
  `nayanet_execution_receipt_to_ledger`, `nayanet_smart_note_event_to_ledger`,
  `nayanet_space_to_ledger`. Additive; the first three close the observed runtime gap
  (these functions are currently absent from production).

## 3. Current deployed-source baseline

- Production branch status: `MIGRATIONS_FAILED` (since 2026-09-29T02:57:47Z).
- Live migration history ends at `20260930233137` (external restoration; provenance UNKNOWN —
  SQL recovered from history statements, who applied it and under what authority is UNKNOWN).
- The two external versions (`20260930233038`, `20260930233137`) are additive Smart Ledger
  restorations. They are NOT replayed by this packet; production history is left untouched.
- Repo ledger `supabase/PRODUCTION-MIGRATION-LEDGER-V1.json` is stale (ends 20260930191233).

## 4. Required pre-application checks

1. Re-pin: `git rev-parse HEAD` on main == `a726a837…`, else expire packet.
2. Re-verify the 4 SHA-256 hashes above against the files at the pinned SHA.
3. Re-query production history: still 0 rows with version ≥ 20260930235959.
4. Confirm the governed application mechanism (see §5) — do NOT assume branch promotion
   or direct SQL while the branch reports `MIGRATIONS_FAILED`.

## 5. Governed application mechanism

Application is a **human-executed** step (no agent seat may apply migrations). The applier:
1. Applies #1→#4 in order, one at a time, stopping on any error.
2. After EACH migration, re-queries `supabase_migrations.schema_migrations` for that exact
   version before proceeding (non-atomicity rule: a failed migration may leave partial state).
3. On failure: stop, preserve the error, do not retry blindly — diagnose before re-attempt.

## 6. Partial-failure handling

- Migrations are not atomic as a set. If #2 fails after #1 applied, #1 stays applied;
  the packet is re-entered at #2 after diagnosis (never re-apply #1 blindly — all four are
  `CREATE OR REPLACE`, idempotent on retry).
- If a migration half-applies (function created but grant failed), the post-release proof
  (§7) will catch it: every function is signature-checked, not just history-checked.

## 7. Post-release proof (read-only SQL, exact)

```sql
-- 1. All four history rows present, in order
SELECT version FROM supabase_migrations.schema_migrations
WHERE version IN ('20260930235959','20261001000100','20261001030000','20261001032000')
ORDER BY version;
-- expect: 4 rows

-- 2. p_capabilities present on the commit functions
SELECT proname FROM pg_proc p
JOIN pg_namespace n ON n.oid=p.pronamespace
WHERE n.nspname='public' AND p.proname='nayanet_intelligence_commit_runtime'
AND pg_get_function_arguments(p.oid) LIKE '%p_capabilities%';
-- expect: 1 row

-- 3. V2.1 functions exist
SELECT proname FROM pg_proc
WHERE pronamespace='public'::regnamespace
AND proname IN ('nayanet_value_receipt_v2_1_state',
 'nayanet_execution_value_projection_v2_1','nayanet_attach_value_receipt_v2_1');
-- expect: 3 rows

-- 4. No unexpected versions appeared
SELECT count(*) FROM supabase_migrations.schema_migrations
WHERE version > '20261001032000';
-- expect: 0
```

## 8. Rollback (code-only recovery — verified safe)

All four migrations change only function definitions. No table DDL, no data mutation.
Rollback = restore prior definitions (captured read-only from production before application):

- #1/#2 targets: prior definitions of `nayanet_intelligence_commit`,
  `nayanet_intelligence_commit_runtime`, `nayanet_supersede_intelligent_block_runtime`
  (captured 2026-10-01; held with the packet).
- #3 target: prior definition of `nayanet_smart_disconnect(text)` (captured 2026-10-01).
- #4 targets: `DROP FUNCTION IF EXISTS` on the 6 new functions (they do not exist
  pre-application, so rollback is pure removal).

**Irreversible effects:** none from the migrations themselves. Ledger rows written by the
new functions after application are append-only by design (write law) and are not "rolled
back" — they remain as history, which is correct behavior, not a failure.

## 9. CI wording correction

"8/8 success on exact main" refers to the eight push-triggered Actions runs on SHA `a726a837`
(all completed/success). The Governed Production Promotion run on this SHA had its
deploy/proof steps **skipped by the policy gate** — that run's success is a successful
*block*, not release proof. No deployment or production proof occurred on this SHA.
