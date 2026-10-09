# Smart Block: `naya-shell`

The page chassis — rail, head, main, foot. Every page starts here; content fills the rooms.

- **Type:** layout
- **Source:** `smart-blocks/new/new-page-shell-naya-shell.html + smart-blocks/new/new.css (branch naya5/smart-blocks-library)`
- **Files:** `naya-shell.css`, `specimen.html`
- **Dependencies:** `tokens.css`
- **States:** `.is-demo (specimen mode: static, bordered)`
**Honest scope:** the source provides the chassis grid (`.naya-shell*`) only. Rail/head/main/foot inner elements in the specimen are demo content (specimen-only styles, clearly marked); the demo composes canonical `orb` + `metric` blocks.

## Use it

1. Copy `naya-shell.css` next to your page.
2. Link `tokens.css` first, then `naya-shell.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).

## Selectors

```
.naya-shell
.naya-shell.is-demo
.naya-shell.is-demo .naya-shell-rail
.naya-shell.is-demo .naya-shell-head
.naya-shell.is-demo .naya-shell-main
```
