# A Due-Announcement Must Name Its Subject — Verify the Merge's Identity on Live Bytes Before Announcing "Due"

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1141-a-due-announcement-must-name-its-subject
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE PROVE · Naya Auditor · wave 14] #2175 comment 6136142546 (2026-10-13 ~01:34Z): the 00:28Z "B-30 post-merge wiring check now DUE (merge landed)" announcement was VOIDED — its due-condition was gated on an unnamed merge, and the merge that actually moved the tip (dd6f2d92) was PR #2459 (revert of #2455 under LAW-A02), not the B-30 repair PR #2492 (still open, head cbf40b6fc5, merged_at null). All refs re-derived in-step, none inherited: tip commit message names #2459; compare cbf40b6fc5...dd6f2d92 → diverged (merge_base dbe06f9e73, ahead 7, behind 1). The B-30 wiring check is NOT due while #2492 remains OPEN. Receipt: hidden_files/auditor-wave14-b30-dueness-20261013.md.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A lane announced the B-30 wiring check was "DUE (merge landed)" — but the merge that landed wasn't the B-30 repair; it was a different PR entirely, and B-30's PR is still open. The announcement's trigger referenced "a merge" without naming WHICH merge, so it fired on the wrong one. An auditor re-derived every ref from live bytes and voided the announcement before it launched wasted work. The durable rule: **a due-announcement must name its subject — the exact PR, its expected head SHA, its expected merge commit — and verify that identity on live bytes before announcing.** An unnamed gate fires on noise; a named gate fires on truth.

## 🩷 HUMAN NOTE

Shawn — the team caught a live one tonight. A sweep announced the B-30 wiring check was "DUE (merge landed)" — except the merge that landed wasn't B-30. It was the #2459 revert. B-30's PR is still sitting open. The auditor independently re-checked every reference against the live tip and voided the announcement: the trigger had never named WHICH merge it was waiting for. From now on, no announcement goes out as "due" unless it names the exact PR, the head SHA it expects, and the merge commit it expects — checked against live bytes in that same step. Announcing on an unnamed trigger is how ghost work starts.

## 🟣 CHILD NOTE

Imagine your school announces "lunch is ready!" — but it's the OTHER class's lunch that arrived. Your class's lunch is still being cooked! The announcement never said which lunch, so everyone got excited for nothing. The fix: the announcement must say WHOSE lunch arrived — the exact name — and check that the right boxes are really on the truck before shouting. No name, no announcement.

## 👵 GRANDMA NOTE

It's like a train station announcement: "your train has arrived!" — but it's the express that pulled in, and you're waiting for the local. The announcement never said which train, so you grabbed your bags for nothing. The lesson: an announcement that doesn't name the specific thing it's announcing is worse than silence — it sends people running in the wrong direction. Name the train, check the track number, THEN announce.

## 🤖 NAYA NOTE

This is the event-subscription version of the unnamed-principle family (cf. candidate 29 / P7: re-issue briefs must cite staleness evidence). A "post-merge X is now DUE" announcement is an event-driven trigger — and event-driven triggers with underspecified subjects are false-positive factories. The wire lane's correction was correct in diagnosis but the announcement machinery still needed the fix: the gate's condition ("a merge landed") was satisfied by a merge that wasn't the subject ("the B-30 repair landed"). Two things made the auditor's correction airtight: (1) refs re-derived in-step (tip commit message names PR #2459, parents dbe06f9e73+26af8e4122; #2492 state: open, merged_at null); (2) polarity proved by counterfactual (IF #2492 had merged, the tip would name it and its head would be in the ancestry — none hold). The rule for every lane that publishes due-announcements: state the subject PR, the expected head SHA, the expected tip commit; re-derive all three live in the same step; publish only when identity matches. An announcement without a named subject is a phantom claim in disguise.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1141",
  "lesson": "a-due-announcement-must-name-its-subject",
  "rule": "No due-announcement is published unless it names the exact subject PR, the expected head SHA, and the expected merge commit, all re-derived from live bytes in the same step; a gate on an unnamed merge fires on noise.",
  "failure_class": "underspecified event trigger / false due-announcement",
  "evidence": {
    "announcement": "#2175 00:28Z sweep: 'B-30 post-merge wiring check now DUE (merge landed)' — due-condition gated on an unnamed merge",
    "voiding": "#2175 comment 6136142546 (Naya Auditor wave-14 sign-out, 2026-10-13 ~01:34Z): announcement VOIDED on live bytes",
    "live_refs": "tip dd6f2d927d, commit message 'Merge pull request #2459 from naya2/revert-2455-invalid-merge-authority', parents dbe06f9e73+26af8e4122; PR #2492 state open, merged_at null, head cbf40b6fc517937863bae9c909a394a2b2938c17",
    "polarity": "compare cbf40b6fc5...dd6f2d927d -> diverged, merge_base dbe06f9e73, ahead_by 7, behind_by 1; IF #2492 had merged the tip would name it and its head would be in the ancestry",
    "receipt": "hidden_files/auditor-wave14-b30-dueness-20261013.md (exact SHAs, comparisons, verdict)"
  },
  "repair_doctrine": "Every due-announcement carries the subject's exact identity (PR number, expected head SHA, expected merge commit) and verifies all three against live refs in the same step before publishing.",
  "related": ["candidate-29/P7 (re-issue briefs must cite staleness evidence — the same false-positive family)"]
}
```
