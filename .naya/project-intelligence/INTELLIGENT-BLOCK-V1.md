# INTELLIGENT BLOCK V1 — CANONICAL CONTRACT

STATUS: OFFICIAL NayaNET ARCHITECTURE
VERSION: V1
EFFECTIVE: 2026-09-21

## Purpose

An Intelligent Block is a structured, multidimensional representation of what NayaNET currently understands about a meaningful subject, concept, decision, capability, discovery, or problem.

It is not merely a note and not merely an event.

**INTELLIGENT BLOCK = WHAT WE UNDERSTAND**

The block is the reusable understanding layer built from one or more provenance-bound Intelligent Events.

## Canonical perspectives

A block should express the perspectives needed to make the subject understandable and useful:

- nutshell — what it is in the fewest truthful words;
- human — why it matters to a person;
- child — simplest understandable explanation;
- practical — how an ordinary person can use it;
- lived/practical wisdom — what it means in everyday life;
- AI — what an intelligence system should understand;
- machine — structures, inputs, outputs, constraints;
- algorithm — logic, transformations, decision rules;
- software — implementation/runtime implications;
- meaning — what it ultimately means;
- application — how it can be applied;
- benefit — what value it creates;
- usefulness — what problem it solves;
- helpfulness — how it helps the recipient;
- evidence — why the understanding is trustworthy;
- limitations — what is not known or cannot be claimed.

Not every block requires every perspective. The block must contain the perspectives necessary for its purpose.

## Required identity

Every canonical block MUST have:

- block_id
- subject_id or canonical subject key
- title
- block_type
- version
- status
- owner_scope
- created_at
- updated_at
- source_event_ids
- evidence_refs
- provenance
- understanding_state
- value_context
- applicable_scope
- supersedes / superseded_by when applicable
- schema_version

## Block types

- CONCEPT
- CAPABILITY
- DECISION
- DISCOVERY
- PROCEDURE
- PRINCIPLE
- MODEL
- PERSON_CONTEXT
- SYSTEM_STATE
- LESSON
- PATTERN
- EXPLANATION
- OUTCOME
- OTHER_GOVERNED

## Understanding states

- CANDIDATE
- CONTEXTUALIZED
- INTERPRETED
- VERIFIED
- DISTILLED
- APPLIED
- LEARNED
- SUPERSEDED

A block may be useful before verification, but it MUST clearly expose that state.

## Event relationship

Blocks are derived understanding, not replacements for events.

A block MUST retain source_event_ids sufficient to reconstruct why it exists.

A block can be rebuilt or revised when new events change understanding.

Example:

EVENT A: Shawn describes a problem.
EVENT B: Naya discovers a pattern.
EVENT C: Runtime verifies the pattern.
EVENT D: Shawn corrects one assumption.
EVENT E: Naya measures the resulting improvement.

BLOCK X then becomes the current verified understanding of the problem/pattern.

The events remain historical truth. The block is the current reusable interpretation.

## Value model

A block should make explicit:

- who benefits;
- what benefit is produced;
- what becomes easier/faster/better;
- what work can be avoided;
- what decision it enables;
- what risks it reduces;
- what limitations remain.

The system should optimize for:

**HIGHEST RESPONSIBLE VERIFIED HUMAN VALUE**

A block with high apparent usefulness but weak evidence is not equivalent to a verified high-value block.

## Distillation

Distillation MUST preserve:

- meaning;
- material context;
- evidence;
- provenance;
- uncertainty;
- authority;
- applicable scope;
- causal relationships necessary for verification.

Distillation MAY remove:

- redundant wording;
- already-understood explanation detail;
- irrelevant intermediate context;
- transient working material.

Distillation MUST NOT convert unknown into known or remove the ability to determine where the understanding came from.

## Retention

A block may be:

- ACTIVE — current working understanding;
- DURABLE — retained reusable intelligence;
- SUPERSEDED — preserved historical understanding replaced by a newer one;
- RELEASED — no longer active working context but recoverable through authorized provenance;
- DELETED — only when deletion is authorized and policy permits it.

Release is not forgetting the truth.

## Human comprehension protocol

The block should support progressive disclosure:

1. nutshell first;
2. benefit/meaning second;
3. practical application third;
4. evidence/provenance available immediately;
5. deeper technical perspectives on demand.

Naya should not make the human read the entire block to get its value.

## Quality rules

1. Truth before elegance.
2. Evidence before confidence.
3. Meaning before volume.
4. Context before compression.
5. Human usefulness before system convenience.
6. Reuse before repeated reconstruction.
7. Correction creates learning.
8. Unknown remains unknown.
9. Capability does not create authority.
10. A block is never authoritative merely because it exists.

## Minimum acceptance

A production implementation of INTELLIGENT_BLOCK_V1 must prove:

- source event linkage;
- evidence/provenance;
- explicit understanding state;
- useful multidimensional representation;
- authorized retrieval;
- revision/supersession;
- durable reuse;
- successor comprehension.

> The block is where events become reusable understanding.
