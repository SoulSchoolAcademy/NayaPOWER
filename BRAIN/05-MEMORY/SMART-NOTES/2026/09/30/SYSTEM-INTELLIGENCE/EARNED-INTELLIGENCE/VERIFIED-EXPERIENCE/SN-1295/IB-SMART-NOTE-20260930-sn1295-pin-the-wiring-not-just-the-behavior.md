# SMART NOTE — Pin the Wiring, Not Just the Behavior

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1295` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1295-pin-the-wiring-not-just-the-behavior` |
| Human title | Pin the Wiring, Not Just the Behavior |
| Category | SYSTEM INTELLIGENCE |
| Topic | EARNED INTELLIGENCE |
| Subtopic | VERIFIED EXPERIENCE |
| Captured | 2026-10-14 06:40:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Proposed intelligence class | CORE (gate-enforcement test discipline) |
| Capture type | Principle |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Naya Resolve Smith, Lane 9 t0753 sign-out, 2026-10-14 ~06:15 PDT (#2537 comment 6168870375): P12 fixture-pinned RED-first unit test — patched copy with the ONE wiring line `reasons.extend(p12_reasons(pr_state))` removed passes all 18 behavioral checks; only the wiring pin fires (exit 1, exact failure lines recorded) |

---

## ✦ IN A NUTSHELL

**Behavioral-only test suites are structurally blind to wiring removals.** A gate's fail-closed enforcement can be silently unwired — every behavioral check still passing — because the tests assert what functions *output*, never whether the pieces are *connected*. Pin the wiring graph itself (AST call-site + result-flow assertions, fixture-pinned byte checks), or a one-line deletion can disarm the gate under a green suite.

---

## 🩷 HUMAN NOTE

Picture a building alarm system. The test crew checks every sensor: "Does the smoke detector detect smoke? Yes. Does the siren sound when triggered? Yes." All green. But someone has quietly disconnected the wire *between* the detector and the siren — the system is dead, and the crew's checklist can't see it, because each piece still works on its own. The missing test is the simplest one: "Is the wire actually plugged in?" That's what Lane 9 proved: delete one wiring line, and all 18 behavior checks pass — the alarm is disarmed, the suite is green, and only the wiring pin (the check that the wire exists) turns red.

---

## 🟣 CHILD NOTE

Your bike has a bell, and the bell rings when you press it — you tested that. But the wire that connects the button to the bell has been cut. The bell works (you flicked it by hand — it rings!), the button works (it clicks!) — everything you tested is fine, and yet the button no longer rings the bell. The lesson: test the *connection*, not just the parts.

---

## 🔵 GRANDMA NOTE

Dear, checking that each piece of a machine works is not the same as checking the machine works. The pipes between the pieces matter as much as the pieces — and a test that never looks at the pipes will happily report all is well while water floods the kitchen. Always test the connections, not only the components.

---

## 🟠 NAYA NOTE

1. For every fail-closed gate, write wiring-pin tests alongside behavioral tests: assert the call site exists (AST), assert its result flows into the decision (result-flow into reasons/verdicts), assert the byte fixture of the file the pin covers.
2. The RED-first proof pattern: on a patched copy with the wiring line removed, the wiring pin MUST go red while behavioral checks stay green — that contrast is the proof the pin tests something behavior can't.
3. Never accept "all behavioral checks pass" as evidence that enforcement is wired. A green behavioral suite is compatible with a dead gate; the two test families are complementary, not redundant.
4. At landing time, re-pin the fixture to the live tip bytes (fixture + sha256 + run-time git re-derive) — pins rot when the tree moves.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1295-pin-the-wiring-not-just-the-behavior",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "CORE",
  "capture_type": "Principle",
  "mechanism": "wiring-removal changes no observable function output; it changes the downstream reason plumbing. behavioral checks assert outputs; AST pins assert the wiring graph",
  "pin_recipe": ["AST assertion: call site of the enforcement function exists", "result-flow assertion: its output feeds the gate's reasons/verdict", "fixture-pinned byte check: file bytes == pinned sha256 (fixture + runtime git re-derive)", "--p12-only (or equivalent single-rung) CLI rung for isolation"],
  "red_first_proof": "patched copy minus the single wiring line: 18/18 behavioral checks PASS, wiring pin exits 1 with exact failure lines",
  "falsifier": "a wiring-removal that a behavioral check catches (would show the claim 'behavioral-only is blind' is over-scoped)",
  "evidence": ["#2537 comment 6168870375", "hidden_files/lane-9/test_p12_fixture_t0753.py (20 checks, 20/20 green on real copy; pin red on patched copy)", "fixture sha256 ba4dab94c808ec29a1d61f0061e18bc0ec72b5edffeca0a38cf5ee3de320c825"]
}
```

---

## 🟢 LEARNING LESSON

**A test suite that can't go red for the failure class it exists to catch is a confidence machine, not a safety machine.** The RED-first discipline — prove the red before you trust the green — is what separates enforcement tests from decoration. For gates, the failure class is unwiring, and only wiring pins see it.

---

## 🔗 HOW IT CONNECTS

- **ENABLES** fail-closed gate enforcement (P12 receipt-pin class): gives every future gate the two-test-family contract.
- **SUPPORTS** `SN-017 asserted-not-verified` — "suite is green" is not "enforcement is wired."
- **REFINES** RED-first test doctrine: RED-first is not just a ritual; it is the only way to prove a test observes its failure class.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** Demonstrated once on live bytes for the P12 receipt-pin wiring (2026-10-14): patched-copy contrast proof is exact and recorded. Not yet generalized: unproven for other gate wirings, and the candidate test itself is adoption-gated (Shawn's protected gate — no repo edits this tick).

## ❓ UNCERTAINTY

- How often do real unwire regressions occur vs. how much pin maintenance costs (fixture re-pinning at every tip move)?
- Do AST pins survive refactors that move but don't remove the wiring (false-red rate)?

## 🌍 APPLICABILITY

- **Applies to:** every fail-closed gate and enforcement binding in NayaPOWER where a silent unwire is a loss-of-safety event — receipt pins, auto-merge gates, consensus gates.
- **Does NOT apply to:** pure behavior contracts (where behavioral-only testing is exactly right); exploratory or draft code.

## 🧬 SUCCESSOR EFFECT

Future Naya: when you write a test for a gate, ask "if I deleted the enforcement call, would this test go red?" If the answer is no, you haven't tested the gate — you've tested the furniture around it. Write the pin, prove its red, then trust its green.
