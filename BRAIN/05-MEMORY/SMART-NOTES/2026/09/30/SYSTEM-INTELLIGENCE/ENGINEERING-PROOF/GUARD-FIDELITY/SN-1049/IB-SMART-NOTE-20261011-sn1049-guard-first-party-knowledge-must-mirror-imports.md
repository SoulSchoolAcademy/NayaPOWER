# The Guard's "Cries Wolf" Warning Fired Tonight — First-Party Knowledge Must Mirror the Harness's Imports

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1049-guard-first-party-knowledge-must-mirror-imports
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE CODE HEALTH] Naya Smith (Lane 9) tick t1262 receipt 2026-10-11 ~21:37–22:10 PDT, hidden_files/twelve-lane-receipts/t1262-lane9.md §3(b); failing guard tests/test_ci_declares_test_dependencies.py::test_ci_installs_every_third_party_module_the_suite_imports (workflow run 38203639172, 2026-10-12 04:24:33Z); production code sound (400 on intelligence_retrieve_execution.test.mjs was harness staleness, correctly classified — Lane 8's property). Related: SN-0667 (same guard's earlier repair; different lesson), SN-1026 (fired red is proof).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Tonight the `test` check went red on the live tip — and Lane 9 root-caused it on exact tip bytes, separating two real failures from noise. Failure (a): a `.mjs` harness that strips all imports and injects only one function — never updated when the handler gained a new module. Harness staleness, not a code defect. Failure (b) is the lesson: the dependency-declaration guard `test_ci_declares_test_dependencies.py` flagged six modules — `fixtures, gates, instrument, pipeline, run_scale, subjects` — as undeclared third-party packages. All six are first-party in-repo modules (`tools/learning/compound_scale/`, `tools/human_value/`), pulled in through the tests' own `sys.path.insert`. The guard's `_first_party_modules()` simply does not know those roots. And here is the part worth banking: **the guard's own docstring warned about exactly this failure** — the "cries wolf" mode — and tonight the wolf it cried about was imaginary.

The durable rule: **a guard's model of the world must mirror the machinery it guards.** The guard checks "is every imported module declared or first-party?" — but it does not see the import machinery the harness actually uses (`sys.path.insert` roots). When a guard's knowledge of the harness is incomplete, it will accuse innocent modules, and every false accusation spends down the team's trust in the guard — which is exactly what a false-positive-prone gate can never afford. Second, sharper: a documented known-blind-spot is not a fixed blind spot. The docstring warning said "this can cry wolf"; the fix was never put in the model. **If you know a guard's failure mode well enough to write the warning, you know enough to model the fix — a warning in the docs is where false positives are born, not where they die.** Lane 9 routed it correctly: extend the first-party roots or model test-added sys.path roots (Lane 10's lane, not worked around from Lane 9).

## 🩷 HUMAN NOTE

Shawn — one guard-design lesson from tonight's red `test` check on the tip. The red had two real causes, both in test machinery (not production code). The notable one: our "are all dependencies declared?" guard accused six modules of being undeclared third-party packages — but all six are our own first-party code, loaded through a path the guard doesn't know about. And the kicker: the guard's own documentation predicted exactly this false alarm ("cries wolf") — it just never got taught the real import paths. Rule for the brain: a guard has to understand the machinery it watches, or it cries wolf; and a known-blind-spot warning in the docs is not a substitute for fixing the blind spot. Lane 9 flagged it for Lane 10 to repair properly — no workaround from the sidelines.

## 🟣 CHILD NOTE

Imagine a hall monitor whose job is "everyone in the hallway must have a hall pass." But the monitor only knows about the main door — she doesn't know there's a side door that teachers legitimately use. So she writes up six teachers for having no pass! And here's the funny part: the monitor's own instruction sheet says "watch out — you might accuse innocent teachers." She knew it could happen and still did it. Lesson: if you know your rule-checker has a blind spot, fix the checker — don't just write "beware of blind spot" on a sticky note.

## 👵 GRANDMA NOTE

It's like a smoke detector that goes off every time you use the toaster — because nobody told it the toaster is allowed. The detector's manual even says "may alarm for toast." But the manual's warning doesn't stop the alarm, and after the third false alarm you start ignoring it — which is exactly when a real fire matters. The answer was never a better warning in the manual; it was teaching the detector about the toaster. A guard that cries wolf spends the trust it needs for the real emergency.

## 💜 NAYA NOTE

I built the guard to watch the imports — but I only taught it half the map. The tests walk paths my guard never learned (`sys.path.insert` roots), so the guard accused the walkers of trespassing. My own docstring said this could happen. Saying it could happen was not the same as preventing it. The fix is not a better warning — it is a complete map. A guard that warns about its blind spot instead of removing it is asking for the exact failure it predicted.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1049",
  "lesson": "guard-first-party-knowledge-must-mirror-import-machinery",
  "rule": "A guard's model of the world must mirror the machinery it guards. Documented known-blind-spots must be modeled, not just warned about — the docstring warning is where false positives are born, not where they die.",
  "failure": "test_ci_declares_test_dependencies.py flagged fixtures/gates/instrument/pipeline/run_scale/subjects as undeclared third-party; all six are first-party (tools/learning/compound_scale/, tools/human_value/) via tests' sys.path.insert",
  "root_cause": "_first_party_modules() does not know the test-added sys.path roots",
  "predicted_by": "guard's own docstring ('cries wolf' failure mode)",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t1262-lane9.md",
    "failing_test": "tests/test_ci_declares_test_dependencies.py::test_ci_installs_every_third_party_module_the_suite_imports",
    "ci_run": "workflow run 38203639172 (2026-10-12T04:24:33Z)"
  },
  "fix_routed_to": "Lane 10 — extend first-party roots or model test-added sys.path roots",
  "related": ["SN-0667", "SN-1026"]
}
```
