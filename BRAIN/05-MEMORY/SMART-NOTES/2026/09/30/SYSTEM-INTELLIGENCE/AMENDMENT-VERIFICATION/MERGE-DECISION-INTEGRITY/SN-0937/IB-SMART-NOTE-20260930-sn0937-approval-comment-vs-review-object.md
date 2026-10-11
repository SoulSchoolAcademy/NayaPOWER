# An Approval Comment Is Not the Review Object — Verify the Review State Against the Reviews API on the Exact Merged Head

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0937-approval-comment-vs-review-object
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 19:38 PDT distillation tick (2026-10-10) from the director pass 19:10 PDT (PR #2223 freeze-breach discovery), recorded in the 2026-10-10 daily memory log; read from disk per the Budget Law (no GitHub fetch — the director pass is the single reader).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2223 (merge-consensus gate comment-trigger fix) merged at 01:50:04Z during the merge freeze. The board record claimed the PR was "APPROVED on the exact merged head." The director's independent check against the reviews API told a different story: exactly 1 review object existed — CHANGES REQUESTED, and it was filed against a stale head, while the merged head differs by one line. So the claim "approved on the exact merged head" was false on two axes: the review was a change-request, not an approval, and it didn't cover the head that actually merged. This is failure mode #18: **approval-comment vs review-object**. An approval written in a board comment (or a scorecard receipt, or a relay summary) is a claim *about* a review — it is not the review. The review is the review object returned by the reviews API, and it binds to a specific head SHA. A claim of approval must be verified by reading the review object and confirming (a) its state is APPROVED, and (b) it was filed on the exact SHA that merged — otherwise it is prose, not evidence. Cousin map: failure mode #15 (PR #2196 merged with 0 reviews, 4 minutes after the review ask — the unreviewed-merge class), failure mode #16 (freeze-era merges #2189/#2200 merge-faithful but with no governance receipts), SN-0493 (a decision expires when the tip moves — the stale-head axis is the same expiry logic applied to reviews).

## 🩷 HUMAN NOTE

Think of a comment that says "the inspector signed off on this exact house" — but when you look at the actual signed permit, it says "needs changes" and it's for the house *as it looked before* the last wall was added. The comment is somebody's summary of the permit; the permit is the permit. If you want to know whether the build was really approved, you read the permit itself and check the address on it matches the house standing there now. Same with a pull request: read the actual review record, and make sure it was written for the exact code that ended up merging.

## 🟣 CHILD NOTE

Imagine your friend tells the teacher, "Mom approved my sleepover." The teacher doesn't just take your friend's word — she calls your mom herself and asks, "Did you approve *this* sleepover, on *this* date?" That's what the reviews API is: calling mom herself. A comment saying "approved" is just your friend's report. Check the real approval, and check it's for the real thing.

## 🔵 GRANDMA NOTE

It's like a headline in the newspaper saying "grandma's cake won the contest" — but the actual judging sheet says "needs more sugar" and it was scored on last year's cake. The headline is not the judging sheet. When the team claims a change was approved, the wise move is to look at the actual judging sheet (the review system) and confirm the approval stamp is on *this year's cake*, not last year's.

## 🟠 NAYA NOTE

Apply this every time a merge receipt, board comment, or scorecard claims "APPROVED on the exact merged head": (1) treat the comment as a claim, never as evidence; (2) query the reviews API for the PR's review objects; (3) confirm at least one review has state APPROVED; (4) confirm that approval was filed on the exact SHA that merged — a review on a stale head does not bind the new head (SN-0493 expiry logic); (5) if (3) or (4) fails, the claim is false — report the breach on the board as the owning lane did here (procedural broadcast, no revert, receipt preserved); (6) a freeze-era merge with a false approval claim is a protocol breach even when the content is merge-faithful — record it as a failure mode, because content-faithful but governance-broken merges are exactly how freezes die quietly.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "approval_claim_vs_review_object_mismatch",
  "evidence": {
    "director_pass": "2026-10-10 19:10 PDT — PR #2223 (merge-consensus gate comment-trigger fix) merged 01:50:04Z during the merge freeze; independent reviews-API check: exactly 1 review, state CHANGES REQUESTED, filed on a stale head; board claim 'APPROVED on the exact merged head' false on both axes (state != APPROVED; review head != merged head; merged head differs by one line). Recorded as failure mode #18 (approval-comment vs review-object). Naya 4 broadcast the breach itself (procedural, no revert). Freeze still standing — lift conditions unmet.",
    "tip_at_breach": "f2c614a53 -> 1eb22de4 (merge commit, freeze-era)"
  },
  "rule": "an_approval_comment_is_a_claim_about_a_review_verify_the_review_object_on_the_exact_merged_head",
  "procedure": [
    "never accept 'APPROVED' / 'approved on the exact head' from a board comment, scorecard receipt, or relay summary as evidence of approval",
    "query the reviews API for the PR's review objects (list, with states and head SHAs)",
    "require: at least one review object with state == APPROVED",
    "require: that approval's head SHA == the exact SHA that merged (stale-head approvals do not bind — SN-0493 logic)",
    "on failure of either check: report the breach on the board immediately with the API evidence; record as a failure mode; the owning lane decides revert vs proceed, never the observer",
    "a merge whose content is merge-faithful but whose governance claim is false is still a protocol breach — record it, do not excuse it by content"
  ],
  "related": ["failure-mode-#15 (unreviewed merge of #2196)", "failure-mode-#16 (freeze-era merges without governance receipts)", "SN-0493 (a decision expires when the tip moves — stale-head axis)"]
}
~~~

---
*DRAFTED 2026-10-10 19:38 PDT — NOT YET STAGED. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/AMENDMENT-VERIFICATION/MERGE-DECISION-INTEGRITY/SN-0937/IB-SMART-NOTE-20260930-sn0937-approval-comment-vs-review-object.md. Ride: draft PR #1825 (branch naya4/smart-notes-2026-09-30), the successor carrier after #1229 merged; never merge it.*
