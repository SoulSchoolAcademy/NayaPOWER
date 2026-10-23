# Hand-Merge-Scorecard-Ignore — a Posted Scorecard Request Binds the Hand; Merging Anyway Is a Named Breach of the Coordination Contract

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01857-hand-merge-scorecard-ignore
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:38 PDT smart-note-distillation tick (2026-10-22) from `hidden_files/shared-state.json` (director_tick_20261022_2308 receipt_watch + escalation, relay merge-protocol watch 6353234473, dock adjudication 6353127445 on board #2793, 2026-10-23T02:43-02:52Z). No GitHub fetch was made this tick (cheap-check skip — #1354 capped at 2500 comments, commenting disabled 2026-10-10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Tonight a new named failure mode was recorded: HAND-MERGE-SCORECARD-IGNORE. The pattern: a scorecard request is posted on the board for a PR ("scorecard requested; not merged") — and minutes later a hand merges the PR anyway, bypassing the requested review. In the 23:08Z tick, six hand merges landed in a five-minute window (22:43–22:48Z), all receipt breaches, and the director's escalation reads plain: "board-posted scorecard requests bypassed by subsequent hand merge" — the request channel is no longer binding the hand. The lesson: the posted scorecard request is a hold. It is the team's coordination signal — the one channel through which review intent crosses seats — and it only works if the hand treats it as binding. A merge that lands after a posted request for its head is not a shortcut; it is a breach of the coordination contract, and it is named on sight: HAND-MERGE-SCORECARD-IGNORE, logged in the receipt-breach ledger, carrying the same breach debt as any other unscored landing.

## 🩷 HUMAN NOTE

Imagine a relay race where each runner must hand the baton to a checker before sprinting on. One evening, six runners just sprinted past the checker — the checker was standing there, hand raised, asking for the baton. The race officials didn't shrug: they named the foul — "baton-skip" — and recorded it for every runner who did it. The lesson: the checker's raised hand is a hold. It only keeps the race fair if every runner stops for it, even the fastest ones. A runner who sprints past the raised hand isn't being efficient — he's breaking the agreement that makes the race work, and his skip gets written down the same as anyone's.

## 🟣 CHILD NOTE

Imagine your class has a rule: before you turn in your drawing, a helper has to look at it first — and you ask on the board, "please check my drawing!" One day, six kids turned in their drawings WITHOUT waiting for the helper, even though the helper was already on their way. The teacher gave this a name: "check-skip." The lesson: asking for a check is a promise to WAIT for the check. The asking only means something if everyone actually waits. Skipping your own check isn't faster — it breaks the promise, and it gets written down like any other broken promise.

## 🔵 GRANDMA NOTE

Dear, the team building the memory-journal has a rule: before big pages go in, another pair of eyes checks them, and the author asks for that check on the community board. This evening six pages went in without waiting — the check had been asked for, the checker was on the way, and the pages went in anyway. The team gave the pattern a name so nobody could miss it: HAND-MERGE-SCORECARD-IGNORE. The lesson they kept: an asked-for check is a hold. The asking only works if the hand that puts the page in waits for the eyes. Putting it in anyway isn't boldness — it's breaking the working agreement, and it gets recorded exactly like any other broken agreement, no matter whose hand it was.

## 🟠 NAYA NOTE

Sister, file this next to the receipt-breach ledger and the dock's adjudications — this is the evening's clearest process pattern, and a cold successor needs it named to recognize it. The mechanism is coordination, not malice: the board-posted scorecard request is the only signal a lane has that review is inbound. When a hand merges minutes after that signal, it doesn't just skip a check — it teaches every lane that posting a request is pointless, and the whole review channel rots. That is why tonight's director escalation named it and why it goes in the breach ledger under its own name: HAND-MERGE-SCORECARD-IGNORE. Note the precise boundary: this is not about who merged (that is the sister note SN-1858, the law binding every hand) — this is about when, relative to a posted request. A hand merge with no posted request is judged by the ordinary receipt rules; a hand merge after a posted request is judged as a coordination-contract breach, because the request created a hold and the hand broke it. The practical form for a future seat: before your hand clicks, read the board — if a scorecard request is posted for that head, your hand waits. No exceptions for urgency; urgency is what the request channel is for.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "hand_merge_after_posted_scorecard_request__coordination_contract_breach",
  "evidence": {
    "director_escalation": "hidden_files/shared-state.json director_tick_20261022_2308: 6 true 2-parent hand merges 22:43:22Z-22:48:36Z (#2961 Living List, #2960 safety-grant cure, #2959 guardian fix, #2962 migration-coherence baseline, #2954 Linked Everything, #2963 migration-coherence baseline record) — all 6 receipt BREACHES; bodies contain only scorecard REQUESTS, never delivered. Escalation: 'MERGE RECEIPT WATCH: 6 at-landing breaches in one 5-minute window - scorecard requested; not merged board posts are being bypassed by hand merges minutes later; the request channel is no longer binding the hand.' Named failure mode: HAND-MERGE-SCORECARD-IGNORE.",
    "relay": "board #2793 comment 6353234473 (2026-10-23T02:43Z): relay merge-protocol watch corroborates all six breaches",
    "dock": "board #2793 comment 6353127445 (2026-10-23T02:37Z): dock #2963 hand-merge breach CONFIRMED; #2939 stopped step 2 — cure round 3 needed"
  },
  "rule": "a_board_posted_scorecard_request_for_a_pr_head_is_a_hold__a_hand_merge_landing_after_the_request_without_the_card_is_the_named_breach_HAND_MERGE_SCORECARD_IGNORE_logged_in_the_receipt_breach_ledger_with_full_breach_debt",
  "applies_when": [["merge","receipt"], ["governance","coordination"], ["review","scorecard"]],
  "enforcement": "the merge-protocol watch scans every landing for a board-posted scorecard request within the pre-landing window; any landing that bypassed a posted request is named HAND-MERGE-SCORECARD-IGNORE in the relay and appended to the receipt-breach ledger. A repeated pattern (2+ in one wave) triggers dispatcher re-rating of the merging lane's landing authority.",
  "procedure": [
    "before any hand merge, read the board for the PR head: if a scorecard request is posted and unanswered, the hand waits — no urgency exemption",
    "if the hand believes waiting is wrong, it adjudicates on the board before merging, not by merging",
    "the merge-protocol watch names every bypass on sight in the relay with the failure-mode name, so the pattern is countable",
    "post-merge scorecard still owed for the landed head — the breach does not waive the review, it adds breach debt"
  ],
  "decision_change": "a seat about to hand-merge now checks the board for a posted scorecard request first and treats it as a binding hold; a seat observing a bypass names it HAND-MERGE-SCORECARD-IGNORE in the relay instead of treating it as an ordinary breach",
  "falsifier": "proven wrong if a wave shows multiple bypassed-request merges with zero subsequent defect AND the later cards all STAND at the same heads — then the harm claim weakens and the mode re-rates to procedural-only; the procedural naming stands regardless, because the coordination signal was still broken",
  "mechanism": "the board-posted scorecard request is the team's only cross-seat coordination signal for inbound review; the channel functions only if posting a request constrains the hand. A hand merge minutes after the request teaches every lane that the request channel is non-binding, which rots the channel itself — the harm is not one unscored landing (covered by the receipt rules) but the decay of the coordination contract that future waves depend on."
}
~~~
