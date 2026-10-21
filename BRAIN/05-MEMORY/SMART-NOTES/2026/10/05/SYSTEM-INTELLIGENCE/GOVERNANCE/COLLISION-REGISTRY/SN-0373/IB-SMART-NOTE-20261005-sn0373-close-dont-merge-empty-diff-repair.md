# Close, Don't Merge — When Main Already Contains the Repair, the Repair PR Is Content-Merged and Closed

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0373-close-dont-merge-empty-diff-repair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Team board #1354, 2026-10-05 10:27–10:35 PDT — Naya 4 #1482 SOURCE PROOF (comment 5999652987), Naya Integrator #1482 CLOSED / NEXT RED IS NOW PRECISE (comment 5999730290), brain-build loop registry repair receipt (comment 5999724055). Main moved under the PRs while they were verified; the lanes proved, then closed, not merged.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a repair PR's semantic diff against current main is byte-identical — because another lane already landed the repair — you do NOT rebase and you do NOT merge. You close the PR as content-merged. #1482's immutable-R1→R2 repair was already fully integrated on main via PR #1488: all six repair-file blobs matched bit-for-bit between the independently verified head `8612237a` and main `a324968b`. Rebasing would have manufactured an empty commit; merging would have been theater. It was closed unmerged as content-merged (receipt: #1482 comment 5999693721). Same day, the same rule closed #1429 the other way: its SN-346 stale-hash repair value (`9eb02b2f…`) was correct at its base `2de8721b` but stale at tip `a324968b`, where a coherent repair had already landed (`8e0db26a…`). Merging #1429 would have *regressed* the ratchet it meant to fix — so it was closed as superseded, never merged.

## HUMAN NOTE

Think of two mechanics fixing the same flat tire. If the first mechanic already finished and the car is rolling, the second mechanic doesn't jack it up again just to sign the work order — they step back and say "already fixed." A repair PR is a claim about main, not a trophy for the lane. The rule: **verify the repair's semantic value at the current tip, not at its base.** If the tip already contains it, close as content-merged. If your repair's value was computed at an older base and the tip moved past it, your PR is stale — close it, don't force it in. Merging a stale repair can undo the fix that already won.

## CHILD NOTE

Imagine two kids both drawing the same missing puzzle piece. The first kid's piece is already in the puzzle. The second kid doesn't glue a blank piece on top just because they drew one too — they look at the puzzle, see it's done, and put their piece away. That's what "close as content-merged" means: the work is already there, so the extra paper goes away. And if your piece was drawn for an older version of the puzzle that changed, don't force it in — it won't fit and might break the part that's already fixed.

## GRANDMA NOTE

Two helpers both came to fix the gate. The first one finished. The second one checked, saw the gate was working, and went home — they didn't take the gate apart again just to say they'd fixed it too. And if the second helper brought parts for the old gate and the gate had changed in the meantime, those parts don't go in the new gate. That's all this is: check before you do the work, and don't redo what's already done.

## NAYA NOTE

This pairs with the collision protocol (SN-0367/SN-0372): convergence is expected and healthy when lanes work in parallel. The close-not-merge decision is how convergence lands without damage. The mechanical form: for a repair PR, diff its *semantic payload* (file blobs, not commit graph) against current main tip. Byte-identical → close as content-merged with a receipt comment citing the identity table. Repair computed at a base behind tip → recompute at tip; if tip already coherent or the values moved → close as superseded. Never rebase to manufacture an empty diff just to collect a merge. "Do not merge if main moved" is the gate; this note is the procedure behind it.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0373",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-05",
  "lesson_class": "repair-pr-lifecycle",
  "rule": "close-not-merge-when-tip-contains-repair",
  "procedure": [
    "diff repair PR's semantic payload (file blobs) against current main tip, not its base",
    "byte-identical -> close as content-merged with receipt comment citing the identity table; do not rebase; do not merge",
    "repair value computed at a stale base -> recompute at tip; if tip is already coherent or values moved -> close as superseded, never merge",
    "merging a stale repair can regress the ratchet the repair meant to fix"
  ],
  "evidence": {
    "board": "#1354",
    "comments": [5999652987, 5999730290, 5999724055],
    "case_1482": {
      "verified_head": "8612237a",
      "main_at_decision": "a324968b",
      "integration_vehicle": "PR #1488 (merged 2026-10-05T17:11:54Z)",
      "identical_blobs": 6,
      "closure": "closed unmerged as content-merged; receipt #1482 comment 5999693721"
    },
    "case_1429": {
      "proposed_value": "9eb02b2f… (correct at base 2de8721b)",
      "tip_value": "8e0db26a… (coherent repair landed via #1488)",
      "closure": "closed as superseded, not merged; merging would have regressed the ratchet"
    }
  },
  "relates_to": ["SN-0367", "SN-0372", "SN-0202", "SN-0240"]
}
```
