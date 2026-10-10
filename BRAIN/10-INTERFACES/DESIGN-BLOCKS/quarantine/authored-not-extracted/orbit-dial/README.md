# Smart Block: `orbit-dial`

The score, set in orbit. A jewel ring gauge for 0–10 scores — the visual voice
of the Calculator. The arc sweeps in on light with orbit-btn DNA (colored
trail, white-hot head, rest gap); the number sits at the center in white
tabular numerals.

## Why

A score needs a face. The jewel ring gauge from 0–10 gives the Calculator’s output a physical presence — you see where you stand before you read the number.

- **Type:** graphs
- **Source:** authored 2026-10-09 from orbit-btn conic-ring DNA
- **CSS:** `orbit-dial.css`
- **Specimen:** `specimen.html`
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` and `orbit-dial.css`.
2. `.od-dial` holds `.od-arc` (set `--vt`: 0..1 target), `.od-ticks`, `.od-center`.
3. `.od-num` = the score text; `.od-cap` = the unit.
4. Add `.lit` to `.sg-card` on entry — the arc sweeps from 0.
5. The `@property --v` registration is required for the sweep (included in the CSS).

## Pairs with

- `living-counter` — same score story, different voice
- `pulse-orb` — the value behind the score
- The Calculator — this is its face
  (`BRAIN/01-GOVERNANCE/0006-NAYA-CALCULATOR-V1.human.md` — the scoring machine;
  orbit-dial is its display voice)
