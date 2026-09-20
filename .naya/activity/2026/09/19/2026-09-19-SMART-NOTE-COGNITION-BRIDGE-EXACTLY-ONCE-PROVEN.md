# Smart Note -> Cognition Bridge + Exactly-Once Projection Proof

Date: 2026-09-19
Status: PROVEN at database authenticated-context level

## Inspected
- Live GitHub main HEAD at execution start: ad1b9841598968c8d361290524a1cd955c2002ca.
- Live Supabase Smart Note, Cognition, Smart Ledger, and Intelligence Index contracts.
- Existing Smart Note duplicate index triggers.
- Existing Cognition -> Smart Ledger trigger.
- Existing Intelligence Index writer.
- Existing authenticated v7_create_smart_note contract.

## Executed
1. Added deterministic Smart Note -> Cognition bridge.
2. Removed redundant Smart Note Intelligence Index trigger.
3. Added Cognition -> Intelligence Index projection trigger.
4. Executed v7_create_smart_note under Supabase authenticated role with JWT sub for an existing owner.
5. Replayed the identical idempotency key.
6. Verified cardinality across Smart Note, Cognition, Ledger, Index, and transaction records.

## Proven transaction
Smart Note event: 9bdb54e0-359e-4b0e-ad2b-00c62ca8aa80
Cognition row: ba7d66ad-6323-4d78-8ac4-7df1956d45fb
Cognition event identity: smart_note:9bdb54e0-359e-4b0e-ad2b-00c62ca8aa80
Smart Note Ledger row: 4664d4a1-c3ac-460e-af3a-eab4f6e05a27
Cognition Ledger row: f07a05b9-38ea-44d2-a59b-8d2e10d28e41

## Cardinality
- Smart Note event: 1
- Cognition event: 1
- Smart Note Ledger: 1
- Cognition Ledger: 1
- Smart Note Index: 1
- Cognition Index: 1
- Smart Note transaction: 1

Replay returned the original event ID and transaction row; it did not create a second Smart Note transaction.

## Trigger state
smart_note_events now has:
- nayanet_index_smart_note_event -> nayanet_index_intelligence_row
- nayanet_smart_note_event_to_cognition -> nayanet_smart_note_to_cognition
- nayanet_smart_note_event_to_smart_ledger -> nayanet_smart_note_to_ledger

The redundant trg_smart_note_events_to_intelligence_index is removed.

nayanet_cognition_events now has:
- nayanet_cognition_event_to_smart_ledger -> nayanet_cognition_event_to_ledger
- nayanet_index_cognition_event -> nayanet_index_intelligence_row

## Architecture result
One Smart Note remains the domain event. Cognition is the generalized event identity layer. Smart Ledger remains the evidence/integrity projection. Intelligence Index remains the retrieval projection.

No third event store was created.

## Authentication boundary
This was a real database transaction executed under Supabase's authenticated Postgres role with the owner's JWT subject claim, exercising the same auth.uid/RLS context used by Supabase authenticated requests.

This proves the authenticated database execution path and ownership binding. It is not a substitute for a separate browser/client proof using an externally issued access token.

## Remaining
- Run the same transaction through the deployed Hub/client session.
- Prove two-independent-real-user isolation.
- Backfill historical Smart Notes only if later required; none was done here.
- Reconcile four live Smart Note artifacts against the desired five-perspective product contract.

## Protected
No third event table, no Ledger replacement, no governance weakening, no duplicate Smart Note index trigger, no verifier weakening.
