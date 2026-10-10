# Smart Block: `section`

Content rhythm. Generous vertical spacing with full-width gutters that breathe on mobile and expand on desktop.

## Why

Pages are read in breaths, and this block sets the rhythm of each breath. Generous fluid spacing plus the glowing divider with its diamond break means long pages stay scannable instead of collapsing into walls.

- **Type:** layout
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `section.css`
- **Specimen:** `specimen.html`
- **States found:** responsive (`@media max-width: 480px`)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `section.css`.
2. Wrap each content area in `<section class="naya-section">`.
3. Modifiers:
   - `naya-section--compact` — tighter rhythm
   - `naya-section--roomy` — airier rhythm
   - `naya-section--divided` — hairline top divider with purple glow
   - `naya-section--jewel` — diamond jewel seated on the divider (pair with `--divided`)
   - `naya-section--tint` — whisper of purple atmosphere

## Selectors in this block

```
.naya-section
.naya-section--compact
.naya-section--roomy
.naya-section--divided
.naya-section--divided::before
.naya-section--jewel::after
.naya-section--tint
```

## Pairs with

`layout/page-shell` (the ground), `type/headline` + `type/body` (section content), `layout/row-grid` (section layout).

## Notes

- Padding uses `clamp()` so rhythm scales fluidly — never cramped on mobile, never lost on desktop.
- The divider's purple glow (`rgba(141,99,245,.35)`) ties sections to the soul accent without shouting.
- The jewel is the library's diamond language (`gem-bullet` family) at 12px.
