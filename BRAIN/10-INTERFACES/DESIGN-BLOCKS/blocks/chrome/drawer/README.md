# Smart Block: `drawer`

The Hub's slide-in drawer: backdrop + panel + open-state classes. On mobile the left rail becomes a fixed drawer (translateX(-106%) &rarr; 0). Toggle via `.drawer-open` on shell/body. Note: the fuller `.naya-drawer` variant (Ledger file) is a future extraction.

- **Type:** chrome
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `drawer.css`
- **Specimen:** `specimen.html`
- **States found:** .drawer-open (shell + body), mobile breakpoint
- **Dependencies:** drawer.js (open/close toggle), tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `drawer.css`.
3. Copy the HTML from `specimen.html`.
4. Include `drawer.js`, or toggle `.drawer-open` on `.shell` and `body` yourself.

## Selectors in this block

```
.drawer-backdrop
.shell.drawer-open .rail.left
.shell.drawer-open .drawer-backdrop
body.drawer-open
.rail.left
@media (max-width: 900px)
```
