# Superbrain canonical event lifecycle — observed 2026-08-25

## Verified facts

The authoritative corpus currently consists of chronological Note Events loaded by `.naya/memory/smart_notes_v3.py`. Validation, duplicate/entity audit, relationship graph construction, derived indexing, retrieval, Daily CIS, and continuity enforcement consume that corpus.

The authoritative gate proves the corpus is valid, but the repository does **not yet prove a single production write function used by every event-producing caller**. Therefore this pass adds a safe canonical/idempotent creation primitive for controlled adoption rather than falsely declaring the write path fully centralized.

## Target lifecycle

`INPUT → IDENTITY/IDEMPOTENCY → CANONICAL EVENT → VALIDATION → PERSISTENCE → RECEIPT → DELIVERY → HANDOFF → DERIVED INDEX`

## New implementation

`.naya/runtime/canonical_event_store.py` provides:

- deterministic content fingerprinting;
- source/event idempotency keys;
- atomic `O_EXCL` creation;
- replay detection;
- conflict detection instead of overwrite;
- deterministic idempotency index.

It is root-injectable for safe tests and does not rewrite historical corpus files.

## Remaining adoption boundary

The next safe step is to route the real production event-producing callers through `create_or_replay()` (or a thin canonical adapter) only after every caller has been enumerated and its compatibility contract proven.

This distinction is intentional: **the primitive is implemented and tested; universal production adoption is not yet claimed.**
