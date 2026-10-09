# Smart Block: `hero`

The top of the page: emblem, kicker, headline, subhead, primary action row. Elevated at rest — hairline edge, contact shadow, restrained spectrum wash. Centered, thumb-first.

- **Type:** composition
- **Source:** authored 2026-10-09 (cold-test gap fill — no source file existed)
- **CSS:** `hero.css`
- **Specimen:** `specimen.html`
- **States found:** `:active` (tap compress), `@media (max-width: 560px)`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page) and `hero.css`.
2. Copy the `<header class="cmp-hero">` structure from `specimen.html`.
3. Set `--hc` to the page's ignition color (default purple `#8d63f5`).
4. Fill `.cmp-hero__actions` with `buttons/*` blocks (e.g. `naya-btn`). The row guards every action to a 44px minimum touch target.

## Composing

- Lives first inside `page-shell`'s inner column, before any `section`.
- The built-in diamond emblem is self-contained. For a living emblem, replace it with an `orbs/*` block — same slot, same 64px footprint.
- Headline/subhead here are hero-scoped. For headlines elsewhere on the page, use the `headline` block.

## Selectors in this block

```
.cmp-hero
.cmp-hero::after
.cmp-hero__emblem
.cmp-hero__kicker
.cmp-hero__title
.cmp-hero__sub
.cmp-hero__actions
.cmp-hero__actions > *
.cmp-hero__actions > :active
```
