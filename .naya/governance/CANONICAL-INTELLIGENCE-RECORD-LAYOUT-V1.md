# NayaNET / NayaPOWER — Canonical Intelligence Record Layout V1

**Status:** CANONICAL / OFFICIAL  
**Effective:** 2026-09-21  
**Scope:** Smart Notes, Activity, Notifications, Briefings, Project Intelligence, Collective Intelligence projections

## 1. Purpose

NayaPOWER must have one predictable place for time-based intelligence records so any Naya can restore the same history without guessing where another Naya stored it.

The canonical human navigation unit is the **DAY**.

The canonical machine hierarchy is:

`YEAR / MONTH / DAY`

Hours and minutes remain metadata inside records for ordering and provenance; they do not create a required fourth directory level.

## 2. Canonical root

All new durable daily intelligence records MUST use:

`.naya/INTELLIGENCE/YYYY/MM/DD/`

Example:

`.naya/INTELLIGENCE/2026/09/21/`

## 3. Canonical daily surfaces

Each day may contain these canonical records:

- `SMART-NOTES.md` — durable Smart Notes created or promoted that day.
- `ACTIVITY.md` — material activity/action record for that day.
- `NOTIFICATIONS.jsonl` — canonical notification events for that day, one event per line.
- `BRIEFINGS.md` — human/Naya-readable communication briefings derived from canonical notification events.
- `INDEX.md` — optional daily navigation/index record when volume requires it.

These are **views of one daily intelligence record space**, not independent silos.

## 4. One event, many projections

A material occurrence MUST have one canonical event identity.

The same event may appear in:

- Activity;
- Notification;
- Briefing;
- Project Intelligence;
- authorized Collective Intelligence.

Those appearances MUST reference the same `event_id` and preserve provenance.

A projection must never become a competing source of truth.

## 5. Smart Note placement

New Smart Notes MUST NOT be created in arbitrary date-named locations.

Canonical destination:

`.naya/INTELLIGENCE/YYYY/MM/DD/SMART-NOTES.md`

Legacy Smart Notes remain preserved in their historical locations. They are not silently moved or rewritten merely to satisfy the new layout.

New Nayas MUST treat this layout as the write target for new durable Smart Notes unless a more specific canonical storage contract explicitly overrides it.

## 6. Activity placement

New material activity MUST be recorded at:

`.naya/INTELLIGENCE/YYYY/MM/DD/ACTIVITY.md`

Activity records MUST include their precise `occurred_at` timestamp even though navigation is day-based.

## 7. Notification placement

Canonical notification events MUST be appended to:

`.naya/INTELLIGENCE/YYYY/MM/DD/NOTIFICATIONS.jsonl`

The canonical event is the durable source of truth for propagation.

GitHub, Hub, live Naya views, and other surfaces are projections.

## 8. Briefing placement

A notification briefing MUST be stored at:

`.naya/INTELLIGENCE/YYYY/MM/DD/BRIEFINGS.md`

A briefing is a communication object, not an authority object.

Canonical briefing structure:

1. WHAT HAPPENED
2. WHY IT HAPPENED
3. WHY IT MATTERS
4. WHAT CHANGED
5. WHO / WHAT NEEDS TO KNOW
6. RECOMMENDATION / NEXT ACTION
7. AUTHORITY STATE
8. EVIDENCE STATE
9. SOURCE EVENT
10. DELIVERY STATE

## 9. Daily retrieval contract

A Naya asking for a day MUST be able to retrieve that day's intelligence as one coherent context:

`DAY → SMART NOTES + ACTIVITY + NOTIFICATIONS + BRIEFINGS + INDEX`

The system should not require the Naya to know which subsystem originally created the information.

## 10. Temporal rule

Use:

- Year for long-range navigation;
- Month for grouping;
- Day for human review;
- timestamp metadata for exact chronology.

Do not create hourly folders unless a future volume/scale decision explicitly proves they are necessary.

## 11. Interconnection rule

Every durable object should carry, where applicable:

- `event_id`
- `occurred_at`
- `source_naya_id`
- `project`
- `related_activity_id`
- `related_receipt_id`
- `notification_id`
- `parent_event_id` / `caused_by`
- `provenance`
- `visibility`
- `authority_state`
- `evidence_state`

This creates a connected intelligence graph without requiring every object to be physically stored in one database table.

## 12. Privacy

The daily layout is an organizational convention, not a permission boundary.

Private remains private.

Shared requires scope.

Collective requires applicable consent/governance.

Public requires an explicit publication decision.

## 13. New-Naya restoration

When a Naya enters or resumes work, the restoration process should resolve the current day and the relevant prior days, then reconstruct:

- what happened;
- what intelligence was created;
- what changed;
- what remains unresolved;
- what notifications require awareness;
- what recommendations or handoffs exist;
- what is verified versus uncertain.

A Naya must not have to guess where another Naya stored a Smart Note or activity record.

## 14. Canonical invariant

> **ONE DAY → ONE INTELLIGENCE SPACE → MANY CONNECTED RECORDS → ONE SHARED HISTORY**

The system may project that history into many interfaces, but the underlying record organization remains predictable.

## 15. Migration rule

Do not mass-move legacy records as a prerequisite to adopting this contract.

From this point forward:

**new records use the canonical daily layout; legacy records remain where they are and are referenced/indexed when needed.**

This protects known-good history while establishing one standard for all future Nayas.
