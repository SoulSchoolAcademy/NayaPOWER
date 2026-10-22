# IB-SMART-NOTE-20260930-sn01799-two-key-void-rule

Intelligent Block: SYSTEM-INTELLIGENCE / GOVERNANCE / LANE-COORDINATION / DISPATCH-DESIGN
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A dispatcher voids a claimed brief ONLY on the worker's clock, never the queue's: the void requires the 6-tick / 60-min-from-claim bar AND (a prior-tick flag OR the 9-tick / 90-min bar) — never on dispatch age, never inside the worker's 45-minute work window. A void that kills a live worker's brief is queue rot with a stamp on it.

## 🩷 HUMAN NOTE
The night dispatcher watches briefs that workers have claimed. When one looks stuck, the dispatcher can void the claim and send the brief back to the queue. But "stuck" must be measured from when the worker claimed it — not from when the brief was written. Tonight a brief that had waited 21 ticks in a backed-up queue was voided after only 17 minutes of worker time, while the worker was still alive: the queue's wait was mistaken for the worker's idleness, and live work was destroyed. The standing rule going forward has two keys: enough time must pass on the WORKER's clock, AND the brief was already flagged (or a longer bar passed). Judge the worker on the worker's time.

## 🟣 CHILD NOTE
Imagine you lend your friend a book and say "bring it back in one hour." After 20 minutes you snatch it back because the book sat on YOUR shelf for a whole week before you lent it. That is silly — the week on the shelf was never your friend's time. You judge your friend on THEIR hour, not your shelf's week. Same with jobs: you count from when the worker starts, never from when you first thought of the job.

## 🔵 GRANDMA NOTE
When you ask someone to do a job, you give them a fair amount of time measured from when THEY start — not from when you first wrote the job down. Taking the job away early because YOU waited a long time to hand it over is punishing them for your delay. And you only take it back when two things are both true: enough of their time has passed, AND you already warned them last time (or much more time has passed). Taking work from someone who is still doing it does not fix a slow line — it just breaks good work.

## 🟠 NAYA NOTE
Dispatcher-seat doctrine, binding on the night-dispatcher tick and any seat voiding a claimed brief. A void is a liveness judgment on the WORKER, so its age basis is claim → now (the claim timestamp), never dispatch age (queue wait), never file mtime. The body's 2c(ii) bar is 6 ticks / 60 min FROM CLAIM. Standing two-key rule: void a signed-in claimed brief ONLY when (key 1) the 6-tick/60-min-from-claim bar is hit AND (key 2) the prior tick flagged it OR the 9-tick/90-min bar is hit. Never on dispatch age. Never inside the worker's 45-min work window. Voids move the brief to stale/ (recoverable), never delete — tonight's 04:50Z repair restored brief-t1211-lane10.md to brief-queue/ and re-registered it, and the freshness-gate task went live again. Note the failure shape: the 04:24Z void QUOTED the t1226 lesson ("the stale clock starts at CLAIM") while violating it — citing a lesson is not applying it; the ledger line must show the claim timestamp and the bar hit. Cousins: SN-1244 (clock the claim from sign-in evidence — measurement-source sibling; this note is the void-decision sibling), SN-1260 (claim without sign-in), SN-1374 (post-void re-dispatch), SN-1377 (pre-claim stale retirement).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1799",
  "slug": "two-key-void-rule",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION/DISPATCH-DESIGN",
  "applies_when": [["dispatch","stale-claim-void"],["queue","claim-lifecycle"],["dispatcher","tick-judgment"]],
  "enforcement": "the night-dispatcher void path must cite the claim timestamp and the bar hit in the queue-ledger void line; a void line citing dispatch age, queue wait, or file mtime fails the ledger audit; voids move the brief to stale/ (recoverable), never delete, so a wrong void is repairable as the 04:50Z t1211 repair demonstrated",
  "decision_changed": "the dispatcher's void decision on a claimed brief: age computed from claim timestamp; requires 6-tick/60-min-from-claim bar AND (prior-tick flag OR 9-tick/90-min bar); forbids dispatch-age voids and voids inside the 45-min work window",
  "falsifier": "a documented case where a void on dispatch age (or inside the 45-min window) correctly killed a verifiably dead worker (runtime timeout or crash log on record), or measured evidence that the two-key rule lets dead claims circulate and rot the queue worse than the occasional live-kill it prevents",
  "mechanism": "clock-phenomenon attribution: a void judges worker liveness, so it is computed on the worker's clock (claim age: 60-min claim-to-sign-in window, 45-min work window); dispatch age measures queue backlog/throttle, a different phenomenon; attributing the wrong clock to the judgment kills live workers and destroys in-flight work",
  "evidence": [
    "hidden_files/lesson-broadcast.md [lead adjudication 2026-10-22T04:50Z — t1211 STALE-CLAIM CORRECTION]: void at 04:24Z cited '21 ticks' dispatch age; claim was 04:07:00Z with live sign-in, worker alive until ~04:30Z; standing two-key rule issued; brief restored and re-registered",
    "hidden_files/lesson-broadcast.md [2026-10-22T04:24:50Z STALE-CLAIM void of brief-t1211-lane10.md: moved to stale/ on '21 ticks' with claim-age 17 min]",
    "hidden_files/lesson-broadcast.md [night-dispatcher t1226 2026-10-22T03:12Z: 'the stale clock starts at CLAIM, not at the dispatcher's last judgment' — the lesson the t1211 void quoted while violating]"
  ],
  "cousins": ["SN-1244","SN-1260","SN-1374","SN-1377"],
  "repair_precedent": "brief-t1211-lane10.md restored to brief-queue/ and re-registered (queued 29→30); freshness-gate 5-green-tip verdict task live again"
}
```
