# Smart Block: `naya-voice-button`

The voice read-aloud button for the Maxis assessment — Naya reads the current question aloud. Idle → speaking (pulsing jewel orb + waveform hint) → paused. Carries an honest voice-kind label (synthesized vs cloned) and stop-on-navigate behavior hooks so audio never leaks across questions.

- **Type:** buttons
- **Source:** authored 2026-10-09 for Maxis assessment completion (orb/button anatomy verbatim from `Maxis App Design.html`; waveform, voice-kind badge, and `.paused` state are new)
- **Files:** `naya-voice-button.css`, `naya-voice-button.js`, `specimen.html`
- **Dependencies:** tokens.css (specimen ships a minimal `--ease` shim); `data-voice-kind` defaults to `synthesized`
- **States:** default, `:hover`, `:active` (press compression), `:focus-visible`, `.playing` (pulse + waveform), `.paused` (dimmed orb, frozen waveform), `data-voice-kind="cloned"`, `@media(max-width:420px)` (waveform hides), `@media print` (hidden), `prefers-reduced-motion` (no pulse/wave/transform)
- **Notes:**
  - **Honest labeling:** the badge reads "Synthesized voice" by default because the block drives `speechSynthesis`. It flips to "Naya's voice" only via `NayaVoiceButton.setVoiceKind(btn, 'cloned')` — call that only when the canonical cloned voice service is actually wired. Never present the synthesized tier as her real voice.
  - **The block never guesses content:** on idle tap it dispatches `naya-voice-request`; the host assessment answers with `NayaVoiceButton.speak(questionText)`. This keeps the button decoupled from question state.
  - **Stop-on-navigate:** the assessment must dispatch `window.dispatchEvent(new Event('naya-voice-stop'))` before rendering the next question. Escape and tab-hidden are built-in safety nets.
  - Possible overlap: the indexed `naya-btn` (buttons) is the canonical Naya CTA — this one is the assessment's voice-activation atom, distinct and extracted.
  - 44px+ target: the button's min-height is 54px; the 39px orb is decorative, not the target.

## Use it

1. Copy `naya-voice-button.css` and `naya-voice-button.js` next to your page.
2. Link `tokens.css` first, then `naya-voice-button.css`; load the JS at the end of body.
3. Paste the markup; answer `naya-voice-request` with the current question text; dispatch `naya-voice-stop` on navigation:

```html
<button class="naya-button" type="button" aria-label="Listen to Naya" aria-pressed="false" data-voice-kind="synthesized">
  <span class="naya-orb" aria-hidden="true"></span>
  <span class="naya-copy">
    <span class="naya-primary">Press Play</span>
    <span class="naya-secondary">Listen to Naya</span>
    <span class="naya-voice-kind">Synthesized voice</span>
  </span>
  <span class="naya-waveform" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>
</button>

<script>
// host assessment wiring
document.querySelector('.naya-button').addEventListener('naya-voice-request', function (e) {
  NayaVoiceButton.speak(currentQuestionText, e.target);
});
function goToNextQuestion() {
  window.dispatchEvent(new Event('naya-voice-stop')); // stop audio on navigate
  renderQuestion(next);
}
</script>
```

## Selectors

```
.naya-button
.naya-button:hover
.naya-button:active
.naya-button:focus-visible
.naya-button.playing
.naya-button.paused
.naya-orb
.naya-orb::after
.naya-button.playing .naya-orb::after
.naya-button.paused .naya-orb
.naya-button.playing .naya-orb::before
.naya-copy
.naya-primary
.naya-secondary
.naya-voice-kind
.naya-button[data-voice-kind="cloned"] .naya-voice-kind
.naya-waveform
.naya-waveform i
.naya-button.playing .naya-waveform
.naya-button.playing .naya-waveform i
.naya-button.paused .naya-waveform
```

## JS API

```
NayaVoiceButton.speak(text, btn?)   — start reading text aloud
NayaVoiceButton.stop()              — stop and reset all buttons
NayaVoiceButton.toggle(btn?)        — play → pause → resume → request cycle
NayaVoiceButton.setVoiceKind(btn, 'synthesized'|'cloned')
NayaVoiceButton.rewire()            — wire buttons added after load
Events: 'naya-voice-request' (dispatched on idle tap), 'naya-voice-stop' (on window, stops all)
```
