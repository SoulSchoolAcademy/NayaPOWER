# Smart Block: `naya-avatar-stack`

Overlapping avatar stack: the companion container for naya-avatar. Negative-margin overlap, page-colored ring.

- **Type:** chrome
- **Source:** `naya5/smart-blocks-library @ 1dc1241e (branch) — ported 2026-10-09`
- **CSS:** `naya-avatar-stack.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css, naya-avatar

## Use it

1. Include the shared `tokens.css` (once per page).
2. Include `naya-avatar-stack.css`.
3. Copy the HTML from `specimen.html`.
4. Include the `naya-avatar` block first — the stack is its companion container.

## Selectors in this block

```
.naya-avatar-stack
.naya-avatar-stack .naya-avatar
```

Companion to `naya-avatar`: the stack holds avatars, it is not an avatar itself.
