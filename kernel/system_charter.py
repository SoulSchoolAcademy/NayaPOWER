"""Ratification-gated compiler for the NayaPOWER System Charter.

This module does not create a tenth node or a second authority system.
It validates and compiles the human charter into directives for the existing
SELF→LAW→ACT→KNOW→PROVE→CONNECT→VERIFY→LEARN→EVOLVE organism.

Candidate charter material may be inspected and tested, but it cannot govern
runtime behavior until the Human Director ratifies the exact version.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

from kernel.runtime_boot import CANONICAL_NODE_NAMES, find_repository_root

CONTRACT_PATH = Path("BRAIN/03-KERNEL/0006-SYSTEM-CHARTER-MACHINE-CONTRACT-V1.json")
VALUE_CALCULUS_ID = "NAYA-DECISION-VALUE-CALCULUS-V2.1"
ACTIVE_STATUS = "RATIFIED_ACTIVE"
CANDIDATE_STATUS = "CANDIDATE_NON_GOVERNING"

class CharterContractError(RuntimeError):
    pass

def load_system_charter(root: Path | None = None) -> dict:
    repo = find_repository_root(root)
    path = repo / CONTRACT_PATH
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CharterContractError(f"system charter machine contract missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CharterContractError(f"invalid system charter JSON: {path}") from exc
    validate_system_charter(doc)
    return doc

def validate_system_charter(doc: dict) -> None:
    if doc.get("schema") != "naya.system-charter.machine.v1":
        raise CharterContractError("SYSTEM_CHARTER_SCHEMA_INVALID")
    if doc.get("contract_id") != "NAYAPOWER-SYSTEM-CHARTER-V1":
        raise CharterContractError("SYSTEM_CHARTER_ID_INVALID")
    if doc.get("status") not in {CANDIDATE_STATUS, ACTIVE_STATUS, "SUPERSEDED", "RETIRED"}:
        raise CharterContractError("SYSTEM_CHARTER_STATUS_INVALID")

    laws = doc.get("laws") or []
    ids = [law.get("id") for law in laws]
    if ids != list(range(1, 13)):
        raise CharterContractError("SYSTEM_CHARTER_MUST_HAVE_EXACT_12_LAWS")

    known_nodes = set(CANONICAL_NODE_NAMES)
    bindings = doc.get("node_bindings") or {}
    if set(bindings) != known_nodes:
        raise CharterContractError("SYSTEM_CHARTER_MUST_BIND_EXACT_NINE_NODES")

    covered = set()
    for law in laws:
        nodes = law.get("nodes") or []
        if not nodes or any(node not in known_nodes for node in nodes):
            raise CharterContractError(f"SYSTEM_CHARTER_LAW_NODE_BINDING_INVALID:{law.get('id')}")
        covered.update(nodes)
    if covered != known_nodes:
        raise CharterContractError("SYSTEM_CHARTER_LAWS_DO_NOT_COVER_ALL_NODES")

    for node in CANONICAL_NODE_NAMES:
        binding = bindings[node]
        if sorted(binding.get("laws") or []) != sorted(
            law["id"] for law in laws if node in law["nodes"]
        ):
            raise CharterContractError(f"SYSTEM_CHARTER_NODE_LAW_DRIFT:{node}")
        if not binding.get("must") or not binding.get("must_not"):
            raise CharterContractError(f"SYSTEM_CHARTER_NODE_BEHAVIOR_INCOMPLETE:{node}")

    objective = doc.get("objective") or {}
    if objective.get("decision_system") != VALUE_CALCULUS_ID:
        raise CharterContractError("SYSTEM_CHARTER_MUST_USE_SHARED_VALUE_CALCULUS")
    if set(objective.get("decision_outcomes") or []) != {"ACT","READ_MORE","ASK","REFUSE"}:
        raise CharterContractError("SYSTEM_CHARTER_DECISION_OUTCOMES_INVALID")

    authority = doc.get("authority") or {}
    activation = doc.get("activation") or {}
    governing = (
        doc.get("status") == ACTIVE_STATUS
        and authority.get("ratified") is True
        and bool(authority.get("ratification_receipt"))
        and activation.get("runtime_enabled") is True
    )
    if activation.get("runtime_enabled") and not governing:
        raise CharterContractError("SYSTEM_CHARTER_CANNOT_ACTIVATE_WITHOUT_RATIFICATION")

    hard = set(doc.get("hard_stops") or [])
    if hard != {"HARM_PEOPLE","BREAK_LAW","DESTROY_EVIDENCE","BREAK_TRUST"}:
        raise CharterContractError("SYSTEM_CHARTER_HARD_STOPS_DRIFT")

    distinctions = set(doc.get("truth_distinctions") or [])
    required = {
        "UNKNOWN!=VERIFIED","BLOCKED!=PASS","IMPLEMENTED!=VERIFIED",
        "VERIFIED!=PRODUCTION_PROVEN","RECEIPT!=OUTCOME","STORED!=LEARNED",
        "RETRIEVED!=UNDERSTOOD","APPLIED!=CAUSALLY_IMPROVED",
        "CAPABILITY!=AUTHORITY","RETRIEVAL!=AUTHORITY","CONTINUITY!=AUTHORITY",
    }
    if not required.issubset(distinctions):
        raise CharterContractError("SYSTEM_CHARTER_TRUTH_DISTINCTIONS_INCOMPLETE")

def charter_is_governing(doc: dict) -> bool:
    validate_system_charter(doc)
    return (
        doc["status"] == ACTIVE_STATUS
        and doc["authority"]["ratified"] is True
        and bool(doc["authority"]["ratification_receipt"])
        and doc["activation"]["runtime_enabled"] is True
    )

def compile_node_directive(doc: dict, node_name: str, *, require_governing: bool = True) -> dict:
    validate_system_charter(doc)
    if node_name not in CANONICAL_NODE_NAMES:
        raise CharterContractError(f"UNKNOWN_NINE_NODE:{node_name}")
    governing = charter_is_governing(doc)
    if require_governing and not governing:
        raise CharterContractError("SYSTEM_CHARTER_NOT_RATIFIED_ACTIVE")
    binding = doc["node_bindings"][node_name]
    laws = {law["id"]: law for law in doc["laws"]}
    return {
        "schema":"naya.system-charter.node-directive.v1",
        "contract_id":doc["contract_id"],
        "contract_version":doc["version"],
        "governing":governing,
        "node":node_name,
        "objective":copy.deepcopy(doc["objective"]),
        "laws":[copy.deepcopy(laws[i]) for i in binding["laws"]],
        "purpose":binding["purpose"],
        "consumes":copy.deepcopy(binding["consumes"]),
        "must":copy.deepcopy(binding["must"]),
        "must_not":copy.deepcopy(binding["must_not"]),
        "hard_stops":copy.deepcopy(doc["hard_stops"]),
        "truth_distinctions":copy.deepcopy(doc["truth_distinctions"]),
        "privacy_rule":doc["privacy_rule"],
        "proof_ladder":copy.deepcopy(doc["proof_ladder"]),
    }

def simulate_ratification(doc: dict, receipt: str = "TEST-RATIFICATION-RECEIPT") -> dict:
    """Test helper: returns an activated copy without mutating canonical bytes."""
    candidate = copy.deepcopy(doc)
    candidate["status"] = ACTIVE_STATUS
    candidate["authority"]["ratified"] = True
    candidate["authority"]["ratification_receipt"] = receipt
    candidate["activation"]["runtime_enabled"] = True
    validate_system_charter(candidate)
    return candidate
