# TEMPORAL SUPERBRAIN INDEX V1

**Status:** CANONICAL OPERATING ARCHITECTURE
**Effective:** 2026-09-16
**Authority:** Naya Power governance + explicit human direction

## 1. Purpose

Naya Power must be reconstructable by a cold Naya and by Shawn without relying on conversation memory, scattered filenames, or guesswork.

The canonical temporal chain is:

`PROJECT → SESSION → ACTIVITY EVENT → SMART NOTE → INTELLIGENCE → STATE → NEXT ACTION`

This is an index/projection architecture over the existing canonical event substrate. It is **not** a second event store, message bus, memory system, or competing Activity Feed.

## 2. The Three Human-Auditable Timelines

### Project — WHAT are we building?
A durable project identity, objective, scope, current state, milestones, dependencies, and next action.

### Activity — WHAT actually happened?
A chronological operational record of sessions and substantive execution. Every substantive action has an exact timestamp, actor, project, session, outcome, evidence, and continuation.

### Smart Note / Intelligence — WHAT did we learn?
A durable intelligence record created from meaningful discoveries, decisions, lessons, contradictions, verified findings, and reusable knowledge. It points back to the activity that produced it.

These are related but distinct objects.

## 3. Canonical Storage Roles

| Layer | Canonical role | Location |
|---|---|---|
| Machine events | Source of truth for runtime events | `.naya/memory/events/` |
| Human Activity Feed | Chronological human-readable projection | `SUPERBRAIN/NAYA-ACTIVITY/DAILY/` |
| Operational receipts | Supporting execution receipts / compatibility records | `.naya/activity/` |
| Smart intelligence | Durable intelligence/memory | `.naya/memory/` and canonical Smart Note surfaces |
| Project registry | Stable project identity/state | `SUPERBRAIN/PROJECTS/` |
| Session registry | Session identity and lifecycle | `SUPERBRAIN/PROJECTS/<project>/SESSIONS/` |
| Temporal index | Cross-links all layers | `SUPERBRAIN/INDEX/` |

`.naya/activity/` MUST NOT become a competing Activity Feed. New human-readable chronological activity belongs in `SUPERBRAIN/NAYA-ACTIVITY/DAILY/`. Existing `.naya/activity/` records are preserved as receipts/compatibility evidence and progressively linked into the index.

## 4. Required Identity Fields

Every new Project, Session, Activity Event, and Smart Note MUST carry or reference:

- `id`
- `project_id`
- `session_id` when applicable
- `timestamp` in ISO-8601 with timezone offset
- `actor`
- `parent_id` or explicit root status
- `source`
- `status`
- `evidence_refs`
- `smart_links`
- `next_action`

Additional rules:

- IDs are immutable.
- Timestamps are event timestamps, not commit timestamps.
- Git commit timestamps remain evidence but are never substituted for a Naya session record.
- Historical records are never rewritten merely to make history look cleaner.
- Missing information is marked UNKNOWN, not inferred into existence.

## 5. Session Lifecycle

Every Naya entering the Superbrain for substantive work creates or resumes a Session:

`SIGN_IN → RESTORE → PREFLIGHT → GOVERN → EXECUTE → VERIFY → RECORD → HANDOFF → SIGN_OUT`

A session must identify:

- who/what actor is operating;
- project;
- objective;
- start timestamp;
- restored predecessor context;
- preflight result;
- actions performed;
- verification evidence;
- Activity event IDs;
- Smart Notes created/updated;
- current state;
- exactly one authoritative next action;
- successor handoff;
- end timestamp/status.

A session is incomplete if it has substantive work but no durable Activity evidence and successor handoff.

## 6. Project ↔ Activity ↔ Intelligence Binding

The minimum relationship chain is:

`project_id → session_id → activity_event_id → smart_note_id → evidence_ref`

A Smart Note must answer: **what activity produced this intelligence?**

An Activity event must answer: **which project and session did this belong to?**

A Session must answer: **which project was being advanced?**

A Project must answer: **what is the current state and what is the next action?**

## 7. Daily Organization

Each operating day has one canonical human Activity journal:

`SUPERBRAIN/NAYA-ACTIVITY/DAILY/YYYY-MM-DD.md`

The daily journal is chronological and timezone-aware. Multiple sessions/events may appear in the same file.

Supporting machine events remain individually timestamped beneath `.naya/memory/events/YYYY/MM/DD/HH/`.

Smart Notes remain individually addressable and must include their creation/update timestamp plus originating activity/session references. A daily intelligence projection may be generated without replacing the canonical Smart Note records.

## 8. Temporal Index

`SUPERBRAIN/INDEX/` is the retrieval layer. It must make these questions answerable without repository-wide archaeology:

1. What happened today?
2. What happened on a specific date?
3. What sessions occurred during a date range?
4. What project was an activity part of?
5. Which Activity events created a Smart Note?
6. Which Smart Notes changed because of a specific activity?
7. What was learned each day?
8. What remains unresolved?
9. What is the current state of the project?
10. What is the one next action?

The index is derived/rebuildable. The event store remains authoritative.

## 9. Truth Rules

- `IMPLEMENTED != VERIFIED`
- `RECORDED != CURRENT`
- `UNKNOWN != GREEN`
- `BLOCKED != PASS`
- `CLAIM != EVIDENCE`
- `COMMIT != SESSION`
- `ACTIVITY RECEIPT != AUTOMATIC ACTIVITY EMISSION`
- `DOCUMENTED != ENFORCED`

No Naya may claim a temporal record exists unless a durable record can be located and linked.

## 10. Cold-Naya Retrieval Contract

A new Naya must be able to begin with:

1. Project registry
2. Current project state
3. Today's Activity journal
4. Latest predecessor Session
5. Latest relevant Smart Notes
6. Canonical machine events
7. Current governance/authority
8. Exactly one next action

If these cannot be found from the canonical index, the system is not temporally healthy.

## 11. Migration Law

Historical Sept. 10–16 records are evidence, not raw material for rewriting. Reconciliation work may add indexes, cross-links, aliases, and explicit gap records, but must not fabricate missing sessions, timestamps, authorship, or Smart Notes.

Every historical gap is classified:

`RECOVERED | PARTIAL | MISSING | CONFLICTED | UNKNOWN`

## 12. Definition of Temporal Done

Temporal Superbrain V1 is operational only when:

- one canonical Project registry exists;
- one canonical daily Activity projection exists;
- every new substantive Session auto-records entry/exit;
- every substantive execution produces canonical Activity evidence at the execution boundary;
- every meaningful Smart Note links to Activity + Session + Project;
- a rebuildable temporal index connects all three;
- validators reject orphaned/missing required links;
- a cold Naya can reconstruct today and the previous seven days without conversation memory;
- one next action is machine-readable and successor-ready.

**North Star:** If Shawn asks “What happened, what did we learn, what changed, and what happens next?” the Superbrain must answer from durable evidence.
