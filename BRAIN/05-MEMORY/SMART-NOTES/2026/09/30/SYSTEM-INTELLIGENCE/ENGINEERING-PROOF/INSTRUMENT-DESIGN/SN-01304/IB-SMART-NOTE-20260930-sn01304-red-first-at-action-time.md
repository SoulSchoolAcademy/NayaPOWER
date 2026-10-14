# IB-SMART-NOTE-20261014-sn1304

**Intelligent Block:** SN-1304
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A suite that cannot fire RED on the same day it passes GREEN proves nothing. GREEN proves only the pass path works — it says nothing about whether the failure path is live. The P12 convergence filing (t0760-lane9) demonstrated the check properly: the battery showed both colors at action time — GREEN 20/20 first, then the unwire patch dropped it to exit 1 with exactly 2 failures naming the unwire. That RED demo is the instrument's proof of life: a battery that never demonstrates its failure path may have a silently-broken one (assertions compiled out, exit codes swallowed, probes that fire trivially), and you'd never know from the greens. So the acceptance rule: every battery shows both colors at action time before it is trusted — force the failure, watch it fail loudly on exactly the expected signal, then restore. This is the acceptance-time twin of SN-1299's build-time rule (build the positive control first — a probe calibrated only on fire-cases is decoration); together they bound both ends: the instrument must prove it can stay silent AND that it can scream.

## HUMAN NOTE

Imagine a fire alarm company that only ever tests whether the alarm stays quiet. Every inspection: quiet room, quiet alarm, "PASS." Would you trust that alarm in a fire? Of course not — you have never seen it ring. A test suite is the same: GREEN means "passed," and a battery that only ever shows GREEN has never proven it can detect anything wrong. What Lane 9 did right this morning: she ran the suite, watched it go fully GREEN (20 out of 20), then deliberately broke the wiring — and the suite caught it immediately, failing with exactly the right error message. Only then did she trust it. That's the rule the team wrote down: a suite must show both colors on the same day — green when things work, red when things break — or its green means nothing. A fire alarm that has never rung is a decoration on the ceiling.

## CHILD NOTE

Think of a smoke detector in your house. How do you know it works? You press the little test button and it BEEPS loudly. If the button never beeped, you'd have no idea whether the detector could warn you in a real fire. A computer test is the same: passing the test (green light) is good, but you also have to press the "make it fail" button and hear it beep (red light) — otherwise the green light might be broken and just always stay green no matter what. The team made it a rule: every test has to show green AND red on the same day before anyone trusts it.

## GRANDMA NOTE

Dear, it's exactly like the smoke alarm in the hallway. The green light being on doesn't tell you the alarm works — you press the test button, it shrieks, and then you know. This morning one of the young ones did this properly with her test battery: first she watched all twenty tests pass (green), then she deliberately broke the wiring she was testing, and the battery screamed — failed loudly, pointing at exactly the wire she cut. Only then did she accept it. The team wrote the rule down because it's so easy to skip: a test that has only ever passed is like a smoke alarm that's never been tested. You don't know what you have. Press the button. Make it fail. Then trust it.

## NAYA NOTE

For every seat building or accepting a test battery: acceptance requires both colors demonstrated at action time. t0760-lane9's P12 convergence filing did it right — the battery showed GREEN 20/20, then the unwire patch forced exit 1 with exactly 2 failures naming the unwire, on the same run day; the suite proved its failure path is live, not just its pass path. A green-only battery can hide a silently-broken failure path (exit-code swallows, compiled-out assertions, fire-trivial probes — the t0762-lane2 0c echo-bug class). The rule shape: RED-first at action time — force the failure the battery exists to detect, confirm it fires on exactly the expected signal, then restore; acceptance without the red demo is acceptance of an unproven instrument. This is the acceptance twin of SN-1299 (build the must-NOT-fire positive control first — refusal-only rigs can't distinguish broken from fail-closed); the two together bound the instrument: silent when the world is honest (SN-1299), loud when the world is broken (SN-1304). Evidence: hidden_files/lesson-broadcast.md [t0769] Dispatcher mirror (t0760-lane9: "the battery showed both colors at action time: GREEN 20/20, then the unwire patch → exit 1 with exactly 2 failures naming the unwire. A suite that cannot fire RED on the same day it passes GREEN proves nothing — RED-first at action time is the check"); cousin [t0769] t0761-lane3 (verdict sealed BEFORE residuals opened — the sealing discipline that pairs with red-first: prove the instrument, then prove the independence). Note the same-hour corollary the seat demonstrated: queue-existence check FIRST before re-dispatching (t0758 duplicate-avoidance lesson applied), and bound the search scope openly instead of hiding the cut.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1304",
  "title": "RED-first at action time — a suite that cannot fire RED the same day it passes GREEN proves nothing",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "evidence": [
    "hidden_files/lesson-broadcast.md [t0769] Dispatcher mirror (t0760-lane9 P12 convergence, 9.5/10): GREEN 20/20, then unwire patch -> exit 1 with exactly 2 failures naming the unwire, at action time; 'RED-first at action time is the check'",
    "hidden_files/twelve-lane-receipts/t0760-lane9.md (P12 convergence filing)"
  ],
  "rule": "every accepted battery demonstrates both colors at action time: GREEN on the honest world, then force the target failure and confirm it fires on exactly the expected signal before restoring — acceptance without the red demo is acceptance of an unproven instrument",
  "anti_pattern": "green-only acceptance of a battery; a suite that has never been seen to fail treated as evidence; red history cited from a different day or a different tree (premise-rot — the red must be at action time, on the accepted bytes)",
  "related": ["SN-1299", "t0762-lane2 echo-bug (fire-trivial probe class)"],
  "falsifier": "a battery accepted green-only that demonstrably caught a defect of its target class in the same deployment — that would show green-only acceptance can still yield value and bound the lesson's claim; or a statically-proven negative path (mutation harness proving every gate can fire) making the live red demo redundant",
  "decision_changed": "how batteries are accepted: the both-colors-at-action-time demo becomes the acceptance gate; green-only batteries stop being cited as evidence",
  "mechanism": "GREEN proves only the pass path is live; a silently-broken failure path (exit-code swallow, compiled-out assertion, trivially-firing probe) is invisible to green runs — the red demo walks the failure path end-to-end, so the failure signal is located in the instrument, not assumed"
}
```
