"""Consistency tests for the nine-organ health matrix spec.

Adversarial intent: the spec's organ list must track the registry exactly, the
rung list must track the organism contract exactly, and the machine schema must
refuse the failure modes the spec's fail-closed rules name. Drift in any of
these is a silent downgrade of the health matrix's authority.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "BRAIN/03-KERNEL/0005-NINE-ORGAN-HEALTH-MATRIX-SPEC-V1.md"
SCHEMA_PATH = ROOT / "BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json"
REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
CONTRACT = ROOT / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"


def _spec_organs():
    """Extract the ordered organ list from spec §1's canonical-order line."""
    text = SPEC.read_text(encoding="utf-8")
    m = re.search(r"^`((?:[A-Z]+ → )+[A-Z]+)`$", text, re.M)
    assert m, "spec must state the canonical organ order on one backticked line"
    return [o.strip() for o in m.group(1).split("→")]


def _spec_rungs():
    """Extract the ordered rung list from spec §2's rung-order line."""
    text = SPEC.read_text(encoding="utf-8")
    m = re.search(r"highest-first claim order:\n\n`((?:[A-Z_]+ → )+[A-Z_]+)`$", text, re.M)
    assert m, "spec must state the canonical rung order right after the claim-order line"
    return [r.strip() for r in m.group(1).split("→")]


def test_spec_organ_list_tracks_registry_exactly():
    registry_order = json.loads(REGISTRY.read_text(encoding="utf-8"))["node_order"]
    assert _spec_organs() == registry_order


def test_spec_rung_list_tracks_contract_exactly():
    contract_ladder = json.loads(CONTRACT.read_text(encoding="utf-8"))["nodes"]["SELF"]["proof_ladder"]
    assert _spec_rungs() == contract_ladder
    assert len(contract_ladder) == 8


def test_schema_organs_and_rungs_match_spec():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    organ_enum = schema["properties"]["organs"]["items"]["properties"]["organ"]["enum"]
    rung_enum = schema["properties"]["organs"]["items"]["properties"]["current_rung"]["enum"]
    rung_evidence_enum = schema["properties"]["organs"]["items"]["properties"]["rung_evidence"]["items"]["properties"]["rung"]["enum"]
    assert organ_enum == _spec_organs()
    assert rung_enum == ["UNKNOWN"] + _spec_rungs()
    assert rung_evidence_enum == _spec_rungs()


def test_schema_demands_exactly_nine_organs():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    organs = schema["properties"]["organs"]
    assert organs["minItems"] == 9 and organs["maxItems"] == 9


def test_schema_stamped_sha_refuses_short_sha():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    pattern = schema["properties"]["stamped_sha"]["pattern"]
    assert re.fullmatch(pattern, "507d34213333a38708912d343537985e619938ac")
    # Adversarial: short SHAs, SHAs with non-hex chars, and empty strings must fail.
    for bad in ("507d3421", "507d34213333a38708912d343537985e619938aZ", "", "main"):
        assert not re.fullmatch(pattern, bad), f"bad SHA accepted: {bad!r}"


def test_schema_requires_next_proof_fields():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    item = schema["properties"]["organs"]["items"]
    for field in ("organ", "current_rung", "missing_rung", "next_proof", "rung_evidence"):
        assert field in item["required"], f"missing required field {field}"
    # UNKNOWN_NOT_DISPATCHED / UNKNOWN_NOT_QUALIFIED must exist so PRODUCTION and
    # SUCCESSOR can never be claimed from CI alone.
    statuses = item["properties"]["rung_evidence"]["items"]["properties"]["status"]["enum"]
    assert "UNKNOWN_NOT_DISPATCHED" in statuses
    assert "UNKNOWN_NOT_QUALIFIED" in statuses


def test_spec_contains_fail_closed_rules():
    text = SPEC.read_text(encoding="utf-8")
    for marker in (
        "UNKNOWN ≠ PASS",
        "UNKNOWN_NOT_DISPATCHED",
        "UNKNOWN_NOT_QUALIFIED",
        "caps every organ at CONTRACT",
        "never hand-edited",
        "manufactured tenths",
    ):
        assert marker in text, f"spec missing fail-closed marker: {marker}"


def test_spec_does_not_score_organs_numerically():
    # The matrix records rungs, not numbers: no "X/10" organ-score claims.
    text = SPEC.read_text(encoding="utf-8")
    assert not re.search(r"\b\d(\.\d)?/10\b", text), "spec must not carry numeric organ scores"
