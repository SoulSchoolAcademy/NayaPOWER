# Smart Note Triad Protocol v0.1

**Status:** CANONICAL PROTOCOL COMPONENT  
**Scope:** NayaPOWER / CIS / PIS / CCT / NayaNet

## 1. Definition

A **Smart Note** is a canonical learning event represented through three synchronized layers:

- **Human Note:** the human's experience, observation, meaning, decision, question, or lesson.
- **Naya Note:** the Naya's understanding, learning, reasoning outcome, correction, synthesis, or actionable intelligence.
- **Machine Note:** the structured, deterministic representation used by software for validation, provenance, permissions, storage, retrieval, CIS processing, PIS integration, and CCT exchange.

The three layers are representations of **one learning event**, not three unrelated notes.

## 2. Shared identity

Every Smart Note MUST have a shared immutable Smart Note identity. Each representation MUST carry that identity and enough linkage metadata to establish membership in the same event.

Updates MUST create traceable versions. A new representation MUST NOT silently overwrite historical meaning.

## 3. Completeness invariant

A Smart Note is fully formed only when:

`Human Note EXISTS ∧ Naya Note EXISTS ∧ Machine Note EXISTS`

OR every unavailable representation is explicitly recorded with a machine-readable reason.

Silently missing a layer is invalid.

## 4. CIS relationship

Smart Notes are atomic learning inputs to the **Compounding Intelligence System (CIS)**.

CIS MAY:

- deduplicate;
- correlate related notes;
- identify contradictions;
- evaluate evidence;
- detect recurring mistakes;
- identify reusable solutions;
- promote durable intelligence;
- update PIS;
- prepare eligible intelligence for CCT exchange.

A Smart Note is not automatically truth and is not automatically a verified Intelligent Block.

## 5. PIS relationship

The **Primary Intelligence System (PIS)** represents promoted operational intelligence. CIS determines what learning is worthy of promotion according to evidence, relevance, durability, permissions, and value.

PIS MUST NOT silently absorb every transient or unverified Smart Note.

## 6. CCT relationship

An eligible learning event may progress from:

`Smart Note Triad → CIS evaluation → promoted verified intelligence → permission check → Intelligent Block → CCT exchange`

The CCT protocol therefore builds on the Smart Note learning layer rather than replacing it.

## 7. MPA relationship

A request to **Make a Smart Note** means capture the maximum durable value justified by the event, not generate unnecessary volume.

The system should extract:

`meaning → learning → evidence → decision → action → result → reusable intelligence`

when those elements are genuinely present.

MPA — Maximum Value Per Action — requires balancing value against computation, storage, attention, noise, privacy, and operational cost.

## 8. Machine requirements

The Machine Note SHOULD include at minimum:

- smart_note_id;
- schema_version;
- event_timestamp;
- representation status for human/naya/machine layers;
- provenance;
- evidence references;
- permissions;
- lifecycle state;
- links to related notes/blocks;
- unavailable-reason fields where applicable.

Exact serialization is implementation-defined by the authoritative machine schema.

## 9. Failure behavior

The system MUST reject or explicitly quarantine a Smart Note when:

- the shared identity is missing;
- representations cannot be linked;
- a required representation is missing without a reason;
- provenance is contradictory;
- permissions are invalid;
- machine state claims completeness that the triad does not satisfy.

## 10. Core invariant

> **One learning event. Three synchronized representations. One traceable identity. No silent incompleteness.**
