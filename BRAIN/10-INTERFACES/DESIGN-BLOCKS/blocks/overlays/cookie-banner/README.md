# Smart Block: `cookie-banner`

Consent banner. Bottom sheet, obsidian, jewel-purple accept. Persists the choice.

- **Type:** overlays
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `cookie-banner.css`
- **Specimen:** `specimen.html`
- **States found:** .is-on, :hover, :focus-visible, .ck-btn--ghost
- **Dependencies:** cookie-banner.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `cookie-banner.css`.
3. Copy the `.ck` markup. Buttons use `data-ck-accept` / `data-ck-decline`.
4. Include `cookie-banner.js` — shows once, stores choice in localStorage, emits `ck:choice`.

## Selectors in this block

```
.ck
.ck-actions
.ck-btn
.ck-btn--ghost
.ck-btn:focus-visible
.ck-btn:hover
.ck-copy
.ck-text
.ck-title
.ck.is-on
```

## Notes

- Copy is human: "Your presence, your rules." Never legalese.
- `ck:choice` bubbles with `detail.choice` ('accepted' | 'declined') — gate analytics on it.
- Mobile: stacks vertically, buttons go full-width.
