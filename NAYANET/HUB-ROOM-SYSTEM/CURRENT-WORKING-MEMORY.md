# CURRENT WORKING MEMORY — Hub Room System

**Purpose:** Durable working memory for the active Hub sub-project. This file captures high-value decisions, discoveries, design reasoning, corrections, and unresolved questions from active human–Naya work so they remain recallable after the conversation ends.

## Why this exists

Conversation is a working surface, not a durable source of project truth. Valuable reasoning must be distilled into GitHub where a future Naya, decoder, implementer, or human can recover it without reconstructing the conversation.

This is **not a generic meeting-notes file**. It is an organized intelligence layer for the current sub-project.

## Project position

```
NayaNET / NayaPOWER
└── NAYANET
    └── HUB
        └── HUB-ROOM-SYSTEM
            ├── Room contracts
            ├── Registry / freeze state
            └── CURRENT-WORKING-MEMORY.md  ← active sub-project memory
```

The Hub is itself a sub-project within NayaPOWER/NayaNET. Each Hub room is a sub-project within the Hub. A room can contain further bounded workstreams.

## Memory hierarchy

1. **System truth** — architecture, governance, source-of-truth rules.
2. **Project truth** — Hub shell, runtime, release/proof contracts.
3. **Room truth** — the room's durable Product + UX + Intelligence Contract.
4. **Working memory** — active discoveries, decisions, design reasoning, corrections, questions, and next actions for the current room.
5. **Evidence** — source SHAs, proof runs, artifacts, runtime observations, and receipts.

Working memory informs implementation; it does not override canonical source or verified evidence.

## Current active work

**Room:** 01 — Your Intelligence Today  
**Stage:** Contract deepening before implementation  
**Operating rule:** Do not code until the Product + UX + Intelligence Contract is sufficiently explicit to prevent guesswork.

## Durable decisions from the current design conversation

### 1. The room is an application, not a page
The sidebar is navigation. Clicking a room transforms the Hub's middle workspace into that room's software. The Hub shell remains intact.

### 2. The middle workspace is the primary canvas
The room should use the available center width beneath the persistent search/header. A permanent full-height Naya right rail is not required. Any shell-level change to reclaim right-rail space is a separate bounded task and must not be mixed into Room 01 implementation.

### 3. Your Intelligence Today is a Daily Intelligence Cockpit
It should answer useful human questions, not merely display cards:
- What happened?
- What did I learn?
- What changed?
- What matters now?
- What should I remember?
- What am I missing?
- What can I do about it?

### 4. Every element must earn its place
A room element must materially help the user **CAPTURE, UNDERSTAND, REMEMBER, CONNECT, DECIDE, ACT, or VERIFY**. Decorative elements without utility are not justified.

### 5. “What Changed?” is a core intelligence function
The room should distinguish current intelligence from the prior daily boundary where evidence permits. It should surface meaningful changes, not simply list recent records.

### 6. “What did I learn?” is not the same as “what information exists?”
The room should distinguish, where evidence supports it, between information captured, understanding gained, a change in state, a decision made, and durable knowledge worth retaining.

### 7. “What matters now?” must be evidence-grounded
Potentially important unresolved questions, blocked work, discoveries, decisions, opportunities, commitments, or awaiting-human-action states may be surfaced only when supported by available evidence. Unknown remains unknown.

### 8. “What am I missing?” is a feature, not a failure
The room should expose meaningful gaps in knowledge or verification using explicit states such as KNOWN / CHANGED / UNCERTAIN / MISSING. It must not fill gaps with invented certainty.

### 9. Naya's synthesis is interpretation, not fabricated truth
Naya may explain significance, uncertainty, and attention based on observed intelligence. Observed facts and Naya interpretation must remain distinguishable.

### 10. The Intelligence Diary is human-centered
The room is about the person's intelligence today: what they experienced, learned, created, understood, decided, corrected, gave, and what happened because of it.

## Working memory protocol

During active work, whenever a conversation produces a durable design decision, important discovery, correction, rejected approach, evidence-backed constraint, or unresolved question, it should be distilled here **without requiring the human to explicitly say “take a note.”**

Use the smallest useful durable entry:
- **Decision** — what is now true by agreement.
- **Reason** — why it matters.
- **Evidence** — source/proof when available.
- **Impact** — what future work must preserve.
- **Open question** — only if genuinely unresolved.
- **Next action** — the bounded action that follows.

Do not dump entire conversations. Distill intelligence.

## Retrieval protocol for any future Naya

Before acting on this sub-project:

1. Read this file.
2. Read `ROOM-REGISTRY.md`.
3. Read the target room contract.
4. Inspect current implementation and current proof/evidence.
5. Treat verified evidence as stronger than remembered conversation.
6. Preserve frozen rooms and prior decisions unless an explicit new decision supersedes them.
7. If new conversation changes the design, update working memory and the relevant contract before implementation when practical.

## Current next action

Deepen `01-YOUR-INTELLIGENCE-TODAY.md` into the full Product + UX + Intelligence Contract, then implement only against that contract.
