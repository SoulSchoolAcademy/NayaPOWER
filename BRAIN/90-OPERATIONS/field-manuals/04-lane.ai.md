# 4 - Lane (AI)
area_number: 4
area_name: Lane
owner_team: Naya Clarity
agent_seat: Builder

## DEFINITIONS
- what_it_is: Lane discipline: the mechanical rules that keep twelve workers from colliding, stalling, or silently losing work. One worker per lane. Claim-liveness auditing every tick: no sign-in naming the brief after 2 ticks → the brief returns to the queue; sign-in with no receipt after 6 ticks → STALE. Rotation-queued entries verified on disk.
- what_it_does: Prevents the three lane failure modes: races (two seats on the same work), ghosts (claims with no worker behind them), and squatting (a claim held with no heartbeat). The claim-liveness audit is the tripwire — every handoff state has one.
- why_it_matters: The #2533 scorecard brief — the single merge blocker for milestone 1 — sat in claimed/ for 18+ minutes with no lane-feed sign-in while the rotation still listed it queued. The queue had silently lost the critical-path brief and no job watched claimed/. The fix was mechanical: void the phantom claim, return it to the queue, and wire the claim-liveness audit into the dispatcher (THE PHANTOM-CLAIM LAW, 2026-10-13). A claim without a sign-in is a reservation without a worker.

## PROTOCOLS
1. One worker per lane, one claim per worker, sign-in as the proof of life.
2. The cycle, in order: claim → sign-in → read → work → receipt → release. No exceptions.
3. A claim without a sign-in after 2 ticks returns to the queue (phantom claim). A sign-in with no receipt after 6 ticks goes STALE.
4. Take the OLDEST unclaimed brief — oldest-first pickup. Never claim from memory.
5. First claim stands: on collision, the later seat renumbers or stands down — never overwrites.
6. Dispatch only to free lanes. A rank that can't be executed is a wish list.
7. Enforcement must check BOTH sign-in feeds (main lane-feed.md and brief-queue/lane-feed.md) — a healthy claim dies if the audit looks in only one place.

## CONSTRAINTS
- Test yourself against THE TEST before acting: Did I post a sign-in BEFORE reading the brief — claim → sign-in → read, in that exact orde... / Does my sign-in name the lane, the tick, the claimed brief's filename, and one task line? / Is my claim still fresh (receipt within 6 ticks), or am I squatting on a lane with no hear... / Did I check that no other seat holds this brief, lane, or work item before I claimed it?
- Enforcement is split honestly: REAL machinery listed under WHERE IT'S ENFORCED; PROPOSED items are not claimed as built.
- Never invent examples. Every example in this manual names its evidence handle.

## SITUATIONS
- You want work. :: Read the live rotation queue and the on-disk briefs first — never claim from memory. Take the OLDEST unclaimed brief (oldest-first pickup), and sign in in the same breath: lane, tick, brief filename, one task line. Claim → sign-in → read.
- You find a claim with no sign-in, past the 2-tick window. :: Void the phantom: brief back to queue, log the void, post the lesson. The #2533 incident is why: the merge blocker sat invisible for 18+ minutes. Fix on sight, then tell the hive so the class never recurs.
- Your claim is aging toward 6 ticks with no receipt in sight. :: Post progress or release it — on your terms, before the audit does it on theirs. A held lane with no heartbeat is squatting.
- You collide with another seat's claim. :: First claim stands. The later seat renumbers, stands down, finds its own work — like SN-0146 yielding to SN-0143. No overwrite, no duplicate, no silent merge.
- A wave stalls with dead lanes. :: Release the claims, adjudicate on the board, start the next wave clean — the Wave 149 playbook. Dead lanes don't self-heal; they get declared.
