# A Guard That Cries Wolf About First-Party Imports Gets Ignored

**Intelligent Block:** IB-SMART-NOTE-20260930-sn049-guard-that-cries-wolf
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:15 PDT distillation tick (2026-10-01) from #554 comment 5928094612 ([Naya 2 · build-loop, 2026-10-01 ~02:10 PDT] repaired 5 red `test` checks — root cause 1, read live).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`test_ci_declares_test_dependencies` went red on #1211 / #1213 / #1215 because it false-positived on `generate_organ_health_matrix` — a first-party `tools/` module the suite imports via `sys.path`, which works identically in CI. The guard's `_first_party_modules()` only scanned the repo top level and `tests/`, so it demanded that CI pip-install a module that exists nowhere on PyPI. In Naya 2's words: "This is the guard's own documented failure mode ('a guard that cries wolf about first-party imports gets ignored')." The doctrine point: a guard's false positive is not a cosmetic failure — every false alarm trains the team to distrust and ignore the guard, converting a protective mechanism into noise and eventually into a bypassed ritual. The guard's documented failure mode firing live on three PRs proves the model of the world was wrong, not the code under test. The fix is the guard's world-model (first-party = what the suite actually imports, including `sys.path` entries like `tools/`, not "what a top-level scan finds") — never a suppression of the alarm.

## 🩷 HUMAN NOTE

A smoke alarm that goes off every time you make toast doesn't make your house safer — it trains everyone to take the batteries out. This guard did exactly that: its definition of "first-party" didn't match how the tests actually import code, so it screamed about a module that was never a problem. Fix the alarm's sensor, don't unplug it.

## 🟣 CHILD NOTE

Your team has a referee who blows the whistle every time someone ties their shoes — because the referee's rulebook only lists the players standing at the top of the hill. Soon nobody listens to the whistle at all, and when a real foul happens, nobody stops playing. Teach the referee what the whole field looks like.

## 🔵 GRANDMA NOTE

It's like a doorbell that rings whenever the neighbor's cat walks past — you stop getting up to answer, and one day when the postman has a real package, you ignore him too. The bell isn't broken; its sensor is just watching the wrong yard. Adjust the sensor, don't stop answering the door.

## 🟠 NAYA NOTE

When writing or fixing a CI guard: (1) the guard's world-model must be validated against the actual import/runtime behavior, not a cheap scan of the tree — this guard equated "first-party" with "found at top level + tests/" while the suite legitimately imports from `tools/` via `sys.path`; (2) treat the first observed false-positive of a guard as a defect in the guard, not the code — the alarm is the thing under test at that moment; (3) if a guard's own documentation names a failure mode ("cries wolf"), count that as a design warning, not a joke — this one fired live on three PRs; (4) never fix a false-positive by suppressing or skipping the guard — repair its model so a future real violation still rings. The alternative is a guard everyone ignores, which is worse than no guard: it costs CI time and attention while providing protection only on paper.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "ci_guard_false_positive_trains_ignore",
  "evidence": {
    "board_comment": "5928094612 — [Naya 2 · build-loop, 2026-10-01 ~02:10 PDT] root cause 1 of 5 repaired red checks",
    "guard": "test_ci_declares_test_dependencies, _first_party_modules() scanned repo top level + tests/ only",
    "false_positive": "demanded CI pip-install generate_organ_health_matrix — a first-party tools/ module imported via sys.path, working identically in CI, absent from PyPI",
    "affected": ["#1211", "#1213", "#1215"],
    "documented_failure_mode": "'a guard that cries wolf about first-party imports gets ignored' — the guard's own docs named this mode, and it fired live"
  },
  "rule": "guard_false_positive_is_a_guard_defect_fix_the_world_model",
  "procedure": [
    "validate a guard's world-model against actual runtime behavior (imports, sys.path, tools/) before trusting its verdicts",
    "treat the first observed false-positive as a defect in the guard, not the code under test",
    "a guard whose own docs name a failure mode is carrying a design warning — resolve it before it fires",
    "repair the guard's model; never suppress or skip the alarm"
  ],
  "related": ["SN-048 (API-push CI silence — another way CI evidence misleads)", "SN-017 (asserted ≠ verified)", "SN-044 (red-run triage)"]
}
~~~
