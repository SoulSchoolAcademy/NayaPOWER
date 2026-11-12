# Smart Block: `nl-switch`

Toggle switch from Missing Blocks library.

## Why

Toggle switch. Binary choices should feel physical — a knob that moves is a promise kept. Settings feel certain: on means on.

- **Type:** toggles
- **Source:** `Naya_Lego-blocks.html` (extracted byte-true, never rewritten)
- **CSS:** `nl-switch.css`
- **Specimen:** `specimen.html`
- **States found:** :focus, :focus-visible, :disabled
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `nl-switch.css`.
3. Copy the HTML from `specimen.html`.


## Selectors in this block

```
.nl-switch
.nl-switch input
.nl-switch input:checked ~ .nl-knob
.nl-switch input:checked ~ .nl-track
.nl-switch input:disabled
.nl-switch input:disabled ~ .nl-track
.nl-switch input:focus-visible ~ .nl-track
```
