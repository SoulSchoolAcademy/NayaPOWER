# P0 Gate Spec: Canonical-Capture Exclusivity

**Law:** The canonical Receiver (`supabase/functions/v7-smart-note-canonical`) is the
SINGLE canonical capture path. Durable intelligence objects are Intelligent Blocks.
Never create a second memory.

**Gate:** `scripts/gate-canonical-capture.py` — FAILS (exit 1, fail-closed) when a
second capture/memory path appears.

## Checks

| ID | What | How |
|----|------|-----|
| C1 | Live DB has no unallowlisted intelligence tables | Read-only `pg_tables` scan vs allowlist + name patterns |
| C2 | No unauthorized writes to intelligence tables | Static scan of all edge functions: every `.from(T).insert/upsert/update/delete` on an intelligence table must be explicitly allowlisted |
| C3 | Canonical creation RPCs only invoked by Receiver | Static scan: `v7_create_smart_note`, `nayanet_record_cognition_event` |
| C4 | No new intelligence tables in migrations | `CREATE TABLE` scan vs allowlist + name patterns |

## Allowlisted writers (verified by reading source on main, 2026-10-07)

- `nayanet_intelligent_blocks`: Receiver creates via `v7_create_smart_note` RPC;
  `nayanet-learning-verify` may UPDATE (governed promotion transitions only).
- `nayanet_cognition_events`: Receiver creates via `nayanet_record_cognition_event` RPC.
- `learning_evidence`: Receiver INSERTs one CANDIDATE row per Smart Note
  (canonical seeding); `nayanet-learning-verify` INSERT/UPDATE (promotion).
- `nayanet_brain_relationships`: Receiver via RPC; `nayanet-learning-verify` UPDATE.
- `nayanet_intelligence_index`, `nayanet_intelligence_lineage`,
  `nayanet_checkpoint_receipts`: Receiver pipeline RPCs.
- `nayanet_project_cognition_state`: `nayanet-learning-verify` UPDATE.
- `nayanet_collective_wisdom`, `nayanet_successor_handoffs`, `nayanet_smart_ledger`:
  no writers — any writer FAILS.

## Explicitly out of scope (documented)

- `.naya/capture/*.json` staging: file-based, PR-reviewed. Staging is not
  persistence; edge functions cannot read the repo filesystem.
- Operational tables (`nayanet_execution_receipts`, `nayanet_execution_outcomes`,
  `nayanet_authority_grants`, `nayanet_github_dispatch_receipts`): receipts and
  grants, governed elsewhere — not second memories.
- Direct SQL via API: governance boundary (read-only policy), not a code path.

## Key findings from the investigation

1. `naya-decision-context/index.ts` EXISTS in the repo (history to 2026-09-20)
   but is READ-ONLY (single SELECT on `learning_evidence`, zero writes).
   Naya 4's "phantom" finding holds for PERSISTENCE — it writes nothing, so it
   is not a second memory. The file's existence is recorded here so the gate's
   allowlist is explicit rather than assuming absence. Whether it is DEPLOYED
   as a live edge function is unverified from here.
2. `v7_smart_note_transactions` is referenced by `nayanet-github-dispatch` as
   "the authoritative record" but DOES NOT EXIST in the live DB. Broken reference,
   not a second memory — flagged for the owning lane.
3. `nayanet-learning-verify` is the only non-Receiver writer to intelligence
   tables, and only for governed promotion (CANDIDATE→ACTIVE/REJECTED). This is
   the LEARN lifecycle step, explicitly allowlisted with justification.
4. The gate caught its author's own incomplete allowlist during testing (the
   Receiver's CANDIDATE seeding INSERT) — verification before trust, applied
   to the gate itself.

## CI wiring (proposed)

Follow the `regenerate_brain_index.py --check` pattern: run on PRs touching
`supabase/functions/**` or `supabase/migrations/**`. Static checks (C2/C3/C4)
run without credentials; C1 needs the read-only Supabase skill.

## Falsifier

`--self-test`: 5 fixtures. Mock shadow INSERT into `nayanet_intelligent_blocks`
(C2), mock shadow table migration (C4), rogue RPC invoker (C3) — all must FAIL.
Allowlisted writers and read-only consumers — must PASS. 5/5 green, 2026-10-07.
