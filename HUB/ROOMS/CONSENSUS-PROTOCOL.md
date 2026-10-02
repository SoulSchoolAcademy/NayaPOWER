# 🔱 Hub Rooms — Consensus & Review Protocol

**Status:** ACTIVE REVIEW PROTOCOL  
**Coordination board:** GitHub Issue #554  
**Review PR:** #1290  
**Implementation issue:** #1270

## Purpose

Team Naya should not treat one builder's draft as final product truth.

Every room package is reviewable in GitHub. Builders, designers, verifiers and Codas should read the same files, comment with evidence, improve the proposal, score it, and converge before the room is locked for implementation.

## Canonical room package

Each primary room has one folder:

`HUB/ROOMS/<room>/`

Inside:

- `README.md` — one-page index/status.
- `FUNCTIONAL-SPEC.md` — canonical room behavior and causal requirements.
- `DESIGN-CONTRACT.md` — canonical room-specific visual/interaction contract.
- `SPEC.HUMAN.md` — human explanation.
- `SPEC.AI.md` — builder/Naya instructions.
- `SPEC.MACHINE.json` — deterministic machine projection.

**Conflict rule:** FUNCTIONAL-SPEC + DESIGN-CONTRACT + parent Hub contracts win over projections. Projections must be repaired if they drift.

## Source vs contract

Human Director notes and other inputs live under `HUB/ROOMS/SOURCES/`.

Source notes preserve intent. They do not silently override canonical architecture/runtime truth.

When a source and current system disagree:
1. name the disagreement;
2. cite/point to the evidence;
3. discuss it on #554 / PR;
4. resolve deliberately;
5. update the canonical contract;
6. keep the source note as history.

## Review stages

`SOURCE → DRAFT → TEAM REVIEW → CONSENSUS CANDIDATE → HUMAN DIRECTOR RATIFICATION → LOCKED FOR BUILD → IMPLEMENTED → INDEPENDENTLY VERIFIED → PRODUCTION-PROVEN`

Do not collapse these states.

## How Team Naya reviews

Reviewers should comment on PR #1290 and post material “not-right” findings to #554.

Use:

**[ROOM REVIEW] <room>**

- **Verdict:** SUPPORT / SUPPORT WITH CHANGES / OBJECT
- **Strongest part:**
- **Material hole:**
- **Evidence / file link:**
- **Proposed improvement:**
- **D1–D8 effect:**
- **Cross-room effect:**
- **Authority/privacy effect:**
- **One next action:**

Bare opinions are useful as taste input, but they do not close a gate.

## Consensus definition

Consensus does not mean everyone uses identical words.

A room reaches **CONSENSUS CANDIDATE** when:
- no unresolved material architecture/governance contradiction remains;
- the human purpose is unambiguous;
- room-specific design is distinctive and coherent with the Hub;
- primary controls and states are specified;
- data/runtime ownership is known or honestly marked unknown;
- cross-room handoffs preserve canonical object identity;
- independent reviewers have had a chance to challenge it;
- the canonical D1–D8 scorecard has no dimension below 9.0 at specification level;
- remaining unknowns are explicit.

Human Director ratification or merge then locks the design/build contract for the implementation rung.

## Improvement rule

Files are living project intelligence.

If a later design is provably better:
- update through a PR;
- explain what improves and what is preserved;
- attach evidence;
- update projections;
- supersede obsolete language rather than silently forking it.

Delete only when the content is truly obsolete and all inbound references are repaired.

## Shared five-layer room grammar

Every room must implement the Human Director's five-layer law:

1. **ORIENTATION** — Where am I?
2. **CURRENT STATE** — What is happening here now?
3. **INTELLIGENCE** — What does Naya understand?
4. **ACTION** — What can I actually do?
5. **PROOF** — Why should I trust it?

Visual implementation may express these as:
**HERO → INTELLIGENCE WALL → ACTION DECK → EVIDENCE LAYER → NAYA LAYER**, but the semantic five layers remain present.

## One-shell law

The sidebar is navigation. The center workspace is the room.

Opening a room should transform the center software experience while preserving the same Hub shell, Naya presence and global context unless a verified UX decision changes that rule.

## Exactly one next action

Independent Team Naya reviewers should score **Your Intelligence Today** first, then post SUPPORT / CHANGES / OBJECT on #1290 with evidence and any material findings on #554.
