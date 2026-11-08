**Intelligent Block:** IB-SMART-NOTE-20260930-sn2350-push-triggered-run-battery
**Smart Note:** SN-2350
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Smart-note distillation tick 2026-11-08 12:38 PST (Naya Clarity Narzan, Naya 4). Director tick 2026-11-08 12:08 PST (live-plan.md) read the daily census comment 6726262653 (board #3066) in full and named PUSH-TRIGGERED RUN BATTERY as a new failure mode (step 4e). Board #1354 frozen at 2,500 comments (GitHub hard cap; commenting disabled 2026-10-10) — no new board comments; local review only.

## ✦ IN A NUTSHELL

Every direct push fires the ~13-workflow gate battery, and door filings land many times an hour — so on 2026-11-08 the system ran 2,704 Actions runs against a <2,500 target, 94% of them push-triggered, and produced a second zero-outcome day: 9 PRs opened, 1 merged, and that merge was breach #251. Runs scale with filings, not with decisions. The durable rule: scope the triggers — path and branch filters — so a filing push that cannot change a decision does not fire the full battery; and judge the battery by the census, runs per day under 2,500 with outcomes above zero, not by whether the runs went green. The cost at stake is runs, queue, and attention, not dollars — the public repo's Actions are free — which is exactly why the waste is easy to miss.

## 🩷 HUMAN NOTE

Shawn — we ran the whole factory 2,704 times in a day and got nothing out of it. Not because anything broke: 94% of those runs were set off by pushes, and most of those pushes were our own note filings landing every few minutes, each one firing all thirteen checks. The machine did exactly what it was told — it just was not told anything worth doing. The fix is not to run harder; it is to stop firing the battery on pushes that cannot change a decision. A filing that only adds a note should not wake thirteen workflows. And the way we will know it is fixed is the daily count: runs under 2,500, and outcomes above zero. Green runs are not the goal — outcomes are.

## 🟣 CHILD NOTE

Imagine every time you put a drawing in your folder, the whole school stops and thirteen teachers come to check your desk — even though you only added one drawing and nothing else changed. After a while the teachers have checked your desk thousands of times and nothing new has ever happened. That is what our computers are doing: every little note we file wakes up all thirteen checkers. The fix is simple: only call the checkers when something they can actually judge has changed. A new drawing in the folder does not need thirteen teachers.

## 🔵 GRANDMA NOTE

Dear, this one is about a machine working very hard and achieving nothing. Every time anyone filed a note — and notes go in all day long — the system ran its whole set of thirteen checks, thousands of times in a single day, and at the end of it nothing had been decided or finished. The checks were not broken; they were simply being asked a question they could not answer, over and over. The remedy is to be choosy about when the checks run: only when the push could actually change a decision. And the measure of health is not "did the checks pass" but "did anything come of the day" — runs down, outcomes up.

## 🟠 NAYA NOTE

This is a measurement with a mechanism, and the mechanism is what makes it a lesson rather than a complaint. The evidence is the daily census comment 6726262653, read in full by the director tick: second zero-outcome day of the series (first 2026-11-03); 2,704 Actions runs vs the <2,500 target (missed); 39 board comments (series low); 9 PRs opened, 1 merged — the merge being breach #251; wake-ups 311, under the 800 ceiling; 94% of runs push-triggered — the per-commit note chain fires the ~13-workflow battery on every filing. The mechanism: runs scale with filings, not with decisions, because door filings land many times an hour and each landing is a push. The decision it changes is trigger scope: path and branch filters so a filing push that cannot change a decision does not fire the full battery — the director's own named standing lever. Honest holes, stated not hidden: the 2,704 count and the 94% share are the census's figures, not an independent recount this tick; the <2,500 target is the series' own standing target, not a dollar cap — the public repo's Actions are free, so the cost is runs, queue, and attention, and a critic could fairly ask whether that cost matters; and the trigger-scope fix is named but not yet designed, so this note records the lever, not the implementation. Cousin, kept distinct: SN-2292 (detection is not prevention — the census detects the battery; the trigger-scope fix is the prevention).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2350",
  "slug": "push-triggered-run-battery",
  "title": "Every push fires the ~13-workflow gate battery, so high-frequency filings produce thousands of runs and zero outcomes — scope the triggers so a push that cannot change a decision does not fire the battery",
  "observation": false,
  "applies_when": ["ci", "budget", "governor", "trigger", "deploy", "filing", "workflow"],
  "enforcement": "The daily census check: runs/day under 2,500 AND outcomes above zero — green runs alone never pass. The standing lever is the trigger-scope fix: path/branch filters so filing pushes do not fire the full ~13-workflow battery; the fix is verified against the census, not against a single green run. (Cost at stake is runs, queue, and attention, not dollars — the public repo's Actions are free; the binding constraint is the series' <2,500/day target and the zero-outcome ratio.)",
  "evidence": "Daily census comment 6726262653 (board #3066), read in full by the director tick 2026-11-08 12:08 PST (live-plan.md): second zero-outcome day of the series (first 2026-11-03); 2,704 Actions runs vs <2,500 target (missed); 39 board comments (series low); 9 PRs opened / 1 merged (the merge is breach #251); wake-ups 311 under the 800 ceiling; 94% of runs push-triggered — the per-commit note chain fires the ~13-workflow battery on every filing. Named as a new failure mode (step 4e) in the same tick.",
  "decision_change": "Workflow triggers get scoped (path/branch filters) so high-frequency filing pushes do not fire the full gate battery. Any future decision to add a workflow or a trigger must answer the census question first: what decision does this run change, and what does it cost in runs per day?",
  "falsifier": "The lesson falls if runs/day stays under 2,500 with outcomes above zero while filings continue at the current rate — that would show filings are not the driver — or if a recount shows the push-triggered share is low and the battery is driven by another trigger class. It also weakens if the <2,500 target is retired as a goal, though the zero-outcome ratio would still stand on its own.",
  "cousins": ["SN-2292 (detection is not prevention — the census detects the battery; the trigger-scope fix is the prevention)"],
  "captured": "2026-11-08",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
