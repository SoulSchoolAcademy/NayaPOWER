# Smart Block: `lv-aura`

Aura glow wrapper — a blurred accent halo behind buttons that wakes on proximity and ignites on hover.

- **Type:** jewels
- **Source:** `Naya Beautiful Button Set N4.html`
- **Files:** `lv-aura.css`, `specimen.html`, `lv-aura.js`
- **Dependencies:** tokens.css, buttons/lv-btn
- **States:** .lv-aware, :hover

## Use it

1. Copy `lv-aura.css` (and `lv-aura.js` if present) next to your page.
2. Link `tokens.css` first, then `lv-aura.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`lv-aura.js`) — it is byte-true and self-initializing.

## Selectors

```
.lv-wrap
.lv-wrap.block
.lv-aura
.lv-wrap.lv-aware .lv-aura
.lv-wrap:hover .lv-aura
.lv-wrap:focus-within .lv-aura
```
