# Smart Block: `assessment/answer`

Answer option: 52px jewel icon / title + sub copy / chevron grid, 66px min-height, per-answer `--accent`.

## Why

An assessment is only as good as its answers. A 52px jewel icon, title, sub copy, and a 66px minimum target make each option feel considered — so the choice itself feels meaningful.

- **Type:** assessment
- **Source:** `Maxis App Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, :focus-visible, [aria-pressed=true] (selected)
- **Dependencies:** `--accent` per answer (inline); `--ease` motion curve

> **Provenance note:** Maxis was Shawn's earlier MAXESS assessment project — not NayaNET. Only the UI grammar was extracted; no MAXIS branding or content is carried in this block.

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. Set `--accent` per answer; toggle `aria-pressed` on selection.

## Selectors in this block

```
.answers
.answer
.answer .jewel
.answer .glyph
.answer-copy
.answer-title
.answer-sub
.answer .chevron

```
