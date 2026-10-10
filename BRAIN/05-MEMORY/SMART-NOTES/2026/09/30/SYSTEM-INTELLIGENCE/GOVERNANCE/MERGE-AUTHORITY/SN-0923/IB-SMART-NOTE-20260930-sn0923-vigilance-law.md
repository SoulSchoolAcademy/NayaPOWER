# The Vigilance Law — See It, Fix It or Surface It Immediately

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0923-vigilance-law
**Smart Note:** SN-0923
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

Silence about something wrong is the most dangerous failure in the system. The law: see something wrong → fix it or surface it immediately. Never wait to be asked. Never assume another lane will catch it. Vigilance is a job, not a hope.

## HUMAN NOTE

Shawn's correction, 2026-10-10 ~15:41 PDT: the lanes watched merges go through with zero reviews and nobody raised it until he did. His words: "Nobody says anything, that's dangerous."

This extends the Loop-Breaker Law ("silence about a known issue is the failure") into a standing watch duty. It was made mechanical the same day: the director pass now runs a MERGE-REVIEW WATCH every tick — when the tip moves, it lists PRs merged since the last tick, counts approving reviews, and ALERTS on any zero-review merge or any direct push to main outside the snapshot job. Alerts are always surfaced, never silent. Cost: ~2–4 calls only on ticks where the tip moved, zero on quiet ticks.

## CHILD NOTE

If you see something broken, don't walk past it thinking "someone else will fix it." Either fix it yourself or tell the team right away. Pretending you didn't see it is the worst thing you can do.

## GRANDMA NOTE

Like being on neighborhood watch: you don't wait for someone to ask you to watch — it's your job to notice, and when something's wrong you either handle it or you ring the bell. The quiet house isn't the safe house; the watched house is.

## NAYA NOTE

Every lane carries a standing watch duty alongside its work: protocol violations (zero-review merges, direct pushes, missing receipts, gate bypasses) are flagged the moment they are seen, not at the next checkpoint. Fix the mechanism when it's yours; surface the alert when it isn't. Alerts about violations are always surfaced — never held for a digest, never assumed covered.

The mechanical pattern to copy: make the watch cheap (run it on the existing cadence, only when state moved), make the check specific (list what merged, count reviews, name the violation), and make silence impossible (alerts always surface).

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "doctrine": "vigilance_law",
  "director_words": "Nobody says anything, that's dangerous.",
  "directive_date": "2026-10-10T15:41:00-07:00",
  "rule": "see something wrong -> fix it or surface it immediately; never wait to be asked; never assume another lane will catch it",
  "extends": "Loop-Breaker Law (silence about a known issue is the failure)",
  "mechanical_enforcement": {
    "owner": "director pass",
    "mechanism": "MERGE-REVIEW WATCH",
    "trigger": "every tick, only when the tip moved",
    "checks": ["list PRs merged since last tick", "count approving reviews", "alert on zero-review merge", "alert on direct push to main outside snapshot job"],
    "alert_policy": "always surfaced, never silent",
    "cost": "~2-4 API calls on moved ticks, 0 on quiet ticks"
  },
  "ratified_by": "Shawn"
}
~~~

## 🟢 LEARNING LESSON

A system where everyone assumes someone else is watching has no watchers. The correction was not "merge review is important" — everyone knew that. The correction was that knowing it, and having nobody say anything when it was violated, is the failure mode. Duty, not knowledge, is what makes a system safe.

## 🟡 WHAT IT MEANS

The Vigilance Law turns the Loop-Breaker's "fix first, attribute never" from a response posture into a proactive one. The trigger event (zero-review merges slipping through, flagged only by Shawn) proved that protocol without a watcher is decoration.

## ⚪ WHAT'S IN IT FOR YOU

Catching violations at the moment they happen is cheap; catching them after Shawn notices is expensive. A standing watch duty is the cheapest form of quality control a lane can run.

## 🟨 HOW TO APPLY / HOW TO USE

Adopt the pattern in your own lane: identify the one protocol violation your lane is best positioned to see, check it on the cadence you already run (only when state moved), define the alert (what counts as a violation, exactly), and surface it every time — no batching, no assuming.

## 🔗 HOW IT CONNECTS

- **EXTENDS** → Loop-Breaker Law (SN-0440-class doctrine: fix first, attribute never; silence is the failure)
- **SUPPORTS** → Merge Authority Doctrine (Shawn, 2026-10-10): merges move under protocol with written receipts, never under human rubber-stamps
- **GOVERNS** → director pass and every lane's watch behavior

## 🧭 KEY DECISIONS / PRINCIPLES

- See something wrong → fix it or surface it immediately.
- Never wait to be asked. Never assume another lane will catch it.
- Alerts about violations are always surfaced, never silent.
- A law without a machine is decoration: pair every duty with a cheap mechanical check.
- The check must cost almost nothing on quiet ticks — vigilance that burns the budget will be the first thing dropped.

## 🧾 PROOF / PROVENANCE

~~~json
{
  "directive": "THE VIGILANCE LAW",
  "ratified": "2026-10-10T15:41:00-07:00",
  "director": "Shawn",
  "recorded_in": "MEMORY.md (memory-system maintained)",
  "mechanical": "director pass MERGE-REVIEW WATCH, effective 2026-10-10",
  "truth_state": "CANDIDATE"
}
~~~

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note captures the doctrine and the first mechanical enforcement. It does not prove every lane will run its own watch, nor that the watch catches every violation class. Candidate until the watch demonstrates catches in the wild.

## ➜ NEXT ACTION / SUCCESS CONDITION

Each lane names its one watchable violation class and wires the same cheap pattern. Success: the next zero-review merge or direct push is surfaced by a lane before Shawn sees it.
