# Smart Block: `onboarding/onb-welcome-card`

First-run welcome board: Naya's drawn face lit from within, one warm line in her voice, exactly one next action, and a quiet "I'll explore on my own" exit.

## Why

The first-run greeting board: Naya's face and her energy — light with a face, drawn, never a stock avatar — one warm line in her voice, and exactly one clear next action. Law 3: the board rides the field with the full 5-layer shadow; it is a warm front door. Personal without creepy: the card knows only what the user gave it. No name known, no name used — the specimen below shows the honest nameless state.

**Do / Don't** — Do: keep exactly one primary CTA — the card has one job: get the user to the first step. Don't: add a second bright button "just in case," and never three competing CTAs; every extra button halves the chance the user presses any of them.

- **Type:** onboarding
- **Catalog:** NAYA-ONB-002
- **Source:** `gap-blocks-2/onboarding-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.onb-welcome:hover` (lift 5px, chrome-purple ignition), `.onb-cta:active` (settle 1px), `.onb-cta:focus-visible` (white 2px ring), `.onb-quiet:hover` (underline, 65% → full opacity)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — it personalizes the greeting from `data-name` on `#onbWelcome` (nameless default reads "Welcome." — no placeholder).

## Selectors in this block

```
.onb
.onb-welcome
.onb-welcome:hover
.onb-face
.onb-face svg
.onb-face::after
0%
100%
50%
.onb-kicker
.onb-hello
.onb-line
.onb-cta
.onb-cta svg
.onb-cta:hover
.onb-cta:active
.onb-cta:focus-visible
.onb-quiet
.onb-quiet:hover
.onb-knows
@keyframes onb-halo
```

## Notes

- Anatomy (from the source spec): - **Naya's face:** drawn SVG — lit orb (white → purple → black), two eyes with catchlights, one calm arc. A face *and* energy: the halo breathe is the energy. Never an emoji, never a stock avatar, never just a logo. - **Kicker:** "First run," letterspaced — it names the moment honestly. - **Headline:** serif voice, 32px. The name slot fills only from `data-name`; the template never invents one. - **One line:** 15px, 1.7 line-height, max 44ch — warm, plain words, one promise. Not a paragraph of …
