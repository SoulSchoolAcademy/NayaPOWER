# 9F INTELLIGENT HUB — SUPERBRAIN RETRIEVAL & KNOWLEDGE SYSTEM
## Version 1.0

**Status:** CANONICAL ENGINEERING/DATA DESIGN CONTRACT  
**Effective:** 2026-09-09  
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## PURPOSE

Define the system that sits around raw Markdown/files so Naya can retrieve the right intelligence rather than merely access a large pile of documents.

## CORE MODEL

```text
RAW SOURCES
   ↓
CANONICAL OBJECT IDENTITY
   ↓
TIME + METADATA + SCOPE + PROVENANCE
   ↓
DERIVED INDEXES
   ├─ exact/ID
   ├─ full-text
   ├─ semantic
   ├─ temporal
   ├─ relationship
   ├─ lifecycle
   └─ permission
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
CANONICAL SOURCE UPDATE + INDEX REFRESH
```

## 1. CANONICAL OBJECT IDENTITY

Every durable intelligence object receives a stable identifier independent of filename, folder, title, or UI location.

Recommended identity fields:

```yaml
id: <stable-id>
type: <object-type>
scope: <scope-id>
project: <project-id-or-null>
```

IDs must survive renames and moves.

## 2. TIME MODEL

Time must be explicit and multi-dimensional.

```yaml
event_at: <when the event happened, if known>
created_at: <record creation time>
updated_at: <last material update>
observed_at: <when state/source was observed>
effective_from: <optional>
effective_to: <optional>
supersedes: <optional stable id>
superseded_by: <optional stable id>
```

### Rules

- Prefer ISO-8601 with timezone when known.
- Never fabricate a time.
- Preserve source timestamps separately from ingestion timestamps.
- Chronology must be reconstructable.
- A display date must never overwrite the underlying event time.
- Historical restore must use evidence available at the requested point in time.

## 3. HIERARCHY

Use hierarchy for deterministic navigation:

```text
SYSTEM
  └── DOMAIN
      └── PROJECT
          └── OBJECT
              └── EVENT / DETAIL
```

Folder structure is useful but is not the only organization mechanism.

## 4. METADATA

Metadata should describe an object without duplicating its full content.

Minimum useful dimensions:

- identity;
- type;
- scope;
- project;
- timestamps;
- status/lifecycle;
- authority;
- provenance;
- tags/classification;
- relationships;
- permissions;
- summary;
- source path/location;
- checksum/version where appropriate.

Metadata must remain machine-readable and human-inspectable.

## 5. PROJECT BOUNDARIES

Every retrieval operation must determine scope before assembling context.

Example scopes:

```text
PERSONAL
BUSINESS
CLIENT/<id>
PRODUCT/<id>
PROJECT/<id>
ENGINEERING/<id>
EXPERIMENT/<id>
COLLECTIVE/<id>
PUBLIC
```

Default behavior: **deny cross-scope retrieval unless explicitly authorized or governed by a rule.**

## 6. PERMISSIONS

Permission evaluation occurs before context delivery, not after an agent has already received sensitive content.

At minimum distinguish:

- owner;
- reader;
- contributor;
- editor;
- administrator;
- shared/collective membership;
- public.

Permissions must be attached to stable objects/scopes and inherited only according to explicit rules.

## 7. PROVENANCE

Every meaningful knowledge object should be traceable to one or more sources.

Recommended provenance fields:

```yaml
source_type: conversation | file | github | web | user | tool | system
source_ref: <stable reference>
source_observed_at: <timestamp>
source_authority: verified | user_asserted | external | generated | inferred
```

Generated or inferred information must not silently become verified fact.

## 8. INDEXING

Indexes are derived acceleration structures. They never replace canonical source files.

Maintain independently refreshable indexes for:

### Identity index
Maps stable IDs to objects and locations.

### Lexical/full-text index
Supports exact words, phrases, titles, filenames, and field searches.

### Semantic index
Supports conceptually related queries using embeddings or another semantic representation.

### Temporal index
Supports date ranges, point-in-time restore, recency, chronology, and effective-state queries.

### Relationship index
Supports graph traversal and connected-context discovery.

### Scope/permission index
Supports safe filtering before retrieval.

### Lifecycle index
Supports current, active, stale, superseded, archived, conflicted, and unknown states.

## 9. HYBRID RETRIEVAL

Never depend exclusively on vector search.

Use a staged retrieval strategy:

1. **Intent extraction** — determine what the user is actually asking.
2. **Scope resolution** — identify project/domain/permission boundary.
3. **Exact retrieval** — IDs, filenames, explicit names, dates, exact phrases.
4. **Lexical retrieval** — relevant text matches.
5. **Semantic retrieval** — conceptually relevant material.
6. **Relationship expansion** — connected decisions, sources, dependencies, and outcomes.
7. **Temporal filtering** — current/historical/effective period.
8. **Lifecycle filtering** — exclude superseded/stale material unless historically relevant.
9. **Authority filtering** — favor authoritative evidence.
10. **Ranking** — score remaining candidates by task relevance.
11. **Context assembly** — produce the smallest sufficient evidence set.
12. **Source traceability** — preserve references for consequential claims.

## 10. RELEVANCE RANKING

Conceptual ranking formula:

```text
RELEVANCE =
  task_intent
+ semantic_match
+ lexical_match
+ scope_fit
+ permission_fit
+ authority
+ temporal_fit
+ lifecycle_fit
+ relationship_proximity
+ explicit_user_reference
```

The exact numerical implementation may evolve. The governing principle does not:

> **The best result is the most useful authorized evidence for this task—not simply the most similar text.**

## 11. RELATIONSHIP GRAPH

Objects may explicitly relate through typed edges:

```text
relates_to
part_of
depends_on
supports
contradicts
supersedes
derived_from
decides
implements
verifies
caused_by
results_in
shares_scope_with
```

Graph traversal should be bounded by task relevance, permissions, and scope. Do not retrieve an entire graph because one node matched.

## 12. SUMMARIZATION

Use progressive context:

```text
INDEX
  ↓
OBJECT SUMMARY
  ↓
RELEVANT EXCERPT / DETAIL
  ↓
PRIMARY SOURCE
```

Summaries are derived artifacts and must preserve source references.

A summary should answer:

- What is this?
- Why does it matter?
- What changed?
- What is the current state?
- What evidence supports it?
- What related intelligence matters?
- What action, if any, follows?

## 13. CONTEXT ASSEMBLY

Naya should receive context in layers rather than a giant dump:

### Tier 0 — System authority
Applicable laws, safety, governance, and runtime rules.

### Tier 1 — Task context
The current user request and immediate objective.

### Tier 2 — Project context
Current project state, protected surfaces, constraints, and next action.

### Tier 3 — Relevant intelligence
Top-ranked notes, decisions, knowledge, and relationships.

### Tier 4 — Evidence
Primary source excerpts required for verification.

### Tier 5 — Historical context
Only when the task requires chronology or reconstruction.

This implements:

> **FULL SYSTEM AWARENESS + SELECTIVE DEEP LOADING.**

## 14. CURRENT VS HISTORICAL TRUTH

For current-state questions, current verified evidence outranks historical material.

For historical questions, retrieve the state applicable to the requested time and do not contaminate it with later knowledge.

Every state-sensitive answer should distinguish:

**CURRENT / HISTORICAL / STALE / SUPERSEDED / CONFLICTED / UNKNOWN**

## 15. WRITE-BACK / LEARNING LOOP

When a task creates durable intelligence:

```text
CONVERSATION / ACTION
        ↓
DISTILL
        ↓
CLASSIFY
        ↓
ASSIGN ID + TIMESTAMPS
        ↓
ATTACH SOURCE + SCOPE + PERMISSIONS
        ↓
CONNECT RELATIONSHIPS
        ↓
WRITE CANONICAL OBJECT
        ↓
UPDATE DERIVED INDEXES
        ↓
VERIFY
        ↓
AVAILABLE FOR FUTURE RETRIEVAL
```

Do not write every conversational sentence into permanent memory.

## 16. DUPLICATION CONTROL

Prefer one canonical object plus references/memberships over multiple independent copies.

If duplication is necessary for performance or portability, mark derived copies and retain the canonical source reference.

## 17. CONFLICT DETECTION

When multiple relevant sources disagree, the system should surface the conflict rather than silently selecting a convenient answer.

Conflict evaluation should consider:

- authority;
- timestamp;
- scope;
- lifecycle state;
- source provenance;
- explicit supersession;
- verification state.

## 18. RETRIEVAL EVALUATION

The system must eventually be tested against a curated retrieval benchmark containing:

- exact lookup cases;
- semantic lookup cases;
- cross-document relationship cases;
- current-vs-historical cases;
- stale/superseded cases;
- permission-boundary cases;
- project-isolation cases;
- timestamp reconstruction cases;
- contradiction cases;
- summary-to-source traceability cases.

Success is not "search returned something." Success is **correct, authorized, sufficiently complete, source-traceable context delivered with minimal unnecessary context.**

## 19. ORGANIZATION LAW

> **FOLDERS ORGANIZE LOCATION. METADATA ORGANIZES MEANING. RELATIONSHIPS ORGANIZE CONNECTION. INDEXES ORGANIZE DISCOVERY. TIME ORGANIZES HISTORY. PERMISSIONS ORGANIZE ACCESS. RELEVANCE ORGANIZES ATTENTION. SUMMARIZATION ORGANIZES CONTEXT.**

No single mechanism should be forced to do all of these jobs.

## 20. ULTIMATE ACCEPTANCE TEST

Ask Naya:

> "What did we decide about X, why did we decide it, when did we decide it, what evidence supported it, what project did it belong to, what superseded it, what is the current state, and what should we do next?"

A mature Superbrain should be able to answer by assembling the relevant evidence—not by guessing from a giant pile of files.

## 21. BUILD PRIORITY

The implementation sequence is:

**IDENTITY → TIME → METADATA → SCOPE → PERMISSIONS → PROVENANCE → EXACT SEARCH → FULL-TEXT INDEX → SEMANTIC INDEX → RELATIONSHIPS → RELEVANCE → SUMMARIZATION → LIFECYCLE → AUDIT → CROSS-TOOL ORCHESTRATION → EVALUATION**

Build the boring foundations first. They are what make the extraordinary intelligence possible.
