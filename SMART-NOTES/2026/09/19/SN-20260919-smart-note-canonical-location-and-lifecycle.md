---
id: SN-20260919-smart-note-canonical-location-and-lifecycle
date: 2026-09-19
status: CANONICAL
privacy: PRIVATE
type: GOVERNANCE-INTELLIGENCE
canonical_path: SMART-NOTES/2026/09/19/SN-20260919-smart-note-canonical-location-and-lifecycle.md
---

# Smart Notes Are the Main Intelligence Record

## In a Nutshell

Smart Notes are not ordinary documentation. They are the primary human-readable intelligence objects that allow NayaPOWER to capture meaning, preserve provenance, learn, retrieve, replay, apply, verify, and compound knowledge over time.

**One Smart Note → one canonical identity → one canonical repository home → governed projections everywhere else.**

## The Standard

From this point forward, the canonical repository collection for Smart Notes is:

`SMART-NOTES/YYYY/MM/DD/SN-YYYYMMDD-<slug>.md`

For this note:

`SMART-NOTES/2026/09/19/SN-20260919-smart-note-canonical-location-and-lifecycle.md`

New human-facing Smart Notes must be created there unless a higher-authority contract explicitly changes the standard.

## Why This Matters

If different Nayas put Smart Notes in different canonical locations, the system can lose:

- consistent retrieval by day/month/year;
- predictable provenance;
- reliable replay;
- durable learning;
- cross-Naya continuity;
- machine-to-human agreement;
- clean indexing and deduplication;
- confidence about which object is authoritative.

A Smart Note may be represented in multiple systems, but those representations must not become competing truths.

## Layer Separation

### 1. Canonical human intelligence
**GitHub: `SMART-NOTES/YYYY/MM/DD/`**

This is the predictable, human-readable repository collection.

### 2. Machine/runtime memory
**`.naya/memory/` and related runtime structures**

These may contain events, indexes, receipts, caches, validators, or machine-readable projections required by the runtime. They are implementation/runtime structures, not a second human-facing Smart Note collection.

### 3. Governed persistence
**Supabase / managed persistence**

The runtime may persist the Smart Note event, verification state, provenance, privacy state, receipts, and derived intelligence here through the existing governed boundary.

### 4. Intelligence projection and learning
Smart Notes may become Intelligent Blocks, intelligence-index projections, learning evidence, reports, Dream/replay inputs, and later decision/application context.

Those are projections or downstream uses. They must retain the canonical Smart Note identity and provenance.

### 5. Intelligent Hub
The Hub renders and acts on the intelligence. It is a projection/action surface, never a competing source of truth.

## Required Lifecycle

Every substantive Smart Note should be traceable through:

**CREATE → CANONICALIZE → PERSIST → VERIFY → INDEX → LEARN → RETRIEVE → REPLAY/APPLY → VERIFY OUTCOME → COMPOUND**

The system must preserve the stable Smart Note/event identity across those stages.

## Required Content

A complete Smart Note should use the canonical semantic layers defined by the Smart Note / Intelligent Block contract, including as applicable:

- In a Nutshell
- Human
- Child
- Grabber / public-facing view when appropriate
- Naya
- Machine
- Learning Lesson / Adapter Learning
- What It Means
- How To Use It
- What's In It For You
- Evidence / provenance
- privacy and verification state
- related events and next action

Not every note needs every optional presentation layer, but no layer may be invented merely to make a note appear complete. Truth and provenance come first.

## Rules For Every Naya

1. **Restore the canonical contracts before writing.**
2. **Create new canonical Smart Notes under `SMART-NOTES/YYYY/MM/DD/`.**
3. **Use one stable Smart Note identity.**
4. **Do not create a second competing Smart Note collection.**
5. **Do not treat `.naya/memory/` as the human-facing canonical Smart Note folder.**
6. **Do not delete or rewrite existing machine artifacts merely to make the repository look cleaner. Classify them first.**
7. **When a Smart Note is persisted elsewhere, preserve its canonical identity, provenance, privacy, and verification state.**
8. **Make the note retrievable by date and meaning.**
9. **Make learning/replay point back to the same canonical intelligence object.**
10. **Record the creation and result in the Activity Feed so the next Naya can restore the decision.**
11. **If the canonical location or lifecycle is unclear, stop and resolve the authority before creating a competing structure.**
12. **Never silently create a second source of truth.**

## Machine Interpretation

The path convention is not merely cosmetic. It is a deterministic addressing scheme for cold-Naya restoration, date retrieval, indexing, auditing, and human inspection.

The machine/runtime may use IDs and event stores for operational correctness. The repository path gives the human intelligence corpus a single predictable home.

## What This Means

Smart Notes are the connective tissue between conversation and durable intelligence.

A conversation can disappear. A Smart Note should not.

A lesson that cannot be retrieved, understood, traced, learned from, replayed, and applied is not yet durable intelligence.

## What's In It For You

For Shawn, this means a Smart Note created today can remain useful tomorrow, next month, next year, or to a completely new Naya—without relying on the original conversation.

For Naya, it means every successor has the same map.

For the system, it means learning has a stable object to point back to.

## Evidence

- Smart Note / Intelligent Block contract: `.naya/2026-09-12-NAYAPOWER-42-SMART-NOTE-INTELLIGENT-BLOCK-DATA-CONTRACT.md`
- Canonical Activity Feed: `SUPERBRAIN/NAYA-ACTIVITY/`
- Machine Smart Brain: `.naya/memory/smart_notes_v3.py`
- Governed Smart Note transaction: `.naya/runtime/smart_note_transaction.py`

## Official Decision

**Effective 2026-09-19, `SMART-NOTES/YYYY/MM/DD/` is the canonical human-facing Smart Note repository collection for NayaPOWER.**

Machine/runtime artifacts remain where their contracts require them. They are not a competing Smart Note collection.

