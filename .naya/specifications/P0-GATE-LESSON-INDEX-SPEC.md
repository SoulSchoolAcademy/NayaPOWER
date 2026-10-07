# SN-0460 "Index the Lesson" — Enforcement Gate Spec V1

## Law

Captured ≠ retrievable. A captured Smart Note that has no index entry or
cannot be retrieved by the retrieval corpus is NOT LEARNED. It is archived.

## Numbering note (honest)

The 2026-10-06 digest labeled this law "SN-0460", but the canonical SN-0460
on main is `IB-SMART-NOTE-20261006-sn0460-ratified-predecessor-guard`
(a truth-state guard). This is a digest numbering collision of the same
class as the earlier SN-0501 collision. This gate enforces the LAW
(the principle), cited by its text until the collision is resolved.
It does not claim the SN-0460 number.

## What the gate checks

For a given Smart Note (by SN id):

| Check | What | Fail means |
|---|---|---|
| I1 | Lesson-index entry present AND retrieval-ready: `content.title` / `essence` / `lesson` non-empty (weight-A), `applicable_scope` non-empty (weight-B), `disposition` set; GATE dispositions must name a `falsifier` | captured but unindexed → NOT LEARNED |
| I2 | An intelligent block in `nayanet_intelligent_blocks` references the SN (servable status) | captured but not corpus-present → NOT LEARNED |
| I3 | The note's core terms live in retrieval-weighted fields (A: title/essence/summary, B: lesson/applicability), matching the cold-retrieve migration's weighting contract | unretrievable by ranked query |

Index sources (priority order):
1. `.naya/index/lesson-index-20261006.json` (the 43 triaged notes; on branch
   `naya5/lesson-index-20261006` until its PR merges, then main)
2. `.naya/memory/smart-notes/index.json` (projection index, older notes)

## Modes

- `repo` (default): I1 + I3 against the index entry. CI-safe, stdlib only,
  no credentials. This is the mode that runs in CI.
- `corpus`: adds I2 via `--corpus-json` (a dump) or `--corpus-live`
  (read-only sb-api skill, targeted ILIKE probe — never full-table scan).

## Exit codes (drift-tripwire pattern)

- `0` — PASS (indexed and retrievable)
- `1` — FAIL (not learned; names the failing check)
- `2` — usage or infrastructure error (including unreachable corpus —
  never a silent pass)

## Empirical state at build time (2026-10-07)

- I1 sweep over the 43 digest notes against the lesson index: **43/43 PASS**.
- I2 sweep: **0/43 corpus-present** — the notes are indexed but no
  intelligent-block rows exist in the live DB yet. Loading them is a
  production DB write: the Director's gate.
- Old projection index: 40/43 digest SNs missing (expected — the lesson
  index supersedes it for these notes).

## CI wiring (proposed, not yet merged)

- `repo` mode on PRs touching `.naya/index/**` or `BRAIN/05-MEMORY/SMART-NOTES/**`:
  every new/changed SN must pass I1+I3.
- `corpus` mode on a schedule (read-only skill): every indexed SN must pass I2;
  failures open a tracking issue, they do not page anyone at 3am.

## Honest limits

- I3 is a static weighting-contract check, not a live ranking proof. True
  retrieval proof needs the corpus loaded and a query run (the cold-retrieve
  PR #1665 path, post-merge).
- The gate cannot verify that a retrieved lesson actually changed behavior —
  that is #1602's compounding track, not this gate.
- Re-index discipline (keeping the lesson index current as new notes land)
  is enforced by CI wiring, not by this script alone.

## Score

8.5/10 — gate built, falsifiers green (7/7), empirically validated against
the real index and live corpus, staged on a branch, nothing touched main.
−1.5: corpus loading is a pending Director gate; CI wiring proposed not merged.
