# Smart Block: `activity-stream`

The time-grouped stream: time heads, timeline rows, live dot with pulse, ambient pulse ring. The container the feed renders through.

## Why

Time is the feed’s real structure. Time-grouped heads with a live pulse dot turn a pile of cards into a day you can follow — the container that makes the stream feel alive.

- **Type:** feed
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `activity-stream.css`
- **Specimen:** `specimen.html`
- **States found:** live dot pulse (livedot), ring breathe (pulsebreathe)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `activity-stream.css`.
3. Copy the HTML from `specimen.html`.

## Selectors in this block

```
.activity-stream
.activity-time-group
.activity-time-head
.activity-timeline-row
.activity-live-dot
.activity-pulse-ring
```
