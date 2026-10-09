# Smart Block: `hero`

The page opening. Large editorial headline with eyebrow kicker, sub-line, and CTA row.

## Why

The first three seconds of a page decide whether anyone stays. Voice serif at editorial scale, a purple kicker, and a staggered entrance give the opening the weight of a cover, not a header.

- **Type:** type
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `hero.css`
- **Specimen:** `specimen.html`
- **States found:** `@media (prefers-reduced-motion: no-preference)` entrance animation
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `hero.css`.
2. Structure:
   ```html
   <header class="naya-hero">
     <span class="naya-hero__eyebrow">Kicker</span>
     <h1 class="naya-hero__title">Headline with <span class="naya-accent">accent</span></h1>
     <p class="naya-hero__sub">Sub-line.</p>
     <div class="naya-hero__actions"><!-- buttons --></div>
   </header>
   ```
3. `naya-hero--center` for centered layout.
4. Wrap accent words in `<span class="naya-accent">` for the purple gradient treatment.

## Selectors in this block

```
.naya-hero / .naya-hero--center
.naya-hero__eyebrow
.naya-hero__title
.naya-hero__title .naya-accent
.naya-hero__sub
.naya-hero__actions
```

## Pairs with

`layout/page-shell` (ground), `layout/section` (spacing), `buttons/naya-btn` or `buttons/orbit-btn` (CTAs in the actions row).

## Notes

- Headline uses the voice serif (`--voice`: Cormorant Garamond) — Naya's editorial voice. Body UI stays Inter.
- `text-wrap: balance` keeps display lines elegant; `pretty` keeps the sub-line readable.
- Entrance animation is staggered (eyebrow → title → sub → actions) and fully disabled under reduced motion.
- The dimensional text-shadow is subtle — depth, not glow.
