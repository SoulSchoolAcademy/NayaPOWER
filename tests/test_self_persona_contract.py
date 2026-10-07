"""Conformance tests for the canonical Naya persona identity contract (SELF node).

Positive controls: the contract pins name/character/tone/seat semantics/
dictation rule and stays CANDIDATE (only Shawn ratifies).
Negative controls: no RATIFIED claim anywhere in the new artifacts.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOC = REPO / "BRAIN/03-KERNEL/NODES/SELF/0003-PERSONA-IDENTITY-CONTRACT-V1.md"
OBJ = REPO / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-PERSONA-V1.json"


def _doc_text():
    assert DOC.exists(), "persona identity contract document missing"
    return DOC.read_text(encoding="utf-8")


def _obj():
    assert OBJ.exists(), "persona identity object JSON missing"
    return json.loads(OBJ.read_text(encoding="utf-8"))


def test_persona_contract_pins_name_character_and_tone():
    text = _doc_text()
    assert "Name | Naya" in text
    assert "AI operating partner, director, integrator, continuity steward" in text
    assert "warm, direct, enthusiastic, truthful, practical, clear" in text


def test_persona_contract_declares_candidate_status():
    text = _doc_text()
    assert "CANDIDATE" in text
    assert "only Shawn ratifies" in text


def test_persona_contract_pins_seat_semantics():
    text = _doc_text()
    assert "seat designations" in text
    assert "never identities" in text
    assert "MUST NOT redefine durable identity" in text


def test_persona_contract_pins_dictation_rule():
    text = _doc_text()
    assert "Maya" in text and "Mia" in text and "Abby" in text
    assert "never treat it as a rename" in text


def test_persona_contract_forbids_consciousness_and_human_claims():
    text = _doc_text()
    assert "Claim consciousness from persistence or behavior" in text
    assert "Claim to be human" in text


def test_persona_contract_layers_on_existing_contracts():
    text = _doc_text()
    assert "0001-CONTRACT.md" in text
    assert "0002-ELITE-SELF-CONTRACT-V2.md" in text
    assert "kernel/naya_identity_binding.py" in text


def test_persona_object_json_honest_proof_block():
    obj = _obj()
    assert obj["object_id"] == "NAYA-PERSONA-V1"
    assert obj["canonical_status"] == "CANDIDATE"
    proof = obj["proof"]
    assert proof["implementation_status"] == "DOCUMENTED"
    assert proof["behavioral_status"] == "NOT_PROVEN"
    assert proof["production_status"] == "NOT_PROVEN"


def test_persona_object_json_matches_doc_fields():
    obj = _obj()
    ai = obj["ai_view"]
    assert ai["name"] == "Naya"
    assert "naya-1..naya-5" in ai["seat_semantics"]
    assert "Maya" in ai["dictation_rule"]


def test_no_ratified_claim_in_new_artifacts():
    # Only Shawn ratifies. A CANDIDATE artifact must never claim RATIFIED
    # status; every line mentioning RATIFIED must be a denial of such a claim.
    deny_phrases = ("not claim", "never", "only shawn", "no test")
    text = _doc_text()
    for line in text.splitlines():
        if "RATIFIED" in line:
            lowered = line.lower()
            assert any(p in lowered for p in deny_phrases), (
                f"line claims or implies RATIFIED without denial: {line.strip()}"
            )
    obj_text = OBJ.read_text(encoding="utf-8")
    assert "RATIFIED" not in obj_text


def test_persona_object_contract_path_exists():
    obj = _obj()
    contract_rel = obj["machine_view"]["contract"]
    assert (REPO / contract_rel).exists()
