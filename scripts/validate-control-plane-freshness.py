#!/usr/bin/env python3
"""Fail-closed control-plane freshness and explicit UNKNOWN resolution audit."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / ".naya/control-plane/STATE.json"
BLOCKS_PATH = ROOT / ".naya/control-plane/BLOCKS.json"
MAP_PATH = ROOT / ".naya/control-plane/MAP.json"
PROOF_PATH = ROOT / ".naya/control-plane/PROOF.json"
BATON_PATH = ROOT / ".naya/control-plane/BATON.json"
UNKNOWN_REGISTRY_PATH = ROOT / ".naya/control-plane/UNKNOWN-REGISTRY.json"
UNKNOWN_RESOLUTION_PATH = ROOT / ".naya/control-plane/UNKNOWN-RESOLUTION-LEDGER.json"
TEAM_HUB_LOCK_PATH = ROOT / ".naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md"
HUB_PATH = ROOT / "NAYANET/HUB/index.html"
REPORT_PATH = ROOT / "control-plane-freshness-audit.json"
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
RESOLUTION_STATUSES = {"RESOLVED", "SUPERSEDED", "BLOCKED", "STILL_UNKNOWN"}
REGISTRY_STATUSES = {"UNKNOWN", "RESOLVED", "SUPERSEDED", "BLOCKED", "STILL_UNKNOWN"}


class FreshnessError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FreshnessError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"MISSING: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FreshnessError(f"INVALID_JSON: {path}: {exc}") from exc
    require(isinstance(value, dict), f"INVALID_ROOT: {path}")
    return value


def git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise FreshnessError(f"GIT_FAILED: git {' '.join(args)}: {detail}")
    return result.stdout.strip()


def commit_exists(root: Path, sha: str) -> bool:
    if not isinstance(sha, str) or not COMMIT_PATTERN.fullmatch(sha):
        return False
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    if not commit_exists(root, ancestor) or not commit_exists(root, descendant):
        return False
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def parse_timestamp(value: Any, label: str) -> datetime:
    require(isinstance(value, str) and value.strip(), f"{label} is missing")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise FreshnessError(f"{label} is not ISO-8601: {value}") from exc
    require(parsed.tzinfo is not None, f"{label} must include a timezone")
    return parsed


def normalize_state_unknowns(state: dict[str, Any]) -> list[dict[str, Any]]:
    raw = state.get("unknown")
    require(isinstance(raw, list), "STATE.unknown must be a list")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(raw):
        if isinstance(item, str):
            require(bool(item.strip()), f"STATE.unknown[{index}] is empty")
            normalized.append({"id": None, "statement": item, "declared_status": None})
            continue
        require(isinstance(item, dict), f"STATE.unknown[{index}] must be a string or identity object")
        identity = item.get("id")
        statement = item.get("statement")
        require(isinstance(identity, str) and identity.strip(), f"STATE.unknown[{index}] missing id")
        require(isinstance(statement, str) and statement.strip(), f"STATE.unknown[{index}] missing statement")
        normalized.append({"id": identity, "statement": statement, "declared_status": item.get("status")})
    return normalized


def index_registry(registry: dict[str, Any], state_unknowns: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    require(registry.get("status") == "CANONICAL", "UNKNOWN_REGISTRY_NOT_CANONICAL")
    entries = registry.get("entries")
    require(isinstance(entries, list), "UNKNOWN_REGISTRY_ENTRIES_MISSING")
    by_id: dict[str, dict[str, Any]] = {}
    by_statement: dict[str, str] = {}
    for index, entry in enumerate(entries):
        require(isinstance(entry, dict), f"UNKNOWN_REGISTRY_ENTRY_{index}_INVALID")
        identity = entry.get("id")
        statement = entry.get("statement")
        status = entry.get("status")
        require(isinstance(identity, str) and identity.strip(), f"UNKNOWN_REGISTRY_ENTRY_{index}_ID_MISSING")
        require(identity not in by_id, f"DUPLICATE_UNKNOWN_ID: {identity}")
        require(isinstance(statement, str) and statement.strip(), f"UNKNOWN_REGISTRY_ENTRY_{index}_STATEMENT_MISSING")
        require(statement not in by_statement, f"DUPLICATE_UNKNOWN_STATEMENT: {statement}")
        require(status in REGISTRY_STATUSES, f"UNKNOWN_REGISTRY_STATUS_INVALID: {identity}")
        if status == "UNKNOWN":
            require(entry.get("resolution") is None, f"UNKNOWN_RESOLUTION_MUST_BE_NULL: {identity}")
        by_id[identity] = entry
        by_statement[statement] = identity
    listed_ids: set[str] = set()
    for item in state_unknowns:
        statement = item["statement"]
        require(statement in by_statement, f"UNKNOWN_IDENTITY_MISSING: {statement}")
        identity = by_statement[statement]
        if item["id"] is not None:
            require(item["id"] == identity, f"UNKNOWN_IDENTITY_MISMATCH: {statement}")
        listed_ids.add(identity)
    return by_id


def validate_evidence(record: dict[str, Any], identity: str) -> None:
    evidence = record.get("evidence")
    require(isinstance(evidence, list) and bool(evidence), f"RESOLUTION_EVIDENCE_MISSING: {identity}")
    for item in evidence:
        if isinstance(item, str):
            require(bool(item.strip()), f"RESOLUTION_EVIDENCE_EMPTY: {identity}")
        else:
            require(isinstance(item, dict) and bool(item), f"RESOLUTION_EVIDENCE_ITEM_INVALID: {identity}")


def validate_resolution_commit(
    root: Path,
    record: dict[str, Any],
    identity: str,
    live_head: str,
) -> None:
    source_commit = record.get("source_commit") or record.get("commit")
    if record.get("status") in {"RESOLVED", "SUPERSEDED"}:
        require(isinstance(source_commit, str) and COMMIT_PATTERN.fullmatch(source_commit), f"RESOLUTION_SOURCE_COMMIT_MISSING: {identity}")
        require(commit_exists(root, source_commit), f"RESOLUTION_SOURCE_COMMIT_UNKNOWN: {identity}")
        require(is_ancestor(root, source_commit, live_head), f"STALE_RESOLUTION_PROOF: {identity}")
    elif source_commit is not None:
        require(isinstance(source_commit, str) and COMMIT_PATTERN.fullmatch(source_commit), f"RESOLUTION_SOURCE_COMMIT_INVALID: {identity}")
        require(commit_exists(root, source_commit), f"RESOLUTION_SOURCE_COMMIT_UNKNOWN: {identity}")


def resolve_unknowns(
    registry: dict[str, Any],
    state_unknowns: list[dict[str, Any]],
    ledger: dict[str, Any],
    root: Path,
    live_head: str,
    proof: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(isinstance(proof, dict) if proof is not None else True, "PROOF must be an object")
    require(ledger.get("status") == "CANONICAL", "UNKNOWN_RESOLUTION_LEDGER_NOT_CANONICAL")
    entries = index_registry(registry, state_unknowns)
    records = ledger.get("resolutions")
    require(isinstance(records, list), "UNKNOWN_RESOLUTION_RECORDS_MISSING")
    by_identity: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        require(isinstance(record, dict), f"UNKNOWN_RESOLUTION_RECORD_{index}_INVALID")
        identity = record.get("resolves_unknown")
        require(isinstance(identity, str) and identity in entries, f"RESOLUTION_IDENTITY_UNKNOWN: {identity}")
        require(identity not in by_identity, f"DUPLICATE_RESOLUTION_FOR_UNKNOWN: {identity}")
        status = record.get("status")
        require(status in RESOLUTION_STATUSES, f"RESOLUTION_STATUS_INVALID: {identity}")
        validate_evidence(record, identity)
        validate_resolution_commit(root, record, identity, live_head)
        if status == "SUPERSEDED":
            replacement = record.get("replacement")
            require(isinstance(replacement, dict), f"SUPERSEDED_REPLACEMENT_MISSING: {identity}")
            require(isinstance(replacement.get("statement"), str) and replacement["statement"].strip(), f"SUPERSEDED_REPLACEMENT_STATEMENT_MISSING: {identity}")
            require(bool(replacement.get("evidence_ref") or replacement.get("proof_ref")), f"SUPERSEDED_REPLACEMENT_EVIDENCE_MISSING: {identity}")
        if status == "BLOCKED":
            require(bool(record.get("blocker")), f"BLOCKED_REASON_MISSING: {identity}")
            require(bool(record.get("external_dependency")), f"BLOCKED_DEPENDENCY_MISSING: {identity}")
        by_identity[identity] = record
    listed_ids = {identity for identity, entry in entries.items() if any(item["statement"] == entry["statement"] for item in state_unknowns)}
    statuses: dict[str, str] = {}
    for identity, entry in entries.items():
        base_status = entry["status"]
        record = by_identity.get(identity)
        require(base_status == "UNKNOWN" or record is not None, f"REGISTRY_RESOLUTION_WITHOUT_PROOF: {identity}")
        effective_status = record["status"] if record else base_status
        listed = identity in listed_ids
        if effective_status in {"RESOLVED", "SUPERSEDED"}:
            require(not listed, f"RESOLVED_UNKNOWN_STILL_LISTED: {identity}")
        else:
            require(listed, f"UNRESOLVED_UNKNOWN_MISSING: {identity}")
        for item in state_unknowns:
            if item["statement"] == entry["statement"] and item.get("declared_status"):
                require(item["declared_status"] == effective_status, f"UNKNOWN_DECLARED_STATUS_MISMATCH: {identity}")
        statuses[identity] = effective_status
    return {
        "statuses": statuses,
        "resolved": sorted(identity for identity, status in statuses.items() if status == "RESOLVED"),
        "superseded": sorted(identity for identity, status in statuses.items() if status == "SUPERSEDED"),
        "blocked": sorted(identity for identity, status in statuses.items() if status == "BLOCKED"),
        "still_unknown": sorted(identity for identity, status in statuses.items() if status in {"UNKNOWN", "STILL_UNKNOWN"}),
    }


def validate_head(root: Path, state: dict[str, Any], live_head: str, live_branch: str) -> dict[str, Any]:
    current_head = state.get("current_head")
    require(isinstance(current_head, dict), "STATE.current_head is missing")
    require(current_head.get("source") == "git:HEAD", "STATE.current_head is not live-resolved")
    require(current_head.get("value") == "LIVE_AT_EXECUTION_TIME", "STATE.current_head is recorded as authoritative")
    require(live_branch == "main", f"NON_MAIN_CURRENT_AUTHORITY: {live_branch}")
    observed = current_head.get("observed_head")
    if observed:
        require(commit_exists(root, observed), "STATE.observed_head is not a repository commit")
        if observed != live_head:
            require(current_head.get("recorded_head_is_not_authoritative") is True, "STALE_STATE_HEAD_WITHOUT_AUTHORITY_FLAG")
    return {"live_head": live_head, "live_branch": live_branch, "recorded_observed_head": observed}


def validate_actions(state: dict[str, Any], blocks: dict[str, Any], map_data: dict[str, Any], baton: dict[str, Any]) -> dict[str, str]:
    active = blocks.get("active_block")
    require(isinstance(active, dict), "BLOCKS.active_block is missing")
    block_actions = active.get("next_actions")
    require(isinstance(block_actions, list) and len(block_actions) == 1, "BLOCKS.next_actions must contain one action")
    state_actions = state.get("next_actions")
    require(isinstance(state_actions, list) and len(state_actions) == 1, "STATE.next_actions must contain one action")
    state_next = state.get("next_action")
    state_current_next = state.get("current_next_action")
    require(isinstance(state_next, dict), "STATE.next_action object is missing")
    require(isinstance(state_current_next, dict), "STATE.current_next_action object is missing")
    actions = {
        "BLOCKS.active_block.next_action": active.get("next_action"),
        "BLOCKS.active_block.next_actions[0]": block_actions[0],
        "STATE.single_next_action": state.get("single_next_action"),
        "STATE.next_actions[0]": state_actions[0],
        "STATE.next_action.action": state_next.get("action"),
        "STATE.current_next_action.action": state_current_next.get("action"),
        "MAP.execution_map.next_action": map_data.get("execution_map", {}).get("next_action"),
        "MAP.next_action": map_data.get("next_action"),
        "BATON.next_action.action": baton.get("next_action", {}).get("action"),
        "BATON.source_snapshot.block_next_action": baton.get("source_snapshot", {}).get("block_next_action"),
    }
    require(all(isinstance(value, str) and value.strip() for value in actions.values()), "NEXT_ACTION_MISSING")
    require(len(set(actions.values())) == 1, f"NEXT_ACTION_DIVERGENCE: {json.dumps(actions, sort_keys=True)}")
    return actions


def validate_active_block(state: dict[str, Any], blocks: dict[str, Any], map_data: dict[str, Any], baton: dict[str, Any]) -> dict[str, str]:
    active = blocks.get("active_block", {})
    values = {
        "BLOCKS.active_block.id": active.get("id"),
        "STATE.current_block": state.get("current_block"),
        "MAP.execution_map.active_block": map_data.get("execution_map", {}).get("active_block"),
        "BATON.current_state.active_block": baton.get("current_state", {}).get("active_block"),
        "BATON.source_snapshot.state_block": baton.get("source_snapshot", {}).get("state_block"),
    }
    require(all(isinstance(value, str) and value.strip() for value in values.values()), "ACTIVE_BLOCK_MISSING")
    require(len(set(values.values())) == 1, f"ACTIVE_BLOCK_DIVERGENCE: {json.dumps(values, sort_keys=True)}")
    status_values = {
        "BLOCKS.active_block.status": active.get("status"),
        "STATE.current_block_status": state.get("current_block_status"),
        "BATON.current_state.active_block_status": baton.get("current_state", {}).get("active_block_status"),
    }
    require(all(isinstance(value, str) and value.strip() for value in status_values.values()), "ACTIVE_BLOCK_STATUS_MISSING")
    require(len(set(status_values.values())) == 1, f"ACTIVE_BLOCK_STATUS_DIVERGENCE: {json.dumps(status_values, sort_keys=True)}")
    return {**values, **status_values}


def validate_proof(root: Path, proof: dict[str, Any], live_head: str) -> dict[str, str]:
    require(proof.get("status") == "CANONICAL", "PROOF_NOT_CANONICAL")
    claim_evidence = proof.get("claim_evidence")
    require(isinstance(claim_evidence, dict), "PROOF.claim_evidence is missing")
    for claim_type in ("SOURCE", "BUILD", "AUTOMATED", "RUNTIME", "VISUAL", "WHOLE_JOURNEY", "PRODUCTION"):
        require(claim_type in claim_evidence, f"PROOF_CLAIM_TYPE_MISSING: {claim_type}")
    for rule in ("IMPLEMENTED != VERIFIED", "VERIFIED != PRODUCTION_PROVEN", "RECORDED != CURRENT", "UNKNOWN != GREEN"):
        require(rule in proof.get("separation_rules", []), f"PROOF_SEPARATION_RULE_MISSING: {rule}")
    current_evidence = proof.get("current_evidence")
    require(isinstance(current_evidence, dict), "PROOF.current_evidence is missing")
    observed = current_evidence.get("observed_head")
    recording = proof.get("recording_commit")
    require(isinstance(observed, str) and commit_exists(root, observed), "PROOF_OBSERVED_HEAD_INVALID")
    require(isinstance(recording, str) and commit_exists(root, recording), "PROOF_RECORDING_COMMIT_INVALID")
    require(is_ancestor(root, recording, live_head), "PROOF_RECORDING_NOT_ANCESTOR")
    return {"observed_head": observed, "recording_commit": recording}


def extract_team_hub_sha(text: str) -> str:
    matches = re.findall(r"SHA:\s*`([0-9a-f]{40})`", text, flags=re.IGNORECASE)
    require(bool(matches), "TEAM_NAYA_HUB_SHA_MISSING")
    require(len(set(matches)) == 1, "TEAM_NAYA_HUB_SHA_AMBIGUOUS")
    return matches[0]


def validate_hub(root: Path, state: dict[str, Any], map_data: dict[str, Any], baton: dict[str, Any], live_head: str) -> dict[str, str]:
    require(HUB_PATH.is_file(), "CANONICAL_HUB_SOURCE_MISSING")
    actual = git(root, "rev-parse", f"{live_head}:NAYANET/HUB/index.html")
    state_sha = state.get("hub_pre_execution_gate", {}).get("canonical_hub_source_sha") or state.get("hub", {}).get("canonical_hub_source_sha")
    map_sha = map_data.get("intelligent_hub_pre_execution", {}).get("canonical_hub_source_sha") or map_data.get("intelligent_hub", {}).get("canonical_hub_source_sha")
    map_top_sha = map_data.get("canonical_hub_source_sha")
    baton_sha = baton.get("source_snapshot", {}).get("canonical_hub_source_sha")
    team_sha = extract_team_hub_sha(TEAM_HUB_LOCK_PATH.read_text(encoding="utf-8"))
    values = {
        "STATE": state_sha,
        "MAP.pre_execution": map_sha,
        "MAP.top_level": map_top_sha,
        "BATON": baton_sha,
        "TEAM_NAYA": team_sha,
    }
    require(all(isinstance(value, str) and value for value in values.values()), "CANONICAL_HUB_SHA_MISSING")
    require(all(value == actual for value in values.values()), f"CANONICAL_HUB_SHA_DIVERGENCE: actual={actual} values={json.dumps(values, sort_keys=True)}")
    return {"actual": actual, **values}


def validate_baton(root: Path, state: dict[str, Any], blocks: dict[str, Any], map_data: dict[str, Any], proof: dict[str, Any], baton: dict[str, Any], live_head: str) -> dict[str, Any]:
    for field in ("identity", "generated_at", "source_of_truth", "current_state", "current_intelligence", "truth", "active_block", "next_action", "evidence", "successor_prompt", "playback"):
        require(field in baton, f"BATON_FIELD_MISSING: {field}")
    source = baton.get("source_of_truth", {})
    expected_sources = {
        "live_state": ".naya/control-plane/STATE.json",
        "active_block": ".naya/control-plane/BLOCKS.json",
        "mission_map": ".naya/control-plane/MAP.json",
        "proof": ".naya/control-plane/PROOF.json",
    }
    for key, expected in expected_sources.items():
        require(source.get(key) == expected, f"BATON_SOURCE_MISMATCH: {key}")
    active = blocks.get("active_block", {})
    require(baton.get("current_state", {}).get("active_block") == active.get("id"), "BATON_ACTIVE_BLOCK_MISMATCH")
    require(baton.get("current_state", {}).get("active_block_status") == active.get("status"), "BATON_ACTIVE_BLOCK_STATUS_MISMATCH")
    require(baton.get("next_action", {}).get("count") == 1, "BATON_NEXT_ACTION_COUNT_INVALID")
    require(baton.get("next_action", {}).get("action") == active.get("next_action"), "BATON_NEXT_ACTION_MISMATCH")
    snapshot = baton.get("source_snapshot", {})
    require(snapshot.get("state_block") == active.get("id"), "BATON_SNAPSHOT_BLOCK_MISMATCH")
    require(snapshot.get("block_next_action") == active.get("next_action"), "BATON_SNAPSHOT_ACTION_MISMATCH")
    require(snapshot.get("state_status") == state.get("status"), "BATON_SNAPSHOT_STATE_STATUS_MISMATCH")
    require(snapshot.get("map_status") == map_data.get("status"), "BATON_SNAPSHOT_MAP_STATUS_MISMATCH")
    require(snapshot.get("proof_status") == proof.get("status"), "BATON_SNAPSHOT_PROOF_STATUS_MISMATCH")
    require(isinstance(baton.get("evidence"), list) and bool(baton.get("evidence")), "BATON_EVIDENCE_MISSING")
    snapshot_head = snapshot.get("live_head")
    require(isinstance(snapshot_head, str) and commit_exists(root, snapshot_head), "BATON_SNAPSHOT_HEAD_INVALID")
    require(is_ancestor(root, snapshot_head, live_head), "BATON_SNAPSHOT_HEAD_NOT_ANCESTOR")
    generated = parse_timestamp(baton.get("generated_at"), "BATON.generated_at")
    snapshot_time = parse_timestamp(git(root, "show", "-s", "--format=%cI", snapshot_head), "BATON.snapshot_time")
    require(generated >= snapshot_time, "BATON_GENERATED_BEFORE_SOURCE_SNAPSHOT")
    now = datetime.now(timezone.utc)
    require(generated <= now, "BATON_GENERATED_IN_FUTURE")
    changed = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            f"{snapshot_head}..{live_head}",
            "--",
            ".naya/control-plane/STATE.json",
            ".naya/control-plane/BLOCKS.json",
            ".naya/control-plane/MAP.json",
            ".naya/control-plane/PROOF.json",
            ".naya/control-plane/UNKNOWN-REGISTRY.json",
            ".naya/control-plane/UNKNOWN-RESOLUTION-LEDGER.json",
        ],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    require(changed.returncode == 0, "BATON_SOURCE_SNAPSHOT_STALE")
    return {"generated_at": baton["generated_at"], "snapshot_head": snapshot_head, "age_hours": round((now - generated).total_seconds() / 3600, 2)}


def validate_all(root: Path = ROOT) -> dict[str, Any]:
    state = load_json(root / ".naya/control-plane/STATE.json")
    blocks = load_json(root / ".naya/control-plane/BLOCKS.json")
    map_data = load_json(root / ".naya/control-plane/MAP.json")
    proof = load_json(root / ".naya/control-plane/PROOF.json")
    baton = load_json(root / ".naya/control-plane/BATON.json")
    registry = load_json(root / ".naya/control-plane/UNKNOWN-REGISTRY.json")
    ledger = load_json(root / ".naya/control-plane/UNKNOWN-RESOLUTION-LEDGER.json")
    live_head = git(root, "rev-parse", "HEAD")
    live_branch = git(root, "branch", "--show-current")
    head_info = validate_head(root, state, live_head, live_branch)
    active_info = validate_active_block(state, blocks, map_data, baton)
    actions = validate_actions(state, blocks, map_data, baton)
    state_unknowns = normalize_state_unknowns(state)
    unknown_info = resolve_unknowns(registry, state_unknowns, ledger, root, live_head, proof)
    proof_info = validate_proof(root, proof, live_head)
    baton_info = validate_baton(root, state, blocks, map_data, proof, baton, live_head)
    hub_info = validate_hub(root, state, map_data, baton, live_head)
    return {
        "schema": "NAYANET_CONTROL_PLANE_FRESHNESS_AUDIT_V2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "live_head": live_head,
        "live_branch": live_branch,
        "status": "FRESH",
        "checks": {
            "head_authoritative": True,
            "active_block_coherence": True,
            "active_block_status_coherence": True,
            "next_action_coherence": True,
            "unknown_identity_resolution_explicit": True,
            "unknown_resolution_count": len(unknown_info["resolved"]) + len(unknown_info["superseded"]),
            "still_unknown_count": len(unknown_info["still_unknown"]),
            "proof_commit_references_valid": True,
            "baton_generated_from_current_state": True,
            "canonical_hub_sha_coherence": True,
        },
        "head": head_info,
        "active_block": active_info,
        "next_actions": actions,
        "unknown_resolution": unknown_info,
        "proof": proof_info,
        "baton": baton_info,
        "canonical_hub": hub_info,
    }


def failure_report(root: Path, error: Exception) -> dict[str, Any]:
    try:
        live_head = git(root, "rev-parse", "HEAD")
    except Exception:
        live_head = None
    return {
        "schema": "NAYANET_CONTROL_PLANE_FRESHNESS_AUDIT_V2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "live_head": live_head,
        "status": "RED",
        "first_divergence": str(error),
        "checks": {"freshness": False},
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    output = root / "control-plane-freshness-audit.json"
    try:
        report = validate_all(root)
    except Exception as exc:
        report = failure_report(root, exc)
        write_report(output, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        print(f"FRESHNESS=RED\nFIRST_DIVERGENCE={exc}", file=sys.stderr)
        return 1
    write_report(output, report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
