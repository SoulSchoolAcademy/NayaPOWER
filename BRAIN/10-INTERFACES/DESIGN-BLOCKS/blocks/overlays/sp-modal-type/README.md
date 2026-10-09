# Smart Block: `sp-modal-type`

The space-type selector modal — "What kind of space?" Space-type options (Gathering, Channel, Circle, Studio) render as selectable cards, each with its own jewel mark and description. Also carries the sp modal typography kit: `.sp-mtitle` (24) / `.sp-msub` (18) / `.sp-mnote` (14) / `.sp-mlabel` (11 kicker).

- **Type:** overlays
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-modal-type.css`, `sp-modal-type.js`, `specimen.html`
- **States:** `.sp-mback.open`, `.sp-mtype-opt.on` (selected, own-color jewel edge + glow), `:hover`, `:active` (press), `:focus-visible`, option grid 2→1 col ≤520px, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** `buttons/sp-btn` (the footer actions are the canonical `.sp-btn` atoms — link `sp-btn.css` alongside this file; ownership: `sp-btn`). Self-contained otherwise; `--sc` tint per instance, `--oc` per option.

## Use it

1. Copy `sp-modal-type.css` + `sp-modal-type.js` into your page or component folder.
2. Link `buttons/sp-btn/sp-btn.css` on the same page for the actions.
3. Paste the markup below; open with `back.spModalType.open()`, close with `.close()`.
4. Listen for `sp-type-change` (`event.detail.type`) on `.sp-mtype` to read the selection.
5. Close triggers: `[data-sp-close]` elements, backdrop click, `Escape`.

```html
<div class="sp-mback">
  <div class="sp-mtype" role="dialog" aria-modal="true" aria-labelledby="spmt-t" style="--sc:#7c3aed">
    <div class="sp-mtype-head">
      <p class="sp-mlabel">New space</p>
      <h2 class="sp-mtitle" id="spmt-t">What kind of space?</h2>
      <p class="sp-msub">Pick the shape that fits your people.</p>
      <button class="sp-mtype-x" data-sp-close aria-label="Close">✕</button>
    </div>
    <div class="sp-mtype-grid" role="radiogroup" aria-label="Space type">
      <button class="sp-mtype-opt on" data-type="gathering" style="--oc:#7c3aed">
        <span class="sp-mtype-jewel" aria-hidden="true"></span>
        <span class="sp-mtype-name">Gathering</span>
        <span class="sp-mtype-desc">An open room for people, posts, and conversation.</span>
      </button>
      <button class="sp-mtype-opt" data-type="channel" style="--oc:#1e6fd9">
        <span class="sp-mtype-jewel" aria-hidden="true"></span>
        <span class="sp-mtype-name">Channel</span>
        <span class="sp-mtype-desc">Broadcast updates to everyone who follows.</span>
      </button>
      <button class="sp-mtype-opt" data-type="circle" style="--oc:#0d9e6f">
        <span class="sp-mtype-jewel" aria-hidden="true"></span>
        <span class="sp-mtype-name">Circle</span>
        <span class="sp-mtype-desc">Private and trusted — just your chosen few.</span>
      </button>
      <button class="sp-mtype-opt" data-type="studio" style="--oc:#d4a017">
        <span class="sp-mtype-jewel" aria-hidden="true"></span>
        <span class="sp-mtype-name">Studio</span>
        <span class="sp-mtype-desc">Build together — a project room with its own rhythm.</span>
      </button>
    </div>
    <div class="sp-mtype-actions">
      <button class="sp-btn sp-btn--ghost" data-sp-close>Back</button>
      <button class="sp-btn sp-btn--create" style="--sc:#7c3aed">Continue →</button>
    </div>
  </div>
</div>
```

## Selectors

```css
.sp-mback, .sp-mback.open
.sp-mtype
.sp-mtitle, .sp-msub, .sp-mnote, .sp-mlabel
.sp-mtype-head, .sp-mtype-x, .sp-mtype-x:hover, .sp-mtype-x:active
.sp-mtype-grid
.sp-mtype-opt, .sp-mtype-opt:hover, .sp-mtype-opt:active, .sp-mtype-opt.on, .sp-mtype-opt:focus-visible
.sp-mtype-jewel, .sp-mtype-name, .sp-mtype-desc
.sp-mtype-actions
```
