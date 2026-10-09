# Smart Block: `command-palette`

⌘K quick-action palette. Centered obsidian command bar, live filtering, jewel-grouped results.

- **Type:** overlays
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `command-palette.css`
- **Specimen:** `specimen.html`
- **States found:** .is-on, .is-active
- **Dependencies:** command-palette.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `command-palette.css`.
3. Copy the `.cp-backdrop` + `.cp` markup. Items need `data-action` and `data-group`.
4. Include `command-palette.js` — global ⌘K/Ctrl+K opens it; emits `cp:run` with `detail.action`.

## Selectors in this block

```
.cp
.cp-backdrop
.cp-backdrop.is-on
.cp-foot
.cp-hint
.cp-icon
.cp-input
.cp-input-row
.cp-item
.cp-item.is-active
.cp-jewel
.cp-kbd
.cp-label
.cp-list
.cp-none
.cp.is-on
```

## Notes

- Jewel color encodes the verb: blue = go, magenta = do, green = ask.
- Arrow keys navigate, Enter runs, Escape closes. Filter is substring, case-insensitive.
- `cp:run` carries the action id — the host app executes it. The palette never executes itself.
- Only real commands. A palette entry that does nothing violates the honesty law.
