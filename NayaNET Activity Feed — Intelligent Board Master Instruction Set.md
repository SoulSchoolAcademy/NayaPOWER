# NayaNET Activity Feed — Intelligent Board Master Instruction Set

## Status
**Canonical design contract — locked direction**

This document defines the intended presentation of NayaNET Intelligent Feed / Smart Intelligence Boards. The 5:09 pm NayaNET HUB HTML remains the structural foundation. Existing feed implementations are reference material only: preserve their valuable ideas, but do not preserve incorrect presentation.

## 1. Core principle

An Intelligent Board represents **ONE intelligence event**, not a collection of unrelated dashboard cards.

The board must make intelligence easier to understand without compressing the intelligence to fit the interface.

> **Content-length agnostic intelligence:** the interface adapts to the intelligence. Intelligence is never shrunk, truncated, or cramped merely to fit a fixed visual grid.

## 2. Remove the obsolete comprehension bar

Remove the useless bar containing:

**View · Scam · Learn · Verify · Operate · Explore · Teach**

It creates cognitive noise and has no sufficiently clear user purpose in the current experience. Do not replace it with another decorative taxonomy unless a real functional requirement is established.

## 3. NayaNET statement placement

Remove the flashing/loading statement immediately beneath the search area:

**“Your life creates your intelligence every day, and it helps you capture it, understand it, remember it, compound it, and use it.”**

The statement itself remains valuable. Restore the **beautiful centered NayaNET statement/banner treatment that belongs above the bottom bar**, rather than displaying a competing flash beneath Search. It must render stably with no first-load flash or layout glitch.

## 4. Intelligent Board physical structure

The primary board is an **obsidian-black, elevated 3D surface** centered in the feed.

It must visibly sit above the page rather than looking flat. Use restrained but unmistakable living depth: layered shadows, subtle edge light, material separation, controlled glow, and dimensional layering.

### Critical depth rule
There are **multiple layers of elevation**:

1. Page/background
2. Main obsidian Intelligence Board elevated above the page
3. Individual inner intelligence sections elevated above the main board
4. Interactive controls retain their own tactile/elevated treatment

The visual effect should feel like layers of intelligence **coming forward toward the user**.

Do not flatten these into a single background with borders.

## 5. Inner intelligence sections

The following sections are presented **vertically, one after another, full-width within the board**. They are NOT arranged side-by-side in a grid and must NOT be forced into equal heights.

Default sequence:

1. **IN A NUTSHELL** — the smallest useful explanation / essence
2. **HUMAN** — lived experience and real-world relevance
3. **CHILD** — simplest accurate explanation
4. **GRANDMA** — wisdom, consequence, durable lesson
5. **NAYA** — synthesis, implications, relationships, contradictions, opportunities, risks, unknowns
6. **MACHINE** — evidence, mechanism, measurement, sources, tests, limitations
7. **LEARNING** — what should be remembered
8. **MEANING** — why it matters
9. **ACTION** — how to use it / next useful move
10. **TRUST** — evidence, provenance, uncertainty and confidence state
11. **CONNECTIONS** — related intelligence, memory, context and relationships

Not every intelligence event must require every section. Use the smallest structure that produces complete understanding. But when sections are present, they remain vertical and content-length agnostic.

## 6. Typography and readability

Each inner board must have:

- clear, immediately readable headline
- strong black/white contrast
- comfortable reading width
- generous vertical breathing room
- typography that does NOT shrink because content is long
- no forced fixed-height content boxes
- no unreadable tiny text
- no faded low-contrast copy

A short section may be compact. A long section must simply become taller.

## 7. Color architecture

The outer Intelligence Boards use a deliberate sequential color language, progressing through the established spectrum (purple → violet/indigo/blue → magenta as appropriate).

Color is not decoration. It is part of the visual information architecture.

The inner sections echo the corresponding color system so the outer board and its inner layers feel like one coherent language.

Do not use random colors. Do not use color merely because it looks flashy.

## 8. Board controls — locked placement

### TOP LEFT
**Create Space**

This is the board's creation/context action.

### TOP RIGHT
**Save / Favorite**

Saving sends the intelligence to **Smart List**. The user can save it as a favorite and/or organize saved intelligence into lists.

### BOTTOM LEFT
**Love · Like · Rank** interaction area.

- Love: heart icon; unselected = white, selected = red.
- Like: thumbs-up icon; unselected = white, selected = indigo blue.
- Rank: five-star rating interaction.

### BOTTOM CENTER
A clear **Rate This Intelligence** / **Rate This Intel** treatment with the five-star rating centered in the board's bottom interaction area.

### BOTTOM RIGHT
**Share Intel +**

The plus is the share action. On mobile it should naturally connect to the device's sharing flow where supported.

These placements are part of the board grammar and should remain consistent across feed items.

## 9. Feed behavior

The feed is a vertical sequence of complete Intelligent Boards:

**Board 1 → Board 2 → Board 3 → Board 4 → ...**

As the user scrolls, the outer board color treatment can progress through the established spectrum while preserving the same structural grammar.

Consistency comes from **repeatable architecture**, not from making every board visually identical.

## 10. What to preserve from existing work

The current 5:09 Hub and existing middle-feed prototypes contain valuable material. They should be studied before replacement for:

- existing shell and navigation
- Naya presence
- feed/content model
- existing controls and interaction concepts
- semantic color ideas
- dimensional surface treatment
- existing intelligence content
- Smart List / save concepts
- sharing concepts
- any already-working functionality

Do not throw away working functionality merely to achieve the new visual structure.

## 11. What is explicitly NOT the target

Do not create:

- dashboard card soup
- side-by-side perspective grids
- tiny text to fit content
- random hero banners that compete with the feed
- duplicate feeds
- decorative comprehension boxes with no function
- flat 2D panels
- arbitrary color decoration
- dead buttons
- fake interactions
- unnecessary navigation taxonomy
- first-load flashing content

## 12. Definition of “right”

A correct Intelligent Board should feel like a **living intelligence object** rather than software furniture.

The user should perceive:

**one intelligence → multiple ways of understanding it → evidence and trust → learning → meaning → action → connection → human interaction.**

The visual hierarchy must communicate that order immediately.

## 13. Engineering doctrine

Use the existing **5:09 NayaNET Hub as the foundation**. This is surgical evolution, not a blind rebuild.

Workflow:

**PROVEN BASELINE → FORENSIC UNDERSTANDING → GAP ANALYSIS → SURGICAL EVOLUTION → VERIFY → ADVANCE**

No new implementation is considered an improvement merely because it is new. It must be demonstrably better in readability, hierarchy, depth, usefulness, interaction, and visual quality while preserving valuable existing behavior.

## 14. Release gate

Before calling an Intelligent Feed change complete, verify:

- no first-load flash/glitch
- obsolete comprehension bar removed
- correct NayaNET statement placement restored
- one primary obsidian board per intelligence event
- multi-layer 3D elevation visibly present
- inner sections vertical
- content-length agnostic
- correct color progression
- correct control placement
- Save → Smart List behavior preserved/implemented
- Share Intel + behavior preserved/implemented
- Love/Like state colors correct
- five-star rating present and usable
- no dead or decorative controls presented as functional
- responsive behavior remains coherent
- existing 5:09 shell/functionality not unnecessarily damaged

**This is the master instruction set for future NayaNET Intelligent Feed work.**
