# Smart Block: `calendar/cal-date-picker`

Form date picker: input-styled trigger opening an elevated mini month grid; today in gold, past dates truly inert, full keyboard contract (arrows/Enter/Esc).

## Why

A compact picker for embedding in forms: an input-styled trigger showing the chosen date, a dropdown mini month grid, keyboard-honest focus states, past dates visibly dimmed and truly inert. Law 1: the trigger lifts and ignites chrome-purple like any control; the days ignite purple on hover and hold it when chosen.

**Do / Don't** — Do: make past dates visibly dimmed and keyboard-unreachable — a disabled date that still takes focus is a lie with styling. Don't: pre-fill the trigger with "today" to look alive; an unchosen picker says "Choose a date" until a human chooses.

- **Type:** calendar
- **Catalog:** NAYA-CAL-003
- **Source:** `gap-blocks/calendar-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.cal-trigger:hover` (lift 2px, chrome-purple ignition), `.cal-drop[hidden]` / open (elevated panel, `aria-expanded`), `day `:hover` / `:focus-visible` (white 2px ring)`, `.is-chosen` (held purple edge + glow), `.is-todayd` (gold edge + gold number), `past days (32% opacity, `disabled`, out of tab order)`
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — it builds the mini month, wires open/close, and enforces the keyboard contract. `trig.dataset.value` carries the chosen ISO date.

## Selectors in this block

```
.cal
.cal-pick
.cal-trigger
.cal-trigger:hover
.cal-trigger:active
.cal-trigger:focus-visible
.cal-trigger svg
.cal-trigger .ph
.cal-drop
.cal-drop[hidden]
.cal-drop-head
.cal-drop-head h3
.cal-mini
.cal-mini .wd
.cal-mini button
.cal-mini button:hover:not(:disabled)
.cal-mini button:focus-visible
.cal-mini button.is-chosen
.cal-mini button.is-todayd
.cal-mini button:disabled
.cal-mini button:disabled:hover
.cal-tz
```

## Notes

- Anatomy (from the source spec): - **Trigger:** the form-facing face — reads as an input, behaves as a button. Glyph is drawn SVG, never emoji. - **Dropdown panel:** the mini month — weekday initials, 36px day buttons, the month title in serif voice. - **Day button:** the unit — number, hover ignition, chosen hold, today gold, past inert. - **Timezone footnote:** the honesty line — "Calendar date only — no timezone is assumed or stored." It is part of the block, not documentation. **What it will NOT fake:** it never pretends …
