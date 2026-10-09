# Smart Block: `assessment/score-stage`

260px circular score stage: glowing ring gauge with big number + out-of label. The results hero number.

- **Type:** assessment
- **Source:** `Maxis App Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** none (ring via --scoreDeg)
- **Dependencies:** `--scoreColor`, `--scoreDeg` (score × 3.6deg) on `.score-stage`

> **Provenance note:** Maxis was Shawn's earlier MAXESS assessment project — not NayaNET. Only the UI grammar was extracted; no MAXIS branding or content is carried in this block.

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. Set `--scoreColor` and `--scoreDeg` per result.

## Selectors in this block

```
.score-stage
.score-content
.score-number
.score-outof

```
