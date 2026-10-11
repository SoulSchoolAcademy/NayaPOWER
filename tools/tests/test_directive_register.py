"""Directive Register validation tests.

Validates BRAIN/01-GOVERNANCE/directive-register.json against Shawn's
requirements. These are REAL asserts — if the register is wrong, the tests
fail. No theater.

Shawn's number: 58 master directives (D8-D65). D6-D7 are meta-governance
(resolutions/reopening), not master directives for building the system.
"""
import json
from pathlib import Path

REGISTER_PATH = Path(__file__).parent.parent.parent / "BRAIN" / "01-GOVERNANCE" / "directive-register.json"

VALID_STATUSES = {"NOT_STARTED", "BUILDING", "BUILT_AS_CODE", "ENFORCED"}
VALID_OWNERS = {"naya2", "naya4", "naya5", "all"}
VALID_WAVES = {1, 2, 3, 4, 5, 6}


def load_register():
    """Load the directive register. Fails if file missing or invalid JSON."""
    assert REGISTER_PATH.exists(), f"Register not found at {REGISTER_PATH}"
    with open(REGISTER_PATH) as f:
        data = json.load(f)
    assert isinstance(data, list), "Register must be a JSON array"
    return data


def test_count_is_58():
    """Shawn's number: exactly 58 master directives (D8-D65)."""
    data = load_register()
    actual = len(data)
    assert actual == 58, (
        f"Directive count is {actual}, expected 58 (Shawn's number). "
        f"D8-D65 = 58. D6-D7 are meta-governance, excluded."
    )


def test_no_duplicate_ids():
    """Every directive ID must be unique."""
    data = load_register()
    ids = [d["id"] for d in data]
    assert len(ids) == len(set(ids)), (
        f"Duplicate directive IDs found: {[i for i in ids if ids.count(i) > 1]}"
    )


def test_ids_are_d8_through_d65():
    """IDs must be exactly D8, D9, ..., D65 with no gaps."""
    data = load_register()
    ids = sorted([d["id"] for d in data], key=lambda x: int(x[1:]))
    expected = [f"D{i}" for i in range(8, 66)]
    assert ids == expected, (
        f"ID mismatch. Missing: {set(expected) - set(ids)}. "
        f"Extra: {set(ids) - set(expected)}."
    )


def test_every_entry_has_source():
    """Every directive must trace to its source issue and comment. No exceptions."""
    data = load_register()
    for d in data:
        assert "source_issue" in d and d["source_issue"], (
            f"{d.get('id', '?')}: missing source_issue"
        )
        assert d["source_issue"] in (1354, 2175), (
            f"{d['id']}: source_issue must be 1354 or 2175, got {d['source_issue']}"
        )
        assert "source_comment" in d and d["source_comment"], (
            f"{d['id']}: missing source_comment"
        )
        # Comment ID must be numeric
        assert str(d["source_comment"]).isdigit(), (
            f"{d['id']}: source_comment must be a numeric comment ID, "
            f"got {d['source_comment']}"
        )


def test_every_entry_has_owner():
    """Every directive must have a valid owner."""
    data = load_register()
    for d in data:
        assert "owner" in d and d["owner"], f"{d.get('id', '?')}: missing owner"
        assert d["owner"] in VALID_OWNERS, (
            f"{d['id']}: owner must be one of {VALID_OWNERS}, got {d['owner']}"
        )


def test_status_values_valid():
    """Status must be one of the four valid values."""
    data = load_register()
    for d in data:
        assert "status" in d and d["status"], f"{d.get('id', '?')}: missing status"
        assert d["status"] in VALID_STATUSES, (
            f"{d['id']}: status must be one of {VALID_STATUSES}, got {d['status']}"
        )


def test_evidence_pr_requires_built_status():
    """If evidence_pr is set, status must be BUILT_AS_CODE or ENFORCED.
    
    A PR number without built status is a lie — it claims code exists
    that hasn't been built.
    """
    data = load_register()
    for d in data:
        pr = d.get("evidence_pr")
        if pr is not None:
            assert d["status"] in ("BUILT_AS_CODE", "ENFORCED"), (
                f"{d['id']}: evidence_pr=#{pr} set but status is {d['status']}. "
                f"Must be BUILT_AS_CODE or ENFORCED."
            )
            assert isinstance(pr, int) and pr > 0, (
                f"{d['id']}: evidence_pr must be a positive integer, got {pr}"
            )


def test_built_as_code_requires_evidence_pr():
    """If status is BUILT_AS_CODE or ENFORCED, evidence_pr must be set.
    
    You cannot claim BUILT_AS_CODE without pointing to the code.
    """
    data = load_register()
    for d in data:
        if d["status"] in ("BUILT_AS_CODE", "ENFORCED"):
            assert d.get("evidence_pr") is not None, (
                f"{d['id']}: status is {d['status']} but evidence_pr is not set. "
                f"Point to the PR."
            )


def test_wave_values_valid():
    """Wave must be 1-6 or null."""
    data = load_register()
    for d in data:
        wave = d.get("wave")
        if wave is not None:
            assert wave in VALID_WAVES, (
                f"{d['id']}: wave must be 1-6 or null, got {wave}"
            )


def test_no_enforced_without_proof():
    """ENFORCED status requires explicit justification.
    
    Currently 0 directives are ENFORCED (per 2026-10-11 re-score: all 8
    'built' directives are CODE-ONLY, not enforced). This test documents
    that ENFORCED is a higher bar than BUILT_AS_CODE — it means a machine
    gate actively blocks violations.
    
    If this test fails because someone marked a directive ENFORCED, they
    must provide proof of the enforcement mechanism.
    """
    data = load_register()
    enforced = [d for d in data if d["status"] == "ENFORCED"]
    # Currently expecting zero — the re-score proved 0 of 8 are enforced.
    # This is not a failure; it's the honest baseline.
    # When a directive becomes truly enforced, update this test with proof.
    for d in enforced:
        assert d.get("enforcement_proof"), (
            f"{d['id']}: marked ENFORCED but no enforcement_proof provided. "
            f"ENFORCED requires a machine gate that fails on violation."
        )
