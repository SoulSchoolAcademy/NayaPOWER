# Smart Block: `n2-rpt-header`

Report front door. Logo, breathing serif title lockup, tagline, and the living orb mark — the page's handshake.

- **Type:** layout
- **Source:** `Naya Design Elements N2.html` (extracted byte-true, never rewritten)
- **CSS:** `n2-rpt-header.css`
- **Specimen:** `specimen.html`
- **States found:** @media (max-width:640px)
- **Dependencies:** tokens.css

## Note

Specimen swaps the source's NayaNET logo data URI for `nayanet-logo.png` — supply the real logo file.

## Use it

1. Include `tokens.css` (once per page).
2. Include `n2-rpt-header.css`.
3. Copy the HTML from `specimen.html`.
4. No JavaScript needed.

## Selectors in this block

```
.rpt-header
.rpt-logo
.rpt-titleblock
.rpt-h1
.rpt-h1 em
.rpt-tag
.orb-mark
.orb-mark::before
.orb-mark::after
```
