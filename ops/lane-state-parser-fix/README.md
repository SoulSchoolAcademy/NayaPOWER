# lane_state.py false-OCCUPIED repair — review branch

**Branch:** `naya5/lane-state-parser-fix` · **base:** `501bf82a` (origin/main, 2026-10-12)
**Author:** Naya Kappa (TEAM lead) · **Date:** 2026-10-12 ~05:30 UTC, defect 3 added ~08:15 UTC, defect 4 added ~11:15 UTC
**Status:** review only — NO PR, NO merge press. The merge lane decides.
Defect 3 received different-seat IV ACCEPT 9.5 at 09:06Z (live copy
byte-identical 8190ac15…); defect 4 dispatched as its suspected sibling.

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

**Defect 4 — #1713: seatless sign-out closed the EARLIEST open claim,
not the signer's own.**
Suspected sibling of defect 3, found in Kappa's own domain. Sign-out
`6121753742` (09:45:14Z, `[SIGN-OUT] learn-convergence-builder` — the
bracketed header holds only the role marker, which `normalize_seat`
strips to `None`, so the parser read it as seatless) fell into the
"names no matching seat" fallback and closed the EARLIEST open claim
`6121713676` (09:42:32Z, Naya Alpha's compound observation) instead of
the signer's own most-recent open claim `6121747521` (09:44:49Z, the
exercise's sign-in). Net effect: Alpha's worker lost its claim to
another seat's sign-out and never folded; the exercise's claim stayed
open as a ghost. Reproduced on the real comment bodies
(`repro_20261012_1115.py`, `fixture-61217*.json`) before the fix;
confirmed fixed after.

**Defect 4b — same file: named-but-unmatched sign-out dethroned the
occupant.**
The old fallback also fired for a sign-out that NAMED a seat with no
open claim, closing the earliest open claim — the same misfire shape
(defect 3's own rule says a sign-out closes *the signer's own*
most-recent claim; closing the occupant's instead is claim theft).
Fail-closed: such sign-outs follow the same LIFO rule as seatless
ones (fix 5) — never the §6 occupant while rivals stand. A/B evidence
on the full #1713 stream showed "close nothing" would have been wrong
here: `6120647358` (**[Naya Epsilon — VERIFY] SIGN-OUT**, seat
`naya epsilon — verify`, no matchable seat on the claim) legitimately
released `6120277769`; closing nothing ghosted it into a false
STALE-SUSPECT.

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
   never the earliest claim that happens to share the seat.
4. **Seatless sign-out attributes to the newest open claim** (defect 4):
   sessions end LIFO, and the comment's posted time decides — so a
   sign-out with no attributable seat closes the NEWEST open claim. This
   can never dethrone the §6 earliest-wins occupant while rivals stand
   (with a single open claim the attribution is unambiguous). Closing
   nothing instead would strand legitimate headerless-style sign-outs
   and ghost their claims until the 120-minute lease dies.
5. **Unattributable sign-out attributes to the newest open claim**
   (defect 4b): a sign-out naming a seat with no open claim follows the
   same LIFO rule as a seatless sign-out — the old code closed the
   earliest open claim here, handing the lane to a seat that never held
   it. One unified rule: an unattributable sign-out can never dethrone
   the §6 occupant while rivals stand.

## Verification

- `test_lane_state.py`: **29/29 green** (25 pre-existing incl. all defect-3
  pins + 4 new regression tests: `test_seatless_signout_closes_newest_not_earliest`,
  `test_seatless_signout_single_claim_frees`,
  `test_named_signout_without_open_claim_closes_newest`,
  `test_defect4_real_fixture_seatless_closes_signers_own_claim`).
  The old `test_seatless_signout_releases_lane` pinned the defective
  behavior (close-earliest) and was rewritten — its old expectation WAS
  defect 4.
- Real-data repro (defect 3): `repro_20261012_0707.py` loads the three real
  #1715 comment bodies — old code prints
  "sign-out 6118197320 … closes sign-in 6117761106" (exit 0, bug present);
  fixed code prints "… closes sign-in 6118180575" (exit 1, fixed).
- Real-data repro (defect 4): `repro_20261012_1115.py` loads the three real
  #1713 comment bodies (`fixture-61217*.json`) — old code prints
  "sign-out 6121753742 … closes sign-in 6121713676" (exit 0, bug present);
  fixed code prints "… closes sign-in 6121747521" (exit 1, fixed).
- Full-stream A/B (389 real #1713 comments, old vs fixed code, same fetch):
  OLD verdict FREE was built on claim-theft closes (incl. the 09:45Z
  misfire). NEW verdict FREE is built on legitimate closes only:
  `6120647358`→`6120277769` (LIFO, sole open claim — verified against the
  real bodies: Epsilon's sign-out legitimately releasing Epsilon's claim),
  Alpha's three seat-matched closes (`6120817444`→`6120714606`,
  `6121327773`→`6121232104`, `6121531162`→`6121407628`),
  `6121753742`→`6121747521` (defect-4 fix), `6122593052`→`6121713676`
  (LIFO, sole open claim), `6123174327`→`6123122873` (seat match).
  No close line in the new walk dethrones the §6 occupant while rivals
  stand. The "close nothing" alternative for named-unmatched was tested
  in the A/B and rejected: it ghosted the legitimate `6120647358`
  release into a false STALE-SUSPECT.
- Full-stream A/B (203 real #1715 comments, old vs fixed code, same fetch):
  only the seat-match close-lines re-resolve; the verdict moves from
  STALE-SUSPECT on `6118180575` (wrongly open) to STALE-SUSPECT on
  `6117958252` (genuinely never signed out, since 04:50:12Z). Evidence pack:
  `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/lane-state-defect3-evidence/.
- Live copy `~/workspace/naya/bin/lane_state.py` re-synced byte-identical
  to the proven source AFTER 29/29 green (sha256 verified).

## What this does NOT claim (D32)

- It does not claim lane #1713 was free at 05:15Z — only that the parser no
  longer attributes occupancy to a signer who signed out. The remaining
  open claim (BUILDER sign-in `6117820612`, 04:35Z, never signed out) is
  real feed state; judging it abandoned is a human read, not a mechanical one.
- It does not change the 120-minute stale-lease rule.
- Defect 4 DOES change the unattributable-sign-out fallback (was: closes
  earliest open claim; now: closes newest open claim, LIFO). The old
  behavior is preserved nowhere — it was the defect.
- It does not authenticate signers: any comment classifying as SIGNOUT is
  trusted as a sign-out. Attribution is by seat match, then LIFO; a
  hostile or stray sign-out with a single open claim still releases the
  lane, exactly as before this fix. Signer authentication is out of
  scope for a comment-stream referee.
- It does not touch `cmd_verify`'s closed-check, which still treats ANY
  later SIGNOUT as closing an earlier sign-in (coarse claim-minute
  heuristic). Under the new attribution that check can read optimistic;
  the error direction is bounded by the §6/§7 collision protocol (a
  wrongly-WON claimant gets a collision note and owes a stand-down).
  Aligning it with the walk's attribution is open future work.
- It does not disambiguate same-seat collisions by mission: where two
  genuinely different workers share one normalized seat, a sign-out closes
  the most-recent matching claim. Mission-descriptor matching was
  considered and rejected (sign-out missions routinely differ from sign-in
  missions — "Mission: X" vs "Mission COMPLETE: X").
- It does not move the tool's canonical home — that decision is open.
- Defect 3 is builder-complete (reproduced, fixed, 26/26 green, live copy
  synced) and received different-seat IV ACCEPT 9.5 at 09:06Z. Defect 4
  is builder-complete (reproduced, fixed, 29/29 green); live copy sync
  and different-seat IV are the next steps.
