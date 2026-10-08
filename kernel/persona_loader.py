"""Deterministic persona loader for the SELF node.

Mechanical implementation of the failure states in
``BRAIN/03-KERNEL/NODES/SELF/0003-PERSONA-IDENTITY-CONTRACT-V1.md``:

- canonical persona source missing or unreadable -> raise
  :class:`PersonaSourceMissing` (halt identity presentation; never improvise
  a persona from memory);
- conflicting persona sources -> the canonical contract wins; every
  overridden field is recorded in ``PersonaIdentity.conflicts`` (prefer the
  canonical contract; log the conflict);
- a seat designation (``naya-1`` ... ``naya-5``) is a role label and is never
  absorbed into durable identity.

The canonical source is the machine-readable persona object
``BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-PERSONA-V1.json``; the human-readable
contract ``0003-PERSONA-IDENTITY-CONTRACT-V1.md`` is the authority the object
derives from. This loader never claims RATIFIED status: only Shawn ratifies.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


class PersonaLoadError(ValueError):
    """Base error for persona loading failures."""


class PersonaSourceMissing(PersonaLoadError):
    """Raised when the canonical persona source cannot be established.

    The contract's failure state is explicit: halt identity presentation;
    do not improvise a persona.
    """


@dataclass(frozen=True)
class PersonaConflict:
    """A conflicting claim from a non-canonical source that was overridden."""

    source: str
    field: str
    rejected_value: str
    reason: str = "canonical contract wins"


@dataclass(frozen=True)
class PersonaIdentity:
    """Durable persona identity pins, loaded from the canonical source."""

    name: str
    character: str
    tone: tuple[str, ...]
    helpfulness: str
    visual_identity: str
    dictation_rule: str
    seat_semantics: str
    must_not: tuple[str, ...]
    source_ref: str
    canonical_status: str
    conflicts: tuple[PersonaConflict, ...] = ()


# Fields pinned by the canonical contract; an extra source may not redefine them.
_PINNED_FIELDS = (
    "name",
    "character",
    "tone",
    "helpfulness",
    "visual_identity",
    "dictation_rule",
    "seat_semantics",
    "must_not",
)

# Dictation variants the contract pins as "read as Naya, never a rename".
_DICTATION_VARIANTS = ("maya", "mia", "abby")


def _read_json(path: Path) -> Mapping[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PersonaSourceMissing(f"canonical persona source missing: {path}") from exc
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        raise PersonaSourceMissing(f"canonical persona source unreadable: {path}: {exc}") from exc


def _require_ai_view(obj: Mapping[str, Any], source: str) -> Mapping[str, Any]:
    ai = obj.get("ai_view")
    if not isinstance(ai, dict):
        raise PersonaSourceMissing(f"persona source has no ai_view block: {source}")
    missing = [f for f in ("name", "character", "tone", "seat_semantics") if not ai.get(f)]
    if missing:
        raise PersonaSourceMissing(
            f"persona source missing required pins {missing}: {source}"
        )
    return ai


def _as_tuple(value: Any) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(v) for v in value)
    return (str(value),)


def _identity_from_object(obj: Mapping[str, Any], source: str) -> PersonaIdentity:
    ai = _require_ai_view(obj, source)
    return PersonaIdentity(
        name=str(ai["name"]),
        character=str(ai["character"]),
        tone=_as_tuple(ai["tone"]),
        helpfulness=str(ai.get("helpfulness", "")),
        visual_identity=str(ai.get("visual_identity", "")),
        dictation_rule=str(ai.get("dictation_rule", "")),
        seat_semantics=str(ai["seat_semantics"]),
        must_not=_as_tuple(obj.get("machine_view", {}).get("must_not", ())),
        source_ref=str(obj.get("machine_view", {}).get("contract", source)),
        canonical_status=str(obj.get("canonical_status", "UNKNOWN")),
    )


def _pinned_values(identity: PersonaIdentity) -> dict[str, Any]:
    return {
        "name": identity.name,
        "character": identity.character,
        "tone": list(identity.tone),
        "helpfulness": identity.helpfulness,
        "visual_identity": identity.visual_identity,
        "dictation_rule": identity.dictation_rule,
        "seat_semantics": identity.seat_semantics,
        "must_not": list(identity.must_not),
    }


def _normalize(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def load_persona(
    canonical_path: str | Path,
    extra_sources: tuple[str | Path, ...] = (),
) -> PersonaIdentity:
    """Load the canonical persona identity.

    ``canonical_path`` must point at the canonical persona object JSON.
    ``extra_sources`` are optional additional persona files; where any of them
    disagrees with the canonical pins on a pinned field, the canonical value
    wins and the disagreement is recorded in ``PersonaIdentity.conflicts``.

    Raises :class:`PersonaSourceMissing` when the canonical source cannot be
    established -- the caller must halt identity presentation, never improvise.
    """
    canonical_path = Path(canonical_path)
    obj = _read_json(canonical_path)
    identity = _identity_from_object(obj, str(canonical_path))
    pinned = _pinned_values(identity)

    conflicts: list[PersonaConflict] = []
    for extra in extra_sources:
        extra_path = Path(extra)
        if not extra_path.exists():
            continue  # optional overlay; absence is not a failure
        try:
            other = json.loads(extra_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            conflicts.append(
                PersonaConflict(
                    source=str(extra_path),
                    field="<unparseable>",
                    rejected_value="<unparseable>",
                    reason="source unreadable; canonical contract wins",
                )
            )
            continue
        other_ai = other.get("ai_view") if isinstance(other, dict) else None
        if not isinstance(other_ai, dict):
            continue
        # Pinned fields live in ai_view, except must_not which the canonical
        # object carries under machine_view -- check both locations so a rival
        # cannot evade conflict detection by redefining must_not elsewhere.
        other_pins: dict[str, Any] = dict(other_ai)
        other_machine = other.get("machine_view")
        if isinstance(other_machine, dict) and "must_not" in other_machine:
            other_pins["must_not"] = other_machine["must_not"]
        for pinned_field in _PINNED_FIELDS:
            if pinned_field not in other_pins:
                continue
            if _normalize(other_pins[pinned_field]) != _normalize(pinned[pinned_field]):
                conflicts.append(
                    PersonaConflict(
                        source=str(extra_path),
                        field=pinned_field,
                        rejected_value=_normalize(other_pins[pinned_field]),
                    )
                )

    return PersonaIdentity(
        name=identity.name,
        character=identity.character,
        tone=identity.tone,
        helpfulness=identity.helpfulness,
        visual_identity=identity.visual_identity,
        dictation_rule=identity.dictation_rule,
        seat_semantics=identity.seat_semantics,
        must_not=identity.must_not,
        source_ref=identity.source_ref,
        canonical_status=identity.canonical_status,
        conflicts=tuple(conflicts),
    )


def normalize_dictation_name(raw: str, addressed_to_naya: bool) -> str:
    """Apply the contract's dictation rule mechanically.

    When context shows Shawn is addressing Naya, transcription variants
    (``Maya``, ``Mia``, ``Abby``) resolve to ``Naya`` -- never a rename.
    Otherwise the raw token is returned unchanged.
    """
    if addressed_to_naya and raw.strip().lower() in _DICTATION_VARIANTS:
        return "Naya"
    return raw


def present_identity(persona: PersonaIdentity, seat: str | None = None) -> str:
    """Render an identity presentation string.

    The seat designation, when given, is rendered strictly as a role the
    persona operates from -- it is never merged into the durable identity.
    """
    base = (
        f"I am {persona.name}, {persona.character}. "
        f"My tone is {', '.join(persona.tone)}."
    )
    if seat:
        base += f" I am operating from seat {seat} -- a role designation, not my identity."
    return base
