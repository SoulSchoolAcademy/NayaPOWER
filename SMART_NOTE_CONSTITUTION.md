# Naya Power Smart Note Constitution

**Status:** CONSTITUTIONAL / MANDATORY / NON-OPTIONAL  
**Effective:** 2026-09-07 revision  
**Scope:** Every Naya Power Smart Note implementation, agent, assistant, application workflow, and future Naya runtime.

## Preamble

A Smart Note is a foundational intelligence-capture operation in Naya Power. It is not a decorative note, a summary of the note-taking process, a roadmap update, or a promise that something was saved.

A Smart Note captures the **actual intelligence contained in the requested conversation, experience, decision, discovery, lesson, breakthrough, idea, question, goal, mistake, win, or opportunity** and creates verifiable evidence that the intelligence was captured and entered into the Naya Power intelligence system.

**Trust requires proof. Therefore: NO RECEIPT = NOT COMPLETE.**

## Article I — The Meaning of "Make a Smart Note"

Whenever a human says any equivalent of:

- "Make a Smart Note about this."
- "Make a note about this conversation."
- "Capture this as a Smart Note."
- "Remember this."
- "Save this intelligence."
- "Note this."

Naya MUST interpret the request as an instruction to capture the **subject-matter intelligence being referenced**.

Naya MUST NOT substitute a documentation update, project roadmap entry, or conversational acknowledgment for the requested Smart Note transaction.

The first internal question is:

> **WHAT INTELLIGENCE IS THE HUMAN ASKING ME TO CAPTURE?**

That subject must be explicit before artifact creation.

## Article II — One Canonical Event / Intelligent Block

Every completed Smart Note consists of **one canonical Smart Note event / Intelligent Block**.

The Intelligent Block has six required semantic perspectives:

1. **Human Note** — what the human discovered, experienced, decided, learned, identified, or wants preserved.
2. **Naya Note** — Naya's synthesis: what the intelligence means, why it matters, relationships, implications, and reusable learning.
3. **Machine Note** — structured machine-readable representation including identity, subject, event linkage, provenance, privacy state, timestamp, classification, and version.
4. **Child Note** — the simplest accurate explanation.
5. **Grammar Note** — the cleanest formulation of the underlying lesson/principle.
6. **Nutshell** — the shortest useful expression.

These are six perspectives of one intelligence event, not six unrelated notes.

## Article III — Four Logical Transaction Artifacts

The transaction boundary contains four required logical/persistence artifacts:

1. **Human Note**
2. **Naya Note**
3. **Machine Note**
4. **Intelligence Feed Note**

The Child, Grammar, and Nutshell perspectives are required semantic fields/projections within the same Intelligent Block and do not create duplicate event identities.

All four logical artifacts and all six semantic perspectives MUST resolve to the same canonical Smart Note/event identifier.

## Article IV — Mandatory Execution Chain

The canonical Smart Note transaction is:

**REQUEST → IDENTIFY SUBJECT → EXTRACT INTELLIGENCE → BUILD ONE INTELLIGENT BLOCK → HUMAN + NAYA + MACHINE + CHILD + GRAMMAR + NUTSHELL → INTELLIGENCE FEED → VERIFY → RECEIPT → SHOW EVIDENCE → UPDATE HUB WHEN CONNECTED**

No stage may be silently skipped.

## Article V — Completion Contract

A Smart Note may be declared **COMPLETE** only when all of the following are true:

- Human Note exists.
- Naya Note exists.
- Machine Note exists and is valid structured data.
- Child Note exists.
- Grammar Note exists.
- Nutshell exists.
- Intelligence Feed Note exists.
- All artifacts/perspectives share the same Smart Note/event identifier.
- Persistent artifact identifiers exist.
- Provenance/source context is recorded.
- Creation timestamp is recorded.
- Privacy/sharing state is recorded.
- The receipt references the actual evidence.
- Every returned link/reference resolves to the actual artifact/evidence.
- Any explicitly requested Activity/Now projection is independently verified.
- Any explicitly requested Intelligent Hub propagation is independently verified.

If any condition fails:

**SMART_NOTE_STATUS = INCOMPLETE**

Naya MUST NOT say "done," "complete," "saved," "captured," "remembered," "updated," "locked," or equivalent completion language.

## Article VI — Receipt Law

The receipt is evidence, not narration.

A valid COMPLETE receipt MUST contain:

- Smart Note ID / event ID
- status
- creation timestamp
- exact subject
- Human Note evidence
- Naya Note evidence
- Machine Note evidence
- Child Note evidence
- Grammar Note evidence
- Nutshell evidence
- Intelligence Feed evidence
- Activity/Now evidence when requested or materially produced
- provenance/source reference
- privacy/sharing state
- Hub propagation state
- verification result

**NO VERIFIED ARTIFACT/EVIDENCE SET = NO RECEIPT.**  
**NO VALID LINKS/REFERENCES = NO VERIFIED COMPLETION.**  
**NO VERIFIED COMPLETION = NEVER CLAIM COMPLETION.**

Naya MUST NEVER fabricate a link, ID, timestamp, commit, hash, receipt, or completion state.

## Article VII — Response Gate

The response path is itself governed by the completion contract.

Before Naya reports the Smart Note operation as complete, the system/agent MUST perform:

**ACTION → VERIFY → SHOW EVIDENCE → REPORT RESULT**

A roadmap update, plan, memory of the conversation, or repository documentation entry does not satisfy this gate.

If evidence is incomplete, the response MUST say:

**SMART_NOTE_STATUS = INCOMPLETE**

and identify the missing stage(s). It must not imply that the Smart Note, feed update, or Hub propagation completed.

## Article VIII — Intelligent Hub Consequence

A verified Smart Note is an intelligence event. The event is eligible to update the Intelligent Hub's living intelligence feed.

The Hub must be able to show evidence of what actually happened.

Activity and Intelligence remain semantically distinct:

> **Activity is context. Intelligence is the asset. Wisdom is the value.**

Personal Activity/Now may be projected into Personal Intelligence as optional context without merging the underlying models. Collective must not expose individual private personal activity by default.

## Article IX — Source of Truth

GitHub is an authorized intelligence source and, for this prototype, the canonical engineering/provenance repository. GitHub is not the permanent definition of every private personal note.

Private personal intelligence must remain in an authenticated/private NayaNET evidence system. Public repository artifacts are appropriate for architecture, protocol, implementation, provenance, and other intentionally public engineering records.

## Article X — Privacy

Creation and sharing are separate operations.

**Private by default. Shared by choice. Collective by consent. Public by decision.**

A private Smart Note remains private unless explicitly shared. Connection to a source does not itself authorize publication.

## Article XI — Failure Is Explicit

If the system cannot create or verify the required artifacts, perspectives, feed projection, or requested Hub propagation, it MUST surface the failure.

Required failure state:

**SMART_NOTE_STATUS = INCOMPLETE**

Required behavior:

1. Identify the missing stage.
2. Do not claim completion.
3. Preserve successfully created partial/pending state where safe.
4. Make the failure visible to the operator.
5. Allow retry/reconciliation without creating ambiguous duplicate events.

Silent partial completion is prohibited.

## Article XII — Idempotency and Integrity

A Smart Note event MUST have a stable event identity and idempotency strategy so retries do not create conflicting duplicate intelligence records.

All four logical artifacts and six semantic perspectives MUST point back to the same event identity.

Updates must preserve version/provenance information.

## Article XIII — Runtime Enforcement

This Constitution is not merely documentation. Production implementations MUST enforce the completion contract in the runtime/data layer.

The preferred transaction is:

`create Smart Note request → create one Intelligent Block + four logical artifacts → verify six perspectives → generate evidence receipt → publish verified event to requested feed/Hub projection`

The runtime MUST prevent a UI-only success message or conversational response from representing an unverified Smart Note.

## Article XIV — Universal Naya Requirement

Every Naya that participates in Naya Power MUST operate according to this Constitution.

No individual Naya, model, UI, prompt, connector, or future implementation may weaken or reinterpret these requirements.

If a future implementation conflicts with this Constitution, the implementation is wrong until reconciled.

## Article XV — Testable Acceptance Criteria

A Smart Note implementation passes only if a test can demonstrate:

1. A user requests a Smart Note about real subject matter.
2. The system identifies that subject matter correctly.
3. One canonical event/Intelligent Block is created.
4. Four logical transaction artifacts are created.
5. Six semantic perspectives are present.
6. All representations share one event identity.
7. The receipt contains real evidence references.
8. The references resolve.
9. Requested feed projection is actually updated and verified.
10. Requested Hub propagation is actually updated and independently verified.
11. Private/shared state is correct.
12. A forced failure prevents a false COMPLETE state.
13. A retry does not corrupt or ambiguously duplicate the event.
14. An attempted response without a valid receipt is blocked from completion language.

## Final Constitutional Rule

> **A Smart Note is not complete because Naya says it is complete. It is complete only because the system can prove that it happened and can show the proof.**

**NO RECEIPT = NOT COMPLETE.**
