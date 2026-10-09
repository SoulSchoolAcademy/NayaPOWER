# Smart Block: `skeleton`

Skeleton loading screens. Shimmer sweeps across obsidian placeholders in feed, grid, and hero compositions.

- **Type:** data
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `skeleton.css`
- **Specimen:** `specimen.html`
- **States found:** .sk--line, .sk--title, .sk--para, .sk--card, .sk--ava, .sk--btn, .sk--img, .sk-feed, .sk-row, .sk-grid
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `skeleton.css`.
3. Compose placeholders with `.sk` + a shape class; wrap in `.sk-feed` / `.sk-grid` / `.sk-stack`.

## Selectors in this block

```
.sk
.sk--ava
.sk--btn
.sk--card
.sk--img
.sk--line
.sk--para
.sk--title
.sk-feed
.sk-grid
.sk-row
.sk-stack
```

## Notes

- Shimmer is a diagonal sweep; disabled under `prefers-reduced-motion`.
- Mark skeletons `aria-hidden="true"` and announce loading via `aria-busy` on the container.
- Widths are inline styles — match them to the content being replaced.
- No JavaScript required — pure CSS block.
