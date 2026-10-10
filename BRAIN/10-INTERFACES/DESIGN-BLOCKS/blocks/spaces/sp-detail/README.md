# Smart Block: `spaces/sp-detail`

Space detail view shell — cover, head row, title/topic/desc, action row, content container.

- **Type:** spaces
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** detail shell; topic line `topic · 🔒 Private` / `topic · Public`; joined / not-joined join button; accent per space via `--sc` (default `#7c3aed` from block.css)
- **Dependencies:** CSS var `--sc` (set on the shell; specimen sets it per space). `.sp-back`, `.sp-join`, `.sp-invite-btn` are emitted by the builder but styled by sibling blocks, not this block's CSS (see Notes).

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spDetail({name, topic, desc, members, accent, privacy, joined, onJoin, onInvite})` and append the returned element. Fill `wrap.content` (the `.sp-dcontent` element) with tab content — tab chrome comes from the `tabs/sp-dtabs` sibling block.

## Selectors in this block

```
.sp-detail
.sp-dhead
.sp-dcover
.sp-dtitle
.sp-dtopic
.sp-ddesc
.sp-dhrow
.sp-dcount
.sp-dcontent
```

## Notes

- Only the DETAIL SHELL is extracted. The source `renderDetail` also renders the tab bar (`sp-dtabs`/`sp-dtab`) and four tab bodies (posts, members, chat, about) — that tab chrome belongs to the `tabs/sp-dtabs` sibling block and the tab bodies to their own blocks; they were intentionally not dragged in.
- Source calls app-state helpers (`spaceById`, `spaceMembers`, `openInviteModal`, `broadcastToSpace`, `toast`, `saveJSON`); the builder takes plain params (`members` count, `onJoin`/`onInvite`/`onMessage`/`onMail` callbacks) instead.
- `.sp-back`, `.sp-join`, and `.sp-invite-btn` have no rules in this block's CSS — `.sp-invite-btn` lives in the `spaces/sp-inv-chip` block's CSS; `.sp-back`/`.sp-join` are styled by sibling blocks. The specimen includes specimen-only styling for these so the demo renders.
