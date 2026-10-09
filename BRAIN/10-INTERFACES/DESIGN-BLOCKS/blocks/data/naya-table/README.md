# Smart Block: `naya-table`

Data you can interrogate — click any header to sort. Statuses ride along as badges.

- **Type:** data
- **Source:** `smart-blocks/new/new-live-data-table-table-naya-table-data-sortable.html + smart-blocks/base.css + smart-blocks/naya-blocks.js (branch naya5/smart-blocks-library)`
- **Files:** `naya-table.css`, `specimen.html`, `naya-table.js`
- **Dependencies:** `tokens.css`
- **States:** `[data-sortable]`, `th.sorted`, `[aria-sort]`

## Use it

1. Copy `naya-table.css` (and `naya-table.js`) next to your page.
2. Link `tokens.css` first, then `naya-table.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`naya-table.js`) — it is byte-true and self-initializing.

## Selectors

```
.naya-table-wrap
table.naya-table
.naya-table thead th
.naya-table[data-sortable] thead th[data-sort]
.naya-table[data-sortable] thead th[data-sort]:hover
.naya-table[data-sortable] thead th[data-sort]::after
.naya-table[data-sortable] thead th.sorted
.naya-table[data-sortable] thead th.sorted[aria-sort="ascending"]::after
.naya-table[data-sortable] thead th.sorted[aria-sort="descending"]::after
.naya-table tbody td
.naya-table tbody tr:last-child td
.naya-table tbody tr
.naya-table tbody tr:hover
```
