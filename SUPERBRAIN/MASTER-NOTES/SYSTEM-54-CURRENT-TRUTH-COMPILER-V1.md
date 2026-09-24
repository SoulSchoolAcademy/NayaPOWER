# Current-Truth Compiler V1

**System 54 — Current-Truth Compiler**

## Purpose

Produce one compact generated cold-boot artifact containing who we are, what we are building, current architecture, current state, proven boundaries, unknown/blocked/stale signals, authority, current mission, and one next action.

## Authority

`CURRENT-TRUTH.md` is **DERIVED**. It never outranks the constitution, live repository identity, canonical control-plane sources, or live runtime evidence.

The compiler exposes conflicts instead of resolving them by guessing.

## Generation

`node scripts/build-current-truth.mjs`

Freshness check:

`node scripts/build-current-truth.mjs --check`

## Completion gate

System 54 requires deterministic generation, live HEAD resolution, explicit current/proven/unknown/blocked/authority/next-action sections, conflict detection without silent guessing, freshness checking, and CI enforcement.

This first implementation establishes the canonical generator and artifact contract; CI enforcement is the next verification step.