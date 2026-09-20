# Repository Relationship Index

**STATUS:** DERIVED NAVIGATION PROJECTION V1  
**SOURCE TREE:** 950c103bd883630779aec42c0527d18f1f7ffb94

This is a derived repository map, not a database, memory system, event store, or authority source.

## What it gives a Naya

**RECORD → PROJECT → SUB-PROJECT → RELATED RECORDS → STATE / EVIDENCE → SUCCESSOR**

## Coverage

- Repository files indexed: **2038**
- Explicit structural relationships: **18**
- NayaNET project areas recognized: **19**
- Source records remain authoritative.
- The index is disposable and regenerable.

## Node classes

- **ACTIVITY** — 71
- **CONTROL_PLANE** — 29
- **EVENT** — 69
- **GOVERNANCE** — 13
- **OTHER** — 1528
- **PROJECT** — 3
- **RUNTIME** — 107
- **SMART_NOTE** — 133
- **SOURCE** — 1
- **SUBPROJECT** — 19
- **TEAM_NAYA** — 32
- **TEST** — 24
- **WORKFLOW** — 9

## Relationship law

**ONE RECORD → MANY EXPLICIT LINKS → ONE CANONICAL TRUTH.**

This first pass deliberately uses conservative structural relationships. It does not manufacture semantic relationships from similar names. Future explicit relationship metadata can be indexed without changing the underlying record system.

## Canonical truth remains in

- .naya/control-plane/STATE.json
- .naya/control-plane/BLOCKS.json
- .naya/control-plane/MAP.json
- .naya/control-plane/PROOF.json
- .naya/governance/
- .naya/memory/events/
- SUPERBRAIN/NAYA-ACTIVITY/
- NAYA-TEAM/PROJECTS/NAYANET/

## Regeneration

Run:

python scripts/build_repository_relationship_index.py

## Acceptance

A cold Naya should be able to start from an indexed record, identify its project/sub-project boundary where one exists, follow canonical sources, and distinguish the index from authority and evidence.

**Law:** one repository • one current truth • one event substrate • many useful views • one next action.
