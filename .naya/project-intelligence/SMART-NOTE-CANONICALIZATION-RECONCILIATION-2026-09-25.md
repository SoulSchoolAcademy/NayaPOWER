# 🔎 Smart Note Canonicalization — Runtime Reconciliation Receipt

**Date:** 2026-09-25  
**Repository:** SoulSchoolAcademy/NayaPOWER  
**Observed main:** `7bfbac3e59fd69a199cebfc9bbdfa17a8742b5b9`  
**Supabase project:** `dahisasgpfvziswqvmvm`  
**Rule:** No new Smart Note is to be created until this reconciliation boundary is accepted.

## Executive finding

The repository already contains a ratified canonical Smart Note / Intelligent Block contract, but the implementation still contains **competing historical/runtime representations**.

The most important concrete defect found is:

> `.naya/runtime/smart_note_transaction.py` locally allocates IB identities from a repository registry, while the ratified contract and live `v7-smart-note-canonical` receiver require the live receiver to allocate the authoritative IB identity.

That violates the canonical identity law and has now been guarded by a failing-first test on branch `naya/smart-note-canonicalization-20260925`.

## 1. Implementations / schemas found

### Canonical contract
- `.naya/codex/CANONICAL-SMART-NOTE-INTELLIGENT-BLOCK-SYSTEM-V1.md`
- Schema: `NAYANET_INTELLIGENT_BLOCK_V1`
- Smart Note = human-facing name.
- Intelligent Block = canonical machine object.
- IB identity = `IB-XXXXXX`.

### Repository runtime helpers
- `.naya/runtime/smart_note_transaction.py`
- `.naya/runtime/smart_note_candidate.py`
- `.naya/runtime/smart_note_calendar.py`
- `.naya/memory/smart-notes/REGISTRY.json`

### Live receiver
- Supabase Edge Function: `v7-smart-note-canonical`
- Live version observed: **19**
- The receiver explicitly allocates the IB identity and passes it into the persisted transaction.

### Database contract
- `public.v7_create_smart_note`
- `public.nayanet_intelligent_blocks`
- `public.smart_note_events`
- `public.smart_note_artifacts`
- `public.smart_note_receipts`

## 2. Storage locations found

| Location | Current role |
|---|---|
| `public.nayanet_intelligent_blocks` | **CANONICAL MACHINE OBJECT** |
| `public.smart_note_events` | **CANONICAL SOURCE EVENT / INTAKE LINEAGE** |
| `public.smart_note_receipts` | **CANONICAL VERIFICATION RECEIPT** |
| `public.smart_note_artifacts` | **SOURCE/PROCESSING ARTIFACT PROJECTION** |
| `public.v7_smart_note_transactions` | **TRANSACTION/COMPATIBILITY ENVELOPE** |
| `public.nayanet_cognition_events` | **COGNITION PROJECTION** |
| `public.nayanet_intelligence_index` | **RETRIEVAL INDEX PROJECTION** |
| `public.nayanet_intelligence_lineage` | **LINEAGE PROJECTION** |
| `.naya/memory/smart-notes/.../IB-XXXXXX/smart-note.md` | **CANONICAL HUMAN-READABLE REPOSITORY PROJECTION** |
| `.naya/memory/smart-notes/REGISTRY.json` | **REPOSITORY PROJECTION REGISTRY; never an identity authority** |
| `.naya/memory/intelligence/` | **LEGACY/LOCAL CIS + receipt projection machinery** |
| `NAYANET/HUB/public/intelligence/pis-feed.json` | **PIS/HUB PROJECTION** |
| `public.nayanet_notes` | **LEGACY COMPATIBILITY STORE** |

## 3. UI representations found

### Current runtime surface
`NAYANET/HUB/index.html` contains:
- Smart Notes capture surface;
- canonical runtime capture through `NayaAssistantRuntime.captureSmartNote()`;
- canonical IB deep-link `/hub?ib=<IB-ID>`;
- owner-scoped retrieval through `retrieveIntelligentBlock()`.

### Historical UI
The same Hub source still contains a **509 reference Smart Note renderer** and historical nine-note presentation.

These are explicitly described in source as legacy/reference material and MUST remain projections/history, not a second creation authority.

## 4. Creation/read functions found

### Creation
- Hub → `NayaAssistantRuntime.captureSmartNote()`
- Supabase `v7-smart-note-canonical`
- Supabase RPC `v7_create_smart_note`
- DB verification `verify_smart_note()`
- DB trigger → cognition/index/lineage/intelligent-block projections

### Retrieval
- Hub deep-link → `retrieveIntelligentBlock(IB-ID)`
- `v7_list_smart_notes()`
- `v7_list_smart_note_events()`
- canonical intelligence index / cognition retrieval paths

### Legacy/compatibility
- `nayanet_notes`
- `smart_note_candidate.py`
- repository Smart Note registry/projection helpers

## 5. Historical naming conventions found

- `Smart Note`
- `SMART_NOTE`
- `SN-...`
- `SMART NOTE 01–09`
- `Naya Power #...`
- UUID source event / database row IDs
- `IB-XXXXXX`
- `IB:<event UUID>` inside the older/live envelope identity representation
- `NAYANET_INTELLIGENT_BLOCK_V1`
- `INTELLIGENT_BLOCK_V1`
- `nayanet_notes`
- `v7_smart_note_transactions`

The last two identity/schema spellings are especially important: the database has an authoritative `IB-XXXXXX` field, while the envelope builder also historically emitted an `object_id` form. The DB RPC currently overwrites the identity with the receiver-issued `IB-XXXXXX`; retrieval must use that canonical field.

## 6. Canonical structure

The ratified contract defines the human structure as:

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

The machine contract additionally requires stable identity, source event, owner/scope, timestamps, provenance, authority, permissions, truth/verification, relationships, lineage, learning, applicability, actions, and outcomes.

## 7. Canonical identity/storage decision

**ONE CANONICAL OBJECT:** Intelligent Block.

**ONE CANONICAL ID:** receiver-issued `IB-XXXXXX`.

**ONE CANONICAL SOURCE EVENT:** owner-scoped `smart_note_events.id` UUID, linked to the IB.

**ONE HUMAN PROJECTION:** `.naya/memory/smart-notes/.../IB-XXXXXX/smart-note.md`.

The repository path is an index/projection. It is never an identity authority.

## 8. Today's runtime evidence

Observed production counts:

- `smart_note_events`: **900**
- `smart_note_artifacts`: **3,600**
- `smart_note_receipts`: **900**
- `v7_smart_note_transactions`: **894**
- `nayanet_notes`: **4**
- `nayanet_intelligent_blocks`: **857**
- `nayanet_cognition_events`: **7,354**
- `nayanet_intelligence_index`: **34,794**

Recent canonical IBs include `IB-000860`, `IB-000859`, `IB-000858`, etc.

Recent Smart Note events are VERIFIED and have corresponding Intelligent Block rows.

The counts do **not** prove universal one-to-one reconciliation. They prove the system currently has multiple populations that require classification before today's notes are declared reconciled.

## 9. Immediate defects / gaps

1. **Local identity allocation defect — FOUND.**
   The repository helper could allocate IB IDs independently. This contradicts the canonical receiver law.

2. **Human schema validation gap — FOUND.**
   The repository helper previously did not require all 15 canonical human sections; it omitted explicit `DATE / TIME`, `WHAT`, and `WHAT IT ULTIMATELY MEANS` from its required validation list.

3. **Historical UI coexistence — FOUND.**
   The canonical Hub contains legacy nine-note rendering. It must remain clearly classified as historical/reference projection and never become a creation/retrieval authority.

4. **Multiple runtime stores — CONFIRMED.**
   The database contains source events, artifacts, receipts, transaction envelopes, cognition events, intelligent blocks, indexes, lineage, and legacy notes. These must be projections/lineage, not competing intelligence identities.

5. **Full today's migration/reconciliation — NOT YET EXECUTED.**
   No destructive cleanup has been performed.

## 10. Safety boundary

**Do not create another Smart Note yet.**

Do not delete or mutate historical records merely to make counts match.

Do not backfill identity by guessing.

Reconciliation must be lineage-preserving and evidence-driven.

## 11. Success condition

Today's Smart Notes may be declared reconciled only when every candidate record can answer:

`WHAT IS THE CANONICAL IB ID? → WHAT IS THE SOURCE EVENT? → WHERE IS THE AUTHORITATIVE OBJECT? → WHAT ARE THE PROJECTIONS? → WHAT IS LEGACY? → IS THE LINEAGE VERIFIED?`

