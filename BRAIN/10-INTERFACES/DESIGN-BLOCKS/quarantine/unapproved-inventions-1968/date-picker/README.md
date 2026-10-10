# Smart Block — forms/date-picker

Obsidian calendar trigger + popup in Naya's design language: machined edges, purple ignite, white text always.

- **Type:** form control · input
- **Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction
- **CSS:** `date-picker.css` (scoped `.dp-*`)
- **JS:** `date-picker.js` (open/close, month nav, select, keyboard)
- **Specimen:** `specimen.html`

## States
- Empty trigger (placeholder, secondary white)
- Open popup (purple edge glow on trigger)
- Hover day (lift + white edge)
- Today (white dot under number)
- Selected day (purple glow ring + purple number)
- Other-month days (30% opacity)

## Dependencies
- `tokens.css` shared tokens (inlined at top of `date-picker.css`, commented "shared")

## Use it
1. Drop the `.dp-root` markup (trigger + `.dp-popup`) anywhere a date is needed.
2. Include `date-picker.css` and `date-picker.js`.
3. Pre-fill by putting the date text in `.dp-label` and removing `.dp-empty` (selection syncs on open).
4. The trigger label updates automatically when the user picks a date.

## Selectors
```css
.dp-root      /* positioning wrapper */
.dp-trigger   /* 56px obsidian pill */
.dp-label     /* date text; .dp-empty = placeholder */
.dp-icon      /* calendar jewel icon */
.dp-popup     /* 320px obsidian panel; .dp-show = visible */
.dp-head      /* month header row */
.dp-month     /* "October 2026" */
.dp-nav       /* chevron nav buttons */
.dp-week      /* weekday header row */
.dp-grid      /* 7-col day grid */
.dp-day       /* 40px day cell; .dp-today / .dp-selected / .dp-dim */
```
