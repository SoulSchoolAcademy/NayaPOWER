# Smart Block: `comments/cmt-reactions`

Reaction row: jewel pills with honest counts, toggle on/off, a plus that opens the fixed five-reaction set. Reactions are opt-in delight — play, never status.

## Why

The play layer: jewel pills with honest counts, toggle on/off, a plus that opens the fixed set. Reactions are opt-in delight — the row never shames, never ranks, never badges. Law 2: each reaction burns its fixed wheel color; Law 1: pills lift and ignite on hover, and yours holds its glow.

**Do / Don't** — Do: render only reactions that exist — a row of three honest pills beats a row of five with two zeros. Don't: sort pills by count to manufacture a leaderboard; the family order is the wheel order, and popularity is not a ranking the UI gets to invent. Do: let anyone take a reaction back — toggling off is as easy as toggling on, no guilt copy, no "are you sure?". Don't: add badges, streaks, "top fan" labels, or any status game on top of the row — reactions are play, and play that keeps score stops being play.

- **Type:** comments
- **Catalog:** NAYA-CMT-003
- **Source:** `gap-blocks-2/comments-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.rx:hover` (lift 2px, own-reaction-color glow), `.rx.is-mine` (`aria-pressed="true"`, held glow + inner wash), `.rx:active` (settle 1px), `:focus-visible` (white 2px ring), `.rx-add` open (elevated popover, fixed five reactions), `zero count (the pill does not exist — no "0" ghost)`
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — pills toggle with `aria-pressed` and re-rendered counts; the plus opens the popover (Esc closes, focus returns).

## Selectors in this block

```
.cmt
.cmt-rx
.rx
.rx svg
.rx b
.rx:hover
.rx:active
.rx:focus-visible
.rx.is-mine
.rx.is-mine svg
.rx-add
.rx-add svg
.rx-add:hover
.rx-add:hover svg
.rx-add:focus-visible
.rx-pop
.rx-pop[hidden]
.rx-wrap
```

## Notes

- Anatomy (from the source spec): - **Pill:** the unit — drawn glyph + honest count in tabular numerals, 44px tall, 1.5px edge in the reaction's fixed color. One pill per reaction that exists. - **Glyph:** drawn SVG in the reaction color — heart, star, ringed dot, check, smile. Law 4: icons are drawn, and each promises exactly what it does. - **Mine state:** the held ignition — glow + wash + filled glyph. Visible without shouting. - **Plus:** the dashed 44px circle — the fixed set lives one tap away. The popover renders the …
