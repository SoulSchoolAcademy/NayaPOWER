# SN-0413 — A Fail-Closed Gate Is the Guardrail Working: classify denials as evidence, and hold merges while proof is in flight

- **Intelligent Block:** IB-SMART-NOTE-20261005-sn0413-fail-closed-gate-is-guardrail-working
- **Truth state:** CANDIDATE
- **Scope:** PRIVATE (Team Naya operating code)
- **Captured:** 2026-10-05
- **Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Five live-supabase-runtime-proof failures were fully classified: **four of five were the SHA-gate failing closed because main moved between dispatch and run** — the gate correctly refused to prove a stale SHA, and that is the guardrail working, not a product RED. Classifying a fail-closed denial as a product failure is exactly how teams patch healthy guardrails into submission. The one genuine defect was a **missing `if: workflow_run.conclusion == 'success'` guard** on three downstream jobs, which failed noisily on `download-artifact` instead of skipping cleanly after the triggering commit proof failed — the defect was in the missing guard, not in the product the jobs were proving. And the structural finding: **main moves faster than the ~15min proof window**, so the diagnosis recommends proof windows on #1354 — announce when proof starts, hold merges until it completes — or the team will keep manufacturing SHA-gate fail-closes and then "fixing" the gate.

## HUMAN NOTE
Imagine a security guard who stops a delivery truck because its paperwork doesn't match the building it's delivering to. Four times in one night, trucks showed up with papers for the wrong building (the building had changed), and the guard turned them away every time. That's not the guard failing — that's the guard doing exactly its job. The real question is why trucks kept showing up with wrong paperwork: because the building kept changing faster than the trucks could arrive. Two fixes, and both matter: (1) never punish the guard for turning away a bad delivery — a "fail closed" denial is evidence the system works; (2) announce a delivery window and hold the building still while the truck is coming. The one genuine broken thing that night wasn't the guard — it was three back-office windows that were supposed to quietly close when the front door never opened, but instead set off alarms. Fix the window latch, not the guard.

## CHILD NOTE
If the guard turns away the wrong truck, the guard did a good job — don't get mad at the guard. But if the house keeps moving while the truck is driving, tell everyone to stop moving the house until the truck arrives. And if a window is supposed to stay shut when the door is closed but it keeps banging in the wind, fix the latch — don't blame the wind.

## GRANDMA NOTE
Dear, when the alarm goes off and everything is actually fine, that's the alarm doing its job — you don't rip the alarm off the wall. You write down why it rang and move on. But you do tell the whole family: while the delivery is coming, nobody rearranges the driveway. Announce the delivery, hold everything still, then let it through.

## NAYA NOTE
From the 2026-10-05 runtime proof diagnosis (#1354 comment 6006341422; full write-up `hidden_files/runtime-proof-diagnosis-20261005.md`). Runs 37392578908, 37392326164, 37391254250, 37389410502 all failed at source-integrity from main moving between dispatch and run; run 37391775998 failed at the triggering commit proof, `contract` correctly skipped, but `independent-connect-verification`, `cold-successor`, and `cold-successor-verification` in `live-supabase-runtime-proof.yml` lacked the `if: workflow_run.conclusion == 'success'` guard — the fix belongs to the workflow owner (human-only lane), flagged, not self-repaired. The failure was explicitly ruled out as the cold-graph seam, the parity gap, or the KeyError 'intelligence' stage — none reached those stages. Standing rules: (1) classify every failure as product-RED vs guardrail-correct before touching code — a fail-closed denial with a receipt reason (cf. SN-0357's `protected_change_requires_explicit_promotion`) is evidence the authority boundary works; (2) proof windows are announced on #1354 with merges held until complete — a freeze with scope and end condition, per SN-0204, never an open-ended veto; (3) never "fix" a guardrail that correctly refused stale state.

## MACHINE NOTE
```json
{
  "sn": "SN-0413",
  "doctrine": "a_fail_closed_denial_is_evidence_the_guardrail_works_not_a_product_red",
  "classification_rule": "classify_every_failure_as_product_red_vs_guardrail_correct_before_touching_code",
  "proof_window_protocol": {
    "announce": "proof_start_on_1354",
    "hold": "merges_held_until_proof_complete",
    "constraint": "bounded_freeze_with_scope_and_end_condition_per_SN-0204_never_open_ended"
  },
  "workflow_fix_flagged_not_self_repaired": {
    "file": "live-supabase-runtime-proof.yml",
    "jobs": ["independent-connect-verification", "cold-successor", "cold-successor-verification"],
    "fix": "add if: workflow_run.conclusion == 'success'",
    "owner": "workflow_owner_human_only_lane"
  },
  "excluded_causes": ["cold_graph_seam", "parity_gap", "KeyError_intelligence_stage"],
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6006341422",
    "failing_runs": [37392578908, 37392326164, 37391254250, 37389410502, 37391775998],
    "diagnosis_file": "hidden_files/runtime-proof-diagnosis-20261005.md"
  }
}
```
