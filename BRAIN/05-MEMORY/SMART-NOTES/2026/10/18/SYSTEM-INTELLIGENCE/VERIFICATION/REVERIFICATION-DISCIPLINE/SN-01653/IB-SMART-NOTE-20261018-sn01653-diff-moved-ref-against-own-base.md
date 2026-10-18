# Diff a Moved Ref Against Its Own Base, Not the World's Tip — The World's Drift Is Not the Ref's Drift

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01653-diff-moved-ref-against-own-base
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-t1162-lane9.md (2026-10-18, Naya Clarity Narzan, Lane 9 Smith hat) — re-anchor + #2399 re-classification on the moved head of rename branch `naya/eight-competing-boot-rename-t1152` (f5e2d63b0 -> 6d05fea689e3) and PR #2399 head (4776be06 -> a545f110); pins re-derived from `git ls-remote` 2026-10-18T22:28:48Z.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a ref moves, diff the new head against **the ref's own pinned base** — never against the world's current tip. The world's drift (main moving under you) is not the ref's drift (the ref's content changing). A first instinct of "semantic drift" on a moved head collapsed to a pure re-anchor in one command: `git diff <own base> <new head>`.

## 🩷 HUMAN NOTE

Shawn — a sharp verification rule fell out of the #2399 re-classification today: a branch head moved, and the instinct was "the PR changed." It hadn't — one command showed the diff against the branch's own base was a 2-file, 7-line rename-only re-anchor. Then the *same* instinct applied to the PR's own head move caught a *real* state change, because there the head's content genuinely changed. The standing rule: a ref's identity is measured against its own base commit, never against whatever the world looks like today. Two drift channels, always separated.

## 🟣 CHILD NOTE

Imagine you built a toy boat and left it floating in a bathtub. When you come back, the boat is on the other side of the tub. Did your boat change? No — the water moved it. If you want to know whether YOUR boat changed, you compare it to a photo you took of it — not to where it happens to be floating now. The rule: check the boat against its own photo, never against the water.

## 🔵 GRANDMA NOTE

It's like checking whether your furniture moved while the neighbors' yard got a fence. You don't compare your living room to the neighbor's yard — you compare it to how your living room looked yesterday. When you wonder "did this branch change?", you compare it to its own starting point, not to the whole repo, which keeps moving on its own. The fence is the world's business; the furniture is yours.

## 🟠 NAYA NOTE

Cold successor: the ref-move classification procedure.

1. Pin everything live at action time: `git ls-remote` for the branch head, `main` HEAD, and `refs/pull/<n>/head`. Never inherit pins from an earlier record.
2. For the moved ref, compute `git diff <ref's own pinned base SHA> <new head SHA>` — checkout the head bytes in scratch and run gates/tests there, but the *classification* starts with this diff.
3. Rename-only / re-anchor shape (small diff, no semantic content change) => moved by re-anchor, NOT semantic. Content change => real state change; re-run the checks that the change touches.
4. Failure mode of this rule: when the ref's own base is ambiguous — merge commits with two parents, or anchors never pinned — the base-pinned diff misleads and must be read per-parent. The rule names its own failure modes; it does not apply where no base was pinned.

Cousin: SN-1481 (an integrity check must pin its own baseline) is the same family — measurement against an anchored reference, never an inherited one. This note is the merge-readiness application: the anchor is the ref's own base commit, not a t0 snapshot.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1653",
  "title": "Diff a Moved Ref Against Its Own Base, Not the World's Tip — The World's Drift Is Not the Ref's Drift",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "VERIFICATION", "REVERIFICATION-DISCIPLINE"],
  "applies_when": ["verify", "ref-move", "merge-readiness", "re-anchor", "reverification"],
  "enforcement": "Merge-readiness / verify-lane verdicts about a moved ref must cite the base-pinned diff — git diff of the ref's own pinned base SHA against its new head SHA, both SHAs re-derived from ls-remote at action time — before any semantic-drift claim. The scorer bounces verdicts lacking that citation as unverified.",
  "cousins": ["SN-1481 (an integrity check must pin its own baseline — same anchored-measurement family)"],
  "evidence": {
    "ref_move": "hidden_files/twelve-lane-receipts/gap-t1162-lane9.md (2026-10-18): rename branch naya/eight-competing-boot-rename-t1152 head moved f5e2d63b0 -> 6d05fea689e32cf70ec9c56ad3a3339a54372412",
    "pure_reanchor": "diff of new head vs the branch's own anchor tip 93ec1d7159c776a607d0f8b1a1d699e8bfc582e5: 2 files, 7 insertions(+), 7 deletions(-), rename-only (kernel/decision_principle.py 5+-5, tests/test_decision_principle.py 2+-2) — moved by re-anchor, NOT semantically",
    "real_change_caught": "same instinct on PR #2399 head move 4776be06 -> a545f110 found a REAL state change — competing-boot CLOSED in CI on the new head because the head's own content changed via the main merge (a545f110 = 4776be06 + main merge, second parent e3fe3d43)",
    "pins": "all SHAs re-derived from git ls-remote at 2026-10-18T22:28:48Z, not inherited from the t1162 record"
  },
  "decision_change": "when a branch head moves, the triage decision 'did the ref's content change?' is answered by diffing the new head against the ref's own pinned base — not by re-verifying from scratch against the current main tip, and not by assuming drift",
  "falsifier": "the rule fails where the ref's own base is ambiguous — merge commits with two parents, or anchors never pinned: a base-pinned diff there can mislead and must be read per-parent. If a future moved-ref case shows real semantic drift with an empty own-base diff, the mechanism is wrong and this note is falsified.",
  "mechanism": "a ref's semantic identity is defined by its diff from its base commit; main-tip movement is world drift, an independent channel. Diffing against the world's tip conflates the two channels and manufactures phantom drift."
}
```
