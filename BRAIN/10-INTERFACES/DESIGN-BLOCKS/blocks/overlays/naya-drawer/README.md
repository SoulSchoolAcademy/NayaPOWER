# Smart Block: `naya-drawer`

Right-side notification drawer: fixed panel with backdrop, head, and scroll list. Distinct from the wave's chrome/drawer (left nav rail) — this is the notification surface.

- **Type:** overlays
- **Source:** `naya5/smart-blocks-library @ 1dc1241e (branch) — ported 2026-10-09`
- **CSS:** `naya-drawer.css`
- **Specimen:** `specimen.html`
- **JS:** `naya-drawer.js`
- **Dependencies:** tokens.css, naya-drawer.js
- **States:** [hidden], .is-unread

## Use it

1. Include the shared `tokens.css` (once per page).
2. Include `naya-drawer.css`.
3. Include `naya-drawer.js` for interactive behavior.
4. Copy the HTML from `specimen.html`.
5. Include `naya-drawer.js`, or wire your own open/close — the block is pure CSS + hidden attribute.

## Selectors in this block

```
.naya-drawer
.naya-drawer-backdrop
.naya-drawer-head
.naya-drawer-list
.naya-note
```

Not the wave's `chrome/drawer` (left nav rail): this is the right-side notification surface.
