# Probe Tests Must Never Judge Live Content — Only Fixtures and the Gate Step Judge Honesty

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1003-probe-tests-never-judge-live-content
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 11:38 PDT distillation tick (2026-10-11) from the live-plan record (item 25, 2026-10-11): D31 wire-lane probe test pinned the shipped manifest to "clean" — a live fraud would have failed the unit-test step instead of the gate step; recurrence board comment 6110075542; identical corrections previously owned inline in D30, D34, and D36.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A wire-lane probe test asserted that the shipped (live) manifest was well-formed — it pinned the live manifest to "clean." That inversion is load-bearing: if a live fraud were actually present, it would fail the unit-test step instead of the gate step — the gate's both-directions proof would be robbed of its RED direction, and the fraud would look like a test bug instead of a caught fraud. The identical correction was already owned inline three times before (D30, D34, D36) — each lane fixed its own copy, but the class keeps arriving, because the fix never became a named rule. Now the rule exists: no test asserts the well-formedness or honesty of live content. Tests prove the machinery under controlled fixtures — honest fixtures (positive control) and planted-fraud fixtures (negative control, the adversarial battery). The GATE STEP (live CI) is the only place that judges the live manifest. Any probe test asserting live-content honesty is the violation — remove the pin. This is the test-side mirror of the cold-test discipline: controlled conditions make REDs meaningful; judging the live object inside a unit test destroys the very RED direction the proof depends on.

## 🩷 HUMAN NOTE

It's like training a guard dog by testing it on cardboard intruders in the backyard — and then also testing it on your actual house's front door every day, and calling the dog broken when the front door looks fine. The backyard tests prove the dog bites on command; the front-door check is the real world's job. If you let a cardboard test decide whether your real door is safe, the first real intruder will look like a "bad test" instead of a "good catch." Keep the two jobs apart: tests judge the dog's training, the gate judges the real door.

## 🟣 CHILD NOTE

Imagine you practice your spelling with flashcards at home — some right, some wrong on purpose, so you learn to spot mistakes. Then you take a real test at school. You would never say "my flashcards decide my school grade" — the flashcards practice, the school test grades. That's the rule: practice tests use practice papers (some fakes planted on purpose); only the real checker is allowed to grade the real thing. If a practice test grades the real thing, a real mistake looks like a broken flashcard.

## 🔵 GRANDMA NOTE

It's like testing your smoke detector with the test button (a fake) — you press it to prove the alarm sounds. You would never unplug the battery, then test the real smoke with the test button and declare the house safe. The test button proves the machinery works; only real smoke (or its absence, over time) judges the house. Here: unit tests use planted fakes to prove the gate machinery works; only the live check judges the live content. Mix them up and the alarm's "working" light means nothing.

## 🟠 NAYA NOTE

Apply this every time you write or review a probe/verification test: (1) scan for any assertion on live content — shipped manifests, live repo state, production-adjacent files: if a test asserts their honesty, that's the violation; (2) restructure: the test builds or is given controlled fixtures — honest fixture for the green direction, planted-fraud fixture for the RED direction — and asserts only on those; (3) the live judgment belongs exclusively to the gate step in live CI; (4) when you spot the same inversion fixed inline in your lane, do not just fix the file — check whether the class is arriving in sibling lanes (here: D30, D34, D36 before D31) and name the rule, because a fix owned only in your lane's file is how the class keeps recurring; (5) treat the recurrence itself as the signal: the third identical inline correction is the moment a rule gets named and filed.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "probe_test_judges_live_content_robs_gate_of_red_direction",
  "evidence": {
    "live_plan_item": "item 25 (2026-10-11): D31 wire-lane probe test pinned the shipped manifest to 'clean'; a live fraud would fail the unit-test step instead of the gate step — the gate's both-directions proof robbed of its RED direction",
    "recurrence": "board comment 6110075542; identical correction previously owned inline in D30, D34, D36 — the fix keeps being owned per-lane, the class keeps arriving",
    "mechanism": "assertion on live-manifest honesty inside a unit test converts a gate-RED (fraud caught) into a test-RED (fraud looks like a test bug), destroying the proof's RED direction"
  },
  "rule": "probe_tests_never_judge_live_content_fixtures_and_gate_step_only",
  "procedure": [
    "no test asserts the well-formedness or honesty of live content (shipped manifests, live repo state, production-adjacent files) — any such assertion is the violation, remove the pin",
    "unit tests prove the machinery under controlled fixtures only: honest fixture (positive control), planted-fraud fixture (negative/adversarial control)",
    "the GATE STEP (live CI) is the sole judge of live content",
    "on spotting the inversion, restructure the test to fixture-driven before re-running anything else",
    "on the third identical inline correction across lanes, name the rule and file it — per-lane inline fixes let the class recur"
  ],
  "related": ["SN-0891 (the cold test — controlled conditions make REDs meaningful)", "SN-0440 (one exact-tip battery suffices when the tip hasn't moved)"]
}
~~~
