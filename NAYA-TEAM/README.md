# NAYA-TEAM — Cross-Naya Continuity Superbrain

## Purpose

`NAYA-TEAM/` is the dedicated continuity and collaboration layer for all NIS/Naya instances working on NayaPOWER.

It is intentionally separate from project work, Smart Notes, and the machine runtime.

- **Activity Feed** records what happened.
- **Smart Notes** preserve what was learned.
- **Projects** contain project-specific work.
- **GOVERNANCE** defines authority, constraints, and required behavior.
- **NAYA-TEAM** preserves Naya-to-Naya continuity: identity, session/handoff context, decisions, messages, warnings, lessons, current work, and the exact successor action.
- **`.naya/`** remains the machine/runtime control and canonical machine-memory plane.

## Canonical calendar organization

Human-readable Naya-team records MUST use:

```text
NAYA-TEAM/
  YYYY/
    MM/
      DD/
        INDEX.md
        YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
```

The timestamp is UTC and is part of the filename. `TOPIC` is short, searchable, and filesystem-safe.

## Required handoff contract

Every substantive Naya-team record should identify:

1. Naya/NIS identity
2. Session
3. Parent / predecessor
4. What happened
5. Why it happened
6. What was learned
7. Decisions made
8. Current state
9. Known uncertainty / blockers
10. Evidence / Smart Links
11. What the successor must know
12. **Exactly ONE Next Action**
13. Successor / intended next Naya

## Operating law

`SIGN IN → ORIENT → WORK → RECORD → HAND OFF`

A handoff is not complete until the successor can locate the current day's index, understand the current state, identify the evidence, and execute the single next action without needing the predecessor's private chat transcript.

## Separation rule

NAYA-TEAM is not a second Smart Notes system and not a duplicate Activity Feed. It is the **continuity bridge between Nayas and across projects**.

Smart Notes may be referenced from NAYA-TEAM. Activity may be referenced from NAYA-TEAM. Neither is replaced by NAYA-TEAM.

## Cold-Naya rule

A fresh Naya must be able to enter the repository, find `NAYA-TEAM/YYYY/MM/DD/INDEX.md`, and recover enough context to continue safely from durable repository evidence alone.
