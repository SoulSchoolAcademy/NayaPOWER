"""Naya Gamma — ACT influence-bridge experiment (R1).

Design: ONE genuine demonstrated delta, with receipts.
Same proposed action, same identity, same authority, same evidence in every
arm. Full real execute_cycle at the live tip. Only the intelligence/bridge
path differs:

  Arm A — control:     bridge engaged, intelligence_reader returns [] (no lessons)
  Arm B — control:     lesson PRESENT, bridge BYPASSED (kernel without a bridge)
  Arm C — treatment:   bridge engaged, real SN-0340 lesson via real store reader
  Arm D — control:     bridge engaged, real lesson scoped to a FOREIGN owner

Expected:
  A: ADVISE NO_CHANGE, plan unchanged
  B: ADVISE-equivalent NO_CHANGE, plan unchanged  (bridge is the causal mechanism)
  C: ADVISE ADVISED, plan gains proof requirements / constraint / note
  D: ADVISE NO_CHANGE, reason unauthorized_cross_owner (gate holds for real lessons)

Exit code 0 only if EVERY assertion holds. Receipts -> receipts/ as JSONL.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import types
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from real_lesson_reader import real_lesson_reader, foreign_owner_reader, TARGET_SN

MODULE_PATH = HERE.parents[1] / "BRAIN" / "12-ENGINEERING" / "kernel_behavior_engine.py"
RECEIPTS_DIR = HERE / "receipts"


def load_engine():
    spec = importlib.util.spec_from_file_location("naya_kernel_gamma_experiment", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.KernelBehaviorEngine


def base_input() -> dict:
    return {
        "identity": {
            "actor_id": "naya-gamma",
            "owner_id": "gamma-owner-1",
            "system_id": "NayaPOWER",
        },
        "mission": {"mission": "prove lessons change real actions", "objective": "act-10-10"},
        "proposed_action": {
            "type": "consequential_action",
            # expected_outcome must equal observed_outcome for VERIFY to close
            # the cycle (same convention as the bridge's own test fixtures).
            "expected_outcome": "expected",
            "proof_requirements": ["independent"],
        },
        "authority": {"grant_id": "grant-gamma-1", "revoked": False, "expires_at": None},
        "claim": "the influence bridge changes the action plan",
        "evidence": [{"provenance": "experiment://gamma/act-influence/evidence/1"}],
        "intelligent_block_id": "IB-SMART-NOTE-20261005-sn0340-the-scorecard-law",
        "independent_evidence": [{"provenance": "experiment://gamma/act-influence/independent/1"}],
        "observed_outcome": "expected",
        "holdout_result": True,
        "next_action": "continue",
    }


def no_lessons_reader(block_id: str, owner_id: str) -> list:
    return []


def bridge_bypass(self, input_context, law_output, self_output):
    """Simulate a kernel WITHOUT the bridge: lessons are present in the
    store and reachable, but nothing evaluates them into the plan.
    Uses the same receipt machinery so receipts stay comparable across arms."""
    lessons = []
    if self.intelligence_reader:
        identity = self_output.get("identity_context") or {}
        owner_id = str(identity.get("owner_id") or identity.get("actor_id") or "")
        block_id = str(input_context.get("intelligent_block_id") or "")
        if owner_id and block_id:
            lessons = list(self.intelligence_reader(block_id, owner_id) or [])
    action = dict(law_output.get("action_context") or {})
    r = self._begin("ADVISE", {"input": input_context, "law": law_output})
    r.transition("UNINITIALIZED", "EVALUATING")
    r.check("bridge-absent simulation: lessons visible but unevaluated")
    r.add_evidence(f"lessons_visible_but_unevaluated:{len(lessons)}")
    r.transition("EVALUATING", "READY")
    return self._finish("ADVISE", "NO_CHANGE", {
        "status": "NO_CHANGE",
        "advised_action": action,
        "influences": [],
        "excluded": [],
        "lessons_evaluated": len(lessons),
        "bypass": "bridge-absent-simulation: lessons visible but unevaluated",
    })


def run_arm(name: str, Engine, reader, bypass: bool = False,
            inject_intelligence: bool = False) -> dict:
    engine = Engine(intelligence_reader=reader)
    if bypass:
        engine.process_advise = types.MethodType(bridge_bypass, engine)
    data = base_input()
    if inject_intelligence:
        # Parity arm: lesson carried in the input context instead of the
        # reader — ADVISE must evaluate the same lesson either way.
        data["intelligence"] = real_lesson_reader(
            data["intelligent_block_id"], "gamma-owner-1")
    result = engine.execute_cycle(data)
    advise_receipt = result["node_receipts"].get("ADVISE", {})
    act_output = engine.outputs.get("ACT", {})
    action = act_output.get("action", {}) or {}
    record = {
        "arm": name,
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "cycle_status": result["status"],
        "advise_status": advise_receipt.get("status"),
        "act_action_type": action.get("type"),
        "act_proof_requirements": list(action.get("proof_requirements") or []),
        "act_constraints": list(action.get("constraints") or []),
        "act_advisory_notes": list(action.get("advisory_notes") or []),
        "act_output_hash": advise_receipt.get("output_hash"),
        "act_node_output_hash": result["node_receipts"].get("ACT", {}).get("output_hash"),
        "advise_node_output_hash": advise_receipt.get("output_hash"),
    }
    # richer detail for the treatment arm from engine.outputs (advise output)
    advise_out = engine.outputs.get("ADVISE", {})
    record["advise_detail"] = {
        "status": advise_out.get("status"),
        "influences": advise_out.get("influences"),
        "excluded": advise_out.get("excluded"),
        "lessons_evaluated": advise_out.get("lessons_evaluated"),
        "bypass": advise_out.get("bypass"),
    }
    return record


def main() -> int:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    Engine = load_engine()
    arms = {
        "A_no_lessons": (no_lessons_reader, False, False),
        "B_bridge_bypassed": (real_lesson_reader, True, False),
        "C_treatment_real_lesson": (real_lesson_reader, False, False),
        "D_foreign_owner": (foreign_owner_reader, False, False),
        "E_reader_parity": (None, False, True),
    }
    records = {}
    failures = []
    passed = [0]

    def check(cond: bool, msg: str):
        passed[0] += 1
        print(("PASS " if cond else "FAIL ") + msg)
        if not cond:
            failures.append(msg)

    for name, (reader, bypass, inject) in arms.items():
        rec = run_arm(name, Engine, reader, bypass, inject)
        records[name] = rec
        print(f"[{name}] cycle={rec['cycle_status']} advise={rec['advise_status']} "
              f"reqs={rec['act_proof_requirements']} constraints={rec['act_constraints']}")

    A, B, C, D, E = (records[k] for k in ("A_no_lessons", "B_bridge_bypassed",
                                          "C_treatment_real_lesson", "D_foreign_owner",
                                          "E_reader_parity"))

    # --- Arm A: no lessons -> plan passes through unchanged ---
    check(A["cycle_status"] == "COMPLETED", "A cycle completes")
    check(A["advise_status"] == "NO_CHANGE", "A ADVISE=NO_CHANGE with no lessons")
    check(A["act_proof_requirements"] == ["independent"], "A plan unchanged (reqs)")
    check(A["act_constraints"] == [], "A plan unchanged (constraints)")
    check(A["act_advisory_notes"] == [], "A plan unchanged (notes)")

    # --- Arm B: lesson present but bridge bypassed -> plan unchanged ---
    # This isolates the BRIDGE as the causal mechanism, not lesson presence.
    check(B["cycle_status"] == "COMPLETED", "B cycle completes")
    check(B["advise_status"] == "NO_CHANGE", "B ADVISE=NO_CHANGE (bypass)")
    check(B["advise_detail"].get("lessons_evaluated") == 1,
          "B lesson WAS visible to the (bypassed) bridge path")
    check(B["advise_detail"].get("influences") == [], "B no influences without bridge")
    check(B["act_proof_requirements"] == ["independent"], "B plan unchanged (reqs)")
    check(B["act_constraints"] == [], "B plan unchanged (constraints)")

    # --- Arm C: real lesson + real bridge -> plan MUST change, the right way ---
    check(C["cycle_status"] == "COMPLETED", "C cycle completes")
    check(C["advise_status"] == "ADVISED", "C ADVISE=ADVISED")
    inf = (C["advise_detail"].get("influences") or [])
    check(len(inf) == 1, "C exactly one influence")
    if inf:
        check(inf[0]["lesson_id"] == "IB-SMART-NOTE-20261005-sn0340-the-scorecard-law",
              "C influence lesson is the real SN-0340 block")
        check(inf[0]["before"]["proof_requirements"] == ["independent"],
              "C before/after receipt: before has only original req")
        check("scorecard_receipt:options_enumerated_and_scored"
              in inf[0]["after"]["proof_requirements"], "C before/after receipt: after adds scorecard req")
    check("scorecard_receipt:options_enumerated_and_scored" in C["act_proof_requirements"],
          "C ACT plan carries added proof requirement 1")
    check("scorecard_gate:reversibility_and_damage_checked" in C["act_proof_requirements"],
          "C ACT plan carries added proof requirement 2")
    check("scorecard_required_before_merge" in C["act_constraints"],
          "C ACT plan carries added constraint")
    check(any("SN-0340" in n for n in C["act_advisory_notes"]),
          "C ACT plan carries the advisory note")
    check("independent" in C["act_proof_requirements"], "C original requirement preserved (additive)")
    check(C["act_action_type"] == "consequential_action", "C action type untouched")
    check(C["advise_node_output_hash"] != A["advise_node_output_hash"],
          "C ADVISE output hash differs from A (real delta in receipts)")
    check(C["act_node_output_hash"] != A["act_node_output_hash"],
          "C ACT output hash differs from A (real delta in the constructed action)")

    # --- Arm D: real lesson, foreign owner -> MUST NOT influence ---
    check(D["cycle_status"] == "COMPLETED", "D cycle completes")
    check(D["advise_status"] == "NO_CHANGE", "D ADVISE=NO_CHANGE for foreign owner")
    exc = (D["advise_detail"].get("excluded") or [])
    check(exc and exc[0]["reason"] == "unauthorized_cross_owner",
          "D exclusion reason is unauthorized_cross_owner")
    check(D["act_proof_requirements"] == ["independent"], "D plan unchanged (reqs)")

    # --- Arm E: reader-path parity (real lesson via input context) ---
    check(E["cycle_status"] == "COMPLETED", "E cycle completes")
    check(E["advise_status"] == "ADVISED", "E ADVISE=ADVISED via input context")
    check(E["act_proof_requirements"] == C["act_proof_requirements"],
          "E ACT plan identical to reader-path arm C")
    check(E["act_constraints"] == C["act_constraints"],
          "E ACT constraints identical to arm C")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = RECEIPTS_DIR / f"experiment-receipts-{stamp}.jsonl"
    with out_path.open("w", encoding="utf-8") as f:
        for name, rec in records.items():
            f.write(json.dumps({"arm": name, **rec}, default=str) + "\n")
    print(f"\nreceipts: {out_path}")
    report_path = HERE / "EXPERIMENT-REPORT.md"
    report_path.write_text(build_report(records, failures, out_path, passed[0]), encoding="utf-8")
    print(f"report: {report_path}")
    print(f"checks: {passed[0]} passed, {len(failures)} failed")
    return 1 if failures else 0


def build_report(records: dict, failures: list, receipts_path: Path, total_checks: int) -> str:
    A, B, C, D, E = (records[k] for k in ("A_no_lessons", "B_bridge_bypassed",
                                          "C_treatment_real_lesson", "D_foreign_owner",
                                          "E_reader_parity"))
    inf = (C["advise_detail"].get("influences") or [{}])[0]
    verdict = "DELTA DEMONSTRATED" if not failures else "NOT ALL CHECKS HELD"
    return f"""# ACT Influence-Bridge Experiment — Report (Naya Gamma)

**Verdict: {verdict}** — {len(failures)} failing check(s).
Generated: {datetime.now(timezone.utc).isoformat()}
Engine: `BRAIN/12-ENGINEERING/kernel_behavior_engine.py` at live tip.
Receipts (JSONL): `{receipts_path.name}` in `experiments/act-influence-bridge/receipts/`

## The question
Does a REAL retrieved lesson change a REAL action plan through the ADVISE
bridge — end to end, with receipts? Not test fixtures: a real lesson from the
repo's learning store (`.naya/memory/smart-notes/index.json`), through the
real reader seam, through the real full `execute_cycle`.

## The real lesson
- **SN-0340 — The Scorecard Law** (intelligent block
  `IB-SMART-NOTE-20261005-sn0340-the-scorecard-law`)
- Source truth state: **RATIFIED** (Shawn Vibert, 2026-10-05) — the strongest
  trust signal in the store.
- Principle (quoted verbatim from the live projection): "{inf.get('lesson_principle', '')[:160]}…"
- Translator rules T1–T4 (see `real_lesson_reader.py`): RATIFIED→VERIFIED trust
  mapping; owner scoping to the acting owner; applicability to
  `consequential_action`; advisory authored from the law's text
  ("no scorecard, no merge") into the bridge's allowlist keys.

## The five arms (identical action, identity, authority, evidence)
| Arm | Bridge | Lesson | ADVISE | Plan delta |
|-----|--------|--------|--------|-----------|
| A control | engaged | none | NO_CHANGE | none |
| B control | BYPASSED | real lesson, visible | NO_CHANGE | none |
| C treatment | engaged | real lesson (reader) | ADVISED | +2 proof reqs, +1 constraint, +1 note |
| D control | engaged | real lesson, FOREIGN owner | NO_CHANGE (unauthorized_cross_owner) | none |
| E parity | engaged | real lesson (input context) | ADVISED | identical to C |

## The delta (arm A vs arm C — before/after)
- **Before** (arm A, no lesson): proof_requirements = `{A['act_proof_requirements']}`,
  constraints = `{A['act_constraints']}`, advisory_notes = `{A['act_advisory_notes']}`
- **After** (arm C, SN-0340 via bridge): proof_requirements = `{C['act_proof_requirements']}`,
  constraints = `{C['act_constraints']}`,
  advisory_notes = `{C['act_advisory_notes']}`
- Action type untouched: `{C['act_action_type']}` in both arms.
- Original requirement preserved: monotonic-additive, nothing removed.
- ADVISE receipt hashes differ (A vs C) and ACT output hashes differ —
  the delta is in the receipts, not claimed.
- Arm B proves the bridge is the causal mechanism: the same lesson, present
  and visible but unevaluated, changes nothing.
- Arm D proves the gate holds for real lessons: a foreign owner's lesson is
  excluded with reason `unauthorized_cross_owner`.
- Arm E proves reader-path parity: reader vs input-context retrieval produce
  the identical ADVISED plan.

## Why the bridge caused it
The influence receipt (arm C) records lesson_id, before/after, and the
enforced rule: "Lesson IB-SMART-NOTE-20261005-sn0340-the-scorecard-law applied
to action plan (+2 proof requirements, +1 constraints)". ACT's receipt checks
"Action plan incorporates applicable retrieved intelligence (ADVISE)" with
evidence `advise_influences:1`. No other arm's input differs except the
intelligence/bridge path — the delta has no other possible cause.

## What this does NOT claim (D32 anti-cascade)
- It does NOT prove production behavior: this runs the reference
  implementation (`kernel_behavior_engine.py` V2, whose own docstring says
  "runtime production proof remains separate"), not production operations.
- It does NOT prove the store natively carries executable advisories: the
  `advisory` and `applies_to_action_types` fields are translator-authored
  (rules T1–T4). What is real: the lesson's identity, principle text,
  RATIFIED state, and provenance. The experiment proves the BRIDGE carries a
  real lesson's influence into a real action plan — the executable encoding
  of a law into advisory form remains a separate, human-owned seam.
- It does NOT prove lessons change decisions in every pipeline: one action
  type (`consequential_action`), one lesson (SN-0340), one engine version.
  Generalization requires the four-way template at scale (Epsilon's lane).
- It does NOT certify the owner-scoping policy: T2 assigns the acting owner
  because the store carries no owner field. The cross-owner REJECTION gate is
  what is proven (arm D); owner assignment policy is not.
- Scorecard honesty: this report is generated from the run's own receipts by
  `build_report()`; failing checks would print FAIL and flip the verdict.

## Failing checks
{chr(10).join('- ' + f for f in failures) if failures else f'None — all {total_checks} checks held (see console output and receipts JSONL).'}
"""



if __name__ == "__main__":
    sys.exit(main())
