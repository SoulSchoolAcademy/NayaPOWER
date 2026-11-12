# Smart Block: `calendar/cal-month-board`

Month-view board: a full month on black ground with white-lit day cells, gold today, event pills in spectrum-wheel order, and an honest +N overflow chip.

## Why

A full month on black ground: serif weekday headers, day cells with white-lit edges, today ignited in gold, event pills in wheel order. Law 1: nothing dead — every in-month cell lifts and ignites; chevrons promise "go somewhere" and do.

**Do / Don't** — Do: walk the wheel down each cell — magenta → purple → blue → green → gold, adjacent pills always in law order, never adjacent duplicates. Don't: paint event types by mood of the day; the meaning of each color is fixed across the whole family, or the wheel becomes decoration.

- **Type:** calendar
- **Catalog:** NAYA-CAL-001
- **Source:** `gap-blocks/calendar-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.cal-day:hover` (lift + chrome-purple ignition), `.cal-day.is-selected` (held purple edge + glow), `.cal-day.is-today` (2px gold edge + gold glow + 4s breathe), `.cal-day.is-out` (34% opacity, jumps to that month on click), `.cal-pill` overflow chip (`+N more`, honest)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Drop the `.cal-month` board in; `block.js` wires day selection (one selected day; Enter/Space on a focused cell).

## Selectors in this block

```
.cal
.cal-month
.cal-head
.cal-title
.cal-title small
.cal-nav
.cal-chev
.cal-chev i
.cal-chev.next i
.cal-chev:hover
.cal-chev:active
.cal-chev:focus-visible
.cal-week
.cal-week span
.cal-grid
.cal-day
.cal-day .dnum
.cal-day:hover
.cal-day.is-selected
.cal-day.is-today
.cal-day.is-today .dnum
0%
100%
50%
.cal-day.is-out
.cal-day.is-out:hover
.cal-pill
.cal-pill::before
.cal-pill:hover
.cal-pill .t
.cal-dots
.cal-dots i
.cal-more
.cal-more:hover
@keyframes cal-breathe
```

## Notes

- Anatomy (from the source spec): - **Board chrome:** 5-layer board shadow, 24px radius, tone under-glow. The board is the world; cells live inside it. - **Title:** serif voice, month in 24px, year as an uppercase letterspaced kicker. White 99%. - **Chevrons:** drawn CSS chevrons (Law 4 — icons are drawn), 44px targets, chrome-purple ignition. A chevron promises "go somewhere." - **Weekday row:** serif, uppercase, letterspaced — the voice of the calendar. - **Day cell:** the unit. Number (serif) + pills + dots + more-chip, in …
