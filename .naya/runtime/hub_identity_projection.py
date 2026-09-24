from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / ".naya/contracts/HUB-IDENTITY-PROJECTION-V1.json"
RECEIPT_PATH = ROOT / ".naya/control-plane/HUB-IDENTITY-PROJECTION-RECEIPT.json"
TEAM_LOCK_PATH = ROOT / ".naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md"
TEAM_MARKER = r"SHA: `([0-9a-f]{40})`"
FILE_HASH_SEMANTICS = {
    "algorithm": "sha256",
    "encoding": "utf-8",
    "newline_normalization": "LF",
    "representation": "normalized_text_bytes",
}


class ProjectionError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProjectionError(message)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ProjectionError(f"GIT_FAILED: git {' '.join(args)}: {detail}")
    return result.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProjectionError(f"INVALID_JSON: {path}: {exc}") from exc
    require(isinstance(value, dict), f"JSON_OBJECT_REQUIRED: {path}")
    return value


def load_contract(root: Path = ROOT) -> dict[str, Any]:
    contract = load_json(root / ".naya/contracts/HUB-IDENTITY-PROJECTION-V1.json")
    require(contract.get("status") == "CANONICAL", "PROJECTION_CONTRACT_NOT_CANONICAL")
    require(contract.get("file_hash") == FILE_HASH_SEMANTICS, "PROJECTION_HASH_SEMANTICS_INVALID")
    authority = contract.get("authority")
    destinations = contract.get("destinations")
    require(isinstance(authority, dict), "PROJECTION_AUTHORITY_MISSING")
    require(isinstance(destinations, list) and destinations, "PROJECTION_DESTINATIONS_MISSING")
    ids = [item.get("id") for item in destinations if isinstance(item, dict)]
    require(all(isinstance(value, str) and value for value in ids), "PROJECTION_DESTINATION_ID_INVALID")
    require(len(ids) == len(set(ids)), "PROJECTION_DESTINATION_ID_DUPLICATE")
    require(authority.get("source_ref") == "origin/main", "PROJECTION_SOURCE_REF_NOT_MAIN")
    return contract


def pointer_parts(pointer: str) -> list[str]:
    require(isinstance(pointer, str) and pointer.startswith("/"), "PROJECTION_POINTER_INVALID")
    return [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]


def get_pointer(document: dict[str, Any], pointer: str) -> Any:
    current: Any = document
    for part in pointer_parts(pointer):
        require(isinstance(current, dict) and part in current, f"PROJECTION_TARGET_MISSING:{pointer}")
        current = current[part]
    return current


def set_pointer(document: dict[str, Any], pointer: str, value: Any) -> None:
    parts = pointer_parts(pointer)
    current: Any = document
    for part in parts[:-1]:
        require(isinstance(current, dict) and part in current, f"PROJECTION_TARGET_MISSING:{pointer}")
        current = current[part]
    require(isinstance(current, dict), f"PROJECTION_TARGET_NOT_OBJECT:{pointer}")
    current[parts[-1]] = value


def read_marker(text: str, marker: str = TEAM_MARKER) -> str:
    matches = list(re.finditer(marker, text, flags=re.IGNORECASE))
    require(len(matches) == 1, "TEAM_NAYA_HUB_SHA_AMBIGUOUS")
    return matches[0].group(1)


def replace_team_marker(text: str, sha: str, marker: str = TEAM_MARKER) -> str:
    matches = list(re.finditer(marker, text, flags=re.IGNORECASE))
    require(len(matches) == 1, "TEAM_NAYA_HUB_SHA_AMBIGUOUS")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", sha)), "AUTHORITY_HUB_SHA_INVALID")
    return re.sub(marker, f"SHA: `{sha}`", text, count=1, flags=re.IGNORECASE)


def replace_team_marker_bytes(data: bytes, sha: str, marker: str = TEAM_MARKER) -> bytes:
    encoded_marker = marker.encode("utf-8")
    matches = list(re.finditer(encoded_marker, data, flags=re.IGNORECASE))
    require(len(matches) == 1, "TEAM_NAYA_HUB_SHA_AMBIGUOUS")
    require(bool(re.fullmatch(r"[0-9a-f]{40}", sha)), "AUTHORITY_HUB_SHA_INVALID")
    replacement = f"SHA: `{sha}`".encode("utf-8")
    match = matches[0]
    return data[:match.start()] + replacement + data[match.end():]


def resolve_authority(root: Path = ROOT, source_ref: str = "origin/main") -> dict[str, Any]:
    require(source_ref == "origin/main", "PROJECTION_SOURCE_REF_NOT_MAIN")
    contract = load_contract(root)
    authority_spec = contract["authority"]
    manifest_path = authority_spec["manifest"]
    manifest_text = git(root, "show", f"{source_ref}:{manifest_path}")
    try:
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        raise ProjectionError(f"MANIFEST_INVALID: {manifest_path}: {exc}") from exc
    require(isinstance(manifest, dict), "MANIFEST_OBJECT_REQUIRED")
    require(manifest.get("status") == "ACTIVE", "HUB_PRESERVATION_NOT_ACTIVE")
    canonical = manifest.get("canonical", {})
    active = manifest.get("active_architecture", {})
    checkpoint = manifest.get("current_checkpoint", {})
    hub_path = authority_spec["hub_path"]
    require(canonical.get("human_facing_entrypoint") == hub_path, "HUB_PATH_AUTHORITY_MISMATCH")
    require(canonical.get("implementation_root") == hub_path, "HUB_ROOT_AUTHORITY_MISMATCH")
    require(active.get("entrypoint_mode") == "STATIC_CANONICAL_HUB", "HUB_ARCHITECTURE_MISMATCH")
    require(active.get("implementation_authority") == hub_path, "HUB_IMPLEMENTATION_AUTHORITY_MISMATCH")
    source_commit = git(root, "rev-parse", source_ref)
    actual_hub_sha = git(root, "rev-parse", f"{source_ref}:{hub_path}")
    active_hub_sha = active.get("entrypoint_blob_sha_at_checkpoint")
    recovery_hub_sha = checkpoint.get("recovery_entrypoint_blob_sha")
    require(actual_hub_sha == active_hub_sha, "HUB_ACTIVE_CHECKPOINT_MISMATCH")
    require(actual_hub_sha == recovery_hub_sha, "HUB_RECOVERY_CHECKPOINT_MISMATCH")
    observed_head = checkpoint.get("main_observed_head")
    require(isinstance(observed_head, str) and bool(observed_head), "HUB_OBSERVED_HEAD_MISSING")
    git(root, "cat-file", "-e", f"{observed_head}^{{commit}}")
    require(git(root, "rev-parse", f"{observed_head}:{hub_path}") == recovery_hub_sha, "HUB_RECOVERY_HEAD_BLOB_MISMATCH")
    previous_commit = checkpoint.get("previous_major_hub_checkpoint_commit")
    previous_blob = checkpoint.get("previous_major_hub_checkpoint_blob_sha")
    require(isinstance(previous_commit, str) and isinstance(previous_blob, str), "HUB_HISTORICAL_CHECKPOINT_MISSING")
    git(root, "cat-file", "-e", f"{previous_commit}^{{commit}}")
    require(git(root, "rev-parse", f"{previous_commit}:{hub_path}") == previous_blob, "HUB_HISTORICAL_CHECKPOINT_BLOB_MISMATCH")
    manifest_blob = git(root, "rev-parse", f"{source_ref}:{manifest_path}")
    return {
        "source_ref": source_ref,
        "source_commit": source_commit,
        "manifest_path": manifest_path,
        "manifest_blob": manifest_blob,
        "manifest": manifest,
        "hub_path": hub_path,
        "hub_sha": actual_hub_sha,
    }


def validate_authority(root: Path, authority: dict[str, Any], source_ref: str = "origin/main") -> None:
    current = resolve_authority(root, source_ref)
    for key in ("source_commit", "manifest_blob", "hub_path", "hub_sha"):
        require(authority.get(key) == current.get(key), "AUTHORITY_SOURCE_MISMATCH")


def expected_value(authority: dict[str, Any], destination: dict[str, Any]) -> str:
    return authority["hub_path"] if destination["value_kind"] == "hub_path" else authority["hub_sha"]


def project_documents(
    authority: dict[str, Any],
    contract: dict[str, Any],
    state: dict[str, Any],
    map_data: dict[str, Any],
    team_lock: str,
) -> dict[str, Any]:
    projected_state = copy.deepcopy(state)
    projected_map = copy.deepcopy(map_data)
    projected_team = team_lock
    projected: list[dict[str, Any]] = []
    for destination in contract["destinations"]:
        if destination.get("producer") == "existing_baton_builder":
            continue
        value = expected_value(authority, destination)
        if "marker" in destination:
            projected_team = replace_team_marker(projected_team, value, destination["marker"])
            actual = read_marker(projected_team, destination["marker"])
        else:
            target = projected_state if destination["file"].endswith("STATE.json") else projected_map
            before = get_pointer(target, destination["pointer"])
            set_pointer(target, destination["pointer"], value)
            actual = get_pointer(target, destination["pointer"])
            require(actual == value, f"PROJECTION_VALUE_MISMATCH:{destination['id']}")
            value = actual
        projected.append({"id": destination["id"], "file": destination["file"], "value": value})
    return {"state": projected_state, "map_data": projected_map, "team_lock": projected_team, "projected": projected}


def destination_value(destination: dict[str, Any], state: dict[str, Any], map_data: dict[str, Any], team_lock: str, baton: dict[str, Any] | None) -> str:
    if "marker" in destination:
        return read_marker(team_lock, destination["marker"])
    document = state if destination["file"].endswith("STATE.json") else map_data if destination["file"].endswith("MAP.json") else baton
    require(document is not None, f"PROJECTION_TARGET_MISSING:{destination['file']}")
    return get_pointer(document, destination["pointer"])


def validate_projection_values(
    authority: dict[str, Any],
    contract: dict[str, Any],
    state: dict[str, Any],
    map_data: dict[str, Any],
    team_lock: str,
    baton: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for destination in contract["destinations"]:
        if destination.get("producer") == "existing_baton_builder" and baton is None:
            continue
        actual = destination_value(destination, state, map_data, team_lock, baton)
        expected = expected_value(authority, destination)
        require(actual == expected, f"PROJECTION_VALUE_MISMATCH:{destination['id']}")
        values.append({"id": destination["id"], "file": destination["file"], "value": actual})
    return values


def validate_projection(
    root: Path,
    authority: dict[str, Any],
    contract: dict[str, Any],
    state: dict[str, Any] | None = None,
    map_data: dict[str, Any] | None = None,
    team_lock: str | None = None,
    baton: dict[str, Any] | None = None,
) -> dict[str, Any]:
    validate_authority(root, authority, authority["source_ref"])
    state = state or load_json(root / ".naya/control-plane/STATE.json")
    map_data = map_data or load_json(root / ".naya/control-plane/MAP.json")
    team_lock = team_lock if team_lock is not None else TEAM_LOCK_PATH.read_text(encoding="utf-8")
    baton = baton or load_json(root / ".naya/control-plane/BATON.json")
    values = validate_projection_values(authority, contract, state, map_data, team_lock, baton)
    actual_hub = git(root, "rev-parse", f"HEAD:{authority['hub_path']}")
    require(actual_hub == authority["hub_sha"], "PROJECTED_HUB_SOURCE_CHANGED")
    return {"status": "PASS", "authority": authority["hub_sha"], "destinations": values}


def file_sha(path: Path) -> str:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProjectionError(f"PROJECTION_TARGET_NOT_UTF8:{path}") from exc
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


def normalized_baton(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("generated_at", None)
    return result


def build_receipt(
    root: Path,
    authority: dict[str, Any],
    contract: dict[str, Any],
    state: dict[str, Any],
    map_data: dict[str, Any],
    team_lock: str,
    baton: dict[str, Any],
) -> dict[str, Any]:
    values = validate_projection_values(authority, contract, state, map_data, team_lock, baton)
    target_files = sorted({destination["file"] for destination in contract["destinations"]})
    file_hashes = {file: file_sha(root / file) for file in target_files}
    generated_at = datetime.now(timezone.utc).isoformat()
    receipt = {
        "$schema": "naya/hub-identity-projection-receipt/v1",
        "status": "VERIFIED",
        "repository": "SoulSchoolAcademy/NayaPOWER",
        "source_ref": authority["source_ref"],
        "source_commit": authority["source_commit"],
        "manifest_path": authority["manifest_path"],
        "manifest_blob": authority["manifest_blob"],
        "hub_path": authority["hub_path"],
        "hub_sha": authority["hub_sha"],
        "file_hash": contract["file_hash"],
        "contract_path": ".naya/contracts/HUB-IDENTITY-PROJECTION-V1.json",
        "generator": ".naya/runtime/hub_identity_projection.py",
        "generated_at": generated_at,
        "destinations": values,
        "file_sha256": file_hashes,
        "protected_sources": [{"path": authority["hub_path"], "blob_sha": authority["hub_sha"]}],
        "verification": {"authority_valid": True, "destinations_match": True, "source_unchanged": True},
    }
    receipt_path = root / contract["receipt_path"]
    if receipt_path.is_file():
        existing = load_json(receipt_path)
        if existing.get("source_commit") == receipt["source_commit"] and existing.get("hub_sha") == receipt["hub_sha"] and existing.get("destinations") == receipt["destinations"]:
            receipt["generated_at"] = existing.get("generated_at", generated_at)
    return receipt


def validate_receipt(root: Path, authority: dict[str, Any], contract: dict[str, Any], receipt: dict[str, Any]) -> None:
    require(receipt.get("status") == "VERIFIED", "PROJECTION_RECEIPT_NOT_VERIFIED")
    require(receipt.get("file_hash") == contract.get("file_hash"), "PROJECTION_RECEIPT_HASH_SEMANTICS_MISMATCH")
    require(receipt.get("hub_sha") == authority["hub_sha"], "PROJECTION_RECEIPT_HUB_SHA_MISMATCH")
    require(receipt.get("manifest_blob") == authority["manifest_blob"], "PROJECTION_RECEIPT_MANIFEST_MISMATCH")
    source_commit = receipt.get("source_commit")
    require(isinstance(source_commit, str), "PROJECTION_RECEIPT_SOURCE_COMMIT_MISSING")
    git(root, "cat-file", "-e", f"{source_commit}^{{commit}}")
    current_head = git(root, "rev-parse", "HEAD")
    ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", source_commit, current_head], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    require(ancestor.returncode == 0, "PROJECTION_RECEIPT_SOURCE_NOT_ANCESTOR")
    require(git(root, "rev-parse", f"{source_commit}:{authority['manifest_path']}") == authority["manifest_blob"], "PROJECTION_RECEIPT_MANIFEST_BLOB_MISMATCH")
    require(git(root, "rev-parse", f"{source_commit}:{authority['hub_path']}") == authority["hub_sha"], "PROJECTION_RECEIPT_HUB_BLOB_MISMATCH")
    state = load_json(root / ".naya/control-plane/STATE.json")
    map_data = load_json(root / ".naya/control-plane/MAP.json")
    team_lock = TEAM_LOCK_PATH.read_text(encoding="utf-8")
    baton = load_json(root / ".naya/control-plane/BATON.json")
    expected = validate_projection_values(authority, contract, state, map_data, team_lock, baton)
    require(receipt.get("destinations") == expected, "PROJECTION_RECEIPT_DESTINATIONS_MISMATCH")
    target_files = sorted({destination["file"] for destination in contract["destinations"]})
    current_hashes = {file: file_sha(root / file) for file in target_files}
    require(receipt.get("file_sha256") == current_hashes, "PROJECTION_RECEIPT_FILE_HASH_MISMATCH")
    for item in receipt.get("protected_sources", []):
        require(git(root, "rev-parse", f"HEAD:{item['path']}") == item["blob_sha"], "PROJECTION_PROTECTED_SOURCE_CHANGED")


def load_baton_module(root: Path):
    path = root / ".naya/runtime/baton.py"
    spec = importlib.util.spec_from_file_location("hub_projection_baton", path)
    if spec is None or spec.loader is None:
        raise ProjectionError("BATON_BUILDER_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: dict[str, Any]) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def apply_projection(root: Path = ROOT, source_ref: str = "origin/main") -> dict[str, Any]:
    contract = load_contract(root)
    authority = resolve_authority(root, source_ref)
    validate_authority(root, authority, source_ref)
    state_path = root / ".naya/control-plane/STATE.json"
    map_path = root / ".naya/control-plane/MAP.json"
    team_path = root / contract["destinations"][-1]["file"]
    baton_path = root / ".naya/control-plane/BATON.json"
    receipt_path = root / contract["receipt_path"]
    original = {path: path.read_bytes() if path.is_file() else None for path in (state_path, map_path, team_path, baton_path, receipt_path)}
    try:
        state = load_json(state_path)
        map_data = load_json(map_path)
        team_bytes = team_path.read_bytes()
        team_lock = team_bytes.decode("utf-8")
        plan = project_documents(authority, contract, state, map_data, team_lock)
        write_json(state_path, plan["state"])
        write_json(map_path, plan["map_data"])
        team_destination = next(destination for destination in contract["destinations"] if "marker" in destination)
        projected_team_bytes = replace_team_marker_bytes(team_bytes, authority["hub_sha"], team_destination["marker"])
        team_path.write_bytes(projected_team_bytes)
        plan["team_lock"] = projected_team_bytes.decode("utf-8")
        baton_module = load_baton_module(root)
        old_baton = load_json(baton_path)
        candidate = baton_module.build_baton(source_commit=authority["source_commit"], hub_source_sha=authority["hub_sha"])
        if normalized_baton(old_baton) == normalized_baton(candidate):
            candidate["generated_at"] = old_baton["generated_at"]
        baton_module.write_baton(candidate=candidate, source_commit=authority["source_commit"], hub_source_sha=authority["hub_sha"])
        baton = load_json(baton_path)
        receipt = build_receipt(root, authority, contract, plan["state"], plan["map_data"], plan["team_lock"], baton)
        write_json(receipt_path, receipt)
        validate_projection(root, authority, contract, plan["state"], plan["map_data"], plan["team_lock"], baton)
        validate_receipt(root, authority, contract, receipt)
        return receipt
    except Exception:
        for path, data in original.items():
            if data is None:
                if path.exists():
                    path.unlink()
            else:
                path.write_bytes(data)
        raise


def check_projection(root: Path = ROOT, source_ref: str = "origin/main") -> dict[str, Any]:
    contract = load_contract(root)
    authority = resolve_authority(root, source_ref)
    validate_authority(root, authority, source_ref)
    receipt_path = root / contract["receipt_path"]
    require(receipt_path.is_file(), "PROJECTION_RECEIPT_MISSING")
    receipt = load_json(receipt_path)
    validate_receipt(root, authority, contract, receipt)
    return validate_projection(root, authority, contract)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("resolve", "check", "apply"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--source-ref", default="origin/main")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command == "resolve":
        result = resolve_authority(root, args.source_ref)
    elif args.command == "check":
        result = check_projection(root, args.source_ref)
    else:
        result = apply_projection(root, args.source_ref)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
