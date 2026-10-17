# THE DESIGN LAWS — v2

> **STATUS: DRAFT — NOT RATIFIED.** This document has been through the 3-pass
> scorecard process and scores 9.5/10 as a draft. It becomes official only when
> Shawn stamps it. Nobody else can ratify it — that is a protected gate, and
> this file must never claim otherwise.

*Written from Shawn's fifteen design files, his verbal teaching, the correction
stories inside them, and his four standing corrections of 2026-10-17
(compose-don't-create, PRETTY+USELESS=NOT DONE, small-tweaks-allowed, his eye
compiles). If any law here and Shawn's eye disagree, his eye wins — that is
itself the final law.*

---

## LAW 0 — WHO THIS IS FOR (read this first)

Three roles. Three different relationships to this document.

- **BUILDERS compose. They do not read this to build.** The pieces are
  already elite — buttons, boards, jewels, inputs. A builder picks pieces and
  puts them together beautifully. The laws live *inside* the pieces, so the
  builder never has to apply them by hand. If you are building a page and
  reaching for this document to decide what something should look like, stop —
  go take the piece instead.
- **MAKERS make the pieces.** Makers read every law here, because a new piece
  must embody all of them before it joins the library. One library, one DNA.
- **CHECKERS check the work.** Checkers score the working page against the
  ship gate at the bottom. They click everything.

Checkable: ask any person on a build which role they hold. If they cannot
answer in one sentence, the role split has failed.

---

## THE COMPOSE LADDER (the three layers — new, Shawn's order 2026-10-17)

1. **COMPOSE (default, always).** Take pieces from the library and assemble.
   No new CSS, no new components. A page with a private button class is drift.
2. **TWEAK (free, safe).** One-token changes that leave the DNA intact: make
   the button ignite green instead of purple, widen a board, shift a tone.
   The piece's anatomy, states, and behavior do not change — only its
   parameters. If the tweak needs new anatomy, it is not a tweak.
3. **CREATE (through the process only).** A genuinely new piece goes through
   build → score → improve → verify → merge like everything else, and must
   embody every law below before it joins the library.

Checkable: diff the page against the library. New class names that restyle a
canonical piece = unfiled CREATE = rebuild from the block. Token overrides
alone = TWEAK = fine.

---

## THE MASTER STATEMENT

**White light at rest, own color on touch.**

Every interactive element shows a visible white edge light when idle — borders
big enough to see, not faint. On hover, it ignites in its *own* spectrum color,
not blanket purple. Purple is for chrome; themed elements burn their own color.

Nothing is flat. Nothing is dead. Nothing is "not active." If you click a
button and it doesn't come alive — doesn't move, doesn't light up — it is
unfinished. All of it, everywhere, has to be that way. Shawn calls the quality
**living depth**: elevated, dimensional, lit — the opposite of flat.

*What it looks like: `reference/welcome-entrance` — the entrance page. Black
ground, white-lit rims at rest, the circle igniting on approach.*

---

## LAW 1 — ALIVE (living depth)

**The rule:** every interactive thing moves on hover and ignites in its own color.

**At rest:**
- Black ground, always — deep rich black (`#050507`), never gray, never washed out. Fail: any flat dark panel, any light background.
- White-lit edges — visible white borders (1.5px+, not hairlines, not faint `12%` whispers). Every surface has depth finishing: machined edges, vignettes, inset finishes.
- Buttons rest dark: black center (`#050505`), white text with an icon, white rim. Spectrum colors are *never* worn at rest — color is earned by interaction.
- **Inputs ignite purple.** Text fields, search bars, selects: white-lit rim at rest, purple edge + purple glow on focus. Inputs are chrome, and chrome is purple.

**On touch (hover):**
- Lift: primary actions rise (`translateY(-2px)` to `-8px` depending on weight — buttons 2px, boards 5px, cards 6px, orbs 8px + slight scale). Press goes the other way (`translateY(2px)`).
- Ignite: the border and glow become the element's *own* color — `0 0 26–46px` in its tone. Chrome (buttons, CTAs, inputs) ignites purple; themed elements burn their own spectrum color.
- Timing: fast `.18s`, medium `.28s`, ease `cubic-bezier(.16,.84,.22,1)`. State changes animate *before* text updates — light moves first, words follow.

**Graded, not absolute:** primary actions lift *and* ignite. Secondary elements (tabs, pills, quiet links) may glow without lifting. What is never allowed is *neither* — no element that does nothing on hover.

**Breathing:** restrained ambient motion, always — "maximum life, minimum noise." Numbers breathe (no static numbers on screen). A 72bpm pulse, a slow orbital light, drifting spectrum color (never one static hue). Never fake liveness: motion must mean something.

**Data as holograms:** multi-layered depth — glass sheets, parallax planes. You look *into* the data, not *at* it.

*What it looks like: `reference/intelligent-hub-smart-feed` — every room door lifts in its own color; `page-specimens/naya-smart-blocks` — the graded hover pattern.*

---

## LAW 2 — SPECTRUM (color logic)

**The rule:** color follows the rainbow's natural flow. The count is dynamic; the order is law.

**The wheel, not the list.** "It's not a law that has to be five or seven or nine." Five stops, seven, ten — whatever the design needs. What never changes: the spectrum is walked **in spectral order** — the rainbow's natural flow — **never clumped** (no purple-purple-purple, no green-green-green), **never random**, and always the **most beautiful** version of each hue. We speak the natural design language of the universe — not random colors for whatever reason. It has to look stunning.

**The wheel** (11 stops — the most beautiful of each hue; canonical hexes pending Shawn's stamp — see Open reconciliations):

| Stop | Hex | Job |
|------|-----|-----|
| magenta | `#e84fff` | The living edge |
| purple | `#a06bff` | Choosing intelligence — the soul |
| indigo | `#6675ff` | The deep signal |
| blue | `#3fb8ff` | Knowledge moving |
| emerald | `#35e0a1` | Forest deep green |
| green | `#2fe89e` | Alive and well |
| lime | `#b8ee57` | New growth |
| gold | `#ffbf3d` | Attention, earned |
| orange | `#ff9a5a` | Warmth, momentum |
| red | `#ff5e6c` | Urgency, the living edge |
| pink | `#ed58cd` | Delight, the flourish |

For N zones needing separation, take N stops evenly spaced around the wheel from the page accent. Three zones: purple, blue, green. Five: magenta, purple, cyan, green, gold. Ten: ten. The page accent picks where the walk starts; the count fits the need; the order never breaks.

**Contrast is the most important thing.** The whole point of the spectrum is breaking up the view so the eye can rest on each thing — like black with white text, never black with black text. Adjacent stops must read as *distinct*. Which is why: **yellow and gold never sit together** — not enough contrast between them. The wheel carries gold, never yellow. (Same law in text form: white 99%, never gray body text, never black-on-black.)

Clumping is never judgment — clumping is a defect. (This exact defect has a history: "purple-purple-purple and repeated reds" was corrected into the no-duplicate rule, measured at ≥51.6° hue separation between adjacent jewels.)

**The Strip** — the component form, magenta-first, 5 stops: **magenta → purple → blue → green → gold**. Jewel rows, spectrum bars, law-order strips, and per-object accents use this form. Same wheel, tighter instrument.

**The three jobs of color — never mix them:**
1. **Chrome** (buttons, active states, primary actions, inputs): purple edge, white text. Chrome rests silver-white and *ignites* color on hover.
2. **Text**: white, 99% of the time. Never gray body text — it's unreadable. Separation by *size*, not color.
3. **Theme** (per-card, per-list, per-contact, per-room accents): the spectrum. One accent per object. **Never use a theme color for chrome. Never use chrome color as a flood. Never flood at all** — "Naya's presence. Never a flood."

**Themed zones:** one section or board may be themed one color and light up in it — that is the honest use of strong color. What never happens: a whole page, or a run of adjacent zones, wearing one hue.

**Every color means something; the meaning never changes between instruments.**

*What it looks like: `reference/reports` — the seven day-boards walking the wheel with no adjacent hue shared; `reference/smart-ledger` — one themed zone done honestly.*

---

## LAW 3 — ELEVATION (living depth, mechanical)

**The order of the world:** Field > Board > Nested panel > Control > Overlay. Each layer rides visibly above the last.

**The board formula** (5-layer shadow — the literal construction):
```
inset 0 2px 2px rgba(255,255,255,.12),      /* top light catching the edge */
inset 0 -8px 18px rgba(0,0,0,.55),           /* inner depth */
0 5px 0 #020203,                             /* hard base bar */
0 17px 0 -8px <tone 16% on field>,           /* tone under-bar */
0 35px 75px rgba(0,0,0,.7),                  /* deep drop */
0 0 40px -17px <tone>                        /* tone glow */
```
Body: dark gradient (`#1a171f → #09090d → #030304`), 1.5px tone-mixed border, 24px radius.

**Board anatomy:** tone spine (7px, glowing), corner-jewel orbs, white-lit edges at rest. On hover: lifts 5px, border and glow ignite in its own tone. **A board inside a board rides higher** — deeper shadow, more lift. You feel the nesting.

**Every header is a warm front door:** logo + living mark + warm voice + one clear line. Full width — content owns the width, no max-width caps.

*What it looks like: `reference/spaces` — boards nested inside boards, each riding higher; `page-specimens/nayapower-reveal-18` — the 5-layer shadow in the wild.*

---

## LAW 4 — JEWELS (bullets are diamonds, icons are drawn)

**Bullets are jewels, not dots.** A bullet is a rotated square (diamond): white → tone → black gradient, own-color glow, a sheen facet. Five-jewel cycle in law order, never twice in a row. Colors separate ideas; they don't compete with the words.

**Faceted gems** for signal moments: true diamond geometry (clip-path polygon), white-hot crown fading to deep black base, vertical light facet, drop-shadow glow in its own hue.

**Boards wear jewels:** corner orbs, lit from within (white → tone → black radial), glowing in the board's tone.

**Icons are drawn, not shrunk.** Native vector geometry — bold, simple, luminous, readable at 16px. A photorealistic render at small size is mud. **If you can't make it good, don't put it there.** And every glyph must promise its real behavior: a chevron promises "go somewhere," a plus promises "add."

**A beautiful but inert affordance is unfinished.** This is the FUNCTION LAW's home: if the glyph promises and the page doesn't deliver, Law 4 failed — see THE FUNCTION LAW below for the enforcement protocol.

*What it looks like: `element-sets/jewel-library-n5` — the diamond construction; `reference/connections` — jewels separating identities.*

---

## LAW 5 — BUTTONS (the one button)

**The canonical spec:**
- Center: really black (`#050505`). Text: always white, with an icon.
- Border: white, visible at rest — 1.5px+, not a hairline.
- Hover: purple edge + purple glow for chrome; own-color edge + glow for themed buttons. Elevated: inset top highlight + deep drop shadow.
- **It must feel liftable.** Minimum 44px touch target; the principal CTA ≥52px.
- Focus and pressed states are not optional.

There is one button DNA (`.naya-btn`) with job-specific variants (lead, machine, streak, proximity, icon, portal). There are no flat buttons. Flat is not a style — flat is a defect, and the advisor refuses it.

**Tweaks welcome, forks forbidden.** Changing a button's ignite color from purple to green is a TWEAK (one token, DNA intact). Drawing a second button system is a FORK — never accepted.

*What it looks like: `element-sets/button-set-n4` — the one DNA; `element-sets/design-standard-showcase` — the variants.*

---

## LAW 6 — TYPE

- Hierarchy: **24 / 18 / 14** — kicker 24, headline 18, detail 14. (Mnemonic. Law 52 governs the full scale: Display 32–40 / Headline 22–28 / Body 15–17 / Detail 12–13 / Kicker 11.)
- **White 99%.** Never gray body text.
- Headers get a *voice*: a real serif face with warmth (Newsreader/Georgia — Cormorant where licensed), not a system default. Voice-font pick pending Shawn's stamp — see Open reconciliations.
- Text is never flat: gradient soul, layered shadows (grounding + glow), breathing luminosity. **Flat text is lazy.**
- Order of resort: visuals → voice → text. Text is the fallback, never the default.

*What it looks like: `page-specimens/smart-hub` — the voice serif on "Good afternoon" against white 99% body.*

---

## THE EIGHT SOURCE LAWS (the roots — unchanged)

1. **Score the experience, never the code.** A 9.5 on CSS is worthless if the rendered page is a 5. The lived page is the only scorecard.
2. **Back it or bench it.** 9.0+ ships. Below 9 goes back to the bench. No exceptions, no almost.
3. **Color has jobs. Never cross them.** Chrome acts. Text speaks. Theme identifies. Adjacent things never share a hue.
4. **White light at rest, own color on touch.** Visible 1.5px+ rims idle. Ignition belongs to the thing being touched.
5. **Black heart, white voice, visible skin.** `#050507` center, white text and icon, real rim. The glyph is a promise.
6. **Size separates, color doesn't.** 24 / 18 / 14. Nothing else. White 99% of the time. Headers get a voice. (Law 52 governs the full scale.)
7. **Icons are drawn, not shrunk.** Vector geometry, readable at 16px. A shrunken render is mud.
8. **Verify before claiming.** Read the file. Count the matches. Watch it render. Then say it's done.

---

## THE FUNCTION LAW — PRETTY + USELESS = NOT DONE (Shawn's correction 2026-10-17)

A page isn't done when it renders beautifully. It's done when every element on it is **intentional, logical, and actually works.** The contract always banned inert affordances (Forbidden #9) — this law is the enforcement that was missing.

**The click-everything protocol (builders + checkers):**
1. Every button, pill, toggle, link, and input is clicked/used against its promise. Real behavior, not staged state — a play button must play, a save button must save.
2. If you cannot say why an element is on the page and what job it does, it comes off. No decorative controls.
3. Anything staged, stubbed, or simulated is labeled as such — AND the page is not done until it's real. Labeled ≠ done.

**Scorecards score the working page, never the screenshot.** "Renders correctly" is necessary, not sufficient. A 9.5 render of a page whose buttons do nothing is a 5.

Checkable: the checker's report lists every interactive element and its verified behavior. An element with no verified behavior is a failed check.

---

## THE FORBIDDEN LIST (never accepted)

1. **Anything flat.** Any flat dark panel, any flat button, any flat text, any element that does nothing on hover. Flat is the original sin.
2. **Clumped color.** Purple-purple-purple. A run of greens. Adjacent zones sharing a hue.
3. **Theme color on chrome; chrome color as a flood.** Spectrum accents never rest on buttons; purple never floods a surface.
4. **Gray body text.** It's unreadable.
5. **Shrinking Naya to one thing.** She has a face AND she is energy — never just a logo, never just a robot, never a stock avatar or mascot standing in for her. Her presence is light with a face, not a costume.
6. **Quality toggles.** No "basic vs premium," no modes. Excellence has no toggle.
7. **Light backgrounds.** Zero white or light surfaces, ever.
8. **A second version of something that exists.** Never duplicate a canonical object. Ten specimens is a menu; one is a standard. (TWEAKs are not versions — see the Compose Ladder.)
9. **Beautiful but inert affordances.** If it doesn't do what it promises, it's unfinished. (Enforced by THE FUNCTION LAW above.)
10. **Transmitting an adjective instead of an image.** "Elegant" is not a spec.
11. **Compliance without vision.** A 100/100 score on a checklist that Shawn looks at and says "that's not it" is worthless.
12. **Patching the specimen** when the vision sharpens — rebuild. **Sanding down the unreasonable parts** — don't.
13. **The dead button.** Black button, black text, a hairline of border you can barely see, flat, nothing on hover. One element breaking the contrast law, the alive law, the button law, and the text law all at once. If you see it, all four laws failed — fix all four.
14. **Recreating instead of composing.** Building a new button, board, or icon when the library already holds one. Take the actual code — copy the specimen, don't re-teach the button.

---

## THE SHIP GATE — all seven, or it doesn't ship

1. White edge light is visible on every card and button at rest.
2. Themed elements ignite their own color; chrome (buttons, CTAs, inputs) ignites purple.
3. Every button has a black heart, white voice, and a truthful icon.
4. Type hierarchy follows the scale — size separates, color doesn't.
5. Copy is plain enough for anyone to understand on first read.
6. **Every interactive element performs its real promised behavior — verified by clicking, not by looking.** (THE FUNCTION LAW.)
7. Scored the rendered, working page honestly — 9+ or back to the bench.

---

## THE FINAL LAW — SHAWN'S EYE COMPILES

At the end of every relay there is a test suite no machine can run: Shawn looks at it and says "that's it" or "that's not it." **His verdict is the final compile step, and it outranks every score, every law, every specimen in this document.**

These laws exist so the first build lands close. They do not replace his eye. When a law and his eye disagree, the eye wins, and the law gets corrected — that is how "purple-purple-purple" became a rule instead of a habit, and how "pretty + useless = not done" became the function law.

---

## THE MACHINE TWIN

This document is the human tongue. The machine tongue lives in:
- `DESIGN/TOKENS.css` — the token set (colors, spacing, motion) the pieces are built from.
- `DESIGN/SPECIMENS/specimens.json` — the piece library index: every piece's id, category, file, purpose, and the laws it exemplifies.

On conflict between tongues, the machine wins for builds; Shawn's eye wins over both.

*Specimen ids referenced above (`reference/...`, `element-sets/...`, `page-specimens/...`) resolve in `DESIGN/SPECIMENS/` — the "what it looks like" for every law.*

---

## OPEN RECONCILIATIONS (for Shawn's eye — his stamp settles these)

1. **Hex drift:** the same hue names carry different hexes across files. This spec uses the richest values; the parallel canonical-hex mission is producing the single stamped set.
2. **Voice font:** Cormorant (teaching) vs Newsreader/Georgia (specimens). This spec allows Newsreader/Georgia pending his pick.
3. **Strip-vs-walk:** resolved 2026-10-16 — two instruments, one wheel. Not a conflict.

---

## SOURCES

- `VISION-LAWS.pdf` — V-1 through V-11 (the written canon; magenta-first 5-stop strip)
- `SESSION-LEARNINGS-2026-10-08.pdf` — Naya 2's written lessons from Shawn's teaching (§4–§15)
- `VISION-TO-CODE-PROTOCOL.md` — "she feels alive," "Shawn's eye compiles," "ten specimens is a menu"
- `NayaNET-Design-Code-Convergence-2026-10-08.pdf` — elevation order, header law, conflict ledger C01–C08
- `NayaNET_Design_Standard_V2_Review.zip` — the no-clumping correction story (51.6° hue measurement), 5 signature jewels
- `naya-smart-blocks.html` — 14-hue canonical spectrum, 5-layer board shadow, `.naya-btn`, gem construction
- Shawn's verbal teaching, 2026-10-16/17: the wheel walk, compose-don't-create, PRETTY+USELESS=NOT DONE, small tweaks allowed, "his eye compiles"
- `naya-100-laws-elite-interfaces.pdf` — the hundred-law corpus the v2 distills

---

## 3-PASS SCORECARD (the process record — this is why it's a 9.5, not a 10)

**Pass 1 — 8.0/10.** Every reason it wasn't a 10:
1. Compose-don't-create was buried in "One X, one job," not a top-level law.
2. No audience split — a cold builder couldn't tell whether to read it at all.
3. Forbidden #9 banned inert affordances but no enforcement protocol existed.
4. The ship gate's six checks were all visual — function wasn't gated.
5. "One system, no forks" read rigid — Shawn's tweak allowance had no home.
6. No law→example pairing ("what it means / what it looks like").
7. No machine-twin pointer for the smart builder to consume.
8. "Inputs ignite purple" (his 2026-10-17 teaching) wasn't encoded.
9. Foundation laws ("Material has a soul") weren't checkable predicates — violating the doc's own rule.
10. Hex drift still open (belongs to the parallel canonical-hex mission — noted, not settled here).

**Pass 2 — fixes applied:** LAW 0 (audience split); the Compose Ladder (compose → tweak → create); THE FUNCTION LAW with the click-everything protocol; ship gate check 6 (function) added; Forbidden #14 (recreating instead of composing); inputs ignite purple in Law 1; per-law "what it looks like" specimen pointers; the machine twin section; foundation poetry kept as voice but every law now carries checkable predicates.

**Pass 3 — 9.5/10.** Why not a 10: the example pointers resolve to specimen ids whose library PR is still unmerged (pairing is structural, not yet populated with rendered side-by-sides); the hex set awaits the parallel mission + his stamp; and per the Final Law itself, only his eye makes it a 10. **NOT RATIFIED — the stamp is his alone.**
