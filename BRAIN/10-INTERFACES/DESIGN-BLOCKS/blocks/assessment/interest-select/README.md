# Smart Block: `interest-select`

The "one last thing" interest-selection board — eyebrow, title, intro copy, a swipeable board of selectable interest cards (orb + check + name + description), board dots, continue + skip actions. Also covers the report-side `.interest-pill` summary chips.

- **Type:** assessment
- **Source:** `Maxis App Design.html`
- **Files:** `interest-select.css`, `specimen.html`
- **Dependencies:** tokens.css (`--interest` is set inline per card)
- **States:** `:hover` and `.selected` on `.interest-area` (check ignites), `.active` on `.interest-board` / `.board-dot`, `.visible` on `.interests`, `:hover` on `.primary-black` / `.interest-skip`, `@keyframes boardIn`, `@media print`, `@media(max-width:760px)`, `prefers-reduced-motion`
- **Notes:**
  - The section shell is verbatim from the source body; the interest cards are JS-rendered (template literal) and converted to static HTML here. The selectable card's real class is `interest-area` (not `interest-pill`) — `interest-pill` is the report-side chip listing chosen areas; both are included.
  - `.primary-black` / `.button-arrow` / `.board-dots` / `.board-dot` rules are bundled because they are part of this board's rendered structure.
  - No indexed block covers interest selection — extracted as new.

## Use it

1. Copy `interest-select.css` next to your page.
2. Link `tokens.css` first, then `interest-select.css`.
3. Paste the markup; toggle `.selected` + `aria-pressed` on the chosen `.interest-area` cards:

```html
<section class="interests visible" id="interestsView" aria-labelledby="interestTitle">
  <div class="interest-eyebrow">ONE LAST THING</div>
  <h2 class="interest-title" id="interestTitle">Where do you want AI to become more useful to you?</h2>
  <p class="interest-intro">Choose anything that interests you. …</p>
  <div class="interest-board active" data-board="0">
    <button type="button" class="interest-area" style="--interest:#35e39b" data-area-id="{{id}}" aria-pressed="true">
      <span class="interest-orb" aria-hidden="true"><span class="interest-check">✓</span></span>
      <span class="interest-name">{{name}}</span>
      <span class="interest-description">{{description}}</span>
    </button>
  </div>
  <div class="board-dots">
    <span class="board-dot active" data-dot="0"></span>
    <span class="board-dot" data-dot="1"></span>
    <span class="board-dot" data-dot="2"></span>
  </div>
  <div class="interest-actions">
    <button class="primary-black" type="button">Continue to My Report <span class="button-arrow">→</span></button>
  </div>
  <button class="interest-skip" type="button">Skip this step</button>
</section>
```

Report-side pills:

```html
<span class="interest-pill">{{chosen area name}}</span>
```

## Selectors

```
.continue-button, .primary-black
.continue-button::before, .primary-black::before
.continue-button:hover:not(:disabled), .primary-black:hover
.button-arrow
.continue-button:hover:not(:disabled) .button-arrow
.interests
.interests.visible
.interest-eyebrow
.interest-title
.interest-intro
.interest-board
.interest-board.active
.interest-area
.interest-area:hover
.interest-area.selected
.interest-orb
.interest-check
.interest-area.selected .interest-check
.interest-name
.interest-description
.board-dots
.board-dot
.board-dot.active
.interest-actions
.interest-actions .primary-black
.interest-skip
.interest-skip:hover
.interest-pill
```
