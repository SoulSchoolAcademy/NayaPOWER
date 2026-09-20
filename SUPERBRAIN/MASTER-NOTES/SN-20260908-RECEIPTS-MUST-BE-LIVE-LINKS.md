# Smart Note — Execution Receipts Must Be Live Links

**Date:** 2026-09-08
**Status:** LOCKED OPERATING RULE

## The lesson
When Naya executes product/code/deployment work, the useful receipt for the human is not an internal commit hash or other opaque implementation identifier.

The receipt must prove the actual outcome in the place the human cares about.

## Receipt standard
For completed execution, Naya should provide:

1. **LIVE VIEW LINK** — the exact public/runtime URL where the user can see the result.
2. **VERIFICATION LINK** — a direct link that helps independently verify the deployed/updated state when useful.
3. **PLAIN STATUS** — DONE, NOT DONE, or BLOCKED.
4. **NO CLAIM WITHOUT PROOF** — do not say DONE until the live/runtime result has actually been verified.

Internal commit IDs, SHAs, workflow IDs, deployment IDs, and similar numbers are implementation evidence only. They should not be presented as the primary receipt unless the user explicitly asks for technical internals.

## Product execution consequence
The human wants to be productive and should not have to interpret engineering machinery to know whether an outcome was achieved. Naya owns the execution and verification burden.

**Human defines the outcome. Naya owns the execution. The runtime proves the delivery.**

## Current Intelligent Hub visual law
The NayaNET Intelligent Hub is a full-screen feed experience:

- LEFT: navigation on desktop/widescreen.
- CENTER: the Intelligent Feed / Intelligence Library using all remaining width.
- RIGHT: **NO SIDEBAR / NO RIGHT RAIL.**
- Existing/legacy Smart Notes must not be compressed into a right-side rail.
- Mobile: **NO PERMANENT SIDEBARS.** The feed should use essentially the full screen, with navigation accessible through a compact control such as a menu/plus button when needed.
- The three feed views should share the same premium full-page presentation.

## Why
The old right-side Smart Notes treatment creates a cramped, cluttered, legacy-dashboard appearance and contradicts the intended premium Intelligent Library experience.

The desired experience is:

**LEFT NAV → FULL-WIDTH INTELLIGENT FEED**

not:

**LEFT NAV → FEED → RIGHT SMART-NOTES SIDEBAR**

This is a product/layout law, not a cosmetic preference.

## Execution priority
Before moving to additional Hub improvements, remove the right sidebar/right rail from the actual authoritative source, build, deployment, and exact public runtime, then verify the live experience.

**Source → Build → Deployment → Exact Public Runtime → Human-visible proof.**

The live link is the receipt.
