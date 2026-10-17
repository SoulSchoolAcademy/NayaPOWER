# Naya Composer v1

**Pieces + page type in → finished page out. Design laws auto-applied.**

Built by Naya Nitro Nu (BUILD seat, Team Nitro) — item 15, directive #4.
Head start: the Design Studio prototype (`../design-studio/studio-v1.html`);
this is not a parallel system — the composer's law engine is ported from
StudioCore and the 43 studio law checks are re-proved on the ported engine
as a 39-check suite. The exact 43→39 accounting — which checks consolidated,
which (if any) were dropped and why, what each of the 39 covers — lives in
`MAPPING-43-39.md`, so any reader can account for every check on both sides.

## The one function

`compose(state, ctx, css)` → `{html, stops, notes, state}` — everything flows
through it. The CLI is a thin wrapper.

## Files

| File | What |
|------|------|
| `composer.js` | The composer. Node ≥14, CommonJS. Law engine (wheel, walk, advisor), piece registry, builders, five page-type recipes, CLI, self-check. Exports its core when `require()`d. |
| `naya-core.css` | The studio's law surfaces, verbatim — ALIVE/ELEVATION in code. Embedded into every page the composer builds, so the laws hold by construction. |
| `report-recipe.json` | Content context for the sample report (stats, chart, table, cards). Not the laws — just the words. |
| `sample-report-page.html` | The sample: `composer.js --type report` on the prototype's pieces (`button:lead, board:mix, tabs:smarttabs, jewels:gems, block:icard, truth:honest`), accent blue. |
| `feed-recipe.json` | Content context for the second specimen (Smart Feed shape: newest-first notes, IN A NUTSHELL anatomy). Not the laws — just the words. |
| `sample-feed-page.html` | The second specimen: `composer.js --type feed` on the prototype's pieces, accent green — proves generalization beyond the report page type. |
| `MAPPING-43-39.md` | The 43→39 accounting: which studio checks consolidated, which were dropped and why, what each of the 39 covers. |
| `README.md` | This file. |

## Usage

```bash
node composer.js --type report --accent blue \
  --pieces button:lead,board:mix,tabs:smarttabs,jewels:gems,block:icard,truth:honest \
  --in report-recipe.json --out sample-report-page.html
node composer.js --selfcheck   # 39/39 law checks on the engine + a composed report
```

Page types: `feed`, `dashboard`, `form`, `gallery`, `report`.
Slots: `button board tabs jewels block truth accent` — unknown pieces fall back
to the prototype default of their slot; a typo never ships a hole.

## The laws, as code

- **SPECTRUM** — every page takes as many stops off the 11-stop wheel as it has
  zones (report: 5 → blue → green → gold → pink → purple), always in spectral
  order, always distinct. Adjacent zones never share a hue by construction.
- **ALIVE / ELEVATION** — the embedded `naya-core.css` carries the 5-layer board
  formula, the one-button DNA, white-lit rest edges, and ignite-on-touch glows.
- **ADVISOR** — flat buttons, colored body text, and unverified stamps are
  refused and upgraded before composition. `truth: honest` keeps stamps honest.
- **HONESTY** — every page ends with the ◈ Demonstration footer and names what
  it is. A composed page can never claim live data it doesn't have.

## Verification evidence

- `node composer.js --selfcheck` → 39/39 passed (wheel/walk/advisor + a
  composed report inspected for balanced divs, wheel-hex zones, zone glows,
  jewel order, the honest footer, no fake-green stamps, no yellow). The
  39 are not the studio's 43 renamed — see `MAPPING-43-39.md` for the
  consolidation, narrowing, and drop accounting.
- `node composer.js --type feed --accent green --pieces button:lead,board:mix,tabs:smarttabs,jewels:gems,block:icard,truth:honest --in feed-recipe.json --out sample-feed-page.html` → the feed
  specimen: 4-zone walk green → orange → magenta → indigo, zero yellow
  hexes, ◈ Demonstration footer + "not live data" badge, deterministic
  (byte-identical across runs except the date stamp).
- `node test-studio-core.js` in `../design-studio/` → 43/43 passed on the
  unmodified prototype (the laws' source of truth).

## What's next (not Nu's seat)

- More page types (index-2 Hub rooms each get a recipe — feed and dashboard
  already cover most rooms).
- `walk()` spacing: current composer takes evenly-spaced stops; the studio
  did the same. Kept.
- A different seat must verify this build before it touches anything real.
