# Cold-Start Intelligence Test — Shawn Note

- Timestamp: 2026-08-30 (exact time unavailable)
- Category: LEARNING
- Status: ACTIVE
- Scope: PROJECT
- Keywords: cold start, NayaPOWER, intelligence test, scorecard, 9.1, continuity, operational understanding, fresh Naya, activation
- Aliases: cold-start test, fresh Naya test, NayaPOWER test, intelligence acceptance test
- Related: `START-HERE.md`; `docs/NAYA-NOTES-MASTER-ACTIVATION-SPECIFICATION.md`; `MASTER-NOTES/PRIMARY-INTELLIGENCE-HUB.md`; Naya Note sibling; Machine Note sibling

## Context

On 2026-08-30, a fresh Naya was given a cold-start intelligence test using the canonical NayaPOWER repository context. The purpose was to determine whether the system transfers operational understanding, evidence discipline, continuity, and executable next-action reasoning to a new Naya without conversational archaeology.

## What We Learned / Decided

The fresh Naya performed strongly and earned an overall cold-start intelligence score of **9.1/10**. She correctly identified NayaPOWER as the shared Superbrain, distinguished current repository truth from stale projections, respected the evidence ladder, classified execution-boundary failures without fabricating proof, preserved the human's authority over destination, and identified the remaining weakness in the existing A→B→C proof: part of B's improved action is manually authored by the fixture rather than independently selected by a fresh Naya.

The test was successful as an orientation/intelligence test, but it also exposed a system weakness: a Smart Note request was not delivered with the complete evidence package (Shawn Note + Naya Note + Machine Note + direct Smart Links) and the system update/propagation receipt was not returned to the human.

## Why It Matters

The test demonstrates that NayaPOWER is transferring meaningful operational understanding, not merely document names. The failure in the surrounding Smart Note delivery is equally important because a claim of durable learning without inspectable receipts is not sufficient for a trusted Superbrain.

## Required Behavior

When Shawn explicitly asks to make a Smart Note/Naya Note, Naya must treat that as a durable-memory execution request: capture the material learning, create the aligned Shawn, Naya, and Machine representations from one underlying intelligence event, persist them through the canonical memory path, return direct Smart Links and exact commit/evidence receipts, and update the canonical intelligence/Running Feed path when propagation is applicable. Naya must never claim the save or propagation without evidence.

## Evidence / Source

Source conversation: 2026-08-30 cold-start intelligence test supplied by Shawn.

Canonical system requirements are defined in `START-HERE.md` and `docs/NAYA-NOTES-MASTER-ACTIVATION-SPECIFICATION.md`; the Primary Intelligence Hub explicitly states that **SMART NOTE = SHAWN NOTE + NAYA NOTE + MACHINE NOTE + SMART LINKS** and that PIS propagation is a separate state transition requiring separate evidence.

## Follow-up

Make the Smart Note delivery contract operational and testable so the next explicit Smart Note request automatically produces the complete evidence bundle.
