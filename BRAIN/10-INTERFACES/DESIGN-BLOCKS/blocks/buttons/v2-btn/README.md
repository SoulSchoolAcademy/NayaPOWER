# Smart Block: `v2-btn`

The canonical V2 button. Black center, white rim, icon slot; color ignites on interaction via `--glow`. Honest disabled state.

- **Type:** buttons
- **Source:** `Open_This_NayaNET_Design_V2.html`
- **Files:** `v2-btn.css`, `specimen.html`
- **States:** :hover, :focus-visible, :active, :disabled
- **Dependencies:** `tokens.css`

## Use it

1. Copy `v2-btn.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `tokens.css`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--glow` to the meaning color (default purple). Put a glyph in `.btn-icon`. If the action is not real yet, use `disabled` — never a fake click.

## Selectors

```css
.btn
.btn:hover,.btn:focus-visible
.btn:active
.btn:disabled
.btn-icon
```
