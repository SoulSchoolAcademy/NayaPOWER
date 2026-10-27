# PI READINESS DATASET — the record, measured and mapped (2026-10-26)

**Essence:** the Project Intelligence record holds **355 rows but only 330 real items** — 25 items are counted twice. Every one of the 330 items now has exactly one area, a named-or-flagged owner state, and a dedup survivor picked by rule. This dataset is preparation only — nothing was written to the production record; applying it stays gated.

## The census (read live tonight, GET-only)

| | Rows | Queued | In progress | Verifying | Done (proven) | Needs Shawn | Blocked |
|---|---|---|---|---|---|---|---|
| Raw rows | 355 | 207 | 75 | 15 | 46 | 8 | 4 |
| Real items (deduped) | **330** | 195 | 70 | 13 | **40** | 8 | 4 |

**Reconciliation — no contradiction, one discovery.** This census matches the newest seat census exactly, state for state (355 / 46 done). Against the earlier census (346 rows, 323 items, 40 done) the record grew +9 rows and +7 items tonight, and proven-done is unchanged at **40 real items** — all 6 extra "done" rows are duplicate twins. The discovery: the duplicates are **double-inserts across 9 different project IDs** in the same table. Filtering to the one canonical PI project alone returns 295 items and hides the problem entirely — the inflation lives in the cross-project twins.

## Duplicates: 25 keys, 0 conflicts

No duplicated item disagrees with its twin about state — every pair is the same item inserted twice, agreeing on title and state. Survivor rule applied in order: (a) evidence + named prover, (b) most advanced state, (c) fuller next action. Almost every pair ties through all three rules and falls to the final tie-break: the canonical-project row survives. Two exceptions worth knowing: **f28 and f32** survive on their non-canonical twin under rule (c), because only that twin carries a next action — on application, its text should be merged into the canonical row, not the item moved. One pair (**enh-a-x1**) is duplicated *inside* the canonical project itself.

## Every item has an area (330 of 330 placed — no "unmapped")

| Area | Items | Done | % done |
|---|---|---|---|
| pi-hub | 74 | 6 | 8.1% |
| hub-dashboard | 72 | 8 | 11.1% |
| factory-interfaces | 52 | 11 | 21.2% |
| voice-audio | 33 | 5 | 15.2% |
| membership-money | 17 | 1 | 5.9% |
| welcome | 15 | 0 | 0.0% |
| connection | 15 | 1 | 6.7% |
| mail-notifications | 14 | 4 | 28.6% |
| projects-spaces | 13 | 1 | 7.7% |
| security-privacy | 12 | 1 | 8.3% |
| identity-settings | 10 | 2 | 20.0% |
| match | 3 | 0 | 0.0% |

Judged item by item (the earlier keyword pass placed only 144 of 323). Confidence: **187 high · 85 medium · 58 low** — every low-confidence placement carries its one-line reason in the machine file. The honest pattern in the lows: team-operations, governance, and loop-health items have no product area of their own, so they sit in pi-hub (their tracking home) or their operating area, flagged as best-fits rather than truths.

## Owners: 139 real items have none

160 raw rows carry no owner; deduped, **139 of 330 items (42%) are ownerless**. Of the owner values that do exist, 16 distinct spellings were found for what should be a handful of seats: the canonical `naya-power` (46 rows), `naya-nitro` (56), and `naya-resolve` (31) are clean, but `director` (37 rows) is a role label, `Resolve` is a short form, and 11 further values are wave/stage/lane labels ("Best-of-Best Wave 1", "Dashboard stage (Nu)", "Team Nitro (cert repair seat…)"). The machine file maps every value found to a proposed canonical form, with the basis for each.

## What applying this dataset would change

1. **Counts become true:** 355 → 330 items; done drops from a displayed 46 to a true 40, and every percentage in the face recomputes from real items.
2. **Every area gets a real denominator** — the per-area percentages above replace the current derivation, which leaves most items unplaced.
3. **25 twin rows are removed by rule**, each survivor named with its rule — no judgment calls left at application time, except the f28/f32 next-action merge.
4. **Owner cleanup becomes a checklist:** 13 non-canonical spellings normalize to canonical seats or slugs, and the 139 ownerless items become the explicit claim list.

Machine file: `pi-readiness-dataset-2026-10-26.machine.json` (same folder) — full census, all 25 dedup plans with both rows of each pair, all 330 area assignments with confidence, and the owner map.
