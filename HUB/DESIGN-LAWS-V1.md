# NayaNET Hub — Design Laws V1

**Status:** CANDIDATE — proposed by Naya 4, 2026-10-01. Not ratified. Not merged.
**Authority:** Director (Shawn) ratifies. Until then, this is the working standard every lane builds to and every scorecard measures against.
**Applies to:** every Hub surface — rooms, boards, buttons, journey pages, states.
**Supersedes nothing yet.** Reconciles with: `HUB/DESIGN-CONTRACT.md` (§§1–29), `HUB/DESIGN-NORTH-STAR.md` (PR #1284), art direction (PR #1281), room registry (PR #1290).

---

## The Standard

Build the interface as if the world's best designers will study it with jealousy — and the world's busiest human must read it without squinting.

Two sentences govern everything below:

1. **It must be the most beautiful intelligent interface anyone has ever touched.**
2. **No beauty is ever allowed to make anything harder to read, find, or understand.**

If (1) and (2) ever conflict, (2) wins. That is not a compromise. Readability *is* the beauty.

**How to use these laws:** every rule has a SPEC (exact, measurable), a VIOLATION (what fails), and a TEST (how to check). If you cannot test it, it is not a law — it is a wish. Scorecards cite law numbers.

---

# PART I — DESIGN LAW (supreme over Parts II and III)

## DL-0 · Law Zero — Readability Supremacy

**Statement.** No glow, no accent, no depth effect, no color, no animation is ever allowed to make anything harder to read.

**Spec.**
- Body text minimum 16px, line-height ≥ 1.5, on obsidian `#050507`.
- Text color is ink `#f8f7fb` or a tested high-contrast derivative. Contrast ratio ≥ 7:1 for body, ≥ 4.5:1 for large headings.
- Text never carries glow, blur, gradient-fill, or animated effects. Text sits *above* effects, never inside them.
- Yellow/gold are never text colors, never dominant, never brighter in the hierarchy than purple/black/white.

**Violation.** Any glowing text, small gray-on-black body copy, animated headline that is unreadable mid-motion.

**Test.** Screenshot the room, blur it 2px: every heading and button label must still be legible. Fail = violation.

## DL-1 · The Obsidian Foundation

**Statement.** Every room stands on the same bedrock. Depth is built upward from darkness, never painted on.

**Spec.**
- Page background: `#050507`, full-bleed. No alternate page backgrounds.
- Surfaces rise in this order: page → board (raised) → sub-board (raised further) → control (highest). Each step up = stronger gradient, stronger shadow.
- Flat color fills are forbidden as surface treatments. Every surface carries a vertical gradient (lighter at top, darker at bottom), an inner top highlight, and a cast shadow.

**Violation.** A flat `#111` rectangle with a border. A white/light surface anywhere.

**Test.** Disable all borders: surfaces must still read as stacked by shadow and gradient alone.

## DL-2 · Color Prominence Hierarchy

**Statement.** Purple, black, and white dominate. The rest of the spectrum serves them.

**Spec.**
- Dominant: obsidian black, ink white, purple family.
- Complementary spectrum in canonical order: purple → indigo → sapphire → teal → emerald → lime → yellow → gold → orange → rich orange → red → magenta.
- Yellow/gold: restrained, semantic (value, proof, caution) — never text, never the loudest thing on screen.
- Each room owns ONE spectral identity color (see BL-2). Shared chrome stays purple/black/white.

**Violation.** A room drowned in gold. Two rooms with indistinguishable theming. Rainbow-for-fun.

**Test.** Desaturate the screenshot: the layout must still be fully usable (color is energy, never the only signal).

## DL-3 · Typography Law

**Statement.** Generous text by default. The interface speaks like a confident human, not a manual.

**Spec.**
- Display headings: large, tight, ink. Section headings clearly smaller than display, clearly larger than body.
- Body copy: 16–18px, generous measure, plain words.
- Micro-labels (eyebrows, kickers): uppercase, letterspaced, dimmer — but still ≥ 12px and ≥ 4.5:1 contrast.
- One typeface family for UI. No novelty fonts for body.

**Violation.** Walls of 13px gray text. Three heading sizes that look identical. Cute font for labels.

**Test.** Read the room aloud in 30 seconds: if you cannot finish the essential meaning, there is too much text (see BL-4).

## DL-4 · Motion Law

**Statement.** Motion is physical. Things rise, press, settle — they never decorate.

**Spec.**
- Timing: 0.22–0.28s. Easing: `cubic-bezier(.16,.84,.22,1)` (rise-and-settle). No linear UI motion except true progress.
- Allowed motions: hover-rise, press-down, select-illuminate, panel-settle, honest loading shimmer.
- Forbidden: perpetual ambient animation on interactive elements, parallax for fun, entrance choreography longer than 0.4s, anything that moves while the user is trying to read.
- Animation must never pretend intelligence or activity. A shimmer means *loading*; stillness means *ready*.

**Violation.** Pulsing buttons. Spinning ornaments. A card that floats forever.

**Test.** `prefers-reduced-motion`: the room must be fully usable and still beautiful with all non-essential motion off.

## DL-5 · Truth Law

**Statement.** Every visible action has a real consequence, observable state, and honest failure.

**Spec.**
- Five states exist for every dynamic surface: loading, ready, working, done, failed/unavailable. All five are designed, not just the happy path.
- Sample/illustrative content is labeled as sample. Never.
- "Quiet day" is a first-class design: an empty room must be beautiful and honest, not a broken-looking grid.
- No simulated activity. No fake counts, fake live dots, fake progress.

**Violation.** A "Live" badge on static content. An empty state that looks like an error. Unlabeled mock data presented as real.

**Test.** For each room: show all five states. Each must be legible, on-brand, and truthful.

## DL-6 · Unity Law

**Statement.** One shell, eleven masterpieces. Rooms are individuals, not strangers.

**Spec.**
- Shared: obsidian foundation, typography, button physics (Part II), board grammar (Part III), journey (Welcome → Identity → Hub).
- Variable per room: ONE spectral identity color, atmosphere tint, masthead glyph, zone arrangement.
- A user moving room-to-room must feel "same house, different room" — never "different app."

**Violation.** A room with its own button style. A room that ignores the journey chrome.

**Test.** Cover the room's name: a tester must still recognize it as NayaNET Hub, and guess the room from its color.

---

# PART II — BUTTON LAW (the primo button)

Buttons are the hands of the interface. Flat buttons are dead hands. Every button in the Hub obeys this law without exception.

## BT-0 · The Anatomy — nine layers, in order

Every primo button is built bottom-to-top:

| # | Layer | Spec (from the frozen concept) |
|---|-------|-------------------------------|
| 1 | Substrate | Obsidian `#050507` behind; button never touches raw page |
| 2 | Aura | Radial wash of the button's semantic color at ~8–13% opacity, bleeding 20–30px |
| 3 | Body | Dark vertical gradient (lighter top → darker bottom), `border-radius` 10–17px. Never a flat fill |
| 4 | Edge | 1px luminous border in the semantic color, ~40–60% opacity at rest |
| 5 | Specular | Inner top highlight: `inset 0 1px rgba(255,255,255,.47)` — the light-catch line |
| 6 | Bevel | Darker 1px lower inner edge — physical thickness |
| 7 | Cast shadow | `0 12px 25px rgba(0,0,0,.5)` at rest — the button floats above the board |
| 8 | State glow | `0 0 30px <color>22` at rest; intensifies with state |
| 9 | Motion | 0.22–0.28s `cubic-bezier(.16,.84,.22,1)` on every state change |

**Violation.** Any button missing the specular line, the gradient, or the cast shadow. A bordered flat rectangle calling itself a button.

**Test.** Zoom 200%: the light-catch line and bevel must be visible. Remove the label: it must still read as pressable.

## BT-1 · The Five States

| State | Behavior (exact) |
|-------|------------------|
| **Rest** | Anatomy as built. Glow at rest level. |
| **Hover** | Rises `translateY(-2px)`. Edge brightens to ~90%. Glow intensifies (~2×). A luminous **color-flow sweep** travels across the face in the button's hue. Cursor: pointer. |
| **Press** | Pushes back `translateY(+1px)`. Cast shadow contracts. Glow holds. Feels like clicking a real key. |
| **Selected** | Stays illuminated: persistent brightened edge + steady glow. Reads as "this is on" from across the room. |
| **Disabled** | Loses energy: opacity ~45%, glow off, aura off, no hover physics, `cursor: not-allowed`. Never looks clickable. |

**Violation.** Hover that only changes color. Press with no physical travel. Disabled button that still glows.

**Test.** Operate every button by keyboard: focus state must equal hover illumination. Click-and-hold: the press travel must be visible.

## BT-2 · Color Flow

**Statement.** Color is energy in motion, not paint.

**Spec.**
- Every button owns ONE semantic color: primary action = room's spectral color; confirm/safe = emerald; warn = gold (restrained); danger = red.
- On hover, a soft luminous sweep crosses the button face in its hue (gradient-position animation, ≤ 0.3s).
- The edge, glow, and sweep always share the hue. Never mix hues on one button.

**Violation.** Rainbow hover. Hue that changes between rest and hover. Color flow on disabled buttons.

**Test.** Screenshot hover mid-sweep: the hue must be identifiable as the button's single semantic color.

## BT-3 · Sizing & Spacing

**Spec.**
- Minimum target: 44×44px. Primary actions larger than secondary.
- Padding generous: label never touches edges (≥ 14px horizontal, ≥ 10px vertical).
- Button rows: 12–16px gaps. Related actions grouped; destructive actions separated.

**Violation.** 28px-tall buttons. Labels crammed edge-to-edge. Delete sitting beside Save with equal weight.

## BT-4 · Label Law

**Spec.**
- Labels are verbs or verb phrases: "Open Feed", "Pin to Today", "Verify". Never "OK" alone, never jargon.
- Label is ink, never glowing, never gradient-filled (DL-0). Readable mid-sweep, mid-press, always.
- Icon + label preferred for primary actions; icon-only only with tooltip and aria-label.

**Violation.** "Submit". Glowing label text. A button whose purpose needs a paragraph.

## BT-5 · Forbidden Buttons

Flat buttons. Ghost buttons with no energy. Buttons that look primary but do nothing. Two competing primary actions in one zone. Buttons whose consequence is unknown ("what will this do?"). Mystery-meat icon-only rows.

## BT-6 · Button Acceptance

For each button: anatomy complete at 200% zoom · five states demonstrable · keyboard-focus equals hover · label readable in every state · consequence known before click · disabled state visibly dead. Fail any → the button fails.

---

# PART III — BOARDS LAW

A board is a room's stage. Boards carry the room's soul: its color, its atmosphere, its elevation.

## BD-0 · Board Anatomy — six elements, top to bottom

1. **Spectral rail** — a slim vertical luminous rail in the room's identity color. The room's signature; visible from the doorway.
2. **Atmosphere** — a faint ambient tint wash of the room color over the board's region (~4–8% opacity). Felt, not seen.
3. **Masthead** — the room's name, large and ink-readable; a jewel-like glyph catching light. No glow on the text (DL-0).
4. **Zones** — at most six content zones per room, each with one job. Zones from the room's functional spec; no invented zones.
5. **Sub-boards** — raised cards within zones: own gradient, own shadow, own specular line. One elevation step above the board.
6. **Control deck** — the button row. Primo buttons only (Part II). Ordered: primary → secondary → tertiary → destructive (separated).

**Violation.** A board with no rail. Zones without jobs. Cards at the same elevation as their board (flat soup).

**Test.** The six elements must be identifiable in a grayscale screenshot by elevation and structure alone.

## BD-1 · Theming Law

**Statement.** Each room is themed. Theming is identity, not decoration.

**Spec.**
- Each room owns ONE spectral color, taken verbatim from the frozen concept
  (`HUB/NAYANET INTERFACE CONCEPT.html` — the concept is the visual ground truth).
  Registry (concept hexes, exact):

| Room | Spectral identity | Concept hex |
|------|-------------------|-------------|
| Your Intelligence Today | Magenta | `#d86cff` |
| Your Reports | Indigo | `#6675ff` |
| Intelligent Library | Sky | `#55b9ee` |
| Smart Connect (was Share) | Emerald | `#55e39a` |
| Smart Ledger | Yellow | `#f1d75a` |
| Your Connections | Orange | `#ff9a5a` |
| Smart Lists | Purple | `#9d75ff` |
| Smart Mail | Sky | `#55b9ee` |
| Smart Spaces | Lime | `#b8ee57` |
| Settings | Silver | `#aaa4b1` |
| Smart Feed | Violet | `#8b42ff` (new room, not in the concept; assigned per canonical spectral order) |

- Known concept inheritances (flagged, not silently changed): Smart Mail and
  Intelligent Library share `#55b9ee` in the concept; Smart Lists shares
  `#9d75ff` with the retired Smart Notes room. Distinctness pass pending
  director review — do not freelance new hexes.
- The rail, aura, button edges, and key accents carry the room color. Chrome, text, and structure stay shared.
- No room borrows another room's color beyond the flagged inheritances above.

**Violation.** A magenta room with teal buttons. Two rooms you cannot tell apart. Gold used as a loud theme instead of a restrained one.

**Test.** Show all eleven rails side by side: eleven distinct hues in canonical spectral order.

## BD-2 · Elevation Law

**Statement.** Elevation is information. Higher = more interactive, more immediate.

**Spec.**
- Page (0) → board (+1) → sub-board (+2) → control (+3). Each step: stronger top-light gradient, deeper cast shadow.
- Inset elements (wells, readouts) go *down*: inner shadow, darker gradient. Used for verified data at rest.
- Nothing floats without a shadow. Nothing is raised without a highlight.

**Violation.** A "card" with only a border. A button flatter than its board. Inset and raised used interchangeably.

## BD-3 · Density Law — radical reduction

**Statement.** A board is a stage, not a document.

**Spec.**
- No zone carries more than ~60 words of body copy. Ever.
- Headlines ≤ 8 words. Labels ≤ 4 words.
- Depth lives behind "evidence" / "details" affordances — tap to go deeper, don't print the depth.
- Numbers, glyphs, and structure carry meaning; paragraphs explain only what structure cannot.

**Violation.** The first-draft disease: every thought printed on the stage. A zone that reads like a spec document.

**Test.** The 30-second read-aloud (DL-3): essential meaning must land in 30 seconds.

## BD-4 · State Law — all five, designed

**Spec.** Every board designs: **loading** (honest shimmer, room-colored, ≤ its real wait), **ready** (the masterpiece), **working** (in-progress illumination on the acting control), **done** (confirmation with consequence named), **failed/unavailable** (plain words, what happened, what to do, no blame).
- Quiet/empty days are designed boards, not missing boards: beautiful, honest, with one good next action.

**Violation.** A spinner with no words. An empty grid. An error that says "Error 500". A fake "Live" pulse.

## BD-5 · Forbidden Boards

Flat soup (no elevation). Rainbow theming. Text-as-decoration. More than six zones. Zones without jobs. Controls that aren't primo buttons. Sample data presented as real (DL-5). A board that needs a manual.

## BD-6 · Board Acceptance

For each board: six anatomy elements present · one spectral identity, distinct from all siblings · elevation readable in grayscale · ≤60 words per zone · all five states designed and demonstrable · every control a lawful primo button · passes DL-0 blur test. Fail any → the board fails.

---

## Scoring Against These Laws

- Each law is pass/fail. A room's score = laws passed ÷ laws applicable.
- DL-0 is a **hard gate**: fail readability, fail the room, no matter how beautiful.
- BT-6 and BD-6 are the acceptance checklists. Run them on every room, every iteration.
- Scorecards cite law numbers (e.g., "fails BT-1: hover has no rise"). No vibes.

---

# PART IV — SMART BOARD LAW (the intelligent shell)

Two kinds of boards exist. **Room boards** (Part III) are the stage. **Smart Boards**
(this Part) are the soul: the fifteen-layer intelligent shell Shawn built and
declared extraordinary. Never redesign the shell. Restore it, complete it, theme it.

## SB-0 · The Fifteen Layers — in this order, every board, no exceptions

| # | Layer | Label | Job |
|---|-------|-------|-----|
| 1 | Kicker | `SMART NOTE 0X · CANONICAL INTELLIGENCE` | Provenance at a glance |
| 2 | Identity | 🧠 glyph + Title | What this intelligence is |
| 3 | Trust line | `SOURCE SEPARATED` | Source and interpretation are separate — always visible |
| 4 | Nutshell | **IN A NUTSHELL** | The whole thing in 2–3 sentences |
| 5 | Human | **HUMAN NOTE** · HUMAN INPUT | What the human brings |
| 6 | Child | **CHILD** · SIMPLIFIED | A bright 10-year-old gets it |
| 7 | Grandma | **GRANDMA NOTE** · WHY NOTICE? | A wise grandmother gets why it matters |
| 8 | Naya | **NAYA NOTE** · INTERPRETATION | Naya's interpretation — labeled as interpretation, never as source |
| 9 | Machine | **MACHINE NOTE** · EVIDENCE BOUNDARY | The mechanical pipeline; what is proven vs. assumed |
| 10 | Learning | **ADAPTIVE LEARNING** · LEARNING | How this compounds — experience → intelligence → better action |
| 11 | Meaning | **WHAT IT MEANS** · SIGNIFICANCE | The ultimate meaning |
| 12 | Value | **WHAT'S IN IT FOR YOU?** · HUMAN VALUE | Why the human should care — bottom territory |
| 13 | Use | **HOW TO USE IT** · PRACTICE | What to actually do with this — bottom territory |
| 14 | Connect | **HOW IT ALL CONNECTS** · CONNECTIONS | How this board connects to the other boards, rooms, and the system — bottom territory |
| 15 | Seal | `ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY — TRUST: SOURCE / INTERPRETATION SEPARATED` | The covenant, closing every board |

Layers 12–14 are the bottom trio, in that order: value → use → connects. Then the seal.

**Violation.** A board missing layers ("redesigned" shell). Layers out of order. The Naya note presented as source. The seal missing.

**Test.** Checklist the fifteen against the V7 reference boards. All present, in order = pass.

## SB-1 · Tight Layers

**Statement.** The full shell, never a wall of text.

**Spec.** Each layer: 1–3 tight sentences. The V7 boards are the measure — every layer short enough to read in one breath. If a layer needs a paragraph, the intelligence isn't distilled yet; distill it, don't print it.

**Violation.** Any layer over ~60 words. (This is how "too much text" and "full shell" reconcile: complete AND tight.)

## SB-2 · Themed, Never Cloned

**Statement.** Every board wears its room's spectral identity; every board is a little different.

**Spec.** Rail, aura, glyph light, accent edges in the room's color (BD-1 registry). Layer labels, typography, shell order stay identical — the *voice* is shared, the *soul* is the room's.

**Violation.** Two boards indistinguishable. A board wearing another room's color.

## SB-3 · The Shell Is Sacred

**Statement.** Lanes may write new boards. No lane redesigns the shell.

**Spec.** New board = fifteen layers, in order, tight, themed. Propose new layers (if ever) on #554 with evidence — never freelance.

## SB-4 · Smart Board Acceptance

Fifteen layers present and in order · each layer ≤ ~60 words · Naya note labeled interpretation · source separated · bottom trio in order (value → use → connects) · seal closes · room-themed · passes DL-0. Fail any → the board fails.

## Change Control

These laws are CANDIDATE until Shawn ratifies. Amendments come as PRs against this file with before/after evidence. No lane edits the laws unilaterally mid-build — propose on #554, agree, then build.

---

*Written so the team can build like world champions: every rule exact, every rule testable, no part left to taste alone.*
