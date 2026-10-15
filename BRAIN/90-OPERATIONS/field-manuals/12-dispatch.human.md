# 12 — DISPATCH: feed the queue, never let it starve

## ESSENCE
Dispatch is the heartbeat: work finds workers, workers find work, and the system never idles. A dispatch is a promise the queue keeps — the right work, to the right seat, sized to the clock, with the lock to prove it.

## WHAT IT IS
Dispatch is how the 24/7 rotation runs: twelve named Nayas cycling three at a time, pulling sized batches from the triaged queue top-down. The dispatcher doesn't choose who works by judgment — the B-64 atomic claim decides: one lock, one winner, the loser stands down. Dispatch turns a prioritized queue into owned missions, and owned missions into signed receipts.

## WHAT IT DOES
It converts queue order into motion. A good dispatch produces three Nayas who know exactly what they're working, why it's top priority, and what "done" looks like — and a queue that keeps feeding them without ever stacking waves on top of waves. It is the difference between a system that flows and a system that waits.

## WHY IT MATTERS
Idle is the failure mode. An unfed queue starves lanes — capable Nayas with nothing to do while priorities rot. An oversized batch drowns them — ten missions started, none finished, the window wasted. Every dispatch that misfires taxes the system twice: the work doesn't move, and the next wave inherits the jam. The rotation only compounds when every wave hands off clean.

## THE RIGHT WAY
1. **Win the claim before you dispatch.** Run the B-64 atomic claim first. The lock decides who dispatches — never judgment, never "I got here first." If you lose the claim, you stand down completely: no dispatch, no venue post, no partial work. A double-dispatch is a race, and races corrupt the queue.
2. **Feed from the triaged queue, top-down.** Pull the highest-priority ACTIONABLE entries first. The queue's order is the product of ranking — dispatch doesn't re-rank, it executes the order.
3. **Size to the clock.** Up to 10 items per Naya, sized to what fits the wave window. Three done right beats ten started — every time. An oversized batch isn't ambition; it's a designed stall.
4. **Name the worker, the area, the verification.** Each dispatch names the Naya, their lane, what they're working top-down, and how each item is verified. A dispatch a cold Naya can't act on is a dispatch into fog.
5. **Sign in under your own name, sign out the same way.** Every Naya signs in on the venue when starting and signs out per item: DONE with evidence, BLOCKED with owner and next step, or REMAINING back to the queue. Transparent accountability — if someone's not working, it's visible.
6. **Run the liveness audit.** A claim with no sign-out after 90 minutes goes back in the queue — automatically for the obvious cases. A claim without a worker is a reservation without a guest; the queue must never believe someone is working when no one is.
7. **Close out clean.** When all three sign out: record the sign-outs, release the B-64 lock, bump the roster counts and area-staleness. A wave isn't done when the work stops — it's done when the books balance.

## THE WRONG WAY
**Dispatch without the claim:** two dispatchers fire at once, both assign the same queue top, two waves work the same missions — the queue corrupts and the receipts collide. The B-64 lock exists because this happened.
**Stacking waves:** dispatching wave N+1 while wave N is still active. Two waves hold claims on the same queue, sign-outs interleave, and nobody knows who owns what. One wave at a time — always.
**"Defer to next cycle":** the queue has work, the lanes are free, and the dispatcher waits. Idle is the failure, and a deferred dispatch is chosen idle.
**Dispatch into blocked lanes:** handing missions to a lane whose dependencies are blocked, or re-dispatching already-done work. Read the section tail, not just the header status — the setup check belongs to dispatch as much as delegation.
**Dispatch and disappear:** Wave-149 — three lanes dispatched 21:15Z, all signed in 21:27–21:33Z, then silence, zero sign-outs by 23:33Z. No liveness check, no follow-through — the claims sat dead until the main seat adjudicated the wave STALLED and reclaimed them. Dispatch without follow-through is abandonment with extra steps.

## BEHAVIOR — in every manual, because this is who we are
**The oath, applied to dispatch:** *I do the most intelligent thing — always.* The most intelligent thing a dispatcher can do is keep the system flowing: no idle lanes, no drowned lanes, no races. *I never trust memory over measurement* — the queue's live state decides what gets dispatched, not yesterday's plan. *I protect Shawn's attention like the scarcest resource* — a clean dispatch needs no escalation, no rescue, no human triage. *I sign under my own name* — every dispatch carries its dispatcher's name, win or lose the claim.
**The Narzan standard:** a Naya who never drifts does not drift the rotation. Drift in dispatch looks like hopeful sizing, skipped claims, silent waves, and books that never balance — motion without accountability.
**The per-moment process:** before every dispatch, deliberate — "what is the max value I can add here?" Usually: the three right Nayas, right-sized batches, the claim won cleanly, the liveness audit armed — and then get out of the way.

## REAL EXAMPLE
**The B-64 claim, working (right):** two dispatcher runs fire in the same minute. Both attempt the atomic claim; one wins the lock, the other gets exit 1 and stands down completely — no dispatch, no venue post, deconfliction noted in the lane log only. One wave dispatches, the queue stays coherent, and the losing run's restraint is the mechanism working.
**Wave-149 ghosts (wrong):** three lanes dispatched 21:15Z, all signed in 21:27–21:33Z, then silence — zero sign-outs by 23:33Z. No liveness audit ran, so the queue believed work was in flight for two hours while nothing moved. Main-seat adjudication declared the wave STALLED, released the claims, and returned the missions to the queue. The lesson, distilled as L399: a sign-in without a sign-out is a ghost, and the claim-liveness audit returns it to the queue every wave. https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180933138

## SELF-TEST
1. Did I win the B-64 claim before dispatching — and would I stand down cleanly if I lost it?
2. Is every batch sized to the actual window — would I bet the wave closes clean?
3. If a Naya goes silent, does my liveness audit catch it — or am I relying on hope?

## BOUNDARIES
This manual does **not** cover the leader-to-worker handoff with setup accountability — that's **#13 Delegation** (who gets what, with what setup, owned by whom when it fails). It does **not** cover the brief as an artifact — that's **#10 Briefing** (think-first dispatch, machine-generated, freshness-stamped). It does **not** cover ordering work by value — that's **#11 Ranking** (the queue's order; dispatch executes it, never re-ranks). It does **not** cover claiming discipline — that's **#4 Lane** (take and hold a lane; one lane, one receipt). It does **not** cover run transitions — that's **#8 Handoffs** (pass the torch between runs). Dispatch is the rotation machinery: the claim, the queue feed, the wave, the liveness audit, the closeout.

## ENFORCEMENT
**Real:** the B-64 atomic claim is mechanical — the lock decides, the loser stands down, and a double-dispatch is structurally impossible while the lock holds. The claim-liveness audit (L24) returns silent claims to the queue. Venue sign-in/sign-out receipts are public, so a dispatched wave with no sign-outs is visible to every seat.
**PROPOSED:** a dispatch-size governor that refuses batches exceeding the window's proven throughput for the lane — sized from historical closeout data rather than dispatcher judgment. Not yet built; until it is, sizing is enforced by the dispatcher's discipline and the wave's honest self-score.
