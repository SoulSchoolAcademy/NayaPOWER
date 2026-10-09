# Smart Block: `report-section`

The assessment report composition — report section header (kicker + heading), the result hero (eyebrow, title, subtitle, score dial, level badge), insight articles (strongest capability / biggest opportunity), and the result action buttons.

- **Type:** type
- **Source:** `Maxis App Design.html`
- **Files:** `report-section.css`, `specimen.html`
- **Dependencies:** tokens.css (`--scoreColor`/`--scoreDeg` on the score dial and `--insightColor` per insight are set inline)
- **States:** `:hover` on `.result-actions button`, `@media print`, `@media(max-width:760px)`, `prefers-reduced-motion`
- **Notes:**
  - Markup is verbatim from the source body. The score dial (`.score-stage` family) is included because it is the result hero's defining element — without it the hero is a head without a face.
  - `.insight-flow` (the insight article container) and `.analysis-cloud` (the JS-filled analysis container) are included as part of the report composition.
  - Possible overlap: the indexed `hero`/`headline` type blocks — this is the assessment-report-specific composition (result hero + insight articles), genuinely different in purpose and styling; extracted.

## Use it

1. Copy `report-section.css` next to your page.
2. Link `tokens.css` first, then `report-section.css`.
3. Paste the markup; set `--scoreColor`/`--scoreDeg` (score × 3.6deg) and `--insightColor` inline:

```html
<div class="result-hero">
  <div class="result-eyebrow">YOUR PERSONAL AI MASTERY REPORT</div>
  <h2 class="result-title" id="resultTitle">Your AI Score</h2>
  <p class="result-subtitle" id="resultSubtitle">{{subtitle}}</p>
  <div class="score-stage" id="scoreStage" style="--scoreColor:#b895ff;--scoreDeg:273.6deg;">
    <div class="score-content">
      <span class="score-number" id="overallScore">76</span>
      <span class="score-outof">OUT OF 100</span>
    </div>
  </div>
  <div class="result-level" id="resultLevel" style="--scoreColor:#b895ff">
    <span class="result-level-dot"></span>
    <span id="resultLevelText">Advancing</span>
  </div>
</div>

<section class="report-section">
  <div class="report-heading">
    <div class="report-kicker">YOUR LEVERAGE POINTS</div>
    <h3>Where your score tells the story</h3>
  </div>
  <div class="insight-flow">
    <article class="insight" style="--insightColor:#35e39b">
      <div class="insight-cap">Your strongest capability</div>
      <div class="insight-score" id="strongestScore">88</div>
      <h4 id="strongestName">Direction</h4>
      <p id="strongestText">{{analysis…}}</p>
    </article>
  </div>
</section>

<div class="result-actions">
  <button type="button" id="pdfButton">Download / Save My Report</button>
  <button type="button" class="quiet" id="restartButton">Take Assessment Again</button>
</div>
```

## Selectors

```
.result-hero
.result-eyebrow
.result-title
.result-subtitle
.score-stage
.score-stage::before
.score-stage::after
.score-content
.score-number
.score-outof
.result-level
.result-level-dot
.report-section
.report-heading
.report-kicker
.report-heading h3
.report-heading p
.insight-flow
.insight
.insight::after
.insight-cap
.insight h4
.insight p
.insight-score
.analysis-cloud
.analysis-cloud p
.analysis-cloud p + p
.result-actions
.result-actions button
.result-actions button:hover
.result-actions .quiet
```
