# Smart Block: `room-card`

The Hub room shell — the frame every room renders through: room outlet → head (kicker + title + description) → body → scene, with the room toolbar (segmented mode control + LED status line) as composed by the rooms.

- **Type:** cards
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `room-card.css`, `specimen.html`
- **Dependencies:** tokens.css (`--room-accent` set inline)
- **States:** `:hover` and `.active` on `.segmented button`, responsive `@media`, `prefers-reduced-motion`
- **Notes:**
  - JS-rendered in the source (HubView chassis + room builders, e.g. TodayRoom); the specimen converts it to static HTML. The toolbar composition (`.segmented` + `.room-status-line` with `.led`) is verbatim from TodayRoom.
  - The source nests `.room-scene` inside `.room-scene` (the room's zone section inside the scene wrapper) — kept verbatim.
  - `.kicker`, `.led`, `.segmented`, `.between` are bundled as part of the shell's rendered structure.
  - Possible overlap: the indexed `board` block — this is the room chrome (head/toolbar/outlet), not a content board; genuinely different, extracted.

## Use it

1. Copy `room-card.css` next to your page.
2. Link `tokens.css` first, then `room-card.css`.
3. Paste the markup; set `--room-accent`; render room content inside the inner `.room-scene`:

```html
<div class="room-outlet">
  <div class="room-head" style="--room-accent:var(--magenta)">
    <div class="kicker">{{KICKER}}</div>
    <h2>{{Room name}}</h2>
    <p>{{room description}}</p>
  </div>
  <div class="room-body" style="--room-accent:var(--magenta)" aria-live="polite">
    <div class="room-scene" style="--room-accent:var(--magenta)">
      <div class="room-toolbar between">
        <div class="segmented">
          <button type="button" class="active" aria-pressed="true">{{MODE}}</button>
        </div>
        <div class="room-status-line"><span class="led"></span><span>{{STATUS}}</span></div>
      </div>
      <section class="room-scene">{{room content}}</section>
    </div>
  </div>
</div>
```

## Selectors

```
.room-outlet
.room-head (+ .kicker / h2 / p)
.room-body
.room-scene
.room-toolbar (+ .between)
.segmented (+ button / button:hover / button.active)
.room-status-line (+ .led)
.kicker
.led
```
