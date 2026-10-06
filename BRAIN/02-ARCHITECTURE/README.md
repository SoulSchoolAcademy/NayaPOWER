# Architecture

**Brain-level status: PROPOSED pending Human-Director ratification. Individual files carry their own status declarations (see file headers).**

Owns system boundaries, component responsibilities, dependency order, canonical-source law, and architectural decisions. Architecture describes the organism; runtime implements it.

## Contents (10 files + this README = 11)

| File | Purpose |
|---|---|
| [0001-SYSTEM-BOUNDARIES-V1.md](./0001-SYSTEM-BOUNDARIES-V1.md) | What is inside vs. outside the system |
| [0002-DEPENDENCY-ORDER-V1.md](./0002-DEPENDENCY-ORDER-V1.md) | How components depend on each other |
| [0003-NINE-NODE-ORGANISM-MAP-V1.json](./0003-NINE-NODE-ORGANISM-MAP-V1.json) | Machine twin of the nine-node organism map |
| [0003-NINE-NODE-ORGANISM-MAP-V1.md](./0003-NINE-NODE-ORGANISM-MAP-V1.md) | Human twin of the nine-node organism map |
| [0004-DEEP-SYSTEM-MODEL-V1.human.md](./0004-DEEP-SYSTEM-MODEL-V1.human.md) / [.ai.md](./0004-DEEP-SYSTEM-MODEL-V1.ai.md) / [.machine.json](./0004-deep-system-model-v1.machine.json) | The missing mid-layer: 6 machines, 3 loops, 10 engineering primitives, phases 0–6 build order with the understanding test (PROPOSED) |
| [0005-PROVENANCE-CHAIN-EXTENSION-V1.human.md](./0005-PROVENANCE-CHAIN-EXTENSION-V1.human.md) / [.ai.md](./0005-PROVENANCE-CHAIN-EXTENSION-V1.ai.md) / [.machine.json](./0005-provenance-chain-extension-v1.machine.json) | Proposed ACT/LAW extension: PROVENANCE inserted into the action chain — the chain-of-authority fix (PROPOSED) |

## Key Principles

- Clear system boundaries prevent scope creep
- Dependency order is explicit and acyclic
- Canonical source law: one owner per responsibility
