# Smart Block: `dimension-orb`

Score-dimension display for the assessment report — a ring gauge orb with the numeric score, the dimension name, and the level status, arranged in the `.dimension-constellation` grid.

- **Type:** assessment
- **Source:** `Maxis App Design.html`
- **Files:** `dimension-orb.css`, `specimen.html`
- **Dependencies:** tokens.css (`--dimensionColor` and `--dimDeg` are set inline per orb)
- **States:** `@media print`, `@media(max-width:760px)`, `@media(max-width:420px)` (constellation collapses to 2 columns; last orb spans)
- **Notes:**
  - The orbs are JS-rendered in the source (`renderDimensions`); the specimen converts them to static HTML. `--dimDeg` = score × 3.6deg; `--dimensionColor` comes from the source's dimension config (Direction `#ffd45a`, Communication `#35e39b`, Evaluation `#3ca8ff`, Iteration `#765cff`, Systems Thinking `#ed42c4`).
  - Level bands in the source: Master ≥ 90 · Advancing ≥ 75 · Developing ≥ 60 · Foundation < 60.
  - Possible overlap: the indexed `orbit-dial` (graphs) is also a score ring — this one is genuinely page-specific (assessment dimension card with name + status), extracted; note the kinship.

## Use it

1. Copy `dimension-orb.css` next to your page.
2. Link `tokens.css` first, then `dimension-orb.css`.
3. Paste the markup; set `--dimensionColor` and `--dimDeg` (score × 3.6deg) per orb:

```html
<div class="dimension-constellation" id="dimensionConstellation">
  <div class="dimension-orb" style="--dimensionColor:#ffd45a">
    <div class="dimension-ring" style="--dimDeg:295.2deg">
      <span class="dimension-score">82</span>
    </div>
    <div class="dimension-name">Direction</div>
    <div class="dimension-status">Advancing</div>
  </div>
</div>
```

## Selectors

```
.dimension-constellation
.dimension-orb
.dimension-ring
.dimension-ring::after
.dimension-score
.dimension-name
.dimension-status
```
