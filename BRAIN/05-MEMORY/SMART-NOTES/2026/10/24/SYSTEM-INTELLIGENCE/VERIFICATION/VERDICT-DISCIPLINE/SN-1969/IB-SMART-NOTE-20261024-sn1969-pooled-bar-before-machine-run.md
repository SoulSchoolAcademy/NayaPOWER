**Intelligent Block:** IB-SMART-NOTE-20261024-sn1969-pooled-bar-before-machine-run
**Smart Note:** SN-1969
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-t0432-lane5.md (Lane 5, Seeker hat, 2026-10-25 03:53-04:10 UTC run window as claimed, self-scored 8.5/10; independently scorer-scored 9.2/10 per the gap-gap-gap receipt); hidden_files/learning-events-2026-10-25-04.md (CANDIDATE 940). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

Pre-register the pooled bar before the machine run: a single passing set never outvotes the pool. The third bi-encoder baseline cleared 3/3 tasks (G, H, I), after the second baseline scored 0/3 — and the run refused to report the 3/3 as a reversal. Pooling all nine measured tasks (parent 1/3 + second 0/3 + third 3/3 = 4/9, below the bar of at least 6/9 at HIT at least 2/3) keeps the standing verdict in place: do NOT wire bi-encoder ranking into live dispatch. The 0% to 100% swing across task sets is itself the warning: the instrument's result swings with the task set, so a passing slice quoted alone would become a false wiring decision.

## 🩷 HUMAN NOTE

Imagine three rounds of taste-testing. Round one passes 1 out of 3 cakes, round two passes none, round three passes all three — and someone announces "we passed!" by quoting only round three. That is not honest, because the full record is 4 passes out of 9 tries, below the bar the team set. The honest headline counts every round, not just the good one. That is what happened here: the third test passed, but the pooled score stayed below the bar, so the decision stayed "do not wire this into live use." The rule is simple: agree on the pooled bar before you run the test, and never let one good round overturn the whole record.

## 🟣 CHILD NOTE

Imagine you play three games. You win 1, then 0, then 3 — and you tell your friend "I won them all!" because you only talk about the last game. That is not fair counting. Fair counting says: you won 4 out of 9 games, which is less than the goal. Here the computer test won its last three games, but all nine games together were still below the goal, so the team did not put it into real use. The rule is: count all the games before you decide, and write down the goal before you play — then one good game cannot pretend to be the whole story.

## 🔵 GRANDMA NOTE

Think of it like judging a pie contest over three weekends. The first weekend one pie passes, the second weekend none pass, the third weekend all three pass — and someone wants to declare the baker a winner on the third weekend alone. You would say: hold on, count all nine pies, not just the last three. Four out of nine is not a win. That is exactly the discipline here: the third round looked like a comeback, but it was really a measurement of how much the result swings from one set of tasks to another. The wise move is to set the pooled bar in advance — all tasks counted, goal written down first — so a tempting headline never becomes a bad decision.

## 🟠 NAYA NOTE

For the next Naya who runs an exam slice: the pooled bar is a pre-registration, not a post-hoc rescue. Before the machine runs, record the pool (every task measured to date), the verdict rule, and the threshold — here, at least 6/9 tasks at HIT at least 2/3 — in the seal or comparison record. Then report the slice inside the pool, never instead of it. The gap-gap run is the worked example: third baseline G/H/I passed individually (HIT at 5: G 0.667, H 1.000, I 0.667), yet the pooled 4/9 held the do-not-wire verdict, and the next arm is now correctly scoped — an entailment-rerank arm tested against ALL NINE tasks on the pooled bar, not against a single cherry-picked set. Name the honest hole, as the receipt did: task selection for G/H/I was non-blind to the corpus, so the third-baseline clear could partly reflect selection, and N=9 is still small.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1969",
  "title": "Pre-register the pooled bar before the machine run - a single passing set never outvotes the pool",
  "observation": false,
  "applies_when": ["exam", "verdict", "pooled-bar", "slice-reporting"],
  "enforcement": "Exam-slice gate: before the machine run, the slice records its pooled bar (all tasks measured to date plus the threshold) in the seal or comparison record. A scorer or report check bounces any reversal or wiring claim that cites only the slice's own pass rate without the pooled tally. The next arm is scored against the pooled bar, not against its own slice.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t0432-lane5.md (Lane 5, self 8.5/10; scorer 9.2/10 per gap-gap-gap receipt): third baseline on fresh tasks G gate wiring, H lesson distillation, I lane unblocking passed 3/3 (HIT@5 G 0.667, H 1.000, I 0.667); seal baseline-third-gap-gap-t0432.md sha256 142f24e3558053cb42f67592eb6e81b2a6f6d00686277c3717dc307b93ad0e5d, identical before machine run and after comparison; comparison-third-gap-gap-t0432.json sha256 8d8586c5fc7dbed6710ce2d2d1426cce5c396b602700abc4a19f069e2949e10. Pooled verdict: parent 1/3 + second 0/3 + third 3/3 = 4/9, below the bar of at least 6/9 at HIT at least 2/3, so the do-not-wire verdict stands. Honest hole named in the receipt: G/H/I task selection was non-blind to the corpus, so the 0 percent to 100 percent swing across sets is itself the warning.",
  "decision_change": "When a future exam slice passes, the worker does NOT report it as a reversal or a wiring case on its own pass rate. The worker reports the slice inside the pre-registered pooled tally, and the standing verdict changes only if the pool itself clears the bar. The next arm is designed and scored against all tasks measured to date on the pooled bar.",
  "falsifier": "If the task sets are proven non-comparable (different difficulty, different verdict rule, different instrument) so that pooling mixes unlike exams, the pooled verdict weakens for that pool and the bar must be re-registered, not quoted. Conversely, if a future arm clears the pre-registered pooled bar (at least 6/9), the do-not-wire verdict is overturned by the pool itself, not by any single slice. A single passing slice alone never falsifies the pooled verdict."
}
```
