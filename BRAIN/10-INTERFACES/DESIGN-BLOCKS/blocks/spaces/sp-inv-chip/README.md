# Smart Block: `spaces/sp-inv-chip`

Invite chip ("tap to step into a room") plus invite-list rows with Invite buttons.

## Why

‘Tap to step into a room.’ The invite chip is the doorway made literal — and the invite-list rows with Invite buttons turn a guest list into an action list.

- **Type:** spaces
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** invite chip (default, hover), invite list row with Invite button (default, hover), invite list (scrollable, max-height 320px), `.sp-invite-btn` (default, hover); accent per chip via `--sc` (default `#7c3aed` from block.css)
- **Dependencies:** CSS var `--sc` (set on the chip; specimen sets it per chip). `.sp-invite-row` has no rule in this block's CSS (see Notes).

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spInvChip({name, accent, onJoin})` for a chip, `spInviteRow({name, avatar, onAdd})` for a row, and wrap rows in `spInviteList([rows])`.

## Selectors in this block

```
.sp-invite-btn
.sp-invite-list
.sp-invite-name
.sp-invite-add
.sp-inv-chip
.sp-inv-chip-name
.sp-inv-chip-join
```

## Notes

- `.sp-invite-btn` is the source's generic invite/action button class (used in the detail head row); it lives in this block's CSS, so `spaces/sp-detail` depends on this block for its button styling.
- The source invite row calls `avatar(p,'sm')` from the avatar sibling block — the builder takes a pre-rendered `avatar` Element param instead. The source's `.sp-invite-row` base-source rule (flex layout, dividers) was not in the extracted CSS; the specimen reproduces it as specimen-only styling so the demo renders source-faithfully.
- Source click behavior wrote to localStorage / called `toast()` / re-rendered the app; the builders take `onJoin` / `onAdd` callbacks instead.
- This block's CSS does not include the source's `sp-marquee`/`sp-marquee-track`/`sp-invited`/`sp-invited-title` welcome-strip wrappers — those are a layout concern outside the block's extracted selectors.
