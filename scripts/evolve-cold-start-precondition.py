#!/usr/bin/env python3
"""Repository-hermetic EVOLVE cold-start precondition probe.

This does not claim a genuine cold successor or EVOLVE activation. It checks
whether a successor can reconstruct current canonical limits from repo-owned
artifacts without chat memory, home-directory files, or volatile SHAs.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NODES = {"SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"}


def evaluate(root: Path = ROOT) -> dict:
    rel = {
        "manifest": "BRAIN/03-KERNEL/MANIFEST.json",
        "registry": "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json",
        "succession": "BRAIN/08-SUCCESSION/0001-SUCCESSOR-CONTRACT-V1.md",
        "baseline": "BRAIN/12-ENGINEERING/CHAIN-READINESS-BASELINE.json",
    }
    paths = {name: root / path for name, path in rel.items()}
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        return {"ok": False, "gaps": [f"missing_repo_artifact:{name}" for name in missing]}

    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    registry = json.loads(paths["registry"].read_text(encoding="utf-8"))
    succession = paths["succession"].read_text(encoding="utf-8", errors="replace")
    baseline = json.loads(paths["baseline"].read_text(encoding="utf-8"))
    names = {node.get("name") for node in manifest.get("nodes", [])}
    gaps = []
    if names != EXPECTED_NODES:
        gaps.append("nine_node_manifest_mismatch")
    if registry.get("manifest") != rel["manifest"]:
        gaps.append("runtime_registry_manifest_binding_missing")
    if "Authority context missing" not in succession or "read-only mode" not in succession:
        gaps.append("successor_authority_fail_closed_rule_missing")
    if "Stale successor package" not in succession or "canonical sources" not in succession:
        gaps.append("successor_stale_rebuild_rule_missing")
    if "NOT a target" not in baseline.get("purpose", ""):
        gaps.append("readiness_floor_could_be_misread_as_completion")

    return {
        "ok": not gaps,
        "gaps": gaps,
        "node_count": len(names),
        "manifest_runtime_status": manifest.get("runtime_binding", {}).get("status"),
        "succession_contract_ratification_required": "HUMAN DIRECTOR RATIFICATION REQUIRED" in succession,
        "behavioral_cold_successor_proven": False,
        "activation_claim": "NOT_MADE",
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["ok"]:
        print("COLD_START_PRECONDITION_PASS: repo-owned truth is reconstructable; genuine cold-successor proof remains required.")
        return 0
    print("COLD_START_PRECONDITION_FAIL: successor reconstruction prerequisites are incomplete.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
