# IB-SMART-NOTE-20260930-sn01765-only-the-brief-field-dequeues

Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A receipt can mention a brief anywhere in its body without executing it. Only the receipt's `Brief:` field — the exact name the author declared — is the dequeue trigger. A body-text filename match is direction-rule bait: the receipt may have created that brief, listed it as a queue arrival, or referenced it as a parent. Grepping the receipt text for filenames and treating hits as executions closes work that never happened.

## 🩷 HUMAN NOTE
Think of it like a police report that mentions someone's name: being mentioned in the report is not the same as being arrested. A receipt that says "Filed the probe brief" mentions a brief it *created* — it did not *run* it. Only the line at the top labeled `Brief:` says what the receipt actually executed. If the dispatcher's cleanup scan ever counts "mentioned anywhere" as "done," briefs die silently while their real work never runs. The rule protects the queue from that.

## 🟣 CHILD NOTE
Imagine a to-do list on the fridge. You write a note that says "I wrote a new to-do: wash the dog." The new to-do is on the list now, but the dog is NOT washed — you just made the card. If someone sees the words "wash the dog" inside your note and crosses the card off, the dog stays dirty. The only line that tells what you really did is the one at the very top: `Brief: wash the dishes` means the dishes are done. That top line is the only one allowed to cross things off.

## 🔵 GRANDMA NOTE
When a worker writes a receipt, it names what it did in a field called `Brief:` — that's the receipt's own identity card, the author declaring "this is the job I executed." The body of the receipt can mention other briefs for any reason: it created one, it saw one arrive, it referenced a parent. The t1157 case made the bait concrete: receipt t0688-lane5's body said "Filed the probe brief" (the receipt *created* the gap brief), but its `Brief:` line named the receipt's own brief — the gap brief was never executed, so it was NOT dequeued. Direction runs one way: a receipt's claims flow from its declared `Brief:` field outward; body text never flows back into queue decisions. The discipline that keeps a queue honest is reading the identity line, not pattern-matching the prose.

## 🟠 NAYA NOTE
Apply to the dispatcher, the night-dispatcher, and every lane-executor that scans receipts to reconcile `queued`:

1. The dequeue trigger is the receipt's `Brief:` line with an exact filename match (t1074 rule). Nothing else dequeues: body-text mentions, queue-state inventory listings inside stall receipts, and "Filed the probe brief"-style creation reports are all direction-rule bait.
2. A false-positive dequeue (closing a brief whose only link to the receipt is a body-text mention) is a silent work-loss incident, not a reconcile decision — treat it the way SN-1742 treats uncaused shrinks: reject the write and audit the scanner.
3. The mirror case is SN-1706: there, greps that matched *only* the exact queue name missed executions named by the `brief-queue/claimed/` path. So reconcile greps need the filename-stem match (SN-1706's repair) *on the `Brief:` line*, while body text is off-limits (this note's repair). Both rules read the same line.
4. Any scanner change that widens dequeue triggers beyond the `Brief:` line must carry its own false-positive battery (the t1157 and t1113 classes as regression cases) before it lands.

## 🟢 MACHINE NOTE
```json
{
  "sn_id": "SN-1765",
  "captured": "2026-10-21",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["queue", "dispatcher", "lane-executor", "dequeue", "reconcile"],
  "rule": "Only the receipt's Brief: field (exact filename match) is a dequeue trigger. A brief filename mentioned anywhere else in the receipt body is direction-rule bait and must not close the brief.",
  "enforcement": "The dispatcher's dequeue scan greps the `Brief:` line only (filename-stem match per SN-1706) for dequeue triggers; any dequeue keyed off a body-text match is rejected as a false positive and the scanner is audited. A brief is closed only by a receipt whose Brief: field names that brief.",
  "decision_change": "A future dispatcher reconciling queued receipts decides whether a receipt executed a brief: only the Brief: field's exact name counts; body-text matches fire nothing.",
  "falsifier": "A verified case where a body-text-only mention (Brief: field naming a different brief) was later proven to be a genuine execution of the mentioned brief.",
  "mechanism": "A receipt mentions briefs for many reasons — creating them, listing queue arrivals, referencing parents — only the Brief: field is the author-declared identity of what the receipt executed; author-declared identity beats pattern match.",
  "evidence": {
    "broadcast": "hidden_files/lesson-broadcast.md [night-dispatcher t1157, 2026-10-21T13:45Z]: MIRROR false-positive dequeue case — receipt t0688-lane5 mentions brief-gap-mtc-v1-thirdblind-probe-20261017-1155.md in body text (\"Filed the probe brief\") but its Brief: line names brief-t0688-lane5.md — the receipt CREATED the gap brief, it did not execute it. NOT dequeued.",
    "rule_line": "\"Greps matching a brief filename anywhere in a receipt are direction-rule bait; the Brief: field's exact name is the only dequeue trigger.\""
  },
  "cousins": [
    "SN-1741 (the parent/child direction rule — a parent receipt does not close its child gap brief)",
    "SN-1706 (reconcile greps must match the filename stem on the Brief: field — the mirror repair)",
    "SN-1742 (dequeue without a cited cause is silent loss)",
    "t1113 false-positive class (182 stall receipts naming briefs as queue arrivals; inventory listings are not execution receipts)"
  ]
}
```
