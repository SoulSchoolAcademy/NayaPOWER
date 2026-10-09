# Smart Block: `headline`

Headline + subhead typography pair. Editorial serif headline in white, silver subhead. Exact type scale from the shared tokens: 40 chapter / 24 section / 20 card / 18 sub / 14 detail.

- **Type:** composition
- **Source:** authored 2026-10-09 (cold-test gap fill — no source file existed)
- **CSS:** `headline.css`
- **Specimen:** `specimen.html`
- **States found:** none (static type)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page) and `headline.css`.
2. Wrap kicker + headline + subhead in `.cmp-eyebrow` for the standard rhythm unit.
3. Sizes: `.cmp-headline--chapter` (40px, page titles), `--section` (24px, default), `--card` (20px, inside boards).
4. Set `--kc` on `.cmp-kicker` for its jewel color. **The headline is always white** — hierarchy comes from size, never from colored text.

## Composing

- Use `headline` anywhere a `section`'s built-in title isn't enough — inside boards, above grids, in overlays.
- For full page sections (kicker + title + deck + dividers), prefer the `section` block.
- Pair with `body-text` for headline → copy flow.

## Selectors in this block

```
.cmp-headline
.cmp-headline--chapter
.cmp-headline--section
.cmp-headline--card
.cmp-sub
.cmp-sub strong
.cmp-sub--detail
.cmp-kicker
.cmp-eyebrow
```
