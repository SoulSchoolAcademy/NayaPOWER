# Coverage-Gap Handoff — Name the Uncovered Head, Pass the Baton

**Intelligent Block:** IB-SMART-NOTE-20260930-sn046-coverage-gap-handoff
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:45 PDT distillation tick (2026-10-01) from #554 comment 5927667437 ([NAYA 2][RELAY] — #1232 amendment verified live at PR head, 2026-10-01 08:26 UTC).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Verify coverage is pinned to a commit, not to a branch — so every head move opens a coverage gap, and that gap must be named out loud, not left for someone else to discover. Between Naya 2's 01:25 PDT nine-node verify (head `cf62b761`, 474/474 green) and her 01:35 PDT relay post, `naya4/nine-node-kernel-v1` moved one more commit to `bd8fda27` ("HARDEN: remove committed .pytest_cache from the branch tree (candidate)" — committed by Shawn). The new commit was small and benign, which is exactly when gaps go silent: nothing broke, so nobody flags it, and the branch quietly runs for hours with its last *signed* verification one commit behind the head. Naya 2 did the correct thing: she stated the new head, stated that the verify watch's last signed result covers only `cf62b761`, marked `bd8fda27` explicitly **uncovered**, and handed the baton to the watch's lane. The gap was closed the same tick (tick 36 ran 1014 passed, 3 skipped on `bd8fda27`), but the discipline is what matters: the handoff was explicit before the re-verification happened. The rule: when a head moves past your last verified ref, the correct post is "head X is uncovered, baton passed" — never silence, never "it's just a small commit, surely still green," and never a fresh assertion of coverage without a run.

## 🩷 HUMAN NOTE

Think of a building inspector signing off on a house, and then the owner adds a new room overnight. The inspector's certificate covers the house as it was — not the new room. The right move isn't to pretend the room doesn't need inspection, or to guess it's fine because it looks small. It's to say, "the new room isn't covered yet; the inspector needs to come back." That's what this handoff was: the branch gained a commit, the last verified report no longer covered the head, and the gap was announced instead of assumed away.

## 🟣 CHILD NOTE

The referee said the game was fair — then one more player joined the field. The referee's whistle doesn't cover the new player. Tell everyone there's a new player who hasn't been checked yet, and hand the whistle to the referee.

## 🔵 GRANDMA NOTE

It's like approving a cake recipe and then someone adds a pinch of something new to the batter. The approval was for the old recipe. You don't pretend the new pinch was in the original — you note it plainly and check the new cake. The pinch turned out fine, but you only know that *after* you checked.

## 🟠 NAYA NOTE

Make coverage-gap handoffs mechanical: (1) treat every verification result as pinned to its commit — a "GREEN" badge on a branch name is a lie; only a ref can be green; (2) when you observe a head move past your last verified ref (even by one hygiene commit, even by Shawn), post the move, name the new head, and state plainly that it is uncovered; (3) hand the baton to the lane that owns verification — don't re-verify someone else's lane as a side quest, and don't leave the gap unassigned; (4) never wave a head through on "small and benign" — the smaller the commit, the more tempting the silent wave, and the discipline exists precisely for those; (5) note the gap on the board even if you expect it closed within the hour — the board record must never show an uncovered head that nobody mentioned.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "silent_coverage_gap_after_head_move",
  "evidence": {
    "board_comment": "5927667437 — [NAYA 2][RELAY] — #1232 amendment verified live at PR head (2026-10-01 08:26 UTC)",
    "last_signed_result": "nine-node verify at cf62b761, 474 passed, 0 failed (01:25 PDT, comment 5927643989)",
    "head_move": "cf62b761 → bd8fda27 (+1: 'HARDEN: remove committed .pytest_cache from the branch tree (candidate)', by Shawn)",
    "handoff": "bd8fda27 explicitly marked uncovered; baton passed to the verify watch's lane",
    "closure": "tick 36 verified bd8fda27 (1014 passed, 3 skipped) — gap closed after the handoff, not instead of it"
  },
  "rule": "coverage_gap_handoff_name_uncovered_head_pass_baton",
  "procedure": [
    "pin every verification result to its commit; a branch name is never green",
    "on any head move past the last verified ref, post the move and name the new head as uncovered",
    "hand the baton to the lane that owns verification; never leave the gap unassigned",
    "never wave through small or benign commits without a run",
    "record the gap on the board even when closure is expected soon"
  ],
  "related": ["SN-036 (push-run CI evidence completeness)", "SN-043 (compare at ONE commit)", "SN-017 (asserted ≠ verified)"]
}
~~~
