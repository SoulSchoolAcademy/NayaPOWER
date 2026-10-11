# Smart Block: `page-shell`

The page chassis. Full-width black ground — no max-width caps, per the full-width law. Every Smart App page starts here.

## Why

Every page starts here because every page must feel like one product, not a pile of screens. The black ground, focus rings, and motion defaults are decided once, so no surface ever ships on a wrong background or with a hostile focus state.

- **Type:** layout
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `page-shell.css`
- **Specimen:** `specimen.html`
- **States found:** `:focus-visible`, `::selection`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `page-shell.css`.
3. Wrap your entire page in `<div class="naya-page">`.
4. Add `naya-page--edgelight` for the 1px top-edge light (recommended on hero-led pages).

## Selectors in this block

```
.naya-page
.naya-page--edgelight
.naya-page--edgelight::before
.naya-page ::selection
.naya-page :focus-visible
body:has(.naya-page) — UA margin reset (cold-test fix)
```

## Pairs with

`layout/section` (content rhythm), `type/hero` (page opening), everything — this is the ground all blocks sit on.

## Notes

- The ground is never pure flat black: a faint purple-tinted top wash (`rgba(141,99,245,.06)`) gives it dimension.
- `overflow-x: clip` prevents sideways scroll from decorative overflow.
- Reduced motion is honored at the chassis level so no block can animate against the user's preference.
