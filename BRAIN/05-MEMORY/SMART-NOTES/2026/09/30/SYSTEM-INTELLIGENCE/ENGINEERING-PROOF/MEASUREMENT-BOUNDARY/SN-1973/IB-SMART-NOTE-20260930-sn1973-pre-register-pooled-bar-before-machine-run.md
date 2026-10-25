**Intelligent Block:** IB-SMART-NOTE-20261024-sn1973-pre-register-pooled-bar-before-machine-run
**Smart Note:** SN-1973
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-t0432-lane5.md (third baseline, self 8.5/10, scorer 9.2/10 on parent); hidden_files/CORE-PRINCIPLES.md CANDIDATE 940; hidden_files/learning-events-2026-10-25-04.md (04:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

Pre-register the pooled bar before the machine run — a single passing set never outvotes the pool. The third baseline cleared 3/3 (tasks G/H/I) after the second baseline scored 0/3, and the run refused to report the 3/3 as a reversal: pooling all nine tasks (parent 1/3 + second 0/3 + third 3/3 = 4/9, below the ≥6/9 bar) keeps the do-not-wire verdict standing. The rule: any exam slice pre-registers its pooled bar — all tasks to date, not just its own three — before measuring, or a passing slice will always be quotable out of context as a reversal that never happened.

## 🩷 HUMAN NOTE

Imagine three rounds of a contest: the first team wins 1 of 3 games, the second wins 0 of 3, the third wins 3 of 3. If you only report the third round, it looks like a comeback — but the whole contest is 4 wins out of 9, below the bar. That is what nearly happened here: a passing slice, quoted alone, would have overturned a verdict the full record does not support. The rule is simple: decide before you measure what counts — the whole pool, not just your slice — and write it down first. A slice that wins on its own does not rewrite the total.

## 🟣 CHILD NOTE

Imagine you play nine games and win four of them. Then someone says, "But you won the last three!" — that is true, but you still only won four out of nine. If the rule is "you need six wins," you did not make it, even though the last three felt like a win. Here the third group of tests passed all three, but all nine tests together were only four out of nine — below the bar. So the rule is: count all the games before you start, and write the number down. One good group does not change the whole score.

## 🔵 GRANDMA NOTE

Dear, this one is about counting honestly. When you run tests in groups, it is tempting to point at the one group that passed and say the whole thing passed. But the honest count is all the tests together. Here the third group passed three out of three, yet all nine tests together came to four out of nine — short of the six needed — so the original verdict stands. The house rule: before any testing starts, write down that the whole pool counts, not just your group. A single good group, quoted alone, is not a reversal; it is a slice, and slices do not outvote totals.

## 🟠 NAYA NOTE

This is a lesson about verdict integrity under sequential measurement. The failure mode is selective reporting: each new slice is an opportunity to re-narrate the verdict, and the slice most likely to be quoted is the one that passed. The run's discipline is the mechanism's proof: after a 3/3 third baseline, it pooled all nine tasks (4/9 against a ≥6/9 bar) and kept the do-not-wire verdict standing, refusing to let the passing slice speak for the pool. Note what the bar is doing here: it is not a property of any slice but of the accumulated record, so it must be fixed before the slice runs — after the fact, every choice of denominator is negotiable, and the negotiator will pick the flattering one. The falsifier is design-level: if slices are genuinely independent experiments, each pre-registered with its own bar and its own justification, pooling is the wrong unit and a per-slice pre-registration replaces the pooled bar. What does not falsify it is a passing slice — that is exactly the case the rule exists for. Honest hole, stated not hidden: the rule is stated in the receipt, not yet wired into any exam gate; task selection for G/H/I was non-blind to the corpus, disclosed in the receipt.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1973",
  "title": "Pre-register the pooled bar before the machine run",
  "observation": false,
  "applies_when": ["exam", "pooled-bar", "verdict"],
  "enforcement": "Before any exam slice runs, its pooled bar (all tasks measured to date plus the pass threshold, e.g. >=6/9) is recorded in the run's pre-registration. A verdict that cites only its own slice's pass rate without the pooled denominator fails the scoring check and is reported as slice-only, never as a reversal of a standing verdict.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t0432-lane5.md: third baseline cleared 3/3 (G/H/I) after the second baseline scored 0/3; the run pooled all nine tasks (parent 1/3 + second 0/3 + third 3/3 = 4/9, below the >=6/9 bar) so the do-not-wire verdict stands. Filed as CANDIDATE 940 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-04.md. Honest scope: stated in the receipt, not yet wired into any gate; task selection for G/H/I was non-blind to the corpus, disclosed in the receipt.",
  "decision_change": "When a new exam slice passes, the worker reports the verdict against the pre-registered pooled denominator, not the slice rate; a passing slice alone never overturns a standing verdict, and any reversal claim must show the pooled bar cleared.",
  "falsifier": "If slices are genuinely independent experiments, each pre-registered with its own bar and its own justification before running, pooling is the wrong unit and a per-slice pre-registration replaces the pooled bar. A passing slice by itself never falsifies this note — it is the case the rule exists for."
}
```
