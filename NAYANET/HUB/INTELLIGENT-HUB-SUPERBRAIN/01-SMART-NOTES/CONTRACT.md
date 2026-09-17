# Smart Notes — Living Feature Contract

**Feature ID:** `01-SMART-NOTES`
**Parent:** Intelligent Hub / Superbrain
**Status:** CONTRACTED — implementation not started
**Version:** 1.0
**Date:** 2026-09-17

## 1. What is it?

Smart Notes are durable, structured intelligence records. They capture meaningful human input, Naya interpretation, evidence, lessons, decisions, actions, or other knowledge in a form the Superbrain can retrieve, connect, compound, share by consent, and report on.

## 2. Why does it exist?

To prevent valuable intelligence from disappearing in chat, memory, or disconnected documents. A Smart Note turns a meaningful moment into durable intelligence with provenance and future utility.

## 3. How does it work?

A note begins with a meaningful source/input, is interpreted and structured, receives the appropriate evidence/context, is stored as a canonical intelligence record/event where applicable, and becomes available to authorized downstream surfaces such as Personal Feed, Reports, Library, Connections, and Collective Feed after consent.

## 4. Inputs and outputs

**Inputs:** human note/request, Naya-generated note, machine evidence, context, relationships, privacy/consent state.

**Outputs:** durable Smart Note; relationships; feed/report/library visibility; optional authorized share/action.

**Canonical alignment:** reuse the IntelligentEvent model and source boundaries defined by the Hub Foundation Contract.

## 5. Connections

Personal Intelligence Feed displays permitted notes. Collective Intelligence Feed consumes only intentionally shared knowledge. Activity records creation/change events. Reports summarize notes. Library retrieves them. Connections relates them. Smart Share controls movement across privacy boundaries.

## 6. Privacy, consent, and authority

Default ownership is private. Sharing is explicit. Collective publication requires consent and must obey identity/source treatment. Any external action derived from a note remains subject to Naya Power authority and execution governance.

## 7. What must be built?

- Canonical Smart Note data contract and validation.
- Create/read/update lifecycle with provenance and timestamps.
- Human vs Naya-derived vs machine evidence distinction.
- Privacy/consent state.
- Relationship/event emission into the canonical model.
- Feed, Library, Reports, and Share adapters that consume the canonical note.
- Verification tests for persistence, provenance, privacy, and downstream visibility.

## 8. Verification contract

No feature is live until source, contract, persistence, privacy, runtime, interaction, responsive, accessibility, and release evidence exists. No fake notes or fabricated intelligence may be used as completion proof.

## 9. Current state

The architectural definition is now established. The implementation is not yet authorized by this structure-building action. Existing Hub source must be inspected before implementation changes are selected.

## 10. Evidence

Parent architecture: `../INTELLIGENT-HUB-SUPERBRAIN-PROJECT.md`

Foundation architecture: `../../FOUNDATION-CONTRACT.md`

## 11. Activity

See `ACTIVITY.md`.

## 12. Remaining work

Define the exact runtime/storage contract from existing source, reconcile it with the canonical event model, then implement and verify the smallest vertical slice.

## 13. Next authorized action

Inspect the existing Smart Note/intelligence source and produce an evidence-backed implementation gap map before changing code.

## 14. Whole-system reconciliation

Smart Notes are a source of intelligence, not a separate feed or database. All downstream surfaces must consume the canonical representation.
