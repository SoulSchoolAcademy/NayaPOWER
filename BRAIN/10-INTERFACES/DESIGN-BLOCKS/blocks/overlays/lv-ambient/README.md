# Smart Block: `lv-ambient`

The page receiving the button's light — a fixed ambient wash that follows the cursor near any `.lv-btn`/`.lv-board` and tints with its accent.

- **Type:** overlays
- **Source:** `Naya  Elite Buttons N5.html`
- **Files:** `lv-ambient.css`, `specimen.html`, `lv-ambient.js`
- **Dependencies:** tokens.css, buttons/lv-btn
- **States:** body.lv-lit

## Use it

1. Copy `lv-ambient.css` (and `lv-ambient.js` if present) next to your page.
2. Link `tokens.css` first, then `lv-ambient.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`lv-ambient.js`) — it is byte-true and self-initializing.

## Selectors

```
.lv-ambient
body.lv-lit .lv-ambient
```
