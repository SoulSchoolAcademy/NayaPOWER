# 🔱 NayaNET Experience System — Canonical Design Language

**Status:** LOCKED — v1.0  
**Authority:** NayaPOWER canonical design system  
**Applies to:** E01, E02, E03, E04 and every future NayaNET Intelligent Hub Experience (E-Series)  
**Locked:** 2026-08-31  

## Purpose

This document is the canonical visual, interaction, motion, component, and continuity language for the NayaNET Intelligent Hub / Naya Power entrance to the internet.

An E-Series experience is a chapter in one coherent intelligent world—not a collection of unrelated webpages.

## Non-negotiable principles

1. **Preserve what works. Change only what is wrong.**
2. **Scene → Transition → Interaction → Response** is the primary design unit.
3. Do not redesign an approved scene when changing another scene.
4. Do not introduce a new visual language for each E.
5. Do not default to SaaS dashboards, card grids, generic AI UI, or decorative gradients.
6. The specification is the minimum contract; excellence is the product requirement.
7. Technical correctness never substitutes for visual or experiential quality.
8. A capability must never be represented as live when it is not actually live.

## Experience architecture

E01, E02, E03… are independently deployable experiences with a shared Naya Experience System and shared lightweight session contract.

Default progression:

`E01 → E02 → E03 → E04 → …`

Default connection method: URL navigation with shared session state. Experiences must not depend on another experience's DOM, JavaScript runtime, iframe internals, or implementation details.

Groove is the outer composition/orchestration layer. Cloudflare-hosted E artifacts are independently testable and deployable.

Embedding is reserved for cases where a module genuinely must remain on the same screen. It is not the default coupling mechanism.

## Visual language

### World

- Deep-space black foundation.
- Controlled luminous fields rather than flat backgrounds.
- Strong negative space.
- Depth, scale, atmosphere, and asymmetry.
- Light is functional: it establishes hierarchy, attention, state, and transition.
- Purple is the primary Naya intelligence accent.
- White is used for authority and readability.
- Gold is reserved for premium/high-value moments, not decoration everywhere.

### Geometry

Use the Naya spatial vocabulary:

- Living Sun / luminous core.
- Concentric rings.
- Orbital paths.
- Radial fields.
- Nodes and intelligent destinations.
- Controlled particles only when they improve depth.

Geometry should communicate intelligence and relationship—not become ornamental noise.

### Typography

- Large, confident display hierarchy for primary statements.
- Short copy with generous breathing room.
- High contrast between primary and supporting information.
- Avoid dense paragraphs and UI-copy overload.
- Typography is part of composition, not merely content styling.

## Naya presence

Naya is a presence, not a decorative portrait.

Her official locked visual asset must be used where Naya is represented. The asset must be treated as part of the experience composition: scale, crop, lighting, glow, position, and motion establish presence.

Naya state language must remain consistent across experiences:

- RESTING
- ATTENTION
- LISTENING
- SPEAKING
- SUCCESS
- DISCONNECTED

## Canonical button system

**Buttons are LOCKED as a system.** Individual E experiences may not invent a new button style without explicitly extending this system.

### Primary — Naya Action

Purpose: the single highest-priority action in a scene.

Visual character:
- premium luminous surface;
- substantial touch target;
- restrained gradient/light response;
- subtle depth rather than flat fill;
- clear hover/focus lift;
- confident typography;
- no excessive pill styling;
- never a generic Bootstrap/SaaS button.

### Secondary — Supporting Action

Purpose: important but subordinate action.

Visual character:
- transparent/deep-space surface;
- luminous border or controlled edge light;
- same geometry, typography, radius family, and motion language as Primary;
- visually quieter than Primary.

### Ghost / Text Action

Purpose: low-emphasis navigation or optional action.

Visual character:
- minimal surface treatment;
- typography and hover light establish affordance;
- never compete with the Primary action.

### Continue / Next

Purpose: progression through an experience.

Uses the Primary family and communicates forward movement consistently. The label may change by context, but the visual grammar does not.

### Back

Uses the Secondary family and remains visually subordinate.

### Disabled / Processing

Must preserve the same geometry and hierarchy while visibly communicating unavailable/processing state. Never appear as a broken or unrelated control.

### Button invariants

Every button must have:

- minimum accessible touch target;
- visible focus state;
- keyboard accessibility;
- hover/active/disabled states;
- consistent typography;
- consistent radius and dimensional language;
- consistent transition timing;
- clear primary/secondary hierarchy.

## Surfaces

Avoid unnecessary cards.

When a surface is required, it should feel like part of the environment:

- translucent/deep-space material;
- controlled edge light;
- subtle depth;
- enough negative space;
- no excessive shadows or generic card borders.

## Motion language

Motion must communicate state and spatial continuity.

- Arrival: slow, atmospheric reveal.
- Recognition: focused light/attention shift.
- Interaction: immediate but refined response.
- Transition: spatial continuity rather than hard section swapping.
- Success: controlled luminous confirmation.
- Failure: calm, informative recovery.

Respect `prefers-reduced-motion`.

## Interaction language

The user should always understand:

1. where they are;
2. what Naya is doing;
3. what they can do next;
4. what happened after they acted.

Avoid dead controls, ambiguous affordances, and fake backend behavior.

## Responsive language

Responsive behavior is compositional, not merely a stack of desktop boxes.

The world must remain intentional from narrow mobile through large desktop.

Do not let mobile become an afterthought.

## E-Series continuity contract

Every E must define:

- `experienceId` (E01, E02, …)
- `previousExperience`
- `nextExperience`
- identity/session read contract
- completion state
- design-system version

Example:

```json
{
  "experienceId": "E01",
  "previousExperience": null,
  "nextExperience": "E02",
  "designSystem": "NayaNET-Experience-v1",
  "identityMode": "local-preview"
}
```

## Non-regression protocol

When a human rejects an element:

1. Identify the exact failed design unit.
2. Preserve unaffected scenes/components.
3. Change only the affected unit.
4. Re-test.
5. Compare against the accepted baseline.
6. Confirm no regression.
7. Lock the repaired unit once accepted.

## Acceptance gates

An E is not complete until it passes:

- Technical
- Visual
- Interaction
- Emotional
- Brand
- Coherence
- Human acceptance

The final gate is not a numeric score. It is whether the experience is genuinely worthy of NayaNET.

## Current lock

**NayaNET Experience System v1.0 is the canonical design authority for the E-Series.**

Future E work must reference this document before introducing visual components, button variants, motion patterns, or navigation conventions.
