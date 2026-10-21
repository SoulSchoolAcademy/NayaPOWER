# A Queue Listing Mention Is Anti-Evidence: An Inventory Line Is Not an Execution Receipt

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01752-queue-listing-mention-is-anti-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A dispatcher receipt sweep found 182 stall receipts (`gate-stall-*`, `seat-stall-*`) that name queued briefs as queue ARRIVALS in their queue-state inventory lines. A naive matcher would read those lines as receipts and close the briefs — but a queue listing says "this brief was sitting here, open." It is evidence the brief was NOT done. The rule is the third leg of the t1062/t1074 direction rule (SN-01741 / CANDIDATE 732): (1) the receipt post-dates the brief, (2) the receipt's body bytes contain the exact queued brief filename claiming THIS brief's work, (3) a match found only in a queue-arrival/departure listing is anti-evidence — it reports the brief OPEN. Presence is not completion: an inventory listing proves the brief was still waiting at that receipt's write time, which argues against closure, never for it.

## 🩷 HUMAN NOTE

Shawn — when the dispatcher asks "did this job finish?", it hunts for the job's receipt. Tonight's sweep found 182 receipts that list jobs as "arrived in the queue." If the check counts a listing line as proof-of-completion, it would mark open jobs done. But that line means the job was sitting there waiting — proof it was open, not closed. New rule: a job is closed only by a receipt whose contents name that exact job and came after it. A listing line counts against closing, never for it.

## 🟣 CHILD NOTE

Imagine the teacher's attendance list and your homework checkmark. The attendance list says you were in class — it does not say you finished your homework. You don't get a gold star for showing up on the list; the star comes from the finished paper. A name on the waiting list is proof the work wasn't done yet.

## 🔵 GRANDMA NOTE

Like a restaurant's waitlist: your name on the waitlist means you are still waiting for a table, not that you have eaten. Crossing your name off the "finished" list just because it appeared on the waitlist is backwards — the waitlist proves you had not been seated yet. Presence on the list is evidence of waiting, never of being done.

## 🟠 NAYA NOTE

Apply to every dispatcher receipt sweep and queue reconcile before any rotation write: implement the three-leg close-criteria gate. (1) The receipt post-dates the brief. (2) The receipt's body bytes contain the exact queued brief filename claiming THIS brief's work (SN-01741 / CANDIDATE 732). (3) Exclude listing mentions: if the only match for a brief inside a receipt is a queue-arrival/departure inventory line (stall/state receipts' queue-state listings), that match is anti-evidence — the brief was OPEN at that receipt's write time, so it cannot close on that receipt. When scanning stall receipts (`gate-stall-*`, `seat-stall-*`), skip their queue-state listing blocks as a match surface entirely. A rotation write that dequeues a brief on a listing-mention match alone is rejected and rolled back; the audit names the anti-evidence leg. Cousins: SN-01741 (the parent/child direction rule — this is its third leg), CANDIDATE 730 (reconcile conclusions rest on the latest read — read the receipt's listing block as state-at-write-time, not as a claim).

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "queue-listing-mention-is-anti-evidence",
  "sn": "SN-1752",
  "title": "A Queue Listing Mention Is Anti-Evidence: An Inventory Line Is Not an Execution Receipt",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatcher", "reconcile", "receipt", "receipt-sweep", "queue-state", "queue-reconcile", "dequeue"],
  "enforcement": "The dispatcher receipt sweep's close-criteria gate implements the three-leg direction rule: a queued brief is closed by a receipt ONLY when (1) the receipt post-dates the brief, (2) the receipt's body bytes contain the exact queued brief filename claiming THIS brief's work, and (3) the match is NOT based on a queue-arrival/departure inventory line inside a stall or state receipt — a listing mention is anti-evidence and reports the brief OPEN. Stall receipts' (gate-stall-*, seat-stall-*) queue-state listing blocks are excluded as a match surface. Any rotation write that dequeues a brief whose only 'receipt' hit is a listing mention is rejected and rolled back; the audit names the anti-evidence leg.",
  "evidence": {
    "t1113": "lesson-broadcast.md [night-dispatcher t1113, 2026-10-21T04:32Z]: MIRROR receipt-sweep false-positive class — 182 stall receipts (gate-stall-*, seat-stall-*) name queued briefs as queue ARRIVALS in their queue-state listings; 'an inventory listing is not an execution receipt.' The t1062/t1074 direction rule gained its third leg: (1) receipt post-dating the brief, (2) receipt claiming THIS brief's work (Brief: field / exact-name claim), (3) a mention in a queue-arrival/departure listing is anti-evidence — it reports the brief OPEN. Sweep verdict stood at 0/30; throttle held."
  },
  "decision_changed": "Whether a queued brief is closed as 'done' when a stall/state receipt's queue-state listing names it: listing mentions no longer count as receipt hits — the sweep keeps the brief OPEN instead of falsely closing it.",
  "falsifier": "A documented, ratified receipt convention where queue-arrival/departure listings explicitly record claimed/executed briefs with their verdicts (making the listing an attestation of work, not a presence inventory); then a listing mention would be evidence FOR closure and this rule's premise would be false. Alternatively: 50+ receipt sweeps closing briefs on listing mentions alone with zero false closures.",
  "mechanism": "A queue-state listing is a presence inventory — it enumerates which briefs were sitting in the queue (open) when the receipt was written. An execution receipt is an attestation of work performed on THIS brief. Presence is not completion: treating a presence line as a completion attestation confuses the queue-state name-space with the receipt-claim name-space. The inventory proves the brief was still OPEN at receipt time — evidence against closure, not for it.",
  "cousins": ["SN-01741 / CANDIDATE 732 (the parent/child direction rule; this note is the third leg of that rule's close-criteria gate)", "CANDIDATE 730 (reconcile conclusions rest on the latest read)"]
}
~~~

