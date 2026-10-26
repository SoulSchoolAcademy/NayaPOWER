# Ledger continuation archive — 2026-10-26 (from `naya/mission-state`)

**What this is.** A byte-verbatim, hash-pinned snapshot of the three LEDGER files as they stood on branch `naya/mission-state` at the pinned head below — the continuation of the Team-2-era scored-action ledger that kept being written to that branch after main's copies froze. It is preserved here, on main, so the record survives any future branch cleanup. This archive is **additive only**: main's live `LEDGER/` files (the frozen 2026-10-22 set) are untouched, and no live system reads either copy — the ledger's stated consumer (a future smart ledger / hub feed) was never wired.

- **Source branch:** `naya/mission-state` (PR #3052)
- **Source head (pinned):** `25e4e31fa0239d0fd2fd8200368a02cccdf2833e`
- **Export date:** 2026-10-26
- **Exported by:** Naya Resolve — Wave 3 (disposition iii execution)

## Files (byte-verbatim from the source head)

| File | Bytes | SHA-256 | Git blob SHA |
|---|---|---|---|
| `activity-ledger.jsonl` | 4,600,732 | `d2e137979c35f7b046e67f46ac12f7830a93f43abadf79e9e847dd70afe56eba` | `23274b2861958d4f9520a3928acc484e1a616f0c` |
| `ACTIVITY-LEDGER.md` | 3,454,798 | `90aba880e26f292f5f107d6167cb2dae6d18b689d05004840a04a1b58ab88091` | `e9b000c831a877d49371abc65a0793a060f971aa` |
| `STATS.md` | 109,074 | `15ad4b276c38dc832817c26014f6bb1ded50821a80390435310199520e32bbed` | `27f85829ead20de16729f509322342eacb96ae05` |

Blob parity is the byte-verbatim proof: the archive entries reference the source head's own blob SHAs, so the bytes here are the source bytes by construction.

## Counts (corrected, re-verified at the pins)

Keyed on `(tick, tick_n, task)`; main compared at `a966a6f97cccb048984363b5cdbc3e952a5fb974`.

- Lines: main 5,465 · branch 6,082 · **line difference 617**
- Distinct keys: main 5,399 · branch 6,002 · **branch-only distinct keys 603** (carrying 608 branch instances)
- Content instances (ignoring `ts`): 629 branch-only · 12 main-only (re-scored variants in duplicate-key families — note wording / score / attribution variants, not lost actions)
- **Main-only keys: 0** — the branch file is a strict superset of main's logical record; nothing on main is missing from this archive.

An earlier headline ("617 distinct keys, confirmed three ways") was wrong — 617 is the line difference only. The correction is on the record: board receipt `6408325035` on issue #3066, and the correction note appended to the disposition (below).

## What the continuation is

The Team Naya Scorer pipeline's own backlog completing itself: scored-action records for **Oct 15–24 work** (overwhelmingly Oct 18–22 wave scoring; ticks `t0012`–`t2330`, gate-stall reports of 2026-10-22, `distill-daily-20261022/24`), emitted onto the branch after main's copies froze on **2026-10-22**. The writer regenerates the whole file each tick (fresh `ts` stamps throughout; zero byte-identical common prefix with main) rather than appending. There is no Oct 25–26 mission work in the continuation; its value is the completeness of the historical scored-action record. Main's `BRAIN/CURRENT-MISSION-STATE.md` (director-ruled Option C snapshot) is a separate question and is not part of this archive.

## References

- Disposition (option iii scored winner, 35 vs 34/28/12): Wave 2 analysis `ledger-617-disposition` (goal record) + its appended correction note.
- Correction receipt: board comment `6408325035` on issue #3066.
- PR #3052 scorecard: **3/10 — do not merge; close as superseded** (Resolve Wave 1).

## Closing PR #3052 deletes nothing

PR #3052 is to be closed as superseded once this archive lands. A PR close never deletes a branch — and with these bytes now pinned on main under content-addressed blob SHAs, the continuation of record no longer depends on the branch at all. The branch itself is **not** deleted by this disposition: the "(director pass)" writer still targets it, and branch deletion is a later, separate ruling paired with stopping or re-pointing that writer (the root defect named in the #3052 scorecard).
