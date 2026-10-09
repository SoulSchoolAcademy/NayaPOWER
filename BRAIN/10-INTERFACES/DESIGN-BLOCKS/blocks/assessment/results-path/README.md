# Smart Block: `results-path`

The assessment results journey — score reveal → dimension breakdown → path forward, as a stepped progression. Phases arrive in stages (IntersectionObserver + score count-up) so the report moment feels like an arrival, not a printout. Builds on the `dimension-orb` language for phase 2.

- **Type:** assessment
- **Source:** authored 2026-10-09 for Maxis assessment completion (`.score-stage` family and `.path*` rules verbatim from `Maxis App Design.html`; journey wrapper, phase heads, arrival wash, and dividers are new)
- **Files:** `results-path.css`, `results-path.js`, `specimen.html`
- **Dependencies:** tokens.css (`--ease`; specimen ships a minimal shim); `assessment/dimension-orb` for the phase-2 constellation (specimen links it via relative path)
- **States:** `.revealed` on `.results-phase` (arrival), `--phase-i` stagger, `@media(max-width:760px)` (path → 1 column, smaller stage), `@media print` (all phases visible, light treatment), `prefers-reduced-motion` (final state instantly, no count-up)
- **Notes:**
  - **Arrival, not printout:** phases start at `opacity:0` + `translateY(26px)` and reveal as they enter the viewport; the score counts up with an easeOutCubic landing. Reduced motion skips all of it — the reveal is a courtesy, never a gate.
  - **Set `--scoreDeg`** = score × 3.6deg and **`--scoreColor`** per score band on `.score-stage`; put the final score in `data-count-to` on `.score-number` for the count-up.
  - **Accessibility:** the score stage carries `role="img"` + a full `aria-label` (the counting number is `aria-hidden`); each phase is labelled by its title.
  - The `.results-divider` between phases is structural rhythm, not decoration — it marks the journey's beats.
  - Calm by design: one accent wash (the arrival radial), jewel only in the ring, level pill, and divider diamond. Maximum life, minimum noise.

## Use it

1. Copy `results-path.css` and `results-path.js` next to your page; also copy the `dimension-orb` block for phase 2.
2. Link `tokens.css`, then `dimension-orb.css`, then `results-path.css`; load the JS at the end of body.
3. Paste the markup; set `--scoreColor` / `--scoreDeg` / `data-count-to`; render dimension orbs and path steps from your results:

```html
<div class="results-path">
  <section class="results-phase results-phase-arrival" style="--phase-i:0" aria-labelledby="rpScoreTitle">
    <div class="results-phase-kicker">Your personal AI mastery report</div>
    <h2 class="results-phase-title" id="rpScoreTitle">Your Naya Power Score</h2>
    <p class="results-phase-sub">{{one calm line about what the score means}}</p>
    <div class="score-stage" style="--scoreColor:#b895ff;--scoreDeg:295.2deg" role="img" aria-label="Naya Power Score: 82 out of 100">
      <div class="score-content">
        <span class="score-number" data-count-to="82" aria-hidden="true">0</span>
        <span class="score-outof">OUT OF 100</span>
      </div>
    </div>
    <div class="result-level" style="--scoreColor:#b895ff">
      <span class="result-level-dot"></span><span>Advancing</span>
    </div>
    <div class="results-divider" aria-hidden="true"></div>
  </section>

  <section class="results-phase" style="--phase-i:1" aria-labelledby="rpDimsTitle">
    <div class="results-phase-kicker">Your five dimensions</div>
    <h2 class="results-phase-title" id="rpDimsTitle">How you actually work with AI</h2>
    <p class="results-phase-sub">{{why the breakdown matters}}</p>
    <div class="results-dimensions">
      <!-- assessment/dimension-orb constellation here -->
    </div>
    <div class="results-divider" aria-hidden="true"></div>
  </section>

  <section class="results-phase" style="--phase-i:2" aria-labelledby="rpPathTitle">
    <div class="results-phase-kicker">Your next level</div>
    <h2 class="results-phase-title" id="rpPathTitle">Where to go from here</h2>
    <p class="results-phase-sub">{{the path framing}}</p>
    <div class="path">
      <article class="path-step">
        <div class="path-number" aria-hidden="true">1</div>
        <h4>{{step title}}</h4>
        <p>{{step body}}</p>
      </article>
    </div>
  </section>
</div>
```

## Selectors

```
.results-path
.results-phase
.results-phase.revealed
.results-phase + .results-phase
.results-phase-kicker
.results-phase-title
.results-phase-sub
.results-phase-arrival
.results-phase-arrival::before
.score-stage
.score-stage::before
.score-stage::after
.score-content
.score-number
.score-outof
.result-level
.result-level-dot
.results-divider
.results-divider::after
.results-dimensions
.path
.path-step
.path-number
.path-step h4
.path-step p
```

## JS API

```
ResultsPath.reveal(phase)   — reveal one phase immediately
ResultsPath.revealAll()     — reveal every phase (e.g. before printing)
ResultsPath.reobserve()     — re-run the IntersectionObserver (after dynamic render)
```
