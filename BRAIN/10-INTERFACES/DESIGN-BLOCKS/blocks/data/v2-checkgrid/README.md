# Smart Block: `v2-checkgrid`

Quality gate grid. Pre-ship checks as jewel cards: the check name and what it really means.

- **Type:** data
- **Source:** `Open_This_NayaNET_Design_V2.html`
- **Files:** `v2-checkgrid.css`, `specimen.html`
- **States:** responsive stack
- **Dependencies:** `tokens.css`, `jewels/v2-facet-gem`

## Use it

1. Copy `v2-checkgrid.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `tokens.css`, `jewels/v2-facet-gem`.
3. Paste the markup from `specimen.html` where the component should live.
4. One check per card, `--c` spaced across the grid. A check that cannot be verified honestly does not ship.

## Selectors

```css
.checkgrid
.check
.check .jewel
.check b
.check p
```
