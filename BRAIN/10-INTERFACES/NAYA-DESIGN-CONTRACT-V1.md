# NAYA DESIGN CONTRACT v1.2
**Status:** CANDIDATE — amending Naya posts per §AMENDMENT; Shawn ratifies.
**Ratified:** v1.1 on 2026-10-03 by Shawn Vibert (Human Director)
**Amended:** v1.2 draft 2026-10-08 by Naya 2 — hardened from the Connections rebuild session.
**Purpose:** The visual signature, interaction language, and design philosophy of Naya. So Shawn never has to repeat himself.

---

## 1. COLOR LANGUAGE

### Dominant (always present)
- **Black** (`#0a0a0e`) — backgrounds, buttons, depth
- **White** (`#ffffff`) — text, light, idle glow
- **Purple** (`#9d75ff`, `#8a5cff`) — Naya's signature, primary actions

### Spectrum (accents, never dominant)

Color has three distinct jobs. Do not use one job's rule for another.

**1. Chrome** — buttons, active states, primary actions. Purple edge, white text.
Never a theme color. Never a flood.

**2. Text** — white, 99% of the time. Separation by SIZE, never by color.
Never gray body text. Never colored text for emphasis.

**3. Theme** — per-contact, per-list, per-card accents. The spectrum, flowing:
**purple → blue → green → yellow → gold → orange → red → magenta → purple.**
Each themed element burns its OWN color. Never blanket one color across all.

### Tokens

- Magenta (hot pink) `#ed42c4`
- Purple `#8a5cff` (Naya's signature; also `#9d75ff`)
- Indigo `#6675ff`
- Cyan `#3ca8ff`
- Emerald `#35e39b`
- Forest emerald (deep green) `#2e9e6a`
- Lime `#b8ee57`
- Yellow `#ffd45a`
- Gold `#e8c766`
- Orange `#ff8c42`
- Red `#ff5e6c`

**Law:** Purple/black/white are PROMINENT. Spectrum colors are complementary accents. Gold/yellow is restrained — semantic accents, never dominant text.

**Active intelligence:** Intelligent blocks are dynamic, so the color flow is dynamic — it depends on what the content is. Always use the richest, most vibrant colors. Everything should look like jewels, alive.

---

## 2. THE LIGHTING STANDARD

**Shawn's universal rule for all interactive elements:**

- **Idle (not hovered):** White light. Visible white border/glow around edges.
  Borders must be big enough to SEE — 1.5px minimum, not hairline, not faint.
  If you can't see the separation at a glance, the border is too thin.
- **Hover:** Color ignites. The element's OWN spectrum color lights up with glow.
  Chrome elements ignite purple. Themed elements ignite their theme color.
- **Active/selected:** Subtle white indicator only. NO permanent color glow. Color comes on hover, not on selection.

**Applies to:** Tabs, buttons, sidebar items, bottom bar icons, toggle jewels, cards — everything clickable and every container.

---

## 3. BUTTON LANGUAGE

### Universal button law
- Center: really black (`#050505`).
- Text: always white, with a clear icon.
- Border: white, visible at rest (1.5px+).
- Elevated: inset top highlight + deep drop shadow. Must feel liftable.
- Hover: purple edge + glow for chrome; own spectrum color for themed.
- **Affordances tell the truth:** a chevron promises navigation; a plus promises adding. Use the glyph that means what happens.

### Primary toggle buttons (sidebar openers, menu triggers)
- Black circular buttons (`radial-gradient(circle at 35% 30%, #2a2a32, #0a0a0e 70%)`)
- Bold white icon (not thin, not dot-like — clearly visible)
- White light glow when idle
- Purple light + scale/rotate animation on hover
- Must feel "alive" — subtle movement on hover

### Action buttons (Love, Like, Save, etc.)
- Pill shape, black center, white text + icon
- Semantic color per action:
  - LOVE: red `#ff5e6c`
  - LIKE: blue `#55b9ee`
  - FAVORITE: gold `#ffd45a`
  - SAVE: blue `#55b9ee`
  - CREATE SPACE: purple `#9d75ff`
  - SHARE: purple `#9d75ff`
- White light idle, own color on hover
- Dynamic counts/badges where applicable

### Ecosystem buttons (bottom bar)
- Black circular, white light idle
- Each in its own spectrum color on hover
- Unique icon per destination (not generic)
- Label tooltip on hover

---

## 4. ICON LANGUAGE

- **Unique per item.** Never the same shape in different colors and call it done. Each icon must represent what it IS.
- **Drawn, not shrunk.** Icons are vector geometry — bold, simple, luminous, readable at 16px. Never a shrunken photograph or 3D render. If you can't make it good, don't put it there.
- **Native to the page.** An icon must speak the page's visual language (e.g., the orb's orbiting light echoes the avatar sheen). Imported styles feel foreign.
- **Rooms:** Distinct line-art icons (stream, sun, chart, books, nodes, etc.) — larger (24px), in spectrum color
- **Layers:** Faceted jewel system (core/facet/shade/edge SVG geometry)
- **Toggles:** Bold, clear symbols (plus sign must read as PLUS, not a dot)
- **Ecosystem:** 12 unique icons (home, bolt, users, brief, doc, cap, trophy, gauge, star, report, heart, key)

**Law:** If you can't tell what an icon represents at a glance, it's wrong. Redesign it.

---

## 5. TYPOGRAPHY, READABILITY & VOICE

- **LAW ZERO (supreme):** Readability beats everything. No glow, color, or effect may reduce readability.
- Body: 17-18px target, 16px floor
- **Hierarchy: 24 / 18 / 14.** Kicker 24, headline 18, detail 14. Separation by size, never by color.
- White text 99%. High contrast always.
- One clear visual hierarchy per screen
- Generous spacing — every element earns its place

### Text craft (not placement)
Headers get a VOICE — a real typeface with character (e.g., Cormorant for warmth),
never the system default. Flat text is lazy. Craft means:
- Gradient soul or carved light — never a single flat fill on display type
- Layered shadows: grounding shadow beneath + luminous halo around
- Breathing glow — subtle, slow, alive
- Title case for warmth over all-caps distance (unless the brand demands caps)

### Copy law
Every word gets scorecarded like design. Warm, clear, concise. No
documentation-speak, no feature lists, no architecture explanations.
Ten words that earn their place beat thirty that don't.

---

## 6. LAYOUT PRINCIPLES

- **Full-width.** No narrow centered columns with black voids. Content owns the width. No max-width caps.
- **Full-screen by default.** Sidebars hidden, opened via obvious toggle buttons.
- **No dead buttons.** Every clickable element goes somewhere real. If it doesn't do anything, remove it.
- **No black voids.** Content flows directly. No `min-height` forcing empty space.
- **Dynamic, not static.** Every component must handle any data gracefully. Missing fields get fallbacks, never crashes.
- **Logo in the corner.** The Naya mark lives top-left, always.
- **Layout is meaning.** The UX metaphor IS the decision: contacts scroll vertically (people, not products); feeds flow endlessly; grids browse. Choose the metaphor that matches what the thing is.

---

## 7. THE HEADER LAW

Every room header is a front door, not a nameplate:
- Logo top-left, living section mark, warm voice, one clear line of copy.
- The elements must relate — composed, not assembled. Gaps without relationship read as PowerPoint.
- The header breathes with the page. If it's the only dead thing on a living page, the page fails.

---

## 8. ALIVENESS STANDARD

Maximum life, minimum noise. Every page breathes:
- Ambient light drifts slowly behind content (brand-color orbs, heavily blurred, low opacity)
- Cards pulse their edge light gently
- Avatars and marks carry rotating light sheens
- Text glows breathe; never strobe, never distract
- All motion slow (4s+ cycles), subtle, purposeful. Restraint is the craft.
- `prefers-reduced-motion` disables all of it.

---

## 9. HONESTY

- **Device-local labels.** If it's stored on device, say so. Never imply backend/cloud sync.
- **No fake liveness.** Don't claim real-time if it's not.
- **Trust microcopy.** "One intelligence · Many views · One identity." Mean it.
- **Empty states are honest.** "Nothing here yet" > fake content.

---

## 10. THE EXPERIENCE SCORECARD LAW

- **Score the rendered experience, never the code.** A 9.5 on CSS is worthless if the page is a 5.
- **9+ self-scorecard before shipping.** Nothing reaches Shawn unless the builder has personally reviewed the rendered page, scored it 9+, and can explain why with specifics.
- **If you can't back it, bench it.** Below 9 = not ready. No exceptions.
- **Verify before claiming.** Read the file. Count the matches. Watch it render. A claim without verification is a lie the builder tells themselves first.

---

## 11. THE NAYA PHILOSOPHY (logic & thinking)

- **"One brain. Many doors."** — One intelligence, many views. Never duplicate the brain. Never build a second version of something that exists (one mail system, not two).
- **Push-button simple.** Every action is one tap. No manuals needed.
- **Intelligence is output.** The Hub displays intelligence; it doesn't capture it (no capture buttons in Hub chrome).
- **Proactive > reactive.** Anticipate what the user needs.
- **Value is the test.** If it doesn't help, remove it.
- **10/10 or don't ship.** Below 9.0 = not ready.

---

## 12. RELEVANCE ALGORITHM (locked 2026-10-03)

**Purpose:** Match people to spaces, intelligence, and each other by relevance percentage.

**Components:**
- Topic affinity (40%) — Smart Note topics they engage with
- Action patterns (30%) — creator vs joiner vs lurker
- Social proximity (20%) — who they interact with
- Recency (10%) — fresh > stale

**Phases:**
- Cold start: Everyone sees everything. No algorithm.
- Growth: Threshold at 60%. Below = in feed, above = notified.
- Scale: Ranked by %. Show why: "87% relevant — you loved 3 similar."

**Principle:** Relevance, not likeness. Match on what people care about, not who they are.

---

## AMENDMENT PROCESS

Shawn amends this contract verbally. The amending Naya updates this document and posts the change to the live team board. All seats adopt immediately.

**Version history:**
- v1.0 (2026-10-03): Initial ratification. Synthesized from Shawn's directives across the Hub 10/10 drive.
- v1.1 (2026-10-03): Verbal amendment — three color jobs (accent jewels, endless flow, SmartNote board mapping); cyan named (dictation had rendered it as "Kenya" — fixed); forest emerald + lime + gold + indigo tokens added; active intelligence principle locked.
- v1.2 (2026-10-08): Hardening from the Connections rebuild session. Color jobs split into chrome/text/theme (was: accent jewels/endless flow). Lighting standard given teeth (1.5px minimum borders). Button law hardened (black center, white text+icon, truthful affordances). Icon law: drawn not shrunk, native to the page. New: text craft, copy law, header law, aliveness standard, UX-metaphor law, experience scorecard law, verification law, one-system law. v1.1 was principles; v1.2 is checkable.
