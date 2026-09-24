from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
GOVERNANCE = ROOT / ".naya" / "governance"
for path in (RUNTIME, GOVERNANCE, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from governance_kernel import Epistemic
from execution_controller import derive_epistemic_state


def test_verified_requires_explicit_pass_and_verified():
    assert derive_epistemic_state({"result": "PASS"}, {"status": "VERIFIED"}) == Epistemic.VERIFIED


def test_observed_requires_explicit_observed_verification():
    assert derive_epistemic_state({"result": "PASS"}, {"status": "OBSERVED"}) == Epistemic.OBSERVED


def test_missing_evidence_is_unknown():
    assert derive_epistemic_state({}, {"status": "VERIFIED"}) == Epistemic.UNKNOWN


def test_missing_verification_is_unknown():
    assert derive_epistemic_state({"result": "PASS"}, {}) == Epistemic.UNKNOWN


def test_fail_is_never_observed():
    assert derive_epistemic_state({"result": "FAIL"}, {"status": "VERIFIED"}) == Epistemic.UNKNOWN


def test_malformed_evidence_is_unknown():
    assert derive_epistemic_state(["PASS"], {"status": "VERIFIED"}) == Epistemic.UNKNOWN


def test_unknown_input_is_unknown():
    assert derive_epistemic_state({"result": "UNKNOWN"}, {"status": "UNKNOWN"}) == Epistemic.UNKNOWN


if __name__ == "__main__":
    tests = [
        test_verified_requires_explicit_pass_and_verified,
        test_observed_requires_explicit_observed_verification,
        test_missing_evidence_is_unknown,
        test_missing_verification_is_unknown,
        test_fail_is_never_observed,
        test_malformed_evidence_is_unknown,
        test_unknown_input_is_unknown,
    ]
    for test in tests:
        test()
        print(f"PASS — {test.__name__}")
    print(f"PASS — {len(tests)} epistemic mapping tests")
