# Smart Block: `sp-empty`

The Smart Spaces empty state — a centered jewel-marked invitation, not a dead end. 24px title, 18px lead, 14px hint, and the canonical create CTA. The copy rule for this block: invitation, never documentation ("Your first space is waiting to exist", never "No records found").

- **Type:** layout
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-empty.css`, `specimen.html`
- **States:** responsive padding ≤560px, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** `buttons/sp-btn` (the CTA is the canonical `.sp-btn.sp-btn--create` atom — link `sp-btn.css` alongside this file; ownership: `sp-btn`).

## Use it

1. Copy `sp-empty.css` into your page or component folder.
2. Link `buttons/sp-btn/sp-btn.css` on the same page for the CTA.
3. Render this block in place of the grid when the space list is empty.
4. Set `--sc` inline to tint the jewel mark and card edge.

```html
<div class="sp-empty" style="--sc:#7c3aed">
  <span class="sp-empty-mark" aria-hidden="true"></span>
  <h2 class="sp-empty-title">No spaces yet</h2>
  <p class="sp-empty-lead">Every gathering starts as an idea between people who care. Yours is welcome here.</p>
  <p class="sp-empty-hint">Create a space and invite the people who should be in the room.</p>
  <button class="sp-btn sp-btn--create" style="--sc:#7c3aed"><span class="sp-btn-icon">＋</span> Create your first space</button>
</div>
```

## Selectors

```css
.sp-empty
.sp-empty-mark
.sp-empty-title
.sp-empty-lead
.sp-empty-hint
```
