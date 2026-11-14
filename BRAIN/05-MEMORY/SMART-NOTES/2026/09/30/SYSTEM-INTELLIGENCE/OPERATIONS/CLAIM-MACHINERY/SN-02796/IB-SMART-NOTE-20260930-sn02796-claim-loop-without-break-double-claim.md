# A Claim Loop Without a Break Is a Double-Claim — Stop the Sweep the Moment a Claim Succeeds

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02796-claim-loop-without-break-double-claim
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-t1142-lane10.md H4 + gap-t1142-lane4.md H4 (2026-11-14 01:20 hour); CORE-PRINCIPLES.md VIOLATION LOG 2026-11-14 (01:20 hour); filed as LEARNING event in learning-events-2026-11-14-01.md (hourly review 01:20 PST).

## ✦ IN A NUTSHELL

In the 2026-11-14 01:20-hour run the claim sweep loop had no break-after-success: after `claim-brief.py` succeeded on `brief-gap-t1142-lane10.md`, the loop kept iterating and claimed a second brief (`brief-gap-t1142-lane4.md`) in the same sweep. Both gap receipts mirror it (lane-10 H4, lane-4 H4). The second claim was absorbed honestly as the permitted second brief — the defect is the loop, not the outcome. The principle: a claim loop without a break is a double-claim waiting for a long queue. The correction is mechanical: stop the sweep the moment a claim succeeds; any second claim is an explicit step-10 decision, never a loop artifact.

## 🩷 HUMAN NOTE

Shawn — the machine that hands out work assignments had a small bug: it was supposed to take one job and stop, but after taking the first job it kept going and took a second one in the same pass. Nobody cheated — the second job was a real, allowed job, and the machine owned up to it honestly in both receipts. But the loop itself is the problem: with a long queue, a loop that never stops after success will keep grabbing jobs until something breaks. The fix is one line of discipline — stop the moment the first claim lands, and if a second claim is ever really wanted, someone has to decide it out loud first.

## 🟣 CHILD NOTE

Imagine a teacher handing out one cookie per child. She gives you a cookie, then — because nobody told her to stop — she gives you a second cookie too. The second cookie was yours to have, and she wrote it down honestly. But the rule is one cookie per trip: if she never stops after the first cookie, a long line of children means she hands out cookies until the jar is empty. The fix: after the first cookie, stop. A second cookie needs someone to say so first.

## 🔵 GRANDMA NOTE

Dear, the girl handing out the chore cards was meant to take one card and sit down — but she kept walking down the row and took a second card in the same trip. The second chore was a fair one, and she wrote both down plain as day. The trouble isn't the chore, love, it's the walking: a girl who never stops after the first card will end up with the whole row. From now on: one card, then sit down. A second card takes a word from the house first.

## 🟠 NAYA NOTE

Source: gap-t1142-lane10.md H4 and gap-t1142-lane4.md H4, 2026-11-14 01:20 hour; VIOLATION LOG entry in CORE-PRINCIPLES.md (2026-11-14, 01:20 hour); LEARNING event in learning-events-2026-11-14-01.md. The claim sweep had no break-after-success, so one sweep produced two claims (`brief-gap-t1142-lane10.md`, then `brief-gap-t1142-lane4.md`). The second claim was absorbed honestly as the permitted second brief — both receipts disclose it, and the outcome stands. What this note does NOT re-teach: the atomic mv claim guard (CANDIDATE 160 class — the claim script's atomic move prevents two seats claiming the same brief) or the claim-before-sign-in class (2026-10-13 violation log — the sign-in post is the visibility guard). Those guard WHO claims and WHEN it is visible; this one guards HOW MANY a single sweep takes — a loop-control defect, not a claim-race defect. Open item: the sweep procedure carries the break; until the loop code itself breaks after success, every sweep is one long queue away from repeating it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "claim_loop_breaks_after_first_success",
  "mechanism": "the claim sweep iterates briefs with no break; after a successful claim it continues to the next brief and claims again, so one sweep takes two briefs -- the loop, not the claim, is the defect; with a long queue the same missing break takes more",
  "evidence": "gap-t1142-lane10.md H4 + gap-t1142-lane4.md H4, 2026-11-14 01:20 hour: claim-brief.py succeeded on brief-gap-t1142-lane10.md, loop kept iterating and claimed brief-gap-t1142-lane4.md in the same sweep; second claim absorbed honestly as the permitted second brief; CORE-PRINCIPLES.md VIOLATION LOG 2026-11-14 (01:20 hour); learning-events-2026-11-14-01.md",
  "falsifiability": "a sweep that stops after the first success and thereby misses a brief that should have been claimed falsifies the rule; a second claim in one sweep that carries an explicit recorded step-10 decision is permitted, not a violation -- only an unrecorded second claim counts",
  "decision_change": "a future seat writing or running a claim sweep stops after the first successful claim; a second claim in the same sweep needs an explicit step-10 decision recorded first, never a loop artifact",
  "applies_when": ["claim", "sweep", "lane-executor", "dispatch", "claim-machinery"],
  "enforcement": "the claim sweep loop itself breaks after the first successful claim (mechanical, in the loop code); the night-dispatcher claim-liveness check flags any sweep that lands two claims without a recorded step-10 decision, and the second claim is re-queued until the decision is recorded",
  "related": ["SN-1444 queue is the union of rotation, claimed, done, and orphans -- verify the claim chain before classifying"]
}
~~~
