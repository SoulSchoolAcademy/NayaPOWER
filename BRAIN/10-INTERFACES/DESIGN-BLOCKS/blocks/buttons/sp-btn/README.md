# Smart Block: `sp-btn`

The canonical Smart Spaces button — black heart, white voice, visible skin, own-color ignite. Dark elevated body with edge light at rest; the instance's `--sc` ignites the border and glow on hover/active. Press compresses (scale .98 + inset shadow).

- **Type:** buttons
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-btn.css`, `specimen.html`
- **States:** `:hover`, `:active` (press compression), `:focus-visible` (jewel outline), `:disabled`, `.sp-btn--create`, `.sp-btn--ghost`, `.sp-btn--block`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** none — self-contained; per-instance `--sc` set inline. Canonical owner of the `.sp-btn` atom used by `sp-toolbar`, `sp-modal-type`, `sp-empty`, `sp-magic-note`.

## Use it

1. Copy `sp-btn.css` into your page or component folder (or link it).
2. Paste the markup below where the button should live.
3. Set `--sc` inline to give the button its identity color.

```html
<button class="sp-btn sp-btn--create" style="--sc:#7c3aed">
  <span class="sp-btn-icon">＋</span> Create Space
</button>
<button class="sp-btn sp-btn--ghost">Cancel</button>
```

## Selectors

```css
.sp-btn
.sp-btn:hover, .sp-btn:focus-visible
.sp-btn:active
.sp-btn:focus-visible
.sp-btn--create
.sp-btn--ghost
.sp-btn--ghost:hover, .sp-btn--ghost:focus-visible
.sp-btn--block
.sp-btn:disabled
.sp-btn-icon
```
