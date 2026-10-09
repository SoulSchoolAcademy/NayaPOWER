# Smart Block: `naya-drawer`

The side drawer that slides in from the right — notifications live here, one tap away, dismissed with the backdrop.

- **Type:** overlays
- **Source:** `smart-blocks/new/new-notification-drawer-naya-drawer.html + smart-blocks/new/new.css + smart-blocks/base.css (branch naya5/smart-blocks-library)`
- **Files:** `naya-drawer.css`, `specimen.html`
- **Dependencies:** `tokens.css`
- **States:** `[hidden]`
**Honest scope:** the source fragment provides the trigger button only. The drawer panel in the specimen is composed demo content (specimen-only styles + inline open/close wiring, clearly marked); the panel chrome and backdrop are the block. `icons.svg` is not ported (needs Shawn’s eye), so the specimen uses a text trigger.

## Use it

1. Copy `naya-drawer.css` next to your page.
2. Link `tokens.css` first, then `naya-drawer.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. No canonical JS in the source — the specimen wires open/close inline (specimen-only, clearly marked).

## Selectors

```
.naya-drawer
.naya-drawer[hidden]
.naya-drawer-backdrop
.naya-drawer-backdrop[hidden]
```
