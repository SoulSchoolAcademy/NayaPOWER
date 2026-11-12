# Smart Block: `calendar/cal-agenda-list`

Day agenda as a vertical timeline: serif time gutter, glowing spectrum spine per event type, cards in the CAL-002 language, gold now-line, honest empty state.

## Why

The day's events as a vertical timeline: time gutter, glowing spectrum spine per event type, cards in CAL-002's language. A day with nothing on it says so honestly — "Nothing scheduled — the day is yours."

**Do / Don't** — Do: give every event one glowing spine in its fixed type color, in wheel order down the day — the timeline should read as a walked spectrum. Don't: render a now-line on any day that isn't today; a fake "now" on last Tuesday is a trust violation with styling.

- **Type:** calendar
- **Catalog:** NAYA-CAL-004
- **Source:** `gap-blocks/calendar-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.cal-ev:hover` (lift 4px, own-color ignition), `.cal-now` (gold now-line + "now" flag, today only), `.cal-empty` (gold jewel, "Nothing scheduled"), `.cal-ev.is-past` (spine dimmed to 40%, no hover lift)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Render `.cal-agenda`; cards follow the CAL-002 markup language. Render `.cal-now` only when viewing today; past events get `.is-past` (dimmed, no hover theater).

## Selectors in this block

```
.cal
.cal-agenda
.cal-agenda h2
.cal-agenda .sub
.cal-tl
.cal-tl li
.cal-tl li:last-child
.cal-gutter
.cal-spine
.cal-tl li::before
.cal-ev
.cal-ev:hover
.cal-ev:focus-visible
.cal-ev h3
.cal-ev .tag
.cal-ev .meta
.cal-now
.cal-now i
.cal-now b
.cal-empty
.cal-empty .jewel
.cal-empty h3
.cal-empty p
```

## Notes

- Anatomy (from the source spec): - **Time gutter:** serif times, right-aligned — the rail the day hangs on. - **Spine:** 3px glowing line per event in its type color — the same identity mark as CAL-002's card spine, so the two blocks read as one object. - **Node jewel:** the rotated diamond where gutter meets spine — Law 4, bullets are jewels, at timeline scale. - **Event card:** CAL-002's language compressed — tag, serif title, one meta line. One idea per card. - **Now-line:** the honest present — gold, labeled, clock-driven. …
