# Naya Note — MAXESS Results Rebuild Decision

**Created:** 2026-08-18  
**Category:** Decision / Learning / Insight  
**Project:** MAXESS Results + Naya Nitro  
**Status:** Active / Authoritative

## What we learned

The current approximately 8,000-line Results artifact is not valuable because it is large. Its value is in the proven ideas it contains — especially the MAXESS orb/reveal concept, visual language, effects, interactions, and any implementation patterns worth recovering.

Trying to preserve and edit the entire artifact as one object is likely to create unnecessary context load, regression risk, and implementation drag.

## Decision

Rebuild the MAXESS Results experience **section by section and module by module**.

Do not treat the old large file as the default editing surface.

Use it as a historical/reference source and selectively recover superior pieces when justified.

## First implementation target

**Section 01 — MAXESS Orb / Reveal**

The orb is the strongest proven visual idea to carry forward. The new version should improve dimensionality, orbiting motion, color transitions, glow, responsive behavior, reduced-motion handling, and its connection to the personalized score/result.

## Connected product flow

`maxess.nayanet.xyz` = assessment/questionnaire  
`results.nayanet.xyz` = Results experience  
`nayanet.xyz` = NayaNET ecosystem/brand reference

The Results experience must remain connected to the authoritative MAXESS assessment result contract rather than inventing its own scores.

## Architecture

**FOUNDATION → COMPONENTS → SECTIONS → PAGES → EXPERIENCES**

Execution:

**MAP → DEFINE SECTION → BUILD → PREVIEW → SCORE → IMPROVE → VERIFY → FREEZE → NEXT**

## Naya Nitro lesson

Naya must proactively recommend this approach rather than waiting for the user to discover it.

If a user proposes a risky whole-file edit, Naya should say:

> “I can do that, but based on what you're trying to accomplish, I recommend we work section by section. Here's why…”

Then explain the tradeoffs and let the user choose.

## Deeper principle

> **Preserve valuable ideas. Do not preserve complexity merely because it already exists.**

The goal is not to protect old code. The goal is to achieve the best real-world result safely, efficiently, and repeatably.
