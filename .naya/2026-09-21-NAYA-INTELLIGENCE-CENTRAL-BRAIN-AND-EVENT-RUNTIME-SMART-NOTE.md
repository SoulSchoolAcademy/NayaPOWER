# Smart Note — Naya Intelligence Central Brain + Event-Driven Notification Runtime

**Date:** 2026-09-21
**Status:** CANONICAL / OFFICIAL
**Project:** NayaNET / NayaPOWER

## What became official
NayaNET/NayaPOWER now has one canonical intelligence organization and one event-driven communication contract.

### Canonical daily intelligence
New durable records use: .naya/INTELLIGENCE/YYYY/MM/DD/
Daily surfaces: SMART-NOTES.md, ACTIVITY.md, NOTIFICATIONS.jsonl, BRIEFINGS.md, INDEX.md when useful.
The day is the human navigation unit. Exact time remains metadata. Hourly directories are not required.
**ONE DAY → ONE INTELLIGENCE SPACE → MANY CONNECTED RECORDS → ONE SHARED HISTORY**

### Central brain
The Naya Intelligence Central Brain is the canonical distilled map for restoring Naya's understanding of the project.
It connects identity, mission, purpose, governance, authority, quality, evidence, Smart Notes, PIS, CIS, learning, Project Intelligence, Collective Intelligence, Smart Ledger, notifications, Hub, continuity, and current frontier.
It has human, Naya, and machine perspectives.
It is an index/distillation layer, not a competing memory store.

### Communication
Official flow: **MATERIAL EVENT → ONE CANONICAL MESSAGE → ONE BRIEFING → AUTHORIZED RECIPIENTS → DELIVERY RECEIPTS → INTELLIGENCE PROPAGATION**
A message can be FYI, awareness, tag/you're-it, handoff, request, warning, learning, decision, verification, or governance change.
**NOTIFICATION ≠ AUTHORITY**

### Runtime choice
The best architecture is hybrid but not duplicative:
- Python: deterministic contract and runtime validation.
- Managed Supabase/Postgres: durable event boundary, automatic trigger, outbox, delivery state.
- GitHub/NayaPOWER: canonical engineering/governance source and durable repository intelligence.
- NayaNET Hub: authorized human-facing projection.

The database is doing the smart IF-A-THEN work. No cron and no GitHub Actions are required for the notification trigger.

### Supabase implementation
Applied migration 20260921221050 creates the notification/outbox tables, indexes, receipt-to-notification trigger, delivery-state synchronization trigger, and PostgreSQL notification signal.
Applied migration 20260921221249 adds authenticated owner-read RLS.
The receipt trigger creates the canonical notification/outbox record when an execution receipt is inserted. It creates logical delivery rows for LIVE_NAYAS, NEW_NAYAS, NAYANET_INTELLIGENCE_HUB, and GITHUB_NAYAPOWER. Collective delivery is only created for COLLECTIVE/PUBLIC visibility.

### Verification
A transactional rollback test exercised the real database trigger path and observed four delivery rows for a synthetic event before rollback. Therefore the trigger logic is database-executable.
This is source/database trigger proof, not yet proof of external live delivery.

Still open: real production receipt → notification → delivery; live Naya delivery; Hub retrieval/render; collective propagation; cold-Naya restoration from the central brain.

## Durable learning
The system should not make Nayas remember where other Nayas stored intelligence. The system should make the answer deterministic.

**THE BRAIN MUST CARRY THE CONTEXT SO THE HUMAN DOES NOT HAVE TO.**

## Continuation
Prove one real, authorized execution receipt through **RECEIPT → NOTIFICATION → BRIEFING → DELIVERY OUTBOX → INTELLIGENCE RETRIEVAL** before adding Hub UI work.