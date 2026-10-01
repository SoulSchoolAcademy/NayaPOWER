#!/usr/bin/env python3
"""Validate BRAIN/03-KERNEL/0005-NINE-NODE-ACTIVATION-LADDER-V1.json.

Fail-closed rules (UNKNOWN != PASS):
  - rung claims are only honored when the evidence tier the rung requires is
    named in the node entry; missing evidence -> rung stays where evidence stops.
  - evidence must cover the full ladder prefix: a UNIT claim without named
    STRUCTURAL+CONTRACT evidence is rejected.
  - no fractional/manufactured rungs: current_rung must be exactly one of the
    eight ladder rungs from the organism contract.
  - missing_rung must be exactly the next rung above current_rung (or the file
    must state SUCCESSOR is terminal).
  - status must remain PROPOSED_CANONICAL until human-director ratification
    (issue #864); CANONICAL is rejected here.
Usage: python3 tools/validate_nine_node_activation_ladder.py
Exit 0 when the tracker is internally consistent and evidence-bound.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "BRAIN/03-KERNEL/0005-NINE-NODE-ACTIVATION-LADDER-V1.json"

SCHEMA = "naya.nine-node-activation-ladder.v1"
ALLOWED_STATUSES = {"PROPOSED_CANONICAL"}
EXPECTED_ORDER = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
LADDER = ["STRUCTURAL", "CONTRACT", "UNIT", "INTEGRATION", "BEHAVIORAL", "OUTCOME", "PRODUCTION", "SUCCESSOR"]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def failures(data):
    out = []
    if data.get("schema") != SCHEMA:
        out.append(f"SCHEMA_MISMATCH: {data.get('schema')!r} != {SCHEMA!r}")
    if data.get("status") not in ALLOWED_STATUSES:
        out.append(f"STATUS_NOT_PROPOSED_CANONICAL: {data.get('status')!r}")
    if data.get("proof_ladder") != LADDER:
        out.append("PROOF_LADDER_MISMATCH: ladder must equal the organism contract rungs")
    order = data.get("node_order") or []
    if order != EXPECTED_ORDER:
        out.append(f"NODE_ORDER_MISMATCH: {order!r} != {EXPECTED_ORDER!r}")
    if not SHA_RE.match(str(data.get("as_of") or "")):
        out.append(f"AS_OF_NOT_PINNED_SHA: {data.get('as_of')!r}")
    tiers = data.get("rung_evidence_tiers") or {}
    for rung in LADDER:
        if rung not in tiers:
            out.append(f"TIER_RULE_MISSING: no evidence tier defined for rung {rung}")
    nodes = data.get("nodes") or {}
    if list(nodes.keys()) != EXPECTED_ORDER:
        out.append(f"NODE_KEYS_MISMATCH: {list(nodes.keys())!r} != {EXPECTED_ORDER!r}")
    for name, node in nodes.items():
        rung = node.get("current_rung")
        # No manufactured tenths: exact ladder membership only.
        if rung not in LADDER:
            out.append(f"{name}: INVALID_RUNG: {rung!r} not in proof ladder")
            continue
        idx = LADDER.index(rung)
        evidence = node.get("evidence") or {}
        # Ladder-prefix rule: every rung up to and including the claim needs refs.
        for lower in LADDER[: idx + 1]:
            refs = evidence.get(lower)
            if not refs or not isinstance(refs, list) or not all(isinstance(r, str) and r.strip() for r in refs):
                out.append(f"{name}: EVIDENCE_MISSING_FOR_RUNG {lower}: rung {rung} claim has no named evidence")
        # missing_rung must be exactly the next rung (terminal SUCCESSOR allowed).
        expected_missing = None if rung == "SUCCESSOR" else LADDER[idx + 1]
        if node.get("missing_rung") != expected_missing:
            out.append(f"{name}: MISSING_RUNG_WRONG: {node.get('missing_rung')!r} != {expected_missing!r}")
        if not node.get("node_id"):
            out.append(f"{name}: NODE_ID_MISSING")
        if not (node.get("next_proof") or "").strip():
            out.append(f"{name}: NEXT_PROOF_MISSING")
    return out


def main() -> int:
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on unreadable fixture
        print(json.dumps({"schema": "naya.nine-node-activation-ladder.validation-report",
                          "failures": [f"FIXTURE_UNREADABLE: {exc}"], "passed": False}, indent=2))
        return 1
    fails = failures(data)
    print(json.dumps({"schema": "naya.nine-node-activation-ladder.validation-report",
                      "as_of": data.get("as_of"), "failures": fails, "passed": not fails}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
