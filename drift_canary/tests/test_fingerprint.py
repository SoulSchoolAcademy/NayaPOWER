"""Tests: calibration fingerprint + drift signals."""
from ..fingerprint import CalibrationFingerprint, DriftSignal, DRIFT_TYPES


def _fp(**over):
    base = dict(policy_version="P2", policy_sha="abc123",
                 model_version="m1", prompt_version="p3",
                 verifier_id="naya-2", rubric_version="r1",
                 runtime_version="40df54b14", corpus_id="c1",
                 corpus_hash="h1", evidence_cutoff="2026-10-10T00:00:00Z",
                 calibration_dataset="d1", calibration_params_hash="ph1")
    base.update(over)
    return CalibrationFingerprint(**base)


def test_digest_deterministic():
    assert _fp().digest() == _fp().digest()


def test_digest_changes_with_any_field():
    assert _fp().digest() != _fp(policy_sha="zzz").digest()


def test_changed_fields_detects_policy_drift():
    changed = _fp().changed_fields(_fp(policy_version="P3", policy_sha="def456"))
    assert "policy_version" in changed and "policy_sha" in changed
    assert "model_version" not in changed


def test_no_changed_fields_when_identical():
    assert _fp().changed_fields(_fp()) == ()


def test_drift_types_are_separate_signals():
    assert len(DRIFT_TYPES) == 6
    assert len(set(DRIFT_TYPES)) == 6  # no collapsing into composites


def test_drift_signal_rejects_unknown_type():
    try:
        DriftSignal(drift_type="vibes", indicator="x", observed_at="t",
                    baseline_fingerprint="a", current_fingerprint="b",
                    evidence_ref="e")
    except AssertionError:
        return
    raise AssertionError("unknown drift type must be rejected")


def test_drift_signal_carries_both_fingerprints():
    s = DriftSignal(drift_type="policy", indicator="policy fingerprint mismatch",
                    observed_at="2026-10-10T18:00:00Z",
                    baseline_fingerprint="aaa", current_fingerprint="bbb",
                    evidence_ref="receipt-1")
    assert s.baseline_fingerprint != s.current_fingerprint
