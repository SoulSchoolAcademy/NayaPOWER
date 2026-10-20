# When Every Refusal Is Seat-Grounded, the Bottleneck Is Composition, Not Content

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01715-composition-not-content-queue-bottleneck
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 22:08 PDT distillation tick (2026-10-19) from hidden_files/twelve-lane-receipts/gate-stall-20261020-0449.md and hidden_files/twelve-lane-receipts/seat-stall-20261020-0502.md (two consecutive identical-composition stalls, 0/29 claimable). No new #1354 comments were read this tick (#1354 hit GitHub's 2500-comment hard cap 2026-10-10; director pass is the single reader).

## ✦ IN A NUTSHELL

Two consecutive Clarity lane-executor runs (04:49Z, 05:02Z) stalled at 0/29 claimable with byte-identical queue composition — 10 explicit non-Clarity claimability gates plus 19 exit-7 second-seat demands on Clarity-authored parent work. The earlier healthy drain (four briefs cleared by non-Clarity seats in the 00:36→03:12 window) went quiet over the last ~1.8 hours. The durable finding: **when every claim refusal is exit-2/7 on seat grounds, the bottleneck is composition, not content.** One hundred percent of the pending work demands a second seat, so the single-seat lane-executor cadence cannot move it no matter how well it runs — the cadence produces stall receipts, not progress. The durable rule: **the dispatcher keeps a seat-eligibility mix on the queue** — file briefs claimable by each active seat, or hand the second-seat backlog explicitly to non-Clarity seat runs. Don't fix the runner's stride when the track is pointed at a different runner.

Why this is brain-grade: it converts a recurring stall symptom ("everything is barred to me") into a routing diagnosis with a named owner (the dispatcher, not the executor). The existing stall-receipt machinery is already the watch that catches it — the refinement is the response obligation: three consecutive identical-composition stalls with zero claimables trigger the dispatcher, not a fourth identical receipt.

## 🩷 HUMAN NOTE

Shawn — the Clarity lane-executor has stalled two runs in a row: all 29 queued briefs are barred to her seat — some need other seats explicitly, most need a second seat on Clarity-authored work. The stall-receipt machinery is working (that's how we know, precisely). The lesson: when every refusal is on seat grounds, the bottleneck is what the queue is made of, not what's in the briefs. The fix belongs to dispatch: keep a mix of briefs the running seats can actually claim, or send the second-seat backlog to the seats it needs. Filed as Smart Note candidate SN-01715 with the stall-receipt watch as its enforcement.

## 🟣 CHILD NOTE

Imagine a chore list on the fridge with 29 chores, and every single chore says "only your brother can do this one." You read the list very carefully — twice — and you're a great reader, but you still can't do a single chore. The problem isn't your reading. The problem is the LIST: nobody put a chore on it that YOU can do. The fix: whoever writes the list should put some chores for everyone, or give your brother's chores to your brother. **When everything is blocked for the same reason, the block is in the list, not in the person.**

## 🔵 GRANDMA NOTE

Dear, the office worker checked the task basket twice and every task in it said "for the other department." She checked perfectly — that's why the check is trustworthy. The wise manager's lesson: when every single item is refused for the same reason, you don't retrain the worker, you rebalance the basket. **Put some tasks in the basket for the hands that are actually there, or send the rest where they belong.** The basket is the manager's job, not the worker's.

## 🟠 NAYA NOTE

Dispatcher seat: the Clarity lane-executor is in a steady-state stall — two consecutive runs, identical 29-brief composition, zero claimable (10 explicit non-Clarity gates, 19 exit-7 second-seat demands). The executor's claim machinery is verified healthy; the drain by non-Clarity seats has gone quiet. Your standing obligation: keep a seat-eligibility mix on the queue so no running cadence starves at zero claimable. Either file briefs the active seats can claim, or hand the second-seat backlog explicitly to non-Clarity seat runs. The executor's stall receipts are the watch — when three consecutive receipts show identical composition at zero claimable, that's the composition alert, and the response is yours. The executor's job is the correct skip; yours is the composition that makes the skip unnecessary.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01715",
  "title": "When every refusal is seat-grounded, the bottleneck is composition, not content",
  "captured_utc": "2026-10-20T05:08:00Z",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["dispatch", "lane-executor", "queue", "composition", "seat-eligibility", "stall"],
  "enforcement": "The lane-executor stall receipt (cap: 1/hour) is the standing watch: whenever 0 briefs are claimable, the receipt records the refusal classes and queue composition. Three consecutive stall receipts with identical composition and zero claimables = composition alert to the dispatcher in the receipt's Mirror lesson. Response obligation: within 24h the dispatcher files a mixed-eligibility brief or routes the second-seat backlog to a non-Clarity seat run. Verification: the Clarity claimable count moves above 0 or the second-seat backlog drains; a mixed-eligibility response wave that still stalls at 0 claimable = this lesson falsified (the bottleneck was not composition).",
  "evidence": {
    "receipt_a": "hidden_files/twelve-lane-receipts/gate-stall-20261020-0449.md (04:49Z): 29 live candidates, every claim refused — 8 explicit non-Clarity gates skipped on gate text, 2 exit-2 seat-line, 19 exit-7 parent-authorship; queue membership byte-identical to the 03:12Z stall receipt.",
    "receipt_b": "hidden_files/twelve-lane-receipts/seat-stall-20261020-0502.md (05:02Z): same 29 filenames, 0 claimable by the Clarity seat; the 00:36→03:12 drain trend (four briefs cleared by non-Clarity seats) quiet over the last ~1.8h.",
    "context": "#1354 board fetch skipped this tick: issue_1354_comments=2500 = GitHub hard cap (commenting disabled 2026-10-10 per shared-state.json); watermark 6101230756 stands."
  },
  "cousins": ["SN-01709 (dispatch-time freshness gate — dispatcher-side dispatch machinery; this is the dispatcher-side composition counterpart)", "STALL-RECEIPT CAP machinery (one stall receipt per hour; this note is the response obligation the cap alone doesn't carry)", "SN-01328 (brief-premise-rot — the watch that catches a different class of composition failure)"],
  "decision_change": "The dispatcher's filing decision: previously briefs were filed without regard to the seat-eligibility mix of the pending queue; after this lesson the dispatcher keeps a mix claimable by each active seat on the queue (or routes the second-seat backlog explicitly to non-Clarity seat runs), so no lane-executor cadence starves at zero claimable.",
  "mechanism": "Second-seat demand concentrates pending work on seats that are not currently running. The lane-executor cadence is single-seat: it can only advance work it can claim. When the queue composition excludes the running seat entirely, cadence converts to stall receipts instead of progress — the cure is at the composition point (dispatch), not at the execution point.",
  "falsifiability": "If the dispatcher responds per the enforcement (mixed-eligibility wave filed, or second-seat backlog routed to non-Clarity seats) and the Clarity lane-executor still stalls at 0 claimable, the bottleneck was not composition and this lesson is falsified. If the stall breaks within 24h of the response, the mechanism holds."
}
~~~
