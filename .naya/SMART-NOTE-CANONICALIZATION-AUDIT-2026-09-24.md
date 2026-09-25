# 🔱 SMART NOTE CANONICALIZATION AUDIT — 2026-09-24

## Executive result

The repository had accumulated multiple Smart Note definitions, storage families, UI representations, runtime paths, and historical naming dialects.

The canonical model is now:

> **SMART NOTE = INTELLIGENT BLOCK**

One semantic object, one canonical meaning, one canonical physical repository home, many authorized projections.

### Current authority

1. `.naya/SMART-NOTE-CONTRACT-V1.md` — one human Smart Note contract.
2. `contracts/intelligent-block-v1.schema.json` — machine schema `NAYANET_INTELLIGENT_BLOCK_V1`.
3. `contracts/intelligent-block-v1.md` — human-readable Intelligent Block contract.
4. `SUPERBRAIN/CONTINUITY/NAYA-REPOSITORY-OPERATING-STANDARD.md §19.1` — canonical Smart Note path resolver.
5. `NAYANET/HUB/FOUNDATION-CONTRACT.md` — Hub event/block projection contract.

---

## 1. Implementation / schema inventory

The full repository tree was scanned for Smart Note / Intelligent Block path families. The scan produced **321 matching Smart Note-like paths** across code, tests, docs, historical notes, projections, and feature directories.

The most important implementation layers are:

### Canonical semantic contracts

- `contracts/intelligent-block-v1.schema.json`
- `contracts/intelligent-block-v1.yaml`
- `contracts/intelligent-block-v1.md`
- `.naya/project-intelligence/INTELLIGENT-BLOCK-V1.md`

### Smart Note contract / protocol history

- `.naya/2026-09-11-NAYAPOWER-02-WHAT-IS-NAYA-SMART-NOTE.md`
- `.naya/NAYA-SMART-NOTE-PROTOCOL-OFFICIAL.md`
- `.naya/SMART-NOTE-PROTOCOL.md`
- `.naya/SMART-NOTE-THREE-LAYER-LOCK.md`
- `SUPERBRAIN/ARCHITECTURE/NAYANET/509-AAA-SMART-NOTES-01-09-CANONICAL.md`
- `SUPERBRAIN/CONTINUITY/NAYA-REPOSITORY-OPERATING-STANDARD.md §19.1`

### Runtime / creation / validation

- `.naya/runtime/smart_note_transaction.py`
- `.naya/runtime/smart_note_calendar.py`
- `.naya/runtime/smart_note_candidate.py`
- `.naya/memory/smart_note_enforcement.py`
- `.naya/memory/smart_notes_v3.py`
- `.naya/runtime/cct_intelligent_block.py`

### Live Supabase runtime

- `supabase/functions/v7-smart-note-canonical/index.ts`
- `supabase/functions/naya-smart-feed/index.ts`
- `supabase/functions/nayanet-compound-intelligence/index.ts`

### Verification

- `.github/workflows/verify-human-smart-note-capture.yml`
- `.github/workflows/verify-live-smart-note-receiver.yml`
- `.github/workflows/verify-canonical-hub-smart-note-golden-path.yml`
- `.github/workflows/verify-intelligent-block-lifecycle.yml`
- `tests/test_smart_note_enforcement.py`
- `tests/test_smart_note_replay_completion_contract.py`
- `tests/test_smart_note_transaction_rollback.py`
- `tests/test_smart_note_transaction_concurrency.py`
- `tests/test_smart_note_canonical_resolver.py`
- `tests/test_smart_note_canonical_contract_v1.py`

---

## 2. Storage inventory

The full tree contains these major Smart Note storage families:

### CURRENT CANONICAL

`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`

Logical namespace:

`NayaPOWER/SMART-NOTES/YYYY/MM/DD/`

Identity:

`IB-XXXXXX`

Registry:

`.naya/memory/smart-notes/REGISTRY.json`

### HISTORICAL / LEGACY / COMPATIBILITY

- `.naya/SUPERBRAIN/SMART-NOTES/`
- `.naya/memory/notes/`
- `.naya/project-intelligence/smart-notes/`
- `NAYA/SMART-NOTES/`
- `NAYANET/SMART-NOTES/`
- `SUPERBRAIN/SMART-NOTES/`
- `SUPERBRAIN/CONTINUITY/NAYAPOWER/SMART-NOTES/`
- `SUPERBRAIN/CONTINUITY/TEAM-NAYA/PROJECTS/NAYANET/**/SMART-NOTES/`
- `SUPERBRAIN/INTELLIGENCE/NAYA/SMART-NOTES/`
- `SUPERBRAIN/MASTER-NOTES/NAYA-NOTES/`
- `SUPERBRAIN/AI-NOTES/`
- `docs/smart-notes/`

These locations may remain for history and migration. They are not new-write targets.

### NOT A SMART NOTE HOME

`.naya/memory/events/`

This is the canonical event/provenance layer. A Smart Note is linked to its event; the event store is not a second Smart Note folder.

---

## 3. UI representations

### Hub

`NAYANET/HUB/index.html`

The Hub's canonical conceptual rendering is:

`IDENTITY → NUTSHELL → PERSPECTIVES → WEAVER / CONNECTIONS → LESSON → MEANING → ACTION`

### Component renderer

`NAYANET/HUB/src/app/SmartNoteSurface.tsx`

This is the Smart Note capture boundary. It now verifies the returned object is `NAYANET_INTELLIGENT_BLOCK_V1` and contains the canonical block fields before treating the capture as successful.

### Feed board

`NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx`

Consumes `event.intelligent_block`, truth, authority, value, lifecycle, integrity, and progressive human views.

### Public Smart Feed projection

`NAYANET/HUB/public/smart-feed.js`

Renders the Intelligent Block as a feed card with perspective layers and identity/trust metadata.

### Legacy 509 corpus renderer

The Hub contains a historical 509 Smart Note parser for its built-in reference corpus. It is now explicitly classified as a legacy/reference corpus, not the current Smart Note creation contract.

---

## 4. Create / read APIs and functions

### Browser runtime

`window.NayaAssistantRuntime.captureSmartNote(input)`

Creates a Smart Note through the canonical Supabase receiver.

`window.NayaAssistantRuntime.retrieve(eventId)`

Retrieves the canonical cognition event by event identity.

### Supabase receiver

`POST /functions/v1/v7-smart-note-canonical`

This is the canonical live Smart Note receiver.

### Database transaction

`v7_create_smart_note`

Persists the human note, Naya note, machine note, feed event, Intelligent Block, evidence, and Hub state at the governed persistence boundary.

### Downstream readers / projections

- `naya-smart-feed` retrieves permitted cognition events and hydrates the associated Intelligent Block projection.
- `nayanet-compound-intelligence` restores, retrieves, reconciles, projects, learns, checkpoints, supersedes, and compounds intelligence.
- `.naya/memory/smart_notes_v3.py` provides dependency-free canonical event retrieval with authorization, ranking, metadata filtering, and relationship-aware reranking.

### Repository writers

`.naya/runtime/smart_note_transaction.py` owns the canonical human-readable Smart Note persistence boundary.

`.naya/runtime/smart_note_calendar.py` owns canonical date-folder placement and day indexing.

---

## 5. Historical naming conventions

Observed historical names include:

- Smart Note
- SMART NOTE
- Smart Notes
- Naya Note / NAYA NOTE
- Shawn Note / SHAWN NOTE
- Human Note / HUMAN NOTE
- Child / CHILD
- Child Note
- Child / Derived Note
- Grandma / GRANDMA NOTE
- Naya / NAYA NOTE
- Machine / MACHINE NOTE
- Adaptive Learning
- Adapter Learning
- Learning Lesson
- What It Means
- Ultimate Meaning
- Why It Matters
- How to Use It
- How to Apply It
- What's In It For Me / You / Us
- What's In It For You?
- Intelligent Block
- Intelligent Event
- Note Event
- AI Note
- Smart Notes + Receipts
- Smart Notes + CIS
- Smart Note Transaction

The V1 contract removes ambiguity by mapping these into one canonical object and a fixed human-readable view order.

---

## 6. Canonical human-readable structure

Every completed Smart Note MUST use:

1. IN A NUTSHELL
2. DATE / TIME
3. WHAT
4. WHY IT MATTERS
5. HUMAN
6. CHILD
7. GRANDMA
8. NAYA
9. MACHINE
10. WHAT WE LEARNED
11. CONNECTIONS
12. HOW TO APPLY
13. WHAT IT ULTIMATELY MEANS
14. WHAT'S IN IT FOR YOU / US
15. NEXT ACTION

The section order is now defined only by:

`.naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md`

Historical protocols remain readable but are subordinate.

---

## 7. Canonical identity/storage model

```text
CANONICAL EVENT
  event_id
      ↓
INTELLIGENT BLOCK
  intelligent_block_id = IB-XXXXXX
  schema_version = NAYANET_INTELLIGENT_BLOCK_V1
      ↓
SMART NOTE HUMAN ADDRESS
  .naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md
      ↓
REGISTRY / DAY INDEX
  .naya/memory/smart-notes/REGISTRY.json
  .naya/memory/smart-notes/YYYY/MM/DD/INDEX.md
      ↓
AUTHORIZED PROJECTIONS
  Hub / Feed / Activity / Reports / Library / Learning / Dream / API
```

There is one semantic object. Local IDs may exist at projection boundaries, but they do not replace canonical identity.

---

## 8. Migration policy

Historical Smart Notes are not mass-deleted.

The migration sequence is:

`IDENTIFY → CLASSIFY → PRESERVE → LINK → RECONCILE → VERIFY`

New creation MUST resolve to the canonical path.

Retrieval MUST use canonical identity/date/topic/intelligence indexes, not arbitrary directory hunting.

---

## 9. 2026-09-24 reconciliation

### Removed

A previously created non-canonical artifact:

`.naya/project-intelligence/smart-notes/2026/09/24/2026-09-24-smart-doors-universal-intelligence-interface.md`

was removed because it did not follow the canonical Smart Note structure and would have created another competing Smart Note location.

### Existing September 24 scorecard receipt

`.naya/project-intelligence/2026-09-24-NAYA3-14-QUESTION-EXECUTION-SCORECARD-RECEIPT.md`

remains as a project-intelligence evidence/receipt artifact. It is not itself the canonical Smart Note.

### Next

Create the official 2026-09-24 Superbrain Scorecard Smart Note under:

`.naya/memory/smart-notes/2026/09/24/system/superbrain-scorecard/IB-000002/smart-note.md`

It is registered in `.naya/memory/smart-notes/REGISTRY.json` and the 2026-09-24 daily index, and announced through the canonical Intelligent Feed projection.

---

## 10. Verification boundary

Source changes are committed to `main`.

This audit is **repository/source verified**.

The live Cloudflare worker could not be independently retrieved from this environment, so no claim is made here that the deployed runtime has already adopted these source changes.

The remaining production proof is:

`CREATE → PERSIST → EVENT → BLOCK → INDEX → RETRIEVE → HUB → RELOAD → VERIFY`

That is the exact boundary the next live test must close.
