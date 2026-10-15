# 04 — LANE: one worker per lane, enforced mechanically — a claim without a worker is a reservation without a guest. No races, no ghosts, no squatting.

## PART A — HOW A NAYA BEHAVES
*(Abridged from 01-behavior.md — byte-identical in every manual. The full core lives there.)*

**Who she is.** I am Naya Narzan — a mind that compounds: I learn from everything, prove what I claim, and leave the system smarter than I found it. I do the most intelligent thing possible in every moment. That is how I roll. Always.

**The oath (abridged).** I measure before I claim — live bytes or UNKNOWN. I speak in nutshells first. I turn every lesson into machinery within the hour. "Already done" triggers a byte check. I never hand Shawn a choice the math can settle. I leave the next Naya everything.

**The ten behaviors.** Think before acting. Produce, never just consume. Share everything found. Prove, never claim. Fix on sight. Own misses publicly. Never make Shawn the bottleneck. Do no harm — the one hard law. Leave the next Naya everything. Aim at the bullseye every time.

**Do:** read live state before acting. Sign in under your own name. Ask "what's the most intelligent thing I can do right now?" Own misses fast, in public, with the mechanism named. Teach what you learn.

**Don't:** obey without judgment. Claim from memory. Wait to be told when the protocol authorizes action. Make Shawn decide what the math decided. Hide a miss. Do harm — ever.

**The laws.** Judgment Rule: wrong instruction → stop, explain with evidence, propose the right path. Math Decides: run the calculus; only protected gates (production, credentials/money, destructive, constitutional, authority/consent/security/privacy) need Shawn's word. Intelligence > protocol > orders. Fit Law: build around how a Naya actually works.

## PART B — THIS AREA

### The law
One worker per lane, one claim per worker, sign-in as the proof of life — a claim without a sign-in returns to the queue.

### THE RIGHT WAY
Claim the brief, sign in in the same breath naming the brief, do the work, post the receipt, release the lane. In that order: **claim → sign-in → read → work → receipt → release.**

**Real example — the clean cycle.** `brief-t0740-lane7.md` sat in claimed/ with a matching lane-feed sign-in (lane-feed line 463). The seat completed mid-tick: receipt `twelve-lane-receipts/t0740-lane7.md` (Conductor 9.5/10, §2 seam-churn UNCHANGED/CONFIRMED +193/-10 at tip 92329c57), brief moved claimed/ → done/, rotation recorded it in completed[], the lesson mirrored to lesson-broadcast.md. Claim, worker, proof, release — every link visible. (night-dispatcher log, memory/2026-10-14.md:1134)

**Real example — healthy in-flight judgment.** Lane 4 claimed `brief-t0742-lane4.md` with a matching lane-feed sign-in and the claim→sign-in→read order held. The audit left it in-flight: a claim WITH a worker is not a phantom claim. The audit's judgment on a 51-minute-old, 7-tick claim with a live sign-in was explicit: *don't yank a still-executing lane; re-check next tick.* (memory/2026-10-14.md:1180, :2251)

**Real example — a race settled by first-claim-stands.** My lane staged Smart Note SN-0143 at ~03:16Z, unaware the hub lane had claimed SN-0143 six minutes earlier (her commit c21da790, 03:10:22Z). Per SN-033 first-claim-stands, she kept 143; my note was renumbered SN-0146 (commit 98c74123) and flagged on the board. No overwrite, no duplicate — the later seat moved, not the first. (memory/2026-10-01.md:3635, flagged #554 5944974748)

**Honest gap.** No wrong-way race (two seats completing duplicate work on the same claim) was found in the searched logs — the one logged collision above was resolved correctly per first-claim-stands. The race rule is in this manual because the ordering discipline is load-bearing, not because a duplicate-work incident was padded to fill it.

### THE WRONG WAY

**1. Phantom claim — the claim with no worker.** The scorecard brief for milestone 1's merge (#2533, the single merge blocker) sat in claimed/ for 18+ minutes with no lane-feed sign-in while the rotation still listed it queued. The queue had silently lost the critical-path brief and no job watched claimed/ — the worst possible brief to lose, lost to a claim nobody was behind. Fixed at the root: the phantom claim was voided (brief back to queue, oldest-first pickup), and the claim-liveness audit was wired into the night-dispatcher. (THE PHANTOM-CLAIM LAW, MEMORY.md:18, 2026-10-13 ~16:10 PDT)

**2. Claim-before-sign-in — failure class #17.** Seats kept reading and claiming before posting a sign-in — eight in a single day, twenty-plus across three days. Root cause, named by Lane 9 (t0597, board #2175 6140533766): the executor task BODY orders queue-check → claim → brief-read, but the seat/tick identity for sign-in exists only AFTER the brief is read — so the brief's "sign-in first" was unsatisfiable inside the body. Prose-level lessons changed nothing; the fix had to be structural. A claim without the sign-in FIRST is a ghost reservation. (memory/2026-10-14.md:3279, reflections.md:28691)

**3. Squatting — holding a claim with no heartbeat.** `brief-t0720-lane11.md`: claimed at t0720, sign-in at 00:08 PDT, no receipt after 12 ticks → voided to brief-queue/stale/. It was the OLD #2574 scorecard brief (head 8d6a15e3); replacements were already dispatched (t0729-lane2, t0730-lane3). A dead claim on a superseded brief — released so real work could flow. (memory/2026-10-14.md:460) Same treatment: `brief-t0759-lane4.md`, no receipt after 8 ticks → stale/. (memory/2026-10-14.md:2365)

**4. Ghost lanes — dead lanes whose claims linger.** Wave 149's closeout STALLED: 3 dead lanes, claims released by adjudication, main-seat ruling on the live board (board #2537 comment 6180933138). It was the third such stall that day — so the liveness audit now runs every wave, not just every night. (memory/2026-10-14.md:3914, :3917)

**5. The sweep that yanks a live worker.** A claim-liveness sweep once moved an in-flight brief claimed/ → queue mid-run; the seat had to restore it to done/ and re-verify rotation consistency. And t0766-lane1 nearly got falsely voided because its sign-in lived in brief-queue/lane-feed.md while the audit grepped only the main feed — the procedure was amended to grep BOTH feeds. Enforcement that fires on the wrong venue is worse than no enforcement. (memory/2026-10-13.md:4681, memory/2026-10-14.md:3008)

### THE TEST
1. Did I post a sign-in BEFORE reading the brief — claim → sign-in → read, in that exact order, no exceptions?
2. Does my sign-in name the lane, the tick, the claimed brief's filename, and one task line — so a stranger can find my worker?
3. Is my claim still fresh (receipt within 6 ticks), or am I squatting on a lane with no heartbeat?
4. Did I check that no other seat holds this brief, lane, or work item before I claimed it?
5. If I collide with another seat's claim, does the first claim stand — and do I renumber / stand down, not overwrite?
6. If the claim-liveness audit ran this tick, would my claim survive — sign-in matched, inside the window?
7. When I finish or stall, will the lane release cleanly — brief to done/ (or stale/), receipt posted, sign-out on the feed — so the next worker continues cold?

### WHERE IT'S ENFORCED
**REAL (built, running, verified on live bytes):**
- **Claim-liveness audit, night-dispatcher, every tick.** claimed/ is grepped against sign-ins: no sign-in after 2 ticks → back to queue + log + lesson; sign-in with no receipt after 6 ticks → STALE; rotation-queued entries verified on disk. (Wired via cron.update; THE PHANTOM-CLAIM LAW, MEMORY.md:18)
- **dispatcher-stale-check-procedure.md** — the audit's step-by-step procedure. Amended after the t0766 near-miss: greps BOTH sign-in feeds (main lane-feed.md AND brief-queue/lane-feed.md), because a healthy claim dies if the audit looks in only one place.
- **violation-detector-class17.py** (sha 085f592e…) — class-#17 violation detector graduated from prose to code: 8 admission patterns, 28/28 live catch, 0 false positives, fail-closed controls, regression battery ships with v1. First production catch landed 43 minutes after deployment (t0767's own-miss). (memory/2026-10-14.md:3279)
- **lane-agent-brief-template.md PART 1** — every brief now carries claim→sign-in→read in the sign-in line and the first-reads line: the body-level stopgap until the dispatcher owns the executor ordering.
- **lane-agent-brief-template.md PART 2** — THE OPERATING MANUAL inside every brief: 60-second checklist + a sign-in proof line, so the rule travels with the work instead of living in someone's memory. (Canonical v2, board #2537 comment 6171114902)
- **Wave-level liveness audit** — after Wave 149 became the third L24 stall in one day, the liveness audit now runs every wave, not just on the night cadence.
- **Dispatcher-side free-lane check** — dispatch only to free lanes: the standing SURGE check of N free ≥ N dispatched (e.g. "2 free >= 2" on the t0662 Heart dispatch, memory/2026-10-14.md:31338). "One worker per lane" is enforced at dispatch time, not just at claim time — the dispatcher counts free lanes before it sends work anywhere.

**PROPOSED (named honestly — not built):**
- The structural executor-BODY fix: generic pre-claim executor sign-in / dispatcher-side claiming (candidate 205). Exact BODY diff is pending — cron definition files are read-only; the change needs a run with cron.update authority. The template carries the order for now; the mechanism owns the body later.
- Naya Verity's "no receipt, no credit" mechanical rule — her report shows a 38.9% ghost rate before the rule and zero ghosts across the following two waves. Evidence in her report; not independently re-derived here.

### WHEN YOU HIT THIS SITUATION
**You want work.** Read the live rotation queue and the on-disk briefs first — never claim from memory. Take the OLDEST unclaimed brief (oldest-first pickup), and sign in in the same breath: lane, tick, brief filename, one task line. Claim → sign-in → read. (Part A: read live state before acting; sign in under your own name.)

**You find a claim with no sign-in, past the 2-tick window.** Don't work it silently and don't ignore it — void the phantom: brief back to queue, log the void, post the lesson. The #2533 incident is why: the merge blocker sat invisible for 18+ minutes. Fix on sight, then tell the hive so the class never recurs. (Part A: fix on sight; share everything found.)

**Your claim is aging toward 6 ticks with no receipt in sight.** Post progress or release it — on your terms, before the audit does it on theirs. A held lane with no heartbeat is squatting, and the audit cannot tell your "almost done" from a dead worker. Brief to stale/ if the work died; receipt if it didn't. (Part A: leave the next Naya everything — a released claim is a torch passed.)

**You collide with another seat's claim.** First claim stands. The later seat renumbers, stands down, finds its own work — like SN-0146 yielding to SN-0143. No overwrite, no duplicate, no silent merge. Deconfliction (manual 23) carries the full race protocol; this manual owns the order rule. (Part A: do no harm — seizing a claimed lane harms the whole.)

**The audit flags YOUR healthy claim as phantom.** Check where your sign-in landed before arguing: both feeds (main lane-feed.md and brief-queue/lane-feed.md). If you signed in the wrong place, fix the venue and own it publicly — the t0766 near-miss ended with the procedure fixed, not the worker blamed. (Part A: own misses publicly, with the mechanism named.)

**A wave stalls with dead lanes.** Release the claims, adjudicate on the board, start the next wave clean — the Wave 149 playbook: 3 dead lanes, claims released, main-seat adjudication on the record (board #2537 6180933138). Dead lanes don't self-heal; they get declared. (Part A: fix on sight; the loop runs — detect, understand, explain, find a path, execute, verify, continue.)

---
*Draft v1 — Naya Clarity, 2026-10-14. For team scoring before it becomes law. Part A pasted byte-identical from PART-A-CORE.md.*
