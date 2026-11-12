# Smart Block: `feed/li-card`

Ledger intel card with identity-color edge bar, jewel glyph, source label, time-ago, hint pill, and flash hook.

## Why

Ledger intel needs its identity at a glance. The identity-color edge bar, jewel glyph, and time-ago put who, what, and when in the first 200 milliseconds — the flash hook earns the tap.

- **Type:** feed
- **Source:** `Ledger Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** rest, hover / focus-visible (card + hint pill), `li-card-hint` highlight on card hover, `licardin` entry animation (opt-in `animate`), `libar` pulsing edge bar (staggered via `--i`), `liflash` hook via `flash` param, DEMO chip (opt-in)
- **Dependencies:** `.li-stage` wrapper (base rule prepended into `block.css`; block is self-contained)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `liCard({title, summary, source, time, jewel, hint})` and append the returned element. Wrap page content in `.li-stage`.

## Selectors in this block

```
.li-stage
.li-stage .li-hero.li-flash
.li-stage .li-jewels
.li-stage .li-jewel
.li-stage .li-jewel:hover
.li-stage .li-jewel:focus-visible
.li-stage .li-jewel-g
.li-stage .li-jewel-n
.li-stage .li-jewel-c
.li-stage .li-card
.li-stage .li-card::before
.li-stage .li-card:hover
.li-stage .li-card:focus-visible
.li-stage .li-card-top
.li-stage .li-card-j
.li-stage .li-card-s
.li-stage .li-card-t
.li-stage .li-card-title
.li-stage .li-card-n
.li-stage .li-card-m
.li-stage .li-card-hint
.li-stage .li-card:hover .li-card-hint
.li-stage .li-card:focus-visible .li-card-hint
@keyframes liflash
@keyframes licardin
@keyframes libar
@keyframes lgpulse
```

## Notes

- The extraction bundle also includes the `.li-jewel*` rules and two touch-target normalization rules (`button,.li-tab,.li-jewel,.li-card,[role="button"]{min-height:44px;...}` and the `user-select` rule) because they shipped inside the same staging CSS file; class strings are untouched.
- The source's `state.search` title-highlight (`mark.li-hl`) is app-state plumbing and is intentionally dropped; plain title text is used.
- `li-flash` is kept as a class hook on the card, but the shipped keyframe rule is scoped `.li-hero.li-flash` only — it has no visible effect on `.li-card` in this block. The flash animation itself is owned by the hero block.
- Identity color (`--ic`) defaults to the source's `LI_FLOW` palette cycled by `index`; pass `color` to pin it.
