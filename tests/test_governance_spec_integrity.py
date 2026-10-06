import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / "BRAIN" / "01-GOVERNANCE"

SPECS = {
    "0004": {
        "machine": GOV / "0004-nonstop-loop-v1.machine.json",
        "ai": GOV / "0004-NONSTOP-LOOP-V1.ai.md",
        "human": GOV / "0004-NONSTOP-LOOP-V1.human.md",
        "phases": [
            "OBSERVE", "RANK", "SIGN_IN", "ACT",
            "SIGN_OUT", "SCORECARD", "LEARN", "REPEAT",
        ],
    },
    "0005": {
        "machine": GOV / "0005-captain-operating-protocol-v1.machine.json",
        "ai": GOV / "0005-CAPTAIN-OPERATING-PROTOCOL-V1.ai.md",
        "human": GOV / "0005-CAPTAIN-OPERATING-PROTOCOL-V1.human.md",
        "phases": [
            "OBSERVE", "RANK_TEN", "DECLARE", "ACT",
            "VERIFY", "REPORT_BACK", "LEARN", "REPEAT",
        ],
    },
}


def _load(spec):
    return json.loads(spec["machine"].read_text(encoding="utf-8"))


def test_ratified_governance_machine_twins_parse_and_keep_identity():
    for law, spec in SPECS.items():
        data = _load(spec)
        assert data["schema_version"] == "1.0", law
        assert data["status"] == "DIRECTOR-RATIFIED", law
        assert data["ratified_by"] == "Shawn Vibert", law
        assert data["ratified_date"] == "2026-10-05", law
        assert spec["ai"].is_file(), law
        assert spec["human"].is_file(), law


def test_machine_phase_order_matches_each_normative_ai_projection():
    for law, spec in SPECS.items():
        data = _load(spec)
        loop = data.get("loop") or data.get("cycle")
        assert loop["terminal"] is False, law
        actual = [phase["name"] for phase in loop["phases"]]
        assert actual == spec["phases"], (law, actual)

        ai = spec["ai"].read_text(encoding="utf-8")
        for index, phase in enumerate(spec["phases"], start=1):
            token = phase.replace("_", r"[_ ]")
            assert re.search(
                rf"(?:Phase\s+{index}\b|\|\s*{index}\s*\|).*{token}",
                ai,
                flags=re.IGNORECASE,
            ), f"{law}: phase {index} {phase} missing from AI projection"


def test_human_and_ai_views_both_identify_director_ratification():
    for law, spec in SPECS.items():
        for surface in ("ai", "human"):
            text = spec[surface].read_text(encoding="utf-8").upper()
            assert "DIRECTOR-RATIFIED" in text, (law, surface)
            assert "2026-10-05" in text, (law, surface)


def test_captain_protocol_extends_nonstop_and_points_to_governing_boot_text():
    data = _load(SPECS["0005"])
    assert data["law_id"] == "PROACTIVE-CAPTAIN-V1"
    assert "0004-NONSTOP-LOOP-V1" in data["extends"]
    assert data["cycle"]["declare_before_act"] is True
    assert data["governing_boot_text"] == "AGENTS.md :: CAPTAIN MODE"

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "## CAPTAIN MODE" in agents
    assert "WHAT I SEE" in agents
    assert "RESULT" in agents


def test_ratified_spec_integrity_does_not_silently_drop_evidence_law():
    for law, spec in SPECS.items():
        evidence = _load(spec)["invariants"]["evidence_law"].replace(" ", "")
        assert "UNKNOWN!=PASS" in evidence, law
        assert "IMPLEMENTED!=VERIFIED" in evidence, law
        assert "VERIFIED!=PRODUCTION-PROVEN" in evidence, law
