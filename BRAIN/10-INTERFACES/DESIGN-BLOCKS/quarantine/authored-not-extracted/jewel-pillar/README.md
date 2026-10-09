# Smart Block: `jewel-pillar`

Jeweled pillars for series data. Each pillar is cut like a gem — faceted cap,
specular edge light, glowing base. Values rise on light with a stagger, so the
series reads as a living thing, not a spreadsheet.

## Why

A bar chart reports; a jeweled pillar holds attention. Faceted caps and specular edges turn series comparisons into something worth looking at — which is exactly what makes them looked at twice.

- **Type:** graphs
- **Source:** authored 2026-10-09 from nl-chart bar DNA + gem-bullet facet formula
- **CSS:** `jewel-pillar.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` and `jewel-pillar.css`.
2. One `.jp-col` per value: `.jp-val` (number), `.jp-pillar` (the pillar), `.jp-cap` (label).
3. Set `--v` (0..1 height), `--c` / `--crgb` (spectrum color), `--d` (stagger delay).
4. Add `.lit` to `.sg-card` on entry for the rise animation.
5. Spectrum order: purple → blue → cyan → green → gold. Max five colors.

## Pairs with

- `spectrum-flow` — same series over time, different voice
- `living-counter` — the total above the series
- `type/headline`, `layout/section` — page composition
