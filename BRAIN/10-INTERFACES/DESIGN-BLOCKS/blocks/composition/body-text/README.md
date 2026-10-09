# Smart Block: `body-text`

Body copy: readable measure, silver/white voice, breathing spacing. LAW ZERO — readability supreme.

- **Type:** composition
- **Source:** authored 2026-10-09 (cold-test gap fill — no source file existed)
- **CSS:** `body-text.css`
- **Specimen:** `specimen.html`
- **States found:** `a:hover`, `a:focus-visible`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page) and `body-text.css`.
2. Use `.cmp-body` for paragraphs. `.cmp-body--lead` for the opening paragraph (20px, brighter). `.cmp-body--detail` for evidence and captions (14px — nothing readable goes smaller).
3. **Never color body text with a jewel color.** Emphasis is white (`<strong>`), links underline in purple and brighten on hover.

## Composing

- Follows `headline`'s subhead naturally: headline → sub → body paragraphs.
- Inside `boards/*` cards, body text inherits the card's padding — no extra wrappers needed.
- Keep paragraphs under 65ch; the block enforces it with `max-width`.

## Selectors in this block

```
.cmp-body
.cmp-body:last-child
.cmp-body strong
.cmp-body a
.cmp-body a:hover
.cmp-body a:focus-visible
.cmp-body--detail
.cmp-body--lead
```
