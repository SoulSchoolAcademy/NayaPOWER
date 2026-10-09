# Smart Block: `v2-report-row`

Report row. Jewel marker, 24px claim, 18px human explanation; hairline dividers.

- **Type:** data
- **Source:** `Open_This_NayaNET_Design_V2.html`
- **Files:** `v2-report-row.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css`, `jewels/v2-facet-gem`

## Use it

1. Copy `v2-report-row.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `tokens.css`, `jewels/v2-facet-gem`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--c` per row to separate ideas by color — never repeat adjacent hues. First row drops its divider automatically.

## Selectors

```css
.report-row
.report-row:first-of-type
.report-row .jewel
.report-row p
.report-row strong
```
