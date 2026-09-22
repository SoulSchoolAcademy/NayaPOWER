# Intelligent Block V1 — Real Event → Block → Evidence → Retrieval Proof

Date: 2026-09-21
Status: PROVEN

## Boundary executed

Existing verified Smart Note event:
- canonical event/block ID: b06846b3-49eb-45c1-8557-a986831f0d4c
- Smart Note idempotency key: smart-note-oznwb9
- owner scope: PRIVATE
- Smart Note status: VERIFIED
- source: wave-a-canonical-shell-acceptance
- receipt: 592f90c7-a4d6-4348-811a-ba9b5cd884fd

The existing intelligent_block payload was promoted into the new first-class:
public.nayanet_intelligent_blocks

No parallel event store was introduced.

## Result

Block:
- block_id: b06846b3-49eb-45c1-8557-a986831f0d4c
- title: Wave A canonical September 17 shell acceptance
- block_type: INSIGHT
- version: 1
- status: DURABLE
- understanding_state: VERIFIED
- schema_version: INTELLIGENT_BLOCK_V1
- source_event_ids: [b06846b3-49eb-45c1-8557-a986831f0d4c]
- privacy: PRIVATE

Evidence:
- source_table: smart_note_events
- source_id: b06846b3-49eb-45c1-8557-a986831f0d4c
- receipt_id: 592f90c7-a4d6-4348-811a-ba9b5cd884fd
- verified_at: 2026-09-20T23:23:32.215278+00:00
- original evidence chain preserved:
  human_note → naya_note → machine_note → intelligence_feed → intelligent_block

## Retrieval proof

The canonical retrieval function:
nayanet_get_intelligent_block(block_id)

was executed with the owner's authenticated claim context and returned the same block_id, owner_id, source_event_ids, evidence_refs, provenance, content, state, privacy, and schema version.

The returned object retained:
- the same Block identity;
- the same canonical source event identity;
- the same evidence receipt;
- the same verification timestamp;
- the same provenance;
- the same understanding state.

## Intelligence Index proof

The first-class Block automatically projected into the existing Intelligence Index:

- index source_table: nayanet_intelligent_blocks
- index source_id: b06846b3-49eb-45c1-8557-a986831f0d4c
- object_type: INTELLIGENT_BLOCK
- index_id: 5c5ba965-0985-4abb-a874-0868846e176e
- index status: DURABLE

Live database checks:
- first-class block count: 1
- indexed block count: 1
- Smart Note → Block trigger: present
- Block → Intelligence Index trigger: present
- authorized retrieval function: present

## What changed

A single causal boundary was added:

SMART NOTE / CANONICAL EVENT
→ INTELLIGENT BLOCK V1
→ INTELLIGENCE INDEX
→ AUTHORIZED RETRIEVAL

Future Smart Note transactions now automatically promote their existing intelligent_block payload into the first-class Block table through the governed trigger.

The existing Cognition Event, Execution Receipt, Smart Ledger, Notification, Project Intelligence, Activity, and Hub systems were not replaced or duplicated.

## Proof classification

EVENT: PROVEN
BLOCK: PROVEN
EVIDENCE LINK: PROVEN
INDEX PROJECTION: PROVEN
AUTHORIZED RETRIEVAL: PROVEN

This proof does not claim the full human browser journey is repaired. The previously recorded AppShellV3 human-capture failure remains an independent frontier.

## Successor

Next proof should test idempotent replay/update of the same Smart Note transaction and then prove that a second verified event can create a new Block without identity collision, while preserving source-event lineage and Intelligence Index retrieval.

No Hub redesign.
No parallel event store.
No broad schema rewrite.
