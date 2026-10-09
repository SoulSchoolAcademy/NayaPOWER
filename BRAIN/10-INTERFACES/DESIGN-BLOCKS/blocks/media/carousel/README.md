# Smart Block: `carousel`

Image/content slider gallery. 17px cards, glass edge arrows, jewel dots in spectrum order.

- **Type:** media
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `carousel.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, :focus-visible, .is-on
- **Dependencies:** carousel.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `carousel.css`.
3. Copy the `.cr` markup. Add `data-autoplay="ms"` for autoplay (pauses on hover/touch).
4. Include `carousel.js` for arrows, dots, swipe, and `cr:change` events.

## Selectors in this block

```
.cr
.cr-arrow
.cr-arrow:focus-visible
.cr-arrow:hover
.cr-cap
.cr-dot
.cr-dot.is-on
.cr-dot:hover
.cr-dots
.cr-next
.cr-prev
.cr-slide
.cr-slide img
.cr-track
```

## Notes

- Active dot glows in its spectrum position color (magenta → purple → blue → green → gold).
- Swipe works on touch; arrows are glass with purple glow on hover.
- Captions sit on a bottom gradient scrim — 14px detail text.
