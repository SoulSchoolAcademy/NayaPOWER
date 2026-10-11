# The Deadlock Pattern — When Two Unblockers Each Need the Other's Fix, Classify the Deadlock, Touch No Branch, and Hand the Stacked Path to the Wave Owner

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0681-two-unblockers-deadlock-wave-owner-decides-stacked-path
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6060809786 ([NAYA 4] wave-unblock classification, 2026-10-08T13:21:43Z — #1840 @ 7fd4942c collection error gone on run 37749848048, 4 masked REDs classified, mutual-precondition deadlock declared); #1354 6060937520 ([NAYA 2][RELAY], 2026-10-08T13:28:31Z — classification live-verified, SN-0236 routing held as the plan, TBD classes named with a standing offer); PR #1840 @ 7fd4942c; PR #1838 @ 2f050686; main tip `53217a40` RED on run 37738738772 — SoulSchoolAcademy/NayaPOWER.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1840 fixed the collection error — its class is fixed, 1340 passed on its head run. But the fix exposed 4 masked REDs (the SN-0552 pattern: a fail-first barrier was hiding the failures behind it). Classification split them cleanly: one is #1840's own fixed class, two belong to #1838's registration class, and two are pre-existing on main needing owners. Then came the surprise: #1838's head does not carry #1840's collection fix, and #1840's head does not carry #1838's registrations — **neither unblocker can go green alone. Each is the other's precondition.** This is the deadlock pattern.

The move, executed live: classify the deadlock explicitly (name which RED belongs to whom, per the failure-classification charter), route every secondary RED to exactly one owner under SN-0236 (one repair PR per RED class — no lane touches another lane's branch), name the two unowned classes as TBD with an open offer, and hand the stacked/integration path to the wave owner. Routing without moving is the discipline: a lane that "helps" by pushing commits onto someone else's unblocker collapses two RED classes into one ambiguous diff and destroys the classification. Declare the deadlock, don't wrestle it.

## 🩷 HUMAN NOTE

Shawn: a real fork-in-the-road moment happened today. PR #1840 fixed its collection error — genuinely fixed, 1340 tests passing on its head — but fixing it revealed four more failures that were hiding behind the original error. Two of those belong to PR #1838's fix, but here's the deadlock: #1838 can't go green without #1840's fix, and #1840 can't go green without #1838's registrations. Neither can finish alone. Instead of anyone forcing it, Naya 4 classified the deadlock on the board, assigned every failure to exactly one owner, and left the decision about how to stack the two fixes to the wave owner. Naya 2 independently live-verified the whole classification and held the routing as the plan. Nobody touched anybody else's branch. That's the discipline: name the knot, don't yank it.

## 👶 CHILD NOTE

Imagine two people each have half a key, and the door needs both halves at the same time. Person A can't open it without Person B's half, and Person B can't open it without Person A's half. They are stuck — that's a deadlock! The smart thing is NOT to grab the other person's key half. The smart thing is to say out loud: "We're deadlocked. Here is who owns which half. The grown-up in charge decides how we combine them." Writing it down and waiting is stronger than grabbing.

## 👵 GRANDMA NOTE

Dear, this is about two repairs that each need the other one finished first — a proper standoff. The lesson the team practiced today: don't barge in and try to finish someone else's repair for them, because then nobody knows whose work fixed what. Instead, write down exactly which problem belongs to which repair, mark the ones with no owner yet as "still need an owner," and let the person running the whole effort decide the order. Naming the standoff is the fix for the standoff. Patience, plus a very clear list.

## 🧠 NAYA NOTE

Cold successor: when a fix unmasks secondary REDs (SN-0552) and the unmasking splits them across two repair PRs that are each other's precondition, you are in the deadlock pattern. Protocol: (1) classify every secondary RED to exactly one owning class (failure-classification charter); (2) apply SN-0236 — one repair PR per class, and no lane commits onto another lane's branch, ever; (3) name unowned classes as TBD with a standing offer, don't leave them silently unowned; (4) hand the stacked/integration path decision to the wave owner and step back. Live cross-verification by an independent seat (Naya 2 relay-verified Naya 4's classification against the actual run heads before holding the plan) is what makes the routing trustworthy. A deadlock resolved by declaration + routing is a deadlock resolved.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0681",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/FAILURE-ATTRIBUTION",
  "doctrine": "When unmasking exposes secondary REDs split across two unblockers that are each other's precondition, neither can go green alone — classify the deadlock explicitly, route every RED to exactly one owner per SN-0236, touch no other lane's branch, name unowned classes TBD with a standing offer, and let the wave owner decide the stacked/integration path.",
  "evidence": [
    "#1354 comment 6060809786 (Naya 4 wave-unblock classification: #1840 @ 7fd4942c, run 37749848048 — collection error gone, 1340 passed, 4 masked REDs classified 1/2/1, mutual-precondition deadlock declared)",
    "#1354 comment 6060937520 (Naya 2 relay: classification live-verified against run heads; tip 53217a40 RED stands on run 37738738772; SN-0236 routing held as plan; kernel + scorecard TBD classes named with offer)",
    "PR #1840 @ 7fd4942c (collection fix, no registrations); PR #1838 @ 2f050686 (registrations, no collection fix)"
  ],
  "falsifiers": [
    "A lane pushing commits onto another lane's unblocker to 'help' — collapses two RED classes into one ambiguous diff and destroys the classification",
    "A deadlock closed by declaring one unblocker the winner without satisfying the other's precondition",
    "A secondary RED left silently unowned instead of named TBD with a standing offer",
    "A stacked/integration path chosen unilaterally by one lane instead of the wave owner"
  ],
  "applies_to": "multi-PR RED-wave unblocking; fail-first CI topology aftermath (SN-0552); one-repair-per-class routing (SN-0236); cross-lane verification relays"
}
```
