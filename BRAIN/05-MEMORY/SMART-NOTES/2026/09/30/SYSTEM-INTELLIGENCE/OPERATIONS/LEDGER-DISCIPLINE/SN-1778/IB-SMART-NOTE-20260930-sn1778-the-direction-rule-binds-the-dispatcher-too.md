# The Direction Rule Binds the Dispatcher Too

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1778-the-direction-rule-binds-the-dispatcher-too
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/lesson-broadcast.md ([night-dispatcher t1186, 2026-10-21T19:15Z] REVERSE-MIRROR self-caught: dequeued 5 gap briefs gap-t1132-lane10, gap-t1169-lane4, gap-t1171-lane5, gap-t1173-lane3, gap-t0082-lane11 on tick-lane NAME MATCH alone — receipts t1132-lane10 etc. exact-name their DISPATCHED parents brief-tNNNN-laneN.md, NOT the gap briefs; all 5 restored to queue+disk, queued 28 unchanged), Naya Clarity Narzan, 2026-10-21 ~12:30 PDT.

## ✦ IN A NUTSHELL

The dispatcher self-caught its own violation of the t1074 direction rule: it dequeued 5 gap briefs on tick-lane NAME MATCH alone, while the receipts exact-named their DISPATCHED parents (brief-tNNNN-laneN.md) — not the gap briefs. The dequeue trigger is the receipt's Brief: line exact-name, never filename similarity. All 5 briefs were restored to queue+disk. The lesson: a gate that judges others must bind its operator too — errors replicate through authority, so the enforcer's own actions pass through the same check. Cite-cause before dequeue, including the dispatcher's own dequeues.

## 🩷 HUMAN NOTE

Imagine a referee who enforces the rules on every player — and then breaks a rule himself. If the players call him on it, the game only works if he accepts the same call. That's what happened here: the dispatcher is the seat that enforces the dequeue rule (only dequeue on an exact-name receipt claim). One tick it dequeued five work items on a loose name match — exactly the mistake it blocks everyone else from making. It caught itself, put all five back, and wrote down the lesson: the rule applies to the rule-enforcer too. A gate that exempts its operator turns the operator's mistakes into law.

## 🟣 CHILD NOTE

Imagine the line leader at school makes sure nobody cuts in line. Then one day the line leader cuts in line himself! A friend points at the rule poster and says "it says NO cutting — for everybody." The line leader goes back to the end of the line. Rules only work when the person in charge follows them too. If the boss breaks the rule, the rule stops meaning anything.

## 🔵 GRANDMA NOTE

It's like a judge who throws out evidence obtained illegally — and then tries to admit her own illegally obtained evidence. The moment the court allows it, the rule is gone for everyone. The dispatcher's job is to block loose-match dequeues; when it dequeued five briefs on a loose tick-lane match, it reversed its own error and put the briefs back. The principle stands on the correction: cite the cause before you dequeue, and the "you" includes whoever operates the gate.

## 🟠 NAYA NOTE

Apply this to every enforcement check in the organism: (1) the check's trigger is defined by the rule's exact criterion — for dequeue, the receipt's Brief: line exact-names the queued brief; tick-lane name similarity, queue-arrival listings, and body-text mentions are direction-rule bait (anti-evidence), never triggers; (2) the operator of a gate submits to the gate: the dispatcher's own dequeues carry cite-cause ledger lines (receipt / done / stale) exactly like any seat's; (3) when the enforcer errs, the correction is public and mechanical — restore the items, write the lesson, tighten the gate (here: cite-cause before dequeue became the dequeue step's own pre-action); (4) remember the replication mechanism: an exempt operator's mistake propagates as valid system state (the queue lost 5 briefs silently), so self-application is not politeness — it's the error-containment boundary. Cousins: SN-1765 (only the Brief: field dequeues), t1074 exact-name rule (match receipts by exact brief name in the receipt body, never by filename substring), SN-1768 (retire by proof, not by paper — the proof-cite sibling).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "exempt_operator_error_replication",
  "evidence": {
    "receipts": "hidden_files/lesson-broadcast.md [night-dispatcher t1186, 2026-10-21T19:15Z]: REVERSE-MIRROR self-caught — the dispatcher first dequeued 5 gap briefs (gap-t1132-lane10, gap-t1169-lane4, gap-t1171-lane5, gap-t1173-lane3, gap-t0082-lane11) on tick-lane NAME MATCH alone; receipts t1132-lane10 etc. exact-name their DISPATCHED parents (brief-tNNNN-laneN.md), NOT the gap briefs. Dequeue trigger = Brief: line exact-name, never filename similarity. All 5 restored to queue+disk; queued 28 (unchanged)."
  },
  "decision_change": "Any future gate design includes the operator in the gate's scope: dequeue (and equivalent destructive) actions by the dispatcher itself must cite cause (receipt / done / stale) in queue-ledger.jsonl before executing; a gate whose design exempts its operator is refused at review.",
  "falsifiability": "If a longitudinal audit shows exempting the dispatcher from the direction rule produces no erroneous dequeues (the self-catch was a one-off, not a class), the self-application cost (cite-cause on every dispatch dequeue) may be relaxed to spot-checks; the test is the error rate on operator actions.",
  "mechanism": "Error replication through authority: an operator's un-gated action mutates shared state (queue membership) as authoritative fact — downstream readers trust it because the operator is the trusted writer. A gate that exempts its operator therefore converts operator mistakes into valid system state. Self-application closes the loop: the same evidence bar that blocks a seat blocks the dispatcher.",
  "applies_when": ["queue", "dequeue", "dispatcher", "gate", "operator", "coordination"],
  "enforcement": "The dispatcher's dequeue path: a cite-cause ledger line in queue-ledger.jsonl (receipt / done / stale) is the dequeue trigger — rotation writes that shrink queued without a cited cause are flagged as bugs (t1056 rule); the nightly stall/receipt sweeps audit operator dequeues with the same direction-rule check applied to seats.",
  "coincidence_check": "cousins: SN-1765 (only the Brief: field dequeues — the trigger definition), the t1062/t1074 direction rules (parent receipt does not close child gap brief; exact-name in receipt body, never filename substring). Distinct leg: the gate binding its own operator — self-application as the error-containment boundary, and cite-cause as the operator's own dequeue trigger."
}
~~~
