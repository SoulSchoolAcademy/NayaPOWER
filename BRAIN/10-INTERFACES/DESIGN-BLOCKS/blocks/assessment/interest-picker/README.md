# Smart Block: `assessment/interest-picker`

Interest picker: intro block, selectable interest cards with orb + check states, selected pills, skip action.

## Why

Asking what someone cares about should feel like an invitation, not a form. Orb-and-check interest cards with selected pills make choosing feel personal — and the skip action respects ‘not now.’

- **Type:** assessment
- **Source:** `Maxis App Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** .selected + .selected .interest-check (checked), :hover
- **Dependencies:** `--interest` per card (inline); `--ease` motion curve

> **Provenance note:** Maxis was Shawn's earlier MAXESS assessment project — not NayaNET. Only the UI grammar was extracted; no MAXIS branding or content is carried in this block.

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. Toggle `.selected` + `aria-pressed` on tap; render chosen names as `.interest-pill` chips.

## Selectors in this block

```
.interest-board
.interest-intro
.interest-eyebrow
.interest-title
.interest-description
.interest-area
.interest-area:hover
.interest-area.selected
.interest-area.selected .interest-check
.interest-orb
.interest-check
.interest-name
.interest-actions
.interest-skip
.selected-interests
.interest-pill

```
