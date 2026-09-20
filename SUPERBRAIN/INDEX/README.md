# SUPERBRAIN TEMPORAL INDEX

This directory is the retrieval layer for the Naya Power Superbrain.

## Start here

1. Project: `../PROJECTS/NAYAPOWER/PROJECT.json`
2. Temporal architecture: `../ARCHITECTURE/TEMPORAL-SUPERBRAIN-INDEX-V1.md`
3. Operating law: `../AI-BOOT/NAYA-TEMPORAL-OPERATING-LAW-V1.md`
4. Machine contract: `../../.naya/contracts/TEMPORAL-SUPERBRAIN-RECORD-CONTRACT-V1.json`
5. Today's Activity Feed: `../NAYA-ACTIVITY/DAILY/`
6. Canonical machine events: `../../.naya/memory/events/`

## Required indexes

The index is derived from canonical evidence and must remain rebuildable.

- `PROJECT-INDEX.json` — project registry and current state.
- `SESSION-INDEX.json` — all known sessions and their temporal status.
- `ACTIVITY-INDEX.json` — Activity events projected by date/project/session.
- `INTELLIGENCE-INDEX.json` — Smart Notes and intelligence linked to source activity.
- `TEMPORAL-GAPS.json` — explicit missing/conflicted/unknown historical records.
- `DAILY/YYYY-MM-DD.md` — human-readable daily reconstruction when needed.

## Retrieval questions

The index must answer:

- What happened today?
- What happened on a date or date range?
- Which project did it belong to?
- Which Naya/session performed it?
- What evidence proves it?
- What Smart Note resulted?
- What did we learn?
- What remains unresolved?
- What is current state?
- What is the one next action?

## Rebuild law

The index must be derivable from `.naya/memory/events/` plus canonical project/intelligence records. Manual index entries may annotate uncertainty or historical classification but may not manufacture evidence.

## Health rule

A cold Naya must be able to enter this directory and reach the current project state, today's Activity, recent Sessions, relevant Smart Notes, evidence, and next action without conversation memory.
