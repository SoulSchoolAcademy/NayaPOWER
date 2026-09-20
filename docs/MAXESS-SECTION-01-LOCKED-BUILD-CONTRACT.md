# MAXESS RESULTS — SECTION 01 LOCKED BUILD CONTRACT

Status: ACTIVE / LOCKED
Repository: `SoulSchoolAcademy/MaxRESULTS`
Section: `01 — Naya Arrival + AI Score`
Purpose: authoritative visual, UX, frontend, QA, and execution contract for Section 01.

## 01 — NORTH STAR

Section 01 is the personal result reveal.

The user should immediately feel:

- Naya sees me.
- This is my result.
- This is my AI Score.
- I want to understand what it means.

This is not a sales page, dashboard, report card, generic AI landing page, or Orb demonstration.

## 02 — ABSOLUTE FULL-BLEED RULE

The rendered experience must occupy the entire available viewport: `100vw × 100vh`.

Never create:

- white left/right margins;
- a narrow centered webpage;
- an iframe-like presentation;
- a phone-shaped desktop composition;
- a white Groove parent surrounding the experience;
- a constrained content wrapper that makes MAXESS look embedded inside another page.

The architecture is:

`VIEWPORT → MAXESS`

not:

`GROOVE → CONTAINER → MAXESS`.

The implementation must explicitly escape Groove's constrained parent when required.

## 03 — PROTECTED NAYA COMPONENT

The approved Naya arrival treatment is protected.

Use the supplied approved Naya profile asset: `This-is-good-Naya-Profile.png` when available in the authoritative project assets.

Placement: centered above the score/orb experience.

Required copy:

“Hi. I've looked at your results.”

“This isn't your judgment. It's your map.”

Primary CTA:

`LISTEN TO NAYA`

Naya must feel warm, human, intelligent, and conversational. She must not look like a sales card.

Once this component is approved, later iterations must preserve it unless the human explicitly requests a change.

## 04 — SCORE CONTRACT

Immediately beneath the Naya arrival:

`YOUR AI SCORE`

`[REAL SCORE]`

`[REAL MASTERY STAGE]`

The score is external to the Orb. The score must be large, beautiful, unmistakable, and immediately readable.

Never hide the score inside the Orb. Never replace it with `RESULT PENDING`. Never duplicate it unnecessarily.

Production source of truth:

`window.MAXESS_RESULT`

No competing scoring engine. No fabricated production score.

For visual QA, an explicit preview mode may supply a clearly marked development fixture, but it must never silently masquerade as production data.

## 05 — LIVING MAXESS ORB

The Orb is the visual masterpiece of Section 01 and the living visual expression of the score.

Required layers:

1. outer atmospheric field;
2. diffuse halo;
3. outer orbital geometry;
4. secondary orbital ring;
5. primary orbital ring;
6. MAXESS ORBITAL BEAD;
7. score/energy arc;
8. translucent dimensional shell;
9. inner energy field;
10. luminous core;
11. subtle internal movement;
12. depth/shadow;
13. score-reactive illumination.

The Orb must feel dimensional, luminous, intelligent, alive, calm, cinematic, organic, and unmistakably MAXESS.

Do not create a generic CSS circle, gaming widget, progress meter, stock AI animation, neon toy, or random effects collage.

## 06 — MAXESS ORBITAL BEAD — MANDATORY

The `MAXESS ORBITAL BEAD` is a defining identity component and may not be omitted.

It is a small luminous sphere physically travelling around the exterior of the Orb.

Desktop: 10–16px.
Mobile: 8–12px.
Orbit radius: approximately 100–108% of Orb radius.
Revolution: approximately 8–12 seconds.
Motion: continuous, smooth, elegant, clearly visible.

The bead must have spatial separation from the Orb and must not look like a dot glued to the ring. It must remain visibly distinct throughout normal motion.

Reduced motion: stop positional travel and retain a static luminous bead with a safe, non-animated glow.

## 07 — ORBITAL SYSTEM

Primary ring: thin luminous translucent ring.
Secondary rings: restrained variations in radius, opacity, blur, angle, and brightness.
Energy arc: a meaningful portion of the circumference whose state responds to the actual score.

The Orb must use geometry, layering, light, opacity, scale, and restrained motion to create real depth.

## 08 — SCORE COLOR ENGINE

Use continuous interpolation based on the actual score.

0–49: red spectrum.
50–59: red → orange.
60–74: orange → yellow.
75–84: yellow → green.
85–89: green → cyan/blue.
90–94: blue → violet.
95–100: violet → magenta.

The same score state should influence Orb accent, halo, energy arc, orbital bead, atmospheric glow, and subtle energy intensity.

Use the approved MAXESS semantic palette from the active design directive as the implementation authority. Never sacrifice text contrast for score color.

## 09 — SCORE REVEAL

Sequence:

1. dark atmospheric environment;
2. Orb awakens;
3. energy appears;
4. orbital system activates;
5. orbital bead begins moving;
6. `YOUR AI SCORE` appears;
7. real score resolves;
8. mastery stage appears;
9. Naya becomes the human guide.

Keep the sequence short and engaging. No annoying loading state, fireworks, confetti, excessive counting, or gaming effects.

The score must become readable immediately.

## 10 — INFORMATION HIERARCHY

The visual story is:

`Naya → YOUR AI SCORE → REAL SCORE → MASTERY STAGE → LIVING MAXESS ORB → LISTEN TO NAYA`

Only one object owns primary attention at a time. Nothing else may compete with the Naya/score/Orb reveal.

## 11 — FORBIDDEN CONTENT

Section 01 must contain none of:

- Result Pending;
- giant explanatory paragraphs;
- invented marketing copy;
- generic AI filler;
- three-column SaaS layout;
- sales cards;
- membership information;
- pricing;
- feature lists;
- report explanation;
- dimension breakdowns;
- fingerprint analysis;
- long educational copy;
- duplicate score;
- score hidden inside the Orb;
- random Naya redesign;
- placeholder Naya image;
- missing orbital bead;
- narrow webpage;
- white sidebars.

## 12 — RESPONSIVE CONTRACT

Required inspection targets:

1440, 1280, 1024, 768, 600, 480, 414, 390, 375, 360, 320px.

Desktop: cinematic, full viewport, large Orb, compact Naya, dominant score.
Tablet: intelligently reduced Orb while preserving hierarchy.
Mobile: Naya → score label → score → stage → Orb → Listen CTA; no clipping, overflow, or hierarchy collapse.

## 13 — ACCESSIBILITY CONTRACT

Must include:

- semantic headings;
- accessible score text;
- accessible Orb description;
- real button semantics;
- visible keyboard focus;
- adequate contrast;
- minimum touch target sizing;
- no color-only meaning;
- reduced-motion support;
- no animation required to understand the result.

## 14 — TECHNICAL CONTRACT

Self-contained module. One clear DOM root. One clear initialization path. Namespaced classes and variables. No unnecessary libraries. No duplicate listeners. No uncontrolled observers. No unbounded animation loops.

Use CSS transforms/opacity for motion where practical. Keep particle counts bounded. Prefer CSS/SVG layers when efficient.

The module must mount safely once and be safe to re-render without duplicated behavior.

Section 02 must be attachable without rewriting Section 01.

## 15 — PROTECTED COMPONENT / SURGICAL ITERATION LAW

Before every iteration classify every major component as:

KEEP — approved and protected.
CHANGE — specifically identified by human feedback.
IMPROVE — additional weakness discovered by QA that can be corrected without disturbing KEEP components.
REMOVE — unnecessary or harmful element.

The correct pattern is:

`PRESERVE GOOD → ISOLATE PROBLEM → IMPROVE PROBLEM → RE-RENDER`

Never:

`REBUILD EVERYTHING → HOPE THE GOOD PART SURVIVES`.

Before touching code, determine:

1. What did the human like?
2. What did the human dislike?
3. What caused the failure?
4. What must remain untouched?
5. What is the smallest architectural change that solves the problem?

## 16 — AAA ACCEPTANCE CHECKLIST

Do not present the build until every applicable item is complete and verified.

### Human experience

- [ ] Personal result reveal is immediately understood.
- [ ] Naya feels present and human.
- [ ] Naya feels like she reviewed the result.
- [ ] Experience feels warm, intelligent, calm, premium.
- [ ] User wants to discover what comes next.

### Information

- [ ] `YOUR AI SCORE` is immediately visible.
- [ ] Real score is immediately visible.
- [ ] Mastery stage is immediately visible.
- [ ] Score is outside the Orb.
- [ ] No `RESULT PENDING` hero state.
- [ ] No unnecessary duplicate score.

### Orb

- [ ] Orb is the visual centerpiece.
- [ ] Orb has dimensional depth.
- [ ] Orb has layered geometry.
- [ ] Orb has atmospheric halo.
- [ ] Orb has internal energy.
- [ ] Orb has score-reactive illumination.
- [ ] Orb has score-reactive color.
- [ ] Orbital rings are visible and intentional.
- [ ] Energy arc is present and meaningful.
- [ ] MAXESS ORBITAL BEAD exists.
- [ ] Bead visibly travels around the exterior.
- [ ] Bead remains spatially distinct from the Orb.
- [ ] Bead responds to score state.
- [ ] Reduced motion produces a static, beautiful bead.

### Naya

- [ ] Approved Naya image is used.
- [ ] Approved Naya treatment is preserved.
- [ ] Exact approved copy is used.
- [ ] `LISTEN TO NAYA` is the single primary CTA.
- [ ] Naya does not look like a sales card.

### Composition

- [ ] Full bleed is real, not merely intended.
- [ ] No white sidebars.
- [ ] No narrow parent container.
- [ ] No iframe appearance.
- [ ] Desktop uses the full viewport beautifully.
- [ ] Nothing unnecessary competes with the hero.

### Responsive

- [ ] 1440px inspected.
- [ ] 1280px inspected.
- [ ] 1024px inspected.
- [ ] 768px inspected.
- [ ] 600px inspected.
- [ ] 480px inspected.
- [ ] 414px inspected.
- [ ] 390px inspected.
- [ ] 375px inspected.
- [ ] 360px inspected.
- [ ] 320px inspected.
- [ ] No horizontal scrolling.
- [ ] No clipping or collisions.

### Accessibility

- [ ] Semantic headings.
- [ ] Accessible Orb description.
- [ ] Accessible score.
- [ ] Real button semantics.
- [ ] Visible focus.
- [ ] Contrast verified.
- [ ] Touch targets verified.
- [ ] Color is not the only meaning.
- [ ] Reduced motion verified.

### Data / engineering

- [ ] `window.MAXESS_RESULT` is authoritative in production.
- [ ] No competing scoring engine.
- [ ] No fabricated production data.
- [ ] Preview mode is explicit and unmistakable.
- [ ] Mount is self-contained.
- [ ] Re-render does not duplicate listeners/animation.
- [ ] No console-breaking errors.
- [ ] Groove-compatible source is complete.
- [ ] Source is committed to `SoulSchoolAcademy/MaxRESULTS`.

## 17 — MANDATORY EXECUTION ORDER

The implementation agent MUST execute these stages sequentially and MUST NOT stop early:

### STAGE A — ORIENT

1. Confirm repository: `SoulSchoolAcademy/MaxRESULTS`.
2. Read this contract.
3. Read `docs/NAYA-NITRO-VISUAL-NORTH-STAR.md`.
4. Read the active MAXESS master design directive and relevant component/button/asset contracts.
5. Inspect the current Section 01 implementation only for useful assets/techniques.
6. Identify the approved Naya component and protected elements.
7. Build a requirement-to-implementation checklist before coding.

### STAGE B — ARCHITECT

8. Define the full-bleed mounting strategy.
9. Define DOM structure and component boundaries.
10. Define data normalization from `window.MAXESS_RESULT`.
11. Define explicit preview mode.
12. Define score-to-color interpolation.
13. Define Orb layer stack.
14. Define Orbital Bead geometry and motion.
15. Define score reveal choreography.
16. Define responsive breakpoints.
17. Define accessibility and reduced-motion behavior.

### STAGE C — BUILD

18. Build the complete Section 01 module.
19. Implement the protected Naya treatment first and preserve it.
20. Implement the score hierarchy outside the Orb.
21. Implement the complete Living MAXESS Orb.
22. Implement the MAXESS Orbital Bead.
23. Implement score-reactive color, energy, and atmosphere.
24. Implement reveal sequence.
25. Implement full-bleed Groove escape.
26. Implement responsive behavior.
27. Implement accessibility.
28. Implement reduced motion.
29. Implement safe data/preview handling.

### STAGE D — SELF-QA

30. Inspect the source against every contract item.
31. Render the module in the intended Groove-compatible environment.
32. Inspect the actual visual result.
33. Inspect desktop/widescreen.
34. Inspect tablet.
35. Inspect mobile.
36. Inspect reduced motion.
37. Inspect keyboard/focus behavior.
38. Verify real data behavior.
39. Verify preview behavior.
40. Verify the Orbital Bead is unmistakable and continuously visible.
41. Verify no white sidebars or narrow container.
42. Verify no `RESULT PENDING` hero content.
43. Verify the score is visible outside the Orb.
44. Verify Naya has not been regressed.
45. Verify no console-breaking errors.

### STAGE E — ADVERSARIAL QA

46. Ask: `WHY IS THIS NOT A 10?`
47. Score human experience, information hierarchy, visual design, copy, data correctness, interaction, responsive behavior, accessibility, performance, editability, preservation, and conversion role.
48. Identify every material weakness.
49. Classify each weakness KEEP / CHANGE / IMPROVE / REMOVE.
50. Fix every material weakness without disturbing protected components.
51. Re-render.
52. Inspect again.
53. Repeat this adversarial loop until no material defect remains.

### STAGE F — RELEASE GATE

54. Run the complete acceptance checklist again.
55. Confirm the module is actually Groove-ready.
56. Commit the completed module to `SoulSchoolAcademy/MaxRESULTS`.
57. Verify the committed source is the final rendered source.
58. Prepare the direct raw GitHub source link.
59. Only after every required item is complete, respond to the human.

## 18 — SEND GATE / ZERO-PREMATURE-RESPONSE RULE

The agent MUST NOT send a progress response merely because code exists.

The agent MUST NOT stop at a technically valid prototype.

The agent MUST NOT present an incomplete build for human QA when the internal checklist has not been completed.

The agent MUST NOT say “done” when only the source has been written.

The agent may respond only after:

`BUILD → RENDER → INSPECT → SCORE → CLASSIFY → ITERATE → RE-RENDER → VERIFY → COMMIT → DELIVER`

is complete.

If an internal tool, environment, or access limitation prevents completion of a required gate, the agent must clearly state the exact blocked gate rather than pretending it was completed. It must not fabricate visual QA.

## 19 — REQUIRED FINAL RESPONSE

Only after the send gate passes, respond with:

**STATUS** — concise statement of what was completed.

**PROVEN** — what was actually rendered/tested/verified.

**REMAINING** — only items that genuinely require human visual approval or are externally blocked.

**RECOMMENDATION** — Naya's best next move.

**NEXT PROMPT** — an exact copy/paste prompt for the next action.

**VIEWABLE SOURCE** — the direct raw GitHub source link immediately available for Groove testing.

Never leave the human asking: “Okay… now what?”

## 20 — RELEASE STATE

Valid states:

`DRAFT → BUILT → RENDERED → VISUALLY REVIEWED → IMPROVED → HUMAN APPROVED → FROZEN`

The implementation agent may not declare Section 01 HUMAN APPROVED or FROZEN. Human visual review remains the final gate.
