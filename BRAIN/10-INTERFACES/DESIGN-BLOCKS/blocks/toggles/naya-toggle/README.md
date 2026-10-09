# Smart Block: `naya-toggle`

54px toggle switch: black track, white knob, purple ignite, full ARIA switch semantics.

- **Type:** toggles
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `naya-toggle.css`, `specimen.html`
- **States:** `:hover`, `:focus`, `:focus-visible`, `:focus-within`, `[aria-checked`
- **Dependencies:** `tokens.css`

## Use it

1. Copy `naya-toggle.css` into your page or component folder.
2. Include the shared `tokens.css` on the page.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.naya-toggle
.naya-toggle span
.naya-toggle[aria-checked=true]
.naya-toggle[aria-checked=true] span
.recessed-field:focus-within,.recessed-field:focus-visible,.naya-toggle:hover,.naya-toggle:focus-visible,.smarttab:hover,.smarttab:focus-visible,.app-nav button:hover,.app-nav button:focus-visible,.segmented button:hover,.segmented button:focus-visible
input,.recessed-field,.naya-toggle,.smarttab,.app-nav button,.segmented button,.copy-code
```
