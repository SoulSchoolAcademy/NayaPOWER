"""Demo-1 LAW authorization: proposal -> LawNode.gate() -> envelope.

No new architecture. This module only wires existing contracts:
  - the LAW grant schema (law_node._validate_claim),
  - LawNode.gate() with its four-valued verdicts and ADMISSIBLE envelope,
  - the canonical Smart Door registry declaration as the capability source.

The grant itself is TRANSCRIBED from the director's written orders
(see demo_grant.json provenance). Naya 4 creates no authority; this module
encodes Shawn's.

Constitution pin: the SHA-256 of CONSTITUTION/0000-NAYAPOWER-CONSTITUTION-ACT-V1.md
as it exists at authorization time. The receipt records the hash, so any later
change to the constitution is detectable from the receipt. Fail-closed: an
unreadable constitution refuses authorization.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict

from naya_kernel.nodes import law_node

_HERE = Path(__file__).resolve().parent
GRANT_PATH = _HERE / "demo_grant.json"
CONSTITUTION_PATH = (
    _HERE.parent.parent / "CONSTITUTION" / "0000-NAYAPOWER-CONSTITUTION-ACT-V1.md"
)

# Vocabulary join (documented, demo-scoped): the registry operation declares
# authority_action "staging_write"; LAW grants match scope[] against
# action.scope_tag. This table joins them. It is data, not architecture.
AUTHORITY_ACTION_TO_SCOPE_TAG = {
    "staging_write": "staging_write_demo",
}

PROPOSER = "naya4-demo-runner"


class AuthorizationRefused(Exception):
    """LawNode.gate() did not reach ADMISSIBLE. The reasons are the evidence."""


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_grant(grant_path: Path | str = GRANT_PATH) -> Dict[str, Any]:
    grant = json.loads(Path(grant_path).read_text(encoding="utf-8"))
    if grant.get("revoked"):
        raise AuthorizationRefused(
            "grant %r is revoked — the director revoked it; no proposal is built"
            % grant.get("grant_ref")
        )
    return grant


def constitution_pin() -> Dict[str, str]:
    """Content-address the constitution as it exists right now."""
    if not CONSTITUTION_PATH.is_file():
        raise AuthorizationRefused(
            "constitution unreadable at %s — authorization fails closed"
            % CONSTITUTION_PATH
        )
    digest = _sha256_file(CONSTITUTION_PATH)
    return {"pinned_hash": digest, "path": str(CONSTITUTION_PATH)}


def build_proposal(grant: Dict[str, Any], filename: str,
                   content: bytes) -> Dict[str, Any]:
    """Build the LAW proposal for one demo staging write.

    The action's bounds come from the GRANT (authority), not from the
    caller's wishes. The caller supplies only the specific filename and
    content; everything bounding it is authority-derived.
    """
    bounds = grant.get("bounds") or {}
    scope_tag = (grant.get("scope") or [None])[0]
    pin = constitution_pin()
    return {
        "proposalId": "prop-demo1-%s" % grant["grant_ref"],
        "intent": ("Demo-1 real-effect: write one Smart Note candidate file "
                   "into the bounded staging area, observed and receipted."),
        "action": {
            "type": "staging.write_file",
            "scope_tag": scope_tag,
            "action_class": "WRITE_SCOPED",
            "targets": [bounds.get("target")],
            "bounds": {
                "target": bounds.get("target"),
                "filename": bounds.get("filename"),
                "max_bytes": bounds.get("max_bytes"),
                "overwrite": bounds.get("overwrite", False),
                "requested_filename": filename,
                "requested_bytes": len(content),
            },
        },
        "proposedBy": PROPOSER,
        "authorityClaim": {
            "grant_ref": grant["grant_ref"],
            "grantor": grant["grantor"],
        },
        "evidenceRefs": [
            "demo_grant.json (transcribed director order)",
            "canonical Smart Door registry: DOOR-LOCAL-STAGING/staging.write_file",
            "director's written orders (master directive 2026-10-01; dispatch 2026-10-01 09:32 PDT)",
        ],
        "stakes": "low",
        "reversibility": 1.0,
        "identityContext": {"runner": PROPOSER, "lane": "naya4"},
        "constitutionHash": pin["pinned_hash"],
        "flags": {},
        "material_facts_version": 1,
    }


def authorize(filename: str, content: bytes,
              grant_path: Path | str = GRANT_PATH) -> Dict[str, Any]:
    """Run the demo proposal through the real LAW gate.

    Returns the ADMISSIBLE envelope. Raises AuthorizationRefused otherwise —
    and the refusal reasons name exactly what failed, so a cold reader can
    see whether it was authority, evidence, or a hard stop.
    """
    grant = load_grant(grant_path)
    if grant.get("grantee") != PROPOSER:
        raise AuthorizationRefused(
            "grant %r names grantee %r, not this runner %r"
            % (grant.get("grant_ref"), grant.get("grantee"), PROPOSER)
        )
    proposal = build_proposal(grant, filename, content)
    pin = constitution_pin()
    state = {
        "proposal": proposal,
        "constitution_store": {
            "pinned_hash": pin["pinned_hash"],
            "corpus": {pin["pinned_hash"]: pin["path"]},
            "reachable": True,
        },
        "grants": [grant],
        "evidence": {
            "n": len(proposal["evidenceRefs"]),
            "confidence": 0.9,
        },
        "evidence_floor_k": 3,
        "seen_proposal_hashes": {},
    }
    law = law_node.LawNode()
    result = law.gate(state)
    receipt = law.last_receipt or {}
    if receipt.get("gate") != "ADMISSIBLE":
        raise AuthorizationRefused(
            "LawNode.gate() reached %s, not ADMISSIBLE: %s"
            % (receipt.get("gate"), "; ".join(result.reasons))
        )
    envelope = receipt.get("envelope") or {}
    return {
        "envelope": envelope,
        "gate_receipt_id": receipt.get("receipt_id"),
        "authority_basis": {
            "kind": "director_order",
            "ref": grant["grant_ref"],
            "revoked": False,
        },
        "grant": grant,
        "constitution_hash": pin["pinned_hash"],
    }
