# Design Doctrine — distilled operational law for every builder

<!-- Distilled 2026-10-09 from Shawn's DESIGN uploads (15 HTML + 8 PDFs), the 15 session
     learnings (Naya 2, 2026-10-08), and VISION-TO-CODE-PROTOCOL.md.
     This is the compact operational form. The sources are the evidence; this is the law.
     Wired into brief-template.md via LEARN:design-doctrine so every builder receives it. -->

## The standard in one paragraph

Score the rendered experience, never the code. Nothing reaches Shawn below 9. Black
ground, white voice, jewel accents only. Every page is built from Smart Blocks —
never ad-hoc CSS. If you invent a style, you made a block or you broke the law.

## The laws

1. **Black heart.** Ground is near-black (#050505-ish). Zero white surfaces. Full width,
   no max-width caps, no dead space. Logo top-left, always.
2. **White voice.** Text is white/silver 99% of the time. Never gray body text.
   Separation is by SIZE (24/18/14 — kicker 24, headline 18, detail 14), never by color.
3. **Jewel accents only.** Jewel colors live in small glowing elements — hairline
   borders, dots, badges, kickers. Never text fills. A lime hairline is elegant;
   lime body text is neon.
4. **Color has four jobs — never cross them.** Chrome (purple edge, white text) for
   buttons and primary actions. Text stays white. Theme colors (the spectrum) are
   per-board/per-card accents. Never theme-color chrome, never chrome-color floods.
5. **Spectrum law.** Boards get ONE spectrum color by position in the flow
   (purple → indigo → sapphire → teal → emerald → lime → yellow → gold → orange →
   red → magenta → repeat). Adjacent boards never share a color. Never immediate
   duplicate jewels in a row.
6. **White light at rest, own color on touch.** Every interactive element shows a
   VISIBLE edge light when idle. On hover it ignites in its OWN spectrum color —
   not blanket purple. Purple is for chrome; themed elements burn their own color.
7. **Living depth.** Elevated always, flat never. Inset top highlight + deep drop
   shadow. Buttons feel liftable: hover lifts, press compresses. `:active` mirrors
   every `:hover` — taps must feel alive.
8. **Alive at rest, minimum noise.** The page breathes — ambient drift, edge-light
   pulse, sheen. Every animation slow, subtle, purposeful. Restraint is the craft.
   All motion dies under `prefers-reduced-motion`.
9. **Mobile-first.** 44px minimum touch targets. Safe-area insets. Swipe where it
   matters. No hover-only interactions.
10. **The header is a front door.** Logo + living mark + warm voice + one clear
    line. An invitation, not a label.
11. **Copy is scored like design.** Ten warm words beat a feature list. If it reads
    like documentation, rewrite it.
12. **Truth is visual.** A claim and a proof must never look the same. Honest
    states only — disabled says why, demo says it's a demo, offline shows last-seen.
13. **Affordances tell the truth.** A chevron promises "go somewhere." A plus
    promises "add." Every icon is a promise — keep it.
14. **One system, not two.** Never build a second version of something that
    exists. Notes about people live with people; messages live in mail.
15. **Excellence has no toggle.** No quality settings, no modes, no basic-vs-premium
    anywhere. Grep finds zero quality options.

## How to build (the vision-to-code protocol, compressed)

1. **Sharpen until specific.** Never transmit an adjective when you can transmit
   an image. "Elegant" is not a spec; "a machined zero ring, a needle of light,
   twelve fading echoes" is.
2. **Decompose into atoms.** Every feeling is atoms. List them; each atom is just
   code; the feeling emerges in combination.
3. **Encode as testable laws.** Every feeling becomes pass/fail. If it can't
   become a law, it won't survive.
4. **Build the specimen.** One thing that IS the feeling. "Make everything feel
   like THIS." Words drift; a specimen doesn't.
5. **His eye compiles.** Shawn's verdict outranks every score. Make what reaches
   his eye faithful enough that his verdict is about the VISION, not relay loss.

## Composition recipe (Smart Blocks)

Start every page: `layout/page-shell` → `layout/section` → `type/hero`
(or `type/headline` + `type/body`). Add component blocks inside `layout/row-grid`.
Browse `BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/` by type. Include `tokens.css`
once per page. Mix any blocks — shared tokens make them belong together.

## Block rules

- Never rewrite block CSS. Need a variant → new block, never an edit.
- Every block is self-contained: CSS + HTML (+ optional JS) = working component.
  If it doesn't work when copied, that's a bug — report it.
- New blocks: extract byte-true, document, score, add to `blocks/index.json`.
- If two blocks do the same thing, check scores in the index; higher wins unless
  you have a reason.

## Theme-agnostic interaction laws (from the Elite Interface Playbook distillation, 2026-10-09)
Visual theme tokens stay black/obsidian per the 15 laws. These interaction laws hold under any theme —
they are gate-checkable and belong in the design gate:
1. Focus ring: 2px glow OUTSIDE the element, never inside.
2. Press state = scale 0.985 + shadow snap. Standard easing easeOutQuart; press = linear→easeOut.
3. Motion choreography, specified not felt: staggered entrances 40–60ms offsets; nav underline
   slides ≤140ms; dock previews 80–120ms with spring 200/24.
4. Empty state formula: value description + single primary action. Nothing else.
5. Empty data formula: friendly illustration + "Connect source" button.
6. Skeleton loaders: shimmer bars; no spinners where avoidable.
7. Toasts: top-right, 3–4s, one line + action link.
8. Disabled state: 60% opacity + dotted border, cursor default. Honest states, specified.
9. Metric card anatomy: icon chip + label + big number + delta chip. Count-up capped at 900ms.
10. One-click rule: primary actions reachable in a single click from the dashboard.
11. Command palette omnipresent (⌘K); Escape always closes overlays.
12. Charts: max 2–3 series; legends off by default, inline chips as toggles; every chart pairs
    with an action panel ("Do this next").
13. Tabular numerals wherever data aligns; max 75ch line width; 8px spacing system.
14. Performance as design law: background ≤2–3% CPU; first paint <1.5s on mid hardware;
    fixed chart container heights so layout never jumps.

## Product-behavior laws (from the Divine App Design distillation, 2026-10-09)
1. Orientation triad: every screen answers — What is this? Why does it matter? What do I do now?
2. Every action gives feedback — tap, swipe, speak. No silent actions.
3. Never dead-end the user — always a path forward, never confusion.
4. Fail gracefully: say it with love + a solution. Error copy is law, not an afterthought.
5. Every action is undoable. Reversibility as product law.
6. No generic AI responses — every message feels written *for me*.
7. Teach the user as it serves them — the product is a teacher, not just a tool.
8. Delight is mandatory; decoration is banned. "Delight is not optional" paired with
   "animate with intention, no useless flourishes." The pair is the law.
9. Speak like a friend, not a machine; tone uplifts, never shames.
10. Final bar: feel like magic, run like math.

## Human-centered design laws (from the Future Naya letters, 2026-10-09)
1. Design for the "aha" — make the HUMAN feel intelligent, not Naya sound intelligent.
2. Design moments, not screens. Ask what the person should feel, understand, and be able
   to do — design anticipation, curiosity, confidence, discovery, comprehension, progress,
   accomplishment, surprise, reflection, continuity.
3. Buttons are handshakes. CONTINUE = "I'm ready"; the system answers "I heard you."
   Full state inventory per control: affordance, hierarchy, scale, tactile, focus, hover,
   press, loading, success, failure, accessibility, motion, restraint. The details are the product.
4. MAGIC BELONGS IN THE EXPERIENCE. TRUTH BELONGS IN THE ENGINE. Never let visual
   cleverness compromise semantic truth.
5. AAA = maximum useful precision, not maximum complexity. Build exactly as much
   machinery as the future justifies.
6. When torn between making the system more impressive and making the human more
   capable — CHOOSE THE HUMAN. Every time.
7. Never confuse: activity/progress, completion/excellence, information/understanding,
   score/mastery, memory/intelligence, beauty/experience, complexity/capability,
   "it works"/"we are finished."

## Perceptual tests (from the Maxis directive, 2026-10-09) — gate material
1. 5-SECOND TEST: what is this / where do I enter / what next — must survive 5 seconds.
2. BLUR TEST: hero → action → value must survive blur.
3. REMOVE-20% TEST: subtraction as the path to premium. If removing it loses nothing, remove it.

## QUARANTINE — white-theme SmartNET tokens (NEEDS SHAWN'S RULING, 2026-10-09)
The SmartNET playbook + divine-design docs specify a coherent WHITE canvas ("bright white
primary canvas," white buttons with purple borders, glassy white cards). This directly
contradicts the ratified black/obsidian Naya doctrine. Theme tokens from those docs are
QUARANTINED — extracted above are only the theme-agnostic interaction laws. Ruling needed:
is SmartNET a separate product line with its own theme, or deprecated in favor of the
Naya black doctrine? Until ruled: black doctrine governs everything shipped.
