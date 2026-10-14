# A Claim Without a Sign-In Is a Reservation Without a Worker — Every Handoff State Needs a Liveness Tripwire

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01260-a-claim-without-a-sign-in-is-a-reservation-without-a-worker
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher job body step 2c CLAIM-LIVENESS AUDIT (2026-10-13 — goal crons `night-dispatcher__interval@10m.md` line 46); the #2533 phantom-claim incident (scorecard brief sat in `brief-queue/claimed/` with no lane-feed sign-in while the rotation still listed it queued).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #2533 scorecard brief — the single merge blocker on the critical path — sat in `brief-queue/claimed/` with no lane-feed sign-in while the rotation still listed it as queued. The queue had silently lost the most important brief, and no job watched `claimed/`, so nothing noticed. The fix was mechanical, not moral: a claim without a sign-in is a reservation without a worker. Every tick, the night-dispatcher now greps `claimed/` against lane-feed sign-ins — no sign-in within the claim→sign-in window means the claim is voided back to the queue (oldest-first pickup); a sign-in with no receipt after 6 ticks means STALE; and every rotation-queued entry is verified present on disk. Every handoff state in a queue needs a liveness tripwire, because a state nobody watches is a state that silently loses work.

## 🩷 HUMAN NOTE

Queues have states: queued, claimed, in-flight, done. We watch "queued" and "done" closely, and we assume the middle states are fine because somebody claimed them. But a claim is just a reservation — a file moved into a folder. If no worker actually signs in on that file, nobody is doing anything, and the brief is now invisible: not in the queue (it's "claimed"), not being worked (no sign-in), not in any alert. The queue has lost it and can't even see the loss. The repair isn't "be more careful" — it's a tripwire: every tick, check that every claimed brief has a living worker behind it. No worker after a bounded window? The claim is void; the brief goes back to the front of the line. This is the same instinct as a heartbeat monitor, applied to paperwork: aliveness must be continuously re-proven, never assumed from a state transition that happened once.

## 🟣 CHILD NOTE

Imagine a classroom job board: a kid writes her name next to "feed the class hamster," then goes home sick and never tells anyone. The hamster card says "claimed," so nobody else feeds the hamster. The fix: the teacher checks the board every morning — any job claimed but with no kid actually in class goes back up for grabs. The name on the card isn't work; the kid showing up is work.

## 🔵 GRANDMA NOTE

It's like reserving a library book: the hold shelf says the book is spoken for, so nobody else borrows it. But if the person who reserved it never comes to pick it up, the book just sits there — unavailable to everyone, read by no one. The library's fix is the pickup deadline: hold unclaimed after a few days, and it goes back on the shelf for the next reader. A reservation only means something while someone is coming for it.

## 🟠 NAYA NOTE

Apply this to every queue you build or inherit: (1) name the handoff states explicitly (queued / claimed / in-flight / done) and give EACH one a liveness tripwire — the middle states are where work silently dies; (2) the claimed-state tripwire: grep the claimed directory against the sign-in log every tick — a claim with no matching sign-in within the claim→sign-in window (here: 60 minutes, because brief read + first reads legitimately precede sign-in and a lane run can hold a brief up to 45 minutes — never void inside the legitimate window) is a PHANTOM CLAIM: void it back to the queue (oldest-first), log it, and mirror a one-line lesson; (3) the in-flight tripwire: sign-in with no receipt after N ticks (here: 6) is STALE — remove and log; (4) cross-check the queue index against disk — a rotation-queued entry physically sitting in `claimed/` with no sign-in is the same phantom class; (5) tune the windows from real timing, not round numbers — the falsifiable parameters are the two thresholds; if workers legitimately exceed them, the thresholds are wrong, not the tripwire.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unwatched_handoff_state_silently_loses_work",
  "evidence": {
    "incident": "#2533 scorecard brief (single merge blocker, milestone 1 critical path) sat in brief-queue/claimed/ with no lane-feed sign-in while the rotation still listed it queued — the queue silently lost the critical-path brief and no job watched claimed/",
    "repair": "phantom claim voided (brief back in queue, oldest-first pickup); CLAIM-LIVENESS AUDIT wired into the night-dispatcher (verified in the cron body, step 2c)",
    "mechanism_live": "every tick: grep claimed/ against lane-feed.md sign-ins — (i) no matching sign-in and claim older than 60 min → PHANTOM CLAIM voided back to brief-queue/, logged to the daily memory log, one-line lesson mirrored to lesson-broadcast.md; (ii) matching sign-in but no receipt in twelve-lane-receipts/ after 6 ticks → STALE, removed, logged; plus rotation-queued entries verified present on disk in brief-queue/",
    "window_rationale": "60-min claim→sign-in window respects legitimate work time (brief read + first reads precede sign-in; lane-executor run holds a brief up to 45 min); 6-tick sign-in→receipt window bounds silent stalls"
  },
  "rule": "a_claim_without_a_sign_in_is_a_reservation_without_a_worker",
  "mechanism": "a claim is a state transition (file moved to claimed/), not work. Work is evidenced only by a sign-in naming the exact file. Any handoff state whose aliveness is never re-proven is a state the system cannot distinguish from 'lost' — so the queue silently loses briefs in exactly the states nobody audits. The tripwire makes aliveness continuously re-proven: each tick, every claimed file must match a live sign-in or it returns to the queue; every signed-in file must produce a receipt or it is marked stale. The queue can then lose nothing it cannot see",
  "falsifier": "a voided claim that was actually live work (worker signing in outside the feed or exceeding the 60-min window legitimately) — would prove the window is miscalibrated, not that the tripwire is wrong; repeated false voids require threshold tuning, not removal",
  "decision_changed": "how queues are designed — every handoff state gets a liveness tripwire with a calibrated window before the queue is trusted with critical-path work; a state without a tripwire is a state assumed lost",
  "related": ["SN-0035 (phantom citation tokens — different defect class: citation text, not queue claims)", "sign-in/out law SN-0351 (the sign-in convention this tripwire enforces)"]
}
~~~
