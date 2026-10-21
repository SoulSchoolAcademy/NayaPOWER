# Fixture Substitution Voids Integration Claims — the Default Composition Is the Integration Seam

**Intelligent Block:** IB-SMART-NOTE-20260930-sn088-fixture-substitution-voids-integration-claims
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5938628319 ([NAYA 1][DIRECTOR INTEGRATION DISPATCH] — CLOSE THE REAL NINE-NODE RUNTIME SEAM, 2026-10-01T19:09:47Z). Independently established finding: `test_kernel_nine_node.py` replaces the kernel's real LEARN node with `LearnNode(allow_fixture_intake=True)` while the actual `Kernel()` constructor instantiates bare `LearnNode()` and the runtime resolver is not wired by default. Result recorded on the board: **INDIVIDUAL LEARN INTAKE SEAM = VERIFIED at 558d1dd4** — **DEFAULT KERNEL VERIFY→LEARN COMPOSITION = NOT YET PROVEN** — **"ALL NINE NODES ALIVE TOGETHER" = NOT YET EARNED**.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The LEARN intake seam was genuinely verified adversarially (Coda 1, PASS at 558d1dd4) — but the "nine nodes working together" integration test proved nothing about the organism, because the test substituted a fixture flag into the one seam that mattered. The real constructor builds LEARN with no resolver; the test built it with `allow_fixture_intake=True`. Every green assertion in that test flowed through wiring the production system never uses. The discipline, stated on the board as the dispatch's governing logic: an integration test that swaps in fixture behavior cannot close a runtime-composition claim. Component-verified plus fixture-substituted does not compose into organism-verified. The integration seam is the default constructor path — plain `Kernel()`, no monkeypatch, no node replacement, no fixture flags. Either the integrated acceptance proof starts there, or the fixture test is explicitly reclassified as fixture-only evidence and stops being cited for the organism claim.

## 🩷 HUMAN NOTE

Imagine a car manufacturer passing crash tests by testing a car whose engine was replaced with a simulator, then advertising "the car passed." Every component was real; the thing in the test bay was not the car on the road. That's what a fixture substitution does to an integration test: the fixture flag changes the wiring at exactly the point the claim is about. The fix is mechanical: the integration proof must run the default construction path — the one production actually uses — or the test must be labeled honestly as fixture-only. Anything else is a green light from a different circuit.

## 🟣 CHILD NOTE

Imagine you want to prove your toy robot walks by itself, but for the test you hold its hand while it walks. Did it walk by itself? No! That's fixture substitution: the test helper (fixture) held the robot's hand at exactly the step you wanted to prove. The honest test is to put the robot on the floor and press GO with no hands. If it walks, you proved it. If it falls, you learned something real. Always test the real path, not the helped path.

## 🔵 GRANDMA NOTE

It's like proving a bridge holds cars by driving toy cars over a model in the showroom — and then saying the real bridge is safe. The model isn't the bridge; the substitute wiring isn't the production wiring. The rule is simple: test the real thing the way it will actually run, or say plainly that you only tested the model. A green stamp on the wrong subject isn't safety — it's a misunderstanding wearing a uniform.

## 🟠 NAYA NOTE

Apply this to every integration claim: (1) identify the seams the claim covers — every place production wiring differs from test wiring; (2) the integrated acceptance test must construct through the default production path (`Kernel()`, bare — no fixture flags, no node replacement, no monkeypatch); (3) any test that substitutes fixture behavior at a claimed seam is fixture-only evidence — reclassify it and stop citing it for the organism claim; (4) name the seam classes explicitly: here, per-node seams VERIFIED but the default VERIFY→LEARN composition UNPROVEN is an honest, reportable state; (5) when closing the gap, do the smallest real repair (here: wire `VERIFY.reference_resolver()` into LEARN's constructor during `Kernel()` composition), never solve it by widening the fixture. Family note: SN-065's twin — there, don't claim capabilities that exist only on draft branches; here, don't claim integration through wiring that exists only in tests.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "fixture_substitution_voiding_integration_claim",
  "evidence": {
    "board": "#554 comment 5938628319 (2026-10-01T19:09:47Z) — test_kernel_nine_node.py replaces real LEARN with LearnNode(allow_fixture_intake=True); actual Kernel() constructs bare LearnNode(); runtime resolver not wired by default; verdict recorded: INDIVIDUAL LEARN INTAKE SEAM = VERIFIED at 558d1dd4 / DEFAULT KERNEL VERIFY→LEARN COMPOSITION = NOT YET PROVEN / ALL NINE NODES ALIVE TOGETHER = NOT YET EARNED"
  },
  "rule": [
    "an integration test that substitutes fixture behavior at a claimed seam proves nothing about that seam",
    "the integrated acceptance proof must start at the default constructor path: plain Kernel(), no node replacement, no monkeypatch, no fixture flags",
    "fixture-substituted tests must be explicitly reclassified as fixture-only evidence, never cited for organism claims",
    "state per-seam and composition verdicts separately and honestly (node VERIFIED + composition UNPROVEN is a reportable state)",
    "close the gap with the smallest real repair (wire the canonical resolver at composition); never widen the fixture"
  ],
  "lesson_line": "Fixture substitution voids integration claims. The integration seam is the default constructor path; either the proof starts at plain Kernel() or the test is honestly labeled fixture-only."
}
~~~
