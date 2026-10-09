# Smart Block: `data/li-day`

Day divider line for the ledger stream — centered, tracked-out label between day groups.

- **Type:** data
- **Source:** `Ledger Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** static label (no hover/animation states in source)
- **Dependencies:** `.li-stage` wrapper (base rule prepended into `block.css`; block is self-contained)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `liDay(label)` and append the returned element. Wrap page content in `.li-stage`.

## Selectors in this block

```
.li-stage
.li-day
```

## Notes

- The source applies no `<style>` rule to `.li-day`; styling was inline `cssText` on the divider element (~line 1003). Values were captured verbatim as the `.li-day` rule in `block.css` (per the staging CSS header); the builder relies on the rule and does not duplicate inline styles.
- The source computed the label from the day key (`TODAY` / `YESTERDAY` / `toLocaleDateString(...).toUpperCase()`); the builder takes the final label string directly.
