"""Adversarial regression tests for constitutional authority enforcement.

Design note: the gate does NOT try to guess semantics from wording. It performs a
broad candidate scan and requires every candidate to be classified in the declared
constitutional authority registry. That makes the failure mode "undeclared claim",
which is wording-independent, instead of "phrase I did not think of".

The retired phrase detector is retained in the validator so these tests can prove it
was blind to every real claim in the repository.
"""
import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / ".naya" / "control-plane" / "validate_control_plane.py"
REGISTRY = REPO / ".naya" / "control-plane" / "CONSTITUTIONAL-AUTHORITY-REGISTRY.json"


def _load():
    spec = importlib.util.spec_from_file_location("control_plane_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v = _load()


def _registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


# --- The live conflict is real and is recorded, not resolved -----------------

def test_registry_records_the_conflict_without_resolving_it():
    reg = _registry()
    assert reg["precedence_status"] == "UNRESOLVED"
    competing = [e for e in reg["entries"] if e["role"] == "COMPETING_UNRESOLVED"]
    paths = {e["path"] for e in competing}
    assert ".naya/contracts/00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md" in paths
    assert len(competing) >= 3


def test_unresolved_precedence_blocks_the_gate():
    assert v.precedence_blockers(_registry()) != []


def test_gate_would_pass_only_after_explicit_human_ratification():
    reg = _registry()
    assert v.precedence_blockers(reg), "unresolved precedence must block"

    # A human ratifies precedence and records the superseded claim explicitly.
    reg["precedence_status"] = "RATIFIED"
    for entry in reg["entries"]:
        if entry["role"] == "COMPETING_UNRESOLVED":
            entry["role"] = "SUPERSEDED"
    assert v.precedence_blockers(reg) == []


def test_two_canonical_authorities_always_block():
    reg = _registry()
    reg["precedence_status"] = "RATIFIED"
    reg["entries"].append({"path": ".naya/contracts/99-OTHER.md", "role": "CANONICAL"})
    blockers = v.precedence_blockers(reg)
    assert any("exactly one CANONICAL" in b for b in blockers)


# --- Wording-independent adversarial fixtures --------------------------------

ADVERSARIAL_UNREGISTERED = {
    "plain_constitution": ".naya/contracts/99-OTHER-CONSTITUTION.md",
    "charter_no_word_constitution": ".naya/contracts/99-SUPREME-CHARTER.md",
    "statute": ".naya/contracts/99-FOUNDING-STATUTE.md",
    "no_obvious_title": ".naya/contracts/99-ORDER-OF-RULES.md",
    "amendment_filename_disguise": ".naya/codex/CONSTITUTIONAL-AMENDMENT-DISGUISE.md",
    "registry_titled_claim": ".naya/contracts/99-REGISTRY-OF-TRUTH.md",
}


def test_any_unregistered_authority_claim_blocks_regardless_of_wording():
    registered = {e["path"] for e in _registry()["entries"]}
    for name, path in ADVERSARIAL_UNREGISTERED.items():
        assert path not in registered, f"{name} fixture must start unregistered"
        assert v.unregistered_authority_candidates({path: {}}, registered) == [path]


def test_adding_classifications_never_clears_an_existing_blocker():
    """The gate must not be launderable by adding entries to the registry."""
    reg = _registry()
    before = v.precedence_blockers(reg)
    assert before
    reg["entries"].append(
        {
            "path": ".naya/contracts/99-SUPREME-CHARTER.md",
            "role": "SUBDOMAIN",
            "evidence": "attempt to downgrade a competing claim",
        }
    )
    assert v.precedence_blockers(reg) == before


def test_blocker_names_every_competing_claim_not_just_the_first():
    reg = _registry()
    blocker = " ".join(v.precedence_blockers(reg))
    for entry in reg["entries"]:
        if entry["role"] == "COMPETING_UNRESOLVED":
            assert entry["path"] in blocker


# --- The retired detector was blind -----------------------------------------

def test_retired_detector_missed_every_candidate_in_the_repository():
    candidates = v.enumerate_authority_candidates()
    assert candidates, "candidate scan must find the real claims"
    missed = [p for p, d in candidates.items() if not d["legacy_detector_detected"]]
    assert len(missed) == len(candidates), (
        "if the retired detector caught something the fixtures are not proving blindness"
    )


def test_retired_detector_missed_the_ratified_contract_00():
    raw = (REPO / ".naya" / "contracts" / "00-NAYANET-CONSTITUTIONAL-CONTRACT-LAW.md").read_text(
        encoding="utf-8"
    )
    assert "RATIFIED" in raw
    assert v.legacy_phrase_claim(raw) is False


# --- Live repository consistency --------------------------------------------

def test_every_detected_candidate_is_classified_in_the_registry():
    candidates = v.enumerate_authority_candidates()
    registered = {e["path"] for e in _registry()["entries"]}
    assert v.unregistered_authority_candidates(candidates, registered) == []


def test_every_registry_entry_exists_on_disk():
    for entry in _registry()["entries"]:
        assert (REPO / entry["path"]).is_file(), entry["path"]


def test_exactly_one_canonical_authority_is_registered():
    canonical = [e for e in _registry()["entries"] if e["role"] == "CANONICAL"]
    assert len(canonical) == 1
    assert canonical[0]["path"] == v.CANONICAL_CONSTITUTION


def test_registry_matches_the_governance_kernel():
    kernel = json.loads(
        (REPO / ".naya" / "control-plane" / "GOVERNANCE-KERNEL.json").read_text(encoding="utf-8")
    )
    assert kernel["constitutional_authority"] == v.CANONICAL_CONSTITUTION
