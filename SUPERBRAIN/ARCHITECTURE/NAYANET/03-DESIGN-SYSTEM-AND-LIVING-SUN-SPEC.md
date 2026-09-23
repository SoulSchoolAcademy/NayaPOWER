# 🔱 NAYANET — DESIGN SYSTEM + LIVING SUN SPECIFICATION

**Status:** ACTIVE PRODUCT DESIGN CONTRACT  
**Governing authority:** `NAYA/INTELLIGENCE/DESIGN-ENGINEERING/`  
**Scope:** NayaNET visual identity, Living Sun, surfaces, interaction language, and product-specific design details

> This document remains useful as a product-specific design reference. It is not a competing global design standard. Where this document conflicts with the current Design + Engineering Intelligence standard, the current standard governs.

## 1. Design north star

The visual system must communicate intelligence, energy, warmth, depth, precision, and possibility without becoming visually noisy.

Reference metaphor:

**a luminous intelligence instrument, not a SaaS dashboard.**

## 2. Foundation

Primary canvas:

- near-black / deep-space foundation;
- generous negative space;
- luminous surfaces rather than flat cards;
- restrained glass/translucency only where it improves hierarchy.

Core palette:

- white for primary type;
- black/deep-space for foundation;
- Naya purple as primary identity;
- magenta for energy/activation;
- blue for intelligence/communication;
- green for success/growth;
- semantic accents only when they improve meaning and remain subordinate to the canonical design system.

Do not introduce yellow/gold as a default product accent merely because an older version of this specification mentioned it. Any premium/high-value emphasis must remain compatible with the current canonical design language and accessibility requirements.

## 3. Typography

Hierarchy:

**HEADLINE → SUPPORTING STATEMENT → DETAIL**

Headlines are short and confident.

Supporting statements explain the promise.

Detail appears only when useful.

Never use low-contrast purple text against purple surfaces.

## 4. Geometry language

The NayaNET visual grammar uses:

- circles;
- concentric rings;
- orbital paths;
- nodes;
- radial gradients;
- luminous cores;
- subtle particle/energy fields;
- precise symmetry with controlled asymmetry for movement.

Geometry should imply an intelligent system rather than decoration.

## 5. Living Sun

The Living Sun is the primary Naya visual interface primitive.

Conceptual layers:

```text
Outer ambient field
      ↓
Orbit ring(s)
      ↓
Energy ring
      ↓
Intelligence ring
      ↓
Core glow
      ↓
Naya presence
```

The implementation must be scalable, performant, and accessible.

## 6. Living Sun states

Required semantic states:

- RESTING
- ATTENTION
- LISTENING
- THINKING
- SPEAKING
- PLAYING
- SUCCESS
- WARNING
- ERROR
- DISCONNECTED

Each state specifies:

- motion pattern;
- pulse/rhythm;
- glow intensity;
- ring activity;
- accessible textual state;
- transition timing;
- reduced-motion behavior.

## 7. Resting

Slow, nearly imperceptible breathing.

Purpose: Naya is present without demanding attention.

## 8. Attention

Slightly increased luminosity and orbit activity.

Purpose: something important is available.

## 9. Listening

Outer ring opens rhythmically toward the user.

Purpose: Naya is receiving input.

## 10. Thinking

Orbital motion becomes directional and layered.

Purpose: Naya is processing rather than pretending instant certainty.

## 11. Speaking

Core/rings synchronize subtly with speech when measurable; otherwise use a calm speaking animation.

Purpose: visual confirmation that Naya is communicating.

## 12. Playing

Media-oriented orbit state; playback progress may be represented as a controlled ring.

## 13. Success

Brief outward expansion / completion wave.

No confetti overload.

## 14. Warning / error

Use semantic visual changes plus text. Never communicate an important state through color alone.

## 15. Motion

Motion should feel physical and intentional.

Avoid:

- excessive bouncing;
- random particle spam;
- perpetual high-frequency animation;
- animation that competes with readable content.

Honor `prefers-reduced-motion`.

## 16. Surfaces

Use depth through:

- luminosity;
- edge highlights;
- soft shadows/glows;
- layering;
- scale;
- spatial positioning.

Avoid generic dashboard card grids unless the information genuinely benefits from cards.

## 17. Buttons

Primary CTA:

- visually dominant;
- short verb;
- unmistakable active state;
- keyboard focus;
- touch-safe dimensions;
- truthful engine/state feedback;
- physical/depth cues only when they improve clarity and do not obscure semantics.

Examples:

**Meet Naya**  
**Create My NayaNET**  
**Ask Naya**  
**Start the Challenge**  
**Enter My Hub**  
**Activate Naya Power**

The canonical living-object model is:

**REST → HOVER → FOCUS → PRESS → PROCESSING → SUCCESS / FAILURE**

Where applicable, include semantic states such as disabled, authorized, unauthorized, queued, blocked, retryable, partial, and complete. The interface must never imply engine success when the engine did not succeed.

## 18. Design law

> **Every visual element must either communicate state, hierarchy, meaning, or emotion. If it does none of those, remove it.**

## 19. Governance

This product specification is maintained by the current Design + Engineering Intelligence standard.

Before adding a new global design rule, use:

**SEARCH → COMPARE → DISTILL → UPDATE CURRENT STANDARD → RETIRE DUPLICATE → VERIFY**

Product-specific detail belongs here only when it has a concrete NayaNET role. General design/coding laws belong in `NAYA/INTELLIGENCE/DESIGN-ENGINEERING/`.
