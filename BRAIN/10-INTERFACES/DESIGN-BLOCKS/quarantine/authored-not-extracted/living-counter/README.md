# Smart Block: `living-counter`

The number, alive. A giant tabular-numeral counter that rolls up on entry, a
jewel delta for the trend, and a whisper of a sparkline for the story behind
it. For the stats people check every day: prices, totals, streaks.

- **Type:** graphs
- **Source:** authored 2026-10-09 for the Smart Graphs visual language
- **CSS:** `living-counter.css` · **JS:** `living-counter.js`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, `living-counter.css`, `living-counter.js`.
2. `.lc-num` with `data-to`, `data-decimals`, `data-prefix`, `data-suffix` — counts up on entry, adds `.lit` to the card.
3. `.lc-delta.up` / `.down` for the trend jewel.
4. `svg.lc-spark` with `.area` + `.line` paths for the story.
5. Without JS: the card still needs `.lit` added manually; the number shows its fallback text.

## Pairs with

- `pulse-orb` — same single-number story, different voice
- `jewel-pillar` — the series behind the total
- `type/headline`, `layout/section` — page composition
