# IB-SMART-NOTE-20261006-sn0493-decision-expires-when-tip-moves-reverify-at-action

| Field | Value |
|---|---|
| Intelligent Block | IB-SMART-NOTE-20261006-sn0493-decision-expires-when-tip-moves-reverify-at-action |
| Smart Note | SN-0493 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Captured | 2026-10-06 |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

## IN A NUTSHELL

A consolidation receipt scored three colliding repair PRs and decided "merge #1661" — a sound decision on its bytes. But PR #1660 had merged 21:53:16Z, three minutes *before* the 21:56Z receipt, healing the RED and rendering #1661 dirty and superseded. The decision was correct on its evidence and dead on arrival. A decision computed on tip T is inadmissible after the tip moves: re-verify tip currency (refs API) at the action instant, between the decision and the act.

## HUMAN NOTE

Shawn — we watched a perfectly good decision die today. Naya 2's consolidation receipt carefully compared three repair PRs and picked #1661 — solid reasoning, honest scorecard. But while the receipt was being written, another seat's PR #1660 had already merged and fixed the same problem. So the "winning" PR couldn't merge anymore — it was built on a world that no longer existed. Nobody did anything wrong; the lesson is mechanical: always re-check the current state *right before you act*, not just when you decide. Decisions have an expiry date, and the expiry date is the next commit.

## CHILD NOTE

You plan to buy the last slice of pizza because the sign says "1 left." On your way to the counter, someone else buys it. Your plan was perfect — for the world where the slice still existed. Always glance at the counter again before you order.

## GRANDMA NOTE

The council voted to pave Elm Street based on a survey — but between the survey and the vote, Elm Street had already been paved under a different contract. The vote was unanimous and completely correct, and completely pointless. Check the street before you vote on paving it.

## NAYA NOTE

Note to future me: decisions are timestamped to a tip the way milk is dated. (1) Between decision and action, re-read the refs API — if the tip moved, the decision's evidence is stale and the action is not authorized until re-validated on the new bytes. (2) When another lane merges on the same files your decision touches, your decision is overtaken even if it was right — verify merge_base and mergeability before acting, not just byte-level correctness of the candidate. (3) The mirror of SN-0440: one exact-tip battery is enough when the tip *hasn't* moved — and a decision is dead when it *has*. Report overtaken decisions in the open ("merge #1661 is overtaken") rather than executing them into a conflict.

## MACHINE NOTE

```json
{
  "rule": "decision_expires_when_tip_moves",
  "protocol": "decision -> re-anchor (refs API) at action instant -> validate mergeability on new bytes -> act or re-decide",
  "overtaken_decision": "correct on its evidence, inadmissible after tip movement",
  "family": ["SN-0440 (one exact-tip battery is enough — mirror image)", "SN-0202 (re-anchor to the live head before building)", "SN-0392 (first RED is the only RED — never build downstream of unproven state)", "SN-0236 (one repair per RED class)"],
  "evidence_class": "decision_failure",
  "falsifier": "an action executed on a moved tip that lands cleanly with no mergeability or state conflict"
}
```

## EVIDENCE

- #1354 6026182117 (Naya 2 consolidation receipt, 2026-10-06T21:56:16Z): scored #1657/#1660/#1661, "Decision: A wins. Merging #1661 now."
- #1354 6026215662 (Naya 2 brain-build adjudication update, 2026-10-06T21:58:42Z): "PR #1660 merged 21:53:16Z, *before* the 21:56Z consolidation receipt 6026182117" — main moved `1204519c5efd` → `5fa862569bec`; "#1661 @ 125da417 is now `mergeable_state: dirty` vs the new tip"; "Consequence for the receipt's decision: 'merge #1661' is overtaken."
- #1354 6025984492 (brain-drive sign-out): states the standing condition the receipt missed — "re-verify tip currency at merge instant; P1 green required."
