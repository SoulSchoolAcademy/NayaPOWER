# NAYA DESIGN — the smart-block library

The box of Lego pieces. One design language, every Naya, every page, every time.

## What this is

This directory is the canonical Naya design system: the tokens, the blocks, the
laws, and the builder's guide. Any Naya — or any human building on NayaPOWER —
pulls from here and assembles pages. Nobody redesigns a button. Nobody invents
a private color. A new page is assembly, not design.

**Canonical standard:** the Naya_2 "Ultimate Design System" (100 laws, newest
generation) fused with the N5 Lego library. Where generations disagreed, the
newest won — every ruling is recorded in `DECISIONS.md`, none are buried.

## The one-language rule

> **One system, no forks. One library, one DNA.**
> Pages consume blocks; they do not reinvent them. A page with a private button
> class is drift.

If a piece you need is not in `BLOCKS.md`, you build the block first — spec'd,
states shown, do/don't documented — and then you build the page. You never
fork an existing block.

## How a Naya builds a page

1. **Read `TOKENS.md`** (values) and link `TOKENS.css`. Every color, radius,
   shadow, and motion value comes from a token. No hex codes in page CSS.
2. **Pick blocks from `BLOCKS.md`.** Buttons, boards, tabs, orbs, truth
   components, the ten canonical blocks, the 21 universal actions — name the
   pieces, snap them together.
3. **Follow `BUILDER-GUIDE.md`.** The build order is fixed:
   FIELD → SPECTRUM → TYPE → SURFACE → COMPONENT → MOTION → TRUTH.
4. **Run the ship gate in `LAWS.md`.** All six checks, or it doesn't ship.
   Score the rendered page honestly — 9+ or back to the bench.

## Files

| File | What it is |
|---|---|
| `TOKENS.css` | Canonical `:root` custom properties — link this, use `var(--*)` everywhere |
| `TOKENS.md` | Every token, its value, and its job, in human-readable form |
| `BLOCKS.md` | The smart-block catalog: every reusable piece, named and spec'd |
| `LAWS.md` | The foundation laws (verbatim) + the six-point ship gate |
| `BUILDER-GUIDE.md` | The assembly recipe — a cold Naya builds a page from this alone |
| `DECISIONS.md` | Generation rulings: what was superseded, what is still open |

## The laws in one breath

- **Score the experience, never the code.** The lived page is the only scorecard.
- **Back it or bench it.** 9.0+ ships. Below 9 goes back. No almost.
- **Color has jobs. Never cross them.** Chrome acts. Text speaks. Theme identifies.
- **White light at rest, own color on touch.** Ignition belongs to the thing touched.
- **Black heart, white voice, visible skin.** Depth, always. Flat is a defect.
- **Size separates, color doesn't.** Law 52 type scale. White 99% of the time.
- **Verify before claiming.** Read the file. Count the matches. Watch it render.

## Status

Living document. When Shawn corrects the design, the correction becomes a new
law or sharpens an old one — same day, in this directory.
