# Smart Block: `room-chrome`

The room shell: head (kicker + title + lede) + toolbar + status line + body + outlet. Every Hub room composes this; `--room-accent` themes the kicker and LED.

- **Type:** chrome
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `room-chrome.css`
- **Specimen:** `specimen.html`
- **States found:** mobile/desktop breakpoints
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `room-chrome.css`.
3. Copy the HTML from `specimen.html`.
4. Set `--room-accent` on the outlet per room.

## Selectors in this block

```
.room-outlet
.room-head
.room-head .kicker
.room-head h2
.room-head p
.room-body
.room-scene
.room-toolbar
.room-toolbar.between
.room-status-line
.room-status-line .led
@media breakpoints
```
