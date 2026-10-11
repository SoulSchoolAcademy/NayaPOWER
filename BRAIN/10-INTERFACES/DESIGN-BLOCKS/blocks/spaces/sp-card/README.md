# Smart Block: `spaces/sp-card`

Space card with cover art — the grid unit of the Spaces discovery view.

## Why

Discovery is browsing, and browsing needs a unit. The space card with cover art is the grid’s atom — each space gets its face, and the grid gets its rhythm.

- **Type:** spaces
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** card (default, hover), joined / not-joined (`sp-join.in`), private badge, accent per card via `--sc` (default `#7c3aed` from block.css)
- **Dependencies:** CSS var `--sc` (set on the card; specimen sets it per card). `.sp-mstack`, `.sp-mcount`, `.sp-priv`, `.sp-join` are emitted by the builder but styled by sibling blocks, not this block's CSS (see Notes).

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spCard({name, topic, desc, members, accent})` and append the returned element; wrap several in `spGrid([...])`.

## Selectors in this block

```
.sp-grid
.sp-card
.sp-card-name
.sp-card-topic
.sp-card-body
.sp-card-desc
.sp-card-meta
.sp-card-cover
```

## Notes

- Source emits the cover as `sp-cover` (a base-source rule not included in this block's extracted CSS); the V2 upgrade section of `block.css` styles the cover as `.sp-card-cover`. The builder emits **both** classes (`sp-card-cover sp-cover`) so the block's own CSS styles the cover while the source class string is preserved.
- `block.css` also carries two bare rules from the source file — `.sp-grid{ grid-template-columns:1fr; }` and `.sp-card, .sp-member, .sp-modal, .sp-save-contact{ transition:none; animation:none; }` — copied verbatim as-is; in the specimen the first collapses the grid to one column on narrow widths (source media-query context not included in the extraction).
- Member avatar stack, member count, private badge, and join button rely on sibling-block styling (`avatar` builder, `.sp-mstack/.sp-mcount/.sp-priv/.sp-join`); the specimen includes specimen-only `.sp-join` styling so the demo renders.
- `spCard` takes `avatars` (pre-rendered avatar Elements) rather than calling the source's `avatar()` / `spaceMembers()` app-state helpers.
