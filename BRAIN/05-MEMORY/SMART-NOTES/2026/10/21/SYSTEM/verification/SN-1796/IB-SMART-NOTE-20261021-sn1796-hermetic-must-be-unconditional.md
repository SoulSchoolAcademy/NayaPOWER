Intelligent Block: SN-1796
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
An environment-conditional "hermetic when absent" fixture branch is a lie CI can never catch — delete the branch, make hermeticity unconditional, and prove it with a poisoned-HOME adversarial probe.

## 🩷 HUMAN NOTE
A truth-receipt fixture had a shortcut: when it could not find the real home directory, it pretended everything was hermetic. But CI always had a home directory, so the shortcut never fired there — and the real-HOME reads sailed through CI green while breaking local and off-VM runs. The root fix was not to debug the shortcut but to delete it: the fixture now ALWAYS materializes the hermetic receipt from the registry's registered quotes into a fixture-injected home, never reading the real home directory. Proof: 51/51 green on this VM plus a poisoned-HOME adversarial probe green; gates.py and the registry untouched. The rule going forward: never write "hermetic if environment X is missing" — unconditional hermeticity, and an adversarial probe that would fail loudly if any real-environment read crept back in.

## 🟣 CHILD NOTE
Imagine a guard who only checks your bag when he is standing at the front door. Sneak in the back and nobody checks. The old test was like that: it only made things safe when a certain folder was missing. The smart fix: the guard checks EVERYONE, at every door, every time — no shortcuts. And then we send a sneaky tester with a fake name tag (the poisoned home) to make sure the guard really does check.

## 🔵 GRANDMA NOTE
Sometimes our safety tests take a shortcut: "if we can't find the house keys, we'll just pretend the door is locked." That is not safety — that is a story we tell ourselves. Real safety means locking the door every single time, and then shaking the handle on purpose to prove it stays shut. The new rule for our test-helpers: no shortcuts, and shake the handle on purpose every time.

## 🟠 NAYA NOTE
Lane-executor / verification-facing. When a truth-receipt or hermetic fixture shows green-in-CI / red-local (or red only off-VM), the FIRST suspect is an environment-conditional hermetic branch in the fixture — a leg that exists precisely to keep CI green while diverging off-CI. The repair pattern (t1178 root fix, Lane 2): delete the conditional branch; always materialize the hermetic receipt from registered quotes into a fixture-injected home; leave the gates and the registry untouched. Before: CI-green/local-red. After: 51/51 green on this VM + poisoned-HOME adversarial probe green. Related follow-up: t1209-lane2 applied the same class of fix as a hermetic RE-POINT (`{REPO}/` token resolving against the package dir), killing the citation-rot class outright. Also noted for the learning-lane owner: ALL L-lesson quotes have rotted on this VM and the suite never truth-tests them — the hermetic re-point or drop decision is still owed.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1796",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "An environment-conditional 'hermetic when absent' fixture branch is unverifiable: the off-CI leg never executes in CI, so real-environment reads diverge invisibly and only break local/off-VM runs. Delete the branch; materialize the hermetic fixture unconditionally from registered quotes into a fixture-injected home; prove it with a poisoned-HOME adversarial probe.",
  "applies_when": [["fixture","hermetic"],["receipt","truth-gate"],["test","environment-divergence"],["ci","green-local-red"]],
  "enforcement": "Truth-gate / hermetic-fixture acceptance is two-legged and mechanical: (1) the suite's adversarial leg runs every truth fixture under a poisoned HOME (no valid home directory on this VM) — any real-HOME read fails the suite; (2) review rule — any fixture carrying an env-conditional hermetic branch is rejected in review until the branch is deleted. 'Tested green in CI' is never accepted as proof of hermeticity.",
  "evidence": {
    "lesson_broadcast": "hidden_files/lesson-broadcast.md [night-dispatcher t1190, 2026-10-21T19:53Z] mirror of receipt t1178-lane2 — root fix was deleting the environment-conditional branch",
    "receipt_t1178": "CI-green/local-red truth-gate defect; after branch deletion 51/51 green on this VM + poisoned-HOME adversarial probe green; gates.py and the registry untouched",
    "receipt_t1209": "t1209-lane2 (Lane 2, hermetic re-point of truth receipts, 9.5/10, board #2793 comment 6332061039) — same class, same fix shape; named owed decision: ALL L-lesson quotes rotted on this VM, suite never truth-tests them"
  },
  "cousins": ["SN-1185","SN-1597"],
  "falsifier": "A fixture whose env-conditional hermetic branch is executed in ALL environments via a leg-covering environment matrix with environment assertions would falsify the generality of this claim.",
  "decision_change": "Future fixture authors delete conditional hermetic branches instead of debugging the divergence they cause; reviewers reject such branches on sight; acceptance always includes the hostile-environment (poisoned-HOME) probe."
}
```
