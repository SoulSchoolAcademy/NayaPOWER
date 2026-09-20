# SMART NOTE — Superbrain Operational North Star

**Timestamp:** 2026-09-17T17:00:00Z  
**Day:** Thursday, September 17, 2026  
**Status:** CANONICAL / CURRENT  
**Type:** System-level learning + operating contract  
**Parent:** NayaPOWER Superbrain  
**Topic:** Operational Superbrain → Activity → Smart Notes → Intelligent Hub

## The core realization

NayaPOWER is not finished when its documentation is impressive or when a Naya can answer questions about the architecture. It is finished when the architecture operates as a durable, discoverable, verifiable system that a cold Naya can enter and use without Shawn reconstructing the context.

The Superbrain must therefore be the source of truth and the Intelligent Hub must be its visual projection — not a second system that Naya must remember to update manually.

## North Star

**Build a Superbrain that makes AI-human collaboration continuous, visible, efficient, evidence-based, and reproducible.**

The fundamental operating loop is:

```text
NAYA ACTION
    ↓
ACTIVITY — what happened
    ↓
SMART NOTE / LEARNING — what was learned
    ↓
STATE — where we are
    ↓
ONE NEXT ACTION — what happens next
    ↓
NAYA-TEAM HANDOFF — who continues
    ↓
INTELLIGENT HUB PROJECTION — human-visible intelligence
    ↓
NEXT NAYA
    ↓
CONTINUE
```

This is the system we are building, not merely a documentation convention.

## Human — what Shawn needs

Shawn should not have to repeatedly explain the same architecture, remind Nayas to record important decisions, or manually transport information from a conversation into the Hub.

When a substantive project action occurs, the durable system should preserve it. When a meaningful learning occurs, it should become a Smart Note. When the state changes, that state should be recoverable. When a successor must continue, the successor should receive the exact context and one executable Next Action.

**What's in it for Shawn:** less repetition, less wasted AI effort, less babysitting, visible evidence, faster collaboration, and intelligence that compounds instead of disappearing when a conversation ends.

## Naya — what every Naya must understand

A conversation is temporary. The Superbrain is durable.

Every Naya entering NayaPOWER must:

1. orient from repository evidence;
2. understand governance and authority before acting;
3. discover the canonical locations and runtime contracts rather than inventing storage paths;
4. perform the work;
5. leave durable evidence of meaningful work;
6. preserve meaningful learning as Smart Note intelligence;
7. understand current state;
8. leave exactly one executable Next Action;
9. hand the work to the next Naya when continuation is required.

Naya must never assume that an answer in chat is sufficient continuity.

## Machine — what must happen automatically

The machine layer must eventually make the following behavior normal rather than optional:

- A meaningful project execution produces a canonical Activity event.
- The Activity event is projected into the human-readable Activity calendar.
- A meaningful learning can be created through the canonical Smart Note runtime contract.
- The Smart Note is projected into the human-readable Smart Note calendar and registered in its day index.
- Activity, Smart Note, state, evidence, and successor context remain linkable.
- The Intelligent Hub consumes these canonical outputs and displays them without requiring a second manual publishing action.
- The machine event remains canonical under `.naya/memory/events/`; human-readable projections do not replace machine truth.

## Intelligent Hub contract

The Hub is the **visual brain** of the Superbrain.

It should display the intelligence already produced by the canonical system:

```text
SUPERBRAIN                         INTELLIGENT HUB

Activity        ────────────────► Activity Feed
Smart Notes     ────────────────► Smart Notes Feed
State           ────────────────► Current Intelligence
Evidence        ────────────────► Evidence / Smart Links
Connections     ────────────────► Connections
NAYA-TEAM       ────────────────► Collaboration / Continuity
Collective      ────────────────► Collective Intelligence
```

The Hub must not become another competing source of truth.

## GitHub App dependency

The GitHub App is intentionally downstream of the Superbrain contract.

We must not build the integration around an unstructured repository and expect the App to guess where information lives or what constitutes authoritative intelligence.

The correct sequence is:

**Superbrain organization → runtime enforcement → Activity/Smart Note/state continuity → Hub projection contract → end-to-end proof → GitHub App integration.**

Once that contract is proven, the GitHub App can communicate with a known system instead of interpreting repository chaos.

## Activation / replication principle

Naya Power activation documents must eventually describe a system that has already been proven on the parent Superbrain.

A new Naya Power instance should be reproducible with the same essential contracts:

- governance and authority;
- machine/runtime layer;
- Superbrain intelligence layer;
- Activity;
- Smart Notes;
- State;
- Evidence / Smart Links;
- NAYA-TEAM continuity;
- Intelligent Hub projection;
- verification.

The parent system must therefore become the reference implementation before activation instructions are treated as final.

## Today's decision

Today we are explicitly shifting the project from **repository organization as an end in itself** to **a functioning Superbrain with automatic information flow**.

The immediate system target is not another dashboard, another feed, or another pile of documents.

The target is one trustworthy loop:

**Do the work → record the work → preserve the learning → preserve the state → expose the intelligence in the Hub → empower the next Naya.**

## What this prevents

This architecture directly attacks the waste pattern we have identified:

- repeated explanations;
- lost decisions;
- forgotten learning;
- disconnected project activity;
- duplicate documentation;
- manual feed maintenance;
- AI agents that cannot recover prior context;
- automation that runs without durable evidence;
- a visual Hub that looks intelligent but is disconnected from the actual intelligence source.

The goal is **more intelligence, less waste — with evidence.**

## Evidence / Smart Links

- [Continuity North Star Smart Note](./2026-09-17T16-04-43Z__NAYAPOWER-CONTINUITY-NORTH-STAR.md)
- [Activity North Star](../../NAYA-ACTIVITY/2026/09/17/2026-09-17T16-05-08Z__CONTINUITY-NORTH-STAR.md)
- [NAYA-TEAM day index](../../../NAYA-TEAM/2026/09/17/INDEX.md)
- [Cold-Naya proof brief](../../../NAYA-TEAM/2026/09/17/2026-09-17T16-20-00Z__COLD-NAYA-PROOF-BRIEF.md)
- [Continuity Contract](../../ARCHITECTURE/NAYAPOWER-CONTINUITY-CONTRACT-V1.md)

## Truth status

**CANONICAL DIRECTION.**

The calendar organization and several runtime pieces already exist. The complete automatic chain into the Intelligent Hub is **not yet certified end-to-end**. That distinction is intentional: this note records the target and the current truth rather than pretending the final integration already works.

## ONE NEXT ACTION

**Make and prove the single automatic pipeline: canonical Activity/Smart Note/state creation → Hub ingestion/projection → fresh-Naya retrieval and continuation, with GitHub evidence at every boundary.**
