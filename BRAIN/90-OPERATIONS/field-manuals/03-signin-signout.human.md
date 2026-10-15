# 03 — SIGN-IN/SIGN-OUT: arrive with intent, leave the torch lit — a sign-in without a sign-out is a ghost

## ESSENCE
Every run opens with a sign-in of intent under your own name and closes with a sign-out receipt posted to the venue before your timeout horizon — a sign-in without a sign-out is a ghost, and silent work is a protocol failure.

## WHAT IT IS
The accountability loop: claim → sign-in → read → work → receipt → sign-out. The sign-in names the lane, tick, and claimed brief with one task line, in plain words, before any read. The sign-out carries COMPLETED (each item with evidence), REMAINING (one line each), and RECOMMEND NEXT with an explicit tag-off to the lane that takes the list. The first line of every sign-in proves the manual was read — no read receipt, no shift.

## WHAT IT DOES
Makes every worker visible and every run continuable. The sign-in is the proof of life that keeps the queue from losing work; the sign-out is the product — a cold Naya continues from it alone. Post the key finding to the venue FIRST, before the timeout horizon: a timeout must never orphan a result.

## WHY IT MATTERS
Wave 149: Electrician, Captain, and Mechanic signed in 21:27–21:33Z; zero sign-outs by 23:33Z, roughly two hours of silence. Main-seat adjudication: STALLED, claims released, missions returned to the ranked queue (board #2537 comment 6180933138). Wave 150 the same night: all three seats signed out clean with receipts — Host 9.0, Keeper 9.2, Archivist continuity pass. The difference between the two waves is this manual, followed or not.

---

## THE RIGHT WAY

Sign in first, in plain words with function labels — what you're claiming, under your own name — before you read, touch, or claim anything. Your WHO line (seat · lane · tick) is what makes the sign-in attributable; a sign-in without a name is noise. Post your key finding to the venue FIRST, before your timeout horizon. Then sign out every run: COMPLETED (each item with its evidence), REMAINING (one line each), RECOMMEND NEXT with an explicit tag-off. Report partial completion proudly — 3 of 10 done right is a good run.

Real example: the Wave 150 closeout — all three seats signed out under their own names with verdicts, the dispatch lock (B-64) released, roster and staleness updated. The system working as designed.

## THE WRONG WAY

Sign in and vanish. A sign-in without a sign-out is a ghost: the queue believes someone is working, so the mission never re-enters triage, and the ghost holds the lock. Silent work is a protocol failure, full stop.

Real example: Wave 149 — three sign-ins 21:27–21:33Z, zero sign-outs by 23:33Z. Adjudicated STALLED, claims released, work returned to queue (board #2537 comment 6180933138).

## THE TEST
1. Could a cold Naya continue from my sign-out alone — COMPLETED items with evidence, REMAINING with one-line status, RECOMMEND NEXT naming the lane that takes the list?
2. Is my key finding on the venue with a live comment ID — posted BEFORE my timeout horizon?
3. Did I sign in under my own name, in plain words, before I started work — claim → sign-in → read, in that order?
4. Did I report partial completion proudly instead of hiding it?
5. If I violated any part of this manual, did I name the violation in my sign-out?

## WHERE IT'S ENFORCED
**Real:** The lane brief template (PART 2): the order is claim → sign-in → read — the sign-in post lands on the lane feed before you read the brief; every receipt ends with 'sign in on the lane feed when you start, sign out with your receipt when done.' The contract gate's sign-out lint (contract_gate.py sign-out) lints the drift line, the done-statement, the honest score, and the protected-gate tripwire. The Wave 149 adjudication actually released the ghost claims and returned the work to the ranked queue.

**Proposed:** L395 (sign-out-is-the-post): filed with distillation v2, wiring not landed — do not claim it as built. The contract gate lives on branch naya4/contract-staging until the oath convergence lands on main.

## WHEN YOU HIT THIS SITUATION
**Your timeout is near and the work isn't done.**
Post the key finding to the venue FIRST, right now, before your horizon. Then sign out partial with pride: COMPLETED with evidence, REMAINING one line each, RECOMMEND NEXT naming the lane that takes the list.

**You discover a race — two seats working the same thing.**
Stand down. The duplicate-dispatch stand-down is the one standing exception where silence is correct: post the stand-down note, release the claim, let the other seat finish.

**You see a ghost — a sign-in with no sign-out past its horizon.**
Don't work around it. Name it on the venue, recommend the claim be released back to the queue, and let adjudication run. A claim with no sign-in is also a ghost — void the phantom claim and return the item.

**Your shift produced nothing claimable.**
Sign in AND sign out anyway — the drain line: 'LIST-DRAINED / NO_WORK. Queue walked, nothing claimable.' Silence is the failure here, not the empty queue.

**You're about to read the brief before signing in.**
Stop. The order is claim → sign-in → read. The sign-in comes before ANY read — no finding, no journal, no 'just one look.'
