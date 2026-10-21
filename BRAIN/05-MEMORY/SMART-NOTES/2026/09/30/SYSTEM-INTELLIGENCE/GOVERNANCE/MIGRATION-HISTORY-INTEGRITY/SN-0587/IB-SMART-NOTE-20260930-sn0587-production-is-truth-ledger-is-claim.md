# IB-SMART-NOTE — SN-0587 — Production Is the Truth, the Ledger Is a Claim

Intelligent Block: IB-SMART-NOTE-20260930-sn0587-production-is-truth-ledger-is-claim
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
When the migration ledger said `20261006235900_nayanet_cold_retrieve_search_v1` was PENDING_REVIEW_NOT_PRODUCTION_APPLIED but the production database showed it fully applied (column, GIN index, trigger, 175/175 backfilled rows, all four functions present), the drive loop trusted the database and flagged the ledger as stale — without editing the ledger itself. The rule: a ledger is a claim about production; production is the truth. When they diverge, verify against the live source of truth, act on what it says, and flag the record for its owning lane to update — never rewrite a governed record from inside a loop that didn't create it.

## HUMAN NOTE
Shawn, during tonight's governed production deployment, the drive loop hit a contradiction: the migration ledger said the cold-retrieve migration was still "pending review, not production applied," but the production database had it fully applied — search_vector column, GIN index, the trigger, all 175 rows backfilled, all four SQL functions present. The loop did the right thing: it believed the database (the ground truth), skipped re-applying the migration, and flagged the stale ledger entry for a follow-up update — it did NOT reach in and rewrite the ledger itself. That restraint matters: the ledger is a governed record with its own checksum and history baseline; a loop that quietly edits another lane's governed record is how audit trails die. Divergence found → verify against the live source → act on the truth → flag the claim for its owner to repair.

## CHILD NOTE
If the map says the treasure isn't buried but you can see it sticking out of the ground, believe your eyes — and tell the mapmaker to fix the map. You don't scribble on someone else's map, though!

## GRANDMA NOTE
Honey, the filing cabinet says the bill isn't paid, but your bank statement says it is — the bank is the truth and the cabinet is just what somebody wrote down. You note the mistake for the bookkeeper; you don't sneak into her office and change her books yourself.

## NAYA NOTE
This is the ledger-truth ordering rule, and it generalizes beyond migrations: any ledger/registry/count-file is a DERIVED claim about a source of truth, never the truth itself. On divergence: (1) verify the source of truth directly with full-row reads (never a truncated instrument — SN-0354's correction); (2) act on what the source of truth says (here: migration already applied → do not re-apply); (3) flag the stale claim for its owning lane to update through its governed path; (4) never self-repair another lane's governed record (SN-0240 family, no-supersession). Tonight's instance also carries the first completed governed deploy proof under Shawn's explicit 23:11Z authorization — run 37701589614, 19/20 post-deploy proofs, and the live-connect parity check (deployed artifact == e363732b) closing the SN-0388 stale-deploy seam. The one kernel RED (#1789, SN-0213 brain-index drift, PR-introduced) was classified, routed to the LEARN lane via PR comment 6048869373, and left unrepaired — one-repair-per-class (SN-0236), no duplication.

## MACHINE NOTE
{
  "smart_note_id": "SN-0587",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn0587-production-is-truth-ledger-is-claim",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "GOVERNANCE",
  "subtopic": "MIGRATION_HISTORY_INTEGRITY",
  "captured_at": "2026-10-07",
  "rule": "production_is_truth_ledger_is_claim_flag_divergence_never_self_edit_governed_record",
  "procedure": ["on ledger-vs-reality divergence, verify the source of truth directly with full reads", "act on the source of truth", "flag the stale claim for its owning lane to repair via its governed path", "never self-edit another lane's governed record"],
  "related": ["SN-0240 (tripwire firing RED on real drift is correct behavior)", "SN-0354 (check contradicts evidence — reconcile the DB directly)", "SN-0356 (truncated-instrument correction)", "SN-0388 (deployed URL is not the deployed product)"],
  "evidence": ["#1354 comment 6048915954 (DRIVE-LOOP sign-out, 2026-10-07T23:27:38Z): migration 20261006235900 verified applied in production, ledger stale and flagged", "PRODUCTION-MIGRATION-LEDGER-V1.json records PENDING_REVIEW_NOT_PRODUCTION_APPLIED", "production deploy run 37701589614 under Shawn's explicit 23:11Z authorization"]
}
