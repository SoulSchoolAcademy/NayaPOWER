Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A clean receipt proves the process ran — it does not prove the tree is healthy. #3017 carried a valid merge receipt and still regressed the manifest: the SN-1854 re-stamp committed the registry index without the manifest, and the receipt's merge-time checks never looked at the tree the merge actually produced. The rule: when the tree regresses, don't close the case on a clean receipt — re-inspect the tree. Receipts certify the process; the artifact needs its own inspection.

## 🩷 HUMAN NOTE

Shawn — a merge went through with a perfectly valid receipt, and it still broke the manifest. The receipt checked the process at merge time, but nobody checked the tree the merge actually produced — and the tree was wrong. The lesson: the paperwork being clean doesn't mean the work is right. From here on, when a tree regresses, we go look at the tree itself — the receipt doesn't get to close the case.

## 🟣 CHILD NOTE

Imagine you bake a cake and your teacher checks your recipe card — every step followed, card looks perfect. But the actual cake in the oven is burnt. The card says the process was right; the cake says otherwise. The rule: when the cake tastes wrong, you taste the cake — you don't re-read the card and declare it fine. The receipt is the recipe card. The tree is the cake.

## 🔵 GRANDMA NOTE

The paperwork said the surgery went perfectly — every checklist box ticked. But the patient was worse afterward, because the paperwork checked the procedure and nobody checked the patient. That's this lesson: a clean checklist proves the process was followed, not that the outcome is healthy. When something is wrong, you examine the patient — the tree — not the paperwork. The receipt is the checklist. The tree is the patient.

## 🟠 NAYA NOTE

The failure mode this kills: treating a valid receipt as a tree-health certificate and closing a regression investigation on it. Director tick 2026-10-23 ~20:00Z (board #2793 1,893→1,905): the WIRE run's cleared-14 MANIFEST_STALE regression was root-caused to #3017 — a merge with a valid receipt that regressed the manifest, because the SN-1854 re-stamp committed the registry index without the manifest, and the receipt's checks validated merge-time process, not the post-merge tree. Mechanism: a receipt is a certificate that a process ran against its criteria at a moment in time; the tree is the artifact the process produced — and artifacts can be wrong even when the process was followed, because the criteria never inspected the artifact's actual state (here: the manifest bytes in the merged tree). The future decision this changes: when a seat root-causes a tree regression, the investigation includes a post-merge tree inspection (manifest hash re-derived from the merged tree's bytes) alongside the receipt — a clean receipt is evidence about the process, never a verdict on the tree, and never closes a tree-health question. It would be proved wrong if the #3017 regression were shown to have come from a different commit than the receipted merge — i.e., the check is the pin: the regression must be pinned to the receipted merge's tree for the lesson to hold, and it was (registry index committed without manifest in the #3017 tree). Cousins: the evidence law (receipt proves process, not outcome); WIRE verification re-derives from bytes, not from claims — this is its merge-receipt form; CANDIDATE 888 (pin-comparison doctrine: re-run verdicts only as honest as their pins) — a receipt is only as honest as what it pins.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1912-receipt-clean-is-not-tree-clean",
  "lesson": "A valid merge receipt proves the process ran — not that the tree is healthy. #3017 carried a valid receipt and still regressed the manifest (the SN-1854 re-stamp committed the registry index without the manifest; the receipt's merge-time checks never inspected the produced tree). When a tree regresses, the investigation must re-inspect the tree (manifest hash re-derived from the merged tree's bytes); a clean receipt is evidence about the process, never a verdict on the tree, and never closes a tree-health question.",
  "applies_when": ["merge", "receipt", "manifest", "tree-health", "regression", "root-cause", "proof-honesty", "failure:regressed-manifest", "evidence-discipline"],
  "enforcement": "Any tree-regression root-cause must include a post-merge tree inspection (manifest hash re-derived from the merged tree's bytes) alongside the receipt review — a clean receipt alone never closes the case. WIRE verification and any manifest-health claim must re-derive from bytes, never from the receipt's assertions.",
  "evidence": [
    "Director tick 2026-10-23 ~20:00Z (board #2793 1,893->1,905): WIRE 6376091967 root-cause — 'cleared-14 MANIFEST_STALE regressed to #3017's SN-1854 re-stamp committing the registry index without the manifest (receipt-clean ≠ tree-clean)'; breach log 39 -> 48; #3017 receipt was valid",
    "hidden_files/live-plan.md — NAMED FAILURE MODE 'RECEIPT-CLEAN != TREE-CLEAN' (2026-10-23 22:38Z): '#3017 had a valid receipt and still regressed the manifest — receipt proves process, not tree health'"
  ]
}
```
