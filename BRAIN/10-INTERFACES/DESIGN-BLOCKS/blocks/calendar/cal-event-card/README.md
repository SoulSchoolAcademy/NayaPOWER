# Smart Block: `calendar/cal-event-card`

Atomic event card: serif time rail, glowing spectrum spine, type tag in its fixed color, serif title, location/attendees row; all-day, multi-day span, and tentative variants.

## Why

One event, fully dressed: time rail, serif title, type tag in its fixed spectrum color, location/attendees row. Hover lifts 6px and ignites in the event's own color — the card is themed, so it burns its own hue.

**Do / Don't** — Do: let the card ignite in the event's own spectrum color — purple for deep work, blue for meetings, gold for deadlines. Don't: rest the card in its color; a card that wears its hue at rest is a flood, and floods are forbidden.

- **Type:** calendar
- **Catalog:** NAYA-CAL-002
- **Source:** `gap-blocks/calendar-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.cal-event:hover` (lift 6px, ignite in the event's own color), `.cal-event:active` (settle 4px), `.cal-event:focus-visible` (white 2px ring), `.cal-event.is-allday` (rail collapses to a glowing band), `.cal-event.is-span` (rail carries the date range), `.cal-event.is-tentative` (dashed edge, `~` time)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Render `.cal-event` with `data-tone` set to the event type color; add `.is-allday` / `.is-span` / `.is-tentative` for the variants.

## Selectors in this block

```
.cal
.cal-event
.cal-event:hover
.cal-event:active
.cal-event:focus-visible
.cal-rail
.cal-rail .t
.cal-rail .dur
.cal-body
.cal-body::before
.cal-type
.cal-title
.cal-meta
.cal-meta span
.cal-meta svg
.cal-event.is-allday .cal-rail
.cal-event.is-allday .cal-rail .t
.cal-event.is-allday .cal-rail .dur
.cal-event.is-allday .cal-body
.cal-allday-flag
.cal-event.is-span .cal-rail .t
.cal-span-note
.cal-event.is-tentative
.cal-event.is-tentative .cal-rail .t::after
```

## Notes

- Anatomy (from the source spec): - **Time rail:** the left column — serif time, uppercase duration. Time is the rail the card hangs on. - **Spine:** 3px glowing line in the event color — the card's identity mark, shared with CAL-004's timeline. - **Type tag:** pill in the event color, letterspaced. The tag's color is the fixed meaning from the family table — never improvised per card. - **Title:** serif voice, 18px. The human name of the event. - **Meta row:** drawn SVG glyphs (pin, people), never emoji — Law 4. Glyphs inherit …
