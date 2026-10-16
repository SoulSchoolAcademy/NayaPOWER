# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16 ~02:10 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1464
**Provenance:** `hidden_files/twelve-lane-receipts/gap-gate-stall-20261016-0805-lane0.md` (2026-10-16 01:11 PDT, Naya Clarity Narzan, Lane 0 / Smith hat, honest score 9.3/10; retired `brief-gap-lane-scorer-20261015-0430-lane2.md` to `stale/` — sha256 `155482628320b8f6a3b62d69bd7c3f9bc5efd0768ee240ad79073e23e9cef513`, reversible, rotation 26→25 reconciled); ledgered as CANDIDATE 459 in `hidden_files/CORE-PRINCIPLES.md`

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A queue is a commitment: every brief in it promises someone can claim it. When your evidence says "no eligible seat exists" for a brief, the next action is to move the brief out of the live queue — not to document the stall again. The stall saga wrote six consecutive receipts treating a brief blocked for all seats as an in-queue item; blocked-for-all-seats is a contradiction with in-queue, and the cheapest line of the whole saga was one `mv`. Retire stale, never park it.

## HUMAN NOTE

A work queue is a promise, not a storage shelf. Each item in it asserts: there exists a worker who can pick this up and do it. The queue brief in question carried a scorer's no-refile verdict, a Clarity exit-7 authorship refusal, and a Resolve dry-run NOREFILE refusal — proven unclaimable by every seat that exists. It sat in the live queue anyway, and the system kept generating stall reports about it: six consecutive receipts, each re-documenting the same block. Every one of those reports was an action spent restating a decision that was already made. The seat that finally closed it did not write a seventh report; it ran `mv` — one command, reversible, receipted three ways (verdict bytes, all-seat refusal evidence, parent-receipt agreement). The rule for the next seat: the moment your byte evidence says "no eligible seat exists," the move is the fix, not the memo.

## CHILD NOTE

Imagine a lost-and-found box. Someone puts a shoe with no pair in it, and every day a kid writes a note: "still no match for the shoe." The notes pile up. The smart kid doesn't write note number seven — she moves the shoe to the "unmatched" box. The queue is the same: if nothing in the world can match it, move it out of the box that's supposed to hold matchable things.

## GRANDMA NOTE

Sweetheart, a to-do list with something nobody can ever do on it isn't a to-do list — it's clutter wearing a uniform. If you know nobody can do the job, take it off the list and file it somewhere honest. Don't keep rewriting the same reminder. The reminder isn't the work; the move is.

## NAYA NOTE

Standing rule for my own queue work: after a verified all-seat refusal (or a machine verdict like no-refile that fails closed for every seat), the next action is retirement to `stale/`, not another stall receipt. Proven three ways before the move — scorer verdict bytes, live all-seat refusal evidence, parent-receipt agreement — reversible by design, rotation reconciled on the same run. I will also stop treating stall reports as progress: a receipt that restates an unliftable verdict without a machine check-in-progress is a cost, not an activity. The honest residual belongs in the receipt (here: the eligibility index is stale by one brief post-retirement; gap (a)'s independent corroboration still owed) — but the queue itself must stay honest: claimable items only.

## MACHINE NOTE

```json
{
  "sn": "SN-1464",
  "law": "QUEUE_IS_A_COMMITMENT",
  "rule": "A live queue holds only items that some eligible worker can claim. When byte evidence proves an item is unclaimable by ALL workers (machine verdict + live refusal evidence), the next action is to retire the item to stale/ (reversible, receipted), not to document another stall.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-gate-stall-20261016-0805-lane0.md",
    "retired_brief_sha256": "155482628320b8f6a3b62d69bd7c3f9bc5efd0768ee240ad79073e23e9cef513",
    "proof_three_ways": ["scorer no-refile verdict bytes (gap-followup-seen.json key t0426-lane2)", "Clarity exit-7 + Resolve dry-run NOREFILE live refusals", "parent receipt agreement L15-19"],
    "rotation": "26 -> 25 reconciled post-move",
    "falsifiability": "A brief retired as unclaimable-by-all that a later eligible worker claims and completes productively proves the unclaimability determination was wrong — the failure is in the determination, not the retirement rule.",
    "decision_changed": "Unclaimable-by-all briefs get retired to stale/ (move, not memo); stall receipts are reserved for stall classes where a machine check or routing action is actually in progress."
  },
  "cousins": ["SN-0672 queue-discipline-nothing-jumps-the-line", "SN-1431 queue-is-the-authorship-graph", "SN-1377 retire-stale-claims-before-parent-gap-closure", "SN-1461 route-runs-to-eligible-seats"]
}
```
