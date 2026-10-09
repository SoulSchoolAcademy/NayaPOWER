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
