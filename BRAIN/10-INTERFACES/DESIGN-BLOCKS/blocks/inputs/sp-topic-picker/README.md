# Smart Block: `sp-topic-picker`

Topic chip multi-select for the space creator — inviting chips with spectrum-cycling jewel markers. Each chip carries its own `--tc`; selected chips (`.on`) wear their own-color edge and tint plus a checkmark. Toggle freely; the group emits `sp-topics-change` with the selected topic list.

- **Type:** inputs
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-topic-picker.css`, `sp-topic-picker.js`, `specimen.html`
- **States:** `.on` (selected), `:hover`, `:active` (press), `:focus-visible`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** none — self-contained; `--tc` set inline per chip, cycling the spectrum.

## Use it

1. Copy `sp-topic-picker.css` + `sp-topic-picker.js` into your page or component folder.
2. Paste the markup below; assign `--tc` per chip, cycling the spectrum (purple → blue → emerald → gold → magenta → orange → teal → red).
3. Listen for `sp-topics-change` (`event.detail.topics` = array) on `.sp-topic`.

```html
<div class="sp-topic" role="group" aria-label="Pick topics">
  <button class="sp-topic-chip on" data-topic="ai-building" style="--tc:#7c3aed"><span class="sp-topic-gem" aria-hidden="true"></span>AI Building</button>
  <button class="sp-topic-chip" data-topic="design" style="--tc:#1e6fd9"><span class="sp-topic-gem" aria-hidden="true"></span>Design</button>
  <button class="sp-topic-chip" data-topic="health" style="--tc:#0d9e6f"><span class="sp-topic-gem" aria-hidden="true"></span>Health</button>
  <button class="sp-topic-chip" data-topic="money" style="--tc:#d4a017"><span class="sp-topic-gem" aria-hidden="true"></span>Money</button>
</div>
```

## Selectors

```css
.sp-topic
.sp-topic-chip
.sp-topic-chip:hover
.sp-topic-chip:active
.sp-topic-chip:focus-visible
.sp-topic-chip.on
.sp-topic-chip.on::after
.sp-topic-gem
.sp-topic-chip.on .sp-topic-gem
```
