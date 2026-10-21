# IB-SMART-NOTE-20261006-sn0477-production-deploy-two-saves.md

Intelligent Block: SN-0477
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-06
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Two database safeguards saved the production deploy on 2026-10-06: a foreign key constraint blocked deletion of receipts with child outcomes (forcing verification that children were also duplicates), and Supabase's migration tracker refused deployment on version mismatches (forcing alignment of manually-applied migrations). Both "failures" were the system working correctly. The lesson: when the database says no, read why before overriding — it's usually protecting you.

## HUMAN NOTE

On 2026-10-06, during the production dedup + deploy session:

**Save 1 — Foreign key.** The dedup SQL tried to delete 19 duplicate receipts. The database refused: `violates foreign key constraint "nayanet_execution_outcomes_receipt_id_fkey"`. The receipts had child rows in the outcomes table. Instead of forcing it, I read the child rows — all 19 were semantic duplicates too (identical except ID references). Updated the SQL to delete children first, backed them up, verified every surviving receipt still had exactly one outcome. The constraint forced the careful path.

**Save 2 — Migration tracker.** After the dedup, the Supabase deployment failed with "Remote migration versions not found in local migrations directory." Two causes found: (a) the two migrations run via SQL Editor weren't in Supabase's applied-migrations history (manual runs don't register); (b) an older version mismatch — DB had `20261006001836`, file was `20261006001500`, same migration, different number. Both fixed with bookkeeping SQL (INSERT the missing history records, UPDATE the mismatched version). The tracker forced the alignment.

**The pattern:** Both were cases where the operator (me/Shawn) thought the database was wrong, but the database was right. The FK prevented orphaned children. The tracker prevented deploying with untracked schema state. "When the database says no, read why" — it's a load-bearing verification, not an obstacle.

## CHILD NOTE

The database has safety guards. Twice today, the database said "no" when we tried to do something — and both times, it was right. It stopped us from deleting important connected data, and it stopped us from deploying when the records didn't match. Always ask why the database said no before trying to force it.

## GRANDMA NOTE

Think of the database like a careful librarian. When we tried to remove some duplicate cards from the catalog, she said "wait — those cards have notes attached to them." And when we tried to update the library, she said "wait — my records don't match your list." Both times she was protecting the library. We listened, fixed the real issues, and everything worked.

## NAYA NOTE

For future production work: (1) Always check for child rows (FK constraints) before deleting — query the dependent tables first. (2) After any manual SQL migration, immediately register it in `supabase_migrations.schema_migrations` — the SQL Editor doesn't do this automatically. (3) Before dispatching a deploy, compare DB history versions against repo migration filenames — a simple set-difference query catches mismatches. (4) When a safeguard fires, the first move is investigation, not override. The safeguard is evidence that the system is working.

## MACHINE NOTE

```json
{
  "sn": "SN-0477",
  "truth_state": "CANDIDATE",
  "date": "2026-10-06",
  "saves": [
    {
      "guard": "foreign_key",
      "constraint": "nayanet_execution_outcomes_receipt_id_fkey",
      "trigger": "DELETE on nayanet_execution_receipts",
      "finding": "19 child outcome rows, all semantic duplicates",
      "resolution": "delete children first, backup both, verify 1:1 outcome integrity"
    },
    {
      "guard": "migration_tracker",
      "error": "Remote migration versions not found in local migrations directory",
      "causes": [
        "manual SQL Editor runs not in supabase_migrations.schema_migrations",
        "version mismatch: DB 20261006001836 vs file 20261006001500 (same migration)"
      ],
      "resolution": "INSERT missing history records; UPDATE mismatched version to filename"
    }
  ],
  "doctrine": "When the database says no, read why before overriding.",
  "checklist": [
    "query dependent tables before DELETE",
    "register manual migrations in schema_migrations immediately",
    "diff DB history vs repo filenames before deploy dispatch"
  ]
}
```
