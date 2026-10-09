# Smart Block: `grid`

Responsive 12-column grid collapsing to a single column on mobile, with consistent gutters. Children can never force horizontal overflow.

- **Type:** composition
- **Source:** authored 2026-10-09 (cold-test gap fill — no source file existed)
- **CSS:** `grid.css`
- **Specimen:** `specimen.html`
- **States found:** `@media (max-width: 720px)`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page) and `grid.css`.
2. Wrap items in `<div class="cmp-grid">`.
3. Size items with `.cmp-span-1` … `.cmp-span-12` (default: each child takes one column).
4. Gutter density: `.cmp-grid--tight` (12px) or `.cmp-grid--loose` (32px). Default 20px.

## Composing

- Lives inside `section` (or `hero` for feature rows). Put `boards/*` cards, `data/*` stat blocks, or media inside the spans.
- On mobile (≤720px) every item becomes full-width automatically — no extra classes needed.
- Never set explicit widths on grid children; the spans own the sizing.

## Selectors in this block

```
.cmp-grid
.cmp-grid > *
.cmp-span-1 … .cmp-span-12
.cmp-grid--tight
.cmp-grid--loose
```
