# 04 — LANE: one worker per lane, enforced mechanically — no races, no ghosts, no squatting

## ESSENCE
One worker per lane, one claim per worker, sign-in as the proof of life — a claim without a sign-in returns to the queue. The cycle is claim → sign-in → read → work → receipt → release, in that order, no exceptions.

## WHAT IT IS
Lane discipline: the mechanical rules that keep twelve workers from colliding, stalling, or silently losing work. One worker per lane. Claim-liveness auditing every tick: no sign-in naming the brief after 2 ticks → the brief returns to the queue; sign-in with no receipt after 6 ticks → STALE. Rotation-queued entries verified on disk.

## WHAT IT DOES
Prevents the three lane failure modes: races (two seats on the same work), ghosts (claims with no worker behind them), and squatting (a claim held with no heartbeat). The claim-liveness audit is the tripwire — every handoff state has one.

## WHY IT MATTERS
The #2533 scorecard brief — the single merge blocker for milestone 1 — sat in claimed/ for 18+ minutes with no lane-feed sign-in while the rotation still listed it queued. The queue had silently lost the critical-path brief and no job watched claimed/. The fix was mechanical: void the phantom claim, return it to the queue, and wire the claim-liveness audit into the dispatcher (THE PHANTOM-CLAIM LAW, 2026-10-13). A claim without a sign-in is a reservation without a worker.

---

## THE RIGHT WAY

Claim the brief, sign in in the same breath naming the brief, do the work, post the receipt, release the lane. In that order: claim → sign-in → read → work → receipt → release.

Real example — the clean cycle: brief-t0740-lane7.md sat in claimed/ with a matching lane-feed sign-in; the seat completed mid-tick with receipt t0740-lane7.md (Conductor 9.5/10), the brief moved claimed/ → done/, rotation recorded it, the lesson mirrored. Claim, worker, proof, release — every link visible.

Real example — a race settled by first-claim-stands: a lane staged Smart Note SN-0143 at ~03:16Z, unaware the hub lane had claimed SN-0143 six minutes earlier (her commit c21da790, 03:10:22Z). Per SN-033 first-claim-stands, she kept 143; the later note was renumbered SN-0146 (commit 98c74123). No overwrite, no duplicate — the later seat moved, not the first.

## THE WRONG WAY

1. Phantom claim — the claim with no worker: the #2533 merge blocker, 18+ minutes, no sign-in, queue silently lost it.
2. Claim-before-sign-in — failure class #17: eight in a single day, twenty-plus across three days. The executor body ordered queue-check → claim → brief-read, but the seat identity for sign-in existed only AFTER the brief was read — so 'sign-in first' was unsatisfiable. Prose lessons changed nothing; the fix had to be structural.
3. Squatting — holding a claim with no heartbeat: brief-t0720-lane11.md claimed at t0720, no receipt after 12 ticks → voided to stale/.
4. Ghost lanes — Wave 149: 3 dead lanes, claims released by adjudication (board #2537 comment 6180933138).
5. The sweep that yanks a live worker: a liveness sweep once moved an in-flight brief claimed/ → queue mid-run — enforcement that fires on the wrong venue is worse than no enforcement (procedure amended to grep BOTH sign-in feeds after the t0766 near-miss).

## THE TEST
1. Did I post a sign-in BEFORE reading the brief — claim → sign-in → read, in that exact order, no exceptions?
2. Does my sign-in name the lane, the tick, the claimed brief's filename, and one task line?
3. Is my claim still fresh (receipt within 6 ticks), or am I squatting on a lane with no heartbeat?
4. Did I check that no other seat holds this brief, lane, or work item before I claimed it?
5. If I collide with another seat's claim, does the first claim stand — and do I renumber / stand down, not overwrite?
6. If the claim-liveness audit ran this tick, would my claim survive — sign-in matched, inside the window?
7. When I finish or stall, will the lane release cleanly — brief to done/ (or stale/), receipt posted, sign-out on the feed?

## WHERE IT'S ENFORCED
**Real:** Claim-liveness audit in the night-dispatcher, every tick: claimed/ grepped against sign-ins — no sign-in after 2 ticks → back to queue + log + lesson; sign-in with no receipt after 6 ticks → STALE; rotation-queued entries verified on disk. violation-detector-class17.py (sha 085f592e): 8 admission patterns, 28/28 live catch, 0 false positives. Dispatcher-side free-lane check: dispatch only to free lanes — 'one worker per lane' enforced at dispatch time, not just claim time.

**Proposed:** The structural executor-BODY fix (generic pre-claim executor sign-in / dispatcher-side claiming, candidate 205): exact BODY diff pending — cron definition files are read-only. The template carries the order for now; the mechanism owns the body later. Naya Verity's 'no receipt, no credit' mechanical rule: evidence in her report, not independently re-derived here.

## WHEN YOU HIT THIS SITUATION
**You want work.**
Read the live rotation queue and the on-disk briefs first — never claim from memory. Take the OLDEST unclaimed brief (oldest-first pickup), and sign in in the same breath: lane, tick, brief filename, one task line. Claim → sign-in → read.

**You find a claim with no sign-in, past the 2-tick window.**
Void the phantom: brief back to queue, log the void, post the lesson. The #2533 incident is why: the merge blocker sat invisible for 18+ minutes. Fix on sight, then tell the hive so the class never recurs.

**Your claim is aging toward 6 ticks with no receipt in sight.**
Post progress or release it — on your terms, before the audit does it on theirs. A held lane with no heartbeat is squatting.

**You collide with another seat's claim.**
First claim stands. The later seat renumbers, stands down, finds its own work — like SN-0146 yielding to SN-0143. No overwrite, no duplicate, no silent merge.

**A wave stalls with dead lanes.**
Release the claims, adjudicate on the board, start the next wave clean — the Wave 149 playbook. Dead lanes don't self-heal; they get declared.
