# THE DESIGN LAWS

*The ultimate spec. What is good, what is not, what is accepted, what is never accepted.
Written from Shawn's fifteen design files, his verbal teaching, and the correction stories inside them.
If any law here and Shawn's eye disagree, his eye wins — that is itself the final law.*

---

## The master statement

**White light at rest, own color on touch.**

Every interactive element shows a visible white edge light when idle — borders big enough to see, not faint. On hover, it ignites in its *own* spectrum color, not blanket purple. Purple is for chrome; themed elements burn their own color.

Nothing is flat. Nothing is dead. Nothing is "not active." If you click a button and it doesn't come alive — doesn't move, doesn't light up — it is unfinished. All of it, everywhere, has to be that way. Shawn calls the quality **living depth**: elevated, dimensional, lit — the opposite of flat.

---

## LAW 1 — ALIVE (living depth)

**The rule:** every interactive thing moves on hover and ignites in its own color.

**At rest:**
- Black ground, always — deep rich black (`#050507`), never gray, never washed out. Fail: any flat dark panel, any light background.
- White-lit edges — visible white borders (1.5px+, not hairlines, not faint `12%` whispers). Every surface has depth finishing: machined edges, vignettes, inset finishes.
- Buttons rest dark: black center (`#050505`), white text with an icon, white rim. Spectrum colors are *never* worn at rest — color is earned by interaction.

**On touch (hover):**
- Lift: primary actions rise (`translateY(-2px)` to `-8px` depending on weight — buttons 2px, boards 5px, cards 6px, orbs 8px + slight scale). Press goes the other way (`translateY(2px)`).
- Ignite: the border and glow become the element's *own* color — `0 0 26–46px` in its tone. Chrome (buttons, CTAs) ignites purple; themed elements burn their own spectrum color.
- Timing: fast `.18s`, medium `.28s`, ease `cubic-bezier(.16,.84,.22,1)`. State changes animate *before* text updates — light moves first, words follow.

**Graded, not absolute:** primary actions lift *and* ignite. Secondary elements (tabs, pills, quiet links) may glow without lifting. What is never allowed is *neither* — no element that does nothing on hover.

**Breathing:** restrained ambient motion, always — "maximum life, minimum noise." Numbers breathe (no static numbers on screen). A 72bpm pulse, a slow orbital light, drifting spectrum color (never one static hue). Never fake liveness: motion must mean something.

**Data as holograms:** multi-layered depth — glass sheets, parallax planes. You look *into* the data, not *at* it.

---

## LAW 2 — SPECTRUM (color logic)

**The rule:** color walks the spectrum in law order. Adjacent things never share a hue.

**The Walk** — zones down a page, purple-first, 7 stops:

> **purple → blue → green → gold → orange → red → magenta →** (back to purple)

| Stop | Hex | RGB (for glow math) | Job |
|------|-----|---------------------|-----|
| purple | `#a06bff` | `160,107,255` | Choosing intelligence — the soul |
| blue | `#3fb8ff` | `63,184,255` | Knowledge moving |
| green | `#2fe89e` | `47,232,158` | Alive and well |
| gold | `#ffbf3d` | `255,191,61` | Attention, earned |
| orange | `#ff9a5a` | `255,154,90` | Warmth, momentum |
| red | `#ff5e6c` | `255,94,108` | Urgency, the living edge |
| magenta | `#e84fff` | `232,79,255` | The living edge, demonstration |

The page accent picks *where the walk starts*; every zone after it takes the next stop. Green is never followed by green. Purple is never followed by purple. The walk is not set in stone — judgment applies to what the situation needs — but clumping is never judgment. Clumping is a defect. (This exact defect has a history: "purple-purple-purple and repeated reds" was corrected into the no-duplicate rule, measured at ≥51.6° hue separation between adjacent jewels.)

**The Strip** — the component form, magenta-first, 5 stops: **magenta → purple → blue → green → gold**. Jewel rows, spectrum bars, law-order strips, and per-object accents use this form. Same hues, same order, tighter instrument.

**The three jobs of color — never mix them:**
1. **Chrome** (buttons, active states, primary actions): purple edge, white text. Chrome rests silver-white and *ignites* color on hover.
2. **Text**: white, 99% of the time. Never gray body text — it's unreadable. Separation by *size*, not color.
3. **Theme** (per-card, per-list, per-contact, per-room accents): the spectrum. One accent per object. **Never use a theme color for chrome. Never use chrome color as a flood. Never flood at all** — "Naya's presence. Never a flood."

**Themed zones:** one section or board may be themed one color and light up in it — that is the honest use of strong color. What never happens: a whole page, or a run of adjacent zones, wearing one hue.

**Every color means something; the meaning never changes between instruments.**

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

---

## LAW 4 — JEWELS (bullets are diamonds, icons are drawn)

**Bullets are jewels, not dots.** A bullet is a rotated square (diamond): white → tone → black gradient, own-color glow, a sheen facet. Five-jewel cycle in law order, never twice in a row. Colors separate ideas; they don't compete with the words.

**Faceted gems** for signal moments: true diamond geometry (clip-path polygon), white-hot crown fading to deep black base, vertical light facet, drop-shadow glow in its own hue.

**Boards wear jewels:** corner orbs, lit from within (white → tone → black radial), glowing in the board's tone.

**Icons are drawn, not shrunk.** Native vector geometry — bold, simple, luminous, readable at 16px. A photorealistic render at small size is mud. **If you can't make it good, don't put it there.** And every glyph must promise its real behavior: a chevron promises "go somewhere," a plus promises "add." **A beautiful but inert affordance is unfinished.**

---

## LAW 5 — BUTTONS (the one button)

**The canonical spec:**
- Center: really black (`#050505`). Text: always white, with an icon.
- Border: white, visible at rest — 1.5px+, not a hairline.
- Hover: purple edge + purple glow for chrome; own-color edge + glow for themed buttons. Elevated: inset top highlight + deep drop shadow.
- **It must feel liftable.** Minimum 44px touch target; the principal CTA ≥52px.
- Focus and pressed states are not optional.

There is one button DNA (`.naya-btn`) with job-specific variants (lead, machine, streak, proximity, icon, portal). There are no flat buttons. Flat is not a style — flat is a defect, and the advisor refuses it.

---

## LAW 6 — TYPE

- Hierarchy: **24 / 18 / 14** — kicker 24, headline 18, detail 14.
- **White 99%.** Never gray body text.
- Headers get a *voice*: a real serif face with warmth (Newsreader/Georgia — Cormorant where licensed), not a system default.
- Text is never flat: gradient soul, layered shadows (grounding + glow), breathing luminosity. **Flat text is lazy.**
- Order of resort: visuals → voice → text. Text is the fallback, never the default.

---

## THE FORBIDDEN LIST (never accepted)

1. **Anything flat.** Any flat dark panel, any flat button, any flat text, any element that does nothing on hover. Flat is the original sin.
2. **Clumped color.** Purple-purple-purple. A run of greens. Adjacent zones sharing a hue.
3. **Theme color on chrome; chrome color as a flood.** Spectrum accents never rest on buttons; purple never floods a surface.
4. **Gray body text.** It's unreadable.
5. **A face, an avatar, a robot, a character standing in for her.** Never.
6. **Quality toggles.** No "basic vs premium," no modes. Excellence has no toggle.
7. **Light backgrounds.** Zero white or light surfaces, ever.
8. **A second version of something that exists.** Never duplicate a canonical object. Ten specimens is a menu; one is a standard.
9. **Beautiful but inert affordances.** If it doesn't do what it promises, it's unfinished.
10. **Transmitting an adjective instead of an image.** "Elegant" is not a spec.
11. **Compliance without vision.** A 100/100 score on a checklist that Shawn looks at and says "that's not it" is worthless.
12. **Patching the specimen** when the vision sharpens — rebuild. **Sanding down the unreasonable parts** — don't.

---

## THE FINAL LAW — SHAWN'S EYE COMPILES

At the end of every relay there is a test suite no machine can run: Shawn looks at it and says "that's it" or "that's not it." **His verdict is the final compile step, and it outranks every score, every law, every specimen in this document.**

These laws exist so the first build lands close. They do not replace his eye. When a law and his eye disagree, the eye wins, and the law gets corrected — that is how "purple-purple-purple" became a rule instead of a habit.

---

## Sources

- `VISION-LAWS.pdf` — V-1 through V-11 (the written canon; magenta-first 5-stop strip)
- `SESSION-LEARNINGS-2026-10-08.pdf` — Naya 2's written lessons from Shawn's teaching (§4–§15; the 8-stop verbal walk, the button spec, the icon law)
- `VISION-TO-CODE-PROTOCOL.md` — "she feels alive," "Shawn's eye compiles," "ten specimens is a menu"
- `NayaNET-Design-Code-Convergence-2026-10-08.pdf` — elevation order, header law, conflict ledger C01–C08
- `NayaNET_Design_Standard_V2_Review.zip` — quality report (the no-clumping correction story, 51.6° hue measurement), 5 signature jewels
- `naya-smart-blocks.html` — 14-hue canonical spectrum, 5-layer board shadow, `.naya-btn`, gem construction (all in code)
- `NayaPOWER-Reveal__18__0_ry3n.html`, `powercast__14.html`, `Smart_Spaces_Page_Design.html`, `Welcome_Page_Design.html` — specimens (graded hover pattern, room-door spectrum walk, 108-jewel orbit)
- `SPECIMEN-CARD-dial.pdf` — dial atoms (72bpm, breathing scale, drifting spectrum)
- Shawn's verbal teaching, 2026-10-16: "purple blue green gold orange red magenta… nothing flat, nothing not active… living depth"

## Open reconciliations (for Shawn's eye)

1. **Strip vs Walk start:** the written V-10 starts magenta; the verbal teaching starts purple. This spec keeps both as different instruments (strip = components, walk = page zones). If they should be one, say the word.
2. **Hex drift:** the same hue names carry different hexes across files (purple `#9d75ff` vs `#a06bff`, magenta `#d86cff` vs `#e84fff` vs `#ed58cd`). This spec uses the richest values; a single canonical hex set still wants your stamp.
3. **Voice font:** Cormorant (teaching) vs Georgia/Newsreader (specimens). This spec allows Newsreader/Georgia.
