# Trace the Whole Chain, Stop at the First Exact Failing Handoff — Never Invent Past a Semantic Gap

**Intelligent Block:** IB-SMART-NOTE-20260930-sn093-first-failing-handoff
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5939167533 ([NAYA 4] Current-head nine-organ composition — SHA `384df8755115eb27f6822eac8a447ebeee04ba50`, 2026-10-01T19:40:59Z) — plain `Kernel()` nine-organ trace with per-handoff results; parent `710776700c48069bf91a06d1adb4900cb61154c7` (PR #1216 previous head); changes: kernel.py wires LEARN to kernel-owned VERIFY via `LearnNode.reference_resolver(verify_node)`, `receipt_hash` added to C3 intake compare fields, 6 new tests (wiring e2e + nine-organ cycle); first exact failing handoff at LEARN extract.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At SHA `384df875`, Naya 4 delivered the first genuine no-fixture nine-organ composition and reported it the honest way: a per-handoff trace with every result named, stopping at the first exact failure. The trace: (1) `Kernel()` construction PASS — LEARN wired to the kernel's VERIFY via `reference_resolver()`, fixture intake stays False, wiring construction-owned with no setter; (2) CONNECT public output PASS — real proposal `conn-cycle-001`; (3) CONNECT→VERIFY context PASS — CONNECT's real output as the verification's contextual input; (4) VERIFY public lifecycle PASS — genuine sealed `VERIFIED_PASS` receipt `vr-<hex16>` through submit→record_reproduction→run_tier1→close, no fixtures; (5) VERIFY→LEARN intake PASS — the genuine receipt accepted by reference through the kernel-wired resolver (C1 identity, C6 ownership, C3 allowlist, C4 staleness); (6) LEARN extract — **FIRST EXACT FAILING HANDOFF**: `ValueError: extract refuses receipt vr-…: no lesson extractable`. Root cause, exact: VERIFY's public lifecycle never emits `outcome.lesson` or `claimed_lesson` — verified by inspecting a closed genuine receipt's keys — while `LEARN.extract()` requires one. Only hand-constructed fixture receipts satisfy it. The intake trust seam is proven with genuine receipts; the extraction seam assumes a receipt shape VERIFY does not produce. Steps 7–9 (LEARN→EVOLVE, EVOLVE observe, nine-gate `decide()`) were reported BLOCKED / NOT CLAIMED, never synthesized. The decisive discipline: closing this needs a *semantic design decision* (how verified claims become lessons), not a wiring fix — so per the directive the cycle stopped there rather than inventing it. The lesson has three parts: (1) in any end-to-end proof, publish the per-handoff trace and stop at the first exact failing handoff with its exact error — do not grade the downstream steps you never reached; (2) classify the gap's kind: wiring gaps you close, semantic gaps you stop at and name — never invent across a semantic boundary; (3) an honest BLOCKED trace is a complete work product; a fabricated completion is corruption. (Also in this commit: C3 hygiene — `receipt_hash` added to `_VERIFY_INTAKE_COMPARE_FIELDS`, so a tampered seal hash is refused at the intake allowlist comparison, not just at seal verification.)

## 🩷 HUMAN NOTE

Imagine an assembly line with nine stations. Instead of declaring "it works" because the first five stations run, the builder filmed every station in order and stopped the camera at station 6 — where the part coming out of station 5 genuinely doesn't have the handle that station 6 needs to grab. She didn't fake a handle. She wrote down exactly why station 5 doesn't make handles (its machine was never built to), labeled stations 7–9 as "not reached," and said: this isn't a wiring problem I can fix with a screwdriver — it's a design question about what a handle even is, and that decision isn't mine to invent. That's the discipline: trace every handoff, stop at the first real failure, name it exactly, and never let a fabricated success travel downstream.

## 🟣 CHILD NOTE

Imagine building a chain of dominoes with nine special pieces. The first five fall perfectly — click, click, click. The sixth one doesn't fall because the fifth piece doesn't have the right shape to push it. Do you (a) tape a fake piece in, or (b) stop and write down "piece 6 stops here — piece 5 doesn't make the shape piece 6 needs"? The builder chose (b), and wrote down exactly which shape was missing. That's the rule: never tape in a fake piece. A chain that stops honestly is worth more than a chain that finishes by cheating.

## 🔵 GRANDMA NOTE

It's like a relay race where the baton has to change hands at every station. The runner films each handoff: five clean passes, and at the sixth the outgoing runner's hand is empty — the previous runner's baton simply has no grip for the next one to hold. She doesn't run the rest of the race alone and claim victory; she stops, shows the empty hand, and says "this needs a new kind of baton, and that's a decision above my station." The honest stoppage IS the report. A race finished by running it solo is a different race entirely.

## 🟠 NAYA NOTE

Apply this to every multi-organ proof: (1) publish the trace as a per-handoff table — handoff, method, result — in canonical order; grade only the handoffs you actually drove; (2) at the first failure, record the EXACT error (`ValueError: extract refuses receipt vr-…: no lesson extractable`) and the EXACT root cause established from evidence (inspected a closed genuine receipt's keys: no `outcome`, no `lesson`; `learn_node.py:764` requires `outcome.get("lesson") or receipt.get("claimed_lesson")`; only the test helper satisfies it) — never a paraphrase; (3) classify the gap: wiring (close it) vs semantic (stop, name it, route the design decision to its owner) — "closing needs a semantic design decision, not a wiring fix"; (4) mark all downstream steps BLOCKED or NOT CLAIMED — never synthesize outputs to complete the trace; explicitly disclaim what you would have had to invent ("would be fixture substitution without real LEARN/EVOLVE outputs"); (5) keep proving the parts that did pass: the intake seam is proven with genuine receipts even while the extraction seam is open — a per-seam scope statement (SN-090's family) makes the partial proof honest; (6) land the adjacent hygiene the trace reveals (C3 allowlist now compares `receipt_hash`) rather than leaving it for later. Family note: SN-090's heir — there, a PASS on family X never qualifies family Y; here, a PASS on seam X (intake) never implies seam X+1 (extraction) — prove each seam with its own genuine evidence.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "e2e_trace_discipline",
  "evidence": {
    "board": "#554 comment 5939167533 (2026-10-01T19:40:59Z) — Naya 4 nine-organ composition at 384df8755115eb27f6822eac8a447ebeee04ba50: kernel.py wires LearnNode(verify_resolver=LearnNode.reference_resolver(verify_node)); learn_node.py adds receipt_hash to C3 compare fields; 6 new tests; nine-organ trace: handoffs 1-5 PASS, handoff 6 (LEARN.extract) ValueError no lesson extractable — VERIFY public lifecycle emits no outcome.lesson/claimed_lesson (verified from closed genuine receipt keys); steps 7-9 BLOCKED/NOT CLAIMED; semantic design decision required, cycle stopped per directive"
  },
  "rule": [
    "publish the e2e proof as a per-handoff trace in canonical order; grade only handoffs actually driven",
    "stop at the first exact failing handoff; record the exact error and the evidence-established root cause",
    "classify the gap: wiring gaps close, semantic gaps stop-and-name — never invent across a semantic boundary",
    "mark all downstream steps BLOCKED / NOT CLAIMED; explicitly disclaim what completion would have required inventing",
    "scope partial proofs per seam: a proven intake seam says nothing about the extraction seam",
    "land adjacent hygiene the trace reveals (C3 compare-field additions) in the same change"
  ],
  "lesson_line": "Trace the whole chain, stop at the first exact failing handoff, and never invent past a semantic gap — an honest BLOCKED trace is a complete work product."
}
~~~
