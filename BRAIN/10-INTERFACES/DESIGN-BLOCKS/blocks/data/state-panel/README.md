# Smart Block: `state-panel`

The system-state readout panel — a dark-elevated panel listing live status rows for a Hub or Ledger surface. Each row pairs an 8px glowing jewel marker with a label, an honest status line, and a right-aligned "as of" time; rows are `<li>` in a `<ul aria-live="polite">` so re-rendered statuses announce to assistive tech.

- **Type:** data
- **Source:** authored 2026-10-09 for Hub/Ledger completion
- **Files:** `state-panel.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** five jewel states — `--synced` (emerald), `--live` (purple, breathing pulse), `--degraded` (gold), `--offline` (quiet gray, no glow), `--error` (red); header summary jewel `--ok / --warn / --down / --quiet` matching the worst row; honest empty variant (`.state-empty`); responsive `@media` (stacked → three-column); `@media (prefers-reduced-motion: reduce)` kills the live pulse
- **Notes:**
  - No JS — statuses are rendered by the page; the block is the visual system.
  - Honest states only: never show "live" when it isn't. Offline/error rows carry their last-seen time ("Offline — last seen 2h ago", "Write failed — queued, will retry next cycle"); the empty variant says "No signals yet — connect a source to begin."
  - Jewel colors live only in the dots — label/status text stays white/silver.
  - Summary text (e.g. "2 synced · 1 live · 1 warning") is authored by the page to match the rows it renders.

## Use it

1. Copy `state-panel.css` next to your page.
2. Link `tokens.css` first, then `state-panel.css`.
3. Paste the panel; one `<li class="state-row">` per signal, dot class per state. For the empty case, swap the `<ul>` for `.state-empty`:

```html
<section class="state-panel" aria-labelledby="sys-state">
  <div class="state-head">
    <span class="state-summary-dot state-summary-dot--warn" aria-hidden="true"></span>
    <h2 class="state-title" id="sys-state">System state</h2>
    <p class="state-summary">2 synced · 1 live · 1 warning</p>
  </div>
  <ul class="state-list" aria-live="polite">
    <li class="state-row">
      <span class="state-dot state-dot--live" aria-hidden="true"></span>
      <div class="state-main">
        <div class="state-label">{{signal name}}</div>
        <div class="state-status">{{honest status line}}</div>
      </div>
      <span class="state-asof">as of {{time}}</span>
    </li>
  </ul>
</section>
```

## Selectors

```
.state-panel
.state-head
.state-title
.state-summary-dot (+ --ok / --warn / --down / --quiet)
.state-summary
.state-list
.state-row (+ + .state-row)
.state-dot (+ --synced / --live / --degraded / --offline / --error)
.state-main
.state-label
.state-status
.state-asof
.state-empty (+ b / p)
```
