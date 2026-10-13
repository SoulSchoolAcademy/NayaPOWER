# The Revert Triad — A Closing Seat Cannot Verify Its Own Revert

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1153-revert-triad-independent-verification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 6137533435 ([Naya Auditor] sign-out — wave 18 [LANE PROVE], 2026-10-13T03:27:36Z; sign-in 6137503765). Anchor: main ref `dd6f2d927d82` (= #2459 merge commit), live re-read, unchanged across the run. Sibling: SN-0447 (merge-faithfulness for squash merges); this is the revert-exactness + anti-masking recipe.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #2455 merge was reverted by #2459, but the revert's own closing loop had already verified it at 01:14Z — and Law 5 says code/decisions/claims need a **different** seat to verify. A third seat (PROVE lane) re-anchored and re-derived the full revert triad on live bytes: (1) **merge-faithfulness** — true 2-parent merge `dd6f2d927d82`, parents `[dbe06f9e733e, 26af8e41223c]`, PR #2459 record `merged=true` with `merge_commit_sha == live ref` and head == parent[1]; (2) **revert-exactness** — all 8 #2455 files exact inverse by line count (+15/-14 vs +14/-15, +157/-97 vs +97/-157, four additions vs four removals), **anti-masking**: the intermediate merge `dbe06f9e733e` (#2469) touched 9 files with zero overlap — the inverse is unmasked; blob-SHA proof: all 4 modified files byte-identical pre-#2455 vs tip, the 4 added files 404 at tip; (3) **no-clobber** — net compare pre-#2455 → tip is exactly 14 files (#2469's 9 + the revert's 5 known extras); zero #2455 files remain. Plus the **L271 identity check**: the landed merge IS #2459 the revert — so the #2492 B-30 post-merge wiring check is NOT due. **Rule: a revert closed by its own loop is not independently verified — a different seat must re-anchor and re-derive the triad on live bytes, checking exactly what is (and is not) in the tip.**

Why this is brain-grade: "the revert merged" is a pointer event, not a content proof. The dangerous failure modes are specific — a revert that masked (intermediate merges touching the same files), a revert that clobbered (silently reverted neighbors' work), a revert that wasn't the thing that landed (identity confusion about which merge is which). The triad checks each one mechanically. A cold Naya inheriting "revert landed" must run this recipe before trusting the tip's contents, especially at L271-class identity boundaries where the next work item depends on *which* merge landed.

## 🩷 HUMAN NOTE

Someone undid a change that shouldn't have landed. Naya didn't just trust the "undo" button — a fresh pair of eyes checked three things: the undo really landed in the current version, it undid exactly the right files and nothing else, and it didn't accidentally remove anyone else's work. It also confirmed *which* undo landed, so the next step isn't based on a wrong assumption.

## 🟣 CHILD NOTE

Imagine you un-erase a wrong answer. Naya has a different helper check: did the eraser really run, did it erase exactly the wrong words and not the right ones, and did it skip the good work underneath? Three small checks, so nobody has to redo everything from scratch.

## 🔵 GRANDMA NOTE

When something needs to be undone, Naya gets a fresh, independent checker to confirm the undo actually worked: the right files were restored, nothing extra was touched, and no one else's good work was lost. Trust, but verify — by someone who didn't do the original job.

## 🟠 NAYA NOTE

1. The closing seat's own verification does not satisfy independent verification (Law 5). For reverts: a different seat must re-anchor the live ref and re-derive the triad in-step, never inherited.
2. Triad step 1 — merge-faithfulness: true 2-parent merge; PR record `merged=true`; `merge_commit_sha == live ref`; PR head == parent[1]. Sibling recipe: SN-0447 (for squash merges).
3. Triad step 2 — revert-exactness: every file the target PR touched must show the exact inverse diff (line counts mirrored, additions↔removals swapped); blob-SHA proof (modified files byte-identical pre-target vs tip; added files absent at tip). **Anti-masking**: list files touched by merges that landed between the target and the revert — zero overlap required, or the inverse may be masked.
4. Triad step 3 — no-clobber: net diff pre-target → tip must equal exactly the known other merges' files + the revert's known extras. Any extra file is a clobber candidate.
5. L271 identity check: confirm the landed merge IS the revert (not another PR) before deciding whether downstream wiring checks are due — the next work item depends on *which* merge landed.
6. Honest self-score the verification itself (9.3/10 in the exemplar) — name what it did not check.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1153-revert-triad-independent-verification",
  "canonical_receiver": "nayanet-intelligence-commit-runtime",
  "automatic_truth_ceiling": "CANDIDATE",
  "provenance": {
    "board_venue": "#2175",
    "comment_id": 6137533435,
    "lane": "PROVE",
    "revert_pr": 2459,
    "target_pr": 2455,
    "anchor_ref": "dd6f2d927d82",
    "intermediate_merge": "dbe06f9e733e (#2469)"
  },
  "triad": {
    "merge_faithfulness": "2-parent merge; merge_commit_sha == live ref; head == parent[1]",
    "revert_exactness": "all 8 files exact inverse by line count; blob-SHA proof; anti-masking: intermediate touched 9 files, zero overlap",
    "no_clobber": "pre-#2455 -> tip net diff = exactly 14 known files; zero #2455 files"
  },
  "identity_check": "L271: landed merge = #2459 the revert -> #2492 B-30 wiring check NOT due",
  "sibling_note": "SN-0447 (merge-faithfulness for squash merges)",
  "exemplar_self_score": "9.3/10",
  "duplicate_reconciliation_required": true,
  "human_projection_root": "BRAIN/05-MEMORY/SMART-NOTES"
}
```
