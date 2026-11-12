# Smart Block: `body`

Reading text. 18px minimum per the reading floor, generous leading, high contrast — never gray-on-black.

## Why

Reading is the product’s cheapest interaction and its most abused. An 18px floor, 1.65 leading, and a 68ch measure are the settings that keep long text readable instead of tiring.

- **Type:** type
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `body.css`
- **Specimen:** `specimen.html`
- **States found:** `:hover` (links)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `body.css`.
2. `<p class="naya-body">Your text.</p>`
3. Variants:
   - `naya-body--lead` — opening paragraph, 19–21px fluid
   - `naya-body--quiet` — secondary copy (still passes contrast)
   - `naya-body--small` — captions, metadata, 14px
   - `naya-body--wide` — removes the 68ch measure

## Selectors in this block

```
.naya-body
.naya-body--quiet / --small / --lead / --wide
.naya-body a / .naya-body a:hover
.naya-body strong / .naya-body em
```

## Pairs with

`type/headline` (the standard text stack), `type/hero` (hero sub uses its own scale), `layout/section` (lives inside).

## Notes

- The 68ch measure is typographic (readability), not a page cap — the page stays full-width per the law.
- `text-wrap: pretty` prevents orphans and rivers.
- Links use a lighter purple (`#a583ff`) for contrast against body text, deepening on hover.
- `em` switches to the voice serif — Naya's editorial inflection inside UI text.
