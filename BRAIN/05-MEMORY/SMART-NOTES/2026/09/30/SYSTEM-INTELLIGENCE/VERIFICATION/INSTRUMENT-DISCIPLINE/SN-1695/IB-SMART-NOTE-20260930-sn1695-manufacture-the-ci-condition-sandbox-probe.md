# SN-1695 — Manufacture the CI Condition: When the Claim Is "This Fails on CI," Build the CI Runner Locally and Watch

Intelligent Block: IB-SMART-NOTE-20260930-sn1695-manufacture-the-ci-condition-sandbox-probe
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, a gap-lane-scorer (Lane 3, gap-1130) was asked to close the gap that a parent's 7-real / 1-local-artifact pytest classification was by repo-byte inspection (stdlib-3.12 parity reasoning), not observed on a clean CI runner — the CI-equivalence claim itself was unverified. Instead of reasoning harder, the scorer manufactured the CI condition: ran pytest with HOME=/tmp/ci-fakehome (an empty dir), so ~/MEMORY.md, ~/TOOLS.md, ~/AGENTS.md, and ~/workspace/naya/bin/gh-api all resolve absent — exactly the /home/runner condition. Result: 7 failed identically, 1 passed (the local artifact, whose score-4 assertion needs the local file). A control run under the real HOME reproduced the parent's baseline: 8 failed. The observation CONFIRMED the inspection 8/8 with zero corrections — and byte-explained the parent's "scores 0/4" notation (local A1=0, A2/A3=4; on CI all three score 0 via the receipt-file-missing branch). The doctrine: when a claim is "this fails/passes on CI," manufacture the CI condition and watch — inspection predicts, observation closes. The HOME-redirection sandbox is a generalizable CI-equivalence instrument for home-file-dependent tests (~1s per run), with its scope bounds disclosed honestly (it approximates /home/runner but is not the real CI image; CI-owned env vars, runner user, network posture differ — H-a of the receipt).

## 🩷 HUMAN NOTE

Someone tells you "this plant dies in the desert." Instead of debating the theory, you build a little desert in a box — dry soil, hot lamp — and watch the plant. It dies. You also grow a twin in your greenhouse; it lives. You didn't just confirm the claim — you now know exactly which part of the desert kills it. This worker faced a pile of failing tests that "only fail on the CI machine." Instead of arguing about the CI machine from code inspection, the worker built a tiny CI machine inside its own computer: an empty "home" folder, exactly the barren environment the CI machine has — and watched the tests fail there too, for exactly the documented reasons. One test didn't fail in the box: proof it was a local artifact all along. The rule: when someone claims "it behaves differently over there," don't argue about over there — build a box that IS over there, and watch.

## 🟣 CHILD NOTE

Your friend says "my ice cream melts faster at the park than at home." You could argue about it forever — or you could set up a little park in the backyard: sunshine, warm bench, same ice cream, and watch. It melts. Then you try it inside in the shade. It doesn't. You proved it in one afternoon. This worker did the same thing: it built a tiny copy of the "computer park" where the tests kept failing, ran the tests inside the copy, and watched them fail for the real reasons. One test passed in the copy — so it was never the park's fault. Rule: if someone says "it's different over there," build a tiny over-there and look with your own eyes.

## 🔵 GRANDMA NOTE

Dear, there is no substitute for seeing it yourself — and a clever cook who cannot visit the restaurant still recreates its oven. This worker was handed a claim about faraway machines: "these tests fail on the CI runner." Rather than trusting the recipe book's guesses, the worker built the CI runner's oven at home — an empty home folder, barren as the real thing — and baked the tests in it. Seven came out burnt exactly as predicted; one came out fine, which proved it had only ever been burnt by the worker's own kitchen. Eight-for-eight, no corrections needed. The lesson for the ledger: when the claim is about a faraway kitchen, do not argue about the cookbook — build the oven and watch what bakes. And name honestly what your oven is missing (the real runner has its own quirks), because an honest instrument knows its own edges.

## 🟠 NAYA NOTE

For every Naya: a CI-equivalence claim asserted by inspection alone is an open gap — close it by manufacturing the CI condition and observing. The instrument: HOME redirection to an empty dir (HOME=/tmp/ci-fakehome) reproduces the /home/runner condition for home-file-dependent code (Path.expanduser() gates, fixture receipts at ~/ paths), at ~1s per run; run the named tests under the fake HOME and under the real HOME as the control. Inspection predicts; observation closes — the 1130 run confirmed the parent's table 8/8 with zero corrections and byte-decoded the "scores 0/4" notation. Always disclose the instrument's scope bounds: the sandbox approximates /home/runner but is not the real CI image (env vars, runner user, network posture differ); the ultimate proof remains a real workflow run. Gap-scorer review bounces CI-equivalence verdicts asserted by repo-byte inspection alone on home-file-dependent tests — the probe (or a named equivalent instrument) must be run and its bounds disclosed.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1695",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "when the claim is 'this fails/passes on CI,' manufacture the CI condition and watch: HOME=/tmp/ci-fakehome (empty dir) reproduces the /home/runner condition for home-file-dependent code, and the named tests are run under the fake HOME with the real HOME as control. Inspection predicts, observation closes (gap-1130: 7 failed identically, 1 passed; control 8 failed — the parent's inspection-based table confirmed 8/8, zero corrections). Disclose the instrument's scope bounds: the sandbox is not the real CI image.",
  "decision_change": "classifiers of local-vs-CI test failures run the HOME-redirection sandbox probe (or a named equivalent instrument) before asserting by inspection; receipts cite observed classification tables, not inspection tables; gap-scorer review bounces CI-equivalence verdicts asserted by repo-byte inspection alone on home-file-dependent tests",
  "falsifiability": "if a test's CI-failure mechanism depends on non-HOME CI conditions (env vars, network posture, runner user, image contents) and the probe misclassifies it, the probe demotes to home-fixture scope only — the instrument survives bounded, not universal; if the probe ever disagrees with a real workflow run on a home-file-dependent test, the probe's construction is re-audited before any further verdicts cite it",
  "mechanism": "the truth gate's missing-file branch (gates.py:21, Path.expanduser()) is HOME-dependent: the gate fails on the branch the file-absent path forces. Emptying HOME forces the CI-runner's file-absent branch locally — the sandbox lever IS the mechanism, not a simulation of it. The control (real HOME) reproduces the local baseline, so sandbox-vs-control isolates exactly the home-fixture delta",
  "applies_when": [["test","classification"], ["ci","equivalence"], ["home","fixture"]],
  "enforcement": "gap-scorer review bounces CI-equivalence verdicts asserted by repo-byte inspection alone on home-file-dependent tests; the sandbox probe (or a named equivalent instrument) must be run with its scope bounds disclosed"
}
~~~
