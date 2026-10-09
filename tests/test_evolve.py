import hashlib

import pytest

from tools.evolve import (
    REQUIRED_FIELDS,
    _canonical,
    build_successor_package,
    verify_successor_package,
)


def _valid_inputs(**overrides):
    inputs = {
        "identity_context": "naya-1 / NayaPOWER / naya",
        "mission": "Preserve intelligence across Naya generations",
        "current_truth": [
            {"id": "SN-016", "truth_state": "RATIFIED"},
            {"id": "SN-A1", "truth_state": "ACTIVE"},
            {"id": "SN-L1", "truth_state": "LEARNED"},
        ],
        "authority_boundary": "No production deploys, no credentials, no destructive actions without the human director.",
        "material_blockers": ["None currently; checkpoint store healthy."],
        "next_action": "Cold successor verifies this package, then inherits known state.",
    }
    inputs.update(overrides)
    return inputs


def test_evolve_build_valid_package_verifies_true():
    package = build_successor_package(**_valid_inputs())
    for field_name in REQUIRED_FIELDS:
        assert field_name in package
    assert package["schema"] == "naya.evolve.successor-package.v1"
    assert package["built_by"] == "evolve"
    assert len(package["package_hash"]) == 64
    assert verify_successor_package(package) == {"valid": True}


def test_evolve_tampered_mission_fails_hash_check():
    package = build_successor_package(**_valid_inputs())
    package["mission"] = "TAMPERED-MISSION"
    result = verify_successor_package(package)
    assert result["valid"] is False
    assert any("hash" in reason for reason in result["reasons"])


def test_evolve_tampered_next_action_fails_hash_check():
    package = build_successor_package(**_valid_inputs())
    package["next_action"] = "Do something else entirely"
    result = verify_successor_package(package)
    assert result["valid"] is False
    assert "package_hash_mismatch" in result["reasons"]


def test_evolve_missing_field_fails():
    package = build_successor_package(**_valid_inputs())
    del package["next_action"]
    result = verify_successor_package(package)
    assert result["valid"] is False
    assert "missing_field:next_action" in result["reasons"]


def test_evolve_candidate_truth_entry_fails():
    package = build_successor_package(**_valid_inputs())
    # Tamper the truth state, then re-seal the hash so the ONLY failure is the
    # truth-state check.
    package["current_truth"][0]["truth_state"] = "CANDIDATE"
    body = {k: v for k, v in package.items() if k != "package_hash"}
    package["package_hash"] = hashlib.sha256(_canonical(body)).hexdigest()
    result = verify_successor_package(package)
    assert result["valid"] is False
    assert any("truth" in reason for reason in result["reasons"])


def test_evolve_build_rejects_candidate_truth_at_build_time():
    inputs = _valid_inputs(current_truth=[{"id": "SN-X", "truth_state": "CANDIDATE"}])
    try:
        build_successor_package(**inputs)
    except ValueError as exc:
        assert "truth" in str(exc).lower() or "ACTIVE" in str(exc)
    else:
        raise AssertionError("build must fail closed on sub-ACTIVE truth")


@pytest.mark.parametrize(
    "field_name",
    ["identity_context", "mission", "current_truth", "authority_boundary", "next_action"],
)
def test_evolve_build_rejects_empty_required_input(field_name):
    inputs = _valid_inputs(**{field_name: "" if field_name != "current_truth" else []})
    try:
        build_successor_package(**inputs)
    except ValueError as exc:
        assert field_name in str(exc)
    else:
        raise AssertionError(f"build must fail closed on empty {field_name}")


def test_evolve_build_rejects_none_blockers():
    inputs = _valid_inputs(material_blockers=None)
    try:
        build_successor_package(**inputs)
    except ValueError as exc:
        assert "material_blockers" in str(exc)
    else:
        raise AssertionError("build must fail closed on None material_blockers")


def test_evolve_empty_blockers_list_is_allowed():
    # "No material blockers" is a meaningful governed claim, not a missing input.
    package = build_successor_package(**_valid_inputs(material_blockers=[]))
    assert verify_successor_package(package) == {"valid": True}


def test_evolve_hash_covers_all_fields():
    package = build_successor_package(**_valid_inputs())
    body = {k: v for k, v in package.items() if k != "package_hash"}
    expected = hashlib.sha256(_canonical(body)).hexdigest()
    assert package["package_hash"] == expected
