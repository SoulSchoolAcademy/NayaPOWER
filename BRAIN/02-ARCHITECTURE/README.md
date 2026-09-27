# Architecture

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

Owns system boundaries, component responsibilities, dependency order, canonical-source law, and architectural decisions. Architecture describes the organism; runtime implements it.

## Contents

| File | Purpose |
|---|---|
| [0001-SYSTEM-BOUNDARIES-V1.md](./0001-SYSTEM-BOUNDARIES-V1.md) | What is inside vs. outside the system |
| [0002-DEPENDENCY-ORDER-V1.md](./0002-DEPENDENCY-ORDER-V1.md) | How components depend on each other |

## Key Principles

- Clear system boundaries prevent scope creep
- Dependency order is explicit and acyclic
- Canonical source law: one owner per responsibility
- Architecture is proposed until human ratification
