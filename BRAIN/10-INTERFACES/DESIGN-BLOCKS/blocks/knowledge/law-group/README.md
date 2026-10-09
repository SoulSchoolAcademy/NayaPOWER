# Smart Block: `law-group`

A law library that opens — collapsible groups of the rules that govern, numbered and quotable.

- **Type:** knowledge
- **Source:** `smart-blocks/data/data-law-library-law-group.html + smart-blocks/data/data.css (branch naya5/smart-blocks-library)`
- **Files:** `law-group.css`, `specimen.html`
- **Dependencies:** `tokens.css`
- **States:** `[open]`

## Use it

1. Copy `law-group.css` next to your page.
2. Link `tokens.css` first, then `law-group.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).

## Selectors

```
.law-group
.law-group summary
.law-group summary::-webkit-details-marker
.law-group summary:after
.law-group[open] summary:after
.law-group ol
.law-group li
.law-group li::marker
```
