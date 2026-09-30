# Architecture

**Brain-level status: PROPOSED pending Human-Director ratification. Individual files carry their own status declarations (see file headers).**

Owns system boundaries, component responsibilities, dependency order, canonical-source law, and architectural decisions. Architecture describes the organism; runtime implements it.

## Contents (4 files + this README = 5)

| File | Purpose |
|---|---|
| [0001-SYSTEM-BOUNDARIES-V1.md](./0001-SYSTEM-BOUNDARIES-V1.md) | What is inside vs. outside the system |
| [0002-DEPENDENCY-ORDER-V1.md](./0002-DEPENDENCY-ORDER-V1.md) | How components depend on each other |
| [0003-NINE-NODE-ORGANISM-MAP-V1.json](./0003-NINE-NODE-ORGANISM-MAP-V1.json) | Machine twin of the nine-node organism map |
| [0003-NINE-NODE-ORGANISM-MAP-V1.md](./0003-NINE-NODE-ORGANISM-MAP-V1.md) | Human twin of the nine-node organism map |

## Key Principles

- Clear system boundaries prevent scope creep
- Dependency order is explicit and acyclic
- Canonical source law: one owner per responsibility
