# NAYANET INTELLIGENT HUB — SUPERBRAIN RETRIEVAL & KNOWLEDGE SYSTEM
## Version 1.1

**Status:** CANONICAL ENGINEERING / DATA DESIGN CONTRACT
**Effective:** 2026-09-09
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## PURPOSE

Define the intelligence mechanisms around canonical Note Events so Naya can retrieve the right evidence and context rather than merely access a large collection of files.

## CANONICAL FOUNDATION

The existing NayaPOWER runtime already establishes chronological Note Events as the canonical primary memory store and uses derived indexes and a dependency-free retrieval runtime. This design extends that path rather than creating a competing memory system.

Canonical primary store:

`.naya/memory/events/YYYY/MM/DD/HH/<event_id>.json`

Canonical retrieval runtime:

`.naya/memory/smart_notes_v3.py`

## CORE PIPELINE

```text
CANONICAL NOTE EVENTS
        ↓
IDENTITY + TIME + METADATA + SCOPE + PROVENANCE
        ↓
DERIVED INDEXES
  ├─ identity
  ├─ full-text / lexical
  ├─ semantic
  ├─ temporal
  ├─ relationship
  ├─ lifecycle
  └─ permission / scope
        ↓
HYBRID RETRIEVAL
        ↓
RELEVANCE RANKING
        ↓
CONTEXT ASSEMBLY
        ↓
SUMMARY → DETAIL → PRIMARY SOURCE
        ↓
NAYA REASONING / ACTION
        ↓
VERIFIED CHANGE / NEW INTELLIGENCE
        ↓
CANONICAL EVENT UPDATE + INDEX REBUILD/REFRESH
```

## 1. IDENTITY

Every durable event has a stable `event_id` independent of filename, title, folder, or UI location. IDs survive presentation changes.

## 2. TIME

The event model must preserve, where known:

```yaml
event_at:
created_at:
updated_at:
observed_at:
effective_at:
effective_from:
effective_to:
supersedes:
superseded_by:
```

Rules:

- use timezone-aware ISO-8601 values;
- never fabricate time;
- preserve source time separately from ingestion/creation time;
- reconstruct chronology from evidence;
- never let a display date overwrite underlying event time.

## 3. METADATA

Minimum useful metadata includes identity, type, title, scope/project, timestamps, lifecycle, authority, verification, provenance, tags, aliases, concepts, relationships, permissions, summary, and canonical path/reference.

Metadata is for classification and retrieval. It must not become a duplicate copy of the source content.

## 4. HIERARCHY

Use hierarchy for deterministic navigation:

**SYSTEM → DOMAIN → PROJECT → OBJECT → EVENT / DETAIL**

Physical chronology remains the canonical event-store organization. Semantic hierarchy is a derived view, not a second copy of the events.

## 5. PROJECT AND PRIVACY BOUNDARIES

Every retrieval request must resolve scope before context assembly.

Possible scopes include personal, business, product, client, engineering, project, experiment, collective, and public.

Default rule:

> **DENY CROSS-SCOPE RETRIEVAL UNLESS EXPLICITLY AUTHORIZED.**

## 6. PERMISSIONS

Authorization is evaluated before content is delivered to an agent.

At minimum distinguish owner, reader, contributor, editor, administrator, collective/shared membership, and public access. Permission inheritance must be explicit and auditable.

The current NayaPOWER repository architecture documents privacy/permission boundaries, but full production runtime enforcement remains a proof item until executable evidence demonstrates it.

## 7. PROVENANCE AND AUTHORITY

Meaningful knowledge must be traceable to one or more sources.

Recommended fields:

```yaml
source_type:
source_ref:
source_observed_at:
source_authority:
```

Possible authority states include verified, user_asserted, external, generated, and inferred.

Generated/inferred information must never silently become verified fact.

## 8. DERIVED INDEXES

Indexes accelerate discovery but are never primary truth and must be rebuildable from canonical events.

### Identity index
Stable ID → canonical object/path.

### Full-text index
Titles, filenames, phrases, content, tags, aliases, summaries, and searchable representations.

### Semantic index
Conceptual similarity using the existing TF-IDF baseline, with optional future embedding/vector adapters.

### Temporal index
Date ranges, chronology, recency, effective state, and point-in-time reconstruction.

### Relationship index
Typed graph edges among events and objects.

### Scope/permission index
Safe pre-filtering by authorization and project boundary.

### Lifecycle index
Current, active, stale, superseded, conflicted, historical, archived, and unknown states.

## 9. HYBRID RETRIEVAL

Use this staged strategy:

1. intent extraction;
2. scope and permission resolution;
3. exact IDs, filenames, explicit names, dates, and phrases;
4. lexical/full-text retrieval;
5. semantic retrieval;
6. metadata filtering;
7. relationship expansion;
8. temporal filtering;
9. lifecycle filtering;
10. authority/evidence weighting;
11. task-aware ranking;
12. smallest-sufficient context assembly;
13. source traceability.

Never depend exclusively on keyword search or vector similarity.

## 10. RELEVANCE RANKING

Conceptually:

```text
TASK INTENT
+ EXACT / EXPLICIT USER REFERENCE
+ LEXICAL MATCH
+ SEMANTIC MATCH
+ SCOPE FIT
+ PERMISSION FIT
+ AUTHORITY / VERIFICATION
+ TEMPORAL FIT
+ LIFECYCLE FIT
+ RELATIONSHIP PROXIMITY
+ RECENCY WHEN APPROPRIATE
= TASK RELEVANCE
```

The winning result is the most useful authorized evidence for the task, not the most textually similar document.

## 11. RELATIONSHIP GRAPH

Supported typed relationships include:

`relates_to`, `part_of`, `depends_on`, `supports`, `contradicts`, `supersedes`, `derived_from`, `decides`, `implements`, `verifies`, `caused_by`, `results_in`, `shares_scope_with`.

Traversal must be bounded by relevance, scope, permission, and depth. Never retrieve an entire graph because one node matched.

## 12. CONTEXT ASSEMBLY

Use progressive context:

- **Tier 0:** system authority and applicable laws;
- **Tier 1:** current task;
- **Tier 2:** current project state, protected boundaries, constraints, and next action;
- **Tier 3:** top relevant intelligence;
- **Tier 4:** primary evidence required for verification;
- **Tier 5:** historical context only when required.

This implements **FULL SYSTEM AWARENESS + SELECTIVE DEEP LOADING** and **RELEVANT CONTEXT, NOT MAXIMUM CONTEXT**.

## 13. SUMMARIZATION

Use:

**INDEX → SUMMARY → RELEVANT DETAIL → PRIMARY SOURCE**

Summaries are derived artifacts. They must retain source references and state information sufficient to distinguish current, historical, stale, superseded, conflicted, and unknown knowledge.

## 14. CURRENT VS HISTORICAL

For current-state requests, current verified evidence outranks historical material.

For historical requests, reconstruct only the state supported by evidence available at the requested time. Do not contaminate historical reconstruction with later knowledge.

## 15. WRITE-BACK / LEARNING

Durable intelligence follows:

**DETECT → RESOLVE → CLASSIFY → RELATE → TIMESTAMP → WRITE → VALIDATE → VERIFY → RECEIPT → INDEX → LEARN**

Before creating an event, determine whether to UPDATE, SUPERSEDE, LINK, or CREATE. Duplicate independent events are a failure when one canonical event should be extended.

## 16. AUDITABILITY

Material changes should record actor/tool, timestamps, source, change, reason, supersession, and verification evidence where applicable.

Git history is part of provenance but does not replace semantic event metadata.

## 17. CONFLICT DETECTION

When sources disagree, surface the conflict. Compare authority, time, scope, lifecycle, provenance, supersession, and verification. Prefer current verified reality while preserving historical evidence.

## 18. OUTBOX / EXTERNAL DELIVERY

Canonical event creation must not depend on successful external feed delivery.

```text
CANONICAL COMMIT
      ↓
VERIFIED RECEIPT
      ↓
OUTBOX PENDING
      ↓
EXTERNAL DELIVERY
      ↓
CONFIRMED / FAILED / RETRY
```

Never claim external publication until the destination confirms it.

## 19. RETRIEVAL EVALUATION

The retrieval benchmark must eventually cover exact lookup, semantic lookup, relationship traversal, current-vs-historical questions, stale/superseded material, permissions, project isolation, timestamp reconstruction, contradiction handling, and summary-to-source traceability.

Success means correct, authorized, sufficiently complete, source-traceable context with minimal unnecessary context.

## 20. CURRENT IMPLEMENTATION STATUS

The repository already has substantial implementation: chronological canonical events, an event index, validation, hybrid exact/lexical/TF-IDF retrieval, metadata filters, query expansion, authority/lifecycle weighting, relationship-aware reranking, daily intelligence generation, and runtime continuity contracts.

However, the canonical state explicitly records that real-checkout runtime receipts, A→B→C compounding proof, PIS propagation proof, adversarial continuity execution, full governance benchmark execution, and fresh successor behavioral acceptance remain open. These are proof gaps, not reasons to create a second retrieval architecture.

## 21. BUILD LAW

Before implementing a capability:

**KEEP → EXTEND → REPAIR → REPLACE → BUILD NEW**

Build new infrastructure only when existing canonical capabilities cannot satisfy the contract. Prefer adapters and extensions over parallel systems.

## 22. ULTIMATE TEST

Naya should be able to answer:

> **What did we decide about X, why, when, under which project/scope, based on what evidence, what superseded it, what is true now, and what should happen next?**

The answer must be assembled from authorized canonical evidence, not guessed from a pile of files.
