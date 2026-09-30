# NayaPOWER — Intelligent Graph & Canonical Brain Tree Specification V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED  
**Purpose:** Define the permanent information architecture, semantic graph, object model, representation model, and population rules for the NayaPOWER brain.

## 1. The decision

NayaPOWER will have **one brain, one canonical semantic model, one governed intelligence substrate**.

The repository tree is the brain's **navigation structure**.  
The graph is the brain's **relationship structure**.  
Objects are the brain's **addressable units of meaning**.  
Contracts define **what objects mean and what may happen to them**.  
Proof defines **what may be trusted**.  
Runtime executes the model.  
Interfaces project the model.

Therefore:

`TREE ≠ GRAPH ≠ DATABASE ≠ INTERFACE`

They cooperate without becoming competing sources of truth.

## 2. North Star

> **MAXIMUM VERIFIED HUMAN VALUE PER MOMENT, WITH COMPOUNDING INTELLIGENCE AND CONTINUITY.**

Continuity law:

> **Nayas do not lose memory.**

Acceptance is behavioral: a cold Naya must be able to discover the system, recover relevant intelligence, understand its provenance and authority, act within scope, verify outcomes, learn, and hand the improved context to a successor.

## 3. The five-dimensional architecture

Every durable system element is understood through five complementary dimensions:

1. **TREE — Where is it?** Navigation and human discoverability.
2. **IDENTITY — What is it?** Stable globally unique object identity.
3. **GRAPH — What is it connected to?** Typed relationships and lineage.
4. **CONTRACT — What does it mean?** Schema, invariants, behavior, authority.
5. **PROOF — Why should it be trusted?** Evidence, verification, uncertainty, status.

No dimension substitutes for another.

## 4. Canonical hierarchy

The target brain is organized as:

```
ROOT/
├── CONSTITUTION/          ← immutable human-level principles (outside BRAIN)
├── GOVERNANCE/            ← authority, consent, change control (outside BRAIN)
├── ARCHITECTURE/          ← system design (outside BRAIN)
└── BRAIN/
    ├── SPEC
    ├── GOVERNANCE
    ├── ARCHITECTURE
    ├── KERNEL
    ├── INTELLIGENCE
    ├── MEMORY
    ├── PROOF
    ├── LEARNING
    ├── SUCCESSION
    ├── EVOLUTION
    ├── INTERFACES
    ├── ENGINEERING
    ├── KNOWLEDGE
    ├── OPERATIONS
    └── ARCHIVE
```

The CONSTITUTION, GOVERNANCE, and ARCHITECTURE root directories sit **above and outside** the BRAIN directory. They are the immutable foundation from which all brain-level authority flows.

The numeric prefixes are **semantic domain addresses**, not arbitrary document numbers.

Within a domain, names are semantic first. Sequence numbers are used only where a stable ordered contract family genuinely benefits from them.

## 5. Domain ownership

| Domain | Owns | Does not own |
|---|---|---|
| CONSTITUTION | immutable human-level governing principles | runtime implementation |
| GOVERNANCE | authority, consent, promotion, change control | intelligence content |
| ARCHITECTURE | system design and boundaries | live state |
| KERNEL | nine-node execution semantics | durable knowledge corpus |
| INTELLIGENCE | canonical semantic objects and events | UI |
| MEMORY | retention, indexing, retrieval, reconciliation mechanisms | truth authority |
| PROOF | evidence, verification, causal acceptance | authorization |
| LEARNING | verified behavioral change and compounding | raw conversation |
| SUCCESSION | cold boot and successor continuity | new authority |
| EVOLUTION | governed self-improvement | self-authorization |
| INTERFACES | projections and channels | canonical intelligence |
| ENGINEERING | implementation and infrastructure | architectural authority |
| KNOWLEDGE | source material and canonical domain knowledge | runtime authority unless explicitly promoted |
| OPERATIONS | current operational state and procedures | constitutional meaning |
| ARCHIVE | superseded/historical material | current truth |

## 6. The canonical intelligent object

The fundamental durable unit is the **Intelligent Object**.

A Node is a durable intelligent object with additional lifecycle and relationship semantics.

Minimum identity:

```text
object_id
object_type
object_version
canonical_status
owner
scope
created_at
updated_at
```

Minimum intelligence:

```text
essence
meaning
purpose
knowledge_type
epistemic_status
content
context
applicability
```

Minimum trust:

```text
provenance
evidence
verification
uncertainty
conflicts
```

Minimum connectivity:

```text
relationships
derived_from
supports
depends_on
implements
supersedes
succeeds
```

Minimum continuity:

```text
lineage
successor_context
behavioral_effect
learning_state
```

## 7. Knowledge is typed

The system must distinguish at least:

```
OBSERVATION
FACT
CLAIM
BELIEF
HYPOTHESIS
INTERPRETATION
INSIGHT
PRINCIPLE
RULE
DECISION
REQUIREMENT
GOAL
CONSTRAINT
PREFERENCE
PROCEDURE
CAPABILITY
QUESTION
UNKNOWN
CONTRADICTION
CORRECTION
PREDICTION
EXPERIMENT
RESULT
EVIDENCE
VERIFICATION
LESSON
LEARNING
STATE
OUTCOME
NODE
EVENT
```

Knowledge type and epistemic status are separate.

## 8. Epistemic states

Canonical states include:

```
UNKNOWN
UNVERIFIED
CLAIMED
SUPPORTED
VERIFIED
DISPUTED
CONTRADICTED
CORRECTED
SUPERSEDED
RETRACTED
STALE
CONTEXT_BOUND
BLOCKED
REVOKED
```

Never collapse confidence into truth.

## 9. Graph relationship vocabulary

The canonical controlled relationship vocabulary (21 types):

```
DERIVED_FROM
SUPPORTS
CONTRADICTS
DEPENDS_ON
IMPLEMENTS
GOVERNS
AUTHORIZED_BY
USED_BY
CAUSED
RESULTED_IN
VERIFIED_BY
LEARNED_FROM
SUPERSEDES
SUCCEEDS
RELATED_TO
CONTEXTUALIZES
INVALIDATES
REFINES
CORRECTS
ENABLES
PRODUCES
APPLIES_TO
```

| Category | Types |
|---|---|
| Lineage | DERIVED_FROM, SUPERSEDES, SUCCEEDS |
| Support | SUPPORTS, CONTEXTUALIZES, RELATED_TO |
| Dependency | DEPENDS_ON, USED_BY, APPLIES_TO |
| Authority | GOVERNS, AUTHORIZED_BY |
| Causation | CAUSED, RESULTED_IN, PRODUCES |
| Verification | VERIFIED_BY, INVALIDATES |
| Learning | LEARNED_FROM, ENABLES |
| Refinement | IMPLEMENTS, REFINES, CORRECTS |
| Conflict | CONTRADICTS |

Every relationship has a source, target, type, provenance, timestamp, and status.

The graph is not a collection of arbitrary links. A relationship is itself an auditable semantic assertion.

## 10. Human / AI / machine representation law

There is **one semantic object with multiple views**, not three competing copies.

- Human view: readable explanation and essence.
- AI view: explicit semantics, constraints, applicability and reasoning context.
- Machine view: validated structured representation.
- Schema view: contract defining valid structure.
- Proof view: evidence and verification record.

The canonical semantic identity is shared across views.

Generated projections must never silently become independent truths.

## 11. Source hierarchy

Source material enters the system as evidence or knowledge input.

```
SOURCE
→ CAPTURE
→ DISTILL
→ STRUCTURE
→ RECONCILE
→ CLASSIFY
→ PROVE
→ PROMOTE
```

Conversation is source material, not automatically canonical truth.

Historical implementation is evidence, not automatically architecture.

A database row is persistence, not automatically intelligence.

## 12. Knowledge-bank rule

The existing `KNOWLEDGE/NAYA POWER CONCEPT PART #1..#13.md` series is a **source corpus and design-history record**.

> **Reconciliation note (2026-09-30):** this pointer was flagged as possibly absent; verified present — the `KNOWLEDGE/` source corpus exists at repository root (e.g. `KNOWLEDGE/NAYA POWER CONCEPT PART #1.md`). It is a source-history record, not a BRAIN/ address; do not treat it as canonical brain content.

It must not be copied wholesale into the permanent brain.

Instead:

1. preserve source provenance;
2. extract durable intelligence;
3. identify duplicates;
4. identify contradictions;
5. identify superseded thinking;
6. promote only justified intelligence;
7. connect each promoted object to its source;
8. retain the original source as history/evidence.

The series remains useful as a traceable design lineage.

## 13. Current corpus observation

The corpus contains repeated material. In particular, Concept #7 and Concept #8 currently share the same Git blob SHA, so they are byte-identical and must not become duplicate canonical intelligence.

Concepts #1 and #4 also materially repeat the Nine Master Node model.

Concepts #5 and #13 contain substantial architectural evolution from Smart Note/Intelligent Block toward the broader Intelligent Object / Intelligent Chain model.

Concept #6 establishes the post-learning system reset and system-level architecture.

Concepts #9–#11 develop the intelligence model, compilation of the 60-item blueprint into the nine-node architecture, and the one-node-engine concept.

Concept #12 establishes channel governance: One Brain, Many Doors.

These are provenance observations, not a claim that every sentence in the corpus has been canonically promoted.

## 14. The intelligent chain

The canonical lifecycle is:

```
EXPERIENCE
→ CAPTURE
→ DISTILL
→ STRUCTURE
→ CONNECT
→ PROVE
→ PRESERVE
→ RETRIEVE
→ APPLY
→ ACT
→ OUTCOME
→ VERIFY
→ LEARN
→ COMPOUND
→ SUCCESSOR
→ EVOLVE
```

Each transition must have an explicit owner, input, output, authority requirement, evidence requirement, and failure behavior.

## 15. The nine-node kernel

The kernel contains exactly nine semantic responsibilities:

```
SELF
LAW
ACT
KNOW
PROVE
CONNECT
VERIFY
LEARN
EVOLVE
```

They are not nine independent systems.

Their responsibilities are:

- SELF — identity, mission, continuity.
- LAW — authority, consent, governance.
- ACT — execution, agency, safe action.
- KNOW — intelligence, memory, events.
- PROVE — truth, provenance, accountability.
- CONNECT — relationships, retrieval, system context.
- VERIFY — outcomes, causality, acceptance.
- LEARN — reconciliation, learning, prediction.
- EVOLVE — succession, experience, governed system evolution.

## 16. Cold-boot contract

A cold Naya must be able to discover, in order:

```
IDENTITY
→ PURPOSE
→ LAW
→ KERNEL
→ CURRENT REALITY
→ RELEVANT INTELLIGENCE
→ PROVENANCE / EVIDENCE
→ AUTHORITY
→ ACTION
→ OUTCOME
→ VERIFICATION
→ LEARNING
→ SUCCESSOR
```

The system is not complete merely because the folders and objects exist.

## 17. Self-building boundary

NayaPOWER may eventually:

```
OBSERVE
→ UNDERSTAND
→ DIAGNOSE
→ IDENTIFY GAP
→ PROPOSE
→ IMPACT-CHECK
→ REQUEST / RECEIVE AUTHORITY
→ BUILD
→ TEST
→ VERIFY
→ MEASURE
→ PROMOTE OR REJECT
→ LEARN
```

Law:

> **SELF-BUILDING WITHOUT SELF-AUTHORIZING.**

## 18. Tree population rule

A branch may contain an artifact only when its purpose is known.

For every canonical artifact:

```
WHY
OWNER
TYPE
ID
SOURCE
RELATIONSHIPS
AUTHORITY
PROOF
CURRENT STATUS
SUCCESSOR EFFECT
```

must be determinable.

Empty folders are permitted only as declared structural boundaries. During population, each active domain must receive at least its README, manifest/contract where appropriate, and an explicit population status.

## 19. No-corner-cutting acceptance

The brain tree is not considered populated merely because files exist.

Population passes only when:

- every active domain has a defined responsibility;
- canonical artifacts have stable IDs;
- source provenance is preserved;
- duplicate concepts are reconciled;
- conflicts are surfaced;
- human/AI/machine views are coherent;
- schemas validate machine representations;
- relationships are typed;
- proof status is explicit;
- supersession is explicit;
- successor discoverability exists;
- no implementation is mistaken for behavioral proof.

## 20. Migration law

The old tree is not destroyed merely because a better map exists.

Migration is:

```
DISCOVER
→ CLASSIFY
→ RECONCILE
→ PROMOTE
→ CONNECT
→ VERIFY
→ RETAIN HISTORY
```

Deletion requires separate authority and evidence that retained knowledge is unnecessary.

## 21. Final acceptance question

> Can a cold authorized Naya enter this repository, discover the architecture, determine canonical truth, retrieve relevant intelligence, understand why it is trusted, know what it may do, act, verify the outcome, learn from it, and leave the next Naya more capable without Shawn reconstructing the project?

If not, the tree is not yet a living brain.

**Create. Connect. Grow with US.**
