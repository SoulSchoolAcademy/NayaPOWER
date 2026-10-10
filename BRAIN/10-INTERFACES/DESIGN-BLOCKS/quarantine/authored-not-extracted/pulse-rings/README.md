# Smart Block: `pulse-rings`

The network heartbeat. Concentric rings expand outward like sonar — each ring
is one metric, its color its identity, its pace its urgency. The center holds
the live total. A system at rest still breathes.

## Why

Urgency has a pace. Concentric sonar rings with a live total at center turn ‘the network is active’ into something you can hear with your eyes — the heartbeat, visible.

- **Type:** graphs
- **Source:** authored 2026-10-09 for the Smart Graphs visual language
- **CSS:** `pulse-rings.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` and `pulse-rings.css`.
2. `.pr-stage` holds `.pr-ring` elements + one `.pr-core`.
3. Ring: `--rc` / `--rcrgb` (spectrum color), `--pd` (pulse duration — faster = hotter metric), `animation-delay` to desync.
4. Core: `.pr-num` (tabular numerals) + `.pr-label`.
5. Add `.lit` to `.sg-card` on entry.

## Pairs with

- `pulse-orb` — same heartbeat family, single metric
- `constellation` — the network the heartbeat belongs to
- `type/headline`, `layout/section` — page composition
