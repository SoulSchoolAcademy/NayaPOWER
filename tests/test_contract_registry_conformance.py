from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".naya/runtime/contract_registry_conformance.py"
SPEC = importlib.util.spec_from_file_location("contract_registry_conformance", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
CONFORMANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONFORMANCE)


def audit() -> dict:
    return CONFORMANCE.audit(ROOT)


def findings(report: dict, code: str) -> list:
    return [f for f in report["findings"] if f["code"] == code]


# --- the constitutional truth model must be present and machine-checkable ---------


def test_constitutional_equations_are_all_present():
    report = audit()
    assert findings(report, "CONSTITUTIONAL_EQUATION_MISSING") == []
    assert len(CONFORMANCE.CONSTITUTIONAL_EQUATIONS) == 6


def test_removing_a_constitutional_equation_is_detected(tmp_path):
    law = (ROOT / ".naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md").read_text(
        encoding="utf-8"
    )
    stripped = law.replace(
        "**IMPLEMENTED \u2260 VERIFIED**", "**IMPLEMENTED is basically verified**"
    )
    assert stripped != law, "fixture assumption broken: equation text not found"
    missing = CONFORMANCE.constitutional_equations_missing(stripped)
    assert "IMPLEMENTED \u2260 VERIFIED" in missing


def test_truth_state_vocabulary_drift_is_detected():
    report = audit()
    codes = {f["code"] for f in report["findings"]}
    assert "TRUTH_STATE_VOCABULARY_DRIFT" in codes
    subjects = {f["subject"] for f in findings(report, "TRUTH_STATE_VOCABULARY_DRIFT")}
    assert any("MISSING" in s for s in subjects), subjects


# --- the registry's own claims must be checkable against the repository ----------


def test_every_registry_entry_is_parsed_with_id_and_status():
    report = audit()
    assert report["registry_entries"] >= 27
    assert report["registry_ids_unique"] is True
    assert findings(report, "REGISTRY_STATUS_VOCABULARY") == []


def test_registry_cited_artifact_paths_are_reported_with_existence():
    report = audit()
    drift = findings(report, "CITED_PATH_MISSING")
    # the known phantom migration reference is the evidence this check works
    assert any("20260924110000" in f["subject"] for f in drift), drift
    assert report["cited_paths_checked"] > 0


def test_new_phantom_path_is_always_a_finding():
    phantom = "supabase/migrations/99999999999999_not_a_real_migration_v1.sql"
    assert CONFORMANCE.path_exists(ROOT, phantom) is False
    assert CONFORMANCE.path_exists(ROOT, "supabase/functions/nayanet-smart-mail/index.ts") is True


def test_acceptance_claim_without_enforcement_is_reported():
    report = audit()
    weak = findings(report, "ACCEPTANCE_CLAIM_UNENFORCED")
    assert weak, "registry claims acceptance tests; unrouted/unknown ones must surface"
    for finding in weak:
        assert finding["severity"] in {"ERROR", "WARN"}


def test_enforcement_detection_finds_a_routed_and_an_unrouted_test():
    assert CONFORMANCE.is_routed(ROOT, "tests/int001/test_smart_link_verifier.py") is True
    assert CONFORMANCE.is_routed(ROOT, "tools/test_promote_intelligence.py") is False


def test_unproven_claim_contradicted_by_real_implementation_is_reported():
    report = audit()
    contradictions = findings(report, "UNPROVEN_CLAIM_CONTRADICTED")
    assert any("CC-017" in f["subject"] for f in contradictions), contradictions


# --- ratification boundary --------------------------------------------------------


def test_ratified_claim_requires_a_recorded_ratification_artifact():
    report = audit()
    unproven = findings(report, "RATIFICATION_UNPROVEN")
    assert unproven, "a contract claims RATIFIED; without a human record that must surface"
    for finding in unproven:
        assert "RATIFIED" in finding["detail"]


def test_no_contract_may_self_assert_ratification_without_human_record():
    text = "**Status:** RATIFIED\n"
    assert CONFORMANCE.ratification_record_for(ROOT, ".naya/contracts/00-SOMETHING.md", text) is None


# --- reachability: a cold Naya must be able to find the registry ------------------


def test_registry_reachability_from_canonical_boot_is_reported():
    report = audit()
    reach = findings(report, "REGISTRY_UNREACHABLE_FROM_BOOT")
    assert reach, "registry is not linked from the boot path; a cold Naya cannot reach it"
    assert not (ROOT / ".naya/control-plane/CANONICAL-CONTRACT-REGISTRY.md").is_symlink()


def test_contract_library_index_still_lags_the_tree_is_reported():
    report = audit()
    codes = {f["code"] for f in report["findings"]}
    assert "LIBRARY_INDEX_LAGS_TREE" in codes


# --- the gate itself must be honest ------------------------------------------------


def test_report_declares_known_debt_and_never_claims_conformance():
    report = audit()
    assert report["conforming"] is False
    assert report["known_debt"] > 0
    assert report["new_drift"] >= 0
    assert "generated_from" in report


def test_baseline_suppresses_known_debt_but_not_new_drift(tmp_path):
    report = audit()
    baseline = {f["fingerprint"] for f in report["findings"]}
    assert baseline, "audit produced no fingerprints"
    result = CONFORMANCE.classify(report, baseline)
    assert result["new_drift"] == 0
    assert result["known_debt"] == len(baseline)

    mutated = json.loads(json.dumps(report))
    mutated["findings"].append(
        {
            "code": "CITED_PATH_MISSING",
            "severity": "ERROR",
            "subject": "supabase/migrations/00000000000000_injected_v1.sql",
            "detail": "injected",
            "fingerprint": "injected-fingerprint-not-in-baseline",
        }
    )
    result2 = CONFORMANCE.classify(mutated, baseline)
    assert result2["new_drift"] == 1


def test_module_is_runnable_and_exits_zero_on_current_debt():
    proc = subprocess.run(
        ["python", "-B", str(MODULE_PATH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "CONTRACT_REGISTRY_CONFORMANCE" in proc.stdout
