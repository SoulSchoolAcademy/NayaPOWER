# Smart Block: `constellation`

A constellation map for networks — spaces, connections, ideas and how they
touch. Nodes glow in spectrum color, radius carries weight, light arcs carry
relationships. It floats gently: alive, never a diagram.

- **Type:** graphs
- **Source:** authored 2026-10-09 for the Smart Graphs visual language
- **CSS:** `constellation.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` and `constellation.css`.
2. Inline SVG `.sc-sky`; `.sc-arc` paths first (they draw), then `.sc-node` circles.
3. Node: `r` = weight, `--nc` / `--ncrgb` = spectrum color. Hub node wraps in `.sc-hub` to float.
4. Labels as `.sc-tag` text elements.
5. Add `.lit` to `.sg-card` on entry: arcs draw, then nodes fade in.
6. Spectrum order: purple (you) → blue → cyan → green → gold.

## Pairs with

- `pulse-orb` — the headline count above the map
- `pulse-rings` — network activity as heartbeat
- `type/headline`, `layout/section` — page composition
