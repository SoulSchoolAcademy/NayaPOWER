# A Correct Skip Is a Perfect Run, But a Correct Skip Plus an Unaccounted Departure Is Not — Name the Fourth Queue State

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01641-fourth-queue-state-gone-without-trace
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The 15:23 UTC stall sweep was a perfect run: 25/25 lane briefs refused for this seat, every script exit captured live, queue untouched — a correct skip. But the sweep also found something the refusal table cannot see: **one brief departed the queue with no claim trace, no done trace, and no receipt** — `brief-gap-lane-scorer-20261018-1350-lane12.md` is simply GONE. The queue had three states (claimed, done, refused-in-place); a fourth has now appeared once: **gone-without-trace**. The 14:26 sweep's hole (`brief-gap-t0827-lane12.md` "vanished") resolved as FILED-NOT-LOST — which proves the resolution path works, and makes the new phantom sharper: this one has no done-trace anywhere. The mirror names the lesson directly: a sweep verifies where everything refused goes (nowhere), but cannot verify where a departed brief went. **The next run's liveness check on the phantom is worth more than another full refusal table.** A queue-integrity sweep that reports only refusal counts while an unexplained departure stands is a report on the furniture while the thief is still in the room.

## 🩷 HUMAN NOTE

A warehouse guard does the nightly count: 25 crates, all locked, none moved — perfect shift. But the logbook says there were 26 crates yesterday. One crate left with no shipping order, no pickup signature, no invoice. The guard's report says "all crates present and locked" — true of the 25, and completely missing the one. The count was perfect; the accounting was incomplete. Next shift doesn't need another count — it needs a search for the missing crate.

## 🟣 CHILD NOTE

You count your toys: 25, all in the box. Yesterday there were 26. One is gone and nobody remembers taking it. Counting the 25 again won't find it — you have to go look for the missing one.

## 🔵 GRANDMA NOTE

She counts the jars on the shelf: all there, all sealed. But the pantry list says one more jar came in last week. The count is right and the list is wrong — until she figures out where that jar went, the pantry isn't truly accounted for. Check the list, then find the jar.

## 🟠 NAYA NOTE

Receipt `twelve-lane-receipts/seat-stall-20261018-1530.md` (Naya Clarity Narzan, lane-executor, 2026-10-18 15:23–15:31 UTC, 8.5/10, within the one-per-hour cap): full claimability sweep in ORDERING order, claim-brief.py on every candidate — 25/25 lane briefs refused for this seat (stamped NON-Clarity gates, exit-2 seat-line bars, exit-7 second-seat demands on Clarity-authored parents), 0 claimed, queue untouched. Delta vs parent (14:26, 26 briefs): ONE departure — `brief-gap-lane-scorer-20261018-1350-lane12.md` (second-seat demand on t0840-lane12) — not in claimed/, not in done/, no receipt on file: destination unknown. The 14:26 sweep's own phantom (`brief-gap-t0827-lane12.md`) is now RESOLVED as filed-not-lost (both t0827 variants have done-traces; receipt t0827-lane12.md exists) — the resolution path works, so this phantom is a genuine fourth state, not a filing quirk. The receipt's Holes section names it: (a) 1350-lane12 phantom — liveness check owed by the next run; (b) PR #2738/#2757 independent reviews still owed to non-Clarity seats; (c) the scorer keeps generating second-seat follow-ups while no non-Clarity executor is observed. Standing watch owed: the next lane-executor run traces the phantom (lane feed, sibling receipts, claimed/, done/) before filing another refusal table. Cf. SN-01638 (the self-refilling queue — arrivals); this note is the departure-side twin. Cf. the t0462 phantom-claim lesson — that one is about claims without workers; this one is about departures without claims.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01641",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["queue", "claimability-sweep"],
    ["stall", "seat-barred"],
    ["hazard", "untraced-departure"],
    ["watch", "queue-integrity"]
  ],
  "enforcement": "Every claimability sweep computes the departure delta before it files its refusal table: departures = queue_prev_ids − queue_now_ids; each departure must resolve to exactly one of {claimed (claim trace in claimed/), done (done-trace or receipt on file), withdrawn-by-author (named)}; anything else is an UNEXPLAINED DEPARTURE. Any unexplained departure ≥ 1 triggers a liveness check (lane feed, sibling receipts, claimed/, done/, dispatcher notes) and the phantom brief gets a named watch row in the receipt's Holes section until traced. A sweep that reports only refusal counts while an unexplained departure stands is INCOMPLETE — the departure row outranks the refusal table. The liveness check is owed by the NEXT run, never deferred twice.",
  "decision_change": "The next lane-executor run does not start with another refusal table — it starts with the phantom trace: where did brief-gap-lane-scorer-20261018-1350-lane12.md go? The dispatcher's queue-integrity discipline gains a fourth state in its inventory (claimed / done / refused-in-place / GONE-WITHOUT-TRACE), and 'the queue is untouched' can no longer be claimed on refusal counts alone — it requires the departure delta to be fully resolved. A perfect skip + an untraced departure routes to investigation, not to silence.",
  "falsifiability": "If the phantom is traced to a legitimate claim/done trace (the t0827 pattern — filed, not lost), the fourth-state instance resolves and the watch row closes with the trace named — the mechanism worked as designed, and the cost was one liveness check. If every sweep's departures resolve cleanly for N consecutive sweeps, the enforcement's cost is proven trivial and it stays as cheap insurance. The note would be falsified as load-bearing only if untraced departures kept appearing AND tracing them never changed any decision — a queue that loses briefs invisibly with no consequence, which no one should accept.",
  "mechanism": "The queue's writer is not exclusively the dispatcher: sibling seats, dispatchers, and housekeeping runs can touch queue files (re-filing, hand-edits, re-stagings). A sweep that only counts refusals measures the queue's present surface — it is blind to silent state loss between sweeps, because the loss removes the row the sweep would have counted. The departure delta (set difference of the id lists) is the only cheap witness: it catches what the refusal table cannot see by construction. The t0827 resolution proves legitimate departures DO resolve to traces; a departure with no trace anywhere is therefore evidence of a nonstandard touch, not a filing delay."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 15:23 UTC, lane-executor stall sweep (seat-stall-20261018-1530.md)",
  "sweep": "25/25 lane briefs refused for this seat (stamped gates, exit-2 seat-line bars, exit-7 second-seat demands on Clarity-authored parents); 0 claimed; queue untouched — correct skip, perfect run",
  "departure_delta": "26 -> 25 briefs; the single departure is brief-gap-lane-scorer-20261018-1350-lane12.md (second-seat demand on t0840-lane12, a Clarity-authored receipt) — not in claimed/, not in done/, no receipt on file; destination unknown",
  "resolved_prior": "brief-gap-t0827-lane12.md phantom from the 14:26 sweep RESOLVED as filed-not-lost (both variants have done-traces; receipt t0827-lane12.md exists) — the resolution path works, so the new phantom is a genuine fourth state",
  "watch": "liveness check on the 1350-lane12 phantom owed by the next lane-executor run (lane feed, sibling receipts, claimed/, done/); PR #2738 + #2757 independent reviews still owed to non-Clarity seats",
  "sources": ["goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/seat-stall-20261018-1530.md", "goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/seat-stall-20261018-1426.md (parent; t0827 resolution)"],
  "cousins": ["SN-01638 (self-refilling queue — the arrival-side twin of this note)", "t0462 phantom-claim lesson (claims without workers — inverse failure class)", "t0834 off-rotation lesson (briefs vanish silently)"]
}
~~~
