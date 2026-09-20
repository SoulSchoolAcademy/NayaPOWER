# Sparkling Shape Hub — Visual Contract

**Status:** FROZEN VISUAL SOURCE OF TRUTH for the reactive Hub conversion
**Date:** 2026-09-19
**Runtime inspected:** `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/`
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## Decision

The existing Sparkling Shape Hub is the visual source of truth.

The React work must **elevate that exact experience into a reactive Hub**, not replace it with a different design.

## Observed visual contract

### Global
- Near-black `#050507` base.
- Indigo/purple radial ambient glow with restrained magenta secondary glow.
- White/high-contrast typography with muted gray supporting text.
- Inter/system UI typography.
- Glass/blur sticky surfaces.
- Deep shadows, inset highlights, restrained neon glow.
- Purple, indigo, blue, green, yellow/gold, magenta accent family.
- Buttons are physical-looking: bordered, rounded, gradient-filled, inset highlight, shadow, lift-on-hover.

### Left rail
- Fixed/sticky dark rail, approximately 230px.
- NayaNET brand mark and `INTELLIGENT HUB`.
- `YOUR INTELLIGENCE` section.
- Feature navigation with icon + label.
- Active item uses dark purple surface, magenta border/glow, and right-side magenta indicator.
- Bottom privacy statement:
  **PRIVATE BY DEFAULT · Shared by choice · Collective by consent · Public by decision.**

### Top navigation
- Sticky dark glass header.
- Eight compact primary buttons:
  HOME / NAYA POWER / 5-DAY CHALLENGE / ENTER FREE / POWERCAST / WHITE PAPER / ABOUT US / LOGIN.
- Each button has the established colored border family and lift/glow hover behavior.
- Compact Naya identity/status card at the upper-right.

### Search
- Large bordered rounded search surface beneath the header.
- Purple glow/border.
- Search icon, text input, keyboard hint, and `TALK TO NAYA` action.

### Main intelligence surface
- Large editorial hero/headline.
- Feed/navigation controls.
- Full-width intelligent blocks.
- Strong left-edge vertical intelligence accent.
- Large rounded dark cards with inset highlight and deep shadow.
- `IN A NUTSHELL` section.
- Layered intelligence views with large circular jewel-like icons.
- Nine canonical views are visually distinct by accent:
  HUMAN NOTE, CHILD NOTE, GRANDMA NOTE, NAYA NOTE, MACHINE NOTE, LEARNING LESSON, WHAT IT MEANS, HOW TO APPLY / HOW TO USE, WHAT'S IN IT FOR YOU.
- Layer cards use large physical/jewel treatment, colored borders, glow, and generous readable body copy.
- Action controls are compact, physical, bordered buttons.

### Bottom system surfaces
- Fixed mission strip:
  **CREATE. CONNECT. GROW WITH US.**
- Fixed feature/action bar with gold-accent label and physical buttons.

### Responsive behavior
- Desktop: left rail + main content + right Naya rail in the original source, with later runtime refinements hiding the right rail.
- Medium: left rail narrows and right rail collapses.
- Mobile: left rail collapses; bottom feature bar remains; content becomes single-column; top controls compress.

## Reactive conversion rule

The React Hub may change **data, state, routing, persistence, loading, authorization, and governed actions**.

It must not casually change the established visual language.

Canonical data must replace static/demo intelligence without changing the user's mental model.

## Proof boundary

This contract is based on direct inspection of the current Sparkling Shape runtime and the corresponding repository HTML artifact.

It does **not** yet prove that the new React build has been deployed to Sparkling Shape or that human-facing runtime parity has passed.

Next proof:
**React source → build → Sparkling Shape deployment → live DOM/interaction comparison → canonical intelligence rendered → human acceptance.**
