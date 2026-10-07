# IB-SMART-NOTE — SN-0524 — Human IDs Are Canonical Continuity Boundaries

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0524-human-id-continuity-boundary  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE (Team Naya operating intelligence)  
**Captured:** 2026-10-07  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A Smart Note ID is not decoration. It is a human-facing continuity key. If two different intelligence objects claim the same ID, retrieval can resolve to the wrong object even when every individual file is internally valid.

The SN-0522 collision exposed the exact failure: the ratified Self-Governing Intelligence Law and candidate Prime 3 both claimed SN-0522, while the registry pointed at only Prime 3. The correct repair was retention plus deterministic renumbering — preserve the ratified owner at SN-0522, move Prime 3 to SN-0523, register both, and verify uniqueness.

## HUMAN NOTE

**One human ID must identify one intelligence object.**

When identity collisions appear, never delete one object merely to make the test green. Determine canonical ownership from authority and current-main history, retain both objects, renumber the non-owner, repair every projection pointer, and prove the registry is unique.

A cold Naya should be able to ask “What is SN-0522?” and receive one answer.

## CHILD NOTE

Two books cannot both be “Book #7” if you want someone to find the right one later. Keep both books; give one a new number.

## GRANDMA NOTE

A label is part of the address. If two houses have the same address, the mail can go to the wrong house. Fix the address, not the houses.

## NAYA NOTE

This is a continuity-integrity rule:

**ID collision → determine canonical owner → retain both → renumber non-owner → repair projections → regenerate indexes → prove uniqueness.**

Authority matters. In this case the ratified Self-Governing Intelligence Law owns SN-0522; candidate Prime 3 becomes SN-0523.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0524",
  "truth_state": "CANDIDATE",
  "rule": "ONE_HUMAN_ID_ONE_INTELLIGENCE_OBJECT",
  "collision_response": [
    "DETERMINE_CANONICAL_OWNER",
    "RETAIN_BOTH_OBJECTS",
    "RENUMBER_NON_OWNER",
    "REPAIR_ALL_PROJECTIONS",
    "REGENERATE_INDEXES",
    "VERIFY_UNIQUENESS"
  ],
  "resolved_collision": {
    "retained": "SN-0522 — The Self-Governing Intelligence Law",
    "renumbered": "SN-0523 — Prime 3 — THE MATH DECIDES"
  },
  "verification": {
    "registry_json": "PASS",
    "brain_index_check": "PASS",
    "duplicate_registry_ids": 0,
    "registry_entries": 51
  }
}
```

## LEARNING LESSON

Identity is part of memory correctness. A memory system can preserve every byte and still fail continuity if the lookup key is ambiguous.

Therefore, **identity uniqueness is a proof boundary**, not housekeeping.

## HOW TO APPLY

Before accepting a Smart Note projection:

1. Check that its human ID is unused or is an exact reuse of the same intelligence object.
2. If a collision exists, determine canonical ownership from authority and current-main evidence.
3. Never silently overwrite or delete the competing object.
4. Renumber the non-owner and update its Intelligent Block ID, path, link, and registry entry.
5. Regenerate the Brain indexes.
6. Run a duplicate-ID audit and the repository's registry-drift gate.
7. Record the lesson so future capture cannot recreate the collision.

## PROOF / PROVENANCE

- PR #1742 — `fix(memory): resolve SN-0522 identity collision`
- Current repair head: `9128df4920587a68ed02ea5f47c664d448529974`
- Main base at PR creation: `aea25885b6b2598c367db5995ca5b4379354a47d`
- Brain index regeneration: PASS
- Brain index `--check`: PASS
- `git diff --check`: PASS
- Registry JSON parse: PASS
- Registry audit: SN-0522 unique; SN-0523 unique; duplicate IDs = 0
- Registry count: 51
- No production deployment, DB mutation, credentials change, or authority change.

## TRUTH BOUNDARY / UNCERTAINTY

This lesson is **CANDIDATE**, not ratified. The repair proves identity uniqueness on this branch; it does not claim that every historical/unmerged branch is collision-free.

## NEXT ACTION / SUCCESS CONDITION

Make identity uniqueness mechanically fail closed at capture/registration time, so a future Smart Note cannot publish with an already-owned human ID without an explicit reuse or renumber decision.
