# Smart Block: `sp-magic-note`

The AI-drafted note preview card — "✨ Drafted for you". A gentle shimmer sweeps the card at rest (paused under `prefers-reduced-motion`); **Accept** keeps the draft and resolves the card to a done state, **Edit** swaps the text for an inline editor with Save/Cancel. Copy stays invitational: the draft reads like a warm introduction, never a system notice.

- **Type:** cards
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-magic-note.css`, `sp-magic-note.js`, `specimen.html`
- **States:** `@keyframes sp-mnote-shimmer` (rest), `.is-editing` (editor swap), `.is-done` (resolved), `@media (prefers-reduced-motion: reduce)` (shimmer off)
- **Dependencies:** `buttons/sp-btn` (Accept/Edit/Save/Cancel are the canonical `.sp-btn` atoms — link `sp-btn.css` alongside this file; ownership: `sp-btn`). Self-contained otherwise; `--sc` tint per instance.

## Use it

1. Copy `sp-magic-note.css` + `sp-magic-note.js` into your page or component folder.
2. Link `buttons/sp-btn/sp-btn.css` on the same page for the actions.
3. Paste the markup below; set the draft text in `.sp-mnote-text` and `--sc` inline.
4. Listen for the `sp-mnote` event (`event.detail.action` = "accept" | "save", `event.detail.text`) on `.sp-mnote`.

```html
<div class="sp-mnote" style="--sc:#7c3aed">
  <div class="sp-mnote-tag"><span class="sp-mnote-spark">✨</span> Drafted for you</div>
  <p class="sp-mnote-text">"Builders Collective — a room for people shipping intelligent things, with weekly build reviews and open demos."</p>
  <p class="sp-mnote-sub">Made from what you told us. Tweak it or take it as-is.</p>
  <textarea class="sp-mnote-edit" aria-label="Edit draft"></textarea>
  <div class="sp-mnote-actions">
    <button class="sp-btn sp-btn--create" data-mnote="accept" style="--sc:#7c3aed">Accept</button>
    <button class="sp-btn sp-btn--ghost" data-mnote="edit">Edit</button>
    <button class="sp-btn sp-btn--create" data-mnote="save" style="--sc:#7c3aed;display:none">Save</button>
    <button class="sp-btn sp-btn--ghost" data-mnote="cancel" style="display:none">Cancel</button>
  </div>
  <div class="sp-mnote-done"><span class="sp-mnote-spark">✨</span> Saved — looking good.</div>
</div>
```

## Selectors

```css
.sp-mnote
.sp-mnote::after
.sp-mnote-tag, .sp-mnote-spark
.sp-mnote-text, .sp-mnote-sub
.sp-mnote-actions
.sp-mnote-edit
.sp-mnote.is-editing, .sp-mnote.is-editing .sp-mnote-text, .sp-mnote.is-editing .sp-mnote-edit
.sp-mnote.is-done, .sp-mnote.is-done .sp-mnote-actions
.sp-mnote-done, .sp-mnote.is-done .sp-mnote-done
```
