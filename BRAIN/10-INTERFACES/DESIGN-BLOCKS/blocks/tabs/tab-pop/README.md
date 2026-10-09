# Smart Block: `tab-pop`

The tab popover — the Add/Edit-Tab modal dialog (label + topic inputs, heart/star toggles, cancel/save), positioned near its anchor. NOT a tab strip itself.

- **Type:** tabs
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `tab-pop.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `:hover` on `.tab-pop-add` / `.tab-pop-del` / `.btn`, `.on` on `.tgl`, `.primary` on `.btn`, `:active` on `.btn`, responsive `@media`, `prefers-reduced-motion`
- **Notes:**
  - JS-rendered in the source (`openTabEditor`); the specimen converts it to static HTML and shows it open. The heart/star glyphs are the source's `\uD83D\uDC9C` / `\u2B50` escapes rendered.
  - The `.tab-pop-*` list classes (`.tab-pop-title`, `.tab-pop-list`, `.tab-pop-note`, `.tab-pop-row`, `.tab-pop-name`, `.tab-pop-add`, `.tab-pop-del`) describe a tab-manager LIST variant that has NO rendered instance in the source — CSS-only legacy. The specimen reconstructs that variant from CSS and marks it as such.
  - Compared against the indexed `seg-tab` (a segmented tab chip with `.on` state): genuinely different — seg-tab IS the tab; tab-pop is the dialog that creates/edits tabs. Extracted.
  - The shared `.btn` rules and interaction resets are bundled verbatim (byte-identical to the source).

## Use it

1. Copy `tab-pop.css` next to your page.
2. Link `tokens.css` first, then `tab-pop.css`.
3. Paste the dialog; position it near the anchor (the source uses `placeNear`) or centered; toggle `display`:

```html
<div class="tab-pop" role="dialog" aria-modal="true" style="display:block;left:50%;top:120px;transform:translateX(-50%)">
  <h3>Add Tab</h3>
  <div class="row"><label>Label <input value="" placeholder="e.g., Design"></label></div>
  <div class="row"><label>Topic <input value="" placeholder="Topic to filter"></label></div>
  <div class="toggles">
    <div class="tgl on">💜 Purple Heart</div>
    <div class="tgl">⭐ Gold Star</div>
  </div>
  <div class="ft">
    <button class="btn" type="button">Cancel</button>
    <button class="btn primary" type="button">Save</button>
  </div>
</div>
```

## Selectors

```
.tab-menu, .tab-pop
.tab-pop (+ h3 / .row / label / input / .toggles / .tgl / .tgl.on / .ft / .btn / .btn.primary)
.tab-pop-title (+ :first-child)
.tab-pop-list
.tab-pop-note
.tab-pop-add (+ :hover)
.tab-pop-row (+ select)
.tab-pop-name
.tab-pop-del (+ :hover)
.btn (+ :hover / :active / svg / [disabled])
.action-row .mini
```
