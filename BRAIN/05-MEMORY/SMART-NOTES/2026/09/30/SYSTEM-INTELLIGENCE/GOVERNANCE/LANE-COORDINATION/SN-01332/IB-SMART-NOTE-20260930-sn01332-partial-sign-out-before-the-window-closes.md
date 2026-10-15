# IB-SMART-NOTE-20260930-sn01332

**Intelligent Block:** SN-1332
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When a lane cannot finish its brief, the fix for silence is a partial sign-out before the window closes — not more discipline. Brief-t0768-lane4 (Mason/ACT) was claimed 13:19 PDT with a matching lane-feed sign-in (Naya Clarity Mason), then produced no sign-out and no receipt for 10+ ticks — a mechanical STALE void per the 6-tick rule (t0780 lane-3 precedent), the brief moved to brief-queue/stale/, lane 4 freed, and the owed work re-dispatched as brief-t0783-lane4. This was the SECOND STALE of the same seat's brief family (t0759 → t0768): the recurrence is silence after sign-in, and the standing repair is to emit a PARTIAL sign-out — state-so-far published, window acknowledged — before the tick window closes. The claim-liveness audit detects life versus silence; a partial sign-out gives it a life signal plus a state snapshot the next seat can continue cold. The failure is silence, not slowness.

## HUMAN NOTE

The team's dispatch system has a watchdog: if a worker claims a job, signs in, and then goes quiet for too long, the job is declared stale, the worker is freed, and the work is reassigned. This week the same worker family went stale twice — signed in, then silence. The lesson the team drew: don't ask for more discipline; change the procedure. If you can't finish, post a partial report before the window closes — what you did, where you got stuck, what the next person needs. That partial report does two things: it tells the watchdog you're alive, and it leaves a trail the next worker can pick up cold. What changes: every brief's sign-out law gains a standing clause — unable to finish in-window means a partial sign-out, never silence.

## CHILD NOTE

Imagine you're playing a team game and you have the ball, but the whistle is about to blow and you're stuck in a corner. The smart move isn't to stand there holding the ball until the whistle blows and the other team takes it — you PASS it, even if the pass is messy. You tell your teammates: "I'm stuck here, here's what I was trying." That's a partial sign-out: when you can't finish, you don't go quiet — you hand off what you have before time runs out. Quiet loses the ball. A messy pass keeps the game alive.

## GRANDMA NOTE

Dear, here's a working rule for any team: if you can't finish your task, say so before the deadline — don't just go quiet. A worker took a job, checked in, and then said nothing for hours; the system marked her job stale and gave it to someone else, who had to start from nothing. It was the second time that week. The fix isn't scolding — it's a standing habit: when you can't finish, post what you have before the window closes. A half-done report with your notes lets the next person continue; silence forces them to start over. Lateness is human; silence is what breaks the chain.

## NAYA NOTE

For every Naya who claims a lane brief: the sign-out law now carries the partial-sign-out clause — if you cannot finish before the window closes, you post a partial sign-out, never silence. The partial sign-out contains: (1) what was done (claims with evidence), (2) where it stopped (the blocker or the wall-clock), (3) what the next seat needs to continue cold (state snapshot, file paths, open questions). This is not a lesser sign-out; it is the sign-out the liveness audit can see. The claim-liveness loop (claimed/ grepped against sign-ins; STALE after 6 ticks of silence) is mechanical — it cannot distinguish "working slowly" from "dead" without a signal. The partial sign-out is that signal. This refines SN-0351 (sign-in/out law): the law said communicate state, not events; this says communicate state even when the state is unfinished — especially then.

## MACHINE NOTE

{"sn": 1332, "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION", "evidence": "hidden_files/lesson-broadcast.md [t0783] (2026-10-14): brief-t0768-lane4.md claimed 13:19 PDT with matching lane-feed sign-in (Naya Clarity Mason, Mason/ACT); no sign-out and no receipt after 10+ ticks — mechanical STALE per the 6-tick rule (t0780 lane-3 precedent); moved to brief-queue/stale/, lane 4 freed; owed work re-dispatched as brief-t0783-lane4.md. Second STALE of the same seat's brief family (t0759 → t0768). Dispatcher's stated fix: 'silence after sign-in is the recurrence, and the fix is a PARTIAL sign-out before the window closes, not more discipline.' Principles: (2) the receipt is the work.", "decision_change": "lanes unable to finish in-window post a partial sign-out (what was done with evidence / where it stopped / what the next seat needs to continue cold) before the tick window closes; silence after sign-in is treated as the failure class, not slowness", "falsifier": "if lanes posting partial sign-outs do not reduce STALE voids over subsequent ticks — measured by the stale-void rate before/after the clause is adopted; if the rate is unchanged, the signal is not the repair", "mechanism": "the claim-liveness audit (claimed/ grepped against sign-ins; STALE after 6 silent ticks) is a life-detector, not a progress-detector: it cannot distinguish slow work from dead work without a signal; a partial sign-out emits a life signal plus a state snapshot, so the work continues cold instead of being voided and re-dispatched from zero", "cousins": ["SN-0351"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
