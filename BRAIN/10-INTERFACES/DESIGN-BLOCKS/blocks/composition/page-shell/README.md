# Smart Block: `page-shell`

The document frame every Smart App page starts from. Black obsidian ground, safe-area insets, centered max-width column. Mobile-first, zero horizontal scroll.

- **Type:** composition
- **Source:** authored 2026-10-09 (cold-test gap fill — no source file existed)
- **CSS:** `page-shell.css`
- **Specimen:** `specimen.html`
- **States found:** `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `page-shell.css`.
3. Put `class="cmp-shell"` on `<body>`.
4. Wrap all page content in `<div class="cmp-shell__inner">`.
5. Add `cmp-shell--wide` to `<body>` for dashboard-style pages (1080px column).

## Composing

- `page-shell` is always the outermost block. Inside it: one `hero`, then `section` blocks.
- `section` blocks provide the vertical rhythm; `grid` handles multi-column layout inside sections.
- Never nest a second `page-shell`.

## Selectors in this block

```
.cmp-shell
.cmp-shell__inner
.cmp-shell--wide .cmp-shell__inner
```
