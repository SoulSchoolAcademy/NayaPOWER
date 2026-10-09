# Smart Block: `v2-swatch`

Jewel-lit color swatch. Name + hex on a dark card, ignites in its own color on hover.

- **Type:** jewels
- **Source:** `Open_This_NayaNET_Design_V2.html`
- **Files:** `v2-swatch.css`, `specimen.html`
- **States:** :hover
- **Dependencies:** `tokens.css`, `jewels/v2-facet-gem`

## Use it

1. Copy `v2-swatch.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `tokens.css`, `jewels/v2-facet-gem`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--c` per swatch; the card border and hover glow follow it. Add swatches inside `.palette` for the responsive grid.

## Selectors

```css
.palette
.swatch
.swatch .jewel
.swatch strong
.swatch small
.swatch:hover
```
