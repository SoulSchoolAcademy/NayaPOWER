# Smart Block: `pulse-orb`

A living orb that breathes with the data. The number sits inside the orb; the
value drives its diameter and glow. Bigger value = more light, never more ink.

- **Type:** graphs
- **Source:** authored 2026-10-09 from the orb block DNA (`Naya_5_Jewel_Library.html`)
- **CSS:** `pulse-orb.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css, gem-bullet (optional, for the delta marker)

## Use it

1. Include `tokens.css` and `pulse-orb.css`.
2. Copy the `.sg-card` shell; set `--v` (0..1) on `.pulse-orb` for the value.
3. Recolor with `--oc` / `--oc-rgb` (spectrum order: purple → blue → cyan → green → gold).
4. Add `.lit` to the card when it enters view (IntersectionObserver) for the entrance.
5. `.sg-delta.up` / `.sg-delta.down` for the trend line.

## Pairs with

- `living-counter` — same single-number story, different voice
- `pulse-rings` — same heartbeat family, multi-metric
- `layout/section`, `type/headline` — page composition

## Notes

- Honors `prefers-reduced-motion`.
- The number is the hero: white, tabular numerals, largest on the card.
