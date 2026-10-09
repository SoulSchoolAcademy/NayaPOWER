# Smart Block: `naya-shell`

Page shell: rail + head + main grid chassis. The chassis every page starts from — brand, nav, title, content.

- **Type:** layout
- **Source:** `naya5/smart-blocks-library @ 1dc1241e (branch) — ported 2026-10-09`
- **CSS:** `naya-shell.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css
- **States:** .is-demo, .is-here

## Use it

1. Include the shared `tokens.css` (once per page).
2. Include `naya-shell.css`.
3. Copy the HTML from `specimen.html`.
4. Drop the `is-demo` class for the full-viewport chassis; keep it for embedded previews.

## Selectors in this block

```
.naya-shell
.naya-shell-rail
.naya-shell-head
.naya-shell-main
.naya-shell-link.is-here
```

Demo content in the specimen is placeholder — drop wave `metric` / `orb` blocks into `.naya-shell-main`.
