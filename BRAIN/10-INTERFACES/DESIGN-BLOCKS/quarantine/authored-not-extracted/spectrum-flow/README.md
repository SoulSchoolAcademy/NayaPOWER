# Smart Block: `spectrum-flow`

Layered spectrum bands showing the composition of a whole over time — a river,
not a stack of bars. Each band is one series; its thickness at any point is its
share. The bands drift slowly: the flow never freezes, because the data doesn't.

## Why

Composition is hard to read as numbers. Layered spectrum bands flowing like a river let the eye watch parts become a whole over time — proportion you can feel, not compute.

- **Type:** graphs
- **Source:** authored 2026-10-09 for the Smart Graphs visual language
- **CSS:** `spectrum-flow.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` and `spectrum-flow.css`.
2. Inline SVG `.sf-river`; one `<path class="sf-band">` per series inside `.sf-bands`.
3. Fill bands with the `sfG` gradients (or your own spectrum fills), heaviest series on top.
4. Add `.lit` to `.sg-card` on entry.
5. Spectrum order: purple → blue → cyan → green → gold. Max five bands.

## Pairs with

- `jewel-pillar` — same series, point-in-time voice
- `pulse-orb` — the headline number above the flow
- `type/headline`, `layout/section` — page composition
