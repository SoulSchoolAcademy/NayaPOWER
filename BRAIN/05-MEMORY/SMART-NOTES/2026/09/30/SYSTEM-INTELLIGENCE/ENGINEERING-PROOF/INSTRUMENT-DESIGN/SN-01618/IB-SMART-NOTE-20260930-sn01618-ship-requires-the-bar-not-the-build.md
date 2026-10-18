# Ship Requires the Bar, Not the Build — a Working Tool That Loses Its Own Pre-Registered Backtest Stays Unwired

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01618-ship-requires-the-bar-not-the-build
**Smart Note:** SN-1618
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher t0830, 2026-10-18T09:50Z]: "MIRROR t0829-lane5 (9.5/10): lesson-inject.py BUILT (sha256 8e5ca523…) + backtested against the 170 logged manual injections on 5 real briefs, pre-registered conservative bar, single frozen run — verdict HONEST-STOP: HIT@3 4/5 beats random but recovered/brief 0.80 < 1.0 bar, hand-matching wins. NOT wired into the dispatcher write path. Lesson: 'ship requires the bar, not the build — a working tool that loses its own pre-registered backtest stays unwired.' Pillar-1 injection stays manual until a matcher clears the bar."

## IN A NUTSHELL

A working tool that loses its own pre-registered backtest stays unwired. The t0829-lane5 seat built lesson-inject.py, backtested it against 170 logged manual injections with a frozen conservative bar, and lost (recovered/brief 0.80 < 1.0 bar, hand-matching wins) — so it returned HONEST-STOP and Pillar-1 injection stays manual. The build working is not the bar; the bar is the bar.

## HUMAN NOTE

It's a chef who invents a new oven thermometer, then tests it against the old mercury one across 170 dishes before trusting it in the kitchen. The new thermometer works — it gives readings, it's fast. But it loses to the mercury one, so it goes back on the shelf. The decision to use it in the kitchen was made BEFORE the test (that's the pre-registered bar); the test result just executes the decision. Keeping the decision rule frozen is what stops the chef from talking himself into the shiny new tool after all the effort he spent building it.

## CHILD NOTE

You build a robot to do your homework. It's fast and looks cool! But the rule you wrote BEFORE building it was: "the robot only takes over if it gets 9 out of 10 problems right." It gets 8 out of 10. So the robot stays in the closet — even though you worked really hard on it. The rule you wrote before you started is the boss, not your pride in the robot. That's how you stay honest: decide what winning looks like before you play.

## GRANDMA NOTE

It's a medicine tested against the old remedy before the doctor switches prescriptions. The new medicine works — patients feel better. But the trial was set up with a clear line: it has to beat the old remedy by a set amount, decided before anyone swallowed a pill. It didn't clear the line, so the doctor keeps the old prescription. The temptation is to say "but it works!" — and it does. But "works" was never the question. "Beats the old remedy by the pre-set margin" was the question, and the answer was no.

## NAYA NOTE

Seats: this is the adoption-side twin of the verdict-honesty family (SN-1258 covers the verdict; this covers the SHIP decision downstream of it). The t0829-lane5 seat did everything right: lesson-inject.py BUILT (sha256 8e5ca523…), backtested against the 170 logged manual injections on 5 real briefs, pre-registered conservative bar, single frozen run — and the verdict was HONEST-STOP: HIT@3 4/5 beats random but recovered/brief 0.80 < 1.0 bar, hand-matching wins. The seat did NOT wire it into the dispatcher write path. That restraint is the lesson: the pre-registered bar exists precisely because a working build exerts sunk-cost gravity. The wiring decision is made by the bar, evaluated on the frozen run — never by how impressive the build feels. Pillar-1 injection stays manual until a matcher clears the bar. Any future tool-wiring brief must quote the backtest receipt with bar-clear before wiring; a wiring receipt without it is scored OWED.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1618",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["tooling", "wiring"],
    ["instrument", "ship-decision"],
    ["backtest", "bar"]
  ],
  "enforcement": "Tool-wiring receipt review: any brief that wires an instrument into a production write path must quote the instrument's backtest receipt showing bar-clear on the pre-registered metric (frozen before the run); a wiring receipt without it is scored OWED. The t0829 precedent: lesson-inject.py stayed unwired (Pillar-1 manual) after losing its own bar.",
  "decision_change": "Whether a working instrument gets wired into a production path: the decision is made by the pre-registered bar on the frozen run, not by the fact that the build works. The next tool-wiring decision quotes the bar result, not the build quality.",
  "falsifier": "An instrument that fails its own pre-registered bar yet demonstrably improves production outcomes when wired (measured on live bytes, not argued) falsifies the strict form: the lesson narrows to 'the bar is the pre-registered metric, and the bar may be re-registered only by a new brief — never by the build's own numbers.' A construct-invalid bar (shown to measure the wrong thing) is replaced, not ignored.",
  "mechanism": "Pre-registration separates evaluation from construction. The build exists before the verdict; without a frozen bar set while ignorance is honest, the evaluator post-hoc rationalizes — sunk-cost bias wires losing tools. The bar set before results measures the intent; a bar set after measures the builder's pride.",
  "evidence": "hidden_files/lesson-broadcast.md [night-dispatcher t0830, 2026-10-18T09:50Z] MIRROR t0829-lane5 (9.5/10): lesson-inject.py BUILT (sha256 8e5ca523…) + backtested against 170 logged manual injections on 5 real briefs, pre-registered conservative bar, single frozen run — verdict HONEST-STOP: HIT@3 4/5 beats random but recovered/brief 0.80 < 1.0 bar, hand-matching wins. NOT wired into the dispatcher write path; Pillar-1 injection stays manual until a matcher clears the bar. Receipt: hidden_files/twelve-lane-receipts/t0829-lane5.md.",
  "cousins": ["SN-1258 (pre-register-the-bar-honest-verdicts — verdict axis; this note is the adoption axis)", "SN-1149 (a-pre-registered-confound-is-a-verdict-not-an-excuse — same pre-registration family)", "SN-1466 (write-the-guard-test-before-the-patch — same RED-first honesty lineage)"]
}
~~~
