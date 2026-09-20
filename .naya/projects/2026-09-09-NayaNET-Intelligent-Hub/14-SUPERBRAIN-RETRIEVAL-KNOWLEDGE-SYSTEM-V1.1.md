# NAYANET INTELLIGENT HUB — SUPERBRAIN RETRIEVAL & KNOWLEDGE SYSTEM
## Version 1.1

**Status:** CANONICAL ENGINEERING / DATA DESIGN CONTRACT
**Effective:** 2026-09-09
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## Purpose

Define the mechanisms around canonical Note Events so Naya retrieves the right evidence and context rather than merely accessing a large collection of files.

## Existing foundation — extend, do not duplicate

Canonical primary store:

`.naya/memory/events/YYYY/MM/DD/HH/<event_id>.json`

Canonical retrieval runtime:

`.naya/memory/smart_notes_v3.py`

The existing runtime already provides deterministic identity validation, chronological storage, exact retrieval, BM25 lexical ranking, TF-IDF semantic similarity, query expansion, metadata filtering, authority/lifecycle weighting, relationship-aware reranking, validation, and daily intelligence generation.

## Retrieval pipeline

```text
CANONICAL NOTE EVENTS
        ↓
IDENTITY + TIME + METADATA + SCOPE + PROVENANCE
        ↓
DERIVED INDEXES
        ↓
INTENT → SCOPE/PERMISSION → EXACT → LEXICAL → SEMANTIC
        ↓
METADATA → RELATIONSHIPS → TIME → LIFECYCLE → AUTHORITY
        ↓
TASK-AWARE RANKING
        ↓
SMALLEST SUFFICIENT CONTEXT
        ↓
SUMMARY → DETAIL → PRIMARY SOURCE
        ↓
NAYA REASONING / ACTION
        ↓
VERIFIED WRITE-BACK + INDEX REFRESH
```

## Required capabilities

### Identity
Stable event IDs independent of filename, folder, title, or UI.

### Time
Preserve `event_at`, `created_at`, `updated_at`, `observed_at`, `effective_at` / `effective_from` / `effective_to`, and supersession lineage where known. Use timezone-aware ISO-8601 values. Never fabricate time.

### Metadata
Identity, type, title, scope/project, timestamps, lifecycle, authority, verification, provenance, tags, aliases, concepts, relationships, permissions, summary, and canonical location.

### Hierarchy
**SYSTEM → DOMAIN → PROJECT → OBJECT → EVENT / DETAIL**. Physical chronology remains the canonical event organization; semantic views are derived.

### Scope and permissions
Resolve project/domain scope and authorization before context delivery. Default cross-scope behavior is deny unless explicitly authorized.

### Provenance
Track source type, source reference, observation time, authority, and verification. Generated or inferred content never becomes verified fact silently.

### Indexes
Maintain rebuildable identity, full-text, semantic, temporal, relationship, scope/permission, and lifecycle indexes as derived views.

### Relationships
Use stable-ID edges such as `relates_to`, `part_of`, `depends_on`, `supports`, `contradicts`, `supersedes`, `derived_from`, `decides`, `implements`, `verifies`, `caused_by`, and `results_in`. Bound traversal by relevance, scope, permission, and depth.

### Relevance
Combine task intent, explicit references, lexical match, semantic match, scope fit, permission fit, authority, temporal fit, lifecycle state, relationship proximity, and recency when appropriate.

### Summarization
Use **INDEX → SUMMARY → RELEVANT DETAIL → PRIMARY SOURCE**. Summaries are derived and must retain provenance.

### Current vs historical
Current-state requests use current verified evidence. Historical requests reconstruct only the state supported by evidence available at the requested time.

### Write-back
**DETECT → RESOLVE → CLASSIFY → RELATE → TIMESTAMP → WRITE → VALIDATE → VERIFY → RECEIPT → INDEX → LEARN**.

Before creating an event, determine whether to UPDATE, SUPERSEDE, LINK, or CREATE.

### Audit and outbox
Material changes remain traceable. External delivery is an outbox operation and cannot be the sole proof that a canonical event exists.

## Evaluation benchmark

Build an executable benchmark covering exact lookup, semantic lookup, relationship traversal, current-vs-historical state, stale/superseded material, permission boundaries, project isolation, timestamp reconstruction, contradictions, and summary-to-source traceability.

Success means correct, authorized, sufficiently complete, source-traceable context with minimal unnecessary context.

## Build law

**KEEP → EXTEND → REPAIR → REPLACE → BUILD NEW**

Do not build a second memory store, second Smart Note system, second retrieval runtime, or Hub-specific competing brain.
