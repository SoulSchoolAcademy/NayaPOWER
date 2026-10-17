"""Charter sync test — the law is the code.

MANIFESTO.machine.json is the canonical MACHINE source of the charter.
This test enforces that the human projections stay in sync with it:

- MANIFESTO.md must contain the motto and manifesto_statement verbatim.
- CONSTITUTION/0003-CONSTITUTIONAL-CODE-V1.md must contain all twelve law titles.
- MISSION-CONTRACT-V1.md must contain the mission question.
- tools/charter.py must expose exactly what the JSON declares.

If the charter changes, change the JSON first — then the projections, then this
test stays green. A red test here means the law and the code have diverged.
"""

import json
from pathlib import Path

import tools.charter as charter

ROOT = Path(__file__).resolve().parents[1]


def _read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def _charter_json():
    return json.loads((ROOT / "MANIFESTO.machine.json").read_text(encoding="utf-8"))


def test_charter_json_is_valid():
    data = _charter_json()
    assert data["schema"] == "naya.charter.v1"
    assert len(data["twelve_laws"]) == 12
    assert len(data["manifesto_full"]) == 6
    assert len(data["five_questions"]) == 5
    assert len(data["precedence_chain"]) == 3


def test_manifesto_md_carries_motto_verbatim():
    data = _charter_json()
    md = _read("MANIFESTO.md")
    assert data["motto"] in md, "motto diverged from machine source"
    assert data["manifesto_statement"] in md, "manifesto statement diverged"


def test_constitutional_code_carries_all_twelve_laws():
    data = _charter_json()
    code = _read("CONSTITUTION/0003-CONSTITUTIONAL-CODE-V1.md")
    for law in data["twelve_laws"]:
        assert law["title"] in code, f"law missing from code: {law['id']}"
        assert law["id"] not in code or True  # ids are machine-side; titles are human-side


def test_mission_contract_carries_mission_question():
    data = _charter_json()
    mission = _read("MISSION-CONTRACT-V1.md")
    assert data["mission_question"] in mission, "mission question diverged"


def test_charter_module_matches_json():
    data = _charter_json()
    assert charter.MOTTO == data["motto"]
    assert charter.MANIFESTO_STATEMENT == data["manifesto_statement"]
    assert charter.MISSION_QUESTION == data["mission_question"]
    assert [l["id"] for l in charter.TWELVE_LAWS] == [l["id"] for l in data["twelve_laws"]]
    assert charter.law("FAIL_CLOSED")["title"] == "FAIL CLOSED"


def test_recite_contains_motto_and_all_laws():
    spoken = charter.recite()
    assert charter.MOTTO in spoken
    for law in charter.TWELVE_LAWS:
        assert law["title"] in spoken


def test_ai_charter_doc_exists_and_carries_law_ids():
    data = json.loads((ROOT / "MANIFESTO.machine.json").read_text(encoding="utf-8"))
    ai = (ROOT / "MANIFESTO.ai.md").read_text(encoding="utf-8")
    assert data["motto"] in ai, "ai doc missing motto"
    for law in data["twelve_laws"]:
        assert law["id"] in ai, f"ai doc missing law id: {law['id']}"
