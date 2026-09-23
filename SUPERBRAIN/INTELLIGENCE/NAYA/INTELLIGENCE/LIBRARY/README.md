# 🔱 PROJECT INTELLIGENCE LIBRARY

**Status:** CANONICAL LIBRARY INDEX
**Scope:** Unified NayaNET / NayaPOWER Project Intelligence
**Authority:** Governed by the current Project Intelligence standards; this file is an index, not a competing standard.

## Purpose

Project Intelligence is a searchable library, not a pile of notes.

The repository may contain implementation, contracts, evidence, historical intelligence, and source artifacts in their operational locations. The library provides the common retrieval model and canonical index for that intelligence without requiring duplicate copies of the same content.

## One project

For NayaNET/NayaPOWER:

> **PROJECT INTELLIGENCE = NAYANET / NAYAPOWER**

Do not create artificial project identities for individual departments, documents, or subsystems when they are part of the same project.

## Retrieval model

```text
PROJECT
  → CATEGORY
    → YEAR
      → MONTH
        → DAY
          → TIME
            → INTELLIGENCE
```

Durable intelligence should be retrievable by:

- project
- category
- year / month / day / time
- title
- type
- status
- authority
- source
- provenance
- relationship
- privacy
- verification

Date/time describes when an intelligence item was created or observed. It does not, by itself, establish current authority.

## Canonical categories

| Category | Contains |
|---|---|
| `GOVERNANCE` | Laws, authority, constitutional rules, operating contracts |
| `PRODUCT` | Product vision, UX, journeys, requirements, acceptance criteria |
| `DESIGN` | Visual language, interaction systems, protected references, design decisions |
| `ENGINEERING` | Architecture, implementation contracts, APIs, code/system decisions |
| `RUNTIME` | Deployments, executions, runtime state, operational findings |
| `EVIDENCE` | Receipts, proofs, verification artifacts, independent observations |
| `LEARNING` | Lessons, corrections, generalized knowledge, improvements |
| `DECISIONS` | Material human decisions and rationale |
| `RESEARCH` | External/internal research and source-backed findings |
| `ACTIVITY` | Dated work history and continuity records |
| `MEMORY` | Durable intelligence intended for retrieval and compounding |
| `HISTORICAL` | Superseded intelligence retained for provenance only |

## Authority rule

The library does not create authority by location, filename, timestamp, or document size.

Current authority is determined by the governing standards and current accepted project state. Historical intelligence remains useful when it explains what happened, why something changed, or what was learned; it must not silently compete with the current standard.

## No-duplication rule

Do not copy one intelligence item into multiple folders merely to make it searchable.

Use metadata, indexes, relationships, and source references instead.

The preferred durable path for newly normalized intelligence is:

`NAYA/INTELLIGENCE/LIBRARY/<PROJECT>/<CATEGORY>/<YEAR>/<MONTH>/<DAY>/<TIME>-<SLUG>.md`

Existing operational files may remain in place when moving them would break references, workflows, provenance, or deployment behavior. Normalize by classification and indexing first; migrate physical paths only when the migration has a demonstrated value and a safe compatibility plan.

## Current corpus registry

See [`CORPUS-REGISTRY.md`](./CORPUS-REGISTRY.md) for the first repository-wide normalization pass.

## Maintenance law

Before creating a new intelligence standard or permanent document:

**SEARCH → COMPARE → DISTILL → UPDATE CURRENT AUTHORITY → RETIRE DUPLICATE → VERIFY**

The goal is fewer, stronger sources—not a larger document collection.
