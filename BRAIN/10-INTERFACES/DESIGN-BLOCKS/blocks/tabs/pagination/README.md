# Smart Block: `pagination`

Page number controls. Obsidian pill strip; the current page is a purple jewel.

- **Type:** tabs
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `pagination.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, :focus-visible, :disabled, .is-current, .pg--compact
- **Dependencies:** pagination.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `pagination.css`.
3. Copy the `<nav class="pg">` markup from `specimen.html`.
4. Include `pagination.js` for click-to-switch + `pg:change` events.

## Selectors in this block

```
.pg
.pg--compact
.pg-btn
.pg-btn.is-current
.pg-btn.pg-nav
.pg-btn:disabled
.pg-btn:focus-visible
.pg-btn:hover
.pg-ellipsis
```

## Notes

- `.is-current` is the only filled element — purple solid, dark text. Everything else stays quiet.
- `pg:change` bubbles with `detail.page`; wire it to your data fetch.
- Arrows step between the numbered buttons present in the strip.
