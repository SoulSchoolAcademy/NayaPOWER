# Smart Block: `board`

Intelligent board container with identity spine.

## Why

Intelligent board container with identity spine. Content needs a room, not a box — the spine gives every board a Naya identity. Disparate content feels like it belongs to one mind.

- **Type:** boards
- **Source:** `Naya_4_Design_Element_Set.html` (extracted byte-true, never rewritten)
- **CSS:** `board.css`
- **Specimen:** `specimen.html`
- **States found:** :hover
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `board.css`.
3. Copy the HTML from `specimen.html`.
4. **REQUIRED: set `--ic` (identity color).** This is the block's most important input — the spine, glow, and border all derive from it. Without it, the board renders with no identity:
   ```html
   <div class="board" style="--ic: var(--purple);">
   ```
   Use any spectrum color (`var(--purple)` (#a06bff) purple, `#3fb8ff` blue, `#2fe89e` green, `#ffbf3d` gold, `#e84fff` magenta).

## Selectors in this block

```
.board
.board .corner
.board h3
.board::after
.board::before
.board:hover
```
