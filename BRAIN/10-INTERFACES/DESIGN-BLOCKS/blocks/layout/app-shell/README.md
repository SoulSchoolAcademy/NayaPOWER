# Smart Block: `app-shell`

App chassis: 230px sidebar + main grid, intelligence header, metrics row, board well.

- **Type:** layout
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `app-shell.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css`, `app-nav`, `sphere`, `metric`, `icon`

## Use it

1. Copy `app-shell.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `app-nav`, `sphere`, `metric`, `icon`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.app-board
.app-board h4
.app-board p
.app-intelligence
.app-intelligence .sphere
.app-intelligence .sphere:after
.app-intelligence b
.app-intelligence small
.app-main
.app-metrics
.app-shell
.app-side
.app-top
.app-top h3
```
