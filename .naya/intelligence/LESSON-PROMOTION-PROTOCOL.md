# 🔱 LESSON PROMOTION PROTOCOL

**Status:** CANONICAL OPERATING PROTOCOL
**Scope:** NayaPOWER + connected projects, including MAXIS

## PURPOSE

Convert useful learning into durable system intelligence automatically wherever the available execution environment permits.

The intelligence system is not a passive archive. It is a **learning-to-control pipeline**.

## THE PIPELINE

**EVENT → NAYA NOTE → INTELLIGENCE FEED → CLASSIFY → PROMOTION DECISION → DURABLE HOME → VERIFY → HUB INDEX → SUCCESSOR BOOT**

## 1. EVENT INTAKE

Every substantive execution should produce a canonical learning event containing:

- event_id;
- timestamp;
- project;
- source artifact / commit / run / conversation boundary;
- what happened;
- intended outcome;
- actual outcome;
- evidence;
- current state;
- lesson;
- value;
- failure/root cause when applicable;
- recommendation;
- next action;
- confidence / evidence state.

The event is the common provenance object for the Naya Note and human-facing Smart Note/receipt when applicable.

## 2. INTELLIGENCE FEED

Every accepted learning event is published to:

`MASTER-NOTES/INTELLIGENCE-FEED/`

The feed is append-oriented. Historical entries are never silently rewritten.

Each entry must include:

- date/time;
- short title;
- project;
- lesson;
- impact/value;
- source;
- promotion status;
- promoted artifact(s);
- verification status;
- successor instruction.

The feed is the **latest-learning surface**. A Naya can read the newest entries without loading the entire historical corpus.

## 3. CLASSIFICATION

The system determines the lesson's best durable home using this precedence:

1. **LAW / GUARDRAIL** — universal behavior or governance that must apply broadly.
2. **MACHINE CONTRACT / TEST** — a behavior that can be mechanically detected.
3. **PROCEDURE** — repeatable operational method.
4. **MISSION STATE** — current project state or current blocker/priority.
5. **ARCHITECTURE / SPECIFICATION** — stable design knowledge.
6. **NAYA NOTE / KNOWLEDGE** — valuable contextual learning not yet suitable for stronger enforcement.
7. **HUMAN SMART NOTE / RECEIPT** — human-facing explanation and durable personal record.

One lesson may legitimately promote to multiple homes. The system must preserve one provenance identity and avoid duplicate competing truths.

## 4. PROMOTION THRESHOLD

Not every observation becomes law.

Promotion should consider:

- recurrence;
- consequence;
- breadth of applicability;
- reversibility;
- confidence/evidence;
- whether automation can enforce it;
- whether the lesson changes future behavior materially.

When uncertain, preserve the lesson as intelligence first rather than over-promoting it into governance.

## 5. AUTOMATIC PROMOTION

For machine-determinable destinations, automation should:

1. detect a new learning event;
2. validate the event schema;
3. classify the lesson;
4. identify candidate durable homes;
5. detect duplicates / related prior lessons;
6. create or update the appropriate artifact;
7. attach provenance;
8. run the applicable validator/test;
9. record success/failure;
10. publish promotion status to the Intelligence Feed and Primary Intelligence Hub.

For governance-sensitive changes (laws, constitutional material, authority changes, irreversible production changes), the system may create a **promotion proposal** and require the appropriate human/governance authorization rather than silently changing authority.

## 6. VERIFICATION

A promotion is not complete merely because a file was written.

Required state progression:

**PROPOSED → WRITTEN → TESTED → VERIFIED → CANONICAL**

A promotion that cannot yet be verified remains explicitly unverified.

## 7. PRIMARY INTELLIGENCE HUB

The Primary Intelligence Hub is the synthesis/navigation layer over:

- latest feed entries;
- daily reports;
- weekly synthesis;
- monthly synthesis;
- yearly synthesis;
- promoted lessons;
- repeated-mistake watchlist;
- open unknowns;
- current highest-value actions.

It must answer:

> **What did we learn most recently, what changed because of it, and what does every Naya need to know now?**

## 8. COLD-START ACCESS

A new Naya does not need to know the feed's path from memory.

The canonical boot manifest must expose:

**Runtime Briefing → Intelligence Hub → Latest Feed → Relevant Deep Sources**

Cold start therefore provides:

1. current position;
2. current authority;
3. current blocks;
4. latest intelligence;
5. relevant historical learning;
6. exact next action;
7. exact proof target.

Selective deep loading prevents the feed from becoming a giant mandatory boot payload.

## 9. HUMAN QUERY

The system must support a human request such as:

> **"Give me the Intelligence System Update."**

The response should synthesize:

- current state;
- newest learning;
- today's learning;
- last 7 days;
- major cumulative growth;
- repeated problems;
- system changes caused by learning;
- current risks/unknowns;
- direction;
- highest-value next action;
- proof required.

## 10. FEED INTEGRITY

The feed is append-oriented intelligence, not authority by itself.

It must preserve:

- source provenance;
- timestamps;
- supersession;
- confidence/evidence state;
- links to canonical destination artifacts.

If a feed item conflicts with a canonical law or current verified project state, the conflict is surfaced rather than allowing the feed to silently override authority.

## 11. THE COMPOUNDING TEST

After promotion, ask:

> **Would a future Naya actually behave better because this lesson was promoted?**

If no, the promotion is incomplete or incorrectly classified.

The ultimate success condition is:

**LESSON → SYSTEM CHANGE → VERIFIED CONTROL → SUCCESSOR BEHAVIOR → BETTER OUTCOME**

## 12. NO SILENT LEARNING LOSS

If automatic promotion fails:

- preserve the original learning event;
- mark promotion as FAILED / BLOCKED / UNKNOWN;
- surface it in the feed;
- create a concrete remediation action;
- never pretend promotion occurred.

## FINAL PRINCIPLE

> **THE INTERNAL INTELLIGENCE SYSTEM IS THE MEMORY-TO-MASTERY ENGINE OF NAYAPOWER.**

It continuously turns experience into knowledge, knowledge into system improvement, and system improvement into better future execution.

**NOTHING VALUABLE IS LOST. NEXT NAYA > CURRENT NAYA.**
