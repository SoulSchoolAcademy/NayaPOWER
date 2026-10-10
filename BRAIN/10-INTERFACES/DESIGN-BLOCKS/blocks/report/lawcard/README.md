# Smart Block: `report/lawcard`

Law card: numbered law with diamond marker, title, and body. Governance made visible, one card per law.

## Why

One law, one card. The diamond marker and numbered title make each law citable and distinct — governance you can point at.

- **Type:** report
- **Source:** `Naya Design Element Set N4.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** :hover
- **Dependencies:** `--lc` per card (inline accent); `--ease` motion curve

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. Set `--lc` accent per card; `.ln` holds the law number, `h3` the title.

## Selectors in this block

```
.lawcard
.lawcard .ln
.lawcard .ld
.lawcard h3
.lawcard p

```
