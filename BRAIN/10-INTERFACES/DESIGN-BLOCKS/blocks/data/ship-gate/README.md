# Smart Block: `ship-gate`

The ship gate: spectrum progress bar that fills as checks clear, CLEARED FOR LAUNCH state, and per-color check rows with custom checkboxes.

- **Type:** data
- **Source:** `Naya Epic Elements - Lego pieces N5.html`
- **Files:** `ship-gate.css`, `specimen.html`, `ship-gate.js`
- **Dependencies:** tokens.css
- **States:** .open, :checked, :hover

## Use it

1. Copy `ship-gate.css` (and `ship-gate.js` if present) next to your page.
2. Link `tokens.css` first, then `ship-gate.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`ship-gate.js`) — it is byte-true and self-initializing.

## Selectors

```
.gate-head
.gate-bar
.gate-fill
.gate-shine
.gate-status
.gate-status .gate-lock
.gate-status.open
.gate-status.open .gate-lock
.checks
.check
.check:hover
.check .stage-n
.check input
.check input:checked
.check input:checked::after
.check:has(input:checked)
.check:has(input:checked) .stage-n
.check:has(input:checked) span:last-child
```
