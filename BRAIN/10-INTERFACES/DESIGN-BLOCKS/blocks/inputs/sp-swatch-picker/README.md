# Smart Block: `sp-swatch-picker`

Cover-color swatch picker for the space creator — spectrum swatches at true 44px touch targets. Selected swatch wears a white ring plus its own-color glow; single-select radiogroup with arrow-key travel. Emits `sp-swatch-change` with the chosen color.

- **Type:** inputs
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-swatch-picker.css`, `sp-swatch-picker.js`, `specimen.html`
- **States:** `.on` (selected ring), `:hover` (lift + glow), `:active` (press), `:focus-visible` (white outline), `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** none — self-contained; `--sw` set inline per swatch, cycling the spectrum.

## Use it

1. Copy `sp-swatch-picker.css` + `sp-swatch-picker.js` into your page or component folder.
2. Paste the markup below; give each swatch a `--sw` and an accessible `aria-label`.
3. Listen for `sp-swatch-change` (`event.detail.swatch`) on `.sp-swatch`.

```html
<div class="sp-swatch" role="radiogroup" aria-label="Cover color">
  <button class="sp-swatch-s on" data-swatch="#7c3aed" style="--sw:#7c3aed" aria-label="Purple"></button>
  <button class="sp-swatch-s" data-swatch="#1e6fd9" style="--sw:#1e6fd9" aria-label="Blue"></button>
  <button class="sp-swatch-s" data-swatch="#0d9e6f" style="--sw:#0d9e6f" aria-label="Emerald"></button>
  <button class="sp-swatch-s" data-swatch="#d4a017" style="--sw:#d4a017" aria-label="Gold"></button>
</div>
```

## Selectors

```css
.sp-swatch
.sp-swatch-s
.sp-swatch-s:hover
.sp-swatch-s:active
.sp-swatch-s:focus-visible
.sp-swatch-s.on
```
