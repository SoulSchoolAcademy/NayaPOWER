# Smart Block: `headline`

Section titles. 24px per the type scale, white, confident — with optional kicker and jewel marker.

- **Type:** type
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `headline.css`
- **Specimen:** `specimen.html`
- **States found:** responsive (`clamp()` on `--lg`)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `headline.css`.
2. Basic: `<h2 class="naya-headline">Title</h2>`
3. With kicker:
   ```html
   <div class="naya-headline-group">
     <span class="naya-headline__kicker">Kicker</span>
     <h2 class="naya-headline">Title</h2>
   </div>
   ```
4. With jewel: `<h2 class="naya-headline naya-headline--jewel">Title</h2>`
5. Sizes: `naya-headline--sm` (20px), `naya-headline--lg` (28–36px fluid).

## Selectors in this block

```
.naya-headline
.naya-headline__kicker
.naya-headline--jewel / .naya-headline--jewel::before
.naya-headline--sm / .naya-headline--lg
.naya-headline-group
```

## Pairs with

`type/body` (headline + body = the standard section text stack), `layout/section` (lives inside), `jewels/gem-bullet` (the jewel shares its DNA).

## Notes

- The jewel is the exact `gem-bullet` formula: 140° gradient, white → tone → dark, rotated 45°, glow.
- Use the right heading level (`h2`, `h3`) for document structure — the class handles the look.
- `text-wrap: balance` prevents orphaned words on display lines.
