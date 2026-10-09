# Smart Block: `intel-row`

The compact intel row: type tag + title + summary. `--room-accent` themes the type tag and hover border.

## Why

Not every signal deserves a card. The compact row — type tag, title, summary — is the feed’s shorthand: dense enough to scan a hundred of, honest enough to trust each one.

- **Type:** feed
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `intel-row.css`
- **Specimen:** `specimen.html`
- **States found:** :hover (accent border)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `intel-row.css`.
3. Copy the HTML from `specimen.html`.
4. Set `--room-accent` on the list for the type-tag color.

## Selectors in this block

```
.intelligence-list
.intel-row
.intel-row:hover
.intel-type
.intel-title
.intel-summary
```
