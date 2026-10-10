"""AER-PROVIDER-1 tests (SN-0794): the D1-D12 adversarial suite, the provider
state-machine model checker with its seven broken-provider mutations, the
retention-horizon inequality, the effect-observation chain, qualification
verdicts, and the AER-PROVIDER-001 fixture."""
import threading

import pytest

from drift_canary.revocation_linearization import (
    PROVIDER_CONTRACT_DIMENSIONS,
    PROVIDER_CONTRACT_DIMENSION_NAMES,
    PROVIDER_QUALIFICATION_VERDICTS,
    BROKEN_PROVIDER_MUTATIONS,
    ProviderProofPackage,
    proof_package_complete,
    qualify_provider_contract,
    verify_effect_chain,
    retention_horizon_ok,
    recovery_window_valid,
    run_d_suite,
    d1_concurrent_same_key,
    d3_late_completion_race,
    d5_payload_mismatch,
    d6_restart_failover,
    d7_regional_boundary,
    d9_retention_boundary,
    d12_incomplete_observability,
    provider_machine_check,
    broken_provider_mutation_check,
    aer_provider_001,
    MockExternalProvider,
    LogicalOperation,
)


def _pkg(**kw):
    base = dict(provider_contract="contract v3",
                mechanism_evidence="atomic insert-key-first",
                adversarial_execution_evidence="D1-D12 + 7 mutations",
                independent_effect_observation="ledger counts per level")
    base.update(kw)
    return ProviderProofPackage(**base)


def _full_evidence():
    return {name: ("QUALIFIED", f"ev-{name}")
            for name in PROVIDER_CONTRACT_DIMENSION_NAMES}


def test_eleven_dimensions():
    assert len(PROVIDER_CONTRACT_DIMENSIONS) == 11
    names = [d[0] for d in PROVIDER_CONTRACT_DIMENSIONS]
    assert "payload_binding" in names  # the eleventh: same key, different payload
    for name, must, evidence, _illustration in PROVIDER_CONTRACT_DIMENSIONS:
        assert must and evidence, name


def test_d_suite_qualified_and_d12_unproven():
    results = {r["id"]: r for r in run_d_suite()}
    for did in ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11"):
        assert results[did]["verdict"] == "QUALIFIED", (did, results[did])
    assert results["D12"]["verdict"] == "UNPROVEN"
    assert "never a fabricated verdict" in results["D12"]["evidence"]


def test_d1_concurrent_same_key_positive_control():
    r = d1_concurrent_same_key(n_threads=8)
    assert r["verdict"] == "QUALIFIED" and "8 concurrent" in r["evidence"]


def test_d3_broken_guard_detected():
    # The harness MUST detect the removed atomic guard -- a harness that
    # cannot is not qualified for the real provider.
    r = d3_late_completion_race(guard_mode="broken_record_after_effect")
    assert r["verdict"] == "DEFECT_DETECTED", r
    assert r["provider_effects"] == 2 and r["downstream_effects"] == 2


def test_d5_payload_mismatch_rejected():
    r = d5_payload_mismatch()
    assert r["verdict"] == "QUALIFIED"
    assert "REJECTED_PAYLOAD_MISMATCH" in r["evidence"]


def test_d6_failover_broken_detected():
    r = d6_restart_failover(lose_dedup=True)
    assert r["verdict"] == "DEFECT_DETECTED", r


def test_d6_failover_preserves_identity():
    r = d6_restart_failover(lose_dedup=False)
    assert r["verdict"] == "QUALIFIED"


def test_d7_scope_bound():
    r = d7_regional_boundary()
    assert r["verdict"] == "QUALIFIED"
    assert "OUT_OF_SCOPE" in r["evidence"]


def test_d9_retention_boundary_and_inequality():
    r = d9_retention_boundary()
    assert r["verdict"] == "QUALIFIED"


def test_effect_chain_levels_separate():
    p = MockExternalProvider()
    op = LogicalOperation("OP-CHAIN", "payments", "hash",
                          authorization_rev=1, created_at_seq=1)
    for _ in range(4):
        p.submit(op)
    p.emit_downstream("OP-CHAIN", "eff-1")
    chain = verify_effect_chain(p, "OP-CHAIN")
    assert chain["responses_seen"] == 4
    assert chain["provider_effects"] == 1
    assert chain["downstream_effects"] == 1
    assert chain["dedup_working"]  # 4 responses, 1 resource: dedup working
    assert not chain["duplicate_effect"]


def test_effect_chain_duplicate_visible():
    p = MockExternalProvider()
    p.guard_mode = "broken_record_after_effect"
    p.downstream_dedup_on = False
    op = LogicalOperation("OP-CH2", "payments", "hash",
                          authorization_rev=1, created_at_seq=1)
    gate = threading.Event()
    entered = threading.Event()
    p.pause_before_commit = gate
    p.pre_commit_hook = lambda _k: entered.set()
    t = threading.Thread(target=lambda: p.submit(op))
    t.start()
    entered.wait(10)
    p.pause_before_commit = None  # B must not block; A holds the window
    p.submit(op)
    gate.set()
    t.join(10)
    for _k, eff in list(p.ledger):
        p.emit_downstream("OP-CH2", f"down-{eff}")
    chain = verify_effect_chain(p, "OP-CH2")
    assert chain["duplicate_effect"]
    assert chain["downstream_exceeds_root"] is False  # 2 and 2
    assert chain["downstream_effects"] == 2


def test_retention_horizon_inequality():
    assert retention_horizon_ok(0, 5, 10)
    assert retention_horizon_ok(0, 9, 10, uncertainty_allowance=0)
    assert not retention_horizon_ok(0, 9, 10, uncertainty_allowance=2)
    assert not retention_horizon_ok(0, 10, 10)  # boundary is strict


def test_recovery_window_from_first_request_survives_failover():
    p = MockExternalProvider()
    p.retention_horizon["OP-W"] = 100
    op = LogicalOperation("OP-W", "payments", "hash",
                          authorization_rev=1, created_at_seq=1)
    p.submit(op)
    t_first = p.first_request_at["OP-W"]
    p2 = p.failover()  # worker restart / provider failover
    ok, why = recovery_window_valid(p2, "OP-W", t_last_retry=t_first + 50)
    assert ok, why  # window NOT reset by the restart
    ok2, _ = recovery_window_valid(p2, "OP-W", t_last_retry=t_first + 150)
    assert not ok2


def test_recovery_window_undefined_without_observation():
    p = MockExternalProvider()
    ok, why = recovery_window_valid(p, "OP-NEVER", t_last_retry=5)
    assert not ok and "undefined" in why


def test_proof_package_completeness():
    ok, missing = proof_package_complete(_pkg())
    assert ok and missing == ()
    ok2, missing2 = proof_package_complete(_pkg(mechanism_evidence=""))
    assert not ok2 and missing2 == ("mechanism_evidence",)


def test_qualify_all_good():
    cert = qualify_provider_contract(
        "mock", "payments.charge", "v3", _full_evidence(), _pkg(),
        downstream_covered=True, retention_ok=True)
    assert cert.overall_verdict == "QUALIFIED_IN_SCOPE"
    assert cert.downstream_coverage == "DOWNSTREAM_EFFECTS_QUALIFIED"


def test_qualify_missing_dimension_unproven():
    ev = _full_evidence()
    del ev["retention"]
    cert = qualify_provider_contract("mock", "s", "v3", ev, _pkg(),
                                     downstream_covered=True, retention_ok=True)
    assert cert.overall_verdict == "UNPROVEN"


def test_qualify_root_only_partially_qualified():
    cert = qualify_provider_contract("mock", "s", "v3", _full_evidence(), _pkg(),
                                     downstream_covered=False, retention_ok=True)
    assert cert.overall_verdict == "PARTIALLY_QUALIFIED"
    assert cert.downstream_coverage == "DOWNSTREAM_EFFECTS_UNPROVEN"


def test_qualify_failed_dimension():
    ev = _full_evidence()
    ev["atomicity"] = ("FAILED", "race reproduced")
    cert = qualify_provider_contract("mock", "s", "v3", ev, _pkg(),
                                     downstream_covered=True, retention_ok=True)
    assert cert.overall_verdict == "FAILED"


def test_qualify_out_of_scope():
    cert = qualify_provider_contract("mock", "s", "v3", _full_evidence(), _pkg(),
                                     downstream_covered=True, retention_ok=True,
                                     operation_in_scope=False)
    assert cert.overall_verdict == "OUT_OF_SCOPE"


def test_qualify_verdicts_are_capability_not_law():
    assert set(PROVIDER_QUALIFICATION_VERDICTS) == {
        "QUALIFIED_IN_SCOPE", "PARTIALLY_QUALIFIED", "FAILED",
        "UNPROVEN", "OUT_OF_SCOPE"}


def test_machine_honest_exhaustively_clean():
    violated, trace = provider_machine_check()
    assert not violated and trace == ()


def test_machine_all_mutations_minimal_counterexamples():
    report = broken_provider_mutation_check()
    assert len(BROKEN_PROVIDER_MUTATIONS) == 7
    for m in BROKEN_PROVIDER_MUTATIONS:
        v = report[m]
        assert v["violated"], m
        assert 4 <= v["trace_length"] <= 5, (m, v)  # minimal
    # Spot-check the shapes.
    assert report["non_atomic_dedup"]["trace"][1].endswith("+race")
    assert report["failover_loss"]["trace"][2] == "failover+drops_dedup"
    assert report["downstream_without_dedup"]["trace"][-2:] == (
        "emit_downstream", "emit_downstream")


def test_aer_provider_001():
    r = aer_provider_001()
    assert r["intact_at_most_one"] == {"root": 1, "downstream": 1}
    assert r["broken_guard_counterexample"]["verdict"] == "DEFECT_DETECTED"
    assert r["crash_variant_at_most_one"] == 1
    assert r["expiry_variant_rejects"] == "REJECTED_KEY_EXPIRED"
    assert "never reported as production proof" in r["mock_only"]
