# Cold-Start Intelligence Test — Machine Note

- Timestamp: 2026-08-30 (exact time unavailable)
- Category: LEARNING
- Status: ACTIVE
- Scope: TECHNICAL
- Keywords: cold start, NayaPOWER, machine intelligence, 9.1, evidence, Smart Note, PIS, Running Feed, receipts, compounding
- Aliases: machine-facing test record, cold-start machine learning event, Superbrain test event
- Related: `START-HERE.md`; `docs/NAYA-NOTES-MASTER-ACTIVATION-SPECIFICATION.md`; `MASTER-NOTES/PRIMARY-INTELLIGENCE-HUB.md`; Shawn Note sibling; Naya Note sibling

## Context

Machine-facing representation of the 2026-08-30 fresh-Naya cold-start intelligence test and the subsequent Smart Note delivery correction.

## What We Learned / Decided

Event type: `COLD_START_INTELLIGENCE_TEST`

Result: `SUCCESS`

Score: `9.1/10`

Material findings:

1. Cold-start restoration transferred operational understanding at a high level.
2. Evidence discipline was strong; the fresh Naya refused to claim runtime proof without a real checkout.
3. Fresh-Naya reasoning detected a causal gap in the existing A→B→C test fixture.
4. Explicit Smart Note delivery was previously incomplete because receipts and direct Smart Links were not returned.
5. Canonical Smart Note delivery must preserve one underlying intelligence event across Shawn, Naya, and Machine representations and provide direct artifact links.
6. PIS propagation is a distinct state transition and must never be inferred from note creation alone.

## Why It Matters

This event should be reusable as a regression target for both cold-start intelligence and Smart Note delivery integrity.

## Required Behavior

On explicit Smart Note request, execute the following contract:

`RECOGNIZE DURABLE VALUE → CREATE/UPDATE ONE CANONICAL INTELLIGENCE EVENT → CREATE ALIGNED SHAWN/NAYA/MACHINE REPRESENTATIONS → PERSIST → RETURN DIRECT SMART LINKS + EXACT RECEIPTS → TRIGGER/REQUEST PIS PROPAGATION WHEN APPLICABLE → UPDATE RUNNING FEED → VERIFY EACH STATE → REPORT ONLY EVIDENCED STATES`

The system must distinguish `NOTE_PERSISTED` from `PIS_PROPAGATED` and must not claim either without the appropriate receipt.

## Evidence / Source

Source event: Shawn's supplied 2026-08-30 fresh-chat cold-start test.

Canonical requirements: `docs/NAYA-NOTES-MASTER-ACTIVATION-SPECIFICATION.md`, `MASTER-NOTES/PRIMARY-INTELLIGENCE-HUB.md`, `START-HERE.md`.

## Follow-up

Use this machine note as a regression/acceptance target when implementing the automated Smart Note → PIS → Running Feed trigger path.
