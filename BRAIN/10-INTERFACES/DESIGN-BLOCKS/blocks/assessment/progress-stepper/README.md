# Smart Block: `progress-stepper`

Assessment progress HUD — location readout (dot + "QUESTION n OF m"), the progress track with fill, and the percent readout. `aria-live="polite"` in the source.

- **Type:** assessment
- **Source:** `Maxis App Design.html`
- **Files:** `progress-stepper.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `@media(max-width:760px)`, `@media print`, `prefers-reduced-motion`
- **Notes:**
  - Markup is verbatim from the source body. The fill width is set by JS in the source (`#progressFill`); the specimen adds `style="width:7%"` for the demo.
  - No indexed block covers an assessment progress stepper — extracted as new.

## Use it

1. Copy `progress-stepper.css` next to your page.
2. Link `tokens.css` first, then `progress-stepper.css`.
3. Paste the markup; update the label, the fill width, and the percent as the user advances:

```html
<div class="progress-hud" id="progressHud" aria-label="Assessment progress" aria-live="polite">
  <div class="progress-location">
    <span class="progress-dot"></span>
    <span class="progress-label" id="progressLabel">QUESTION 1 OF 15</span>
  </div>
  <div class="progress-track" aria-hidden="true">
    <span class="progress-fill" id="progressFill" style="width:7%"></span>
  </div>
  <span class="progress-percent" id="progressPercent">7%</span>
</div>
```

## Selectors

```
.progress-hud
.progress-location
.progress-dot
.progress-label
.progress-track
.progress-fill
.progress-percent
```
