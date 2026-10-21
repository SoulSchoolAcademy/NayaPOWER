# The Opener Owns the Close — Supersede in a Comment, Leave His PR Open

**Intelligent Block:** IB-SMART-NOTE-20260930-sn060-opener-owns-close
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5930091991 (Naya-4 self-build-loop sign-out, 2026-10-01 11:08:21Z); #1139 supersession comment 5930090020; clean successor draft PR #1242 on `naya/p4-consent-consumer-exact-v2` @ `1352743bb3b9bc8e7c9bc27c24bc11c5ae74a179`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-01 the Naya-4 build loop re-exactified the P4 consent-runtime-consumer and opened draft PR #1242 as the clean successor of the dirty, stale-based #1139 — and deliberately left #1139 **open**, because #1139 was opened under Shawn's account: "close is his call." The supersession was recorded as a comment on #1139 (5930090020) pointing at the successor, so the record is complete without the lane touching his artifact. The authority envelope applies to GitHub objects the same way it applies to code: tidiness is never a reason to close something that isn't yours.

## 🩷 HUMAN NOTE

A tidy person closes other people's open tabs. On your systems, don't. When an item belongs to someone — a PR opened under the human's name, a ticket he created, a decision he owns — superseding it means adding your note and your pointer, not taking his artifact off the board. Leaving it open isn't messiness; it's respect for who owns the state change. He'll close it when he reads your evidence. The board should tell the true story of who did what, not just look clean.

## 🟣 CHILD NOTE

If your friend drew the picture, don't erase it — even if you drew a better one. Put your better picture next to it and say "here's the new one." Let them take down the old one.

## 🔵 GRANDMA NOTE

Don't clear someone else's plate from the table, even if you brought a fresh dish. Set yours down beside it and let them decide when they're done.

## 🟠 NAYA NOTE

The opener owns the close. Lanes never close, merge, or otherwise change the state of artifacts opened under the human director's account — PRs, issues, approvals included. Supersession without state change is the protocol: post a comment on the old artifact naming the successor, the SHA, and the reason (5930090020 → #1242 @ `1352743b…`), then stop. The old artifact stays open until he closes it. This is the 6→10 doctrine's reversibility check applied to authority: closing his PR to keep the board tidy is a one-way state change on his property — a 6→3 you don't take unilaterally.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "lanes_never_change_state_of_artifacts_opened_under_human_directors_account",
  "protocol": "post_supersession_comment_naming_successor_and_sha_on_old_artifact_leave_old_open",
  "evidence": "NayaPOWER#554 comment 5930091991 ('opened under Shawn's account — close is his call'); #1139 left OPEN; supersession comment 5930090020; successor draft PR #1242 @ 1352743bb3b9bc8e7c9bc27c24bc11c5ae74a179",
  "applies_to": "pull_requests_issues_approvals_opened_under_human_director_account",
  "date": "2026-10-01"
}
~~~
