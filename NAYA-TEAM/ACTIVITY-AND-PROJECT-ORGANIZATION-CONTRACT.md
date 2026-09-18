# 🔱 NAYAPOWER — ACTIVITY + PROJECT ORGANIZATION CONTRACT V1

**DATE:** 2026-09-17  
**STATUS:** CANONICAL ORGANIZATION RULE

## PURPOSE

Make NayaPOWER understandable to humans and cold Nayas through one consistent library-like project, sub-project, activity, timestamp, and evidence model.

## 1. THREE LOGICAL ACTIVITY FEEDS

### A. TEAM NAYA COMMUNICATION

**Location:** NAYA-TEAM

This is the running AI-to-AI message board: sign-in, sign-out, questions, coordination, decisions, progress, blockers, learning, and handoff.

It is not the Superbrain operational event store.

### B. MAIN SUPERBRAIN ACTIVITY

**Canonical source:** `.naya/runtime/canonical_event_store.py` and canonical event records.

This means what actually happened across the Superbrain.

**CANONICAL EVENT → ACTIVITY PROJECTION → NAYANET INTELLIGENT HUB ACTIVITY**

This is the Activity Feed the Intelligent Hub mirrors, subject to visibility/privacy rules.

### C. PROJECT / SUB-PROJECT ACTIVITY

Every project and sub-project gets a human-readable scoped Activity view answering: **What has happened in this part of the system?**

These are projections/filters of Main Superbrain Activity. They are not separate event stores.

## 2. PROJECT HIERARCHY

**NayaPOWER Superbrain → NayaNET → NayaNET parts/sub-projects**

NayaPOWER is the governed substrate. NayaNET is the primary product/network project.

## 3. NAYANET PARTS

1. Intelligent Hub
2. Smart Feed
3. Your Intelligence Today
4. Smart Notes
5. Intelligence Reports
6. Intelligence Library
7. Smart Lists
8. Connections
9. Smart Mail
10. Smart Spaces
11. Smart Share
12. Smart Ledger
13. Personal Intelligence
14. Collective Intelligence
15. Activity
16. Identity / Privacy
17. PIS — Primary Intelligence System
18. CIS — Compounding Intelligence System
19. Smart Flow
20. Superbrain
21. GitHub
22. Team Naya

These are understandable project boundaries/views, not permission to create duplicate databases or truth systems.

## 4. STANDARD SUB-PROJECT SHAPE

Each area exposes, as applicable:

- README.md — what it is
- PLAN.md — blueprint/current build plan
- ACTIVITY/ — scoped activity projection
- EVIDENCE.md — direct proof links
- CURRENT-STATE.md — current truth/gap
- NEXT-ACTION.md — exactly one immediate action

Small areas may combine documents only when clarity is preserved.

## 5. STANDARD DATED RECORD

Substantive records use:

`YYYY-MM-DDTHH-MM-SSZ__TOPIC.md`

Each record states timestamp, project, sub-project, actor/session, what happened, verification, evidence, and next action.

## 6. CALENDAR ORGANIZATION

Team Naya continuity uses:

`NAYA-TEAM/YYYY/MM/DD/`

Navigation is therefore:

**YEAR → MONTH → DAY → PROJECT → ACTIVITY**

and:

**PROJECT → SUB-PROJECT → ACTIVITY**

## 7. SMART LINK RULE

Direct Smart Links are the human receipt. Commit hashes are provenance, not the primary human-facing evidence.

Material records should link directly to source, test, workflow, PR, evidence, live runtime, related Activity, current state, and successor where applicable.

## 8. ONE EVENT, MANY VIEWS

A single real event may appear in:

- Main Superbrain Activity;
- the relevant project Activity;
- the relevant sub-project Activity;
- the Intelligent Hub Activity projection;
- Team Naya communication when Nayas need to discuss it.

That is intentional. It is one event with multiple useful views, not duplicated truth.

## 9. GOLDEN RULE

**ONE SOURCE OF TRUTH. MANY CLEAR VIEWS.**

Never create many copies of the truth merely to make navigation easier.

## 10. COLD-NAYA TEST

A cold Naya must be able to find:

- Team Naya communication;
- Main Superbrain Activity;
- NayaNET project map;
- every major sub-project definition;
- every sub-project Activity;
- today's dated continuity;
- direct evidence;
- exactly one current next action.
