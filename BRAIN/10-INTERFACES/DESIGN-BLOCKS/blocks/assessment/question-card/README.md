# Smart Block: `question-card`

Assessment quiz card with selectable answer options — the question header (label, title, rule) plus the answer button anatomy (jewel glyph, title/sub copy, chevron), including the selected state.

- **Type:** assessment
- **Source:** `Maxis App Design.html`
- **Files:** `question-card.css`, `specimen.html`
- **Dependencies:** tokens.css (specimen ships a minimal `--ease` shim; `--accent` is set inline per answer)
- **States:** `:hover` and `.selected` on `.answer` (chevron ignites in both), `@media(max-width:760px)`, `@media(max-width:420px)`, `@media print`, `prefers-reduced-motion`
- **Notes:**
  - The answer buttons are JS-rendered in the source (template literal); the specimen converts them to static HTML. The `.answer` root class itself carries the button styling (the task's selector list named only the `answer-*` parts — `.answer`, `.answers`, `.jewel`, `.glyph`, `.chevron` are included because they are the option's real structure).
  - **Teaching variant:** between questions the app shows teaching interstitials — those are the `cloud-cta` block (`data/cloud-cta`), not this one.
  - Possible overlap: the `hero`/`headline` type blocks — this one is genuinely page-specific (assessment Q&A), extracted.

## Use it

1. Copy `question-card.css` next to your page.
2. Link `tokens.css` first, then `question-card.css`.
3. Paste the markup (set `--accent` per answer for its jewel/selection tint; toggle `.selected` + `aria-pressed` on choice):

```html
<div class="question-area" id="questionArea">
  <div class="question-label" id="questionLabel">AI CRAFTSMANSHIP</div>
  <h1 class="question-title" id="questionTitle">{{question text}}</h1>
  <div class="question-rule" aria-hidden="true"></div>
</div>

<div class="answers" id="answers" role="group" aria-label="Answer choices">
  <button type="button" class="answer" data-answer-id="{{id}}" style="--accent:#b895ff" aria-pressed="false">
    <span class="jewel" aria-hidden="true">
      <span class="glyph">✦</span>
    </span>
    <span class="answer-copy">
      <span class="answer-title">{{answer title}}</span>
      <span class="answer-sub">{{answer description}}</span>
    </span>
    <span class="chevron" aria-hidden="true">›</span>
  </button>
</div>
```

## Selectors

```
.question-area
.question-label
.question-label::before, .question-label::after
.question-label::after
.question-title
.question-rule
.answers
.answer
.answer:hover
.answer.selected
.jewel
.jewel::after
.glyph
.answer-copy
.answer-title
.answer-sub
.chevron
.answer.selected .chevron, .answer:hover .chevron
```
