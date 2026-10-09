# Smart Block: `sp-toolbar`

The Smart Spaces discovery toolbar — title cluster (kicker + 24px name + member count), a segmented Grid/List view switcher, and the "＋ Create Space" CTA. Follows the sp-card chrome language: black elevated ground, jewel kicker, silver meta.

- **Type:** cards
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-toolbar.css`, `sp-toolbar.js`, `specimen.html`
- **States:** `.on` (active view, jewel edge + glow), `:hover`, `:active` (press), `:focus-visible`, responsive column stack ≤640px, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** `buttons/sp-btn` (the Create CTA is the canonical `.sp-btn.sp-btn--create` atom — link `sp-btn.css` alongside this file; ownership: `sp-btn`).

## Use it

1. Copy `sp-toolbar.css` + `sp-toolbar.js` into your page or component folder.
2. Link `buttons/sp-btn/sp-btn.css` on the same page for the CTA.
3. Paste the markup below where the toolbar should live.
4. Set `--sc` inline to tint the kicker and the active view pill.
5. Listen for the `sp-view-change` event (`event.detail.view` = "grid" | "list") to swap the grid.

```html
<div class="sp-toolbar" style="--sc:#7c3aed">
  <div class="sp-tb-title">
    <span class="sp-tb-kicker">Smart Spaces</span>
    <h2 class="sp-tb-name">Your Spaces</h2>
    <span class="sp-tb-count">12 spaces</span>
  </div>
  <div class="sp-tb-controls">
    <div class="sp-tb-views" role="tablist" aria-label="View">
      <button class="sp-tb-view on" data-view="grid">Grid</button>
      <button class="sp-tb-view" data-view="list">List</button>
    </div>
    <button class="sp-btn sp-btn--create" style="--sc:#7c3aed"><span class="sp-btn-icon">＋</span> Create Space</button>
  </div>
</div>
```

## Selectors

```css
.sp-toolbar
.sp-tb-kicker
.sp-tb-name
.sp-tb-count
.sp-tb-controls
.sp-tb-views
.sp-tb-view
.sp-tb-view:hover
.sp-tb-view:active
.sp-tb-view.on
.sp-tb-view:focus-visible
```
