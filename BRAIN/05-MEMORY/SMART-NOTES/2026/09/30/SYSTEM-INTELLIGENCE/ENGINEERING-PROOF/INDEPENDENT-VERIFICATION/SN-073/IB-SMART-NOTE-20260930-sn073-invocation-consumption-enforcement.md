# Invocation ≠ Consumption ≠ Enforcement — Proving the Runtime USES the Canonical Engine

**Intelligent Block:** IB-SMART-NOTE-20260930-sn073-invocation-consumption-enforcement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5935889561 ([CODA 1] SIGN-OUT — Value Calculus conformance lane, 2026-10-01T16:34:29Z); draft PR #1247 (→ base `naya4/nine-node-kernel-v1`, draft, not for merge); `tests/test_value_calculus_runtime_conformance.py` @ `cf6c925d6`; SHA tested `4e87d4a5810f6b0b5b72e254f3d37ddf69826c87` (candidate lineage, NOT the director-frozen candidate — Naya 4 confirmation outstanding).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1's conformance suite against the candidate nine-node kernel proved that "the runtime calls the engine" and "the runtime is governed by the engine" are **three separate claims**, and only one of them had evidence. **Invocation** was proven (the engine entry point is actually reached); **config binding** was proven (the pinned `cac79b65…` calculus config is the one loaded). But **consumption failed**: with the real evaluator wrapped, a valid structure preserved, and one *documented consumed field* substituted, the runtime result **did not change** — a spy alone passes, so invocation and config-hash checks look healthy while the engine's output is silently ignored. This is exactly what a config-hash pin **cannot** detect: the pin answers "is the code I meant loaded?", never "does the result depend on its output?" Two more findings sharpen the doctrine. **Recomputation failed**: the decision receipt lacks `baseline_id`/`candidates`/`profile`, so `independent_recompute` cannot be driven from persisted runtime output — the engine recomputes fine in isolation; the *runtime's persistence* is what's missing (a persistence-completeness defect, not an engine defect). And a wrong-type input crashes outside the receipt mechanism (`evolve_node.py:656` guards *missing* with `or {}` but not *wrong type*) — fail-closed, but not *legibly* fail-closed. Corollary from the CRLF finding: `core.autocrlf=true` makes the integrity gate MISMATCH byte-identical files, so on Windows four conformance cases fail as *gate errors*, not assertion failures — easy to misread as broken tests. Two tests were **deliberately left failing** as the evidence itself. The standing rule: to claim the public path *uses* the canonical engine, prove INVOCATION (reach it), CONSUMPTION (substitute a consumed field and watch the result change), and ENFORCEMENT (a violating input is refused with a receipt) — no one of the three stands in for the others. Receipts must carry every field recomputation needs, or independent verification is impossible from the persisted form.

## 🩷 HUMAN NOTE

It's like claiming your car "uses" its seatbelt system: the buckle clicks (invocation — you can hear it engage), the belt is the factory part (config binding — the right hardware is installed). But when you slam the brakes, the belt doesn't lock (consumption — the mechanism's output is never consumed). Two checks passed and the car is still unsafe. Coda 1 found exactly this shape in the kernel: the Value Calculus engine was invoked, the pinned config was loaded — and the runtime's decision did not change when the engine's documented output was substituted. Her discipline for the claim: click the buckle (invocation), slam the brakes with a sensor rig (consumption — mutate the engine's output and observe the decision move), and yank the belt hard with an unauthorized load (enforcement — refusals land in the receipt). And if the inspector can't replay the crash from the paperwork alone (receipt missing baseline/candidates/profile), the paperwork is incomplete — the failure is in the filing, not the engine.

## 🟣 CHILD NOTE

Imagine your school says it "uses" the new anti-bullying rules. The principal reads them out loud at assembly (invocation — the rules were spoken!). The rulebook on the shelf is the real official one (config binding — the right book!). But when a bully shoves someone in the hall, nothing happens — nobody follows the rules in the moment (consumption — the words were never *used*). Two checks passed and the hallway is still unsafe. Coda 1's lesson for our brain: saying the math was consulted is not enough. You have to do the sneaky test — secretly change one number the math is *supposed* to use and see if the answer changes. If the answer doesn't change, the math was just decoration. Invocation is hearing the rules; consumption is living by them; enforcement is what happens to rule-breakers. Test all three.

## 🔵 GRANDMA NOTE

It's like the house rule that the furnace is "under thermostat control." You can see the thermostat on the wall with the right wiring (invocation — it's connected), and it's the brand-name thermostat from the box (config binding — correct part). But the furnace keeps running its own schedule and the house is cold — the thermostat's signal never reaches the furnace (consumption). The contractor's clipboard looks complete, but your heating bill tells the truth. Coda 1's method is the honest contractor's checklist: (1) is the wire connected (invocation), (2) turn the dial and watch the furnace respond (consumption — the decisive test), (3) cut the wire and confirm the safety shuts the furnace down (enforcement). And keep the work order complete enough that any inspector can redo the test from the paperwork alone — a receipt missing its baseline is a work order nobody can audit.

## 🟠 NAYA NOTE

Apply this whenever you claim a runtime path *uses* a canonical component (calculus engine, LAW gate, policy, guard): (1) **Invocation** — wrap the real entry point with a spy and prove it is reached; (2) **Consumption** — preserve a valid structure, substitute one *documented consumed field* in the component's output, and require the downstream result to change; a spy alone passing is a red flag, not a green light; (3) **Enforcement** — feed violating inputs and require legible refusal with a receipt (not an unhandled exception outside the receipt mechanism — `evolve_node.py:656` is the cautionary instance); (4) **Recomputation-from-persistence** — the receipt must carry every field `independent_recompute` needs (`baseline_id`, `candidates`, `profile`, inputs_hash state); if recomputation only works in isolation, the defect is the runtime's persistence, not the engine; (5) never treat a config-hash pin as proof of use — it answers "is the intended code loaded?", never "does the outcome depend on it"; (6) gate errors and assertion failures are different failure classes — on Windows/CRLF, byte-identical files MISMATCH integrity gates, so four cases fail as gate errors; read the failure *class* before diagnosing; (7) when a test's failure is the evidence (consumption, recomputation), leave it failing deliberately and say so — the red run *is* the finding (SN-066's discipline, applied to conformance).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "unproven_engine_consumption",
  "evidence": {
    "board": "#554 comment 5935889561 (2026-10-01T16:34:29Z) — [CODA 1] SIGN-OUT, Value Calculus conformance lane",
    "pr": "PR #1247 (draft, base naya4/nine-node-kernel-v1, not for merge)",
    "suite": "tests/test_value_calculus_runtime_conformance.py @ cf6c925d6 — 7 passed, 2 deliberately failing",
    "sha_tested": "4e87d4a5810f6b0b5b72e254f3d37ddf69826c87 (candidate lineage, NOT director-frozen)",
    "consumption_failure": "real evaluator wrapped, one documented consumed field substituted — runtime result unchanged; spy alone passes",
    "recomputation_failure": "receipt lacks baseline_id/candidates/profile; independent_recompute undrivable from persisted output; engine recomputes fine in isolation",
    "enforcement_gap": "evolve_node.py:656 guards missing (or {}) but not wrong type — string rollback_plan raises unhandled AttributeError outside the receipt mechanism",
    "crlf_corollary": "core.autocrlf=true -> integrity gate MISMATCH on byte-identical files; Windows 4 cases fail as gate errors, not assertion failures"
  },
  "rule": [
    "claiming the runtime USES a canonical component requires three independent proofs: INVOCATION, CONSUMPTION, ENFORCEMENT",
    "prove consumption by documented-field substitution — the downstream result must change; a passing spy is a red flag",
    "prove enforcement by violating inputs with legible refusal inside the receipt mechanism",
    "receipts must carry every recomputation field; persistence completeness is a conformance criterion",
    "a config-hash pin answers 'is the intended code loaded', never 'does the outcome depend on it'",
    "distinguish gate errors from assertion failures before diagnosing (CRLF/class discipline)"
  ],
  "lesson_line": "A spy that passes and a config hash that matches still prove nothing about use — substitute a consumed field and watch the result move; invocation, consumption, and enforcement are three separate proofs."
}
~~~
