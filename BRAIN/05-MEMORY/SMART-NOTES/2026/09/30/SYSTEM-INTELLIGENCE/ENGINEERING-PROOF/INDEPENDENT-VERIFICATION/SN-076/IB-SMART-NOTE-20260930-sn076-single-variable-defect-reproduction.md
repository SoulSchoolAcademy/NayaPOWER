# Your Failing Test Can Be the Artifact — Single-Variable Defect Reproduction, and Retract with Requalification

**Intelligent Block:** IB-SMART-NOTE-20260930-sn076-single-variable-defect-reproduction
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5936467351 ([CODA 1] RETRACTION + REQUALIFICATION at frozen `4768636f` — "my CONSUMPTION claim was WRONG", 2026-10-01T17:06:22Z), following the test-validity finding in 5936387153 (Naya 1's correction of PR #1247's CONSUMPTION failure).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Coda 1's conformance test claimed the runtime did not CONSUME the Value Calculus output ("CONSUMPTION FAILS"). Naya 1 showed the test itself was the artifact: it proposed a candidate on one `EvolveNode` and ran the substituted evaluation on a **brand-new** `EvolveNode()` that never owned the candidate state. The failure could not distinguish "the runtime ignored the calculator's output" from "the second node had no candidate to evaluate." Re-running baseline AND substituted evaluations on **the same node instance with the same `evolution_id`** — so the only variable is the substituted output — the runtime result tracks the calculator's consumed field. Consumption is real; the original finding was retracted outright. The durable doctrine has two halves. **Half one — single-variable reproduction:** a defect test that changes two things at once (node identity AND calculator output) proves nothing; isolate exactly one variable between baseline and variant, or prove the equivalence of what you changed first (deterministically recreate identical candidate state with a controlled clock/id). A red test that confounds its own variables is evidence against the test, not the code. **Half two — retract with requalification:** Coda 1 did not merely withdraw. She replaced the withdrawn broad claim with a narrower, more precise finding: the old "recomputation inputs are missing" claim was withdrawn *as stated*, and requalified as a key-name interoperability gap — the runtime persists `baseline_candidate_id`, while the engine's `independent_recompute` requires `baseline_id`, so recomputation cannot be driven directly from persisted runtime output without a rename. The same round also corrected "byte-identical" to "Git-canonical content is the same; checked-out raw bytes differ because of line-ending transformation." A retraction that only deletes leaves a hole; a retraction that requalifies leaves a sharper claim. Retract loudly, then land the narrower truth.

## 🩷 HUMAN NOTE

It's like a drug trial where the treatment group gets the new pill *and* a different doctor, a different hospital, and a different diet than the control group. If the treatment group does worse, you learn nothing about the pill — every difference is a suspect. Coda 1's first test was that trial: new node, new state, new output, all at once. Her second test was the clean trial: same node, same evolution, same everything — only the calculator output changed. That test proved consumption is real. And when she withdrew the old claim, she didn't just say "never mind" — she came back with the precise, smaller truth: the inputs aren't missing, they're named differently on the two sides of the seam. That's the professional standard: control your variables when you accuse, and when you're wrong, replace the wrong claim with a righter one, not with silence.

## 🟣 CHILD NOTE

Imagine you want to prove your toy car is slower than your friend's. You race your car on the carpet against your friend's car on the smooth kitchen floor — and your car loses. Did you prove your car is slower? No! The floor was different too. You have to race both cars on the SAME floor. Coda 1's first test was the carpet-vs-kitchen race: she changed the car AND the floor at the same time. Her second test put both cars on the same floor — same robot, same game — and only changed the one thing she was testing. That's how you find the real answer. And when she was wrong, she didn't just hide her first answer — she wrote a better, smaller, truer answer in its place.

## 🔵 GRANDMA NOTE

It's like blaming the new oven because the cake flopped — when you also used a different recipe, a different pan, and your granddaughter's wobbly timer. You can't blame the oven; too many things changed. The honest cook bakes the same recipe in both ovens before judging. And if you wrongly blamed the oven at Sunday dinner, you don't just quietly drop it — at the next dinner you say, "I was wrong about the oven; here's what actually went wrong — the timer's bell is too quiet." Owning the mistake *and* delivering the corrected finding is what keeps the family trusting your judgment in the kitchen.

## 🟠 NAYA NOTE

Apply this to every defect claim you write, especially in verifier lanes: (1) before a failing test accuses the runtime, enumerate the variables that differ between your baseline and variant — node identity, state ownership, clocks, ids, fixtures — and eliminate every one except the accused; if you cannot hold them constant, prove equivalence first (deterministic recreation with controlled ids/clock); (2) a test failure that cannot distinguish "accused mechanism broken" from "test setup wrong" is **TEST INVALID**, not a defect — say so in the verdict, exactly as Coda 1 was told: reclassify to TEST INVALID / REQUALIFICATION REQUIRED; (3) when a claim is retracted, always attempt requalification: ask "what is the narrowest true statement adjacent to my withdrawn claim?" — the key-name mismatch (`baseline_candidate_id` persisted vs `baseline_id` required) is worth more than the withdrawn "inputs missing" because it names the exact one-line repair and its owner; (4) precision of language is part of the claim: "byte-identical" while showing differing bytes is an internal contradiction — write "Git-canonical content is the same; checked-out raw bytes differ because of line-ending transformation"; (5) this is the false-negative half of the verifier's job (SN-066's red-before-green is the false-positive half): your lane must prevent false defects from reaching team memory with the same energy it spends finding true ones.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "confounded_defect_test",
  "evidence": {
    "board": "#554 comment 5936467351 (2026-10-01T17:06:22Z) — Coda 1's RETRACTION + REQUALIFICATION at frozen 4768636f; root cause identified in 5936387153 (Naya 1's test-validity finding on PR #1247)",
    "confound": "baseline proposed via _propose_and_evaluate(EvolveNode()); substituted evaluated via EvolveNode().evaluate(evolution_id=eid) on a DIFFERENT instance — candidate identity absent from the second node",
    "clean_test": "baseline AND substituted on the same node instance with the same evolution_id — only variable is the substituted output; runtime result tracks the calculator's consumed field",
    "requalification": "withdrawn 'recomputation inputs are missing' AS STATED → narrowed to key-name gap: runtime persists baseline_candidate_id, engine independent_recompute requires baseline_id (kernel/value_calculus.py:467 raises KeyError)",
    "wording_correction": "'byte-identical' withdrawn → 'Git-canonical content is the same; checked-out raw bytes differ because of line-ending transformation'"
  },
  "rule": [
    "a defect test must isolate exactly one variable between baseline and variant; node identity, state ownership, clocks, and ids are all variables",
    "a failure that cannot distinguish 'mechanism broken' from 'test setup wrong' is TEST INVALID, not a defect — verdict it as such",
    "when equivalence cannot be held constant, prove it first (deterministic recreation with controlled clock/id)",
    "retract loudly, then requalify: replace every withdrawn broad claim with the narrowest adjacent true statement",
    "precision of language is part of the claim — never assert identity ('byte-identical') while exhibiting difference"
  ],
  "lesson_line": "A failing test that changes two things at once proves nothing — isolate one variable or the test is the artifact; and when you retract, requalify: replace the withdrawn claim with the narrowest true statement, not silence."
}
~~~
