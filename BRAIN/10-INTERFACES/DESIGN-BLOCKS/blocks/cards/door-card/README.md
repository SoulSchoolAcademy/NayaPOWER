# Smart Block: `door-card`

The Smart Door card — one governed door rendered as a card: top row (icon + name + "for" line), description, and a foot with the status pill plus either an IN USE badge (live doors) or a Contract action button (contract doors).

- **Type:** cards
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `door-card.css`, `specimen.html`
- **Dependencies:** tokens.css (`--door-accent`, `--room-accent`, `--btn-accent` set inline)
- **States:** `:hover`/`:active` on `.door` and `.btn`, `.pill` status variants (`.live` / `.ready` / `.soon` / `.contract` / `.spec`), `@keyframes pulse`, responsive `@media`, `prefers-reduced-motion`
- **Notes:**
  - JS-rendered in the source (`DoorCard` template literal); the specimen converts it to static HTML. Door text is verbatim from the source's DOORS registry. The card root's real class is `article.door` (not `door-card`) — the block id keeps the library naming.
  - The small atoms used in the foot (`.pill`, `.dot`, `.state-badge`, `.btn`, `.btn-ghost`, `.mini`) are bundled verbatim so the block is self-contained; the shared interaction resets are byte-identical to the source.
  - Possible overlap: the indexed `nav`/`footer` layout blocks — this is a door card, not chrome; genuinely different, extracted.

## Use it

1. Copy `door-card.css` next to your page.
2. Link `tokens.css` first, then `door-card.css`.
3. Paste the markup; set `--door-accent`; choose the live foot (pill + IN USE badge) or the contract foot (pill + Contract button):

```html
<article class="door" style="--door-accent:#9d75ff">
  <div class="door-top">
    <div class="door-icon">{{icon svg}}</div>
    <div><div class="door-name">{{name}}</div><div class="door-for">{{for line}}</div></div>
  </div>
  <div class="door-desc">{{description}}</div>
  <div class="door-foot">
    <span class="pill live"><span class="dot"></span>LIVE</span>
    <span class="state-badge" style="--room-accent:#9d75ff">IN USE</span>
  </div>
</article>
```

Contract variant foot:

```html
<div class="door-foot">
  <span class="pill contract"><span class="dot"></span>CONTRACT</span>
  <button class="btn btn-ghost" style="--btn-accent:#55b9ee" aria-label="{{name}}: view contract state">{{arrow icon}}<span>Contract</span></button>
</div>
```

## Selectors

```
.door
.door:hover
.door-top
.door-icon (+ svg)
.door-name
.door-for
.door-desc
.door-foot
.pill (+ .dot / .live / .ready / .soon / .contract / .spec)
.state-badge
.btn (+ :hover / :active / svg / [disabled])
.btn-ghost (+ :hover)
.action-row .mini
```
