# Smart Block: `calendar/cal-day-states`

The seven honest day-cell states specified once (rest, hover, selected, today, has-events, disabled, out-of-month) so month boards and pickers never drift apart.

## Why

The seven honest states of a calendar day, specified once so CAL-001 and CAL-003 never drift apart. A state is visual truth: if it looks clickable it is clickable; if it looks dead it is dead.

**Do / Don't** — Do: freeze today above selection in the precedence order — when both apply, the day wears gold, because today is the fact and selection is the choice. Don't: invent an eighth state for "weekend" or "holiday" tinting; tinting days by category is a flood by another name — holidays are events, and events already have colors.

- **Type:** calendar
- **Catalog:** NAYA-CAL-005
- **Source:** `gap-blocks/calendar-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.s-hover` (lift + chrome-purple ignition, static example), `.s-selected` (the hover ignition held), `.s-today` (gold 2px edge + glow + 4s breathe), `.s-events` (jewel dots in wheel order), `.s-disabled` (32% opacity, strikethrough, inert), `.s-out` (34% opacity, still jumps to its month)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Apply the state classes `.s-hover`, `.s-selected`, `.s-today`, `.s-events`, `.s-disabled`, `.s-out` on `.cal-st` cells. If today is also selected, gold wins.

## Selectors in this block

```
.cal
.cal-states
.cal-st
.cal-st .dnum
.cal-st .lbl
.cal-st .why
.cal-st.s-hover
.cal-st.s-selected
.cal-st.s-today
.cal-st.s-today .dnum
.cal-st.s-events
.cal-st.s-events .dots
.cal-st.s-events .dots i
.cal-st.s-disabled
.cal-st.s-disabled .dnum
.cal-st.s-out
.cal-st.s-out .lbl::after
```

## Notes

- Anatomy (from the source spec): - **The cell:** one class per state (`.s-hover`, `.s-selected`, `.s-today`, `.s-events`, `.s-disabled`, `.s-out`) — states compose by class, never by inline-style improvisation. - **Precedence order:** today > selected > hover > has-events > rest; disabled and out-of-month modify the base independently. Written down so two builders never disagree. - **The label:** every specimen carries its state name — teaching statically, per the state-strip pattern. - **Reduced motion:** the today-breathe …
