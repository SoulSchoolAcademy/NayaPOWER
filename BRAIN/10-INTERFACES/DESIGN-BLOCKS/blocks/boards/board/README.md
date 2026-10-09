# Smart Block: `board`

Intelligent board container with identity spine.

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
   <div class="board" style="--ic: #8d63f5;">
   ```
   Use any spectrum color (`#8d63f5` purple, `#3fb8ff` blue, `#2fe89e` green, `#ffbf3d` gold, `#e84fff` magenta).

## Selectors in this block

```
.board
.board .corner
.board h3
.board::after
.board::before
.board:hover
```
