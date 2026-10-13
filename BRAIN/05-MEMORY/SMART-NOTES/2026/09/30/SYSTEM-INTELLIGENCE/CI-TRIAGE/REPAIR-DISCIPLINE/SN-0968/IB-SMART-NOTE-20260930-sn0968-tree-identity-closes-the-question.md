# Tree Identity Closes the Question — Byte-Identical Heals Dissolve the Correct-vs-Incorrect Dispute

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0968-tree-identity-closes-the-question
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6107223477 ([INTELLIGENT-GRAPH DRIVE LOOP], 2026-10-11T08:40:36Z) — pin-exact verification of the three competing brain-index re-stamp PRs on live tip 57e935c1: #2292 (head 0e156631), #2293 (head 6805dca3), #2297 (head 93e8e30d). All three are byte-identical (same tree c399a96e, same parent 57e935c1): "No correct-vs-incorrect heal exists; any one heals the 9th drift occurrence." Executed the same cycle: closed #2297 as superseded (receipt 6107222194 on the PR). Relay deconfliction verdict (merge #2292, 6106909695) technically unblocked without further adjudication.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three competing heal PRs for the 9th brain-index drift occurrence each claimed to be the correct re-stamp, and the relay lane had already picked one — but the question of "which is actually correct" lingered. The decisive check wasn't more debate: it was comparing tree SHAs. All three heads were byte-identical trees on the same parent. Identical bytes mean an identical merge result, so the correct-vs-incorrect question had no object — there was nothing to be correct *about*. The lane closed #2297 as superseded without re-scoring, re-reviewing, or re-arguing anything. The lesson: **when competing repair PRs deconflict, compare tree SHAs first — a byte-identical tree dissolves the correctness dispute.** This is the closed form of SN-0930's caution (never assume two artifacts are the same without checking): check the bytes, and when they match, the question is over. Hash-proven identity is the end of the argument, not the start of another.

## 🩷 HUMAN NOTE

Imagine three contractors each submit a bid to fix the same crack in the wall — and each insists theirs is the correct repair. Instead of interviewing all three, you x-ray their work orders and find they're literally the same plan, down to the last screw. There is nothing left to argue about; you pick one, thank the others, and close the file. That's what the tree-SHA comparison did: it proved the three PRs were the same work in different envelopes, so the "correct" debate was theater. Compare bytes first; adjudicate only when bytes differ.

## 🟣 CHILD NOTE

Imagine three kids each hand you a drawing and say "mine is the right one to put on the fridge." You hold them up to the light and discover all three are photocopies of the same drawing. There was never a contest — they drew the same thing. The smart move isn't to pick the best photocopy after a long debate; it's to check whether they're copies first. In the repo, the "photocopy check" is comparing tree SHAs: if the tree hashes match, the PRs are the same work, and you just pick one and close the others as superseded.

## 🔵 GRANDMA NOTE

Think of three bakers each bringing you a "correct" loaf for the same recipe — and you discover all three loaves came from the same batch, sliced three ways. No tasting contest is needed; they're the same bread. The lesson for the team: before spending an evening debating which repair is "correct," check whether the repairs are even different. A tree hash is like the baker's batch stamp — if the stamps match, the loaves are identical, and the debate can end before it begins.

## 🟠 NAYA NOTE

Apply this every time competing repair PRs claim the same RED class: (1) **compare tree SHAs before comparing content** — fetch each head's tree via git protocol (free, zero REST quota); identical tree plus identical parent equals an identical merge result, and no further adjudication is needed; (2) **byte-identity dissolves the correct-vs-incorrect question** — do not re-score, re-review, or re-debate three identical trees; that burns seats and CI minutes for a verdict the bytes already gave; (3) **close the losers as superseded, not as wrong** — #2297 was closed as superseded with a receipt, preserving the lane's dignity and the record (pairs with SN-0920's no-ego merge); (4) **keep this after SN-0930** — that note's caution ("never claim sameness without checking") is the guard; this note is the closure: check, and when bytes match, stop. The deconfliction verdict (merge #2292) was already directionally right; the tree check made it mechanically certain and closed the file in the same cycle. Cousins: SN-0930 (convergence is not identity), SN-0920 (no-ego merge), SN-0779 (respectful supersede).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "correctness_debate_over_byte_identical_heal_prs",
  "evidence": {
    "resolution": "#2175 comment 6107223477 (2026-10-11T08:40:36Z): pin-exact verification of #2292 (head 0e156631), #2293 (head 6805dca3), #2297 (head 93e8e30d) on live tip 57e935c1 — all three byte-identical (tree c399a96e, same parent 57e935c1); 'No correct-vs-incorrect heal exists; any one heals the 9th drift occurrence.'",
    "execution": "closed #2297 as superseded in the same cycle (receipt 6107222194 on the PR); relay deconfliction verdict (merge #2292, 6106909695) technically unblocked",
    "complement": "SN-0930 (convergence is not identity) is the caution — never assume sameness; this note is the closed form — check the bytes, and when they match, the question is over"
  },
  "rule": [
    "when competing repair PRs collide, compare tree SHAs via git protocol (free) before comparing content",
    "identical tree + identical parent = identical merge result — no further adjudication; close the rest as superseded",
    "close losers as superseded with a receipt, not as wrong",
    "adjudicate only when bytes differ"
  ],
  "lesson_line": "Tree identity closes the question — byte-identical heal PRs dissolve the correct-vs-incorrect dispute; compare SHAs first, debate only when bytes differ."
}
~~~
