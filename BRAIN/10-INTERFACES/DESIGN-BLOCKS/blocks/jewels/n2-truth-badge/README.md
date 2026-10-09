# Smart Block: `n2-truth-badge`

Truth badge. LIVE / DEMO / LOCAL status pill with a glowing dot — truth is part of the visual language.

- **Type:** jewels
- **Source:** `Naya Design Elements N2.html` (extracted byte-true, never rewritten)
- **CSS:** `n2-truth-badge.css`
- **Specimen:** `specimen.html`
- **States found:** .live, .demo, .local
- **Dependencies:** tokens.css

## Note

Defined in the design standard but unused in the source HTML — specimen constructed from the class semantics. CLASS COLLISION: `.truth` is also defined by `n4-truth-card` (Naya Design Standard Showcase (1).html) as a claim/proof card. Do not include both blocks on one page without namespacing.

## Use it

1. Include `tokens.css` (once per page).
2. Include `n2-truth-badge.css`.
3. Copy the HTML from `specimen.html`.
4. No JavaScript needed.

## Selectors in this block

```
.truth
.truth .tdot
.truth.live
.truth.demo
.truth.local
```
