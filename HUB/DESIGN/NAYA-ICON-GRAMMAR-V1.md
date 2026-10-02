# ◈ NAYA ICON / JEWEL GRAMMAR V1 — PROTOCOL PROJECTION

**Status:** CONVERGED CANDIDATE projection of `NAYA-DESIGN-PROTOCOL-V1`; not separate authority.  
**Parent:** `HUB/DESIGN/NAYA-DESIGN-PROTOCOL-V1.md`  
**Purpose:** Give a cold builder enough exact logic to construct a new Naya glyph without inventing a new icon language.

## 1. ONE FAMILY, TWO ROLES

### A — JEWEL MARK
Use for room identity, hero identity, board identity and rare signature moments.

Character:
- precision-cut / faceted;
- luminous but restrained;
- dimensional;
- semantic silhouette;
- visually strong at 48/64/96px;
- calm at rest, more energetic only when state requires it.

### B — ACTION GLYPH
Use for buttons, tabs, controls, compact utilities and state marks.

Character:
- simpler geometry than a Jewel Mark;
- obsidian or transparent housing as context requires;
- same facet/light/optical-weight logic as the Jewel family;
- instantly legible at 16/24/32px.

One material language, two levels of expression.

## 2. CONSTRUCTION LOGIC

1. **Geometry:** derive the glyph from the object's job, not decoration.
2. **Silhouette:** recognizable before internal detail.
3. **Light source:** consistent upper-left illumination across the family.
4. **Core:** primary glyph remains high-contrast neutral/white.
5. **Semantic energy:** accent lives in rim, field, facet or controlled aura — never by tinting away legibility.
6. **Edge:** crisp enough to survive dark backgrounds and high-DPI rendering.
7. **Depth:** use material + highlight + lower shade; never generic blur as the only depth cue.
8. **State:** REST / HOVER-AWARE / FOCUS / SELECTED / DISABLED and LOADING/SUCCESS/ERROR where applicable.
9. **Meaning:** icon plus label at first use when the symbol is not universally learned.
10. **Accessibility:** icon-only controls always receive an accessible name and adequate target.

## 3. DETERMINISTIC SIZE TOKENS

Only these production size tokens are used:

**16 · 24 · 32 · 48 · 64 · 96 px**

Role guidance:
- **16 / 24** — compact utility / action glyph.
- **32** — primary control / rail / compact identity.
- **48** — board identity / high-value object.
- **64 / 96** — room/hero Jewel Mark.
- **Naya emblem:** never below **32px**.

Optical correction happens inside the SVG/viewBox/housing. Do not create random CSS dimensions to compensate for a weak glyph.

## 4. COLOR RULE

Naya identity remains purple/deep-purple + obsidian + white.

Semantic color follows the parent protocol.

- Teal may communicate connection/flow.
- Emerald may communicate healthy/available/confirmed operational state.
- Red communicates risk/destructive consequence.
- Yellow/gold are **not** Naya brand accents or default room/icon colors; use only for necessary semantic states under the protocol's restraint rule.
- No icon receives color merely because the screen feels empty.

The white/neutral core stays legible in every state.

## 5. HOUSING

Valid housings include:
- full Jewel sphere/faceted object;
- compact obsidian chip;
- recessed state well;
- plain inline glyph when the context does not justify a container.

Not every glyph is a gemstone. Every glyph must still look related.

## 6. INTERACTION PHYSICS

### REST
Quiet material presence; restrained aura.

### HOVER / AWARE
Small lift or facet/light response; no text blur and no layout shift.

### FOCUS
Explicit accessible focus treatment independent of hover.

### SELECTED
Sustained, controlled semantic illumination.

### DISABLED
Clearly non-live; legibility preserved.

### LOADING
Only while real work is occurring.

### SUCCESS / ERROR
Brief state resolution backed by actual outcome.

## 7. ANTI-PATTERNS

Fail the glyph if it is:
- emoji in primary production navigation;
- a random icon-pack import that does not match the family;
- stretched/squashed;
- dependent on glow to become visible;
- too detailed to parse at its token size;
- carrying a room/state color with no semantic reason;
- animated without state;
- unlabeled when meaning is ambiguous;
- a duplicate Naya emblem used as generic sparkle;
- visually stronger than the content it is supposed to support.

## 8. ACCEPTANCE PREDICATES

A production glyph passes only when:

1. it uses one allowed size token;
2. its silhouette is recognizable at intended size;
3. monochrome/high-contrast mode remains legible;
4. light direction matches the family;
5. semantic color role is documented;
6. every applicable state exists;
7. keyboard focus is visible for interactive glyphs;
8. accessible name exists where needed;
9. it remains coherent at high DPI;
10. it passes V6 Iconography and V10 Signature review under the parent protocol.

## 9. ROOM-AUTHORITY BOUNDARY

This grammar defines **how icons behave**.

PR #1290 owns **which room gets which final identity glyph/theme**.

Semantic guidance such as “teal = connection/flow” is reusable grammar, not permission to silently change a room contract.

## 10. COLD-BUILDER EXAMPLE

Input:
- object: Smart Connect
- job: governed connection/flow
- role: board identity
- required state: REST + SELECTED

Builder derives:
- size token: 48px;
- family: Jewel Mark;
- glyph: connection/portal silhouette;
- core: high-contrast neutral;
- semantic field: connection/flow token from room contract;
- light: upper-left family light;
- state: restrained rest → sustained selected edge/aura;
- label: visible at first use;
- accessible name: "Smart Connect".

The builder does not invent a new material, random hue, or icon pack.

---

**Truth boundary:** this grammar is implemented on PR #1310 but remains a candidate until the parent protocol passes independent exact-branch verification and Human Director ratification.
