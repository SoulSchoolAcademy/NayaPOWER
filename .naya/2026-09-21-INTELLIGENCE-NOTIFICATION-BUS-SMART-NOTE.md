# Intelligence Notification Bus — Smart Note

**Date:** 2026-09-21

## New intelligence

NayaPOWER must treat material intelligence/activity as a live awareness event, not merely a stored record.

When a Naya enters, creates intelligence, records material activity, triggers an action, completes/blocks/fails an action, changes governance, or creates a handoff, the event must propagate to the required NayaPOWER and NayaNET awareness surfaces.

## Architectural lesson

The canonical event is the source of truth. GitHub and the Intelligence Hub are projections. A new Naya must receive relevant current notifications during context restoration.

## Human value

The system should feel continuously alive and coordinated without producing noise. Every notification should answer:

**What happened? Why does it matter? What changed? Who needs to know? What happens next?**

## Next

Implement the event bus and delivery receipts, then connect GitHub notifications and Intelligence Hub rendering to the same canonical event stream.
