# Factory Step 4 — Page Generator: Build Record

Seat: Naya Nitro
Date: 2026-10-22
Program: Factory Contract-Home audit, step 4 (`FACTORY-CONTRACT-HOME-AUDIT-2026-10-22.md`)
Status: **BUILT + PROVEN as a preview. NOT DEPLOYED** — deploying the generated
page is step 8, after scoring. The live page was not touched (verified below).

## What was built

| File | What it is |
|---|---|
| `engine/generate-factory-page.py` | The generator. Follows the step-2 twin generator's patterns: derives everything, `--check` byte-identity mode, fail-loud (exit 2) on any drift, defaults resolved from its own location. |
| `engine/factory-page-shell.html` | The current live page, harvested byte-for-byte (558,861 bytes, sha256 `b71ec26c1057a45b041e83bfa1e14d5e05217c8c405d75c776a59f18166296cf` = `md5 fb7d742d…` of nayanet.live/smartfactory at build time). The design authority and the generator's shell. |
| `engine/factory-page-presentation.json` | The presentation map, harvested from the shell by `--harvest`: 13 rails, 149 card presentations (rail, order, per-card `--sc`, descriptor, card dialect), both card templates, plus the hand-kept `overrides` (7 entries, each with its reason) and `new_rails` (1). |
| `../factory-page.generated.html` | The generated page — PREVIEW artifact (611,068 bytes, md5 `2ac6eba3003fa75d32aa6b9e646ff396`). |

The generator regenerates ONLY the parts shelf (the picker's `<section
id="step4">` rail region) from the store + map. Everything else is the
shell's bytes, carried verbatim (proof below). The page's other shelves
(templates, contract, examples) are beyond step 4's parts-shelf brief and
remain exactly as the live page has them.

## Reads (design gate)

Contract trio read before building: `NAYA-DESIGN-CONTRACT-V1.md` (v1.2,
stamped), `0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md` (CANONICAL,
ratified 2026-10-22), `~/workspace/team-nitro/DESIGN-LANGUAGE.md`. Parts
used, never recreated: the store's own piece markup (verbatim), the
store's own CSS (`factory.css`), and the live page's own rail + card
grammar (both dialects, harvested). Boot integrity gate: PASS 8/8 in the
worktree.

## Ground truth that corrected the brief

The step-4 brief (from the audit) says the live page shows ~51 of 154
pieces. Measured on the live bytes at build time, the picker already
carries **152 cards**: 148 built from store fragments + 3 hand-drawn
bespoke cards + the superseded NAYA-INP-001. The audit's "51" predates
the current page. The real gaps were six canonical pieces never shown —
including two crowned Reference pieces (INP-008, INP-009) and the crowned
Reference Hero (HRO-001) — plus one canonical piece (BRD-030) shown only
as a hand-made substitute. Those are exactly what generation cures.

## Acceptance equation — proven three ways

**154 (index canonical) == 154 (store canonical) == 154 (cards)**

1. Generator's own mechanical verify on every run (card count, card set
   == canonical set, no duplicates, every store fragment verbatim in the
   page, every ai_label carried): PASS; `--check`: generated file is
   byte-identical to a fresh generation.
2. Independent census (separate one-off counter over the generated
   bytes): 154 cards, 154 unique, set == canonical set, 154×
   `data-ai-purpose` / `data-ai-use` / `data-ai-laws`, zero non-canonical
   cards, zero missing.
3. Rendered DOM (headless Chromium, local file): **154 `.pcard` elements
   at desktop 1440px and at phone 390px, zero page errors on both.**

## Fidelity census (generated cards vs the shell's originals)

- 116 of 149 harvested cards byte-identical (modulo the added ai_label
  data attributes); 135 identical with whitespace ignored; 6 differ only
  by rail-tail segmentation in the census itself (content identical).
- Per-card `--sc` colors and one-line descriptors are page-only data (the
  store carries neither): harvested per piece into the map, never
  derived. The ICONS/INPUTS rails visibly rotate the walk per position;
  other rails are irregular — derivation would have recolored the shelf.
- Rail section colors are the page's own historical sequence, including
  its off-walk fossils (#6675ff, #40d3bb, #ffd45a): preserved verbatim.
  The No-Redesign Law makes the page the authority for its own rails; the
  generator does not "correct" them.

## The seven overrides (canonical pieces the current page does not show)

Recorded with reasons in the map's `overrides`; summary:

- **NAYA-ICO-024 / 025 / 026** (app tiles) → ICONS rail end; `--sc`
  continues that rail's own 7-color cycle. They also needed the store CSS
  (below) — on the shell alone their stages render empty.
- **NAYA-INP-008 Reference Well / NAYA-INP-009 Reference Select** (both
  crowned) → INPUTS rail end; the superseded NAYA-INP-001 leaves the
  shelf (index status superseded; the successor takes its place).
- **NAYA-HRO-001 Reference Hero** (crowned) → new **HEROES** railblock
  appended after OVERLAYS, in the page's exact rail grammar; `--sec`
  #40d3bb is the next color in the page's own 9-color section cycle, the
  card's `--sc` is the hero's own purple. The hero family had no rail at
  all; nothing existing moves.
- **NAYA-BRD-030** → CIRCLES rail, board dialect, after BRD-029 — renders
  the REAL store piece (see deltas).

## Carried CSS (the pieces' own, from factory.css)

The newly shown pieces use 18 classes the shell page never defined
(`app-tile`, the `ref-hero` family, `ref-well` family, `ref-select`
family) — all defined in the canon's own `factory.css`. The generator
derives exactly those rules (file order, @media recursed, referenced
@keyframes and shell-missing :root variables carried) and emits them as
one marked `<style data-generated="factory-piece-css">` block (9,399
bytes). By construction it cannot restyle anything the shell defines —
every class in it is shell-undefined. Verified by render: before the
carry, the app-tile stages were empty black boxes; after, the tiles glow
and the Reference Well shows its true recipe (silver-white rim, obsidian
fill, white placeholder).

## Named deltas (canon wins, on the record — none silent)

1. **BRD-030** — the live page draws a presentation circle that exists
   nowhere in the store; the piece's own ai_label states the stored
   markup is a stat grid. The generated card renders the store piece.
   The index name "Feature circle" stands (canon's name); the descriptor
   is distilled from the ai_label ("metrics with trends, at a glance")
   because the old descriptor described the substitute.
2. **BRD-031 / BRD-032 / BRD-033 excluded** — index status "verified",
   not canonical, absent from the store. The hand-injected
   `#feature-circles-row` wrapper that grouped the three substitutes
   goes with them; the rail is itself the horizontal strip. If these
   circles should be canon, they enter `pieces.json` first (a store
   decision), and generation picks them up via the addition rule.
3. **Extended demos** — NAV-010, OVL-005, BRD-039/040/042/043: the live
   stages repeat some pieces as extra demo instances (the store fragment
   is a strict prefix). Generated stages render the store fragment: each
   piece once, whole — the store is the authority.
4. **ai_label data attributes** on every card (`data-ai-purpose`,
   `data-ai-use`, `data-ai-laws`): additive, invisible, the dual-label
   carry-through in machine-readable form where the piece stands. The
   page's Notes button stays what it is on the live page (the buyer's
   cart note) — untouched.
5. **HEROES rail appended** (see overrides) — the shelf's one shape
   change, because a canonical family had no rail.

## Fail-loud smokes (all on scratch copies)

- Store piece dropped (index still lists it): exit 2 — "canonical sets
  disagree: index-only ['NAYA-BTN-001']".
- Presentation entry dropped: exit 2 — addition rule names the piece.
- Generated file tampered by one byte: `--check` exit 1.
- Shell changed without re-harvest: blocked by the map's shell-sha256
  guard.

## Render + interaction proof (~/workspace/factory-step4-proof/)

13 frames, headless Chromium, local file: page top (shell face
unchanged) · picker rails (desktop) · ICONS rail end with the new app
tiles · card close-ups: ICO-024 (tile glowing), INP-008 (Reference Well
recipe), INP-009 (Reference Select), BRD-030 (the real stat piece),
HRO-001 (purple hero panel) · HEROES railblock · FEATURES rail head
(first card BRD-034 — the 033 substitute is gone) · phone picker ·
phone heroes. Interaction: clicking **Select** on the generated
INP-008 card moved the cart badge 0 → 1; **Notes** opened the page's own
note editor; zero page errors. All 12 inline scripts pass `node --check`.

## Live page untouched

`curl https://nayanet.live/smartfactory | md5sum` after all work:
`fb7d742d6dbc570295ce0a43926f17c3` — the Make It Yours build, unchanged.
Deploying the generated page is step 8.

## Self-score: 9.2 / 10

Why not 10: (1) the six new descriptors are my one-line distillations of
ai_label purpose — a scorer's pass should confirm the voice; (2) the
HEROES rail placement and the hero card's full-height rendering are
judgment calls a different seat should weigh; (3) BRD-030's grid reads
unevenly among the round boards of the CIRCLES rail — truthful to the
store, but the rail's rhythm is canon's call to settle; (4) the picker
region is regenerated, the page's remaining shelves are carried, not yet
generated — full-page generation is a later step's scope, named here so
nobody mistakes this for it.
