# Smart Block: `breadcrumbs`

Breadcrumb trail. Quiet text links, jewel separators cycling the spectrum (never repeating adjacent hues), current page in white.

- **Type:** tabs
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `breadcrumbs.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, :focus-visible, .bc-current, .bc-collapse
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `breadcrumbs.css`.
3. Copy the `<nav><ol class="bc">` markup from `specimen.html`.

## Selectors in this block

```
.bc
.bc-collapse
.bc-current
.bc-item
.bc-link
.bc-link:focus-visible
.bc-link:hover
.bc-sep
```

## Notes

- Separators are 7px jewels following the global spectrum sequence (magenta → purple → blue → green → gold).
- `.bc-collapse` hides middle segments on deep trails; wire it to expand the full path.
- No JavaScript required — pure CSS block.
