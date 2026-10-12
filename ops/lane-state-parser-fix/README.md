# lane_state.py false-OCCUPIED repair — review branch

**Branch:** `naya5/lane-state-parser-fix` · **base:** `501bf82a` (origin/main, 2026-10-12)
**Author:** Naya Kappa (TEAM lead) · **Date:** 2026-10-12 ~05:30 UTC
**Status:** review only — NO PR, NO merge press. The merge lane decides.

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

## Verification

- `test_lane_state.py`: **22/22 green** (16 pre-existing + 6 new regression
  tests: `test_validator_signout_closes_validator_signin`,
  `test_seat_normalization_sibling_variants`,
  `test_readiness_receipt_is_not_a_claim`,
  `test_bracketed_header_without_markers_is_informational`,
  `test_sign_marker_outside_brackets_still_claims`,
  `test_signout_header_family`).
- Real-data repro: defect 1 reproduced on the full #1713 comment window
  (false OCCUPIED by `6118073828` at 05:15Z) and confirmed fixed (sign-out
  `6118133539` now closes sign-in `6118073828`); defect 2 reproduced
  (`6118129535` → OCCUPIED) and confirmed fixed (→ CHATTER, pair → FREE).
- Classification distribution over 49 real #1713 comments: 22 SIGNIN /
  22 SIGNOUT / 3 STANDDOWN / 2 CHATTER — every real claim still classified
  correctly; only the two defect shapes changed outcome.

## What this does NOT claim (D32)

- It does not claim lane #1713 was free at 05:15Z — only that the parser no
  longer attributes occupancy to a signer who signed out. The remaining
  open claim (BUILDER sign-in `6117820612`, 04:35Z, never signed out) is
  real feed state; judging it abandoned is a human read, not a mechanical one.
- It does not change the unmatched-seat fallback (closes earliest open
  claim) or the 120-minute stale-lease rule.
- It does not move the tool's canonical home — that decision is open.
