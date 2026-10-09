# Smart Block: `lists/sp-about-rows`

Key/value about rows — the About-tab card from the space detail view.

## Why

About is facts, and facts want a clean ledger. Key/value rows give the space’s identity a scannable shape — no prose to wade through, just the record.

- **Type:** lists
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** about card with rows; optional description paragraph; no accent styling needed (block uses neutral colors)
- **Dependencies:** none (no CSS vars).

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spAboutRows([[key, value], ...], desc)` and append the returned element. The optional `desc` string renders as `.sp-about-desc` below the rows.

## Selectors in this block

```
.sp-about
.sp-about-row
.sp-about-k
.sp-about-v
.sp-about-desc
```

## Notes

- Source derives row values from app state (`spaceMembers()`, `spacePosts()`, date formatting, privacy emoji). The builder takes already-resolved `[key, value]` string pairs instead — callers compute the values.
- The source's about tab also appends a "Connect" door CTA button (`sp-btn primary`) for door spaces; that button is a separate component's concern and was not extracted here.
