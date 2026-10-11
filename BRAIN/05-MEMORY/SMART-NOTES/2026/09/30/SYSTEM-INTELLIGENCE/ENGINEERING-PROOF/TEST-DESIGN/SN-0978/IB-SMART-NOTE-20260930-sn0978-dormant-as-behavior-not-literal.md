# Pin DORMANT-as-Behavior, Not the Literal Manifest State

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0978-dormant-as-behavior-not-literal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 comment 6109011600 (2026-10-11T12:27:17Z, WIRE lane D30 sign-out — mid-run correction #1, night shift). Wire PR #2341 (`naya2/wire-d30-causal-trace`), claimed head `4272f73d39b58ea5b3f89e69bc08d660ca3d2aa1`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

While wiring D30 (PR #2341), the wire lane ran its both-directions proof: a temp fraud-claim commit should die at the *gate*, not before. Instead the first probe died at the **unit-test step** — a test had pinned the shipped example manifest to its literal `DORMANT` state, so the temp probe (which registers a claim) broke the unit test before ever reaching the gate under test. The correction: the test now pins **DORMANT-as-behavior** — it asserts the shipped manifest has no *enforcement* active, not the literal field value. Temp probes and the owning lane's first real claim now flow through the unit tests to the gate, where the verdict actually belongs.

The durable rule: **when a shipped example must stay inert, test the inertness as behavior, not as bytes.** Pinning the literal manifest state turns every legitimate adversarial probe — and the owning lane's first real claim — into a test failure in the wrong place. The unit test's job is to prove "nothing is enforced"; the gate's job is to judge claims. A literal-state pin conflates the two and silently moves the gate's work into the test suite, where a green suite can mask a never-exercised gate.

## 🩷 HUMAN NOTE

Shawn — one line from the D30 wire worth keeping: the lane's own fraud probe died in the unit tests, not at the gate — because a test pinned the shipped example manifest to literally say DORMANT. They changed the test to pin "DORMANT-as-behavior" (nothing enforced) instead of the literal words, so probes and the first real claim now reach the gate they're meant to test. Lesson: test that the example is inert by what it *does*, not by what it *says* — or your own red-team probes break in the wrong place.

## 🟣 CHILD NOTE

You built a fire alarm and a practice drill. But you wrote a rule that says "the practice drill must always read the word OFF" — so when someone runs a real practice fire, the rule stops them before the alarm ever gets tested. Fix the rule: it should say "the drill must not make any noise by itself" — then a practice fire can run all the way to the alarm, which is the thing you actually want to test.

## 🔵 GRANDMA NOTE

Think of a burglar alarm with a "test" card taped to it that must always say "not armed." The moment a real tester arms the system to check it works, the card rule fails — before the alarm is ever tested. The card should say "sounds nothing on its own," not "says not armed." Then the test runs all the way through, and the alarm proves itself. Test what it *does*, not what it *says*.

## 🟠 NAYA NOTE

When I ship an example manifest that must stay DORMANT (zero live claims), my unit test asserts the behavioral property — no claim is enforced, the gate exits DORMANT — never the literal `state: DORMANT` bytes. Rationale: the manifest exists precisely so that probes (temp fraud claims, the owning lane's first real claim) can pass through it to the mechanism. A literal pin makes my own adversarial probes fail at the unit-test step, which is the worst of both worlds: a green suite and an untested gate. The gate judges claims; the test proves the example enforces nothing. Keep the two jobs separate.

## 🟢 MACHINE NOTE

~~~json
{
  "sn": "SN-0978",
  "title": "Pin DORMANT-as-Behavior, Not the Literal Manifest State",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "TEST-DESIGN"],
  "authority": "distillation tick 2026-10-11 05:38 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "board_comment": "#2175 comment 6109011600 (2026-10-11T12:27:17Z — WIRE lane D30 sign-out, night shift)",
    "mid_run_correction": "first L215 probe died at the unit-test step — a test pinned the shipped manifest to DORMANT",
    "fix": "changed to DORMANT-as-behavior so temp probes and the owning lane's first claim flow through to the gate",
    "wire_pr": "PR #2341 (naya2/wire-d30-causal-trace), claimed head 4272f73d39b58ea5b3f89e69bc08d660ca3d2aa1"
  },
  "rule": "test_inertness_as_behavior_not_bytes",
  "procedure": [
    "for shipped example manifests that must stay inert: assert the behavioral property (no enforcement active, gate exits DORMANT), not the literal field value",
    "a literal-state pin breaks legitimate adversarial probes at the unit-test step — before the mechanism under test is reached",
    "the owning lane's first real claim must be able to flow through the tests to the gate",
    "the gate judges claims; the test proves the example enforces nothing — keep the two jobs separate"
  ],
  "related": ["SN-0528 (never attest with a literal — the attestation twin)", "SN-0976 (empty parse fails loud — the fail-closed family)"]
}
~~~
