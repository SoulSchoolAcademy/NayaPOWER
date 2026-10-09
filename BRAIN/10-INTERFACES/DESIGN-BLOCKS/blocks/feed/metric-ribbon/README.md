# Smart Block: `metric-ribbon`

The stat ribbon: auto-fit grid, 1px hairline gaps, one stat per cell. The `.unknown` variant renders honest "not yet" states. Also covers the Ledger li-card stat pattern (same grammar).

- **Type:** feed
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `metric-ribbon.css`
- **Specimen:** `specimen.html`
- **States found:** .unknown (honest pending state)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `metric-ribbon.css`.
3. Copy the HTML from `specimen.html`.
4. Add `.unknown` to a metric for the honest pending treatment.

## Selectors in this block

```
.metric-ribbon
.metric
.metric b
.metric span
.metric.unknown
.digest-stats
```
