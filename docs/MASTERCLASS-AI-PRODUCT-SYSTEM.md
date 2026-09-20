# AI PRODUCT SYSTEM — MASTERCLASS REFERENCE

This document turns the MAXESS reference experience into a reusable operating system for building extraordinary AI-assisted products.

## The simplest explanation

Tell AI what you want.
Let AI define what must be true.
Store the definition.
Build it.
Test it.
Fix the biggest gaps.
Protect what already works.
Repeat until no important problem remains.
Then ship it.

## The two modes

### CREATE MODE
Use for writing, images, video scripts, posts, presentations, and other mostly self-contained outputs.

KNOW → TELL → ASK → CREATE → SCORE → IMPROVE → VERIFY → SHIP

### BUILD MODE
Use for websites, apps, interactive pages, software, and systems.

DEFINE → MAP → BUILD → RUN → VERIFY → IMPROVE → REGRESS → FREEZE → SHIP

## The AI does the definition work

The human supplies vision, audience, purpose, taste, examples, constraints, and desired outcome.

AI must answer all project-definition questions it can answer from available context. It asks the human only about material unknowns that can change the outcome.

## Project memory

Every software project should maintain durable memory outside the conversation.

Minimum memory set:
- vision;
- north star;
- user and use cases;
- definition of 10;
- information architecture;
- design system;
- component map;
- data contract;
- interaction contract;
- responsive contract;
- accessibility contract;
- performance/release requirements;
- change ledger;
- test matrix;
- decision log;
- smart notes;
- current progress/state.

GitHub is one recommended durable memory layer.

## The master build sequence

1. SHARE VISION
2. SELF-DEFINE PROJECT
3. DEFINE AAA / 10
4. CREATE PROJECT MEMORY
5. MAP SECTIONS + COMPONENTS
6. BUILD A WORKING FIRST VERSION
7. VERIFY CORE FUNCTION
8. SCORE THE SYSTEM
9. IDENTIFY THE HIGHEST-VALUE GAPS
10. FIX THE GAP SET
11. REGRESSION TEST
12. FREEZE VERIFIED AREAS
13. UPDATE SMART NOTES / CHANGE LEDGER
14. REPEAT
15. HUMAN REVIEW
16. RELEASE

## Change ledger principle

Never rely on conversational memory for requested changes.

Every material request becomes a tracked requirement with a status and acceptance criteria.

A change is not complete because code was written. It is complete because the requirement has evidence.

## Preservation principle

PRESERVE WHAT WORKS.
REPAIR WHAT DOESN’T.
RESTRUCTURE WHAT IS WRONG.
INTEGRATE WHAT IS MISSING.
REMOVE ONLY WHEN PROVEN SAFE.

A requested change must not silently reopen or damage unrelated completed work.

## 10-point rule

“Why is this not a 10?” is a diagnostic question, not a finish button.

The correct response is:
1. identify the highest-value remaining weaknesses;
2. convert them into explicit requirements;
3. fix them;
4. verify them;
5. regression-test the rest;
6. repeat.

## Completion rule

A product is not complete because:
- it looks impressive;
- the AI says it is done;
- tests pass;
- the line count increased;
- a newer file exists.

It is complete when its Definition of 10 is satisfied and the real-world release path is verified.

## Why this system exists

The failure mode we are eliminating is:

CONVERSATION → CONTEXT LOSS → REINTERPRETATION → PARTIAL PATCH → REGRESSION → MORE CONVERSATION → LOOP

The intended system is:

VISION → CONTRACT → MEMORY → IMPLEMENTATION → EVIDENCE → FREEZE → NEXT GAP → SHIP

## Daily product target

The operating objective is to make one meaningful product increment shippable in one focused working session whenever the project scope allows it.

Speed comes from persistent context and clear ownership, not from skipping quality.

## Principle

The human is the director.
AI is the engine.
The repository is the memory.
The contract is the shared understanding.
The scorecard is the judge.
Verification is the proof.
The ship is the result.
