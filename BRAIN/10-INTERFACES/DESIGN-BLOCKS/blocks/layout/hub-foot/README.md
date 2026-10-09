# Smart Block: `hub-foot`

The hub's mission close — the mission quote (`.hub-quote`: promise line + sub-line) and the mission footer (`.hub-foot`: mission headline + statement + ecosystem link row with glowing dots).

- **Type:** layout
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `hub-foot.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** responsive `@media` (inherited source breakpoints)
- **Notes:**
  - SPLIT PROVENANCE: the `.hub-quote` markup is verbatim from the source (JS-rendered mission quote). The `.hub-foot` markup was REMOVED from the source on 2026-10-03 ("Mission footer removed — dead buttons with no destination"); its CSS survives, so the footer in the specimen is reconstructed from CSS and marked as such.
  - Possible overlap: the indexed `footer` (naya-footer: brand lockup, link columns, social, legal) — this is the Hub's mission footer + quote treatment; different purpose and styling, extracted with the overlap noted.

## Use it

1. Copy `hub-foot.css` next to your page.
2. Link `tokens.css` first, then `hub-foot.css`.
3. Paste the markup:

```html
<div class="hub-quote">
  <p class="hub-quote-text">Your life creates your intelligence every day.</p>
  <p class="hub-quote-sub">Naya helps you capture it, understand it, remember it, compound it, and use it.</p>
</div>

<footer class="hub-foot">
  <div class="hub-foot-mission">
    <b>{{mission headline}}</b>
    <p>{{mission statement}}</p>
  </div>
  <div class="hub-foot-links">
    <a class="hub-foot-link" href="{{url}}"><span class="hub-foot-dot"></span>{{LABEL}}</a>
  </div>
</footer>
```

## Selectors

```
.hub-quote
.hub-quote-text
.hub-quote-sub
.hub-foot
.hub-foot-mission b
.hub-foot-mission p
.hub-foot-links
.hub-foot-link
.hub-foot-dot
```
