# Smart Block: `door`

The Smart Door card — "one brain, many doors." 17px radius, per-door `--door-accent` theming, accent radial glow top-right, 48px icon. The connection mechanic's card.

## Why

‘One brain, many doors.’ The Smart Door card is the connection mechanic made tangible — per-door accent theming means each door feels like its own place while staying one system.

- **Type:** chrome
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `door.css`
- **Specimen:** `specimen.html`
- **States found:** :hover (lift + glow)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `door.css`.
3. Copy the HTML from `specimen.html`.
4. Set `--door-accent` per door (inline style or parent). Defaults to emerald.

## Selectors in this block

```
.door
.door:hover
.door-top
.door-icon
.door-name
.door-for
.door-desc
.door-foot
```
