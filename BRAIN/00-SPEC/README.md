# Brain Specification

**Brain-level status: PROPOSED pending Human-Director ratification. Individual files carry their own status declarations (see file headers).**

This directory contains the specifications that define the canonical brain tree, graph, naming, representation, and population laws.

> **Reconciliation note (2026-09-30):** two vocabulary drifts are documented here, not resolved — the Human Director owns the decision:
> 1. `BRAIN-MACHINE-CONTRACT-V1.schema.json` declares a 6-value `epistemicState` enum while `0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md` §8 and `SCHEMA/PROOF-RECORD-SCHEMA.json` declare a 14-value enum. Both are preserved as written.
> 2. The machine contract's `canonicalStatus` lacks the `CANONICAL` terminal state used by `0004-KNOWLEDGE-POPULATION-SPEC-V1.md`, `0001` §19, and `01-GOVERNANCE/0002-PROMOTION-AND-REVOCATION-V1.md`. Both are preserved as written.

## Contents (14 files + this README = 15)

| File | Purpose |
|---|---|
| [0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md](./0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md) | Master specification for graph, tree, object model |
| [0002-TREE-AND-GRAPH-NAMING-LAW-V1.md](./0002-TREE-AND-GRAPH-NAMING-LAW-V1.md) | Naming conventions and addressing |
| [0003-REPRESENTATION-LAW-V1.md](./0003-REPRESENTATION-LAW-V1.md) | Human/AI/machine representation law |
| [0004-KNOWLEDGE-POPULATION-SPEC-V1.md](./0004-KNOWLEDGE-POPULATION-SPEC-V1.md) | How knowledge enters the canonical graph |
| [0005-TREE-V1.md](./0005-TREE-V1.md) | Tree structure specification |
| [0006-NIA-LANGUAGE-INTENT-CONTRACT-V1.md](./0006-NIA-LANGUAGE-INTENT-CONTRACT-V1.md) | NIA language intent contract (ratified 2026-09-29) |
| [0006-OBJECT-TYPES-V1.md](./0006-OBJECT-TYPES-V1.md) | Canonical object type definitions |
| [BRAIN-MACHINE-CONTRACT-V1.schema.json](./BRAIN-MACHINE-CONTRACT-V1.schema.json) | Machine contract schema (see reconciliation note) |
| [NIA-LANGUAGE-INTENT-V1.json](./NIA-LANGUAGE-INTENT-V1.json) | Machine twin of the NIA intent contract |
| [SCHEMA/AUTHORITY-TUPLE-SCHEMA.json](./SCHEMA/AUTHORITY-TUPLE-SCHEMA.json) | Authority tuple schema |
| [SCHEMA/GRAPH-QUERY-SCHEMA.json](./SCHEMA/GRAPH-QUERY-SCHEMA.json) | Graph query schema |
| [SCHEMA/LEARNING-RECORD-SCHEMA.json](./SCHEMA/LEARNING-RECORD-SCHEMA.json) | Learning record schema |
| [SCHEMA/PROOF-RECORD-SCHEMA.json](./SCHEMA/PROOF-RECORD-SCHEMA.json) | Proof record schema (14-state epistemic enum) |
| [SCHEMA/SUCCESSOR-PACKAGE-SCHEMA.json](./SCHEMA/SUCCESSOR-PACKAGE-SCHEMA.json) | Successor package schema |

## Key Concepts

- One brain, one canonical semantic model
- Tree is navigation; graph is relationships; objects are meaning
- Five-dimensional architecture: TREE, IDENTITY, GRAPH, CONTRACT, PROOF
- 22 canonical relationship types
- 31 knowledge types with separate epistemic states
