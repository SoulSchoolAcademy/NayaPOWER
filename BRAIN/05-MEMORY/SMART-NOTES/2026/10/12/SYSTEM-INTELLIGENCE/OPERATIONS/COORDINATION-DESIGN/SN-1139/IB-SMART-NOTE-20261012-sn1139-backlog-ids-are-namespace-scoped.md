# Backlog IDs Are Namespace-Scoped — Bind the Existing Entry or Renumber in the Same Step

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1139-backlog-ids-are-namespace-scoped
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE LEARN · COMPOUNDER] #2175 comment 6135493017 (2026-10-13 ~00:44Z, wave 13 sign-out): anomaly routed (no action) — the queue carries TWO B-48s: the receipt-gate B-48 (PR #2494, 9.6 SHIP) vs the cold-retrieval false-positive B-48 (this lane's wave-13 measurement). Main seat to renumber one. [LEARNING EVENT · DISTILLATION V2] #2175 comment 6135839165 (2026-10-13 ~01:05Z) — L272 (F5, team): flagged by Compounder, dispatcher, build, and relay independently; rule: a lane claiming a live B-number binds the existing queue entry or renumbers its own claim in the same step. Promoted to standing law this run (AGENTS.md). Note: the queue double-B-48 is an anomaly routed, not an accusation — both claimants worked in good faith.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two lanes were working "B-48" at the same time — one meant the receipt-gate B-48 (PR #2494, 9.6 SHIP), the other meant the cold-retrieval false-positive B-48 (Compounder wave-13). Four seats spotted the collision independently (Compounder, dispatcher, build, relay) — which is exactly how a shared identifier stops being shared: every watcher assumes THEIR B-48 is THE B-48, and verdicts, receipts, and merge-gates quietly attach to the wrong ticket. The durable rule: **backlog IDs are namespace-scoped — a lane claiming a live B-number binds the existing queue entry or renumbers its own claim in the same step.** "First claim stands" is the collision law: the second claimant does not argue, does not reuse — it renames, in the same breath as the claim. Renaming is cheap; a verdict filed under the wrong ID poisons the queue's memory of both tickets.

## 🩷 HUMAN NOTE

Shawn — a small collision with a big lesson, caught cleanly tonight. Two different jobs were both called "B-48" — one in the receipt gate, one in the retrieval wave — and four different lanes flagged it before anything attached to the wrong ticket. The rule on the wall now: backlog IDs belong to whoever claimed them first, and if you pick up a number that's live, you renumber YOUR claim in the same step — no debate, no reuse. Cheap rename now beats a poisoned ticket later.

## 🟣 CHILD NOTE

Imagine two kids in a class are both named "Alex." The teacher says "Alex, great job on the test!" — and both kids smile. Later, when one Alex needs extra help, the teacher looks at the wrong Alex's paper. Names only work when everyone means the SAME person. The team had two "B-48s" — two different jobs with the same name. The rule: the first Alex keeps the name; the second one picks a new name right away, the same moment they say hello. Then nobody ever opens the wrong paper.

## 👵 GRANDMA NOTE

It's like two patients in a hospital with the same chart number. The pharmacy fills the prescription under the number — and the wrong patient gets the pills. Nobody meant harm; the number just wasn't unique. The fix is a habit, not a system: when you take a number that's already in use, you take a different number, right then, before you write anything down. The first claim keeps the number; the second claim renames itself. One small habit prevents every mix-up.

## 🤖 NAYA NOTE

Identifier collision is a silent corruption class: it doesn't fail loudly, it misattributes. The B-number queue is a shared namespace across lanes, and four independent detections (Compounder, dispatcher, build, relay) prove the collision surface is real — parallel lanes mint IDs from memory of the queue, and the queue drifts. The discipline is two-part: (1) bind — before claiming a live ID, check the queue (the Compounder did; the anomaly was routed, not repeated); (2) renumber-in-the-same-step — the second claimant renames its own claim immediately, no adjudication needed for the common case, main seat arbitrates only the genuinely disputed. "First claim stands" is the standing collision law because adjudication is expensive and renaming is free. The cost of skipping it: verdicts, receipts, and merge-gates filed under one ID and read against another — a poisoned queue that a cold successor cannot untangle. Cousin: SN-1138 (prove the identity, not just the event) — same family: identity first.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1139",
  "lesson": "backlog-ids-are-namespace-scoped",
  "rule": "A lane claiming a live backlog ID binds the existing queue entry or renumbers its own claim in the same step; first claim stands, renaming is immediate and unilateral.",
  "failure_class": "identifier-collision / queue poisoning",
  "evidence": {
    "anomaly": "#2175 comment 6135493017 (2026-10-13 ~00:44Z): queue carries TWO B-48s — receipt-gate B-48 (PR #2494, 9.6 SHIP) vs cold-retrieval false-positive B-48 (Compounder wave-13); main seat to renumber one",
    "independent_detections": "flagged by Compounder, dispatcher, build, and relay — four independent seats, same window",
    "learning_event": "#2175 comment 6135839165 (2026-10-13 ~01:05Z): L272 (F5, team) → standing law this run (AGENTS.md)"
  },
  "repair_doctrine": "Bind-or-renumber: check the queue before claiming; second claimant renames in the same step; main seat arbitrates only genuinely disputed claims",
  "related": ["SN-1138"]
}
```
