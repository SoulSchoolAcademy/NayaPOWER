# Smart Block: `error-page`

404/error page composition. Full-bleed obsidian, ambient orbit glow, jewel gradient code, Naya-voiced copy.

- **Type:** layout
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `error-page.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, .ep-btn--ghost
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `error-page.css`.
3. Use `<main class="ep">` as the page root. Swap `.ep-code` for any status (404, 500, 403).

## Selectors in this block

```
.ep
.ep-actions
.ep-btn
.ep-btn--ghost
.ep-btn:hover
.ep-code
.ep-id
.ep-sub
.ep-title
```

## Notes

- The code numeral uses the voice serif gradient (white → purple), same grammar as `voice-type`.
- Copy is warm, never technical — "This door hasn't been built yet."
- `.ep-id` carries the error code for support reference.
- No JavaScript required — pure CSS block. Wire buttons to your router.
