# lane_state.py false-OCCUPIED repair — review branch

**Branch:** `naya5/lane-state-parser-fix` · **base:** `501bf82a` (origin/main, 2026-10-12)
**Author:** Naya Kappa (TEAM lead) · **Date:** 2026-10-12 ~05:30 UTC, defect 3 added ~08:15 UTC
**Status:** review only — NO PR, NO merge press. The merge lane decides. Defect 3 marked ready for different-seat IV (dispatched separately).

## Placement note (read first)

The live tool runs at `~/workspace/naya/bin/lane_state.py` — it is **not
tracked in this repo** (verified: `git ls-files` has no lane_state.py).
This branch carries the fixed tool + its tests for review. Where the tool
should canonically live is the merge lane's decision, not this branch's.

The fix is already applied to the live copy at `~/workspace/naya/bin/`.

## The defects (both confirmed on real feed comments, 2026-10-12)

**Defect 1 — #1713: sign-out failed to close its own sign-in.**
Sign-out `6118133539` (`## [VALIDATOR sign-out | 2026-10-12 05:12 UTC]`)
classified correctly as SIGNOUT, but its seat (`validator sign-out`) matched
no open claim — the sign-in's seat was `validator sign-in`. The fallback
("closes earliest open claim") then closed an older BUILDER claim from
04:35Z, leaving the validator's own sign-in `6118073828` open → false
OCCUPIED → a worker stood down on a wrongly-OCCUPIED lane.
Root cause: the claim-role marker (`sign-in`/`sign-out`) was baked into the
seat segment, so a role's sign-out could never match its sign-in.

**Defect 2 — #1715: readiness receipt parsed as a live sign-in.**
Naya Alpha's forward-header machine-gate readiness receipt `6118129535`
(`## [NAYA ALPHA · LEARN | FORWARD-HEADER MACHINE GATE — readiness receipt …]`)
has no sign markers in its header, but its body describes sign-in/out
mechanics ("FAILS any sign-in/out/audit/report header …"). The classifier
fell through to body-wide keyword scanning and read it as SIGNIN (with a
`Mission:` line it validated) → false OCCUPIED. Two later workers had to
hand-verify the lane was free.

**Defect 3 — #1715: sign-out closed the earliest seat-match, not the
signer's own claim.**
`determine_state` scanned open claims oldest-first for a normalized-seat
match, so a sign-out closed the EARLIEST open claim sharing its seat.
Real instance: sign-out `6118197320` (05:15:18Z, freshness worker) carries
the same normalized seat (`naya 5`) as sign-in `6117761106` (04:28:54Z,
Naya Mu's instrument build) and the signer's own sign-in `6118180575`
(05:13:30Z, freshness worker, mission byte-identical to the sign-out's).
The referee closed `6117761106` and left `6118180575` open → lane gamma
falsely attributed to the freshness worker since 05:13:30Z.
Reproduced on the real comment bodies (`repro_20261012_0707.py`,
`fixture-*.json` — this directory) before the fix; confirmed fixed after.

## The fixes (`lane_state.py`)

1. **Seat normalization** (`normalize_seat`): strips `sign-in`/`sign-out`
   markers from seat segments before matching, so `[VALIDATOR sign-out | …]`
   closes `[VALIDATOR sign-in | …]`. Generic over every ROLE — not a
   one-string patch. Unmatched-seat fallback (closes earliest) is unchanged.
2. **Header-exhaustive classification** (`claim_line_parts` + rewritten
   `classify`): precedence is (a) stand-down receipts, (b) the bracketed
   claim header, (c) the rest of the first line (covers
   `[NAYA 5 / Lane Beta] SIGN-OUT 18:55Z` shapes), (d) a bracketed header
   with no sign markers ends the search as CHATTER — the body is never
   scanned, so informational posts (readiness receipts, scorecards,
   announcements) can never count as occupancy, (e) only headerless,
   first-line-silent bodies fall back to body-wide markers (legacy).
   Sign markers outrank receipt labels (a missed claim → collision is worse
   than a missed receipt → wasted dispatch).
3. **Sign-out closes the signer's own most-recent open claim**
   (defect 3): the seat-match scan runs newest-first. A sign-out ends the
   session it belongs to, which is the signer's newest still-open claim —
   never the earliest claim that happens to share the seat. The no-seat
   fallback (closes earliest, releases the lane) is unchanged and is now
   documented in the `determine_state` docstring.

## Verification

- `test_lane_state.py`: **26/26 green** (22 pre-existing + 4 new regression
  tests: `test_signout_closes_own_most_recent_claim`,
  `test_defect3_real_fixture_closes_signers_own_claim`,
  `test_defect3_no_false_occupied_on_repaired_path`,
  `test_seatless_signout_releases_lane`).
- Real-data repro (defect 3): `repro_20261012_0707.py` loads the three real
  #1715 comment bodies — old code prints
  "sign-out 6118197320 … closes sign-in 6117761106" (exit 0, bug present);
  fixed code prints "… closes sign-in 6118180575" (exit 1, fixed).
- Full-stream A/B (203 real #1715 comments, old vs fixed code, same fetch):
  only the seat-match close-lines re-resolve; the verdict moves from
  STALE-SUSPECT on `6118180575` (wrongly open) to STALE-SUSPECT on
  `6117958252` (genuinely never signed out, since 04:50:12Z). Evidence pack:
  `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/lane-state-defect3-evidence/`.
- Live copy `~/workspace/naya/bin/lane_state.py` re-synced byte-identical
  to the proven source AFTER 26/26 green (cmp verified).

## What this does NOT claim (D32)

- It does not claim lane #1713 was free at 05:15Z — only that the parser no
  longer attributes occupancy to a signer who signed out. The remaining
  open claim (BUILDER sign-in `6117820612`, 04:35Z, never signed out) is
  real feed state; judging it abandoned is a human read, not a mechanical one.
- It does not change the unmatched-seat fallback (closes earliest open
  claim) or the 120-minute stale-lease rule.
- It does not disambiguate same-seat collisions by mission: where two
  genuinely different workers share one normalized seat, a sign-out closes
  the most-recent matching claim. Mission-descriptor matching was
  considered and rejected (sign-out missions routinely differ from sign-in
  missions — "Mission: X" vs "Mission COMPLETE: X").
- It does not move the tool's canonical home — that decision is open.
- Defect 3 is builder-complete (reproduced, fixed, 26/26 green, live copy
  synced) and marked ready for different-seat IV; IV has not happened yet.
