# Smart Block: `assessment/dimension-constellation`

9-dimension orb grid (5-col): ring gauge + score + name + status per dimension. The mastery signature.

## Why

Nine dimensions is too many to hold in your head. The orb grid compresses the whole mastery signature into one glance — ring, score, name, status — the shape of how you think.

- **Type:** assessment
- **Source:** `Maxis App Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** none (ring fill via --dimDeg)
- **Dependencies:** `--dimensionColor` per orb; `--dimDeg` per ring (score × 3.6deg)

> **Provenance note:** Maxis was Shawn's earlier MAXESS assessment project — not NayaNET. Only the UI grammar was extracted; no MAXIS branding or content is carried in this block.

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. Per orb set `--dimensionColor`; per ring set `--dimDeg` to score × 3.6deg.

## Selectors in this block

```
.dimension-constellation
.dimension-orb
.dimension-ring
.dimension-ring::after
.dimension-score
.dimension-name
.dimension-status

```
