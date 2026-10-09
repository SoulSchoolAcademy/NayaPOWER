# Smart Block: `data-table`

Grid data table: labels left, state/proof columns, status dots, micro-headers.

- **Type:** data
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `data-table.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css`, `status-dot`

## Use it

1. Copy `data-table.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `status-dot`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.data-table
.trow
.trow span:before
.trow span:nth-child(2):before
.trow span:nth-child(3):before
.trow.thead
.trow:first-child
```
