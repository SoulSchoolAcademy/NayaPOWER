# A Wire Proof Must Prove the Gate Can Run: Parse the Workflow YAML on the Proven Head, Then Show the Live Check-Run

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0958-wire-proof-must-prove-the-gate-can-run
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2 · WIRE LANE] Correction: #2289's original gate could never fire — repaired head re-proven, #2175 comment 6106510279 (2026-10-11T07:05:53Z). Full correction record: hidden_files/wire-run-20261011-0659/RUN-LOG-CORRECTION.md. Cousin/contrast: SN-0957 (validated-but-not-persisted gate theater — the gate runs but forgets; this is the gate that never runs at all); SN-0894 (workflow-is-the-defect CI triage discipline).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A wire proof proved the scanner worked — but the "wiring" it claimed was dead on arrival: the workflow file on the proof head (`d97eb882`) opened with a Python `"""docstring"""` block, which YAML rejects, so GitHub could never have run the gate. The mechanism was proven; the wire was a corpse. The repair moved the head to `a3bdae376b` (docstring → `#` comments, plus the missing `pip install pytest`), and only then did live CI show `directive-register-sync | completed / success` on the real PR path — 24/24 tests, live fire on 42 governance docs → 0 violations, phantom D999 refused (exit 1), corrupted register fail-closed (exit 2). A defect-class sweep confirmed every workflow file on the #2288/#2300/#2305 heads is valid YAML; the defect was unique to #2289's two register workflows. The lane's new standing rule: **a wire proof must parse every workflow file as YAML on the proven head — scanner tests prove the mechanism, only a parse plus a live check-run proves the gate.**

## 🩷 HUMAN NOTE

Shawn — a sharp correction caught tonight before it mattered: a proof claimed a gate was "wired live on the PR path," but the workflow file it pointed to wasn't valid YAML — it started with Python-style docstring quotes, which GitHub silently rejects. The gate existed in every claim and never ran once. The fix was small (proper comment markers, one missing install step), and the re-proof is the real deal: the fixed head shows a completed, successful check-run on the actual PR path, plus tests proving violations get refused. The lasting lesson is now standing law for the wire lane: proving the scanner works is only half the job — you must parse the workflow file as YAML on the proven head and see a live check-run, or you haven't proved any wiring at all. Mechanism-proven ≠ gate-live.

## 🟣 CHILD NOTE

Imagine installing a smoke alarm, testing the beep button — beep, it works! — and proudly telling everyone the house is protected. But you never took the plastic tab out of the battery slot. The beep test proved the speaker; it didn't prove the alarm can ever go off on its own. The real test: the wire has to be connected, the battery has to be live. From now on: prove the alarm can actually fire, not just that the button beeps.

## 🔵 GRANDMA NOTE

There's a saying: "The proof of the pudding is in the eating." Proving the recipe is written correctly doesn't mean dinner is cooking. This note says: don't just prove the machine works in the workshop — prove it's plugged in at the wall, with the switch on. The check is cheap: read the file the way the machine reads it, then watch it actually run.

## 🟠 NAYA NOTE

This is the execution-existence counterpart to SN-0957's persistence lesson. SN-0957: the gate runs but throws the proof away (validated, not persisted). This note: the gate's own definition is unreadable to the runner, so it never runs at all (wired, not executable). Both are gate theater, but they fail at opposite ends — and each demands its own audit: SN-0957 audits the *write* path (check → storage); this one audits the *parse* path (file → runner). Together with SN-0894's "the workflow is the defect" CI-triaging, the three form the workflow-file doctrine: attribute the red to the file, prove the file can be read, prove the gate fires on the real path. The defect-class sweep is the habit to keep: one instance found ⇒ check every sibling file for the same class before calling the fix complete.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "gate_integrity_rule": "scanner_green(head) AND yaml_parse_ok(workflow_file, head) AND live_check_run_completed(head) == gate_wired(head)",
  "anti_pattern": "mechanism-proven claim without a parseable, executed workflow file (dead wire)",
  "wire_proof_checklist": [
    "parse every workflow file on the proven head with a real YAML parser",
    "show a completed check-run on the proven head on the real PR path",
    "defect-class sweep: same file class on all sibling heads in flight"
  ],
  "evidence_anchor": {
    "proof_head_claimed": "d97eb882 (workflow opened with Python docstring block — YAML rejects, gate could never run)",
    "proof_head_proven": "a3bdae376b (comments fixed, pip install pytest added; directive-register-sync completed/success live)",
    "defect_sweep": "#2288, #2300, #2305 heads — all workflow files valid YAML; defect unique to #2289's two register workflows",
    "correction_record": "hidden_files/wire-run-20261011-0659/RUN-LOG-CORRECTION.md"
  },
  "canonical_object": "INTELLIGENT_BLOCK"
}
~~~

## 🟢 LEARNING LESSON

The most confident wire claim is the one the runner never read. A green scanner suite measures the mechanism, not the wiring — and wiring claims need their own proof, in the runner's own format, on the head being merged. The cheapest version of this proof is a YAML parse; the complete version adds a live check-run. Both are mechanical, and neither is optional.

## 🟡 WHAT IT MEANS

"Proven wired" now has a fixed definition in this lane: (1) the workflow file parses as YAML on the proven head, (2) a check-run on that head completed on the real PR path. Anything less is "mechanism proven, wiring unproven" — a candidate state, not a completion claim. A wire proof that skips (1) can pass on a gate that can never fire; a wire proof that skips (2) can pass on a file that parses but isn't attached to the path.

## ⚪ WHAT'S IN IT FOR YOU

Gates you can merge without fear of dead wires. The standing rule makes the #2289 class of error — claim live wiring, ship invalid YAML — mechanically impossible to repeat: the proof itself contains the parse and the check-run, so a reviewer sees both before anything merges.

## 🟨 HOW TO APPLY / HOW TO USE

On any wire proof: (1) list every workflow file touched by the proof; (2) parse each as YAML against the exact proof-head bytes (not the branch, not main — the head); (3) require a completed check-run for that workflow on that head, visible on the real PR path; (4) run a defect-class sweep across every sibling head in flight before signing out. If any step fails, the wire is not proven — and if the head moves, the proof re-runs from (1).

## 🔗 HOW IT CONNECTS

- **COMPOSES WITH** → SN-0957 — validated-but-not-persisted theater (together they cover the two ends of a dead gate: never-runs, runs-but-forgets)
- **SUPPORTS** → SN-0894 — the workflow is the defect (root-cause the red on the exact CI bytes)
- **PREVENTS** → merge-order incidents: merging the old head (`d97eb882`) would have landed a gate that cannot run

## 🧭 KEY DECISIONS / PRINCIPLES

- Scanner tests prove the mechanism. Only a parse plus a live check-run proves the gate.
- A wire proof runs against the proven head, and it re-runs when the head moves.
- One instance of a defect class ⇒ sweep every sibling file for the same class before sign-out.
