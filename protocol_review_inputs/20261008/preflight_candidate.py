"""Candidate, non-governing offline preflight verifier.

It only validates structure and source-content fingerprints against a trusted external
manifest supplied by a verifier. It NEVER grants permission to read, write, merge,
ratify, deploy, or execute code. A self-authored receipt is not proof of comprehension.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_UNDERSTANDING = {
    "source_of_truth": "CURRENT_MAIN_AND_MATCHED_PROOF",
    "human_authority": "HUMAN_DIRECTOR",
    "learning_threshold": "CAUSAL_OUTCOME_AND_SUCCESSOR_REUSE",
    "board_role": "COORDINATION_NOT_AUTHORITY",
    "next_action_requirement": "ONE_ADMISSIBLE_NEXT_ACTION",
}


def assess(receipt: Any, *, trusted_main: str, trusted_sources: Mapping[str, str],
           used_sessions: set[str] | None = None) -> dict[str, Any]:
    """Assess a candidate preflight attestation; never a LAW authorization.

    `trusted_main` and `trusted_sources` must be independently obtained from exact-current
    GitHub/checked-out bytes. Supplying untrusted values defeats this prototype.
    `used_sessions` is the caller's independent session registry, not a replacement for one.
    """
    errors: list[str] = []
    if not isinstance(receipt, dict):
        return {"status": "PREFLIGHT_NOT_READY", "errors": ["invalid_receipt"], "authority_granted": False}
    for key in ("actor_id", "session_id", "repository", "source_commit", "observed_at",
                "read_evidence", "understanding", "proposed_action"):
        if key not in receipt:
            errors.append("missing:" + key)
    if not HEX40.fullmatch(trusted_main or ""):
        errors.append("trusted_main_not_a_sha")
    if receipt.get("source_commit") != trusted_main:
        errors.append("stale_or_wrong_main")
    if receipt.get("repository") != "SoulSchoolAcademy/NayaPOWER":
        errors.append("wrong_repository")
    for key in ("actor_id", "session_id", "observed_at"):
        if not isinstance(receipt.get(key), str) or not receipt.get(key, "").strip():
            errors.append("invalid:" + key)
    if used_sessions is not None and receipt.get("session_id") in used_sessions:
        errors.append("reused_session")
    evidence = receipt.get("read_evidence")
    if not isinstance(evidence, dict):
        errors.append("invalid_read_evidence")
    else:
        for path, expected_hash in trusted_sources.items():
            supplied_hash = evidence.get(path)
            if supplied_hash is None:
                errors.append("missing_read:" + path)
            elif not isinstance(supplied_hash, str) or not HEX64.fullmatch(supplied_hash):
                errors.append("invalid_digest:" + path)
            elif supplied_hash != expected_hash:
                errors.append("source_digest_mismatch:" + path)
    answers = receipt.get("understanding")
    if not isinstance(answers, dict):
        errors.append("missing_understanding")
    else:
        for name, expected in REQUIRED_UNDERSTANDING.items():
            if answers.get(name) != expected:
                errors.append("incorrect_understanding:" + name)
    action = receipt.get("proposed_action")
    if not isinstance(action, dict) or not isinstance(action.get("scope"), str) or not action["scope"].strip():
        errors.append("missing_action_scope")
    elif action.get("self_authorized") is True or action.get("preflight_grants_authority") is True:
        errors.append("improper_authority_claim")
    if receipt.get("independently_verified") is True and not receipt.get("independent_verifier_receipt"):
        errors.append("unsupported_independent_verification_claim")
    return {
        "status": "PREFLIGHT_ELIGIBLE" if not errors else "PREFLIGHT_NOT_READY",
        "errors": errors,
        "authority_granted": False,
        "truth_ceiling": "READ_ATTESTED_NOT_COMPREHENSION_PROVEN",
    }


def main() -> None:
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("receipt", type=Path)
    p.add_argument("trusted_manifest", type=Path,
                   help="Independently produced JSON with main_sha and exact source sha256 map")
    args = p.parse_args()
    trusted = json.loads(args.trusted_manifest.read_text(encoding="utf-8"))
    result = assess(json.loads(args.receipt.read_text(encoding="utf-8")),
                    trusted_main=trusted["main_sha"], trusted_sources=trusted["sources"])
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PREFLIGHT_ELIGIBLE" else 2)


if __name__ == "__main__":
    main()
