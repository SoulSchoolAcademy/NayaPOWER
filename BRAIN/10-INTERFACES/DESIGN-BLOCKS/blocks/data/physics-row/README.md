# Smart Block: `physics-row`

Interaction physics, demonstrated — approach, hover, press, focus, reduced motion. The five promises, in a row.

- **Type:** data
- **Source:** `smart-blocks/specialty/specialty-interaction-physics-physics-row.html + smart-blocks/specialty/specialty.css (branch naya5/smart-blocks-library)`
- **Files:** `physics-row.css`, `specimen.html`
- **Dependencies:** `tokens.css`
- **States:** none — one honest face
**Honest scope:** `--soft-line` is referenced by the source CSS but never defined in the branch `tokens.css` (source bug, preserved byte-true). The specimen patches it inline, clearly marked.

## Use it

1. Copy `physics-row.css` next to your page.
2. Link `tokens.css` first, then `physics-row.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).

## Selectors

```
.physics-row
.physics-row:last-child
.physics-row b
```
