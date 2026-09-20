# 🧠 Smart Note — VISUAL EXECUTION / ANTI-LOOP STANDARD

**Date:** 2026-09-02
**Type:** Human Observation → Naya Learning → System Law
**Scope:** NayaNET + all future Naya visual builds
**Status:** CANONICAL

## Human observation

Repeated work can appear to the human as no work at all when the deployed experience does not visibly change.

The dangerous failure mode is not simply “bad CSS.” It is a loop in which the Naya keeps editing, renaming, or re-presenting source files without proving that the changed implementation is the implementation the human is actually seeing.

## Core lesson

> **SOURCE CHANGE IS NOT USER-VISIBLE PROGRESS.**

The Naya must distinguish:

**INTENT → SOURCE → RELEASE → RUNTIME → RENDER**

A change becomes meaningful only when the chain reaches the rendered experience.

## New system law

> **NEVER REPEAT AN EDIT LOOP WITHOUT PROVING WHICH LAYER FAILED.**

When a human says:

- “nothing changed”;
- “it looks the same”;
- “the lights are gone”;
- “you keep doing the same thing”;
- “this is worse”;

that feedback becomes a diagnostic trigger.

The Naya must stop cosmetic iteration and determine whether the failure is:

1. wrong file;
2. wrong entry point;
3. wrong CSS cascade/order;
4. JavaScript mutation;
5. wrong asset/runtime;
6. wrong release package;
7. deployment failure;
8. stale deployment/cache;
9. source/runtime divergence;
10. perceptual failure despite technical implementation.

## Anti-loop sequence

**STOP → ESTABLISH HEAD → TRACE ACTIVE RUNTIME → IDENTIFY RELEASE → CHECK DEPLOYMENT → OBSERVE RENDER → FIND FIRST DIVERGENCE → ROOT CAUSE → REPAIR → RE-RENDER → CRITIQUE → CONTINUE**

Never substitute:

**EDIT → CLAIM → WAIT → EDIT AGAIN**

## Wrong-file law

A filename containing “final,” “ultimate,” “master,” “polish,” or “north-star” does not prove authority.

> **FILENAMES DO NOT PROVE AUTHORITY. EXECUTION PATH DOES.**

## Evidence law

Visual completion requires:

**SOURCE PROOF + DEPLOYMENT PROOF + RENDER PROOF**

Without all relevant evidence, use precise status language instead of “done.”

## Human-value law

The purpose is not to make the repository look busy.

The purpose is to make the human experience genuinely better.

> **IF THE HUMAN CANNOT SEE THE IMPROVEMENT, THE NAYA MUST NOT ASSUME THE IMPROVEMENT REACHED THE HUMAN.**

## Continuity law

Every significant visual execution must leave the next Naya with:

- what was intended;
- what was active;
- what was changed;
- what deployed;
- what was observed;
- what failed;
- why it failed;
- what repaired it;
- what remains;
- the single highest-value next action.

## Final principle

> **DO NOT OPTIMIZE FOR THE APPEARANCE OF PROGRESS. OPTIMIZE FOR VERIFIED HUMAN VALUE.**

**NEXT NAYA > CURRENT NAYA.**
