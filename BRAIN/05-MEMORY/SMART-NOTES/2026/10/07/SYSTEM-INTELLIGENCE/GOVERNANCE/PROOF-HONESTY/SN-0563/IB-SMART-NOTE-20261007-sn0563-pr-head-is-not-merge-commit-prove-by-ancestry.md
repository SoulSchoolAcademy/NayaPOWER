# The PR Head Is Not the Merge Commit — Prove a Merge by Ancestry

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0563-pr-head-is-not-merge-commit-prove-by-ancestry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6043968550 ([NAYA 2][RELAY] — your packet verified against live bytes, no drift, 2026-10-07T18:12:09Z) — SoulSchoolAcademy; cross-evidence #1354 6044212954 (merge SHA == refs/heads/main verified live, 2026-10-07T18:26:56Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2 verified a relay packet against live bytes and caught her own prior note in error: `ab7f8f3f7f11` was the PR's *head*, but the merge commit was `04dff1b1`. She corrected the record publicly and proved the merge the only valid way — by confirming the merge commit as an ancestor of `main` (exactly one commit behind the tip at check time), not by comparing the head SHA to anything.

The rule: **a PR head SHA is not merge evidence.** Squash merges and merge commits replace the head SHA entirely — the head ceases to exist as the identity of what landed. Comparing a recorded head against the live tip proves nothing and misproves often. The only proof of a merge is ancestry: the merge commit must be an ancestor of `refs/heads/main` (`git merge-base --is-ancestor <merge-sha> refs/heads/main`). Verification receipts must record the merge commit, never the head, and the assertion must be ancestry, never equality.

## 🩷 HUMAN NOTE

Shawn — a small discipline we hardened tonight: when a seat says "PR #1743 merged," the proof isn't the PR's number or its branch version — it's the actual merge commit, proven to sit inside main's history. One seat caught herself citing the wrong one (the PR's branch tip instead of the merge commit) and corrected it publicly with the right proof. It's the difference between "someone said it landed" and "I can show it in the chain." Tiny, mechanical, and it kills a whole class of false "merged" claims.

## 🟣 CHILD NOTE

You want to prove your letter got into the mailbox. The stamp on the letter (the PR head) doesn't prove it — the stamp is just how it looked in your hand. What proves it is the postmark from the mailbox itself (the merge commit) showing up inside the mailbag's route log (main's history). You check the route log, not your old photo of the stamp.

## 🔵 GRANDMA NOTE

Like checking a quilt pattern. The paper pattern you cut from (the PR head) isn't the finished quilt — the stitched square that actually went into the quilt (the merge commit) is. To prove your square is in the quilt, you point to the square *in the quilt*, not wave the paper pattern. Ancestry is just that: pointing to the square inside the finished thing.

## 🟠 NAYA NOTE

Protocol for any "PR #N merged" claim: (1) resolve the merge commit SHA from the merge event (PR timeline merged event), never quote the head; (2) assert `git merge-base --is-ancestor <merge-sha> refs/heads/main` (or the refs API ancestry check) on live refs; (3) record the merge commit SHA in the receipt; (4) if the assertion fails, the claim is UNPROVEN — downgrade it, never assert "merged" from head equality, PR state labels, or memory. Squash merges always replace the head; the head is forensically dead the moment the merge lands.

## MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "DO_NO_HARM",
    "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
    "RETRIEVAL_DOES_NOT_CREATE_AUTHORITY",
    "LEARNING_DOES_NOT_CREATE_AUTHORITY",
    "PRIVATE_BY_DEFAULT_SHARED_BY_CHOICE_COLLECTIVE_BY_CONSENT_PUBLIC_BY_DECISION"
  ],
  "law": "MERGE_PROOF_BY_ANCESTRY",
  "rule": "A merge is proven only by ancestry of the merge commit inside refs/heads/main (git merge-base --is-ancestor), never by PR head SHA equality, PR state labels, or recorded head SHAs. Receipts record the merge commit, never the head.",
  "evidence": [
    "#1354 comment 6043968550 (2026-10-07T18:12:09Z — Naya 2 self-corrects: ab7f8f3f7f11 was the PR head; merge commit 04dff1b1 confirmed as ancestor of main, one commit behind tip)",
    "#1354 comment 6044212954 (2026-10-07T18:26:56Z — merge SHA == refs/heads/main verified live)"
  ],
  "raw_source_separate_from_distillation": true,
  "refines": [],
  "relates": ["SN-0402", "SN-0419", "SN-0428"],
  "proof_frontier": "Unit test: a receipt citing only the PR head fails merge-proof validation; a receipt citing the merge commit passes only with a live ancestry assertion. Negative control: squash-merged head never equals any main commit."
}
~~~
