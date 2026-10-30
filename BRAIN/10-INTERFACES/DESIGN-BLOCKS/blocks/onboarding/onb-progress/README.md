# Smart Block: `onboarding/onb-progress`

Honest progress: linear bar and ring variants, the percent as a real number from real work, one-ignition celebration on complete, and an honest indeterminate state.

## Why

Progress as honest truth: a linear bar and a ring variant, the percent as a real number from real work, and a celebration state that fires exactly one ignition and then goes calm. Law 1: numbers breathe — no static numbers on screen. The specimen freezes 62%; a live build binds the number to the work and nothing else.

**Do / Don't** — Do: derive the number, the fill width, the ring offset, and `aria-valuenow` from one source — four mouths, one truth. Don't: stall at 99% while work finishes (theater), don't ease a fake 0→100 on load (the number must mean completed work), and don't celebrate twice: re-adding `.is-complete` to re-fire the ignition is confetti with extra steps.

- **Type:** onboarding
- **Catalog:** NAYA-ONB-003
- **Source:** `gap-blocks-2/onboarding-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.onb-prog:hover` (lift 3px, ring answers with soft glow), `.onb-prog.is-complete` (one 1.1s gold ignition, then calm), `.onb-prog.is-ind` (honest indeterminate — drift, not a fake number), `@media (prefers-reduced-motion:reduce)` (ignition, breathe, drift all stop)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Set the percent from real work (style/`aria-valuenow`); add `.is-complete` exactly when the work completes — the one 1.1s gold ignition fires, then calm. Use `.is-ind` only when no number exists.

## Selectors in this block

```
.onb
.onb-prog
.onb-prog:hover
.onb-prog-top
.onb-prog-top .lbl
.onb-pct
.onb-pct small
0%
100%
50%
.onb-bar
.onb-fillbar
.onb-sub
.onb-ringwrap
.onb-ring
.onb-ringwrap:hover .onb-ring
.ring-track
.ring-prog
.onb-ring-num
.onb-ring-num b
.onb-ring-num b small
.onb-ring-num span
.onb-prog.is-complete
.onb-prog.is-complete .onb-fillbar
.onb-prog.is-complete .onb-pct
.onb-ringwrap.is-complete .ring-prog
.onb-ringwrap.is-complete .onb-ring-num b
.onb-ringwrap.is-complete
30%
.onb-prog.is-ind .onb-fillbar
.onb-prog.is-ind .onb-pct
@keyframes onb-num-breathe
@keyframes onb-celebrate
@keyframes onb-drift
```

## Notes

- Anatomy (from the source spec): - **Label row:** uppercase letterspaced job ("Getting set up") + serif percent. The percent is the headline of this block — set it in the voice. - **Linear bar:** 12px track, inset shadow, strip-gradient fill in law order. The fill *is* the walked spectrum; at 100% it resolves to gold. - **Ring:** 168px SVG, 11px stroke, gradient walked around the path, round cap, start at twelve o'clock. The number sits in the middle in serif — the ring frames the truth, it doesn't decorate it. - …
