# Smart Block: `naya-badge`

A truth label you can read from across the room — verified green, claim gold, demo magenta, danger red.

- **Type:** chrome
- **Source:** `smart-blocks/new/new-badges-naya-badge.html + smart-blocks/new/new.css (branch naya5/smart-blocks-library)`
- **Files:** `naya-badge.css`, `specimen.html`
- **Dependencies:** `tokens.css`
- **States:** `.is-verified`, `.is-claim`, `.is-demo`, `.is-danger`

## Use it

1. Copy `naya-badge.css` next to your page.
2. Link `tokens.css` first, then `naya-badge.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).

## Selectors

```
.naya-badge
.naya-badge::before
.naya-badge.is-verified
.naya-badge.is-verified::before
.naya-badge.is-claim
.naya-badge.is-claim::before
.naya-badge.is-demo
.naya-badge.is-demo::before
.naya-badge.is-danger
.naya-badge.is-danger::before
```
