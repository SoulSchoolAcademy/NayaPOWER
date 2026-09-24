from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any

RECEIPT_SCHEMA = "naya-current-truth-integration-receipt/v1"
DEFAULT_ROOT = Path(__file__).resolve().parents[2]
CURRENT_STATUSES = {"ACTIVE", "CANONICAL"}


class CurrentTruthIntegrationError(ValueError):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_value(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_output(root: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_resolver(root: Path):
    path = root / ".naya" / "runtime" / "project_intelligence_reconstruction.py"
    spec = importlib.util.spec_from_file_location("priority1_project_intelligence_reconstruction", path)
    if spec is None or spec.loader is None:
        raise CurrentTruthIntegrationError("current-truth resolver could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify_items(reconstruction: dict[str, Any]) -> list[dict[str, Any]]:
    category_by_id: dict[str, str] = {}
    for category in ("current", "historical", "superseded", "stale", "conflicted", "unknown"):
        for item in reconstruction.get(category, []):
            if isinstance(item, dict) and item.get("event_id"):
                category_by_id[str(item["event_id"])] = category.upper()
    rows = []
    for event_id, category in sorted(category_by_id.items()):
        item = next(
            item
            for group in ("current", "historical", "superseded", "stale", "conflicted", "unknown")
            for item in reconstruction.get(group, [])
            if isinstance(item, dict) and item.get("event_id") == event_id
        )
        verification = item.get("verification") if isinstance(item.get("verification"), dict) else {}
        status = str(item.get("status") or "UNKNOWN").upper()
        evidence_count = len(verification.get("evidence") or item.get("evidence_ids") or [])
        reasons = []
        if category == "UNKNOWN":
            if item.get("_reconstruction_error"):
                reasons.append("INVALID_TIMESTAMP")
            if status not in CURRENT_STATUSES:
                reasons.append("STATUS_NOT_CURRENT_ELIGIBLE:" + status)
            if verification.get("status") == "VERIFIED" and status not in CURRENT_STATUSES:
                reasons.append("VERIFIED_RECORDED_NOT_CURRENT")
            if not item.get("source") and not item.get("provenance"):
                reasons.append("SOURCE_PROVENANCE_MISSING")
        rows.append(
            {
                "event_id": event_id,
                "classification": category,
                "status": status,
                "verification_status": verification.get("status"),
                "evidence_count": evidence_count,
                "source_present": bool(item.get("source") or item.get("provenance")),
                "lineage_present": bool(item.get("parent_event_id") or item.get("relationships")),
                "reason_codes": sorted(set(reasons)),
            }
        )
    return rows


def collect_head_values(value: Any, key: str | None = None) -> list[str]:
    if isinstance(value, dict):
        values: list[str] = []
        for child_key, child_value in value.items():
            if child_key in {"observed_head", "current_repository_head", "live_head", "current_main_head", "source_head"}:
                if isinstance(child_value, str) and re.fullmatch(r"[0-9a-f]{40}", child_value):
                    values.append(child_value)
            values.extend(collect_head_values(child_value, child_key))
        return values
    if isinstance(value, list):
        values = []
        for child in value:
            values.extend(collect_head_values(child, key))
        return values
    return []


def source_snapshot(root: Path, name: str, path: str, head: str | None) -> dict[str, Any]:
    data = load_json(root / path)
    value = data.get(name) if name and isinstance(data.get(name), dict) else data
    observed = None
    if isinstance(value, dict):
        observed = value.get("observed_head") or value.get("current_repository_head") or value.get("live_head") or value.get("current_main_head")
    recorded_heads = sorted(set(collect_head_values(value)))
    if observed:
        matches = bool(head and observed == head)
        currentness = "CURRENT" if matches else "STALE"
    else:
        matches = None
        currentness = "CURRENTNESS_UNPROVEN"
    return {
        "path": path,
        "section": name or "ROOT",
        "observed_head": observed,
        "recorded_heads": recorded_heads,
        "live_head": head,
        "matches_live_head": matches,
        "authority": "SNAPSHOT_ONLY" if recorded_heads or observed else "MISSING",
        "currentness": currentness,
    }


def build_receipt(root: Path = DEFAULT_ROOT, project_id: str = "NayaNET") -> dict[str, Any]:
    root = root.resolve()
    resolver = load_resolver(root)
    first = resolver.build_current(project_id)
    second = resolver.build_current(project_id)
    reconstruction_sha256 = digest_value(first)
    reproducible = reconstruction_sha256 == digest_value(second)
    state = load_json(root / ".naya/control-plane/STATE.json")
    blocks = load_json(root / ".naya/control-plane/BLOCKS.json")
    control_map = load_json(root / ".naya/control-plane/MAP.json")
    proof = load_json(root / ".naya/control-plane/PROOF.json")
    baton = load_json(root / ".naya/control-plane/BATON.json")
    head = git_output(root, "rev-parse", "HEAD")
    branch = git_output(root, "branch", "--show-current") or "DETACHED"
    source_scope = "CANONICAL_MAIN" if branch == "main" else "NON_MAIN_SOURCE_SCOPE"
    current_items = classify_items(first)
    current_count = sum(item["classification"] == "CURRENT" for item in current_items)
    unknown_count = sum(item["classification"] == "UNKNOWN" for item in current_items)
    state_next = state.get("current_next_action") if isinstance(state.get("current_next_action"), dict) else {}
    map_next = control_map.get("current_next_action") if isinstance(control_map.get("current_next_action"), dict) else {}
    baton_next = baton.get("next_action") if isinstance(baton.get("next_action"), dict) else {}
    next_action = blocks.get("active_block", {}).get("next_actions", [None])[0]
    next_action_status = str(map_next.get("status") or baton_next.get("status") or "UNKNOWN").upper()
    runtime_parity = proof.get("current_evidence", {}).get("runtime_parity", {}) if isinstance(proof.get("current_evidence"), dict) else {}
    snapshots = [
        source_snapshot(root, "current_head", ".naya/control-plane/STATE.json", head),
        source_snapshot(root, "", ".naya/control-plane/BLOCKS.json", head),
        source_snapshot(root, "", ".naya/control-plane/MAP.json", head),
        source_snapshot(root, "current_evidence", ".naya/control-plane/PROOF.json", head),
        source_snapshot(root, "source_snapshot", ".naya/control-plane/BATON.json", head),
    ]
    if source_scope != "CANONICAL_MAIN":
        truth_status = "NOT_CURRENT_SOURCE_SCOPE"
    elif current_count == 0 or next_action_status == "BLOCKED":
        truth_status = "BLOCKED"
    else:
        truth_status = "COMPLETE"
    verification_status = "VERIFIED_MECHANISM" if reproducible else "BLOCKED"
    reconstruction_status = first.get("resolution", {}).get("status")
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "verification_status": verification_status,
        "verification_scope": "RECONSTRUCTION_RECEIPT_ONLY",
        "truth_status": truth_status,
        "reconstruction_status": reconstruction_status,
        "source_identity": {
            "project_id": project_id,
            "branch": branch,
            "head": head,
            "source_scope": source_scope,
            "recorded_heads_are_authoritative": False,
        },
        "reconstruction": {
            "status": first.get("resolution", {}).get("status"),
            "schema": first.get("schema"),
            "sha256": reconstruction_sha256,
            "reproducible": reproducible,
            "counts": first.get("counts", {}),
            "current_items": current_items,
        },
        "control_plane": {
            "state_status": state.get("status"),
            "active_block": blocks.get("active_block", {}).get("id"),
            "active_block_status": blocks.get("active_block", {}).get("status"),
            "state_next_action": state_next.get("action"),
            "map_next_action": control_map.get("next_action"),
            "map_current_next_action_status": map_next.get("status"),
            "baton_next_action_status": baton_next.get("status"),
            "next_action": next_action,
            "next_action_status": next_action_status,
            "runtime_parity_status": runtime_parity.get("status"),
            "snapshots": snapshots,
        },
        "canonical_execution_boundary": {
            "status": "NOT_EXECUTED",
            "authority_registry": ".naya/governance/authority-registry.json",
            "execution_controller": ".naya/runtime/execution_controller.py",
            "universal_execution_gate": ".naya/runtime/universal_execution_gate.py",
            "intelligence_commit": "supabase/functions/nayanet-compound-intelligence/index.ts",
            "event_persistence": ".naya/runtime/canonical_event_store.py",
            "required_chain": [
                "actor",
                "authority",
                "decision",
                "execution",
                "intelligence_commit",
                "persistence",
                "receipt",
            ],
        },
        "truth_boundary": "This receipt reconstructs and explains current truth from existing sources. It does not promote UNKNOWN records, repair control-plane snapshots, execute authority, persist intelligence, or produce a successor receipt.",
    }
    receipt["receipt_sha256"] = digest_value(receipt)
    return receipt


def validate_receipt(receipt: dict[str, Any]) -> list[str]:
    errors = []
    if receipt.get("schema") != RECEIPT_SCHEMA:
        return ["receipt schema is invalid"]
    if "status" in receipt:
        errors.append("ambiguous top-level status field is forbidden")
    if receipt.get("verification_status") != "VERIFIED_MECHANISM":
        errors.append("receipt mechanism verification status is invalid")
    if receipt.get("verification_scope") != "RECONSTRUCTION_RECEIPT_ONLY":
        errors.append("receipt verification scope is invalid")
    if receipt.get("truth_status") not in {"NOT_CURRENT_SOURCE_SCOPE", "BLOCKED", "COMPLETE"}:
        errors.append("truth status is invalid")
    if receipt.get("reconstruction_status") != "RECONSTRUCTED":
        errors.append("reconstruction status is invalid")
    recorded = receipt.get("receipt_sha256")
    material = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    if recorded != digest_value(material):
        errors.append("receipt digest is invalid")
    if receipt.get("reconstruction", {}).get("reproducible") is not True:
        errors.append("reconstruction is not reproducible")
    if receipt.get("canonical_execution_boundary", {}).get("status") != "NOT_EXECUTED":
        errors.append("execution boundary was claimed")
    if receipt.get("source_identity", {}).get("recorded_heads_are_authoritative") is not False:
        errors.append("recorded snapshot authority boundary is invalid")
    expected_paths = {
        ".naya/control-plane/STATE.json",
        ".naya/control-plane/BLOCKS.json",
        ".naya/control-plane/MAP.json",
        ".naya/control-plane/PROOF.json",
        ".naya/control-plane/BATON.json",
    }
    snapshots = receipt.get("control_plane", {}).get("snapshots", [])
    if {snapshot.get("path") for snapshot in snapshots} != expected_paths:
        errors.append("control-plane snapshot matrix is incomplete")
    for snapshot in snapshots:
        if snapshot.get("authority") not in {"SNAPSHOT_ONLY", "MISSING"}:
            errors.append("snapshot authority boundary is invalid")
        if snapshot.get("currentness") not in {"CURRENT", "STALE", "CURRENTNESS_UNPROVEN"}:
            errors.append("snapshot currentness is invalid")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--project", default="NayaNET")
    parser.add_argument("--out")
    args = parser.parse_args()
    receipt = build_receipt(Path(args.root), args.project)
    if args.out:
        output = Path(args.out)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if not validate_receipt(receipt) else 1


if __name__ == "__main__":
    raise SystemExit(main())
