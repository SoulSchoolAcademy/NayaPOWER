# Smart Notes — Living Feature Contract

**Feature ID:** `01-SMART-NOTES`
**Parent:** Intelligent Hub / Superbrain
**Status:** ACTIVE PROJECTION CONTRACT — SMART NOTE / INTELLIGENT BLOCK V1
**Version:** 1.1
**Date:** 2026-09-17

> **Current authority:** `.naya/SMART-NOTE-CONTRACT-V1.md`. Smart Note = Intelligent Block. This Hub feature is a projection/interaction surface over that canonical object.

## 1. What is it?

Smart Notes are durable, structured intelligence records. They capture meaningful human input, Naya interpretation, evidence, lessons, decisions, actions, or other knowledge in a form the Superbrain can retrieve, connect, compound, share by consent, and report on.

## 2. Why does it exist?

To prevent valuable intelligence from disappearing in chat, memory, or disconnected documents. A Smart Note turns a meaningful moment into durable intelligence with provenance and future utility.

## 3. How does it work?

A note begins with a meaningful source/input, is interpreted and structured, receives the appropriate evidence/context, is stored as a canonical intelligence record/event where applicable, and becomes available to authorized downstream surfaces such as Personal Feed, Reports, Library, Connections, and Collective Feed after consent.

The canonical Smart Note artifact is stored at `.naya/memory/notes/YYYY/MM/DD/` through the shared resolver. The event ledger and runtime persistence preserve the same event identity and provenance; Hub, Feed, Reports, Library, Learning, and Dream are downstream projections/uses. CIS and PIS are downstream projections and must not become competing stores of truth.

## 4. Inputs and outputs

**Inputs:** human note/request, Naya-generated note, machine evidence, context, relationships, privacy/consent state.

**Outputs:** durable Smart Note; relationships; feed/report/library visibility; optional authorized share/action.

**Canonical alignment:** reuse the IntelligentEvent model and source boundaries defined by the Hub Foundation Contract.

## 5. Connections

Personal Intelligence Feed displays permitted notes. Collective Intelligence Feed consumes only intentionally shared knowledge. Activity records creation/change events. Reports summarize notes. Library retrieves them. Connections relates them. Smart Share controls movement across privacy boundaries.

## 6. Privacy, consent, and authority

Default ownership is private. Sharing is explicit. Collective publication requires consent and must obey identity/source treatment. Any external action derived from a note remains subject to Naya Power authority and execution governance.

Canonical Smart Note projections now encode `visibility=private` and `consent_state=not_granted` until an explicit consent transition exists.

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

The current implementation slice has source-level reconciliation and an isolated end-to-end verifier for the four hard gates, but production/live verification remains open.

## 9. Current state

The existing Smart Note transaction path has been reconciled rather than rebuilt. Authoritative persistence is read back before downstream projection; canonical PIS events preserve the Smart Note timestamp and source provenance; canonical Smart Note privacy defaults to private/not-granted.

## 10. Evidence

Parent architecture: `../INTELLIGENT-HUB-SUPERBRAIN-PROJECT.md`

Foundation architecture: `../../FOUNDATION-CONTRACT.md`

Runtime transaction: `.naya/runtime/smart_note_transaction.py`

PIS projection: `scripts/build-smart-feed-projection.py`

Verification: `scripts/verify-smart-note-transaction.py`

## 11. Activity

See `ACTIVITY.md` and `STATE.md`.

## 12. Remaining work

Run the updated verifier, independently verify the live Hub consumption path, then complete the remaining lifecycle and downstream adapters without creating a second source of truth.

## 13. Next authorized action

Run the updated Smart Note transaction verifier and inspect the proof before making another code change.

## 14. Whole-system reconciliation

Smart Notes are a source of intelligence, not a separate feed or database. All downstream surfaces must consume the canonical representation.


## 15. Canonical structure

Every created Smart Note follows the V1 human-readable order:

```text
IN A NUTSHELL
HUMAN NOTE
CHILD NOTE
GRANDMA NOTE
NAYA NOTE
MACHINE NOTE
LEARNING LESSON
WHAT IT MEANS
HOW IT CONNECTS
HOW TO APPLY IT
WHAT'S IN IT FOR THEM / YOU / US
EVIDENCE / SMART LINKS
CURRENT STATE
ONE NEXT ACTION
```

The machine object conforms to `NAYANET_INTELLIGENT_BLOCK_V1`. The Hub may progressively disclose these perspectives, but it does not create a second Smart Note structure.
