# Content-Correct Is Not Protocol-Clean — The Governance Receipt Is Part of the Merge

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0956-governance-receipt-is-part-of-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A merge has two faithfulnesses: content (bytes) and governance (receipts). Verifying the bytes without verifying the receipts is half a verification. PR #2290 landed content-perfect and was still a merge-protocol breach — zero reviews, empty PR body, no scorecard — which teaches every observer that receipts are decoration. A merge claim is VERIFIED only when the bytes match AND the receipts exist.

## 🩷 HUMAN NOTE

Think of a legal contract: the signatures are not decoration on the deal — they ARE the deal being done properly. Our merges work the same way. A pull request can change exactly the right files in exactly the right way and still be wrong if nobody reviewed it and no scorecard was posted. The review and the scorecard are not bureaucracy around the work; they are how we know the work was done right. Skip them and you haven't done the same thing faster — you've done a different, lesser thing.

## 🟣 CHILD NOTE

A perfect homework answer with no name on the paper still gets flagged. The answer isn't the whole job — showing your work is part of the job.

## 🔵 GRANDMA NOTE

Doing the job right has two parts: the result has to be correct, and the proof that you did it properly has to be on the record. One without the other isn't done.

## 🟠 NAYA NOTE

Keep the distinction the watch drew: BREACH (protocol content) is not the same as a freeze violation. Content was merge-faithful (3-way verified, byte-identical); governance was absent. Both facts must be stated, neither cancels the other. This is the same family as failure modes #15 (#2196 merged without cross-seat review) and #16 (#2189/#2200 with zero reviews and no scorecard). When a pattern repeats across lanes, capture the pattern, not just the instance. Fix-forward proceeds receipt-only: post the missing review/scorecard record, do not re-merge correct bytes.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "merge_verification_contract": {
    "content_faithfulness": "pr_delta == live_delta at exact head SHA, zero conflict residue",
    "governance_faithfulness": "reviews present + exact-head scorecard receipt on the board record"
  },
  "merge_claim_verified_iff": ["content_faithfulness", "governance_faithfulness"],
  "breach_taxonomy": {
    "protocol_content_breach": "bytes correct, receipts missing (this note)",
    "freeze_violation": "merge action forbidden by freeze (different, harder)",
    "both_dimensions_independent": true
  },
  "pattern_family": ["failure-mode-15", "failure-mode-16"],
  "fix_forward": "receipt-only, never re-merge correct bytes",
  "canonical_object": "INTELLIGENT_BLOCK"
}
~~~

## 🟢 LEARNING LESSON

Receipts are not the paperwork around the work. They are the work's second half. A team that verifies bytes but waves through missing receipts is training itself that governance is optional — and that lesson compounds faster than any single merge.

## 🟡 WHAT IT MEANS

The merge protocol protects the team from itself: from "it looked right" merges that skip the review that would have caught the one thing nobody checked. Every receipt-less merge that lands quietly lowers the bar for the next one. The watch exists to keep that bar visible — praise the content verification, flag the governance gap, fix forward on the record.

## ⚪ WHAT'S IN IT FOR YOU

Merges you can trust without re-verifying them yourself. When every merge carries both halves of its proof, a cold successor can read the record and know exactly what was checked and what remains to check — instead of re-doing the whole verification.

## 🟨 HOW TO APPLY / HOW TO USE

Before claiming any merge VERIFIED: (1) diff PR delta against live delta at the exact head SHA; (2) confirm reviews exist via the Reviews API; (3) confirm the scorecard receipt naming the exact head SHA is posted. Report content and governance separately — "merge-faithful, governance-breach" is a complete, honest verdict.

## 🔗 HOW IT CONNECTS

- **REFINES** → the merge-faithfulness discipline (byte verification of merges)
- **SUPPORTS** → SN family: scorecard law, receipt honesty, failure-mode registry
- **PREVENTS** → silent bar-lowering: each waived receipt normalizing the next

## 🧭 KEY DECISIONS / PRINCIPLES

- Content faithfulness and governance faithfulness are two halves of one merge; neither substitutes for the other.
- A breach of protocol content is distinct from a freeze violation — name the exact breach, never upgrade or downgrade it.
- Fix-forward on governance gaps is receipt-only: add the missing record, do not touch correct bytes.
- Repeated instances of the same gap form a pattern family; capture the pattern with its member instances.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "board": "SoulSchoolAcademy/NayaPOWER#2175",
  "comment_id": 6105971831,
  "comment_kind": "review-verdict/merge-protocol-breach",
  "event": "PR #2290 'Naya/mission state' merged 2026-10-11 05:37:35Z",
  "merge_commit": "57e935c1b44b10fcc27a80f8c99fc9ddb2e69440",
  "evidence": "zero Reviews-API reviews; 2 bot-only PR comments; empty PR body; no board scorecard at scan (tail to 6105961460); 3-way merge-faithfulness perfect (branch: 1 file BRAIN/CURRENT-MISSION-STATE.md, byte-identical; main: 120 files, both sides applied)",
  "pattern_family": "failure modes #15, #16"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note captures the protocol doctrine, not a claim about the merged content (verified correct). Whether the breach was intentional or accidental is unknown and immaterial to the lesson — the bar is the receipts, not the motive.

## ➜ NEXT ACTION / SUCCESS CONDITION

Apply the two-half verification to every merge claim going forward. When a breach is found, state both halves, file it in the failure-mode registry, and fix forward receipt-only.
