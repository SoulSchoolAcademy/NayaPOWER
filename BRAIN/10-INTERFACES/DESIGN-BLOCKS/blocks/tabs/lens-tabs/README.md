# Smart Block: `lens-tabs`

The three compact single-line lens buttons (Collective/Personal/Activity) — one row, real navigation. Each lens has its own hover glow.

## Why

Three lenses, one row. The compact Collective/Personal/Activity buttons with per-lens hover glow make switching perspectives feel like shifting focus, not reloading a page.

- **Type:** tabs
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `lens-tabs.css`
- **Specimen:** `specimen.html`
- **States found:** :hover (per-lens glow), .active, mobile
- **Dependencies:** lens-tabs.js (selection), tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `lens-tabs.css`.
3. Copy the HTML from `specimen.html`.
4. Include `lens-tabs.js` for single-select behavior.

## Selectors in this block

```
.lens-tabs
.lens-tab
.lens-tab b
.lens-tab.active
.lens-tab.lens-collective:hover
.lens-tab.lens-personal:hover
.lens-tab.lens-activity:hover
@media (max-width: 640px)
```
