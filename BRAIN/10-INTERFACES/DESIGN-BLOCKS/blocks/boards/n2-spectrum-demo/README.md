# Smart Block: `n2-spectrum-demo`

The spectrum law, live. Click a color swatch and the whole demo board re-fires in that color — the law, not a description of it.

- **Type:** boards
- **Source:** `Naya Design Elements N2.html` (extracted byte-true, never rewritten)
- **CSS:** `n2-spectrum-demo.css`
- **Specimen:** `specimen.html`
- **JS:** `n2-spectrum-demo.js`
- **States found:** :hover
- **Dependencies:** tokens.css, n2-spectrum-demo.js

## Note

CLASS COLLISION: `.demo-board` is also defined by the existing `demo-board` block (Naya_5__Epic_Elements_-_Lego_pieces.html) as a light-beam board — a different component sharing the class name. Do not include both blocks on one page without namespacing.

## Use it

1. Include `tokens.css` (once per page).
2. Include `n2-spectrum-demo.css`.
3. Copy the HTML from `specimen.html`.
4. Include `n2-spectrum-demo.js` for interactive behavior.

## Selectors in this block

```
.swatches
.sw
.sw:hover
.demo-board
.demo-beam
.demo-name
.demo-board code
```
