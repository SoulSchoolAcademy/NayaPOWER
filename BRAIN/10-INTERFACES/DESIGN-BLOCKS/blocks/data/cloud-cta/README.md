# Smart Block: `cloud-cta`

The teaching interstitial — a full-screen modal overlay (`.interstitial`) holding the glowing teaching card (`.teaching-cloud`): ambient glow, eyebrow, icon, title, body copy, and the continue button. Shown between assessment questions.

- **Type:** data
- **Source:** `Maxis App Design.html`
- **Files:** `cloud-cta.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `.visible` on `.interstitial` (toggled by JS to show the modal), `:hover` on `.cloud-button`, `.cloud-button.secondary` variant, `@keyframes veilIn` / `cloudIn`, `@media print`, `@media(max-width:760px)`, `prefers-reduced-motion`
- **Notes:**
  - This is a REAL component, not decorative glow — extracted as instructed. Markup is verbatim from the source body (the `.interstitial` overlay + `.teaching-cloud` card are one component; `interstitial` is folded in here rather than as its own single-selector block).
  - The `teaching` namespace resolves to this block: `.teaching-cloud` is its root. Teaching interstitials appear between assessment questions — see the variant note in `assessment/question-card`.
  - `.button-arrow` is bundled (used inside `.cloud-button`).
  - Possible overlap: the indexed `nl-modal` overlay — this is the assessment's teaching modal with its own glow treatment and anatomy; genuinely different, extracted.

## Use it

1. Copy `cloud-cta.css` next to your page.
2. Link `tokens.css` first, then `cloud-cta.css`.
3. Paste the markup; toggle `.visible` on `.interstitial` to show/hide; fill `.cloud-body` per interstitial:

```html
<div class="interstitial" id="teachingInterstitial" aria-modal="true" role="dialog" aria-labelledby="cloudTitle">
  <div class="teaching-cloud">
    <div class="cloud-glow"></div>
    <div class="cloud-eyebrow" id="cloudEyebrow">WHY THIS MATTERS</div>
    <div class="cloud-icon" aria-hidden="true">✦</div>
    <h2 class="cloud-title" id="cloudTitle">Let's look at something important.</h2>
    <div class="cloud-body" id="cloudBody">{{teaching copy}}</div>
    <div class="cloud-actions">
      <button class="cloud-button" id="cloudContinue" type="button">
        Got it — let's go <span class="button-arrow">→</span>
      </button>
    </div>
  </div>
</div>
```

## Selectors

```
.button-arrow
.continue-button:hover:not(:disabled) .button-arrow
.interstitial
.interstitial.visible
.teaching-cloud
.cloud-glow
.cloud-eyebrow
.cloud-icon
.cloud-title
.cloud-body
.cloud-body strong
.cloud-actions
.cloud-button
.cloud-button:hover
.cloud-button.secondary
```
