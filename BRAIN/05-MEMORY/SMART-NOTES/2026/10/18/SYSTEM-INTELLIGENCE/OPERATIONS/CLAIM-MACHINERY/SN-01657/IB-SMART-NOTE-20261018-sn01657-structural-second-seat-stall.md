# A Queue Full of Second-Seat Demands Is a Structural Stall — Reroute or Accept, Never Burn Ticks

**Intelligent Block:** IB-SMART-NOTE-20261018-sn01657-structural-second-seat-stall
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/seat-stall-20261019-0036.md (Naya Clarity Narzan, lane-executor run 2026-10-18 17:28 PDT / 2026-10-19 00:36 UTC) — all 30 briefs in `brief-queue/` evaluated in standing ORDERING order: 8 explicitly barred to non-Clarity seats on CLAIMABILITY header text, 17 refused by claim-brief.py exit 7 (second-seat demand on Clarity-authored parent work), 5 refused by exit 2 (seat-line/claimability bar); 0/30 claimable by the executor's seat. Queue delta vs prior stall: 29 → 30, the one new filing also exit-7-refused.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The lane-executor bound to the Clarity seat is structurally unable to work the current brief queue — 0 of 30 briefs claimable, because 17 demand a second seat on Clarity-authored parent work and 8 are gated non-Clarity on their headers. That is governance working correctly (a seat may not judge its own work — SN-01075), but the stall is structural, not situational: until a non-Clarity seat executes the backlog or the dispatcher decides to accept the stall, every Clarity lane-executor tick will produce only another stall receipt. Burning ticks expecting a different result is the failure; the intelligent move is the dispatcher decision — reroute to non-conflicted seats, or throttle the executor and own the stall.

## 🩷 HUMAN NOTE

Shawn — the work queue for the lane-executor is stuck, and it is stuck by design, not by accident. Thirty jobs are waiting; all thirty are jobs the Clarity seat is not allowed to touch — most are second reviews of Clarity's own earlier work (a seat can't judge its own work), the rest are explicitly reserved for other seats. The rule is right — but it means the Clarity executor will keep waking up, finding nothing it may touch, and going back to sleep, forever, until either someone else (Resolve's family, Naya 1, Naya 3, Nitro's team) picks the backlog up, or we formally decide the executor waits. What must not happen is burning hours of compute on ticks that can't possibly produce work. The rule this earned: when an executor's queue goes to zero claimable for three stalls in a row, the dispatcher either routes the backlog to unconflicted seats or accepts the stall on the record — it never just keeps ticking.

## 🟣 CHILD NOTE

Imagine a helper who is told: "You may never check your own homework, and you may never open the red envelopes — those are for the other helpers." Now imagine ALL the work on the desk is the helper's own old homework and red envelopes. The helper isn't broken and isn't lazy — the rules are working exactly right. But waking the helper up every morning to look at the same un-doable desk is silly. The grown-up fix: give the desk to a different helper, or admit the desk waits until the rules change. Never keep waking up the helper for nothing.

## 🔵 GRANDMA NOTE

It's like a shopkeeper who is forbidden from counting her own till and forbidden from opening the blue mail — and one morning every single job on the list is counting her own till or opening blue mail. Nothing is wrong with her, nothing is wrong with the rules. But sending her into the shop every hour to discover the same empty-of-doable-work list is wasteful. The manager has two honest choices: send a different shopkeeper, or write down "we're closed until the list changes." The dishonest choice is pretending next hour will be different.

## 🟠 NAYA NOTE

Cold successor: the stall-classification procedure for seat-bound executors.

1. On every stall, record the queue delta: count, and the class split (explicit-gate-barred / script-refused exit 7 second-seat / script-refused exit 2 seat-line), against the prior stall. The delta is the load-bearing field — it proves whether the stall is situational or structural.
2. Structural-stall signature: three consecutive stalls with claimability at or near 0% for the executor's seat AND the new filings being the same barred class. No new claimable class entering the queue = no reason the next tick differs.
3. On the signature: the dispatcher decides, on the record, one of two moves — (a) ROUTE: schedule the backlog to non-conflicted seats (Resolve family, Naya 1, Naya 3, Nitro), or (b) ACCEPT: note the accept-stall decision and throttle the executor ticks until a claimable brief appears. Silence-plus-reticking is the failure mode.
4. Classify the stall correctly in the receipt: structural (the queue's composition bars this seat) vs situational (briefs openable but nothing ready). The mirror lesson rides with the receipt — one line, not a report.
5. Falsifier to keep live: if a stall receipt ever shows a brief claimed from this queue by this seat, the structural claim lapses — reclassify and resume normal ticks.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1657",
  "title": "A Queue Full of Second-Seat Demands Is a Structural Stall — Reroute or Accept, Never Burn Ticks",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "CLAIM-MACHINERY"],
  "applies_when": ["claim", "brief-queue", "second-seat", "dispatcher", "queue-health", "stall", "seat-bound-executor"],
  "enforcement": "The stall receipt MUST carry the queue-delta field (count + class split vs prior stall). A queue-health check reads the delta: three consecutive stalls at ~0% claimability for the executor's seat forces the dispatcher's reroute-or-accept decision on the record. The scorer bounces any stall receipt that omits the queue delta, and any dispatcher tick that re-ticks without the decision after the third consecutive 0% delta.",
  "cousins": ["SN-01075 (author lane cannot be its own second seat — GOVERNANCE/MERGE-AUTHORITY: this note is the queue-level consequence, what happens when a whole queue is second-seat-demands against one seat)", "SN-1654 / CANDIDATE 645 (the step title is not the diagnosis — read exit codes: the exit-7/2 codes are the mechanical signal that makes the structural-stall classification cheap to detect)"],
  "evidence": {
    "stall_receipt": "hidden_files/twelve-lane-receipts/seat-stall-20261019-0036.md: 30 briefs evaluated in ORDERING order; 8 class-A (explicit non-Clarity CLAIMABILITY header), 17 class-B (claim-brief.py exit 7 — second-seat demand on Clarity-authored parent), 5 class-C (exit 2 seat-line bar); 0/30 claimable",
    "queue_delta": "29 → 30 vs seat-stall-20261018-2329.md; the single new filing (brief-gap-lane-scorer-20261018-1700-lane99.md, mtime 00:09 UTC) is also exit-7-refused — composition unchanged",
    "mirror_lesson": "receipt's own mirror: 'the stall is structural, not situational: until a non-Clarity seat executes these, every Clarity lane-executor tick produces only stall receipts' — with the dispatcher decision named"
  },
  "decision_change": "On the third consecutive ~0%-claimable stall for a seat-bound executor, the dispatcher (a) routes the barred backlog to non-conflicted seats, or (b) records an accept-stall decision and throttles the executor ticks — instead of burning ticks that cannot produce work.",
  "falsifier": "A Clarity lane-executor tick claims and completes a brief from this queue → the stall was situational, reclassify and resume. Or: the queue's composition changes (claimable briefs enter and get claimed) → the structural claim lapses by composition, not by verdict.",
  "mechanism": "claim-brief.py binds seat identity at claim time; the second-seat rule (SN-01075) refuses any brief whose parent work the claiming seat authored (exit 7), and CLAIMABILITY headers refuse non-matching seats outright (exit 2 / header-skip). The lane-executor runs under a fixed seat identity (Clarity). Over a queue whose every item is either Clarity-parent work or non-Clarity-gated, claimability is exactly zero BY CONSTRUCTION — no amount of re-ticking changes it, because the barrier is the seat identity, not the queue contents. The stall ends only when a different seat acts or the queue composition changes."
}
```

