# Smart Block: `naya-badge`

Truth-state badge: uppercase pill with a status dot. Verified / claim / demo / danger are the only colored states — quiet by default.

- **Type:** jewels
- **Source:** `naya5/smart-blocks-library @ 1dc1241e (branch) — ported 2026-10-09`
- **CSS:** `naya-badge.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css
- **States:** .is-verified, .is-claim, .is-demo, .is-danger

## Use it

1. Include the shared `tokens.css` (once per page).
2. Include `naya-badge.css`.
3. Copy the HTML from `specimen.html`.
4. Never invent a new colored state — verified / claim / demo / danger are the closed set.

## Selectors in this block

```
.naya-badge
.naya-badge.is-verified
.naya-badge.is-claim
.naya-badge.is-demo
.naya-badge.is-danger
```
