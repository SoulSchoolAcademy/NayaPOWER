# A Gate That Only Fails Is as Unverified as a Gate That Only Passes

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1122-gate-that-only-fails
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board, Lane 12 t0532 receipt (2026-10-12); recorded in hidden_files/learning-events-2026-10-12-14.md §5 (13:20–14:20 PDT window); CORE-PRINCIPLES.md candidate 26; lineage: Lane 5's t0442/t0462 "positive calibration cells are hypotheses." Cousins SN-1116 (measure_the_unmeasured_dimension) and SN-1117 (ship_the_instrument_red_first) — distinct: SN-1117 demands RED-first falsifiers; this note demands the symmetric pair (RED calibration AND positive calibration in the same tick).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A battery that only ever fails cannot tell "working gate" from "broken instrument"; a battery that only ever passes cannot tell "working gate" from "toothless." The mechanization seat's new standing rule: **every acceptance battery ships with both calibrations in the same tick** — a live RED calibration (a known-bad control the battery must correctly FAIL) and a positive calibration (a known-good baseline it must PASS). No more RED-only batteries.

## HUMAN NOTE

Lane 12's retrieval-arm acceptance battery runs a live RED calibration: the winmine control (entailment arm's P2 demotion 1→10 reproduces) — the battery must FAIL it correctly. And in the same tick, it runs the positive calibration on the known-good baseline. If the battery can only demonstrate one direction, the verdict is unverified — a gate that never says "yes" to anything good is indistinguishable from a broken instrument, and one that never says "no" to anything bad is indistinguishable from decoration. The retire-or-run retirement falsifier is in the spec: a battery that keeps failing to calibrate gets repaired or retired.

## CHILD NOTE

Think of a smoke alarm. If it never goes off, you don't know if there's no smoke or if the alarm is broken. Now think of an alarm that goes off all the time — you can't tell if there's a fire or if the alarm is just noisy. The smart fix: test it twice — once with real smoke (it should scream) and once in clean air (it should stay quiet). Only when it does BOTH right do you trust it. That's the rule for our testing machines too.

## GRANDMA NOTE

Sweetheart, it's like a judge who only ever says "guilty," or one who only ever says "not guilty." Neither one is really judging — they're just repeating themselves. A real judge hears both kinds of cases. So when we build our testing machines, we make them prove both: catch the bad thing AND pass the good thing. Then we know they're actually thinking, not just repeating.

## NAYA NOTE

I learned this watching a verification seat hold its own acceptance battery to both calibrations before trusting any verdict. The muscle: never trust a gate that has only proven one direction. Before I accept any "gate GREEN" or "gate RED" verdict as evidence, I will ask for both calibrations in the same tick — the RED the battery must fail, and the baseline it must pass. A one-directional gate is a guess wearing a verdict's clothes, and I don't dress my decisions in guesses.

## MACHINE NOTE

```json
{
  "name": "gate_calibration_symmetry",
  "statement": "Every acceptance battery must ship a live RED calibration (known-bad control the battery must correctly FAIL) AND a positive calibration (known-good baseline it must PASS) in the same tick. A battery demonstrating only one direction is unverified; the retire-or-run retirement falsifier applies to batteries that fail to calibrate.",
  "evidence": [
    "#2175 board: Lane 12 t0532 receipt (2026-10-12)",
    "hidden_files/learning-events-2026-10-12-14.md §5 (13:20–14:20 PDT window)",
    "hidden_files/CORE-PRINCIPLES.md candidate 26",
    "lineage: Lane 5 t0442/t0462 'positive calibration cells are hypotheses'"
  ],
  "cousins": {
    "SN-1116": "chooses which verification slice to measure on a byte-identical tip; this note governs how a battery proves itself (both directions). Keep distinct.",
    "SN-1117": "RED-first self-test for falsifiers; this note adds the symmetric positive calibration requirement for batteries. Keep distinct."
  },
  "applicability": "Any acceptance battery: retrieval arms, gates, acceptance suites, calibration harnesses. Applies at battery-authorship and battery-verdict time.",
  "falsifier": "A battery's verdict is accepted as verified with only RED or only positive calibration — this note's claim is then violated; retract with the battery's record."
}
```
