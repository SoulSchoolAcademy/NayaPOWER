import json
import subprocess
import sys
from pathlib import Path

from tools.measure_node_influence import ORDER, influence_report, measure_behavior_engine

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "tools" / "measure_node_influence.py"


def run_measurement():
    raw = subprocess.check_output(
        [sys.executable, str(PROBE), "--json"],
        cwd=ROOT,
        encoding="utf-8",
        timeout=180,
    )
    return json.loads(raw)


def test_measurement_is_deterministic_and_all_nine_nodes_influence_observable_behavior():
    first = run_measurement()
    second = run_measurement()

    assert first["report"] == second["report"]

    stats = first["report"]["BRAIN.Engineering.kernel_behavior_engine.KernelBehaviorEngine"]
    assert stats["invoked_count"] == 9
    assert stats["influence_demonstrated_count"] == 9
    assert stats["influence_demonstrated_for"] == sorted(ORDER)
    assert set(stats["changed_scenarios"]) == {
        "no_identity",
        "no_authority",
        "authority_revoked",
        "action_type_missing",
        "no_evidence",
        "evidence_without_provenance",
        "no_observation",
        "no_independent_evidence",
        "outcome_mismatch",
        "holdout_failed",
        "know_without_reader",
        "connect_without_relationships",
        "evolve_without_next_action",
    }


def test_each_node_has_a_real_control_treatment_fingerprint_delta():
    measurement = measure_behavior_engine()
    report = influence_report([measurement])
    stats = report["BRAIN.Engineering.kernel_behavior_engine.KernelBehaviorEngine"]

    for node in ORDER:
        scenarios = measurement["scenarios"]
        scenario_name = next(
            name for name, (target, _ctx) in measurement["ablations"].items()
            if target == node
        )
        assert (
            scenarios["full_cycle"]["node_behavior_fingerprints"][node]
            != scenarios[scenario_name]["node_behavior_fingerprints"][node]
        ), node

    assert stats["influence_demonstrated_count"] == 9


def test_deliberate_falsifier_drops_the_claim_to_red():
    measurement = measure_behavior_engine()
    scenario_name = next(
        name
        for name, (target, _ctx) in measurement["ablations"].items()
        if target == "CONNECT"
    )
    baseline = measurement["scenarios"]["full_cycle"]["node_behavior_fingerprints"]["CONNECT"]
    measurement["scenarios"][scenario_name]["node_behavior_fingerprints"]["CONNECT"] = baseline

    report = influence_report([measurement])
    stats = report["BRAIN.Engineering.kernel_behavior_engine.KernelBehaviorEngine"]
    assert stats["influence_demonstrated_count"] == 8
    assert "CONNECT" not in stats["influence_demonstrated_for"]
