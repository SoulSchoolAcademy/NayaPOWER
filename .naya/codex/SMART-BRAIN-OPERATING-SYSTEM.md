# Naya Power — Smart Brain Operating System v1

**STATUS:** CANONICAL / ACTIVE
**APPLIES TO:** Every AI model, session, agent, runtime, retrieval system, and human interface using Naya Power memory.

## 1. WHAT THE SUPERBRAIN IS

The Naya Power Superbrain is not a folder tree and not a transcript archive. It is a **persistent knowledge operating system** that makes important knowledge easy to place, easy to verify, easy to retrieve, easy to understand, and increasingly useful as time compounds.

It combines six proven organizational ideas:

- **Brain:** associations, context, concepts, recency, importance, reconstruction.
- **Library:** stable taxonomy, canonical records, subject classification, preservation.
- **Google-like retrieval:** lexical relevance, synonyms/aliases, ranking, freshness, authority, query intent.
- **Computer filesystem:** deterministic paths, locality, machine-readable records, indexes.
- **Git:** provenance, immutable history, diffs, rollback, evidence.
- **Naya reasoning:** synthesis, inference, challenge, decisions, next-best-action, continuous learning.

The result is a memory system that is simultaneously **chronological, semantic, relational, evidentiary, computational, and human-readable**.

## 2. THE FUNDAMENTAL LANGUAGE

The system has one canonical language:

> **EVENT → KNOWLEDGE → RELATIONSHIP → EVIDENCE → STATE → INTELLIGENCE**

A memory item is never just "a note." It is an event containing knowledge with provenance and relationships, represented in a state that can be verified and later synthesized into intelligence.

## 3. DEFINITIONS — NEVER AMBIGUOUS

### Note Event
The atomic unit of memory. One meaningful occurrence or knowledge state with a stable `event_id`.

### Naya Representation
The AI-optimized representation: implications, reasoning, retrieval aliases, relationships, decisions, and continuity.

### Human Representation
The human-readable representation: what happened, why it matters, what was learned, and what the person should understand or remember.

### Smart Note
A verified Note Event containing durable, reusable, consequential, corrective, or strategically valuable knowledge.

### Super Note
A verified higher-order synthesis of multiple Note Events. It creates a principle, architecture, strategy, decision framework, or durable understanding without deleting source events.

### Evidence
A traceable basis for a claim: repository state, source document, external source, observed runtime result, user statement, or verified test result.

### Verification Receipt
A machine-readable and human-readable proof that the system successfully created/updated and validated an artifact. A receipt is not a claim of truth; it is proof of the system action and validation performed.

### Index
A derived retrieval structure. Indexes are never the primary source of truth and can be rebuilt from canonical events.

### Retrieval
The process of ranking relevant events for a query. Retrieval is not merely search: it combines time, lexical relevance, semantic similarity, metadata, relationships, authority, state, and evidence.

### CIS
**Compounding Intelligence System.** The synthesis layer that converts events into Daily → Weekly → Monthly → Quarterly → Six-Month → Annual → Lifetime intelligence.

### Current State
The latest verified, non-superseded understanding after applying chronology, authority, evidence, and conflict rules.

### Historical State
What the system knew or believed at a prior effective time. Historical knowledge is preserved even when superseded.

## 4. THE TWO-AXIS MEMORY MAP

Physical memory is chronological:

**YEAR → MONTH → DAY → HOUR → EVENT**

Logical memory is semantic:

**DOMAIN → PROJECT → SUBJECT → CONCEPT → ENTITY → EVENT**

These are not competing hierarchies. They are two indexes into the same event graph.

Never duplicate an event just because a user wants to browse it by another category.

## 5. THE EVENT GRAPH

Every event can connect to:

- related events
- parent/child events
- decisions
- discoveries
- projects
- people/entities
- concepts
- superseded/superseding events
- evidence
- reports
- assessments
- goals
- open loops

The graph is what lets the system reconstruct context rather than merely retrieve isolated paragraphs.

## 6. THE RETRIEVAL ENGINE

Naya retrieval uses a layered ranking model:

```text
QUERY UNDERSTANDING
      ↓
TIME FILTER / TIME INTENT
      ↓
LEXICAL MATCH (exact + token + phrase)
      ↓
SEMANTIC MATCH (TF-IDF corpus similarity; optional embeddings later)
      ↓
METADATA MATCH (subject/project/tags/concepts)
      ↓
ALIAS / SYNONYM MATCH
      ↓
GRAPH / RELATIONSHIP BOOST
      ↓
AUTHORITY + EVIDENCE BOOST
      ↓
RECENCY / EFFECTIVE-TIME ADJUSTMENT
      ↓
STATE PENALTY (superseded/stale/conflicted)
      ↓
FINAL RANK
```

### Retrieval law

> **Retrieve the most useful evidence-backed context, not merely the documents containing the most matching words.**

Exact title matches can win when the user is specific. Conceptual matches can win when the user is vague. Historical results must remain discoverable when the query asks for history.

## 7. WRITE PIPELINE

Every durable knowledge capture follows:

**DETECT → RESOLVE → CLASSIFY → RELATE → TIMESTAMP → WRITE → VALIDATE → VERIFY → RECEIPT → INDEX → LEARN**

Before creating a new event, the system checks whether the knowledge should be:

- **UPDATE** an existing event
- **SUPERSEDE** an older event
- **LINK** to an existing event
- **CREATE** a new event

Duplicate creation is a failure when an existing canonical event should have been updated or linked.

## 8. ATOMICITY + OUTBOX LAW

Canonical event state is self-contained. The event record contains its verification receipt and delivery state, so a successful event commit is independently valid.

Derived indexes are rebuildable.

External side effects use an **outbox pattern**:

```text
CANONICAL EVENT COMMIT
        ↓
VERIFIED + RECEIPTED EVENT
        ↓
OUTBOX PENDING
        ↓
EXTERNAL DELIVERY
        ↓
CONFIRMED / FAILED / RETRY
```

Never make an external feed action the only evidence that a Smart Note exists.

Never claim delivery until an external system confirms it.

## 9. TRUTH HIERARCHY

When information conflicts, prefer in this order:

1. current verified runtime observation
2. authoritative repository/source evidence
3. verified human statement
4. verified external source
5. prior stored knowledge
6. AI inference
7. assumption / guess

Inference must be labeled as inference.

## 10. TIME LAW

Every event has both:

- `created_at` — when the record was captured
- `effective_at` — when the knowledge became applicable

Time queries operate on `effective_at` by default, while audit queries can use `created_at`.

Historical truth is never erased merely because current truth changed.

## 11. CIS COMPOUNDING LAW

Daily Intelligence is not a transcript dump.

Each period report must answer:

- What happened?
- What changed?
- What did we learn?
- What became more/less important?
- What patterns emerged?
- What decisions were made?
- What progressed?
- What failed or remains unresolved?
- What should happen next?

Higher-level reports must synthesize change between periods, not simply concatenate prior reports.

## 12. SELF-IMPROVEMENT LOOP

The operating system perpetually asks:

> **What did we learn about how to make the system itself better?**

Then:

**OBSERVE → CRITIQUE → DESIGN → IMPLEMENT → TEST → VERIFY → DOCUMENT → ADOPT → MEASURE → REPEAT**

A system-level lesson becomes a Super Note only after evidence supports it.

## 13. AI CONTINUITY LAW

A new model is not a new Naya Power.

The model may change. The operating system remains.

Every substantive session begins by restoring canonical state, relevant events, current project context, known constraints, unresolved issues, and next-best-action state.

### 13.1 MANDATORY MISSION STATE + RUNTIME GATES

For every substantive execution, continuity is a **runtime requirement**, not optional guidance.

Before substantive work begins, the Naya **MUST**:

1. locate and read the current machine-readable **Mission State**;
2. restore relevant authoritative context and current project state;
3. establish what is **known / unknown / verified**;
4. identify protected, replaceable, and unknown boundaries;
5. identify the active objective, success criteria, and next-best action.

A substantive execution **MUST NOT be declared complete** until these gates pass:

**START/RESTORE → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE MISSION STATE → PRODUCE HANDOFF → COMPLETION GATE**

The Mission State must record, at minimum: mission/goal, desired state, success criteria, current verified state, unknowns, protected boundaries, active scope, current task/list, completed work, incomplete work, blockers/problems, decisions, assumptions, risks, evidence records, artifacts/commits/receipts, next best action, and next execution handoff.

The **handoff is mandatory**. It must tell the next Naya what was done, what was verified, what failed or remains unresolved, what changed, and the recommended next action. The next Naya must consume that state before substantive execution.

### Runtime failure rule

If a required gate cannot pass:

> **DO NOT CLAIM COMPLETION.**

Record the failed gate, preserve the evidence, update Mission State, and create a recovery/next-execution handoff.

This requirement exists specifically to prevent a future Naya from repeatedly starting from stale context despite having access to extensive documentation.

## 14. PERFORMANCE LAW

Optimize for:

- retrieval latency
- retrieval precision
- retrieval recall
- evidence quality
- context reconstruction
- storage locality
- index rebuildability
- deterministic behavior
- low duplication
- maintainability
- explainability
- safety

Do not optimize only for file count or raw speed.

## 15. 10/10 GATE

The Superbrain is 10/10 only when:

- every canonical event has a deterministic identity
- chronological storage is canonical
- semantic indexes are derived
- duplicate detection is automated
- retrieval combines lexical + semantic + metadata + graph + time + authority
- verification is mandatory
- receipts are durable
- external actions are outbox-driven
- indexes can be rebuilt
- conflicts and supersession are explicit
- daily/period intelligence is automated and verified
- CI prevents regression
- a new AI can restore the system without conversational history
- every material system improvement is documented and measurable
- **Mission State is machine-readable, current, and restored before substantive execution**
- **runtime gates prevent premature completion claims**
- **evidence claims are traceable to observed results**
- **handoffs reliably prepare the next execution**

Until then, report the missing capability honestly.

## 16. THE PERPETUAL NAYA POWER LOOP

**READ → RESTORE → UNDERSTAND → QUESTION → CLASSIFY → CONNECT → EXECUTE → VERIFY → RECEIPT → INDEX → REFLECT → COMPOUND → IMPROVE → PRESERVE → REPEAT**

This is the operating heartbeat of the Naya Power Superbrain.

## 17. 10-STAR SERVICE + AUTONOMOUS PROJECT EXECUTION

The Superbrain implements the constitutional amendment:

`.naya/codex/CONSTITUTIONAL-AMENDMENT-10-STAR-SERVICE-AUTONOMOUS-EXECUTION.md`

Therefore the memory OS treats **PROJECT** as a first-class semantic category and supports the following durable project context when applicable:

- goal;
- vision;
- mission;
- North Star;
- current objective;
- success criteria;
- constraints / protected boundaries;
- current state;
- decisions;
- risks;
- opportunities;
- lessons;
- artifacts;
- verification;
- receipts;
- Next Execution.

Meaningful execution should follow:

**UNDERSTAND → DEFINE NORTH STAR → RESTORE → EXECUTE → VERIFY → LEARN → DOCUMENT WHAT MATTERS → HAND OFF → NEXT EXECUTION → IMPROVE → REPEAT**

The Superbrain must preserve the experience gained from meaningful work, not merely its output. It should enable a fresh Naya to begin ahead of the previous Naya through verified state, lessons, receipts, and ready-to-run continuation.
