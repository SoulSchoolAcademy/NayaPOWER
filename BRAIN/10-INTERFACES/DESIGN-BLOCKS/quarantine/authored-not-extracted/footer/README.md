# Smart Block: `footer`

Page footer. Brand lockup, multi-column link groups, social icons, legal row. Closes the composition with a hairline of top light — it lands, never just stops.

## Why

The page’s last word should be quiet, not dead. Brand lockup, links, social icons, legal row — everything a user looks for at the bottom, set small enough that it never competes with the content above.

- **Type:** layout
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `footer.css`
- **Specimen:** `specimen.html`
- **States found:** `:hover`, responsive (`@media max-width: 900px`, `560px`), `prefers-reduced-motion`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `footer.css`.
2. Copy the specimen `<footer class="naya-footer">` structure.
3. Swap the social SVGs for your own icons, or replace the `.naya-footer__social` links with `nl-iconbtn` blocks.
4. Adjust the link groups to your sitemap — the grid handles 1–4 groups.
5. Modifiers:
   - `naya-footer--compact` — two-column grid for minimal pages

## Selectors in this block

```
.naya-footer
.naya-footer__grid
.naya-footer__brand
.naya-footer__mark-row
.naya-footer__mark
.naya-footer__wordmark
.naya-footer__tagline
.naya-footer__social
.naya-footer__group
.naya-footer__heading
.naya-footer__list
.naya-footer__legal
.naya-footer--compact
```

## Pairs with

`layout/section` (rhythm above it), `jewels/gem-bullet` (the heading markers reuse the diamond language), `buttons/nl-iconbtn` (drop-in social icon replacement), `layout/page-shell` (the ground).

## Notes

- Every link meets the 44px touch-target law, including the small legal links.
- The heading diamond markers are the exact `gem-bullet` gradient at 8px.
- Social icons ignite purple on hover with a lift — the same physics as the rest of the library.
- The grid collapses 4 → 2 → 1 columns; the brand always goes full-width first on mobile.
- Tagline and legal copy are placeholders — write your own. The structure is the block; the words are yours.
