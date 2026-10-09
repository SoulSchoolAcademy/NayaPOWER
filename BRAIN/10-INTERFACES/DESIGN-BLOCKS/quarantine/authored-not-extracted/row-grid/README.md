# Smart Block: `row-grid`

Responsive layout. Mobile-first grids, rows, and splits that collapse cleanly.

- **Type:** layout
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `row-grid.css`
- **Specimen:** `specimen.html`
- **States found:** responsive (`640px`, `900px`, `1024px` breakpoints)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `row-grid.css`.
2. Grids: `<div class="naya-grid naya-grid--3">` — 1 col mobile → 2 col at 640px → 3 col at 1024px.
3. Rows: `<div class="naya-row">` — stacks on mobile, horizontal from 640px.
4. Splits: `<div class="naya-split">` — halves that stack below 900px.
5. Modifiers: `--tight` / `--loose` gaps, `--center` / `--stretch` alignment, `--top` / `--spread` row variants, `--flip` split order.

## Selectors in this block

```
.naya-grid / .naya-grid--2 / .naya-grid--3 / .naya-grid--4
.naya-grid--tight / .naya-grid--loose
.naya-grid--center / .naya-grid--stretch
.naya-row / .naya-row--top / .naya-row--spread
.naya-split / .naya-split--flip
```

## Pairs with

`layout/section` (grid lives inside sections), `boards/*` (grid cells are usually cards), `type/*` (content inside cells).

## Notes

- Gaps use `clamp()` — the whole library breathes on one scale.
- No JavaScript. Pure CSS. Nothing to break.
- Breakpoints (640 / 900 / 1024) are the library standard — don't invent new ones.
