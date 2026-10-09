# Smart Block: `elevated-board`

Elevated board variant: tone spine, corner jewel, authority rank line. Min-height 280px.

- **Type:** boards
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `elevated-board.css`, `specimen.html`
- **States:** `:hover`
- **Dependencies:** `tokens.css`, `source-rank`, `icon`

## Use it

1. Copy `elevated-board.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `source-rank`, `icon`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.elevated-board
.elevated-board .board-corner
.elevated-board .board-spine
.elevated-board h3
.elevated-board p
.elevated-board.editorial
.elevated-board.orbital
.elevated-board:hover
```
