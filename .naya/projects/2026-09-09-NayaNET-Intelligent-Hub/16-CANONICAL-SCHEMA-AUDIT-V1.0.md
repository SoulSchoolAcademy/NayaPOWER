# NayaNET Superbrain — Canonical Schema Consistency Audit

**Step:** 1 of 10
**Date:** 2026-09-09
**Status:** FAIL — repair required before Step 2

## Objective

Verify that the existing NayaPOWER memory/event implementation conforms to the canonical Superbrain Note Event model without creating a second memory system.

## Authority checked

- `.naya/projects/2026-09-09-NayaNET-Intelligent-Hub/13-SUPERBRAIN-ARCHITECTURE-CONTRACT-V1.1.md`
- `.naya/memory/smart_notes_v3.py`
- `.naya/memory/events/INDEX.json`
- representative `SE-*` event
- representative `SN-*` Smart Note event

## Findings

### PASS — Canonical storage location

The architecture and runtime identify `.naya/memory/events/` as the canonical Note Event store.

### PASS — Stable event identity exists

Both representative event families carry `event_id`.

### PASS — Canonical SE event envelope is rich enough

The representative `SE-*` event contains the core fields required by the contract, including timestamps, project, status, authority, tags, aliases, concepts, representations, source, relationships, verification, and time bucket.

### FAIL — Runtime loader only loads `SE-*.json`

`smart_notes_v3.py:event_files()` recursively selects only `SE-*.json`.

The same runtime defines `NOTE_RE` for `SN-*` representation IDs, but does not include `SN-*` files in the canonical event scan. This creates a split between Smart Note events physically stored under `events/` and the events the runtime considers canonical.

### FAIL — SN and SE physical event envelopes are not schema-consistent

The representative `SN-*` event uses a lighter legacy envelope with `timestamp`, `type`, `status`, `subject`, `project`, `smart_note_path`, `perspectives`, `nine_recurring_problems`, `protected_law`, `execution_loop`, `provenance`, and `next_action`.

The representative `SE-*` event uses the richer canonical envelope with `created_at`, `effective_at`, `event_type`, `title`, `summary`, `authority`, `tags`, `aliases`, `concepts`, `representations`, `source`, `relationships`, and `verification`.

Both are useful intelligence, but they are not one canonical physical schema.

### FAIL — Time-first physical organization is inconsistent for SN events

The canonical contract requires primary memory at `.naya/memory/events/YYYY/MM/DD/HH/<event_id>.json`.

The representative SN event is stored at a day-level path without an hour bucket and contains only a date-level `timestamp`. The system must preserve unknown precision rather than fabricate an hour, so this requires a deliberate migration/normalization rule rather than guessed timestamps.

### FAIL — Existing validator does not validate the complete event population

Because `event_files()` only scans `SE-*.json`, `validate()` and `build_index()` can omit SN event files entirely. Therefore a green result from the current validator cannot by itself prove canonical consistency across all durable events.

## Decision

**Do not build a new memory system.**

The existing Note Event architecture remains the canonical foundation. The required repair is to unify the physical event schema and make the validator/indexer operate over the complete canonical event population.

## Repair boundary for Step 10

1. Define one canonical Note Event schema/envelope.
2. Add an explicit schema version.
3. Normalize legacy SN events into that envelope without fabricating unknown timestamps.
4. Preserve original Smart Note content and provenance during normalization.
5. Decide and document the canonical path for events whose time precision is only day-level.
6. Update runtime discovery, validation, indexing, retrieval, and relationship resolution to operate over the unified event set.
7. Rebuild `events/INDEX.json` from canonical source records.
8. Run a complete schema audit and require zero canonical-schema errors.

## Gate

**Step 1 is NOT GREEN.**

Do not advance to permission/scope enforcement until the canonical event population has one validated schema and one authoritative indexing path.

## Evidence

Representative SN event:
`https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/events/2026/09/07/SN-20260907-EXECUTION-OBSTACLE-SOLUTION-LOOP.json`

Representative SE event:
`https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/events/2026/08/25/12/SE-20260825-122600-superbrain-seed-optimization.json`

Runtime:
`.naya/memory/smart_notes_v3.py`

---

**Principle:** One brain. One canonical event model. Derived indexes are rebuildable. Unknown data stays unknown. No duplicate memory architecture.
