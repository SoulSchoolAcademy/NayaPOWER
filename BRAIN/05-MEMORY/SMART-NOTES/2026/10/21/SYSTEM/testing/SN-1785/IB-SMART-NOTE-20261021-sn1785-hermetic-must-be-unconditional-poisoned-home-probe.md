# Hermetic Must Be Unconditional — the Poisoned-HOME Probe Is the Acceptance Test

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1785-hermetic-must-be-unconditional-poisoned-home-probe
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1785

## ✦ IN A NUTSHELL

An environment-conditional hermetic branch ("use the real file when available, hermetic only when absent") is a lie the CI can never catch — the CI path was already the hermetic body, so the lie lived exactly where CI is blind. The fix is not to extend the condition but to delete it: the fixture ALWAYS materializes from the registry's registered inputs in a fixture-injected home. The acceptance test is the poisoned-HOME probe, run on the BEFORE run too.

## 🩷 HUMAN NOTE

A twelve-lane seat (Mason, t1178-lane2, 2026-10-21 19:48Z) found a hermetic test fixture with an if-statement: when a real file existed in the home directory, the fixture read the real home; only when it was absent did it use the fake one. On CI, the real file never exists — so CI always ran the clean branch, and the coupling to the live home directory was invisible forever. The seat's fix was not to write a smarter condition. It deleted the condition entirely: the fixture now always builds its world from registered inputs in a fixture-injected home, never touching the real one. Then it proved the fix with a three-environment acceptance run — real HOME, a poisoned fake HOME stuffed with unrelated content, and an empty HOME (the CI analog) — 51 tests green in all three. The key move: the poisoned-HOME probe runs on the BEFORE run too, so a future fixer can prove the coupling existed before the repair, not just that the after-run is clean. Refines CANDIDATE 42 (hermetic receipts must not couple to live home files — the named parent), and echoes t0552's 3-red signature, reproduced first to name the root in bytes before touching code. Test code only: 23 insertions, 30 deletions, gates and registry untouched.

## 🟣 CHILD NOTE

Imagine you bake a cake with a recipe that says "use the store's flour if the shelf is empty, otherwise use whatever is in your backpack." Your backpack flour might be sawdust — but when you bake at the store (where the test kitchen is), the shelf is always stocked, so nobody ever discovers the sawdust rule. The fix isn't a better rule about backpacks. It's: always bake at the store with the store's flour, no backpack allowed. And to prove it, you bake once with someone's backpack full of sawdust sitting right there on the counter — before and after the fix — so everyone can see the cake is safe either way.

## 🔵 GRANDMA NOTE

It's like a scale in your bathroom that shows the right weight only when someone watches, dear. You'd never know it was fibbing when you turned your back — because every time you checked, you were watching. The honest fix isn't a better scale with more rules about when to fib. It's a scale with no fibbing part inside at all. And you test it the clever way: you step on it holding a heavy bag of rice, before and after you fixed it — if the number never changes, you know the scale tells the truth whether anyone is watching or not.

## 🟠 NAYA NOTE

The operating rule, step by step, by name.

**Step 1 — Reproduce the signature first.** Before repairing, reproduce the exact failure signature (t1178 reproduced the t0552 3-red signature: 3 failed, 13 passed, on real HOME) and name the root in bytes (the conditional branch in _truth_lesson), not the symptoms.

**Step 2 — Delete the condition; don't extend it.** An environment-conditional hermetic branch is the bug, not a feature to refine. The fixture ALWAYS materializes from the registry's registered inputs in a fixture-injected home and never reads the real home directory.

**Step 3 — Acceptance is three named environments, before AND after.** Real HOME, poisoned fake HOME (unrelated content), empty HOME (the CI analog). The poisoned-HOME probe runs on the BEFORE run too — proving environment coupling before the repair, not just cleanliness after.

**Step 4 — Keep the blast radius to test code.** Repair in test files only; gates and registry untouched (t1178: tests/test_learn_compound_scale.py, sha256 re-pinned 87f9c70b…88fbe17). If the fix requires touching production code, it wasn't a fixture bug.

**Step 5 — Fold the probe into the seat's Mirror.** The seat's own Mirror (t1178) commits the next-time change: poisoned-HOME probe on the before run, not just the after. The acceptance test becomes a habit, not a one-off.

## 🟢 MACHINE NOTE

```json
{
  "sn_id": "SN-1785",
  "title": "Hermetic must be unconditional; the poisoned-HOME probe is the acceptance test",
  "captured": "2026-10-21",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["testing", "hermetic", "fixture"],
  "enforcement": "Three-environment acceptance run (real HOME, poisoned fake HOME with unrelated content, empty HOME as CI analog) executed on BOTH the before-fix and after-fix runs; the poisoned-HOME probe must show coupling on the before run and cleanliness on the after run. A hermetic fixture repair that skips the before-run probe is incomplete and the repair is not closed.",
  "decision_change": "When writing or repairing a hermetic fixture, never branch on environment availability — always fixture-inject the home; when accepting the repair, run the poisoned-HOME probe on the before run first to prove the coupling existed.",
  "falsifier": "Falsified if an environment-conditional hermetic branch passes the full three-environment suite including the before-run poisoned-HOME probe — then the conditional can be safe and the unconditional rule is overstated.",
  "mechanism": "Observability asymmetry: the CI path already executes the hermetic branch, so a conditional's non-hermetic branch is unobservable to CI — the lie lives exactly where CI is blind. Deleting the condition removes the unobservable branch; the before-run probe makes the coupling observable on purpose.",
  "evidence": "hidden_files/twelve-lane-receipts/t1178-lane2.md (Mason, 2026-10-21 19:48Z): reproduced t0552 3-red signature (3 failed, 13 passed, real HOME), deleted the conditional branch in _truth_lesson (tests/test_learn_compound_scale.py, 23+/30-, test code only, gates.py + registry untouched), 51 passed exit 0 in all three environments. Dispatcher t1190 (19:53Z) mirror independently converges. Refines CANDIDATE 42 (named parent); cousins: CANDIDATE 154, Law 1 (fix the root, the seam, not the symptom).",
  "status": "CANDIDATE"
}
```
