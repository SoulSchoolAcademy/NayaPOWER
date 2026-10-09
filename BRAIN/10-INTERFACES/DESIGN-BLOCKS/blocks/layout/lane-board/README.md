# Smart Block: `lane-board`

The mission-table lane board — a horizontal set of lanes (NOW / NEXT / WAITING / …), each with a head (name + count) and intelligence cards, plus the honest empty-lane state ("Nothing qualifying here.").

- **Type:** layout
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `lane-board.css`, `specimen.html`
- **Dependencies:** tokens.css (`--room-accent` set inline where needed)
- **States:** responsive `@media` (inherited source breakpoints)
- **Notes:**
  - JS-rendered in the source (ListsRoom render); the specimen converts it to static HTML. Lane names, counts, and the empty-state copy are verbatim.
  - `.lane`, `.list-card`, `.why`, `.meta-row` are bundled as the board's rendered structure.
  - No indexed block covers a lane/kanban board — extracted as new.

## Use it

1. Copy `lane-board.css` next to your page.
2. Link `tokens.css` first, then `lane-board.css`.
3. Paste the markup; one `.lane` per lane, `.lane-count` = item count, `.why` for the empty state:

```html
<div class="lane-board">
  <section class="lane">
    <div class="lane-head"><span>NOW</span><span class="lane-count">2</span></div>
    <article class="list-card">
      <b>{{title}}</b>
      <div class="why">{{why this item is here}}</div>
      <div class="meta-row"><span>{{meta}}</span></div>
    </article>
  </section>
  <section class="lane">
    <div class="lane-head"><span>WAITING</span><span class="lane-count">0</span></div>
    <div class="why">Nothing qualifying here.</div>
  </section>
</div>
```

## Selectors

```
.lane-board
.lane
.lane-head
.lane-count
.list-card (+ b)
.why (+ ::before)
.meta-row (+ span)
```
