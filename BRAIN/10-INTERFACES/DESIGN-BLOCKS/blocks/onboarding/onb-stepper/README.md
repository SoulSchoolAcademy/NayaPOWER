# Smart Block: `onboarding/onb-stepper`

Five-step progress rail: jewel nodes in step colors, a spectrum thread that fills as you advance, done/current/locked states, and an honest empty panel.

## Why

The multi-step progress rail: five jewel nodes (done / current / locked), a spectrum thread behind them that fills as you advance, one job named per step, skippable steps marked honestly "optional." Law 1: reachable nodes lift and ignite in their own step color; the current node breathes. A locked step is dim and truly inert — it never fakes being clickable. Never a wall of forms: the rail shows the journey, each step carries exactly one job.

**Do / Don't** — Do: mark skippable steps with a plain "Optional" chip and give the step's own content an honest "Skip this step" control — skipping is a first-class choice, not a hidden shame. Don't: unlock all steps "for preview": a locked step you can peek into teaches the user that locks are theater, and then nothing in the flow is trusted.

- **Type:** onboarding
- **Catalog:** NAYA-ONB-001
- **Source:** `gap-blocks-2/onboarding-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.onb-step:hover` (reachable: lift 2px, own step-color ignition), `.onb-step.is-current` (held ignition + 3s breathe), `.onb-step.is-locked` (34% opacity, `disabled`, out of tab order), `.onb-step:active .onb-node` (`filter:brightness(1.25)`), `.onb-rail.is-empty` (honest "No steps yet" panel — JS does not touch it)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — click a reachable node to move `.is-current`; `block.js` paints done/current/locked, fills the thread, and stamps aria labels.

## Selectors in this block

```
.onb
.onb-rail
.onb-thread
.onb-fill
.onb-steps
.onb-step
.onb-node
.onb-node .in
.onb-node .in svg
.onb-step:hover .onb-node
.onb-step:hover
.onb-node:active
.onb-node:focus-visible
.onb-step.is-current .onb-node
0%
100%
50%
.onb-step.is-locked .onb-node
.onb-step.is-locked .onb-node .in
.onb-step.is-locked:hover
.onb-step.is-locked:hover .onb-node
.onb-label
.onb-label .k
.onb-label .t
.onb-label .s
.onb-label .s::before
.onb-step.is-locked .onb-label .s::before
.onb-opt
.onb-job
.onb-no-steps
.onb-no-steps .jewel
.onb-no-steps h3
.onb-no-steps p
@keyframes onb-node-breathe
```

## Notes

- Done steps carry no extra rule: the node is colored by its `--sc` step color and the check glyph marks completion; `.is-done` remains the JS/AT state hook.
- Anatomy (from the source spec): - **Thread:** the journey line — dark track, spectrum-strip fill in the 5-stop law order. The fill is the walked spectrum; it never runs backward. - **Node jewel:** the rotated diamond, white → step-color → black, own-color glow. Done shows a drawn check (Law 4 — icons are drawn); current shows the number and breathes; locked shows the number at 34%. - **Label stack:** kicker (Step N, letterspaced), serif title, status with a jewel dot in the step color — the dot is information, not decoration. …
