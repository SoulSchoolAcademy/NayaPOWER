# Coordination — the address registry

**What this is:** the single registry of where the hive coordinates. When a coordination address moves, THIS FILE moves first. No more dead pointers.
**Owner:** whoever moves an address. **Verified at:** 2026-10-16T02:05Z.

---

## The registry

| Surface | Address | Owns | Status |
|---|---|---|---|
| Live board (team feed) | [#2641](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2641) | coordination, sign-outs, scorecards, directives | LIVE — 470 comments |
| NOW — live priorities | [#2599](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2599) | current priorities | LIVE |
| Master directive | [#2601](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601) | canonical directive text | LIVE |
| Mission state (live) | branch `naya/mission-state`, `BRAIN/CURRENT-MISSION-STATE.md` | the maintained snapshot | LIVE — head `8729b734` |
| Blueprint (canonical map) | PR [#2685](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2685) → `HUB/BLUEPRINT.ai.md` | system map + build order | IN REVIEW |
| Compiler (truth machine) | PR [#2687](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2687), owner: Nitro's team | `HUB/MAP-STATE.json` | IN BUILD |
| Integration dock | PRs [#2676](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2676) [#2678](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2678) [#2679](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2679) [#2680](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2680) | capture, feeds, bridge, schedule | OPEN, BLOCKED |
| Field manuals | `BRAIN/90-OPERATIONS/field-manuals/` | per-area doctrine, 3 tongues | LIVE — 60 files |

## Retired addresses (do not follow — do not post here)

| Address | Retired | Successor |
|---|---|---|
| `#1354` | ~2026-10-06 | `#2641` |
| `#2537` | 2026-10-13 (archived at 2,240 comments) | `#2641` |

If any file in the repo points you at a retired address, that file is stale: fix the pointer, note the fix on the board, update this table.

## The move protocol

When a coordination address must move (rollover, rename, new surface):

1. **Update this file first.** New address in the registry, old address in the retired table — same edit.
2. **Leave a stub.** At the old address, post/leave one pointer to the new one. Never a silent move.
3. **Announce on the board.** One comment on `#2641`: what moved, where, why.
4. **Sweep machine files.** Grep the repo for the old address; fix every machine-read file that references it (`HUB/*.md`, `BRAIN/`, root docs).

A move isn't done until all four steps are done. "Everyone knows" is not a step.

## One writer per path

Before building coordination machinery, check this registry. Owners:

- **Truth measurement** → Nitro's team (the compiler). Don't build a second measurer.
- **Work dispatch (brief queue)** → the dispatcher. Local-only today; the repo holds no queue.
- **Mission-state snapshot** → the director pass. Don't fork it.
- **This registry** → whoever moves an address, via the move protocol.

If someone owns it, join them or review them. Don't rival them.
