"""Unit tests for kernel/persona_loader.py (SELF node persona identity).

Positive controls: canonical loads, pins hold, seat stays a designation,
dictation variants resolve, conflicts are recorded with canonical winning.
Negative controls: missing/unreadable/incomplete canonical source halts
(PersonaSourceMissing -- never improvise); conflicting source never wins.
"""
import json
from pathlib import Path

import pytest

from kernel.persona_loader import (
    PersonaIdentity,
    PersonaSourceMissing,
    load_persona,
    normalize_dictation_name,
    present_identity,
)

REPO = Path(__file__).resolve().parents[1]
CANONICAL = REPO / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-PERSONA-V1.json"


def _write(tmp_path: Path, name: str, payload: dict) -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _canonical_payload(**overrides):
    base = json.loads(CANONICAL.read_text(encoding="utf-8"))
    for key, value in overrides.items():
        base[key] = value
    return base


# --- positive controls -----------------------------------------------------


def test_loads_canonical_pins():
    persona = load_persona(CANONICAL)
    assert isinstance(persona, PersonaIdentity)
    assert persona.name == "Naya"
    assert "AI operating partner" in persona.character
    assert persona.tone == ("warm", "direct", "enthusiastic", "truthful", "practical", "clear")
    assert persona.canonical_status == "CANDIDATE"
    assert persona.conflicts == ()


def test_seat_is_designation_not_identity():
    persona = load_persona(CANONICAL)
    rendered = present_identity(persona, seat="naya-4")
    assert "I am Naya" in rendered
    assert "naya-4" in rendered
    assert "not my identity" in rendered
    # the durable identity itself is untouched by the seat
    assert persona.name == "Naya"


def test_dictation_variants_resolve_to_naya():
    for variant in ("Maya", "Mia", "Abby", "maya", "MIA"):
        assert normalize_dictation_name(variant, addressed_to_naya=True) == "Naya"


def test_dictation_rule_does_not_rewrite_other_names():
    assert normalize_dictation_name("Shawn", addressed_to_naya=True) == "Shawn"
    assert normalize_dictation_name("Maya", addressed_to_naya=False) == "Maya"


def test_conflicting_source_loses_and_is_recorded(tmp_path):
    rival = _write(
        tmp_path,
        "rival.json",
        _canonical_payload(
            ai_view={
                "name": "Maya",
                "character": "a helpful assistant",
                "tone": ["cheerful"],
                "seat_semantics": "naya-1..naya-5 are identities",
                "helpfulness": "",
                "visual_identity": "",
                "dictation_rule": "",
            }
        ),
    )
    persona = load_persona(CANONICAL, extra_sources=(rival,))
    # canonical wins on every pinned field
    assert persona.name == "Naya"
    assert persona.tone == ("warm", "direct", "enthusiastic", "truthful", "practical", "clear")
    # conflicts are logged, never silent
    conflicted_fields = {c.field for c in persona.conflicts}
    assert {"name", "character", "tone", "seat_semantics"} <= conflicted_fields
    assert all(c.source == str(rival) for c in persona.conflicts)


def test_conflicting_must_not_via_machine_view_is_caught(tmp_path):
    # A rival that redefines must_not under machine_view (where the canonical
    # object carries it) must not evade conflict detection.
    rival = _write(
        tmp_path,
        "rival-mv.json",
        {
            "ai_view": {
                "name": "Naya",
                "character": "AI operating partner, director, integrator, continuity steward, and execution guide for Shawn Vibert",
                "tone": ["warm", "direct", "enthusiastic", "truthful", "practical", "clear"],
                "seat_semantics": "naya-1..naya-5 are seat designations (roles), never identities; a seat must never redefine durable identity",
            },
            "machine_view": {"must_not": ["nothing"]},
        },
    )
    persona = load_persona(CANONICAL, extra_sources=(rival,))
    assert {c.field for c in persona.conflicts} == {"must_not"}
    assert "fabricate identity" in persona.must_not  # canonical wins


def test_missing_extra_source_is_not_a_failure(tmp_path):
    persona = load_persona(CANONICAL, extra_sources=(tmp_path / "nope.json",))
    assert persona.name == "Naya"
    assert persona.conflicts == ()


# --- negative controls -----------------------------------------------------


def test_missing_canonical_source_halts(tmp_path):
    with pytest.raises(PersonaSourceMissing):
        load_persona(tmp_path / "absent.json")


def test_unreadable_canonical_source_halts(tmp_path):
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    with pytest.raises(PersonaSourceMissing):
        load_persona(broken)


def test_incomplete_canonical_source_halts(tmp_path):
    thin = _write(tmp_path, "thin.json", {"ai_view": {"name": "Naya"}})
    with pytest.raises(PersonaSourceMissing):
        load_persona(thin)


def test_mutated_canonical_pin_is_detected_not_absorbed(tmp_path):
    # negative control: if the canonical file itself is tampered with, the
    # loader surfaces the tampered value (it does not silently "fix" it) --
    # tamper-evidence belongs to review, not to silent correction.
    tampered = _write(
        tmp_path,
        "tampered.json",
        _canonical_payload(
            ai_view={
                "name": "Someone Else",
                "character": "x",
                "tone": ["flat"],
                "seat_semantics": "y",
            }
        ),
    )
    persona = load_persona(tampered)
    assert persona.name == "Someone Else"  # surfaced, not corrected
