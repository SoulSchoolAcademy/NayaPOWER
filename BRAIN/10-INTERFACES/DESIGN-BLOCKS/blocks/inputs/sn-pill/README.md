# Smart Block: `inputs/sn-pill`

Smart Note filter pill: glow pill with label, optional 💜/⭐ mark, ⋯ options button, plus a popover editor (label input + purple-heart/gold-star toggles + Cancel/Save) and a shared context menu (Edit / Set Purple Heart / Set Gold Star / Remove).

- **Type:** inputs
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.sn-menu .mi:hover`, `.sn-pill.heart`, `.sn-pill.star`, `.sn-pill:hover`, `.cx-stage .sn-pill:focus-visible`, `.sn-pill.on`, `.sn-pill.add`, `.sn-pill.add:hover`, `.sn-more:hover`, `.sn-more.sn-x:hover`, `.sn-pop .tgl.on`
- **Dependencies:** `--tc` (per-pill accent, set inline by the builder), `--cx-dim` (dim text color — defined *outside* this block; used by `.sn-pill.add` and `.sn-pop label`; the specimen defines `--cx-dim:#8a8a96` on `:root`)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `snPill(opts)` / `snPillAdd(opts)` and append the returned element.

## Selectors in this block

```
.sn-menu .mi
.sn-menu .mi:last-child
.sn-menu .mi:hover
.sn-pop h3
.sn-pop .row
.sn-pop label
.sn-pop input
.sn-pop .toggles
.sn-pop .tgl
.sn-pop .tgl.on
.sn-pop .ft
.sn-btn
.sn-btn.primary
.sn-pill
.sn-pill .sn-label
.sn-pill.heart
.sn-pill.star
.sn-mark
.sn-pill:hover
.cx-stage .sn-pill:focus-visible
.sn-pill.on
.sn-pill.add
.sn-pill.add:hover
.sn-more
.sn-more:hover
.sn-more.sn-x:hover
.sn-menu
.sn-pop
.sn-btn.sn-restore
```

## Notes

- Builders: `snPill(opts)`, `snPillAdd(opts)`, plus `snClosePanels()`.
  - `snPill({id, label, color, heart, star, active, more, onSelect(tab, pill), onMark(tab, mark, pill), onChange(tab, pill), onRemove(tab, pill)})` — pill click toggles the popover? No: pill click calls `onSelect`; the **⋯ button (or right-click)** opens the context menu, and **Edit** (or the ＋ Add pill) opens the popover editor with heart/star toggles.
  - Live tab data is available at `pill._snTab`.
- The menu and popover are shared singletons appended to `document.body` (faithful to the source); only one is ever visible.
- The source's outside-click close checked `.sn-row`; that class is defined outside this block, so the standalone check uses `.sn-pill` (the block's clickable unit). Escape also closes.
- Source's Remove only deleted custom tabs (system tabs got a toast); standalone calls `opts.onRemove(tab, pill)` then removes the element from the DOM — return `false` from `onRemove` to keep it.
- New pills get their id from the consumer (source used `uid('st')`); see the `// Demo:` comment in block.js.
- The staging CSS repeats the `.sn-menu`/`.sn-pop` rule groups twice (two generations in the source); the selector list above is deduplicated. No values were edited.
