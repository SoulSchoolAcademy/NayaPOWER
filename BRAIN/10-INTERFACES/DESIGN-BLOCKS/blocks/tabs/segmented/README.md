# Smart Block: `segmented`

Segmented control: inset dark track, 40px options, selected option lifts with edge light.

- **Type:** tabs
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `segmented.css`, `specimen.html`
- **States:** `:hover`, `:focus`, `:focus-visible`, `:focus-within`, `[aria-selected`
- **Dependencies:** `tokens.css`

## Use it

1. Copy `segmented.css` into your page or component folder.
2. Include the shared `tokens.css` on the page.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.recessed-field:focus-within,.recessed-field:focus-visible,.naya-toggle:hover,.naya-toggle:focus-visible,.smarttab:hover,.smarttab:focus-visible,.app-nav button:hover,.app-nav button:focus-visible,.segmented button:hover,.segmented button:focus-visible
.segmented
.segmented button
.segmented button[aria-selected=true]
input,.recessed-field,.naya-toggle,.smarttab,.app-nav button,.segmented button,.copy-code
```
