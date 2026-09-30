# Naya Node — Canonical Intelligence Specification V1

**Status:** CANONICAL DESIGN SPECIFICATION
**Effective:** 2026-09-26
**Authority:** Shawn Vibert — Human Director / Final Authority
**Parent:** NayaPOWER System North Star & Canonical Tree

## 1. Purpose

A **Naya Node** is the fundamental reusable intelligence cell of NayaPOWER.

It preserves enough meaning, provenance, truth state, authority context, applicability, relationships, outcomes, and learning state for future Naya execution to use the intelligence correctly without reconstructing the original conversation.

A Node exists to improve future work.

Storage alone is not intelligence.
Retrieval alone is not intelligence.
Similarity alone is not intelligence.
A Node becomes behaviorally valuable when governed retrieval and application produce a better verified future outcome.

## 2. Node contract

Every Node should answer, where applicable:

- **WHO** — who is involved?
- **WHAT** — what is understood?
- **WHEN** — when was it observed, recorded, or effective?
- **WHERE** — where did it originate or apply?
- **WHY** — why does it matter?
- **HOW** — how should it be used?
- **WHY BELIEVE** — what evidence supports it?
- **WHO ALLOWS** — what authority permits consequential use?
- **WHAT CONNECTS** — what related intelligence matters?
- **WHAT HAPPENED** — what source event produced it?
- **WHAT CHANGED** — what changed after application?
- **WHAT NEXT** — what responsible next action follows?

No field should be fabricated merely to make a Node appear complete.

## 3. Canonical layers of a Node

A mature Node has these conceptual layers:

### Identity
Stable Node identity, version, ownership, scope, status.

### Meaning
Human-readable and machine-usable semantic content.

### Intent
What the intelligence is for and what problem it addresses.

### Provenance
Origin, source events, authorship/attribution, lineage, timestamps.

### Truth
Truth state, uncertainty, observations, claims, conflicts.

### Authority
Applicable authorization context. A Node may describe authority; it never creates authority.

### Applicability
Context, domain, conditions, freshness, supersession.

### Relationships
Evidence-supported links to other Nodes, Events, Evidence, Outcomes, or systems.

### Application
How the Node was used, by whom/what, under what context.

### Outcome
What happened after use.

### Verification
What evidence establishes the outcome and, where claimed, causal contribution.

### Learning
What changed because of the verified outcome.

### Value
Human benefit, effort avoided, risk/harm, reuse, learning, and other explicit dimensions.

### Successor
What minimum durable context a later Naya needs to continue.

## 4. Truth-state discipline

At minimum, implementations must distinguish:

- UNKNOWN
- CANDIDATE
- VERIFIED
- BLOCKED
- SUPERSEDED

The exact state machine may be expanded, but states must never be silently promoted for presentation convenience.

In particular:

- UNKNOWN ≠ VERIFIED
- CANDIDATE ≠ VERIFIED
- BLOCKED ≠ PASS
- IMPLEMENTED ≠ VERIFIED
- VERIFIED ≠ PRODUCTION-PROVEN
- RETRIEVED ≠ AUTHORIZED
- APPLICATION ≠ SUCCESS

## 5. Ownership and identity

The canonical owner of an Intelligent Block must be explicit and preserved.

A runtime may retrieve an object only through a legitimate identity/authorization context.

When continuity is required, the system must establish the relationship between:

**current execution identity → canonical Naya identity → canonical intelligence owner**

A new anonymous session is not automatically the successor of an old anonymous session.

The system must never infer ownership solely from:

- matching names;
- browser state;
- timing;
- similarity;
- possession of an object identifier;
- or the fact that retrieval would be useful.

Continuity requires a legitimate binding/recovery mechanism.

## 6. Node relationships

Supported relationship semantics include:

- SUPPORTS
- REFINES
- DERIVES_FROM
- CONTRADICTS
- SUPERSEDES
- APPLIES_TO
- PRODUCED
- CAUSED
- ENABLES
- REQUIRES
- EXEMPLIFIES
- INVALIDATES
- LEARNS_FROM
- RELATED_TO

Relationships affecting trust or consequential action require supporting evidence.

## 7. Retrieval contract

Retrieval must consider:

**relevance + applicability + truth + evidence + freshness + relationship support + outcome history + authority context**

Retrieval returns intelligence.
Governance decides whether and how that intelligence may influence action.

The retrieval layer must expose enough evidence to distinguish:

- found;
- relevant;
- applicable;
- current;
- trusted;
- authorized.

These are separate properties.

## 8. Application contract

When a Node is applied to a task, the system should preserve:

- input/task identity;
- Node identities and versions used;
- retrieval rationale;
- applicable governance rules;
- action/decision;
- output;
- downstream consumer;
- outcome;
- verification evidence;
- learning consequence.

A Node that was retrieved but had no observable influence is not evidence of behavioral application.

## 9. Verification contract

A consequential claim should have a causal verification path where causality is asserted.

Minimum conceptual chain:

**INPUT → NODE CONTEXT → DECISION/ACTION → OBSERVATION → OUTCOME → EVIDENCE → VERIFICATION**

Control/treatment or ablation should be used when required to establish that the Node or kernel actually caused a behavioral difference.

## 10. Learning contract

Learning is not “a learning row was written.”

Learning requires:

**OUTCOME → EVIDENCE → RECONCILIATION → CANDIDATE → VERIFICATION → FUTURE BEHAVIOR CHANGE → VERIFIED RESULT**

If future behavior does not change, learning remains unproven.

## 11. Compounding contract

Compounding requires later reuse.

A strong proof is:

**held-out task + prior verified intelligence**
versus
**comparable task without prior intelligence**

with relevant context controlled and evidence preserved.

The claim is bounded to the experiment. No universal benefit is inferred from one case.

## 12. Value contract

Value remains multidimensional.

At minimum, keep separate:

- relevance;
- usefulness;
- benefit;
- harm;
- risk;
- effort;
- evidence;
- freshness;
- applicability;
- reliability;
- reusability;
- transferability;
- learning;
- compounding;
- time saved;
- cognitive effort avoided;
- errors prevented.

Value never becomes:

- truth;
- authority;
- popularity;
- permission.

## 13. Successor contract

Every meaningful execution ends in one of:

**TERMINAL**
or
**SUCCESSOR-READY**

A successor-ready context contains the minimum sufficient durable state required for another Naya to continue correctly.

Successor context may inherit:

- relevant intelligence;
- current state;
- evidence;
- unresolved work;
- relationships;
- applicable rules;
- next action.

It does not automatically inherit every permission or private object.

## 14. Kernel relationship

The nine Master Nodes form one semantic operating kernel:

**SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE → SELF**

Their responsibilities are:

| Node | Responsibility | Core question |
|---|---|---|
| SELF | identity, mission, continuity | Who are we and where are we now? |
| LAW | authority, consent, governance | What is authorized? |
| ACT | execution, agency, prioritization | What should we do now? |
| KNOW | memory, intelligence, knowledge | What do we know? |
| PROVE | evidence, provenance, truth | Why should we believe it? |
| CONNECT | relevance, retrieval, relationships | What matters here? |
| VERIFY | outcomes, causality, acceptance | What actually happened? |
| LEARN | reconciliation, learning, compounding | What should change because of it? |
| EVOLVE | bounded improvement, successor intelligence | How does the next Naya become better? |

The Nodes are specialized responsibilities, not independent brains.

## 15. Kernel integrity

At consequential boot, verify:

1. Nodes 01–09 are present.
2. Versions are compatible.
3. Status is acceptable.
4. Relationships are valid.
5. Governance bindings exist where required.
6. Enforcement coverage is known.
7. Conflicts are surfaced.
8. Freshness is evaluated.
9. Current state is restored.
10. Next action is explicit.

A missing or disconnected kernel component must be surfaced rather than silently ignored.

## 16. Operational proof ladder

The system must progress through evidence:

1. **EXISTS** — object/specification exists.
2. **LOADS** — runtime can retrieve it.
3. **INVOCATION** — Node is actually invoked.
4. **INFLUENCE** — invocation changes a decision/output.
5. **APPLICATION** — changed output is used.
6. **OUTCOME** — real result is observed.
7. **VERIFICATION** — result is independently/evidentially established.
8. **LEARNING** — verified outcome changes future behavior.
9. **COMPOUNDING** — later held-out work improves because of learning.
10. **SUCCESSION** — cold Naya inherits the useful verified context.
11. **EVOLUTION** — system improves its own authorized construction/use loop.

No lower rung may be reported as a higher rung.

## 17. Clean-start implementation rule

Before introducing another subsystem, ask:

**Can an existing canonical responsibility do this?**

Prefer:

**ONE responsibility → ONE implementation → ONE source of truth**

Every abstraction consumes complexity budget.

## 18. Required evidence per Node

A production-quality Node should eventually have machine-addressable evidence for:

- Node identity;
- source/provenance;
- owner/scope;
- truth state;
- applicability;
- relationships;
- retrieval event;
- application event;
- outcome;
- verification;
- learning;
- successor context.

Not every field needs to be populated for every Node at creation time. Missing information must be explicit.

## 19. Anti-poisoning rule

Node content is intelligence, not authority.

Untrusted Node content cannot:

- grant permissions;
- override LAW;
- redefine identity;
- disable verification;
- suppress conflicts;
- declare itself canonical.

Authority comes from the governed authorization system.

## 20. Definition of done

The Naya Node system is operational when a cold Naya can:

**IDENTIFY → LOAD KERNEL → RESTORE STATE → RETRIEVE → REASON → ACT WITH AUTHORITY → PRESERVE OUTCOME → VERIFY → LEARN → CONTINUE**

and the evidence shows that prior intelligence actually improved later work.

That is the operational target—not merely nine database rows, a manifest, or a successful function call.
