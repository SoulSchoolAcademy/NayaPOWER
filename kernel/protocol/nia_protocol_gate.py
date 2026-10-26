#!/usr/bin/env python3
"""NIA Protocol V1 integrity gate.

This is NOT a second decision engine and grants no authority. It binds the
new behavioral contract to the existing cold-start gate; the actual decision,
authority, scorecard, action, verification and completion checks remain in
their already-canonical modules.

Any change to the NIA human or machine contract requires a deliberate,
reviewed re-pin here. A second document or silent in-place rewrite cannot
quietly alter the behavior a new Naya loads.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = {
    "GOVERNANCE/NIA-PROTOCOL-V1.md": "6841f6b7225ffb97305e640cdb2a2e4834a11b87afbdd713e0f7f6c62e745e04",
    "GOVERNANCE/NIA-PROTOCOL-V1.json": "9b6603b76efc0b3a4b503c4c9d9ddd6c8b3f9c339d8bebcf6265d4d2a1653949",
}
CONSTITUTION = "CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md"
REQUIRED_FIELDS = (
    "name", "version", "classification", "amends_constitution",
    "authority_chain", "protocol_steps", "decision_record_fields",
    "must", "must_not", "team_law", "stop_conditions", "conflict_order",
)
DECISION_FIELDS = ("WHO", "WHAT", "WHY", "SCOPE", "AUTHORITY",
                   "CONSTRAINTS", "EVIDENCE", "AFTER")
PROTECTED_MEANING = (
    "Treat capability as authority",
    "Ask the Director for a logic decision",
    "Present theory as finding",
)


def check_contract(root: Path = ROOT) -> tuple[bool, str]:
    """Fail closed on missing, altered or internally contradictory protocol."""
    base = Path(root)
    for relative, expected in CONTRACTS.items():
        try:
            raw = (base / relative).read_bytes()
        except OSError as exc:
            return False, f"NIA contract missing/unreadable: {relative}: {exc}"
        actual = hashlib.sha256(raw).hexdigest()
        if actual != expected:
            return False, f"NIA contract changed without governed re-pin: {relative}"
    if not (base / CONSTITUTION).is_file():
        return False, "NIA constitutional parent missing"
    if not (base / "PROTOCOL.md").is_file():
        return False, "canonical PROTOCOL.md missing"

    try:
        data = json.loads((base / "GOVERNANCE/NIA-PROTOCOL-V1.json").read_text(
            encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        return False, f"NIA machine contract unreadable: {exc}"
    if not isinstance(data, dict):
        return False, "NIA machine contract must be an object"
    missing = [key for key in REQUIRED_FIELDS if key not in data]
    if missing:
        return False, f"NIA contract missing fields: {missing}"
    if (data["name"], data["version"], data["classification"]) != (
        "NIA Protocol", "V1", "CONTRACT"
    ):
        return False, "NIA identity/version/classification changed"
    if data["amends_constitution"] is not False:
        return False, "NIA cannot self-amend the constitution"
    chain = data["authority_chain"]
    if not isinstance(chain, list) or len(chain) < 3 or (
        "Constitution Act V1" not in str(chain[1])
    ):
        return False, "NIA authority hierarchy invalid"
    if not isinstance(data["protocol_steps"], list) or len(data["protocol_steps"]) != 10:
        return False, "NIA ten-step behavior missing"
    if data["decision_record_fields"] != list(DECISION_FIELDS):
        return False, "NIA eight-field accountability record changed"
    if not isinstance(data["must_not"], list) or any(
        not any(meaning in entry for entry in data["must_not"])
        for meaning in PROTECTED_MEANING
    ):
        return False, "NIA no-ask / no-false-proof / no-false-authority clauses missing"
    for key in ("must", "team_law", "stop_conditions", "conflict_order"):
        if not isinstance(data[key], list) or not data[key]:
            return False, f"NIA {key} obligations missing"
    return True, "NIA Protocol V1 human+machine bytes pinned, constitutional parent and behavior invariants present"
