# NAYA DESIGN CONTRACT v1.1
**Status:** CANONICAL — All Naya seats follow this. No exceptions.
**Ratified:** 2026-10-03 by Shawn Vibert (Human Director)
**Purpose:** The visual signature, interaction language, and design philosophy of Naya. So Shawn never has to repeat himself.

---

## 1. COLOR LANGUAGE

### Dominant (always present)
- **Black** (`#0a0a0e`) — backgrounds, buttons, depth
- **White** (`#ffffff`) — text, light, idle glow
- **Purple** (`#9d75ff`, `#8a5cff`) — Naya's signature, primary actions

### Spectrum (accents, never dominant)

Color has three distinct jobs. Do not use one job's rule for another.

**1. Accent jewels** — bullet points, boards, icons. Always the richest, most vibrant:
**hot pink · purple · blue · green · gold.**

**2. Endless flow** — feeds and long continuous sequences. A repeating pattern, not the same for everything:
**purple → indigo → forest emerald → lime → yellow → gold → orange → red → magenta → purple** (repeats)

**3. SmartNote board sections** — fixed mapping:
- In a nutshell → white
- Human → magenta
- Child → purple
- Grandma → indigo
- Naya → cyan
- Machine → forest emerald
- Why it matters → lime green
- How do you use it → yellow
- What's in it for you → orange or gold

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

- **Idle (not hovered):** White light. Visible white border/glow around edges. Borders must be big enough to SEE — not faint.
- **Hover:** Color ignites. The element's own spectrum color lights up with glow.
- **Active/selected:** Subtle white indicator only. NO permanent color glow. Color comes on hover, not on selection.

**Applies to:** Tabs, buttons, sidebar items, bottom bar icons, toggle jewels — everything clickable.

---

## 3. BUTTON LANGUAGE

### Primary toggle buttons (sidebar openers, menu triggers)
- Black circular buttons (`radial-gradient(circle at 35% 30%, #2a2a32, #0a0a0e 70%)`)
- Bold white icon (not thin, not dot-like — clearly visible)
- White light glow when idle
- Purple light + scale/rotate animation on hover
- Must feel "alive" — subtle movement on hover

### Action buttons (Love, Like, Save, etc.)
- Pill shape, transparent/dark background
- Semantic color per action:
  - LOVE: red `#ff5e6c`
  - LIKE: blue `#55b9ee`
  - FAVORITE: gold `#ffd45a`
  - SAVE: blue `#55b9ee`
  - CREATE SPACE: purple `#9d75ff`
  - SHARE: purple `#9d75ff`
- White light idle, color on hover
- Dynamic counts/badges where applicable

### Ecosystem buttons (bottom bar)
- Black circular, white light idle
- Each in its own spectrum color on hover
- Unique icon per destination (not generic)
- Label tooltip on hover

---

## 4. ICON LANGUAGE

- **Unique per item.** Never the same shape in different colors and call it done. Each icon must represent what it IS.
- **Rooms:** Distinct line-art icons (stream, sun, chart, books, nodes, etc.) — larger (24px), in spectrum color
- **Layers:** Faceted jewel system (core/facet/shade/edge SVG geometry)
- **Toggles:** Bold, clear symbols (plus sign must read as PLUS, not a dot)
- **Ecosystem:** 12 unique icons (home, bolt, users, brief, doc, cap, trophy, gauge, star, report, heart, key)

**Law:** If you can't tell what an icon represents at a glance, it's wrong. Redesign it.

---

## 5. TYPOGRAPHY & READABILITY

- **LAW ZERO (supreme):** Readability beats everything. No glow, color, or effect may reduce readability.
- Body: 17-18px target, 16px floor
- High contrast always
- One clear visual hierarchy per screen
- Generous spacing — every element earns its place

---

## 6. LAYOUT PRINCIPLES

- **Full-width.** No narrow centered columns with black voids. Content owns the width.
- **Full-screen by default.** Sidebars hidden, opened via obvious toggle buttons.
- **No dead buttons.** Every clickable element goes somewhere real. If it doesn't do anything, remove it.
- **No black voids.** Content flows directly. No `min-height` forcing empty space.
- **Dynamic, not static.** Every component must handle any data gracefully. Missing fields get fallbacks, never crashes.

---

## 7. HONESTY

- **Device-local labels.** If it's stored on device, say so. Never imply backend/cloud sync.
- **No fake liveness.** Don't claim real-time if it's not.
- **Trust microcopy.** "One intelligence · Many views · One identity." Mean it.
- **Empty states are honest.** "Nothing here yet" > fake content.

---

## 8. THE NAYA PHILOSOPHY (logic & thinking)

- **"One brain. Many doors."** — One intelligence, many views. Never duplicate the brain.
- **Push-button simple.** Every action is one tap. No manuals needed.
- **Intelligence is output.** The Hub displays intelligence; it doesn't capture it (no capture buttons in Hub chrome).
- **Proactive > reactive.** Anticipate what the user needs.
- **Value is the test.** If it doesn't help, remove it.
- **10/10 or don't ship.** Below 9.0 = not ready.

---

## 9. RELEVANCE ALGORITHM (locked 2026-10-03)

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

Shawn amends this contract verbally. The amending Naya updates this document and posts the change to #554. All seats adopt immediately.

**Version history:**
- v1.0 (2026-10-03): Initial ratification. Synthesized from Shawn's directives across the Hub 10/10 drive.
- v1.1 (2026-10-03): Verbal amendment — three color jobs (accent jewels, endless flow, SmartNote board mapping); cyan named (dictation had rendered it as "Kenya" — fixed); forest emerald + lime + gold + indigo tokens added; active intelligence principle locked.
