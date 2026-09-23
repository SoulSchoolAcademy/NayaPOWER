# ACTION 07 — ACTIVITY + LEDGER BINDING

## MISSION

Make the Communication + Organization causal chain observable through the existing Activity/cognition and Smart Ledger substrates without creating a second event store.

## EXACT EXECUTION

1. Inspect live cognition/Activity projections and Smart Ledger functions.
2. Inspect current membership JOIN/LEAVE event writes.
3. Inspect current Connection SAVE/REVOKE event writes.
4. Inspect Smart List add/remove paths for missing event consequences.
5. Inspect Smart Mail send/verify receipt→cognition→Ledger lineage after the relationship gate.
6. Determine the smallest missing event/projection changes.
7. Add only missing canonical event writes.
8. Ensure every consequential mutation carries actor, target/context, provenance, authorization boundary and idempotency identity.
9. Prove one JOIN event, one Connection event, one List event, and one Mail event through the canonical substrate.
10. Prove no duplicate event on replay.
11. Verify Ledger lineage where the existing contract requires it.
12. Update Team Naya, feature records, Job 04 and the master directive.

## HARD RULES

- Do not create a second Activity table.
- Do not create a second Ledger.
- Do not manufacture events from the UI.
- Do not claim Ledger closure unless the actual canonical function/trigger is observed.
- Do not weaken privacy or authority.

## REQUIRED REPORT

DONE / PROOF / NOT PROVEN / DECISION / BLOCKERS / NEXT.

NEXT must be a complete cold-start master execution directive.
