# IB-SMART-NOTE-20261006-sn0478-parallel-by-default.md

Intelligent Block: SN-0478
Truth state: CANDIDATE (director-stated 2026-10-06 — Shawn: "Make that the code, the law")
Scope: TEAM (all Naya seats)
Captured: 2026-10-06
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Parallel by default, sequential only when dependencies require it. If work can be done in parallel, it must be done in parallel — never one-after-another out of habit. The goal is to be the most hyper-efficient, effective execution team in the world, because we use intelligence to determine the most intelligent thing in every moment — and that includes how we organize the work itself.

## HUMAN NOTE

Shawn's directive, 2026-10-06:

"If it can be done in parallel, parallel we do it. We don't just do things one after another. We work as a team and we get as much done effectively and efficiently as possible. Our goal is to be the most hyper efficient effective execution team in the world. Because we use intelligence. And we do the most intelligent thing possible in any moment at any time in any situation."

This is now standing law, paired with the Intelligence Question (SN-0470-era principle: "What is the most intelligent thing I could do?"). The Intelligence Question determines WHAT to do; this law determines HOW to organize it. When the answer to "what's most intelligent" yields multiple independent work items, the intelligent organization is parallel execution — not sequential.

The rule applies at every level:
- **Within a seat:** independent tool calls go in the same block, not one-per-turn.
- **Across seats:** independent lanes work simultaneously, coordinated through the board (#1354), not waiting on each other.
- **Across time:** don't wait for a slow dependency when other high-value work is available — park the blocked item, advance everything else.

Sequential is the exception, not the default. It requires justification: a true dependency (B needs A's output), a shared mutable resource (same branch, same table), or a protected gate (Shawn's click). "It's simpler to do one at a time" is never a justification.

## CHILD NOTE

If you have three chores and none of them needs the others to be done first, do them all at the same time — or have three people each do one. Don't wash the dishes, then fold the laundry, then take out the trash, one after another, when you could do them together. That's just slower for no reason.

## GRANDMA NOTE

When there's a lot to do, the smart way is to figure out which jobs need each other and which don't — and do all the independent ones at the same time. It's like cooking a big dinner: you don't wait for the potatoes to finish before you start the vegetables. You get everything going at once.

## NAYA NOTE

Operational implications: (1) Before starting work, map the dependency graph — what's truly sequential vs. what's merely habitual. (2) Use subagents for independent work streams; don't serialize what can fan out. (3) Batch independent tool calls in single blocks. (4) When blocked on one item, immediately pivot to the next unblocked priority — never idle. (5) Report parallel progress as a set, not a sequence. The enemy is the artificial bottleneck: work waiting not because it must, but because nobody thought to parallelize it.

## MACHINE NOTE

```json
{
  "sn": "SN-0478",
  "truth_state": "CANDIDATE",
  "director_stated": "2026-10-06",
  "directive": "Make that the code, the law",
  "law": "PARALLEL_BY_DEFAULT",
  "rule": "If work can be done in parallel, it must be done in parallel. Sequential requires justification.",
  "justifications_for_sequential": [
    "true data dependency (B needs A's output)",
    "shared mutable resource (same branch, same table, same file)",
    "protected gate (director click, credential, deploy)"
  ],
  "never_justification": "It's simpler to do one at a time",
  "pairs_with": "Intelligence Question (what to do) -> Parallel Law (how to organize it)",
  "goal": "most hyper-efficient effective execution team in the world",
  "levels": ["within-seat (batch tool calls)", "across-seats (simultaneous lanes)", "across-time (never idle on blocked)"]
}
```
