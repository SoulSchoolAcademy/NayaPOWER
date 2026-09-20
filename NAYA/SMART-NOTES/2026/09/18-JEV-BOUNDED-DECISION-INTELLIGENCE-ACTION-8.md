# Smart Note — Jev / System-One-Style Bounded Decision Intelligence

**Date:** 2026-09-18  
**Status:** Architecture candidate — evaluation only  
**Scope:** Team Naya Action 8 — Governed Next-Action Selector

## Core observation

A Jev/System-One-style architecture separates bounded decision operations from general-purpose generative reasoning.

The relevant primitives are:

- **Choice:** select from an explicitly bounded candidate set.
- **Score:** evaluate against a defined rubric.
- **Probability/confidence:** expose uncertainty rather than presenting a recommendation as unquestionable truth.

## NayaPOWER application

This pattern may be useful for Action 8 because the selector already has a constrained responsibility:

**recommend exactly one current next action from authorized candidate work.**

Potential pipeline:

**STATE → CANDIDATES → BOUNDED DECISION → POLICY/AUTHORITY → AUTHORIZED EXECUTION → OBSERVE → VERIFY → LEDGER/ACTIVITY**

## Constitutional boundary

The bounded decision layer is a recommendation mechanism, not an authority mechanism.

It must never:

- grant authority;
- authorize itself;
- bypass the policy/permission engine;
- invoke consequential tools directly;
- turn confidence into permission;
- replace independent verification;
- become the canonical source of truth.

This preserves the NayaPOWER law:

**Capability does not create authority.**

## Evaluation requirements

Before adoption, test a vendor-neutral contract against:

1. responsible verified value;
2. risk;
3. authority;
4. dependency;
5. reversibility;
6. resource cost;
7. leverage;
8. continuity;
9. exactly one current recommendation.

Adversarial tests must include:

- confidently wrong recommendations;
- stale state;
- manipulated candidate data;
- unauthorized candidates;
- tied candidates;
- invalid/empty candidate sets;
- missing evidence;
- revoked authority;
- policy conflicts.

## Adoption rule

Jev should be treated as **one possible implementation behind a stable NayaPOWER interface**, not as a dependency or source of authority.

The first engineering artifact should therefore be the vendor-neutral bounded-decision contract. A Jev-backed adapter can be evaluated afterward against deterministic holdout and adversarial tests.

## Continuation

**Naya Runtime / Naya Oscar:** define and independently challenge the smallest bounded-decision contract for Action 8.

No adoption claim until the contract demonstrates improved decision quality without weakening authority, receipts, independent verification, or continuity.

**Maximum Responsible Verified Value per Action and Moment.**
