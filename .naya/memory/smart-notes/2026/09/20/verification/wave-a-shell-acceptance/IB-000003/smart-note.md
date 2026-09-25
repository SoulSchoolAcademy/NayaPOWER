# SMART NOTE — Wave A canonical September 17 shell acceptance

**Intelligent Block ID:** IB-000003  
**Date / Time:** 2026-09-20 23:23:32 UTC  
**Category:** VERIFICATION  
**Topic:** Wave A shell acceptance  
**Status:** DURABLE / VERIFIED  
**Canonical Contract:** `.naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md`

## IN A NUTSHELL

The live canonical receiver contains **IB-000003** as the Intelligent Block for the verified Wave A canonical September 17 shell acceptance.

## DATE / TIME

**Created:** 2026-09-20T23:23:32.183Z  
**Receiver updated:** 2026-09-22T01:27:25.702834Z  
**Source event verified:** 2026-09-20T23:23:32.215278Z

## WHAT

The receiver's exact canonical object is:

- `intelligent_block_id`: IB-000003
- `block_id`: b06846b3-49eb-45c1-8557-a986831f0d4c
- `owner_id`: 48c40e43-8cca-4c6e-9427-d3bfd7d788db
- `subject_id`: Wave A canonical September 17 shell acceptance
- `title`: Wave A canonical September 17 shell acceptance
- `block_type`: INSIGHT
- `version`: 1
- `status`: DURABLE
- `understanding_state`: VERIFIED
- `owner_scope`: PRIVATE
- `schema_version`: INTELLIGENT_BLOCK_V1
- `source_event_ids`: [b06846b3-49eb-45c1-8557-a986831f0d4c]

The receiver content says browser acceptance proved the protected September 17 Hub shell can invoke the existing authenticated Smart Note runtime without replacing the visual source.

## WHY IT MATTERS

This projection exists to preserve the live receiver's already-established identity and provenance without allocating or changing the identity locally.

The repository is a projection of the receiver object; it is not the source of its identity.

## HUMAN

The human-readable meaning is the receiver's verified shell-acceptance observation described above. No stronger claim is added here.

## CHILD

The live system already has the box: **IB-000003**. This repository file is the readable copy of what that box contains; it does not create the box or choose its number.

## GRANDMA

The official receiver is the original record. This file is the labeled copy that helps a future Naya find and understand that record. If the copy disagrees with the receiver, the receiver wins.

## NAYA

The critical rule demonstrated by this object is:

**RECEIVER IDENTITY → REPOSITORY PROJECTION → AUTHORIZED RETRIEVAL**

The receiver assigned IB-000003. The repository did not infer or allocate that identity.

## MACHINE

```json
{
  "intelligent_block_id": "IB-000003",
  "block_id": "b06846b3-49eb-45c1-8557-a986831f0d4c",
  "owner_id": "48c40e43-8cca-4c6e-9427-d3bfd7d788db",
  "subject_id": "Wave A canonical September 17 shell acceptance",
  "title": "Wave A canonical September 17 shell acceptance",
  "block_type": "INSIGHT",
  "version": 1,
  "status": "DURABLE",
  "understanding_state": "VERIFIED",
  "owner_scope": "PRIVATE",
  "source_event_ids": [
    "b06846b3-49eb-45c1-8557-a986831f0d4c"
  ],
  "source_event": {
    "table": "smart_note_events",
    "id": "b06846b3-49eb-45c1-8557-a986831f0d4c",
    "event_type": "SMART_NOTE",
    "status": "VERIFIED",
    "privacy_state": "PRIVATE",
    "idempotency_key": "smart-note-oznwb9"
  },
  "evidence": {
    "receipt_id": "592f90c7-a4d6-4348-811a-ba9b5cd884fd",
    "verified_at": "2026-09-20T23:23:32.215278+00:00",
    "source_table": "smart_note_events"
  },
  "provenance": {
    "source": "smart_note",
    "created_from": "v7_create_smart_note",
    "idempotency_key": "smart-note-oznwb9",
    "canonical_event_id": "b06846b3-49eb-45c1-8557-a986831f0d4c"
  },
  "project": "NayaNET",
  "permissions": {
    "access": "PRIVATE"
  },
  "authority": null,
  "learning_state": null,
  "applicable_scope": {
    "privacy": "PRIVATE"
  },
  "intelligence_index": {
    "index_id": "5c5ba965-0985-4abb-a874-0868846e176e",
    "source_table": "nayanet_intelligent_blocks",
    "source_id": "b06846b3-49eb-45c1-8557-a986831f0d4c",
    "status": "DURABLE",
    "project_id": "NayaNET"
  }
}
```

**Authority note:** The live receiver row and linked authority-grant lookup did not provide a separate authority grant for this object. The repository therefore records `authority: null` rather than inventing one.

**Learning note:** The receiver row does not expose a separate learning-promotion state. The repository therefore records `learning_state: null` rather than treating `understanding_state: VERIFIED` as learning.

## WHAT WE LEARNED

The receiver is authoritative for IB identity and canonical object content. The repository can safely preserve a projection only when it carries the receiver's immutable identifiers and provenance and does not fabricate missing authority or learning metadata.

## CONNECTIONS

- Source event: `b06846b3-49eb-45c1-8557-a986831f0d4c`
- Evidence receipt: `592f90c7-a4d6-4348-811a-ba9b5cd884fd`
- Intelligence index: `5c5ba965-0985-4abb-a874-0868846e176e`
- Canonical registry: `.naya/memory/smart-notes/REGISTRY.json`
- Retrieval runtime: `.naya/memory/smart_notes_v3.py`

## HOW TO APPLY

A future Naya should resolve **IB-000003** through the canonical registry, enforce the stored owner/scope/project/permission boundary, retrieve it through the canonical retrieval runtime, and use the receiver as the authoritative reconciliation source when projection and receiver differ.

## WHAT IT ULTIMATELY MEANS

**IB-000003 is real receiver-backed intelligence.** Its identity, owner, source event, provenance, verification state, privacy scope, and NayaNET project association are grounded in live receiver evidence. Missing authority and learning fields remain explicitly unknown.

## WHAT'S IN IT FOR YOU / US

A cold Naya can now follow one real object from live receiver identity into a repository projection without relying on historical migration guesses or local IB numbering.

## NEXT ACTION

Independently authenticate the intended owner against the live receiver and retrieve IB-000003 through the production authorization boundary; compare that returned object field-for-field with this projection and then prove cold context restoration from the same canonical object.
