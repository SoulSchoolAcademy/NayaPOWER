# Smart Block: `section`

A page section: tracked kicker label, serif section title, generous vertical rhythm, spectrum-positioned accent edge.

- **Type:** composition
- **Source:** authored 2026-10-09 (cold-test gap fill — no source file existed)
- **CSS:** `section.css`
- **Specimen:** `specimen.html`
- **States found:** `@media (max-width: 560px)`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page) and `section.css`.
2. Copy the `<section class="cmp-section">` structure from `specimen.html`.
3. Set `--sc` on each section **by document order** — purple, indigo, blue, teal, emerald, lime, yellow, gold, orange, red, magenta, then repeat. Never assign color by category; adjacent sections never share a hue family.

## Composing

- Lives inside `page-shell`'s inner column. Stack sections directly — the hairline divider appears automatically.
- The `__deck` paragraph is optional; use it when the section needs one line of orientation.
- Inside a section: `grid` for multi-column layouts, `boards/*` for content cards, `buttons/*` for actions.
- For the kicker, title, and deck typography on their own (outside a section), use the `headline` block.

## Selectors in this block

```
.cmp-section
.cmp-section + .cmp-section
.cmp-section::before
.cmp-section__kicker
.cmp-section__title
.cmp-section__deck
.cmp-section__deck strong
```
