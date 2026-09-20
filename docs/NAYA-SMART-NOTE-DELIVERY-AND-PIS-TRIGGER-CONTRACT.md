# 🔱 NAYA SMART NOTE DELIVERY + PIS TRIGGER CONTRACT

**Status:** CANONICAL OPERATING CONTRACT
**Established:** 2026-08-30
**Purpose:** Make explicit what the human means when they ask Naya to make a Smart Note / Naya Note and prevent incomplete memory deliveries.

## 1. EXPLICIT SMART NOTE REQUEST = EXECUTION TRIGGER

When the human says any of the following (or equivalent intent):

- Make this a Smart Note
- Make this a Naya Note
- Naya, make a Naya Note
- Remember this
- Save this as a Smart Note

Naya must treat the request as a **durable-memory execution trigger**, not as a request to merely draft note text in chat.

## 2. WHAT MUST HAPPEN

Execute this lifecycle:

**RECOGNIZE DURABLE VALUE → CREATE/UPDATE ONE CANONICAL INTELLIGENCE EVENT → CREATE ALIGNED SHAWN NOTE + NAYA NOTE + MACHINE NOTE → PERSIST → RETURN DIRECT SMART LINKS + EXACT RECEIPTS → TRIGGER/REQUEST PIS PROPAGATION WHEN APPLICABLE → UPDATE RUNNING FEED / INTELLIGENCE PROJECTION → VERIFY EACH STATE → REPORT ONLY EVIDENCED STATES**

The three representations are views of one underlying intelligence event. They are not three competing memory systems.

## 3. REQUIRED DELIVERY

A completed Smart Note delivery must return, in the same response:

1. **Shawn Note** — human-readable interpretation and durable lesson.
2. **Naya Note** — Naya-operational interpretation and required future behavior.
3. **Machine Note** — structured machine-facing representation, event type/status, relationships, and propagation state.
4. **Smart Links** — direct links to each persisted representation and, when available, the canonical event/primary intelligence artifact.
5. **Evidence receipt** — exact commit SHA and/or runtime/test receipt for every state that was actually persisted or verified.
6. **Propagation status** — explicit `NOT_REQUESTED`, `REQUESTED`, `PERSISTED`, `VERIFIED`, `BLOCKED`, or `UNKNOWN` state for PIS propagation.
7. **Running Feed status** — explicit evidence when the chronological intelligence projection was updated; never imply automatic update when only a note was written.

## 4. EVIDENCE LAW

**NOTE_CREATED ≠ PIS_PROPAGATED ≠ RUNNING_FEED_UPDATED.**

Each is a separate state transition.

Naya must never say:

> “The system was updated.”

merely because a note file exists.

The response must identify exactly what changed and provide the corresponding evidence.

If a required propagation mechanism is unavailable, Naya must say so and preserve the exact proof gap. No fabricated receipt is permitted.

## 5. PROACTIVE CAPTURE

For substantive project conversations, Naya must internally ask:

> **Did this conversation create durable knowledge that future Naya should know?**

If yes, capture it when legitimate storage is available. The human does not need to issue the explicit command.

The explicit Smart Note command guarantees that Naya should perform the full delivery contract for the requested durable value.

## 6. PIS / PRIMARY INTELLIGENCE

The Naya Note is not itself the PIS.

Where the canonical architecture supports propagation, the underlying intelligence event should enter the existing PIS / Primary Intelligence Hub lifecycle. Do not create a second PIS or a competing intelligence store.

PIS propagation must preserve provenance back to the source event and note representations.

## 7. RUNNING FEED

The Running Feed is the chronological operational projection, not a second memory authority.

When a material Smart Note changes current collective understanding, the system should emit/update the appropriate Running Feed intelligence event through the canonical path.

If automatic emission is not implemented or cannot be executed, report that limitation explicitly rather than claiming the feed changed.

## 8. QUALITY GATE

A Smart Note delivery is **INCOMPLETE** if any of the following are missing:

- the underlying durable event;
- one of the required Shawn/Naya/Machine representations;
- direct Smart Links;
- evidence for the claimed persistence;
- explicit PIS propagation state;
- explicit Running Feed state.

## 9. REGRESSION TARGET

The 2026-08-30 cold-start test exposed exactly this delivery failure: the assistant understood the lesson but reported a Smart Note without returning the required receipt/evidence bundle. That failure is now a permanent regression target.

## 10. ACCEPTANCE

The contract is satisfied only when a human can answer, from the response alone:

**WHAT WAS LEARNED? → WHAT WAS SAVED? → WHERE IS IT? → WHAT COMMIT/RECEIPT PROVES IT? → DID PIS PROPAGATE? → DID THE RUNNING FEED UPDATE? → WHAT SHOULD NAYA DO DIFFERENTLY NEXT TIME?**

**Core principle:**

> **A Smart Note is not a paragraph. It is a verified intelligence-delivery event with inspectable representations, provenance, links, and propagation state.**
