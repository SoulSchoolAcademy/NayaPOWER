# Smart Block: `continue-button`

The assessment continue CTA, standalone — distinct from generic buttons because it carries momentum: "continue" is a promise of progress. Black heart, white voice, forward-motion affordance (the arrow slides on hover, a restrained sheen sweeps, and a one-time `.ready` breath fires the moment the button becomes clickable).

- **Type:** buttons
- **Source:** authored 2026-10-09 for Maxis assessment completion (`.continue-button` base anatomy verbatim from `Maxis App Design.html`, decoupled from the `.primary-black` compound; sheen, `.ready` breath, and `.continue-hint` are new)
- **Files:** `continue-button.css`, `continue-button.js`, `specimen.html`
- **Dependencies:** tokens.css (`--ease`; specimen ships a minimal shim)
- **States:** default, `:hover:not(:disabled)` (lift + ignite + sheen + arrow slide), `:active:not(:disabled)` (press compression, arrow slides further), `:focus-visible`, `:disabled` (dimmed, `cursor:not-allowed`), `.ready` (one-time breath on enable), `@media(max-width:420px)` (full width), `@media print` (hidden), `prefers-reduced-motion` (no transform/sheen/breath)
- **Notes:**
  - **This is not `primary-black`.** The source coupled `.continue-button` with `.primary-black` (the interest-select compound). This block is the standalone assessment CTA; the interest board keeps its own compound via `assessment/interest-select`.
  - **Momentum, not decoration:** every motion cue points forward — the arrow translates +3px on hover and +6px on press, the sheen sweeps left→right, and the `.ready` breath plays once when `disabled` is removed. The button is dimmed and honest while waiting.
  - **Pair it with `.continue-hint`** ("Select an answer to continue") under the waiting state — calm guidance, never nagging.
  - **The JS never changes disabled state** — it only observes it. Your assessment logic still owns enable/disable; the block just makes the transition felt.
  - 44px+ target: min-height 54px, full-width on small screens.

## Use it

1. Copy `continue-button.css` and `continue-button.js` next to your page.
2. Link `tokens.css` first, then `continue-button.css`; load the JS at the end of body.
3. Paste the markup; toggle `disabled` (+ `aria-disabled`) from your assessment logic when an answer is selected:

```html
<button class="continue-button" type="button" disabled aria-disabled="true">
  <span class="continue-text">Continue</span>
  <span class="button-arrow" aria-hidden="true">→</span>
</button>
<p class="continue-hint">Select an answer to continue</p>

<script>
// when the user picks an answer:
btn.disabled = false;
btn.setAttribute('aria-disabled', 'false'); // the .ready breath fires automatically
</script>
```

## Selectors

```
.continue-button
.continue-button::before
.continue-button::after
.continue-button:hover:not(:disabled)
.continue-button:hover:not(:disabled)::after
.continue-button:active:not(:disabled)
.continue-button:focus-visible
.continue-button:disabled
.continue-button:disabled::after
.button-arrow
.continue-button:hover:not(:disabled) .button-arrow
.continue-button:active:not(:disabled) .button-arrow
.continue-button.ready
.continue-hint
```

## JS API

```
ContinueButton.arm(btn)     — watch one button for the enable transition
ContinueButton.armAll()     — watch all .continue-button on the page
ContinueButton.breathe(btn) — play the .ready breath manually
```
