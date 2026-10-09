# Smart Block: `naya-table`

Live data table: sortable columns with aria-sort, type-aware compare, hover rows. Distinct from the wave's data-table specimen — this one sorts.

- **Type:** data
- **Source:** `naya5/smart-blocks-library @ 1dc1241e (branch) — ported 2026-10-09`
- **CSS:** `naya-table.css`
- **Specimen:** `specimen.html`
- **JS:** `naya-table.js`
- **Dependencies:** tokens.css, naya-table.js
- **States:** th.sorted, [aria-sort="ascending/descending]

## Use it

1. Include the shared `tokens.css` (once per page).
2. Include `naya-table.css`.
3. Include `naya-table.js` for interactive behavior.
4. Copy the HTML from `specimen.html`.
5. Include `naya-table.js` — without it the table is static.

## Selectors in this block

```
table.naya-table
.naya-table[data-sortable] thead th[data-sort]
```

Not the wave's `data-table` (static specimen): this is the live sortable table.
