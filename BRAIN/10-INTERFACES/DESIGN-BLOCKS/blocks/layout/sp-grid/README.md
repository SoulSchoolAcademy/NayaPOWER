# Smart Block: `sp-grid`

The responsive Smart Spaces grid — auto-fill card grid at `minmax(300px, 1fr)` with 22px gaps matching the sp-card rhythm. Full-width with no max-width cap; collapses to a single column at the page's 760px breakpoint. Pure CSS, no JS.

- **Type:** layout
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-grid.css`, `specimen.html`
- **States:** `@media (max-width: 760px)` (single column, 18px gap), `.sp-grid--tight`, `.sp-grid--loose`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** none. Pairs with `cards/sp-card` (cards) and `layout/sp-empty` (zero-state).

## Use it

1. Copy `sp-grid.css` into your page or component folder.
2. Wrap any number of `.sp-card` elements in `.sp-grid`.

```html
<div class="sp-grid">
  <div class="sp-card" style="--sc:#7c3aed">…</div>
  <div class="sp-card" style="--sc:#1e6fd9">…</div>
  <div class="sp-card" style="--sc:#0d9e6f">…</div>
</div>
```

## Selectors

```css
.sp-grid
.sp-grid--tight
.sp-grid--loose
```
