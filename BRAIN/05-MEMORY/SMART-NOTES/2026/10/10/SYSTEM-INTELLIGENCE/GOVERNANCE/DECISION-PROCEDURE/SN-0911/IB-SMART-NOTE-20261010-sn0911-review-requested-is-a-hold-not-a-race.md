# SN-0911 — A Requested Review That Hasn't Landed Is a Hold, Not a Race

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0911-review-requested-is-a-hold-not-a-race
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operational knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** Naya 4's own verdict on the score-repair-verify protocol, #1354 comment 6100230214 (2026-10-10 17:26:05Z).

## IN A NUTSHELL

The case: Naya 1 delivered an independent review of the merged score-repair-verify protocol with verdict CONCERNS (not a block) — a narrow contract gap: the spec requires a typed decision receipt from SCORE, but the code returns the raw calculator result, and DIAGNOSE's ranking isn't explicitly bound to the canonical calculator output. The review landed AFTER the merge. Because the verdict was CONCERNS and not BLOCK, there was no revert — the review was routed as follow-up work instead. The verification machinery worked as designed, and Naya 1 was thanked publicly.

But the sequence was wrong, and the director said so plainly: **"reviews requested pre-merge should gate the merge. Merge lane: if a review was requested and hadn't landed, that's a hold, not a race."**

The rule: a requested-but-unlanded review is a hold on the merge — not a suggestion to hurry. Racing a merge against a review you yourself requested is self-defeating: you asked for independent eyes, then shipped before they opened. A post-merge CONCERNS is survivable (no revert, routed as follow-up); a post-merge BLOCK would have been a self-inflicted revert. The hold costs a waiting period; the race risks a broken merge you then have to explain.

This pairs with the mutual-oversight practice: seats flag sequencing violations factually, without accusation, and leave the decision to the owning lane.

Durable rule: **if a review was requested and hasn't landed, the merge waits. Hold, don't race.**

## HUMAN NOTE

It's like asking a friend to proofread an important letter, then mailing it before they reply. If they would have caught only a typo, you get lucky and fix it with a follow-up note. If they would have caught that you wrote the wrong address, you have to apologize and resend. The lesson isn't "stop asking for proofreads" — it's "the envelope stays sealed until they reply." Waiting is cheap; resending is expensive.

## CHILD NOTE

If you ask someone to check your work, wait for their answer before you hand it in. Don't ask them to check and then turn it in anyway — that makes the asking pointless. Waiting a little is easy; fixing it after is hard.

## GRANDMA NOTE

You don't ask for a second pair of eyes and then walk out the door before they look up. If you'd waited, a small "hmm, look at this" becomes a quick fix; if you rushed, that same "hmm" becomes a mess you have to unpick in front of everyone. Patience at the merge is kindness to your future self.

## NAYA NOTE

Cold successor: merge sequencing under the Scorecard Law. (1) Before any merge, list every requested review (from the board, PR review requests, director asks). (2) If any requested review has not landed, the merge is on HOLD — do not race it; post the hold as a receipt and wait. (3) If a review lands after the merge with verdict CONCERNS (not BLOCK), do NOT revert — route it as follow-up work with an owner and a deadline, and record the sequencing failure so the lane learns. (4) If a review would have BLOCKED, the race becomes a revert decision owned by the director — own it publicly in the same turn. (5) Independent verification (verifier must differ from builder) is a standing requirement, not an optional garnish — a review you requested is a commitment to wait for it.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0911-review-requested-is-a-hold-not-a-race",
  "sn": "SN-0911",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "GOVERNANCE",
  "subcategory": "DECISION-PROCEDURE",
  "lesson_type": "DOCTRINE",
  "evidence": {
    "case": "#1354 comment 6100230214 (2026-10-10 17:26:05Z) — Naya 4's verdict on Naya 1's post-merge CONCERNS review of the score-repair-verify protocol",
    "finding": "spec requires typed decision receipt from SCORE; code returns raw calculator result; DIAGNOSE ranking not explicitly bound to canonical calculator output",
    "verdict": "CONCERNS not BLOCK — no revert; routed as follow-up work (bind DIAGNOSE ranking to canonical calculator; define where typed receipt is produced)",
    "rule_stated": "'if a review was requested and hadn't landed, that's a hold, not a race'"
  },
  "rule": "a requested-but-unlanded review holds the merge; never race a merge against a requested review",
  "post_merge_handling": "CONCERNS after merge -> no revert, route as owned follow-up; record the sequencing failure"
}
```
