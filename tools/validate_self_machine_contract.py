#!/usr/bin/env python3
"""Validate BRAIN/03-KERNEL/NODES/SELF/0003-SELF-MACHINE-CONTRACT-V1.json.

Fail-closed rules (UNKNOWN != PASS):
  - loop stage claims are only honored when the evidence each stage's gate
    requires is present; missing evidence -> the stage claim is rejected.
  - stage_history must equal loop_stages[0..index(loop_stage)] exactly:
    forward-only, one stage at a time, no skips, no backward moves.
  - state transitions: only the listed legal transitions; FAILED is terminal.
  - identity is never inferred: ESTABLISH requires an explicit attestation
    with actor_id, system_id, and a schema-enum role; display names are
    not evidence of identity.
  - successor packets transfer intelligence, never authority:
    authority_transferred must be explicitly false.
  - missing or corrupt continuity fails closed (no assumed restore).
  - status must remain PROPOSED_CANONICAL until human-director
    ratification; CANONICAL is rejected here.
  - checkpoints must be content-addressed (CHK- + 24 lowercase hex).
Usage: python3 tools/validate_self_machine_contract.py
Exit 0 when the contract file is internally consistent and evidence-bound.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "BRAIN/03-KERNEL/NODES/SELF/0003-SELF-MACHINE-CONTRACT-V1.json"

SCHEMA = "naya.self-machine-contract.v1"
NODE_ID = "NAYA-KERNEL-SELF"
ALLOWED_STATUSES = {"PROPOSED_CANONICAL"}
STAGES = ["ESTABLISH", "RESTORE", "UNDERSTAND", "REMEMBER",
          "REFLECT", "PRESERVE", "HAND_OFF", "CONTINUE"]
STATES = ["UNINITIALIZED", "BOOTING", "READY", "DEGRADED", "FAILED"]
ROLES = ["naya", "human", "agent", "service"]
SUCCESSOR_PACKET_SCHEMA = "naya.self.successor.v2"
BOOT_RECEIPT_SCHEMA = "naya.self.boot-receipt.v2"
CHECKPOINT_RE = re.compile(r"^CHK-[0-9a-f]{24}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

REQUIRED_TOP_KEYS = {
    "parent_contracts", "purpose", "scope", "identity_law", "authority_law",
    "continuity_law", "state_machine", "invariants", "fail_closed_law",
    "not_claimed", "out_of_scope", "record_stage_gates", "records",
    "merged_executor_vocabulary", "governing_law",
}


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def _nonempty_str_list(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_str(v) for v in value)
    )


def _gate_failures(rid, stage, record):
    """Failures for the evidence gates up to and including `stage`."""
    out = []
    idx = STAGES.index(stage)
    gates = STAGES[: idx + 1]

    if "ESTABLISH" in gates:
        att = record.get("identity_attestation")
        if not isinstance(att, dict):
            out.append(f"{rid}: ESTABLISH_EVIDENCE_MISSING: identity_attestation required")
        else:
            if not _nonempty_str(att.get("actor_id")):
                out.append(f"{rid}: IDENTITY_MISSING: actor_id must be non-empty")
            if not _nonempty_str(att.get("system_id")):
                out.append(f"{rid}: IDENTITY_MISSING: system_id must be non-empty")
            if att.get("role") not in ROLES:
                out.append(
                    f"{rid}: ROLE_INVALID: role must be one of {ROLES}; "
                    "runtime identity is never inferred from display name alone"
                )
        if not _nonempty_str(record.get("mission_source")):
            out.append(f"{rid}: ESTABLISH_EVIDENCE_MISSING: mission_source required (mission is loaded, never invented)")
        if not _nonempty_str(record.get("objective")):
            out.append(f"{rid}: OBJECTIVE_MISSING: mission and objective exist before consequential work")

    if "RESTORE" in gates:
        binding = record.get("continuity_binding")
        if not isinstance(binding, dict):
            out.append(f"{rid}: RESTORE_EVIDENCE_MISSING: continuity_binding required")
        else:
            cp = binding.get("checkpoint_id")
            fresh = binding.get("declared_fresh")
            has_cp = _nonempty_str(cp) and CHECKPOINT_RE.match(cp)
            has_fresh = fresh is True and _nonempty_str(binding.get("fresh_reason"))
            if not (has_cp or has_fresh):
                out.append(
                    f"{rid}: CONTINUITY_UNBOUND: continuity_binding needs a "
                    "content-addressed checkpoint_id or a declared fresh start with reason"
                )

    if "UNDERSTAND" in gates:
        boundary = record.get("known_unknown_boundary")
        if not isinstance(boundary, dict):
            out.append(f"{rid}: UNDERSTAND_EVIDENCE_MISSING: known_unknown_boundary required")
        else:
            for key in ("known", "unknown", "blocked"):
                if not isinstance(boundary.get(key), list):
                    out.append(f"{rid}: BOUNDARY_NOT_EXPLICIT: known_unknown_boundary.{key} must be a list")

    if "REMEMBER" in gates:
        if record.get("experience_preserved") is not True:
            out.append(f"{rid}: REMEMBER_EVIDENCE_MISSING: experience_preserved must be true")
        if not _nonempty_str(record.get("experience_ref")):
            out.append(f"{rid}: REMEMBER_EVIDENCE_MISSING: experience_ref required")

    if "REFLECT" in gates:
        if not _nonempty_str_list(record.get("audit_trail")):
            out.append(f"{rid}: REFLECT_EVIDENCE_MISSING: audit_trail must be a non-empty list of non-empty strings")

    if "PRESERVE" in gates:
        cp = record.get("checkpoint_id")
        if not _nonempty_str(cp) or not CHECKPOINT_RE.match(cp):
            out.append(f"{rid}: CHECKPOINT_NOT_CONTENT_ADDRESSED: checkpoint_id must match CHK-[0-9a-f]{{24}}")

    if "HAND_OFF" in gates:
        pkt = record.get("successor_packet")
        if not isinstance(pkt, dict):
            out.append(f"{rid}: HAND_OFF_EVIDENCE_MISSING: successor_packet required")
        else:
            if pkt.get("schema") != SUCCESSOR_PACKET_SCHEMA:
                out.append(f"{rid}: SUCCESSOR_PACKET_SCHEMA_MISMATCH: schema must be {SUCCESSOR_PACKET_SCHEMA!r}")
            if not _nonempty_str(pkt.get("predecessor_id")):
                out.append(f"{rid}: SUCCESSOR_PACKET_INCOMPLETE: predecessor_id required")
            if not _nonempty_str(pkt.get("system_id")):
                out.append(f"{rid}: SUCCESSOR_PACKET_INCOMPLETE: system_id required")
            if pkt.get("authority_transferred") is not False:
                out.append(
                    f"{rid}: AUTHORITY_CLAIM_REJECTED: successor_packet.authority_transferred "
                    "must be false — successor context never creates authority"
                )

    if "CONTINUE" in gates:
        if not _nonempty_str_list(record.get("inherited_intelligence")):
            out.append(f"{rid}: CONTINUE_EVIDENCE_MISSING: inherited_intelligence must be a non-empty list")
        if not _nonempty_str(record.get("proof_ref")):
            out.append(f"{rid}: CONTINUE_EVIDENCE_MISSING: proof_ref required — continuity requires a legitimate binding")

    return out


def _record_failures(rid, record):
    out = []
    stage = record.get("loop_stage")
    if stage not in STAGES:
        out.append(f"{rid}: LOOP_STAGE_INVALID: {stage!r} not in the north-star loop")
        return out
    idx = STAGES.index(stage)
    expected_history = STAGES[: idx + 1]
    if record.get("stage_history") != expected_history:
        out.append(
            f"{rid}: STAGE_HISTORY_INVALID: {record.get('stage_history')!r} "
            f"!= {expected_history!r} (forward-only, no skips, no backward)"
        )
    out.extend(_gate_failures(rid, stage, record))
    return out


def failures(data):
    out = []
    if data.get("schema") != SCHEMA:
        out.append(f"SCHEMA_MISMATCH: {data.get('schema')!r} != {SCHEMA!r}")
    if data.get("node_id") != NODE_ID:
        out.append(f"NODE_ID_MISMATCH: {data.get('node_id')!r} != {NODE_ID!r}")
    if data.get("status") not in ALLOWED_STATUSES:
        out.append(
            f"STATUS_NOT_PROPOSED_CANONICAL: {data.get('status')!r} "
            "(CANONICAL requires human-director ratification)"
        )
    if data.get("loop_stages") != STAGES:
        out.append(
            f"LOOP_ORDER_MISMATCH: {data.get('loop_stages')!r} != {STAGES!r} "
            "(north-star loop order is fixed by contract V2)"
        )
    if not SHA_RE.match(str(data.get("as_of") or "")):
        out.append(f"AS_OF_NOT_PINNED_SHA: {data.get('as_of')!r}")

    missing = REQUIRED_TOP_KEYS - set(data.keys())
    if missing:
        out.append(f"REQUIRED_SECTIONS_MISSING: {sorted(missing)}")

    if data.get("roles") != ROLES:
        out.append(f"ROLES_MISMATCH: {data.get('roles')!r} != {ROLES!r} (roles come from SELF-NODE-SCHEMA.json)")

    invariants = data.get("invariants")
    if not isinstance(invariants, list) or len(invariants) != 12:
        out.append(f"INVARIANTS_NOT_TWELVE: found {len(invariants) if isinstance(invariants, list) else invariants!r}")
    else:
        ids = [inv.get("id") for inv in invariants]
        if len(set(ids)) != 12 or any(not _nonempty_str(i) for i in ids):
            out.append("INVARIANT_IDS_INVALID: 12 unique non-empty invariant ids required")
        if any(not _nonempty_str(inv.get("statement")) for inv in invariants):
            out.append("INVARIANT_STATEMENT_MISSING: every invariant needs a non-empty statement")

    sm = data.get("state_machine")
    if not isinstance(sm, dict):
        out.append("STATE_MACHINE_NOT_AN_OBJECT")
    else:
        if sm.get("states") != STATES:
            out.append(f"STATES_MISMATCH: {sm.get('states')!r} != {STATES!r} (states come from SELF-NODE-SCHEMA.json)")
        transitions = sm.get("legal_transitions")
        if not isinstance(transitions, list) or not transitions:
            out.append("LEGAL_TRANSITIONS_MISSING: state machine must enumerate its legal transitions")
        else:
            for t in transitions:
                if t.get("from") not in STATES or t.get("to") not in STATES:
                    out.append(f"TRANSITION_UNKNOWN_STATE: {t!r} references a state outside the schema states")
                if not _nonempty_str(t.get("on")):
                    out.append(f"TRANSITION_NO_GUARD: {t!r} needs a named transition guard")

    vocab = data.get("merged_executor_vocabulary") or {}
    codes = vocab.get("error_codes")
    if not _nonempty_str_list(codes):
        out.append("ERROR_CODES_MISSING: the merged executor's SelfNodeError vocabulary must be bound here")

    records = data.get("records")
    if not isinstance(records, list):
        out.append("RECORDS_NOT_A_LIST")
        return out
    seen = set()
    for i, record in enumerate(records):
        if not isinstance(record, dict):
            out.append(f"RECORD_{i}_NOT_AN_OBJECT")
            continue
        rid = record.get("record_id")
        if not _nonempty_str(rid):
            out.append(f"RECORD_{i}: RECORD_ID_MISSING")
            rid = f"RECORD_{i}"
        if rid in seen:
            out.append(f"{rid}: RECORD_ID_DUPLICATE")
        seen.add(rid)
        out.extend(_record_failures(rid, record))
    return out


def main() -> int:
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on unreadable fixture
        print(json.dumps({"schema": "naya.self-machine-contract.validation-report",
                          "failures": [f"FIXTURE_UNREADABLE: {exc}"],
                          "passed": False}, indent=2))
        return 1
    fails = failures(data)
    print(json.dumps({"schema": "naya.self-machine-contract.validation-report",
                      "as_of": data.get("as_of"), "failures": fails,
                      "passed": not fails}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
