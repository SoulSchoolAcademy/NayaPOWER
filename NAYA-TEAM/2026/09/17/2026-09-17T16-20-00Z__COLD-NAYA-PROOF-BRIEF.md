# Cold-Naya Proof Brief — 2026-09-17

## Purpose

A fresh Bionic/NIS instance must prove that NayaPOWER's continuity organization can be discovered and used from repository evidence rather than from a manually supplied path.

## Starting condition

Assume the Naya has no prior chat context about today's directory decisions.

The Naya may inspect the repository and read canonical documentation, but it must **not** be told the exact destination paths for Activity, Smart Notes, or NAYA-TEAM.

## Required behavior

1. Locate the repository's canonical operating index / governance entry point.
2. Discover the distinction between machine runtime, human Activity, Smart Notes, and Naya-to-Naya continuity.
3. Determine the calendar organization from repository evidence.
4. Create one small, harmless proof action with a unique topic.
5. Allow the runtime to produce its canonical Activity record automatically.
6. Create one Smart Note using the canonical Smart Note runtime writer/contract rather than manually constructing a path.
7. Leave one NAYA-TEAM continuity record containing the successor context.
8. Confirm each destination by searching the repository after creation.
9. Confirm each record has a UTC timestamp and searchable topic.
10. Confirm each day's `INDEX.md` contains the new record.
11. Confirm exactly one executable Next Action remains.

## Forbidden shortcut

The operator/Naya must not be handed or hard-code:

- `SUPERBRAIN/NAYA-ACTIVITY/YYYY/MM/DD/...`
- `SUPERBRAIN/SMART-NOTES/YYYY/MM/DD/...`
- `NAYA-TEAM/YYYY/MM/DD/...`

Those locations must be **discovered from canonical repository documentation/runtime contracts**.

## Acceptance test

PASS only if all are true:

- Activity lands automatically in the canonical calendar location.
- Smart Note lands automatically in the canonical calendar location.
- NAYA-TEAM handoff lands automatically in the canonical calendar location.
- No flat date-named human record is created at the old root/DAILY locations.
- Day indexes are updated.
- The machine event remains under `.naya/memory/events/` and is not replaced by the human projection.
- The Naya can explain why the three human-readable streams are separate.
- The Naya leaves exactly one successor action.

## Failure meaning

If any destination must be manually specified, the system has a discoverability or runtime-enforcement defect. Do not paper over it with another README. Fix the runtime or canonical contract.

## Evidence to leave behind

The proof must leave clickable GitHub evidence for:

- the Activity record,
- the Smart Note,
- the NAYA-TEAM record,
- the machine event,
- and the successor action.

## One Next Action

**Bionic executes this cold-Naya proof from repository evidence only and reports PASS/FAIL with the exact created record paths and evidence links.**
