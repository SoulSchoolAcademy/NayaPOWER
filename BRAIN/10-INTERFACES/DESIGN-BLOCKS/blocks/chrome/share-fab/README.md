# Smart Block: `share-fab`

The 56px jewel FAB — fixed bottom-right, `--jewel` (default #ffea00), 18px radius. Mobile-only in the Hub (hidden on desktop).

- **Type:** chrome
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `share-fab.css`
- **Specimen:** `specimen.html`
- **States found:** :active (scale .94), mobile breakpoint
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `share-fab.css`.
3. Copy the HTML from `specimen.html`.
4. Set `--jewel` to re-theme the jewel.

## Selectors in this block

```
.share-fab
.share-fab:active
@media (max-width: 768px)
```
