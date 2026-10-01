# Your Reports — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/reports`. **Accent:** emerald. **Build order:** 2.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. `hub/reports?period=day|week|month|year`.

## Component tree

1. `ReportsHero` — title, tagline, `PeriodTabs` (giant segmented).
2. `EditionShelf` — edition covers for the period (period label, headline synthesis, coverage note, item counts).
3. `EditionView` — period-specific section templates:
   - Day: summary, discoveries, learning, decisions, creation, relationships, activity, open questions, synthesis.
   - Week: story, emerging themes, momentum, what changed, learned, unresolved, relationships, opportunities.
   - Month: patterns, trajectory, knowledge growth, project movement, relationship development.
   - Year: year-in-intelligence narrative sections.
4. `ClaimBlock` — claim text + inline drill-down affordance + evidence drawer.
5. `CoverageNote` — "based on N verified notes; M gaps."

## Data bindings

- Editions ← synthesis engine over the period's evidence set (Today editions, Feed history, Ledger receipts where value-relevant).
- Generate ← runs synthesis only when evidence exists; persists edition (receipt in Ledger for the generation action).

## States

- `no_edition`: shelf shows "Generate" for the period. `generating`: progress, honest. `ready`: edition view. `thin_data`: edition generates with prominent coverage note. `empty_period`: "Nothing was recorded this week."

## Interactions

- Period tab → center reorganizes (shelf + template swap), URL param updates.
- Generate → synthesis job → edition appears with coverage note.
- Claim drill-down → evidence drawer (Smart Notes, timestamps, sources).
- Share/Export → Connect preview → consent → receipt.

## Design tokens

Emerald accents (tabs, section markers, Generate button). Edition covers: obsidian with emerald edge-light, oversized period typography.

## Acceptance

Period switch reorganizes (not just re-labels); weekly reads as story; every claim drillable; thin data → honest coverage; generation leaves Ledger receipt; 9.0+.
