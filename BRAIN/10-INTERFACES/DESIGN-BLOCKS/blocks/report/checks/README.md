# Smart Block: `report/checks`

Vertical checklist: real checkboxes with accent-tinted rows. Verification you can tick.

## Why

Verification you can tick. Real checkboxes with accent-tinted rows turn a list of claims into something the user can physically confirm — trust, one tick at a time.

- **Type:** report
- **Source:** `Naya Design Elements N2.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** :checked, :hover, :focus-visible
- **Dependencies:** `--cc` per check (inline accent)

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. One `label.check` per item with a real `<input type="checkbox">`.

## Selectors in this block

```
.checks
.check
.check input
.check span

```
