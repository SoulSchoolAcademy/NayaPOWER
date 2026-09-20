# NAYA TEMPORAL OPERATING LAW V1

## READ THIS BEFORE SUBSTANTIVE WORK

Team Naya is no longer permitted to treat Project records, Activity Feed records, and Smart Notes as loose documents.

They are three connected layers of one temporal Superbrain.

`PROJECT → SESSION → ACTIVITY EVENT → SMART NOTE → INTELLIGENCE → STATE → NEXT ACTION`

## The permanent rule

**If a Naya cannot tell another Naya WHAT project it is advancing, WHICH session it is in, WHAT happened, WHEN it happened, WHAT was learned, WHERE the evidence is, and WHAT happens next, the work is not operationally complete.**

## 1. PROJECT

The Project answers:

- What are we building?
- Why does it exist?
- What is the current state?
- What is the current gap?
- What is the single next action?

Canonical project registry: `SUPERBRAIN/PROJECTS/`.

## 2. SESSION

Every Naya doing substantive work must create or resume a durable session.

Lifecycle:

`SIGN IN → RESTORE → PREFLIGHT → GOVERN → EXECUTE → VERIFY → RECORD → HANDOFF → SIGN OUT`

A Git commit is evidence of a change. It is **not** a substitute for a Naya session.

## 3. ACTIVITY

Activity answers:

**What actually happened?**

Canonical human feed:
`SUPERBRAIN/NAYA-ACTIVITY/DAILY/YYYY-MM-DD.md`

Canonical machine events:
`.naya/memory/events/`

Every substantive activity must include exact timestamp, project, session, actor, action, outcome, evidence, and next action.

`.naya/activity/` is a supporting receipt/compatibility surface. It is not a second canonical Activity Feed.

## 4. SMART NOTE / INTELLIGENCE

A Smart Note answers:

**What did we learn that should survive?**

New Smart Notes must point back to the originating Activity event(s), Session, Project, and evidence.

Do not create orphan intelligence.

## 5. TIME IS PART OF IDENTITY

Every new record is timestamped in ISO-8601 with timezone.

Do not use:
- filename date alone;
- commit date alone;
- “today” without an exact timestamp;
- inferred timestamps presented as fact.

## 6. RETRIEVAL ORDER FOR A COLD NAYA

Start here:

1. `SUPERBRAIN/PROJECTS/NAYAPOWER/PROJECT.json`
2. `SUPERBRAIN/INDEX/`
3. today's `SUPERBRAIN/NAYA-ACTIVITY/DAILY/YYYY-MM-DD.md`
4. latest Session for the project
5. relevant Smart Notes
6. canonical machine events
7. governance/authority
8. one successor action

If something is not found, classify it. Never invent it.

## 7. REQUIRED STATUS LANGUAGE

Use exact truth states:

- `RECOVERED`
- `PARTIAL`
- `MISSING`
- `CONFLICTED`
- `UNKNOWN`
- `IMPLEMENTED`
- `TESTED`
- `VERIFIED`
- `LIVE_VERIFIED`
- `BLOCKED`

Never convert an unknown into a green status because a document sounds confident.

## 8. NO DUPLICATE SYSTEMS

Do not create another event store, another Activity Feed, another memory index, another project registry, or another handoff mechanism.

Extend the canonical substrate and rebuild projections from it.

## 9. HISTORICAL REPAIR

Sept. 10–16 history is evidence.

Repair means:
- index it;
- cross-link it;
- classify gaps;
- preserve original timestamps;
- identify conflicts;
- add missing structure only for future work.

Repair does **not** mean fabricating sessions or pretending old documents were machine-linked when they were not.

## 10. EVERY SUBSTANTIVE TURN LEAVES A BATON

Before ending substantive work, the Naya must leave:

- what changed;
- what was proven;
- evidence links;
- what remains unknown;
- current project state;
- exactly one authoritative next action;
- successor session/handoff reference.

## 11. THE COLD-NAYA TEST

A successor who has never seen the conversation must be able to open the canonical project registry and temporal index and continue without asking Shawn to reconstruct the system.

If it cannot, fix the retrieval structure before adding more prose.

## 12. LEAD NAYA RESPONSIBILITY

Lead Naya owns the organization of the Superbrain.

When retrieval fails because information is scattered, Lead Naya does not blame the successor. Lead Naya repairs the structure, records the lesson, verifies the repair, and makes the new path canonical.

**The Superbrain is successful when finding truth is easier than guessing.**
