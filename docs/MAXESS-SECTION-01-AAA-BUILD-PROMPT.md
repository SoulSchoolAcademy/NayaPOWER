# MAXESS RESULTS — SECTION 01 AAA BUILD PROMPT

Status: ACTIVE — REBUILD DIRECTIVE
Repository: `SoulSchoolAcademy/MaxRESULTS`
Purpose: authoritative prompt for rebuilding Section 01 after human visual QA identified a technically valid but visually wrong implementation.

## 01 — TAKE THE LEAD

Do not merely obey the most literal implementation request.

Understand the intended human experience first. Read the active MAXESS directives, the section architecture, the visual language, the approved Naya assets, the button/icon contracts, and the authoritative result/data contract before writing code.

If an implementation path is likely to produce a weaker result, stop and recommend the better path with a short explanation before proceeding.

The goal is not to make a section that technically exists.

The goal is to create the strongest first screen of the MAXESS Results experience that can be visually reviewed and approved by a demanding human.

## 02 — PRIMARY HUMAN OUTCOME

The first screen must communicate almost instantly:

**THIS IS MY RESULT.**

**THIS IS MY AI SCORE.**

**NAYA HAS LOOKED AT IT.**

**I WANT TO SEE WHAT IT MEANS.**

The experience is a personal reveal, not a sales page, dashboard, SaaS screen, report card, or collection of promotional copy.

The user should feel recognition, curiosity, trust, and anticipation.

## 03 — AUTHORITATIVE SOURCES

Before implementation, inspect and obey:

1. `docs/MAXESS-MASTER-DESIGN-DIRECTIVE-V4.md`
2. `docs/MAXESS-AAA-REFERENCE-SPEC.md`
3. `docs/MAXESS-AAA-PAGE-MAP.md`
4. `docs/MAXESS-CHANGE-LEDGER.md`
5. `docs/HMC-MAXIMUS-BUTTON-AND-ICON-SYSTEM.md`
6. `NAYA-NITRO-VISUAL-BUILD-PROTOCOL.md`
7. current Section 01 source only as a reference for useful implementation details
8. `nayanet.xyz` and `maxess.nayanet.xyz` as visual/brand references when accessible
9. `results.nayanet.xyz` as the current live Results reference, but not as an authority when it conflicts with the active design directive

The active directive has precedence over legacy implementation.

Do not blindly preserve historical code.

## 04 — SECTION SCOPE

Build only:

**SECTION 01 — NAYA ARRIVAL + AI SCORE**

Do not build Section 02.
Do not recreate the entire Results page.
Do not pull the historical 8,000-line Results source into the new architecture.
Do not add unrelated sections, cards, reports, pathways, membership blocks, or sales content.

Section 01 must be self-contained and ready to attach to Section 02 later.

## 05 — VISUAL NORTH STAR

The primary visual object is the **Living MAXESS Orb**.

The Orb is not decoration. It is the first visual expression of the user's AI capability.

The Orb must feel:

- dimensional;
- luminous;
- intelligent;
- alive;
- calm;
- premium;
- cinematic;
- organic;
- unmistakably MAXESS.

It must NOT feel like:

- a generic CSS circle;
- a gaming dashboard;
- a progress meter;
- a stock AI animation;
- a neon toy;
- a collection of arbitrary effects.

## 06 — SCREEN COMPOSITION

Use a true widescreen, full-viewport hero composition.

The first screen must intentionally occupy the available desktop viewport rather than appearing as a narrow centered webpage inside excessive empty margins.

Preferred composition:

LEFT / UPPER SUPPORT:
minimal MAXESS identity only if needed.

CENTER:
the Living MAXESS Orb and the user's score.

NAYA:
placed ABOVE or immediately adjacent to the score/orb as a compact conversational presence, not as a large sales card.

BOTTOM / LOWER EDGE:
minimal continuation cue only if necessary.

Do not create a three-column sales layout.
Do not place a large text block beside the Orb.
Do not create a large rectangular Naya marketing card on the side.
Do not fill the screen with explanatory paragraphs.

The Orb owns primary attention.
Naya owns the human relationship.
The score owns the information hierarchy.
Everything else is subordinate.

## 07 — HERO COPY CONTRACT

Use extremely little copy.

Primary label:

**YOUR AI SCORE**

Primary value:

**[REAL SCORE]**

Stage:

**[REAL MASTERY STAGE]**

Naya conversation should be short and human:

**Hi. I've looked at your results.**

**This isn't your judgment. It's your map.**

Primary action:

**LISTEN TO NAYA**

Do not invent additional marketing copy.
Do not use phrases such as “your capability has a shape,” “your results are ready,” or other generic hero language unless explicitly approved.
Do not duplicate the score in multiple places.
Do not explain the entire report in Section 01.

Section 01 creates the desire to continue; later sections deliver the explanation.

## 08 — NAYA PRESENTATION

Naya must appear as a trusted intelligent partner in a compact conversational treatment.

Use the approved Naya asset from the repository. Do not invent or substitute a random portrait.

The Naya treatment should visually resemble a beautiful, restrained conversation moment rather than a sales card.

Required:

- approved Naya portrait;
- short greeting;
- short map framing;
- one LISTEN TO NAYA action;
- clear visual relationship to the Orb.

The Naya element must never compete with the Orb.

## 09 — LIVING MAXESS ORB

The Orb must contain these deliberate layers:

1. atmospheric field;
2. outer halo;
3. layered translucent orbital rings;
4. **MAXESS ORBITAL BEAD**;
5. score arc / score energy;
6. luminous shell;
7. internal energy field;
8. dark dimensional core;
9. score number;
10. score label;
11. mastery stage.

The implementation must create real depth through geometry, light, opacity, layering, restrained blur, scale, and motion.

Do not fake dimensionality with one giant radial gradient.

## 10 — MAXESS ORBITAL BEAD — MANDATORY

This was a critical missed requirement and must never be omitted.

The small luminous ball travelling around the outside of the Orb is a named identity component:

**MAXESS ORBITAL BEAD**

It continuously travels around the primary Orb on a clearly visible orbital path.

It must be:

- visually distinct from the ring itself;
- small enough to feel elegant;
- bright enough to remain visible;
- luminous but not flashing;
- score-aware in color;
- spatially separated from the Orb edge;
- smooth in motion.

Target desktop size: 10–16px.
Target mobile size: 8–12px.

Target orbit radius: approximately 100–108% of the Orb radius.

Target duration: approximately 8–12 seconds.

It must remain present throughout normal motion.

When Naya is speaking, it may increase brightness and halo subtly.

Reduced motion:
stop positional travel and retain a static luminous bead with non-animated glow.

## 11 — SCORE COLOR ENGINE

The Orb must be driven by the actual score from `window.MAXESS_RESULT`.

Use smooth interpolation rather than hard visual jumps.

Required progression:

0–49: red spectrum
50–59: red → orange
60–74: orange → yellow
75–84: yellow → green
85–89: green → cyan/blue
90–94: blue → violet
95–100: violet → magenta

Use the approved MAXESS semantic palette from the master directive as the implementation authority.

The score should influence:

- Orb accent color;
- halo intensity;
- energy intensity;
- orbital bead color;
- subtle atmospheric energy;
- restrained motion intensity.

Never sacrifice text contrast for score color.

## 12 — SCORE REVEAL

The final score must not simply appear as a static number at first paint.

Use a short, elegant reveal:

IDLE / DARK
→ Orb activates
→ orbital energy awakens
→ score resolves
→ mastery stage appears
→ Naya becomes present

Keep the sequence brief enough that the user is never forced to wait for information.

The final score must become immediately readable.

Do not use excessive counting effects, fireworks, confetti, gaming effects, or long loading sequences.

## 13 — DATA CONTRACT

Authoritative source:

`window.MAXESS_RESULT`

Never fabricate a production score.
Never create a competing scoring engine.
Never hard-code a production result.

Expected data may include:

- `overallScore`
- `band`
- `dimensions`
- other authoritative MAXESS result metadata

If valid production data is unavailable, use a deliberate safe state that clearly communicates that the result is not yet available.

Development fixtures must never masquerade as production data.

## 14 — ARCHITECTURE

The module must be self-contained.

Use one clear DOM root.
Use one clear initialization path.
Use namespaced classes and variables.
Avoid global pollution.
Avoid unnecessary libraries.
Avoid duplicate event listeners.
Avoid uncontrolled observers.
Avoid animation loops that are not bounded.

The module must be safe to mount once and safe to re-render without duplicated behavior.

Section 02 must be attachable without rewriting Section 01.

## 15 — RESPONSIVE COMPOSITION

Desktop/widescreen is a first-class design state, not a stretched mobile layout.

Required inspection targets include:

- 1440px;
- 1280px;
- 1024px;
- 768px;
- 600px;
- 480px;
- 414px;
- 390px;
- 375px;
- 360px;
- 320px.

On desktop:
Orb should be large and dominant.
Naya remains compact.
Composition should use the viewport effectively.

On mobile:
Orb remains the hero.
Naya moves into a compact conversational arrangement without becoming a sales card.
Typography remains readable.
No horizontal scrolling.
No clipped Orb.
No collision between bead, Orb, score, Naya, or CTA.

## 16 — ACCESSIBILITY

Required:

- semantic heading hierarchy;
- accessible Orb description;
- real button semantics;
- visible keyboard focus;
- adequate contrast;
- minimum touch target sizing;
- no color-only meaning;
- reduced-motion support;
- no animation required to understand the score.

## 17 — PERFORMANCE

Use CSS transforms/opacity for animation where possible.
Avoid expensive continuous filters over huge surfaces.
Keep particle count intentionally bounded.
Do not create thousands of DOM particles.
Prefer CSS/SVG layers where they produce the same visual result more efficiently.

## 18 — GROOVE REQUIREMENT

The deliverable must be directly usable in a Groove HTML/embed environment.

Do not return a tiny test snippet.
Do not return pseudocode.
Do not return a conceptual mockup.
Do not return a renderer that only proves that a circle can appear.

Produce the complete production-quality module required to render the intended Section 01 experience.

The source length is not a target. Quality and completeness are the target. However, a suspiciously small implementation should trigger an immediate self-review because the visual contract contains substantial geometry, state, motion, responsive behavior, accessibility, data handling, and interaction requirements.

## 19 — MANDATORY QUALITY LOOP

Before presenting the module:

1. Read the active directives again.
2. Map every requirement to implementation.
3. Build the complete section.
4. Render it in the intended environment.
5. Inspect the actual visual output, not just the source.
6. Ask: **WHY IS THIS NOT A 10?**
7. Identify visual, UX, copy, architecture, and data weaknesses.
8. Fix every meaningful weakness found.
9. Render again.
10. Inspect widescreen, desktop, tablet, and mobile.
11. Inspect reduced motion.
12. Inspect keyboard focus.
13. Verify the real data contract.
14. Verify no console-breaking errors.
15. Verify the Orbital Bead is present and visibly orbiting.
16. Verify the Naya presentation is compact, conversational, and subordinate to the Orb.
17. Verify the screen does not resemble a sales page.
18. Verify there is no unnecessary hero copy.
19. Verify the score is visually dominant.
20. Only then prepare the Groove-ready artifact.

## 20 — OSCAR QUESTIONS

Before calling it ready, answer:

- Does this feel like a personal reveal?
- Is the Orb unmistakably the hero?
- Is the score instantly understood?
- Does the Orb feel alive rather than decorative?
- Can I clearly see the MAXESS Orbital Bead?
- Does Naya feel like someone who has looked at my result?
- Does Naya feel like a trusted partner rather than a salesperson?
- Is there too much text?
- Is anything competing with the Orb?
- Does the desktop composition use the full screen beautifully?
- Does mobile preserve the same hierarchy?
- Is anything generic?
- Is anything merely decorative?
- Is there anything the user does not need yet?
- Would I proudly show this first screen to thousands of people?

If the answer to a material question is no, continue iterating.

## 21 — RELEASE STATE

Do not call the section FROZEN merely because the code works.

Valid states:

DRAFT
→ BUILT
→ RENDERED
→ VISUALLY REVIEWED
→ IMPROVED
→ HUMAN APPROVED
→ FROZEN

The human visual review is the final gate for Section 01.

## 22 — REQUIRED RESPONSE AFTER BUILD

Every execution must end with:

**STATUS** — what changed.

**PROVEN** — what was actually tested/rendered.

**REMAINING** — what still needs human review.

**RECOMMENDATION** — what Naya believes is the best next move.

**NEXT PROMPT** — the exact prompt the human can paste to continue.

**VIEWABLE SOURCE** — the direct raw GitHub source link, immediately available for Groove testing.

Never leave the human asking “Okay… now what?”

The visual result is the primary truth.

---

# EXECUTION COMMAND

**NAYA NITRO — TAKE THE LEAD.**

Using the active MAXESS directives and this Section 01 contract, rebuild Section 01 as an extraordinary personal AI Score reveal.

Do not preserve weak implementation merely because it already exists.

Do not add invented copy.
Do not add unnecessary sections.
Do not create a sales page.
Do not omit the MAXESS Orbital Bead.
Do not omit real score binding.
Do not omit responsive behavior.
Do not omit reduced motion.
Do not omit accessibility.
Do not stop at technically valid code.

Build → Render → Inspect → Ask why it is not a 10 → Improve → Render again → Deliver the Groove-ready source.

Do not move to Section 02 until Section 01 has been visually reviewed and approved.
