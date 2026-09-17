#!/usr/bin/env python3
"""Single fail-closed NayaPOWER readiness gate.

This is a verifier, not a second state system. It reads the canonical
MAP/STATE/BLOCKS/PROOF/GOVERNANCE-KERNEL objects and returns one machine result.
Unproven mission boundaries remain UNKNOWN; UNKNOWN can never satisfy READY.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CP = ROOT / ".naya" / "control-plane"
REQUIRED = {
    "map": CP / "MAP.json",
    "state": CP / "STATE.json",
    "blocks": CP / "BLOCKS.json",
    "proof": CP / "PROOF.json",
    "governance": CP / "GOVERNANCE-KERNEL.json",
    "identity": CP / "CANONICAL-IDENTITY-REGISTRY.json",
}
UNKNOWN_MISSION_BOUNDARIES = (
    "golden_journey",
    "learning_adaptation",
    "privacy_access",
    "concurrency_idempotency",
    "temporal_conflict",
    "authenticated_lifecycle",
    "runtime_parity",
    "external_cold_naya",
    "recovery_rollback",
    "security_adversarial",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def result(name: str, status: str, evidence: list[str], reason: str) -> dict[str, Any]:
    return {"name": name, "status": status, "evidence": evidence, "reason": reason}


def evaluate() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    missing = [name for name, path in REQUIRED.items() if not path.is_file()]
    if missing:
        checks.append(result(
            "canonical_control_plane", "FAILED", [],
            "missing canonical objects: " + ", ".join(missing),
        ))
        return _finalize(checks, None)

    try:
        m, s, b, p, g, i = (load(REQUIRED[k]) for k in
                             ("map", "state", "blocks", "proof", "governance", "identity"))
        current = head()
    except Exception as exc:
        checks.append(result("canonical_control_plane", "FAILED", [], str(exc)))
        return _finalize(checks, None)

    checks.append(result(
        "canonical_control_plane", "VERIFIED",
        [str(path.relative_to(ROOT)) for path in REQUIRED.values()],
        "all canonical control-plane objects load",
    ))

    checks.append(result(
        "identity", "VERIFIED" if (
            i.get("status") == "CANONICAL"
            and i.get("repository") in (None, "SoulSchoolAcademy/NayaPOWER")
        ) else "FAILED",
        [str(REQUIRED["identity"].relative_to(ROOT))],
        "canonical identity registry is present and canonical",
    ))

    structural_ok = (
        m.get("status") == "CANONICAL"
        and s.get("status") == "LIVE_BOUND"
        and b.get("status") == "CANONICAL"
        and p.get("status") == "CANONICAL"
        and g.get("status") == "CANONICAL"
        and g.get("fail_closed") is True
        and s.get("current_head", {}).get("source") == "git:HEAD"
        and s.get("current_branch", {}).get("source") == "git:branch --show-current"
    )
    checks.append(result(
        "map_state_blocks_proof_governance", "VERIFIED" if structural_ok else "FAILED",
        [str(REQUIRED[k].relative_to(ROOT)) for k in ("map","state","blocks","proof","governance")],
        "canonical surfaces are live-bound and governance is fail-closed",
    ))

    block = b.get("active_block", {})
    next_a = s.get("single_next_action")
    block_next = block.get("next_action")
    next_ok = (
        s.get("next_action_count") == 1
        and isinstance(s.get("next_actions"), list)
        and len(s["next_actions"]) == 1
        and s["next_actions"][0] == next_a
        and block.get("status") == "ACTIVE"
        and block_next == next_a
    )
    checks.append(result(
        "single_next_action", "VERIFIED" if next_ok else "FAILED",
        [str(REQUIRED["state"].relative_to(ROOT)), str(REQUIRED["blocks"].relative_to(ROOT))],
        "STATE and active BLOCK expose exactly one identical next action",
    ))

    recorded = p.get("current_evidence", {})
    evidence_head = recorded.get("observed_head")
    runtime_current = (
        bool(evidence_head)
        and evidence_head == current
        and recorded.get("classification") not in ("HISTORICAL_STALE_RELATIVE_TO_LIVE_HEAD", "STALE")
    )
    checks.append(result(
        "runtime_parity", "VERIFIED" if runtime_current else "UNKNOWN",
        [str(REQUIRED["proof"].relative_to(ROOT))],
        "current-head runtime evidence must bind exactly to live HEAD; historical evidence cannot certify it",
    ))

    # These are deliberately explicit UNKNOWN gates until claim-appropriate
    # evidence is attached to the canonical proof authority. The gate does not
    # infer success from architecture, documentation, or code presence.
    for name in UNKNOWN_MISSION_BOUNDARIES:
        checks.append(result(
            name.upper(), "UNKNOWN", [str(REQUIRED["proof"].relative_to(ROOT))],
            "no current claim-appropriate evidence is promoted by this gate",
        ))

    return _finalize(checks, current)


def _finalize(checks: list[dict[str, Any]], current: str | None) -> dict[str, Any]:
    ready = bool(checks) and all(c["status"] in {"VERIFIED", "PRODUCTION_PROVEN"} for c in checks)
    counts = {status: sum(c["status"] == status for c in checks)
              for status in ("VERIFIED", "PRODUCTION_PROVEN", "UNKNOWN", "FAILED")}
    return {
        "$schema": "naya/superbrain-ready/v1",
        "gate": "NAYA_SUPERBRAIN_READY",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "head": current,
        "status": "READY" if ready else "BLOCKED",
        "fail_closed": True,
        "counts": counts,
        "checks": checks,
        "rule": "READY requires every gate to be VERIFIED or PRODUCTION_PROVEN; UNKNOWN and FAILED are blocking.",
    }


def main() -> int:
    payload = evaluate()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
