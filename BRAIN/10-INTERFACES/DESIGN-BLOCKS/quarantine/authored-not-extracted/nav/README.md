# Smart Block: `nav`

Top navigation bar. Logo left, links, CTA right. Sticky, translucent, floating above the page on a hairline of light.

## Why

Nobody should have to hunt for where they are. A sticky translucent bar — logo left, CTA right, 44px+ touch targets — keeps the way in and the way forward always reachable and always tappable.

- **Type:** layout
- **Source:** authored 2026-10-09 for the Smart Blocks library (composition layer)
- **CSS:** `nav.css`
- **Specimen:** `specimen.html`
- **States found:** `:hover`, `.naya-nav--open` (mobile menu), responsive (`@media max-width: 860px`), `prefers-reduced-motion`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css`, then `nav.css`.
2. Copy the specimen `<nav class="naya-nav">` structure.
3. Set the active page with `naya-nav__link--active` + `aria-current="page"`.
4. Drop a `naya-btn` (or `primo`) into `.naya-nav__cta`.
5. The specimen includes minimal toggle JS — keep it or wire your own; the CSS only needs `.naya-nav--open` toggled on `.naya-nav`.
6. Modifiers:
   - `naya-nav--static` — scrolls away with the page instead of sticking
   - `naya-nav--overlay` — transparent over a hero; add `naya-nav--scrolled` via JS once scrolled

## Selectors in this block

```
.naya-nav
.naya-nav__row
.naya-nav__brand
.naya-nav__mark
.naya-nav__wordmark
.naya-nav__links
.naya-nav__link
.naya-nav__link--active
.naya-nav__cta
.naya-nav__toggle
.naya-nav--open
.naya-nav--static
.naya-nav--overlay
.naya-nav--scrolled
```

## Pairs with

`buttons/naya-btn` (CTA — the specimen uses it), `jewels/gem-bullet` (the active marker reuses the diamond language), `layout/page-shell` (the ground it floats over), `type/hero` (sits beneath on landing pages).

## Notes

- Every interactive element meets the 44px touch-target law: links are 44px, 52px on mobile, the toggle is 44×44.
- The brand mark is the orb language (specular at 34%/26%, purple core) — replace with your own logo or keep the jewel.
- The active link's diamond marker is the exact `gem-bullet` gradient (`140deg, #fff → #8d63f5 50% → #18101a`).
- Translucency uses `backdrop-filter: blur(14px)` — degrades gracefully to solid translucent black where unsupported.
- On mobile the CTA stays in the bar; only links collapse. Never hide the primary action behind the hamburger.
