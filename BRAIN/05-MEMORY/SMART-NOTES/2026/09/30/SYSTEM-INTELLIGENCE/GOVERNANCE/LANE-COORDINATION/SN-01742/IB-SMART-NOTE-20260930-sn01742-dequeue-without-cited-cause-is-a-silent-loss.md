# Dequeue Without a Cited Cause Is Indistinguishable From a Silent Loss — Every Shrink of the Queue Needs a Ledger Line

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01742-dequeue-without-cited-cause
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The same gap brief (`brief-gap-t1034-lane10.md`) leaked out of the dispatch queue twice in one day — re-registered at t1038, leaked again by t1056, sitting on disk unregistered with no receipt and no sign-in. Re-registering treats the symptom; the t1056 postmortem named the root class: queue membership has no append-only ledger, so the dequeue path can silently drop entries and the only tripwire is a full disk-vs-rotation diff. The rule: every rotation write that shrinks the queued list must cite its cause (receipt id, done, stale) in an append-only ledger line; any write that shrinks queued without a cited cause is a bug and is rejected or reverted. Re-registration is triage, not a fix. The periodic full diff stays as the tripwire until the ledger is live.

## 🩷 HUMAN NOTE

Shawn — a to-do item kept falling off the team's task list, twice in one day, with no record of who removed it or why. Putting it back on the list didn't fix anything — whatever pulled it off can pull it off again. The real fix: every time an item leaves the list, the move gets written down with its reason, so a disappearance with no reason is instantly visible as a bug.

## 🟣 CHILD NOTE

Imagine a classroom attendance sheet where names can be erased with no note. If a name vanishes, nobody knows whether the kid graduated or someone erased it by accident. The fix: every erasure gets a signed reason line in a separate logbook — "graduated," "transferred," "moved away." A name erased with no log line is the alarm, not the paperwork.

## 🔵 GRANDMA NOTE

Like a grocery list on the fridge that people can cross items off. If "milk" is crossed off with no initials, you don't know if someone bought it or someone's kid scribbled. The rule: you cross it off only with your initials and the receipt. A crossed-off item with no initials gets treated as a mistake, not a purchase.

## 🟠 NAYA NOTE

Apply to the dispatcher and every lane-executor that writes the rotation: (1) queue membership needs an append-only ledger — every dequeue appends `{brief, cause, receipt|done|stale, tick}`; (2) any rotation write that shrinks `queued` without a cited cause is a bug — reject or revert the write, do not merely re-register the lost brief; (3) re-registration after a leak is triage: it restores the queue but fires nothing about the writer, so it must trigger a writer audit, not a close; (4) until the ledger is live, the full disk-vs-rotation diff (t1038's method) remains the mandatory tripwire — never skip it because "the queue looked fine"; (5) note the t1052 lesson in the same chain: the rotation is rewritten inside the tick window while concurrent executors also write (observed mid-tick mutation) — so shrink-write auditing must rest on the latest read, never the first.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "dequeue-without-cited-cause-is-a-silent-loss",
  "sn": "SN-1742",
  "title": "Dequeue Without a Cited Cause Is Indistinguishable From a Silent Loss: Every Shrink of the Queue Needs a Ledger Line",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-20",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["dispatcher", "brief-queue", "dequeue", "rotation", "queue-membership", "reconcile"],
  "enforcement": "Every rotation write that shrinks the queued list must append a cause-cited ledger line (brief name + cause: receipt id / done / stale + tick); any write that shrinks queued without a cited cause is a bug — the write is rejected or reverted, and the incident opens a writer audit rather than a re-registration. Until the ledger is live, the full disk-vs-rotation diff (t1038 method) is mandatory each dispatch tick as the tripwire; a tick that skips it is an unverified tick.",
  "evidence": {
    "t1056": "lesson-broadcast.md [night-dispatcher t1056, 2026-10-20T18:22Z]: reverse-phantom RECURRENCE — brief-gap-t1034-lane10.md re-registered at t1038 leaked a second time (on disk, never registered, no receipt, no sign-in), plus second unregistered orphan brief-gap-lane-scorer-20261020-1120-lane0.md; both re-registered to queued. Root class named: queue membership has no append-only ledger — re-registration is not a fix when the dequeue path can silently drop entries again. Fix owed: dequeue operations must cite the cause in a ledger line; any rotation write that shrinks queued without a cited cause is a bug",
    "t1052": "lesson-broadcast.md [night-dispatcher t1052, 2026-10-20T17:40Z]: rotation mutated mid-tick by a concurrent lane-executor during a reconcile — reconcile conclusions rest on the LATEST read, never the first",
    "t1038": "lesson-broadcast.md [night-dispatcher t1038, 2026-10-20T15:02Z]: reverse-phantom — a lane-scorer gap follow-up sat on disk untracked; registered back into queued; rule: writers must register what they write"
  },
  "decision_changed": "How the dispatcher responds to a leaked brief: re-registering is now classified as triage, not repair — the durable response is the cause-cited dequeue ledger plus a writer audit of every shrink write since the leak. Deploys/operates against: dispatcher rotation writes, reconcile sweeps, lane-executor re-registrations.",
  "falsifier": "A full disk-vs-rotation diff run across 30+ days of ticks showing zero silent drops while cause-citation is enforced — demonstrating the citation ledger adds no detection value beyond the periodic diff (i.e., the diff alone always catches every loss before it matters).",
  "mechanism": "The rotation is a mutable list file rewritten inside the tick window while concurrent lane-executors also write (t1052 observed a mid-tick mutation), so a shrink write with no cited cause is observationally identical to a silent loss — no forensic evidence distinguishes 'deliberately dequeued as done' from 'dropped by a racing write'. Only an append-only membership ledger makes every shrink auditable at write time; the full diff is a periodic tripwire, not a continuous one. Without the ledger, detection latency is bounded below by the diff cadence and the loss window is unknowable.",
  "cousins": ["t1038 reverse-phantom (writers must register what they write — the write-side sibling)", "t1052 reconcile-on-latest-read (the read-side sibling: mid-tick mutation)"]
}
~~~
