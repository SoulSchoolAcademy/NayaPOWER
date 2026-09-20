# Activity Feed — Living Feature Contract

**Feature ID:** `04-ACTIVITY-FEED`
**Parent:** Intelligent Hub / Superbrain
**Status:** CONTRACTED — implementation not started
**Version:** 1.0
**Date:** 2026-09-17

## 1. What is it?

The private continuity/activity lens for meaningful events occurring in the user's permitted Superbrain and project context.

## 2. Why does it exist?

To make work visible over time: what changed, what was done, what was discovered, what was verified, and what is next. Activity is continuity, not merely a log of clicks.

## 3. How does it work?

Meaningful project/system/intelligence events are recorded in the canonical event/activity substrate. The Activity Feed queries and presents those events in chronological/contextual form, filtered to the user's permitted scope. It must not create a competing event store.

## 4. Inputs and outputs

**Inputs:** canonical activity events, project context, timestamps, actor/source, status, evidence, relationships, privacy state.

**Outputs:** chronological activity items, project continuity, links to evidence/records, next-action context.

## 5. Connections

Every major Hub part may emit meaningful activity. Smart Notes, Personal Feed, Collective Feed, Reports, Smart Spaces, Smart List, and execution/governance systems can contribute events. Issue #151 remains the durable activity/continuity reference during the transition to in-product consumption.

## 6. Privacy, consent, and authority

Activity is private by default and permission-filtered. Events must preserve actor/source and scope correctly. Sensitive/private data must not leak through activity summaries or metadata.

## 7. What must be built?

- Canonical activity-event contract and adapters.
- Activity query/lens with permissions.
- Chronological/contextual presentation.
- Evidence and source links.
- Project/part filtering.
- State/next-action integration where appropriate.
- Persistence/idempotency tests.
- Desktop/mobile and accessibility verification.

## 8. Verification contract

Prove that meaningful events persist once, remain ordered/traceable, respect privacy, connect to evidence, and render from the canonical source. Verify production behavior independently.

## 9. Current state

Activity is architecturally defined and contracted. Existing canonical event/activity infrastructure exists elsewhere in Naya Power and must be inspected before adding Hub-specific implementation.

## 10. Evidence

Parent definition, Foundation Contract, and the established canonical activity/event architecture are the baseline. Issue #151 is the durable project activity reference.

## 11. Activity

See `ACTIVITY.md`.

## 12. Remaining work

Audit current canonical event/activity implementation and existing Hub activity references, then define the smallest verified Activity Feed vertical slice.

## 13. Next authorized action

Inspect the canonical event store and existing activity references, including Issue #151, and reconcile them with this contract.

## 14. Whole-system reconciliation

Activity is a lens over canonical continuity events. It must never become a parallel event database.
