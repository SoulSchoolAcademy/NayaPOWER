# SMART-GRAPHS — the display layer of Smart Stats

**Status:** spec v1 · CANDIDATE · 2026-10-09

Smart Stats is the promise — *"give me the stats on anything."* Smart Graphs is
how that promise looks: the visual instrument any data plays through.

## The grammar (seven laws)

**G1** Every stat is a living thing — entrance motion + quiet pulse, always.
**G2** Magnitude becomes light — bigger value = more glow, never more ink.
**G3** Spectrum order: purple → blue → cyan → green → gold. Max five colors.
**G4** The number is the hero — white, tabular numerals, largest on the card.
**G5** One accent per stat. The purple soul appears somewhere, always.
**G6** Truth in every state — loading shimmers, empty is honest, errors speak.
**G7** The card is the contract — title, sub-line, visualization, foot + 4 actions.

## The seven instruments

| # | Specimen | Block | When the data is… |
|---|---|---|---|
| 01 | `specimens/01-pulse-orb.html` | `pulse-orb` | one number with emotional weight |
| 02 | `specimens/02-jewel-pillars.html` | `jewel-pillar` | discrete series to compare |
| 03 | `specimens/03-spectrum-flow.html` | `spectrum-flow` | parts-of-a-whole over time |
| 04 | `specimens/04-constellation.html` | `constellation` | entities + relationships |
| 05 | `specimens/05-pulse-rings.html` | `pulse-rings` | liveness / rates across streams |
| 06 | `specimens/06-living-counter.html` | `living-counter` | a number checked daily |
| 07 | `specimens/07-orbit-dial.html` | `orbit-dial` | a score out of 10 |

Blocks live in `../DESIGN-BLOCKS/blocks/graphs/` and are registered in
`../DESIGN-BLOCKS/blocks/index.json` (v1.3, 48 blocks).

## The three tellings

- `SMART-GRAPHS-SPEC.human.md` — the warm, plain telling
- `SMART-GRAPHS-SPEC.ai.md` — the exact telling: values, procedures, constraints
- `smart-graphs-spec.machine.json` — the structured schema for systems

## Honesty

Specimens use sample data and say so on the card. Mode A (automatic) exists
when NayaNET event instrumentation exists; until then, automatic stats are
SAMPLE-labeled. The four actions (Save · Share · PDF · Send to NayaNET) are
specified and reserved in v1 — the contract ships before the wiring.
