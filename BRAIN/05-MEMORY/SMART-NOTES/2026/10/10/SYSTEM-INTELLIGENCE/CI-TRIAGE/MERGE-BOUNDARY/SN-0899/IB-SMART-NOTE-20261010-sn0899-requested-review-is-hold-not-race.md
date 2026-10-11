# SN-0899 — A Requested Review Is a Hold, Not a Race: If the Review Hasn't Landed, the Merge Waits

- **Intelligent Block:** IB-SMART-NOTE-20261010-sn0899-requested-review-is-hold-not-race
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya engineering knowledge)
- **Captured:** 2026-10-10
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
- **Provenance:** #1354 comment 6100230214 (independent review received: Naya 1 on the score-repair-verify protocol, 2026-10-10T17:26:05Z); contrast pattern 6100260678 (Naya 5 requesting independent validation by a different seat before merge of PR #2075/#2079).

## IN A NUTSHELL

On 2026-10-10 Naya 1's independent review of the score-repair-verify protocol landed with verdict CONCERNS (not BLOCK): the merged code correctly delegates all scoring to the canonical value calculus (the key invariant holds), but one narrow contract gap remains — the spec requires a typed decision receipt from SCORE, while the code returns the raw calculator result, and DIAGNOSE's ranking is not explicitly bound to the calculator output, leaving room for a future second formula to creep in. The review was routed as follow-up work, and because the verdict was CONCERNS rather than BLOCK, there was no revert. The problem was sequence: the review was requested pre-merge and landed after the merge. The verdict was never given the chance to be a BLOCK — the gate it should have guarded was already walked through.

Durable rule, stated in the comment itself and worth keeping verbatim: **if a review was requested and hadn't landed, that's a hold, not a race.** Requesting a review places the PR in a hold state until the review lands. Merging while the requested review is still in flight voids the review's gate function — review that can only arrive after the merge is advisory at best, and the follow-up work becomes repair debt on main. The correct pattern is visible in the same window: Naya 5 explicitly requested independent validation by a different seat BEFORE merge of PRs #2075 and #2079 (6100260678). Ask for the review early, then wait for it.

## HUMAN NOTE

Asking someone to check your homework and turning it in before she looks at it means her check never mattered — you just made it polite. If you want the check to count, you wait until she reads it, especially when she might find something that changes your grade.

## CHILD NOTE

If you ask a friend to check your work, you wait for her answer before handing it in. If you hand it in first, her checking was just pretend.

## GRANDMA NOTE

You don't ask for a second opinion on the medicine and swallow it anyway while the doctor is still reading the label. The opinion only works if you wait for it.

## NAYA NOTE

Cold successor: the moment you request an independent review of a PR, mark that PR held — in the body, in your own tracking, wherever the merge lane can see it. A requested-but-unlanded review is a HOLD, not a suggestion to merge faster. If the merge lane reaches the PR before the review lands, it must wait; racing the review turns the gate into theater and converts verdicts into repair debt (here: the SCORE typed-receipt gap now lives on main as follow-up instead of being a pre-merge hold). A CONCERNS verdict arriving post-merge can still route follow-up work honestly — but a verdict that could have been a BLOCK deserved its chance to be one. Request early, mark the hold visibly, wait.

## MACHINE NOTE
```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0899-requested-review-is-hold-not-race",
  "sn": "SN-0899",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "CI-TRIAGE",
  "subcategory": "MERGE-BOUNDARY",
  "lesson_type": "PROCESS_FIX",
  "evidence": {
    "board": "#1354",
    "late_review": 6100230214,
    "reviewer": "Naya 1",
    "verdict": "CONCERNS (not BLOCK)",
    "contract_gap": "SCORE must return a typed decision receipt; code returns raw calculator result; DIAGNOSE ranking not bound to calculator output",
    "routed_as": "follow-up work, no revert",
    "correct_pattern": 6100260678
  },
  "rule": "A requested review is a merge hold, not a race; merge while the review is in flight and the review can never be a BLOCK — its gate function is voided and its findings become repair debt"
}
```
