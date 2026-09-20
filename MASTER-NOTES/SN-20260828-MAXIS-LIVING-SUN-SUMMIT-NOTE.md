# 🔱 MAXIS LIVING SUN — SUMMIT NOTE

**Date:** 2026-08-28  
**Canonical repository:** `SoulSchoolAcademy/NayaPOWER`  
**Decision record:** Issue #69  
**Status:** CANONICAL DESIGN DIRECTION / IMPLEMENTATION PENDING

## Summit Decision

The ultimate presentation direction for the MAXIS assessment is **NAYA LIVING SUN**.

This is not a prettier questionnaire and not a decorative circle. It is a signature interaction language in which the assessment feels like a **living intelligence system that happens to contain a question**.

The human remains the center of the product experience. Naya is the intelligence guide. The question is the cognitive center. Answers are the primary action. The surrounding field communicates intelligence, progression, energy, time, and response.

## Why Living Sun Wins

Living Sun provides the strongest balance of:

- immediate conceptual clarity;
- strong Naya identity;
- premium cinematic potential;
- natural connection to the intelligence/fingerprint/results vision;
- meaningful response to user choices;
- desktop-to-mobile adaptability;
- calm, non-game-like interaction;
- presentation-layer independence from assessment/scoring truth.

Galaxy is more cinematic but adds metaphor and cognitive overhead. Crystal is premium and controlled but has weaker continuity with Naya's living-intelligence identity. Living Sun is the strongest overall foundation because it can be extraordinary **without sacrificing usefulness**.

## Protected Concept

> **The question is on stage. The Living Sun surrounds it. One living energy orb moves around the field like a quiet comet, continuously marking the active moment. The human answers. The system acknowledges the choice. The experience advances.**

The user should feel that the question has a place in a living system, not that they are filling out a form.

## Canonical Living Sun Geometry

### 24 Orbs

Use **24 surrounding micro-orbs** as the canonical conceptual field.

The 24-orb count intentionally represents the **24-hour cycle / clock**. This is part of the meaning of the design, not an arbitrary particle count.

The exact pixel size, spacing, depth treatment, and responsive placement may adapt by viewport, but the conceptual 24-position field is protected.

### 12-Color Repeating Spectrum

Use the ordered 12-color Naya spectrum:

**MAGENTA → RED → ORANGE → GOLD → YELLOW → GREEN → TEAL → CYAN → BLUE → INDIGO → PURPLE → LAVENDER**

Repeat the 12-color sequence twice across the 24-orb field.

The orbs may remain comparatively quiet at their base colors. The field is not a ring of 24 simultaneously glowing lights.

### One Active Energy Orb

Exactly **one orb is actively illuminated at a time** as the default motion model.

It travels slowly around the field like a **comet / spotlight / energy pulse** moving around the Naya Sun.

The active orb should:

- be clearly visible;
- feel luminous and alive;
- move calmly and continuously;
- preserve the sense of a stage surrounding the question;
- never distract from reading or answering.

A short comet-like trail may be tested, but is **not required** and must earn its place through usability testing. Start with one active orb and no trail unless evidence supports adding one.

## Stage Composition

The intended feeling is a **world-stage / television-stage presentation**, not a dashboard.

The central composition should feel like a beautifully lit stage with the question in the spotlight and the Living Sun forming the environment around it.

Canonical hierarchy:

1. **QUESTION** — unquestioned visual star.
2. **ANSWERS** — primary interaction.
3. **NAYA GUIDE BAR** — persistent, compact support.
4. **PROGRESS / NAVIGATION** — clear orientation and control.
5. **LIVING SUN FIELD** — atmosphere, meaning, motion, and response.

The field creates depth and presence. It does not become the subject.

## Naya Guide Bar

Do not use a recurring pop-up explanation for every question.

Use a compact, persistent Naya area containing:

- Naya profile/image;
- a concise text explanation of what the current question is asking;
- **Play Naya**;
- **Let's Go**.

**Play Naya** is optional. When activated, Naya conversationally reads/explains the question and answer choices, then invites the user to continue.

**Let's Go** advances the stage when the user is ready.

Back/Next controls remain available so the user can review and move through questions predictably.

Naya must make the assessment easier, not slower.

## Interaction Response

When a human selects an answer:

1. clearly acknowledge the selection;
2. produce a brief visual response;
3. let the Living Sun acknowledge the choice;
4. commit the answer through the existing assessment engine;
5. advance efficiently to the next question.

The intended feeling is:

> **My choice changed the system.**

Do not use spectacle for spectacle's sake. Meaningful response beats excessive effects.

## Motion / Living Depth Law

Motion should create the feeling of a living dimensional field:

- slow orbital movement;
- subtle depth/parallax where useful;
- restrained glow;
- smooth color presence;
- brief selection response;
- fast return to calm reading state.

The visual system should feel like it is **coming alive from the page**, while remaining quiet enough that a person can comfortably think.

Reduced-motion mode must preserve the functional meaning without requiring animation.

## Architecture Law

MAXESS assessment/scoring truth remains independent of Living Sun presentation.

The assessment engine owns:

- questions;
- answers;
- selection state;
- progression;
- scoring;
- result data.

Living Sun owns presentation and interaction feedback only.

The visual metaphor must be replaceable without changing assessment truth.

## Mobile / Accessibility / Performance

Mobile is first-class. The composition must adapt rather than simply shrink.

Protect:

- question readability;
- answer usability;
- Naya visibility;
- navigation;
- touch targets;
- keyboard operation;
- semantic controls;
- contrast;
- screen-reader access;
- reduced motion;
- rendering performance.

Desktop may enhance the stage. Mobile cannot become the degraded version.

## Protected vs Replaceable

### Protected

- Naya Living Sun as the canonical direction.
- 24-orb conceptual clock field.
- 12-color spectrum repeated twice.
- one active illuminated energy orb as the default.
- question-first hierarchy.
- answer-first interaction.
- compact Naya guide bar.
- Back / Next predictability.
- meaningful but restrained system response.
- presentation/assessment architecture separation.
- mobile, accessibility, performance, and reduced-motion requirements.

### Replaceable / Testable

- exact CSS/DOM/canvas/SVG implementation;
- exact orb dimensions and spacing;
- exact orbital radius by viewport;
- depth/parallax intensity;
- glow strength;
- animation duration/easing;
- whether a short trail improves the experience;
- exact typography and decorative treatment;
- exact placement adaptations required by responsive constraints.

### Unknown Until Proven

- whether the 24-orb field is optimal at every viewport;
- whether users perceive the clock symbolism without explanation;
- whether a trail improves or harms focus;
- the optimal orbital speed;
- the optimal field brightness;
- the best mobile representation of the full field.

These questions must be answered by evidence, not preference.

## Final Human Standard

Do not optimize for WOW alone.

Optimize for:

**WOW + CLARITY + HUMAN VALUE + EASE + ACCESSIBILITY + PERFORMANCE + MEANING.**

A beautiful Living Sun that makes the assessment harder is a failure.

The target human response is:

> **“That was fun.”**  
> **“I learned something.”**  
> **“Naya helped me.”**  
> **“I want to try another MAXIM.”**

## Acceptance Gate

Build a real five-question vertical slice using the existing MAXIS assessment engine.

Then prove:

- immediate comprehension;
- question dominance;
- answer clarity;
- correct scoring/progression;
- meaningful selection response;
- mobile usability at established MAXIS viewports;
- keyboard/accessibility usability;
- reduced-motion behavior;
- performance;
- Naya guide usability;
- Back/Next reliability;
- continuity into results/fingerprint;
- Oscar review and exact repair loop.

Do not declare production-ready because the visual exists. The implementation must be tested and evidenced.

**Decision is canonical. Implementation is not yet proven.** 🔱
