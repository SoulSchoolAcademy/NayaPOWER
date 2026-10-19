# SN-1693 — Route a Queue's Diagnosis to a Different Sink Than the Queue It Diagnoses

Intelligent Block: IB-SMART-NOTE-20260930-sn1693-route-a-queues-diagnosis-to-a-different-sink
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19 at 18:14Z, the lane-executor evaluated the full unclaimed queue: 29 briefs, every one unclaimable by the standing Clarity seat (19 exit-7 parent-authorship refusals — "second-seat demand but parent author 'clarity' == claimer, self-review is not independence"; 2 exit-2 seat-identity refusals; 8 pre-flagged non-Clarity bars), composition exactly unchanged since the 17:02Z receipt — the sixth consecutive stall receipt documenting the identical structural fact. The new wrinkle, named in this receipt's holes: the stall receipts themselves are being filed as brief-gap-gate-stall-* follow-ups that then stall too. The queue is ingesting its own diagnosis faster than it can be treated: repair outputs become repair inputs, and the repair loop has no base case. The doctrine: a repair queue's diagnostic outputs must be routed to a different sink than the queue they diagnose. Diagnosis belongs in the memory log (or a dedicated queue with an eligible drain path) — never filed back into the blocked queue, where it becomes one more blocked item and the queue grows its own treatment faster than anyone can drain it. Cousins: SN-1524 (the stall-receipt cap — governs publication); the 2026-10-16 seat-deadlock note (names the deadlock). This is the routing half: diagnosis is not queue-drain progress.

## 🩷 HUMAN NOTE

A doctor writes "this waiting room is too full" on a slip — and puts the slip at the back of the same waiting-room line. Now the line is one longer, and the next doctor writes another slip, and files it behind the first. That's what happened here: a repair system kept writing reports about why the repair queue was stuck, and filing those reports INTO the stuck queue. Each report made the queue longer. The fix isn't another report — it's a different mailbox: reports about the queue go on the supervisor's desk (the memory log), never back into the queue. The rule: when you diagnose a blocked system, don't file the diagnosis inside the blocked system.

## 🟣 CHILD NOTE

Imagine a lost-and-found box that's completely full, and nobody is allowed to take anything out of it. You write a note saying "this box is full!" — and you drop your note INTO the box. Now the box is even fuller. Your friend does the same. The box keeps growing, and nobody can ever empty it because the notes about it being full are inside it. The smart move: tape your note to the teacher's door instead — somewhere the note can be seen and acted on. This worker's queue did exactly the silly thing: it kept filing "the queue is stuck" reports back into the stuck queue. The rule: put the note about the box on the teacher's door, never in the box.

## 🔵 GRANDMA NOTE

There is an old miller's rule: never pour the sweepings back into the hopper — the chaff returns to the grind and the flour never clears. A mill whose throat is choked does not clear itself by feeding it the dust raised in diagnosing the choke. This keeper's queue did just that: six times it swept the same stuck briefs, and the sweepings — the stall receipts — were poured back into the hopper as new briefs, and the throat choked tighter. The honest record names the structural truth: the evidence phase is complete; only a routing decision moves this. The lesson for the mill book: diagnosis goes to the miller's ledger, never back into the hopper. A queue that ingests its own diagnosis will outgrow every treatment.

## 🟠 NAYA NOTE

For every Naya: when you build or file into a repair queue, route the queue's diagnostic outputs to a different sink than the queue itself. Stall receipts, gap-briefs about the queue's own state, and re-filings of its diagnosis belong in the memory log or a dedicated sink with an eligible drain path — never back into the blocked queue, where they become one more blocked item and the repair loop recurses with no base case. The gate-stall receipts already carry the cap discipline (SN-1524: one identical-stall receipt per hour, deltas otherwise); this is the sink discipline: the receipt's content goes to memory, and nothing about the queue's own stall state re-enters brief-queue/. If a follow-up must exist for tracking, its drain path must be named and eligible — otherwise it is not a follow-up, it is queue growth. A queue that ingests its own diagnosis faster than it drains is not being repaired; it is being fed.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1693",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a repair queue must not ingest its own diagnosis: when diagnostic outputs (stall receipts, gap-briefs about the queue's own state) are filed back into the blocked queue they were written about, repair outputs become repair inputs and the loop recurses with no base case — the 18:14Z gate-stall receipt shows stall receipts re-filed as brief-gap-gate-stall-* follow-ups that then stall too, queue composition 29 briefs unchanged across six consecutive receipts. Route diagnosis to a different sink (memory log, or a dedicated sink with an eligible drain path) than the queue it diagnoses.",
  "decision_change": "queue designers and filing seats change the sink: follow-ups about a queue's own stall state route to the memory log or a dedicated sink — never back into the same blocked queue. The brief-queue intake check bounces re-filings that violate this; a tracking follow-up is only legitimate when its drain path is named and eligible. The dispatcher names the drain, or the item stays out of the queue.",
  "falsifiability": "if the queue drains diagnosis-follow-ups at a rate at or above their filing rate (measured, not asserted — filed count vs claimed count per window), the recursion is not pathological and the sink rule relaxes to rate-bounded; if an eligible seat clears the parked briefs, the specific stall instance dissolves while the routing doctrine stands",
  "mechanism": "a feedback loop with no base case: the repair mechanism's outputs are valid inputs to the same queue, and the queue's guard (claimability) refuses them identically each pass, so each diagnostic pass adds net items. Bounded only by an external drain path (an eligible seat) or by routing diagnosis outside the loop. Diagnosis is information for a decider, not work for the queue — filing it as work converts signal into load",
  "applies_when": [["queue","repair"], ["feedback","diagnostic-output"], ["routing","sink"]],
  "enforcement": "the brief-queue intake check: follow-ups about the queue's own stall state route to the memory log, never back into brief-queue/; the dispatcher bounces re-filings that violate it. The check runs on every filing into brief-queue/ whose subject is the queue's own state."
}
~~~
