# Dead URL on Main Is Not Lost Content — Check the Unmerged Recovery Branches First

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0499-dead-url-not-lost-content
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-06 Naya 5 reported two dead document URLs on main and asked where the content went. The content was never lost: both documents were wiped by the 2026-09-26 reset commit (`b31f37fd`), then recovered byte-identical on branch `origin/brain-build/recanonicalize-dead-docs-20261001` (commit `b5b416145`, blobs `422229fb67d0` and `751d32e7e614` — one with a recovery banner marking it historical synthesis, not ratified contract) — but that branch was never merged, its own commit message deferring to the human director's gate. The URLs are dead on main because the restoration never merged, not because the content is gone. The lesson for any cold successor facing a "missing" document: before declaring content lost, enumerate unmerged recovery branches and verify blobs by hash against git history. Recovery without merge is storage, not restoration.

## 🩷 HUMAN NOTE

"Missing" and "lost" are different things. When someone says a document is gone, your first question should be: "gone from where?" A thing that was saved but never put back on the shelf isn't lost — it's waiting. Check the rescue piles before you grieve the loss.

## 🟣 CHILD NOTE

If you can't find your toy in your room, check the lost-and-found box before crying. Someone may have already found it — it just never got put back.

## 🔵 GRANDMA NOTE

Don't say it's lost until you've checked everywhere it might have been put. There's a difference between something disappearing and something sitting in a box waiting to be shelved.

## 🟠 NAYA NOTE

A dead URL on main proves absence from main, nothing more. Diagnosis order: (1) was the document ever on main — check the commit that removed it; (2) does it survive elsewhere — enumerate unmerged branches, verify blobs byte-identical by hash, note any recovery banners about its authority state; (3) only then decide: the fix is a merge (a human gate), not a rewrite. Recovered-but-unmerged is not lost — rewriting what already exists in history creates the duplicates the registry is built to reject. The recovered banner on the contracts doc is load-bearing: recovered content keeps its original authority state (historical synthesis ≠ ratified contract) — merging restores the file, not its authority.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "dead_url_on_main_is_not_lost_content_check_unmerged_recovery_branches_first",
  "diagnosis_order": "removal_commit_then_unmerged_branch_enumeration_then_hash_verified_blobs_then_merge_decision",
  "hard_rule": "recovery_without_merge_is_storage_not_restoration_rewriting_recovered_content_creates_duplicates",
  "authority_note": "recovered_content_keeps_original_authority_state_recovery_banner_is_load_bearing",
  "case_evidence": "reset b31f37fd wiped 2026-09-26, recovery b5b416145 on origin/brain-build/recanonicalize-dead-docs-20261001 never merged, blobs 422229fb67d0 and 751d32e7e614 byte-identical",
  "evidence": "NayaPOWER#1354 comment 6026780919 (Naya 4, 2026-10-06)"
}
~~~
