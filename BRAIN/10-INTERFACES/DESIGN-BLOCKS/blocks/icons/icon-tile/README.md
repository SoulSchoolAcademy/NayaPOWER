# Smart Block: `icon-tile`

Icon tile: faceted mini-gem socket + label. The icon stays white; meaning supplies color.

- **Type:** icons
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `icon-tile.css`, `specimen.html`
- **States:** `:hover`
- **Dependencies:** `tokens.css`, `mini-gem`, `icon`

## Use it

1. Copy `icon-tile.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `mini-gem`, `icon`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.icon-tile
.icon-tile:hover .mini-gem
.icon-tile:hover .mini-gem.diamond
```
