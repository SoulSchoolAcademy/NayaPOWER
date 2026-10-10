# Smart Block: `report/law-steps`

Vertical law-pipeline steps: jewel marker + bold rule + explanation. Governance as a readable staircase.

## Why

Governance is a staircase, not a wall of text. Jewel marker, bold rule, explanation per step — the pipeline of a law made readable at a glance.

- **Type:** report
- **Source:** `Naya Design Elements N2.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** none
- **Dependencies:** `.jewel.mini` from the jewels category (or any 1em marker)

## Use it

1. Include `block.css` (and jewels block CSS for `.jewel.mini`, or substitute your own marker).
2. Copy the HTML from `specimen.html`.
3. One `.law-step` per pipeline stage.

## Selectors in this block

```
.law-steps
.law-step
.law-step > div
.law-step strong
.law-step span

```
