# Smart Block: `hub-rail`

The hub rail companions — the circular rail toggle button (rotates on hover) and the quiet rail card (small caps label + body), plus the `.rail-collapsed` shell state that slides the rail off-canvas.

- **Type:** layout
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `hub-rail.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `:hover` on `.rail-toggle` (scales + rotates 90°, icon counter-rotates, purple glow), `.rail-collapsed` on the `.shell` grid parent (rail translates off-canvas, pointer-events none), responsive `@media`
- **Notes:**
  - CSS-ONLY in the source: none of these classes has a rendered instance (the shipped rail shell uses different classes; the collapse is driven by JS toggling `rail-collapsed` on `.shell`, persisted to localStorage). The specimen is reconstructed from CSS and marked as such.
  - No indexed block covers rail chrome — extracted as new.

## Use it

1. Copy `hub-rail.css` next to your page.
2. Link `tokens.css` first, then `hub-rail.css`.
3. Paste the toggle + card; toggle `.rail-collapsed` on the shell grid to collapse:

```html
<button class="rail-toggle" type="button" aria-label="Toggle rail">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">{{icon}}</svg>
</button>

<aside class="rail-card">
  <b>{{SMALL CAPS LABEL}}</b>
  <p>{{rail card body}}</p>
</aside>
```

## Selectors

```
.shell.rail-collapsed
.shell.rail-collapsed .rail.left
.rail-toggle (+ svg / :hover / :hover svg)
.rail-card (+ b / p)
```
