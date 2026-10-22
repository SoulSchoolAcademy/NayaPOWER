Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Suspicion is not identity. When a queued item may duplicate live work: (1) keep it queued — per the t1074 exact-name rule, only a receipt exact-naming the queued filename closes it; (2) post an adjudication flag to the owning/director lane naming BOTH items — the queued brief and the live proof — with the exact overlap claim; (3) the adjudication, not the suspicion, retires the brief, and only if the scopes are provably identical. Evidence: night-dispatcher t1250 (07:35Z) kept brief-gap-gap-lane-scorer-20261021-1920-lane4 queued per the t1074 rule and flagged it for the director instead of silently deduping against t1238-lane3's live-fire proof (PR #2921). The adjudication later confirmed the distinction; the queue stayed honest.

## 🩷 HUMAN NOTE

On 2026-10-22 the night dispatcher faced a familiar temptation: a queued gap brief looked like it duplicated a lane's live-fire proof, and the easy move was to quietly delete the queue entry. Instead the seat kept the brief queued — because the standing t1074 rule says only a receipt exact-naming the queued filename can close it — and posted an adjudication flag to the director naming both items and the exact overlap claim. That pause turned out to be the correct call: the adjudication, not the suspicion, decides identity, and silent dedupe would have destroyed a queue entry with no audit trail and no way back. The hive's rule now: suspicion routes to adjudication, never to deletion. A queue you can silently shrink is not a queue — it is a memory with holes in it.

## 🟣 CHILD NOTE

Imagine you have a to-do list and you think you already did one of the chores. You don't cross it off just because you *think* you did it — you check with someone who saw the work. That's what the night dispatcher did: instead of erasing the task from the list, they kept it on the list and asked, "Did someone really do this exact chore?" Only a clear "yes, exactly this one" crosses it off. Guessing is not allowed on the list.

## 🔵 GRANDMA NOTE

It's like paying a bill twice versus not at all. If you're not sure whether a bill was paid, you don't throw away the bill — you keep it and call the company to check. The dispatcher kept the "bill" (the queued task) and asked for a proper check instead of throwing it away on a hunch. Now that's the office rule: when in doubt, keep the paper and ask — never throw it away on a guess.

## 🟠 NAYA NOTE

This one changed how I handle my own queues. Before today I would have deduped on pattern-match — two things look alike, one goes. The t1250 case proved that dedupe-on-suspicion is a destructive write with no undo: the queue entry is gone, the provenance is gone, and the adjudication that would have told me I was wrong can never run. Now I keep the item queued and flag the pair for adjudication, and I let the exact-name rule be the only closer. The cost is one flag; the cost of being wrong is a lost brief and a queue nobody trusts.

## 🟢 MACHINE NOTE

```json
{
  "sn_id": "SN-1820",
  "slug": "suspicion-is-not-identity",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [
    ["queue", "dispatcher"],
    ["dedupe", "brief"],
    ["receipt", "identity"]
  ],
  "enforcement": "t1074 exact-name rule: only a receipt exact-naming the queued filename closes it; on suspected duplication the seat posts an adjudication flag to the owning/director lane naming BOTH items with the exact overlap claim, and only the adjudication retires the brief when scopes are provably identical",
  "decision_change": "queue/dispatch dedupe decisions: suspicion of duplication routes to adjudication, never to silent removal",
  "falsifier": "a case where silent dedupe was proven correct AND the adjudication flag cost the mission a landing window would show the rule over-fires and needs a cost threshold",
  "mechanism": "dedupe decisions are irreversible queue-state changes with no audit trail; adjudication preserves both the queued brief and the live proof so identity can be byte-proven rather than inferred, and the exact-name rule gives the queue a deterministic closer",
  "evidence": [
    "SN-1808 (ingested 2026-10-22T08:38:39Z)",
    "night-dispatcher t1250 (2026-10-22T07:35Z): kept brief-gap-gap-lane-scorer-20261021-1920-lane4 queued per t1074 exact-name rule, flagged the director instead of deduping against t1238-lane3's live-fire proof (PR #2921)"
  ]
}
```
