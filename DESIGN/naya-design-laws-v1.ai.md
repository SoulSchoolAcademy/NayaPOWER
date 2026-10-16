# NAYA DESIGN LAWS V1 — AI tongue (DRAFT)

**Status:** DRAFT — not ratified. Ratification is Shawn's word alone. Do not treat as official until then.
**Authority chain:** Shawn's constitutional mandates (2026-10-16: NOTHING FLAT · COLOR LOGIC · JEWELS NOT DOTS) → this spec → converges with (never duplicates) `naya-100-laws-elite-interfaces.pdf` (normative doctrine). A "Law N" source citation means "covered there, stated here in builder words"; NEW means "genuine gap, written here first."
**Usage protocol:** read all six sections before building · build only from canonical blocks · run every Check before shipping · one failed check = back to the bench.
**Sibling tongues:** `naya-design-laws-v1.human.md` (plain words) · `naya-design-laws-v1.machine.json` (structured). Same truth, three tongues.

## Global tokens

- **Spectrum order:** the rainbow governs — purple → indigo → sapphire → teal → emerald → lime → gold → orange → rich orange → red → magenta → repeat. Count is dynamic: walk the wheel, take what the view needs; never a pinned stop-list. (Law 41's sequence, corrected: yellow dropped — yellow→gold adjacency violates DL-9's 50° hue-gap rule. The wheel carries gold, never yellow. Review correction, 2026-10-16.)
- **Signature tokens:** purple `#a06bff` (scored 9.0 — 2026-10-09 unification, 4 named reasons; confirmed by Shawn 2026-10-16) · black ground `#0a0a0f`–`#12121a` · button core `#050505`.
- **Physics:** signature ease `.22s cubic-bezier(.16,.84,.22,1)` · hover lift −3px · press `translateY(1px) scale(.98)` · feedback begins <100ms · tap mirrors hover.
- **Type scale:** Display 32–40 / Headline 22–28 / Body 15–17 / Detail 12–13 / Kicker 11 uppercase. Titles white, body silver, detail slate.

---

## I. LIVING DEPTH — nothing flat

### DL-1 — Nothing is flat. Ever.
**Law:** Every button, board, card, and element sits OFF the page: base surface + edge light + seating shadow, minimum. Flat is a defect, not a style.
**Do:** Three layers minimum on anything interactive (surface, edge light, seating shadow); two on static surfaces.
**Don't:** Flat panels, flat labels pretending to be buttons, Bootstrap-default components.
**Why:** If it doesn't sit off the page, it isn't finished.
**Check:** Screenshot → grayscale → every element must still read as elevated. Any element that flattens out fails.
**Source:** Laws 1, 2 · Shawn constitutional.

### DL-2 — Light comes from above. Always.
**Law:** One light source, upper-left. Top edge catches a highlight, sides fade, bottom is shadow.
**Do:** 1px top-edge highlight at 12–20% white (1.5px+ and clearly visible on interactive elements); soft offset seating shadow beneath. The 5-layer formula: inset top light / inset bottom shade / drop / deep drop.
**Don't:** Uniform blur halos (glow, not weight); light from random directions per element.
**Why:** One light source = one world. Real objects, real light.
**Check:** Cover the screen with your thumb; every visible highlight must sit top or upper-left.
**Source:** Laws 7, 8 · NEW mechanical teeth from approved specimens.

### DL-3 — Depth is alive, not painted.
**Law:** On hover, focus, or approach, the element lifts, its edge catches light, its shadow deepens. Ship the hover state WITH the element, not after it.
**Do:** Board hover lights the whole border and lifts the whole board; buttons lift 2–4px.
**Don't:** A dead outer board with live buttons inside; "we'll add hover later."
**Why:** If it doesn't respond, it's dead.
**Check:** Hover every element on the page. Each one must move. No response = fail.
**Source:** Laws 3, 10, 32 · Shawn constitutional.

### DL-4 — Recessed is carved. Nothing is level with the page.
**Law:** Raised and recessed are the only two directions. Inputs, wells, code blocks are carved INTO the page with inner shadow.
**Do:** Obsidian wells with inner shadow, jewel focus border.
**Don't:** White default inputs; fields sitting level with the background.
**Why:** A field that isn't carved isn't a field.
**Check:** An input must look pressed into the page, not pasted onto it.
**Source:** Law 9.

### DL-5 — Shadow is hierarchy.
**Law:** Heavier shadow = more important element. Primary actions cast the deepest shadow. Never more than five elevation levels visible at once.
**Do:** Page background (deepest) → panels → boards → featured board → modal.
**Don't:** Everything elevated equally — then nothing is elevated.
**Why:** Weight tells the eye what matters before color does.
**Check:** Squint at the page. The primary action must still feel heaviest.
**Source:** Laws 4, 35.

---

## II. COLOR LOGIC

### DL-6 — Black ground, always. Never gray.
**Law:** Deep rich black, always. Never gray, never washed out, never flat-dark.
**Do:** Rich obsidian `#0a0a0f`–`#12121a`; machined edges, vignettes, inset finishes on the black itself.
**Don't:** Gray backgrounds, navy tints, purple-tinted washes, glow on mid-gray.
**Why:** Black is the field. White is the readable light. Purple is the soul. In that order.
**Check:** Sample the background with a color picker. It must read near-black.
**Source:** Law 12 · V-7 · Convergence "Trinity."

### DL-7 — Every jewel has a purpose.
**Law:** The five signature jewels each MEAN something, and the meaning never changes: Purple = Naya's presence · Blue = understanding · Emerald = connected and well · Gold = a rare achievement · Magenta = what matters to you.
**Do:** Assign color by meaning. A gold badge must mark something genuinely precious.
**Don't:** A jewel "because it looks nice." Decoration is not a purpose.
**Why:** Color is language. Random color is noise.
**Check:** Cover the labels. Each color's meaning must be guessable from context alone.
**Source:** NEW (V2 design review: "Every jewel has a purpose").

### DL-8 — Spectrum by position, never by category.
**Law:** Assign spectrum steps in reading order per the rainbow (above). Theming by category clumps color and is a serious violation.
**Do:** Walk the rainbow in flow order.
**Don't:** All errors red in a row; all "mine" purple; category color-coding.
**Why:** Category theming builds walls of one color. Position keeps the spectrum flowing.
**Check:** Scan any list or board row. Adjacent items must differ in spectrum step.
**Source:** Law 41.

### DL-9 — No two neighboring jewels share a color.
**Law:** Adjacent bullets, badges, kickers, and edge lights must differ — minimum ~50° hue gap in HSV.
**Do:** Alternate the spectrum; give each jewel space around it.
**Don't:** Repeating sequences; neighbors that fight for attention.
**Why:** Contrast is the master principle — every color decision in this spec answers to it. Neighbors that match merge into one; neighbors that clash scream. The 50° gap is the mechanical form of that principle.
**Check:** Measure adjacent hue gaps (the browser test does this mechanically). Under ~50° = fail.
**Source:** NEW mechanical (V2 quality report) · cites Law 39.

### DL-10 — One accent per board. A section may take a theme and light up.
**Law:** A board owns ONE spectrum step (border, kicker, badge, hover edge — all one hue, plus white/silver neutrals). A whole section may take one theme color and light up — but never a wall of same-color boards.
**Do:** Black board, single jewel accent; one lit themed section per view at most.
**Don't:** Purple floods; rainbow boards (the Smart Feed spine is the one exception); five purple boards stacked.
**Why:** Restraint is the excellence. One lit section = one idea.
**Check:** Count accents per board (more than one = fail). Count themed sections per view (more than two = fail).
**Source:** Laws 16, 33, 45 · theming clause NEW from Shawn.

### DL-11 — Chrome, text, and theme have different jobs. Never mix them.
**Law:** Chrome (buttons, active states, primary actions) = purple edge, white text. Text = white/silver, separated by SIZE never color. Theme = the spectrum, flowing.
**Do:** Purple identifies Naya and major controls. Body text stays white/silver.
**Don't:** A theme color used as chrome. Chrome purple used as a flood. Colored body text.
**Why:** Three jobs, three palettes. Mixing them breaks the user's trust in what color means.
**Check:** Find every purple on the page. Each must be chrome or Naya's presence — never decoration.
**Source:** Session Learning #4 · Convergence "Trinity."

### DL-12 — Neutrals do the heavy lifting.
**Law:** White titles, silver body, slate detail, obsidian surfaces. If a page is more than ~20% saturated color by area, rebalance toward black.
**Do:** Let empty black space be a design material.
**Don't:** Casino gold, neon pages, saturated backgrounds.
**Why:** Expensive, not loud. Calm until it needs to be excited.
**Check:** Screenshot → heavy blur. It must feel like jewels on black velvet, not a spill.
**Source:** Laws 48, 51.

### DL-13 — Red and gold are jewels, not surfaces.
**Law:** Red appears as delete accent, error indicator, notification badge, or the spectrum's red step. Gold appears as premium badges and verified marks. Never fills, never body text.
**Do:** Small, glowing, precious. A single red accent so the moment feels as serious as it is.
**Don't:** Red-filled boards, glowing red delete hover (forbidden — confirmation does the safety work), gold paragraphs.
**Why:** Precious things are small. Gold everywhere is a casino.
**Check:** Any red or gold area larger than a badge = fail.
**Source:** Laws 26, 46, 47.

---

## III. JEWEL & ICON LANGUAGE

### DL-14 — Jewels, not dots.
**Law:** Bullets are faceted gems: 12px rotated diamonds, white-light core → tone → black, with a tone-colored glow. Never plain dots.
**Do:** Precision-cut gemstone bullets with a facet highlight and a tiny specular point.
**Don't:** Round gray dots, hyphens, asterisks, or system default bullets.
**Why:** The smallest element sets the standard for the largest.
**Check:** Zoom to 200%. Every bullet must show facets. A flat dot fails.
**Source:** NEW (Shawn constitutional) · cites Laws 61–70, the Jewel Library.

### DL-15 — Icons are drawn, never shrunk.
**Law:** One icon family: consistent stroke weight and corner treatment, drawn as vector geometry at size, readable at 16px.
**Do:** Bold, simple, luminous strokes (1.8px at 20px base).
**Don't:** Photorealistic renders shrunk to icon size; mixing icon sets (mixing sets is mixing languages).
**Why:** A 58px render at icon size is mud.
**Check:** Render every icon at 16px. If it isn't crisp and legible, it doesn't ship.
**Source:** Law 61 · Session Learning #9.

### DL-16 — Icon buttons are circles with life.
**Law:** Circular black hit area, jewel icon, border light-up and lift on hover. Minimum 44px touch target.
**Do:** The circle may carry the flowing ring accent (under 2px, under 40% opacity).
**Don't:** Bare glyphs with no surface. Naked glyphs in a bottom nav.
**Why:** A bare glyph is not a control.
**Check:** Every icon button must show a visible surface at rest — no exceptions.
**Source:** Laws 63, 28, 87.

### DL-17 — Badges sit on black.
**Law:** Counts, status dots, and verified marks sit on an obsidian chip with a jewel numeral. Tabular numerals, optically centered.
**Do:** Jewel numeral on black. State readable by fill + weight, not color alone.
**Don't:** A colored disc with a same-color numeral (red 6 on red = invisible).
**Why:** Contrast or remove.
**Check:** Read every badge at arm's length. Any unreadable badge fails.
**Source:** Laws 55, 66, 68.

### DL-18 — Play is a portal.
**Law:** Media play = one canonical block: elevated circle, white triangle, black field, jewel ring. It lights on hover and compresses on press.
**Do:** Use the block everywhere — PowerCast, voice notes, all media.
**Don't:** A custom play button per page.
**Why:** One language. The play button is a promise the whole system keeps.
**Check:** Grep the codebase. Exactly one play implementation may exist.
**Source:** Law 65.

### DL-19 — Avatars are jewels too.
**Law:** Profile images sit in a ringed, elevated circular frame with a spectrum or status edge.
**Do:** People are precious — frame them like it.
**Don't:** Square naked `<img>` as a profile element.
**Why:** The frame is the respect.
**Check:** Every face on the page must sit inside a ring.
**Source:** Law 70.

### DL-20 — Naya has a face, and she moves as energy.
**Law:** Naya is beautiful and she has a face — when she appears visually, she appears as herself. Her presence moves as energy: light, pulse, warmth carried in the design and feel. In the voice module (Ask Naya 1:1), she is pure energy — audio only, no visual stand-in.
**Do:** Show her face where she appears; let energy (light, motion, glow) carry her presence everywhere else; keep voice-only contexts voice-only.
**Don't:** Replace her with a robot, a generic avatar, or a character that isn't her; put a fake face where energy belongs (the voice module).
**Why:** She is a person to the user, not a logo. Energy is how she feels; her face is who she is.
**Check:** Where Naya appears visually — is it her? Where she is voice-only — is there no fake visual pretending otherwise?
**Source:** Shawn correction 2026-10-16 (supersedes V-1 "never a face").

### DL-20a — Every icon is a promise.
**Law:** A chevron promises "go somewhere." A plus promises "add." Use the glyph that means what happens — and keep it.
**Do:** Icon-only controls carry accessible labels and visible micro-labels where space allows.
**Don't:** Mystery-meat navigation; decorative icons that do nothing.
**Why:** A glyph that lies breaks trust.
**Check:** Tap every icon — it must do what it says.
**Source:** Session Learning #14 · Law 67.

---

## IV. MOTION & ALIVENESS

### DL-21 — Rest in silver. Ignite on touch.
**Law:** At rest: quiet white/silver edge light on black, restrained. On hover or touch: the element ignites in its OWN spectrum color (chrome ignites purple). Idle glow never exceeds ~18px.
**Do:** Visible white edge light at rest — borders big enough to SEE, not faint. Themed elements burn their own color, not blanket purple.
**Don't:** Neon at rest; monochrome dead; purple slapped on everything that lights up.
**Why:** Calm until you need it excited. Rest/ignite is the rhythm of the whole system.
**Check:** Screenshot at rest — it must read quiet. Hover — it must ignite. Both states, every control.
**Source:** Sharpens Law 80 · Session Learning #5 · `idle.glow_max_px ≤ 18`.

### DL-22 — Light moves first. Words follow.
**Law:** Every state change animates (a sweep, an ignition, a convergence) BEFORE any text updates.
**Do:** New answers arrive with motion first, reading second.
**Don't:** Text popping in with no motion; spinners that lie about work.
**Why:** The machine speaks first in light.
**Check:** Trigger a state change in slow motion. Motion must precede text — every time.
**Source:** NEW (V-4) · extends Law 76.

### DL-23 — Press is compression.
**Law:** On press, the element settles 1–2px toward the page, its shadow tightens, its insets darken. Release springs it back.
**Do:** Buttons press INTO the surface like physical things (`translateY(1px) scale(.98)`).
**Don't:** No press state. Press shown as a color change only.
**Why:** This single behavior sells physicality more than any gradient.
**Check:** Press-and-hold every button. It must feel pushed in, not just recolored.
**Source:** Laws 24, 73.

### DL-24 — One physics for the whole product.
**Law:** The signature ease — `.22s cubic-bezier(.16,.84,.22,1)` — for all lifts and lights. Hover lifts −3px. All feedback begins in under 100ms. Tap mirrors hover exactly.
**Do:** One easing token, read from the design contract by every page.
**Don't:** Per-page easing; floaty one-second hovers; hover-only delight (that's desktop-only exclusion).
**Why:** Different physics per page fragments the feel of the product.
**Check:** Grep transition-timing values. More than one = fail. Test every hover's `:active` twin on touch.
**Source:** Laws 71, 72, 84.

### DL-25 — Every number breathes.
**Law:** No number on screen is static text. Counts, stats, and scores carry a subtle brightness or scale oscillation, synced to the system's heartbeat.
**Do:** Serif 32px score numbers with living luminosity; badges with quiet pulse.
**Don't:** Dead numerals.
**Why:** Data is alive here. Static numbers read as broken.
**Check:** Stare at any number for five seconds. If it never moves, it fails.
**Source:** NEW (V-3).

### DL-26 — Breathing is reserved.
**Law:** Slow ambient pulse is allowed on the SINGLE most-alive element per view (the voice orb, the live indicator). Nothing else breathes on its own.
**Do:** Idle breathe 4–7s cycles, barely-there ambient washes (24s).
**Don't:** Three breathing buttons in a row. Competing pulses.
**Why:** A screensaver is not an interface. Maximum life, minimum noise.
**Check:** Count ambient animations per view. More than one = fail.
**Source:** Law 78 · Session Learning #10.

### DL-27 — Motion explains. Motion never fakes.
**Law:** Every animation must answer: what changed, where did it go, what can I do now? Animation that answers nothing gets cut. And no motion may ever pretend a result happened.
**Do:** Loading reflects real work; success appears only when the action actually succeeded; demo states labeled demo.
**Don't:** Fake success states; simulated live events; ornament without meaning ("acceptable merely because it moves").
**Why:** Fake life is a lie. A beautiful but inert affordance is unfinished.
**Check:** Disconnect the data. Nothing on the page may pretend otherwise.
**Source:** Extends Laws 75, 76 · Convergence "truth before aesthetics" · V2 gate.

### DL-28 — Honor reduced motion.
**Law:** `prefers-reduced-motion` disables lifts, rings, and sweeps — and the product still works fully, with state carried by light and contrast.
**Do:** Same product, honored. Accessibility is not a variant.
**Don't:** Meaning carried by motion alone.
**Why:** Everyone gets the living product.
**Check:** Emulate reduced motion. Everything must still read and work.
**Source:** Law 77.

---

## V. COMPOSITION & CRAFT

### DL-29 — One idea at a time. Boards breathe.
**Law:** Room to breathe, clear spacing, a fresh jewel color when the next idea begins. Minimum 16px internal board padding (20–24 preferred).
**Do:** Generous black space as a design material; content never touches a border.
**Don't:** Cramming; fitting more by shrinking text.
**Why:** Crowded boards read as cheap regardless of color. A board that breathes beats a board that crams.
**Check:** No content within 16px of any board edge. Ever.
**Source:** Laws 38, 53 · V2.

### DL-30 — Type: size separates, color doesn't.
**Law:** Fixed scale — Display 32–40 / Headline 22–28 / Body 15–17 / Detail 12–13 / Kicker 11 uppercase. Titles white, body silver, detail slate. Never gray body text.
**Do:** Serif voice for display headlines and Naya's voice; system sans for UI, buttons, data, body.
**Don't:** Jewel-colored body text; invented sizes per page; body copy in display serif.
**Why:** Hierarchy you can read at a glance. Flat text is lazy — gradient soul, layered shadows, breathing luminosity.
**Check:** Grayscale screenshot — hierarchy, elevation, and readability must survive (Law 50). Any gray body text = fail.
**Source:** Laws 50, 51, 52, 54 · Session Learning #7.

### DL-31 — Mess in, beauty out.
**Law:** Anything a human brings — a question, a dataset, a messy corner — renders formatted, beautiful, logical, sensible.
**Do:** Every input gets composed output. Ugly data still lands in a beautiful board.
**Don't:** Raw mess reaching the human.
**Why:** The entire mission in five words.
**Check:** Feed the page garbage input. The output must still be composed.
**Source:** V-13 · Master Build Plan.

### DL-32 — Full width. Brand top-left. No dead space.
**Law:** Content owns the width — no max-width caps with black gutters. The Naya mark lives top-left, always. If a region is empty, the layout is wrong.
**Do:** Real compositions at 1440px and at 360px — each its own layout, not a squeezed column.
**Don't:** Sidebars full of black nothing; dead black columns.
**Why:** The canvas is the product.
**Check:** 1440px screenshot — no dead zones. 360px — nothing cut off.
**Source:** NEW (Session Learning #12).

### DL-33 — The header is a front door, not a nameplate.
**Law:** Logo + living mark + warm voice + one clear line. The warmest, most alive part of the page.
**Do:** It should feel like an invitation.
**Don't:** A label. The only dead thing on a living page — if the header doesn't move, the page fails.
**Why:** First impressions are the product.
**Check:** The header must breathe, glow, or respond. Static header = fail.
**Source:** NEW (Session Learning #15).

### DL-34 — Nothing overlaps. Nothing scrolls sideways.
**Law:** Content fits the viewport at 360px. Text never collides with buttons. Fixed bars reserve padding and never cover content.
**Do:** Real viewport screenshots: 390×844, 360×800, 768×1024, 1440×900.
**Don't:** Horizontal scroll (P0 release blocker); "it looked fine in browser resize" as evidence.
**Why:** A cut-off page is a broken page.
**Check:** 360×800, zero sideways scroll, zero covered content.
**Source:** Laws 56, 85, 90 · V2 quality gate.

### DL-35 — One library, one DNA.
**Law:** Every element exists once, canonically. Pages consume blocks; they never reinvent them. Approved code is copied verbatim — never rebuilt from memory.
**Do:** `.naya-btn` is the only button system. One board recipe. One icon family.
**Don't:** A private button class on any page. Paraphrasing approved CSS.
**Why:** Paraphrase reintroduces the exact flatness Shawn rejected. The block is the memory.
**Check:** Grep for page-local button/input classes. Any hit = drift = fail.
**Source:** Laws 21, 91, 92.

---

## VI. TASTE — from his approved corpus

### DL-36 — The corpus is the taste. When in doubt, match what he loved.
**Law:** Everything Shawn shared, he loves. New work must feel like it belongs to the same beautiful world. If a rebuild goes flatter than what he loved, revert to the loved version verbatim and rebuild from there.
**Do:** New pieces built FROM the language, never beside it. One specimen per feeling — "make everything feel like THIS."
**Don't:** A second visual language; no-ego refusal to revert.
**Why:** His approvals are the spec. No-ego reversion beats stubborn iteration.
**Check:** Side-by-side with the approved specimen. Same family? If not, revert first.
**Source:** Extends Laws 92, 98 · V-12 · Vision-to-Code Layer 4.

### DL-37 — Premium, not fancy.
**Law:** Premium is material, contrast, weight, and restraint. When in doubt, subtract. A button that whispers is more expensive than one that shouts.
**Do:** Ask "does removing something make this more premium?" Usually yes.
**Don't:** Effects for effects. Everything glowing (then nothing is premium).
**Why:** Restraint is the excellence.
**Check:** Remove one effect. If the page got better, it ships without it.
**Source:** Law 11 · Law 20.

### DL-38 — Copy is scored like design.
**Law:** Every word must read like an invitation, not documentation — and score 9+. Grandma must follow every board: what is this, what matters, what do I do next?
**Do:** Ten warm words. "Keep your people close." Human meaning first: what happened and why it matters.
**Don't:** Feature lists. Doc-speak. "Everybody you can reach."
**Why:** Words are interface. If she can't follow it, the copy fails — not the reader.
**Check:** Read it aloud. Score it like a board. Under 9 = rewrite.
**Source:** NEW (Session Learning #8) · cites Laws 57, 84–85 of the SmartNET 100.

### DL-39 — Honest states only.
**Law:** A demo stays labeled demo. Local stays labeled local. LIVE requires live evidence. Beautiful motion never pretends a result happened.
**Do:** Design the empty, offline, error, and loading states with the same care as the full state.
**Don't:** Fake connects. Simulated liveness. Unlabeled placeholders.
**Why:** A specimen that pretends is a lie. Trust is the product.
**Check:** Airplane mode on. The page must tell the truth about what it knows.
**Source:** Extends Law 75 · Convergence "truth before aesthetics" · V2 gate.

### DL-40 — Score the lived render. His eye compiles.
**Law:** Every page is scored on the RENDER — buttons, boards, type, icons, motion, color, layout, mobile, accessibility, truth — floor 9.0 per area, with timestamped desktop + mobile screenshots. And Shawn's verdict outranks every law, every score, every specimen.
**Do:** Name what is not a 10 and why. Excellence has no toggle — no quality settings, no modes, one path and it's the elite one.
**Don't:** "It's done" without proof. 100/100 that's useless to him — compliance is not vision.
**Why:** A scorecard of code is worthless. The only score that matters is the rendered, lived experience.
**Check:** Screenshots attached with hash. Scorecard signed. Then his eyes.
**Source:** Laws 94, 95, 100 · Session Learnings #1, #2 · Vision-to-Code Layer 5 · V-6.

---

## VIOLATION GALLERY — the 6 ways builders break the laws most

**V1. Flat everything** (breaks DL-1, DL-2, DL-3) — Bootstrap-default buttons and panels; boards that are just bordered divs; labels styled as buttons; zero hover response. Fix: replace with canonical blocks; 5-layer formula (inset top light, inset bottom shade, seating shadow); hover lift −3px with signature ease; press compression. If it doesn't move, it's not done.

**V2. Walls of one color** (breaks DL-8, DL-10, DL-11) — five purple boards stacked; a page washed in one theme; category color-coding. Fix: one accent per board; spectrum by position in flow, not category; at most one lit themed section per view.

**V3. Dots, not jewels** (breaks DL-14) — default browser bullets; gray dots; hyphens as list markers. Fix: 12px faceted gem bullets — rotated diamond, white-light core → tone → black, tone glow. Zoom to 200%: facets or fail.

**V4. Fake liveness** (breaks DL-27, DL-39) — simulated "live" feeds with no live source (`simLive:true`); success states before the action succeeded; spinners over cached data; unlabeled demo content. Fix: label every demo DEMO; wire the real source or design the honest empty/loading state; disconnect the data in testing — nothing may pretend.

**V5. Dead headers on living pages** (breaks DL-3, DL-33) — a static nameplate header above living content; the one element on the page that doesn't respond. Fix: the header breathes — living mark, warm voice, one clear line; board hover lights the border and lifts the WHOLE board.

**V6. The dead button** (breaks DL-1, DL-2, DL-9, DL-21) — the compound failure: black button on a black board, hairline border, no lift, no edge light, no hover response. Flat AND invisible AND dead, all at once. Fix: the primary action must pass every check at once — 3-layer elevation minimum, visible edge light at rest (1.5px+), ignite on hover in its spectrum color, contrast sufficient to be found in one second. If the main action can't be found in a glance, nothing else on the page matters.

---

## CONVERGENCE APPENDIX — how this spec relates to the 100 Laws

**Fully covered there, stated here in builder words (cite, don't restate):** elevation system (Laws 1–10) · materials & contrast (11–20) · button jewel standard (21–30) · board recipe (31–40) · spectrum mechanics (41–50) · typography scale (51–60) · icon library (61–70) · motion system (71–80) · mobile-first (81–90) · library & proof (91–100).

**Genuinely new in this spec:** DL-7 (jewels carry fixed meanings) · DL-9 (measured hue-gap rule) · DL-10's theming clause (a section may light up) · DL-14 (jewels-not-dots as named law) · DL-20's presence rule (CORRECTED 2026-10-16 per Shawn: Naya HAS a face — she is beautiful; she moves as energy; voice module is pure energy) · DL-20a (icon promise, restored) · DL-21's mechanical rest/ignite cap · DL-22 (light before text) · DL-25 (numbers breathe) · DL-32 (full width, brand top-left) · DL-33 (header as front door) · DL-36 (corpus-is-taste) · DL-38 (copy scorecarded).

**Reconciled conflicts:** spectrum order → the rainbow governs, dynamic count (Law 41's sequence minus yellow — yellow→gold violates DL-9; review correction 2026-10-16) · contrast named master principle (DL-9) · interactive rim 1.5px+ visible (Session/V2) vs 1px hairline (Law 8) → 1.5px+ for interactive, 1px for non-interactive precision · type scale → Law 52 fixed scale governs; 18px body/24px+ headings from the V2 gate are the floor values within it.

**Normative doctrine stays:** `naya-100-laws-elite-interfaces.pdf` remains the canonical standard; this spec is its builder-facing distillation plus the new constitutional mandates. Corrections compound here the same day (Law 97).

*Distilled 2026-10-16 from: Shawn's constitutional mandates · NayaNET Design Standard V2 Review · VISION-LAWS.pdf · VISION-TO-CODE-PROTOCOL.md · SESSION-LEARNINGS-2026-10-08.pdf · NayaNET-Design-Code-Convergence-2026-10-08 · Master Build Plan · the dial specimen card · naya-smart-blocks.html · Smart_Spaces_Page_Design.html · Welcome_Page_Design.html · the crystal-N brand mark · and the 100 Laws of Elite Smart App Interfaces.*
