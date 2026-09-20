# Smart Note Runtime Operating Protocol

**Constitutional authority:** `SMART_NOTE_CONSTITUTION.md`  
**Status:** MANDATORY IMPLEMENTATION CONTRACT  
**Effective:** 2026-09-07 revision

## Purpose

This protocol translates the Smart Note Constitution into an executable operating contract for every Naya Power implementation.

## Trigger

A Smart Note operation begins whenever the user asks Naya to capture, remember, save, note, or make a Smart Note about referenced subject matter. Equivalent natural-language requests are operational commands, not requests for documentation about the Smart Note system.

## Mandatory subject resolution

Before writing anything, the runtime must resolve:

- `subject`
- `source_context`
- `event_type`
- `user/member identity`
- `privacy_state`

The `subject` is the intelligence being captured. The default subject is never "Smart Notes" merely because the operation is a Smart Note.

## One canonical event / Intelligent Block

One operation creates **one canonical Smart Note event / Intelligent Block**.

The Intelligent Block has six semantic perspectives:

1. **Human Note** — what the human discovered, experienced, decided, learned, identified, or wants preserved.
2. **Naya Note** — Naya's synthesis, meaning, implications, relationships, and reusable learning.
3. **Machine Note** — structured identity, event linkage, provenance, privacy, timestamp, classification, state, and machine-readable representation.
4. **Child Note** — the simplest accurate explanation.
5. **Grammar Note** — the cleanest formulation of the underlying lesson/principle.
6. **Nutshell** — the shortest useful expression.

These are perspectives of one event, not six disconnected notes.

## Required transaction artifacts

The transaction boundary has four required logical/persistence artifacts:

```text
smart_note_event / Intelligent Block
├── human_note
├── naya_note
├── machine_note
└── intelligence_feed_note
```

The Child, Grammar, and Nutshell perspectives are mandatory semantic fields/projections of the same Intelligent Block. They do not create duplicate event identities.

Each artifact/perspective must resolve to the same canonical event identity.

## Canonical execution chain

```text
REQUEST
→ IDENTIFY SUBJECT
→ EXTRACT INTELLIGENCE
→ BUILD ONE INTELLIGENT BLOCK
→ CREATE HUMAN + NAYA + MACHINE + CHILD + GRAMMAR + NUTSHELL
→ CREATE INTELLIGENCE FEED PROJECTION
→ PERSIST
→ VERIFY
→ GENERATE RECEIPT
→ SHOW EVIDENCE
→ UPDATE HUB WHEN CONNECTED
```

No stage may be silently skipped.

## Transaction rule

Where runtime/database support exists, artifact creation must be atomic or reconciled to an explicit `INCOMPLETE` state. A UI success state must never be emitted from client-side intent alone.

## Verification rule

The system verifies:

```text
4 transaction artifacts exist
+ 6 semantic perspectives exist
+ same event ID
+ valid IDs
+ provenance exists
+ timestamp exists
+ privacy state exists
+ links/references resolve
+ requested feed projection exists
+ Hub event reference is independently verified when Hub propagation is requested
= VERIFIED
```

Otherwise:

```text
SMART_NOTE_STATUS = INCOMPLETE
```

## Receipt rule

Only a verified event can produce a COMPLETE receipt. The receipt must contain real artifact/evidence references. If a reference cannot be resolved, the receipt is invalid and completion must not be claimed.

A compliant receipt must show, when available:

- Smart Note/event ID
- status
- timestamp
- exact subject
- Human Note evidence
- Naya Note evidence
- Machine Note evidence
- Child Note evidence
- Grammar Note evidence
- Nutshell evidence
- Intelligence Feed evidence
- Activity/Now evidence when Activity was requested or materially produced
- provenance/source context
- privacy/sharing state
- Hub propagation state
- verification result

## RESPONSE GATE — NON-NEGOTIABLE

Before Naya uses completion language such as **done, complete, saved, captured, remembered, locked, updated, or successfully added**, the runtime/agent response path must check for a valid receipt.

The required response sequence is:

**ACTION → VERIFY → SHOW EVIDENCE → REPORT RESULT**

If the receipt or required evidence is missing:

- status MUST be `INCOMPLETE`;
- Naya MUST identify what is missing;
- Naya MUST NOT imply that the requested operation completed;
- Naya MUST NOT substitute a roadmap, plan, conversational acknowledgment, or documentation update for the Smart Note transaction.

This gate exists specifically to prevent a conversational response from bypassing the Smart Note protocol.

## Hub update rule

The Intelligent Hub consumes the verified intelligence event. The Hub may display pending/incomplete state, but it must never display an unverified event as completed intelligence.

If the user explicitly requests an Activity/Now or Personal Intelligence feed update, the requested projection must be independently verified before the response reports it as updated.

## Sharing rule

Creation and sharing are separate operations.

```text
Smart Note → private intelligence event
        ↓ explicit user choice
Sharing Gate
        ↓
Intelligent Block
        ↓ authorization/consent
Collective
```

A connected source is not a shared source.

## Idempotency rule

Retries use the same operation/event identity when the original request is recoverable. The runtime must reconcile partial artifacts rather than blindly creating ambiguous duplicates.

## Failure contract

If any required artifact, perspective, feed projection, or verification condition fails:

- do not say "done"
- do not say "saved"
- do not generate a false receipt
- expose the missing component
- preserve safe partial state
- allow retry/reconciliation

## Universal implementation rule

Every Naya Power Naya implementation must treat this protocol and the Smart Note Constitution as higher-priority product behavior than cosmetic UI, convenience, or conversational completion language.

## Acceptance test

The implementation is not production-ready until an automated test can force each of these outcomes:

1. successful Smart Note with four transaction artifacts and six semantic perspectives;
2. missing Human Note;
3. missing Naya Note;
4. invalid Machine Note;
5. missing Child/Grammar/Nutshell perspective;
6. missing Feed Note;
7. mismatched event IDs;
8. broken evidence link;
9. missing provenance;
10. unauthorized sharing attempt;
11. requested Activity/Now projection not actually updated;
12. requested Hub propagation not independently verified;
13. response attempted to claim completion without a valid receipt;
14. retry after partial failure without duplicate ambiguity.

## Non-negotiable invariant

> **Naya may report completion only when the system has independently verified completion and can show the evidence.**
