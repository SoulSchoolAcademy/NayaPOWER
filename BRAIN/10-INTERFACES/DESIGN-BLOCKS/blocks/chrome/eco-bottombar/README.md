# Smart Block: `eco-bottombar`

The mobile bottom bar shared across Hub, Ledger, and Spaces: 46px round buttons on a radial dark bar, jewel plus-button, pop-up destination menu. `--jewel` themes the plus.

- **Type:** chrome
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `eco-bottombar.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, [aria-expanded], .open, mobile breakpoint
- **Dependencies:** eco-bottombar.js (menu toggle), tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `eco-bottombar.css`.
3. Copy the HTML from `specimen.html`.
4. Include `eco-bottombar.js` for the plus-menu toggle.
5. `--jewel` (default #ffea00) and `--eco` (default #9d75ff) are optional per-instance accents.

## Selectors in this block

```
.eco-bottombar
.eco-bb-btn
.eco-bb-btn:hover
.eco-ico
.eco-plus
.eco-plus[aria-expanded="true"]
.eco-menu
.eco-menu.open
.eco-menu a
@media (max-width: 900px)
```
