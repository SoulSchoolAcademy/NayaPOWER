# Smart Block: `wizard-stepper`

Interactive multi-step wizard. Jewel step nodes on a progress spine, obsidian panels, Naya-style buttons.

- **Type:** assessment
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `wizard-stepper.css`
- **Specimen:** `specimen.html`
- **States found:** .is-now, .is-done, :hover, :focus-visible, :disabled, .wz-btn--ghost
- **Dependencies:** wizard-stepper.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `wizard-stepper.css`.
3. Copy the `.wz` markup: `.wz-steps` (one `.wz-step` per step) + `.wz-panels` (one `.wz-panel` per step, same order).
4. Buttons use `data-wz-back` / `data-wz-next`. Include `wizard-stepper.js`.

## Selectors in this block

```
.wz
.wz-actions
.wz-body
.wz-btn
.wz-btn--ghost
.wz-btn:disabled
.wz-btn:hover
.wz-label
.wz-node
.wz-node:focus-visible
.wz-panel
.wz-panel.is-on
.wz-panels
.wz-step
.wz-step.is-done
.wz-step.is-now
.wz-steps
.wz-title
```

## Notes

- Current node is a purple jewel; completed nodes turn green. The spine lights up behind progress.
- Completed steps are clickable to go back; future steps are not.
- `wz:step` bubbles with `detail.step` and `detail.total` — gate validation on step change.
- Labels hide on small screens; nodes stay tappable.
