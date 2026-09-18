# NAYA NITRO — VISUAL NORTH STAR / PERMANENT UI RULES

Status: ACTIVE / LOCKED

## 1. GROOVE FULL-BLEED RULE — ABSOLUTE

Every MAXESS Results section and every future Groove-rendered Naya/MAXESS experience MUST render as a true full-viewport, full-bleed experience.

Never, under any circumstance, intentionally create:

- a narrow centered webpage inside Groove;
- an iframe-like visual presentation;
- white margins on the left or right;
- white space surrounding a dark page because the embed did not escape the parent container;
- a phone-width composition on desktop;
- a constrained page wrapper that makes the experience look embedded inside another page.

The visual canvas must own the viewport.

Implementation must explicitly account for Groove's parent container and break out to the viewport when required, using a robust full-bleed strategy rather than assuming `width:100%` is sufficient.

Required design intent:

`viewport → MAXESS experience → internal composition`

Never:

`Groove page → narrow container → MAXESS experience`

## 2. RENDERED EXPERIENCE IS THE PRIMARY TRUTH

Source code is not proof of visual quality.

The authoritative workflow is:

BUILD → RENDER → VIEW → SCORE → IMPROVE → FREEZE

A section is not visually complete because the HTML exists, the GitHub file exists, or the code appears technically sound.

## 3. SECTION 01 INFORMATION HIERARCHY

Section 01 is a personal result reveal.

Required hierarchy:

1. Naya arrival / trusted relationship
2. AI SCORE headline and actual score
3. Living MAXESS Orb
4. Mastery stage
5. One clear continuation action

The Orb is the visual hero, but the score must be clearly presented outside the Orb as the primary informational headline when that produces the clearest experience.

Do not put a large score label inside the Orb merely because it is technically convenient.

## 4. NO-DATA PRESENTATION RULE

Never fabricate a production result.

However, a visual QA build MUST have an explicit preview mode so the human can inspect the visual result without the production result contract being available.

Preview data must be unmistakably development/preview data and must never silently masquerade as production data.

The production page consumes `window.MAXESS_RESULT`.

## 5. NAYA PRESENTATION

Naya should feel like a trusted intelligent partner who has reviewed the user's result.

For Section 01, the compact conversational presentation is preferred:

- approved Naya visual asset;
- brief human message;
- LISTEN TO NAYA action;
- no sales-page card treatment;
- no unnecessary explanatory paragraph.

## 6. ORB IDENTITY

The Living MAXESS Orb must be extraordinary, dimensional, calm, intelligent and unmistakably MAXESS.

The MAXESS Orbital Bead is mandatory.

It must remain clearly visible as a small luminous object travelling around the Orb's exterior.

## 7. DESKTOP-FIRST COMPOSITION

Desktop/widescreen is a first-class design state.

The composition must use the available viewport rather than behaving like a mobile card centered on a desktop page.

Mobile must adapt the hierarchy, not redefine the experience.

## 8. QA LANGUAGE

When a render fails visually, say so plainly.

Do not defend technically valid code when the visual result is wrong.

Ask:

**WHY IS THIS NOT A 10?**

Then fix the underlying problem, not merely the visible symptom.

## 9. NEXT-ACTION RULE

Every Naya Nitro execution must end with a clear next action and an exact next prompt.

The user must never be left thinking:

**“Okay… now what?”**

The preferred immediate artifact is always the viewable Groove-ready source when visual review is the current gate.

## 10. SECTION 01 CURRENT CORRECTION

The failed V5 presentation exposed these problems:

- score not visible when production data was absent;
- `RESULT PENDING` was presented as hero content instead of a graceful no-data state;
- score was placed inside the Orb rather than as the external headline;
- Groove full-bleed behavior was insufficient;
- Orb needed stronger dimensional/art-directed presence;
- Naya treatment was directionally good and should be preserved/refined rather than discarded.

These findings are now part of the active Section 01 design contract.

## 11. SURGICAL ITERATION / COMPONENT PRESERVATION RULE — ABSOLUTE

When a human approves or positively identifies a component, that component becomes a **PROTECTED COMPONENT** for subsequent iterations.

Do not redesign, reposition, restyle, replace, or remove a protected component merely because another part of the section is being improved.

Every iteration must explicitly separate:

**KEEP** — approved elements that must survive unchanged unless the human asks otherwise.

**CHANGE** — the specific element(s) the human is reacting to.

**IMPROVE** — additional weaknesses discovered by Naya that can be corrected without disturbing protected elements.

For Section 01 V7, the compact Naya arrival treatment is protected because the human explicitly identified that direction as good. The score/orb composition is the change target.

The correct iteration pattern is:

`PRESERVE GOOD → ISOLATE PROBLEM → IMPROVE PROBLEM → RE-RENDER`

Never:

`REBUILD EVERYTHING → HOPE THE GOOD PART SURVIVES`

Before every visual iteration, Naya Nitro must state internally:

1. What did the human like?
2. What did the human dislike?
3. What specifically caused the failure?
4. What must remain untouched?
5. What is the smallest architectural change that can solve the problem?

This rule exists to prevent regressions where fixing one visual component destroys another component that was already working.
