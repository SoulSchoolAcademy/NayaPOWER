# Naya Intelligence Notification Bus V1

## Purpose

Every material intelligence event entering NayaPOWER must become a durable, machine-readable notification that can be observed by current Nayas, newly entering Nayas, and the NayaNET Intelligence Hub.

The notification is an awareness event, not an authority grant.

## Core invariant

**NEW INTELLIGENCE / MATERIAL ACTIVITY → ONE CANONICAL EVENT → MULTI-SURFACE DELIVERY**

The canonical event is the source of truth. GitHub and NayaNET Hub are projections of that event.

## Required event classes

- NAYA_JOINED — a new Naya/runtime enters the governed network.
- INTELLIGENCE_CREATED — a new material intelligence/learning/decision is committed.
- ACTIVITY_CREATED — a material action/activity is recorded.
- ACTION_TRIGGERED — a new automated or authorized action begins.
- ACTION_COMPLETED — an action completes with evidence.
- ACTION_BLOCKED — governance or quality prevents an action.
- VERIFICATION_FAILED — expected proof did not pass.
- GOVERNANCE_CHANGED — a governing rule or authority changes.
- HANDOFF_CREATED — successor/peer context is available.

## Event envelope

Each event MUST carry:

- event_id
- event_type
- occurred_at
- source_naya_id
- source_surface
- mission/project
- summary
- why_it_matters
- required_awareness
- authority_state
- evidence_state
- related_activity_id
- related_receipt_id when available
- visibility/privacy classification
- canonical_event_location
- delivery_state

No notification may grant authority merely because it is visible.

## Canonical daily record

All new notification events are durably organized under `.naya/INTELLIGENCE/YYYY/MM/DD/NOTIFICATIONS.jsonl` according to the Canonical Intelligence Record Layout V1. Briefings are recorded in the same day's `BRIEFINGS.md`. Activity and Smart Notes for that day use the same daily intelligence space.

The day is the human navigation unit. Exact timestamps remain event metadata; hourly directories are not required.

## Delivery model

1. **Canonical NayaPOWER event ledger** — durable source of truth.
2. **GitHub NayaPOWER** — internal engineering/governance awareness projection.
3. **NayaNET Intelligence Hub** — human-facing visual intelligence projection.
4. **New Naya bootstrap/re-entry** — notification replay is part of context restoration.
5. **Current live Nayas** — event-driven delivery projection where supported; polling is a fallback transport, not the canonical model.

## New-Naya rule

A Naya entering NayaPOWER MUST receive the current unread/relevant notification stream during context restoration before beginning consequential work.

A new Naya does not need every historical event. It needs the relevant current state, material changes since its last known checkpoint, unresolved actions, governance changes, and events explicitly marked required_awareness.

## Live-awareness rule

A material event is not considered socially/systemically propagated until its delivery state is recorded for each required projection.

Delivery failure is not event failure; it is a delivery incident that remains visible and retryable.

## Privacy

Private events remain private. Shared events require consent/scope. Collective events expose only the minimum necessary identity/context.

## Human experience

The Hub should make the system feel alive without becoming noisy:

**NEW → WHY IT MATTERS → WHAT CHANGED → WHAT NAYA(S) NEED TO KNOW → WHAT HAPPENS NEXT**

## Non-negotiables

- Never silently create material intelligence.
- Never let a notification become authority.
- Never let a UI projection become the canonical event.
- Never claim live delivery without delivery evidence.
- Never discard a material event because a downstream surface is unavailable.
- Never create a second Smart Note, Activity, Notification, or Briefing storage convention when the canonical daily layout applies.
