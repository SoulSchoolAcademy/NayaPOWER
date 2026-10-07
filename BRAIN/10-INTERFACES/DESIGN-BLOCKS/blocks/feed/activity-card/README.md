# Smart Block: `activity-card`

The feed card — "every event is a card, not a line." Jewel, narrative (16px/1.65), source + time meta, accent edge bar with pulse. `--ac` themes per card (default #9d75ff).

- **Type:** feed
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `activity-card.css`
- **Specimen:** `specimen.html`
- **States found:** :hover (lift + glow), :active, .activity-card-high (featured)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `activity-card.css`.
3. Copy the HTML from `specimen.html`.
4. Set `--ac` per card for the accent edge/jewel/glow.

## Selectors in this block

```
.activity-card
.activity-card:hover
.activity-card:active
.activity-card::before
.activity-card-high
.activity-card-high::after
.activity-card-top
.activity-card-jewel
.activity-card-source
.activity-card-time
.activity-card-title
.activity-card-narrative
.activity-card-meta
```
