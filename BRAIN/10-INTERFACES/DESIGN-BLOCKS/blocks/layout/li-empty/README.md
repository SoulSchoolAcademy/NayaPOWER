# `li-empty`

Stream container + empty-state text: the vertical card stack (`.li-stream`) and the centered dim empty message (`.li-empty`).

- **Type:** layout
- **Source:** `Ledger Page Design.html`
- **Files:** `li-empty.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css` (none required — `--li-dim` comes from `.li-stage` in the source page)
- **Usage note:** the `.li-empty` rule is a real, styled empty-state component in the source CSS. At runtime the page actually renders an inline-styled `li-empty-box` div for the no-results case (unstyled class + `style="text-align:center;padding:48px 24px;color:#8a8a96;"`), so `.li-empty` is currently unused in the live markup — but the CSS component is complete and extraction-worthy. Adopters should use `.li-empty` directly.

## Use it

```html
<div class="li-stage">
  <div class="li-stream">
    <div class="li-empty">{{empty message}}</div>
  </div>
</div>
```

## Selectors

```css
.li-stage .li-stream
.li-stage .li-empty
```
