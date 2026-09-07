#!/usr/bin/env python3
"""Deterministic NayaPOWER Superbrain restore runtime.

Restores repository reality, canonical orientation, current project state,
durable learning, and successor continuity. Repository reality is primary;
orientation documents are projections and contradictions are never silently
accepted.

Standard-library only. No network access is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
NAYA = ROOT / ".naya"
MEMORY = NAYA / "memory"
STATE_PATH = MEMORY / "STATE.json"
MANIFEST_PATH = NAYA / "naya-context-manifest.json"
BRIEFING_PATH = MEMORY / "NAYAPOWER-RUNTIME-BRIEFING.md"
FEED_PATH = NAYA / "INTELLIGENT-FEED.md"
PROJECT_PATH = NAYA / "projects" / "CURRENT-PROJECT.md"
START_PATH = ROOT / "START-HERE.md"
CHECKPOINT_DIR = NAYA / "checkpoints"
HANDOFF_DIR = NAYA / "handoffs"

import sys
sys.path.insert(0, str(MEMORY))
from memory_runtime import load_json, notes, retrieve, validate  # noqa: E402

ISO_Z_RE = re.compile(r"Z$")
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
CURRENT_HEAD_RE = re.compile(
    r"(?im)^\s*(?:live|current|observed)\s+`?(?:main|head|git head)`?.{0,120}?\b([0-9a-f]{40})\b"
)


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    value = ISO_Z_RE.sub("+00:00", value)
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def now() -> datetime:
    return datetime.now(timezone.utc)


def run_git(*args: str) -> str | None:
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True)
        return p.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def repository_reality(at: datetime | None = None) -> dict[str, Any]:
    if at is None:
        head = run_git("rev-parse", "HEAD")
        branch = run_git("branch", "--show-current")
        status = run_git("status", "--porcelain")
        commit = run_git("show", "-s", "--format=%H|%cI|%s", "HEAD")
    else:
        stamp = at.isoformat()
        head = run_git("log", "-1", "--format=%H", f"--before={stamp}")
        branch = run_git("branch", "--show-current")
        status = None
        commit = run_git("show", "-s", "--format=%H|%cI|%s", head) if head else None
    parts = commit.split("|", 2) if commit else []
    return {
        "available": head is not None,
        "root": str(ROOT),
        "branch": branch,
        "head_sha": head,
        "clean": status == "",
        "working_tree_status": status,
        "commit": {"sha": parts[0] if len(parts) > 0 else None, "timestamp": parts[1] if len(parts) > 1 else None, "subject": parts[2] if len(parts) > 2 else None},
        "historical": at is not None,
        "requested_at": at.isoformat() if at else None,
    }


def load_state() -> dict[str, Any]:
    return load_json(STATE_PATH)


def load_manifest() -> dict[str, Any]:
    return load_json(MANIFEST_PATH)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return ""


def current_head_declarations(text: str) -> list[str]:
    """Return only SHAs presented as current/live/observed head declarations.

    Historical SHA references are intentionally ignored. This prevents every
    new commit from making the orientation layer falsely appear contradictory.
    """
    return CURRENT_HEAD_RE.findall(text)


def orientation_projection(path: Path, actual_head: str | None) -> dict[str, Any]:
    body = read_text(path)
    declarations = current_head_declarations(body)
    matches = bool(actual_head and actual_head in declarations)
    mismatch = bool(actual_head and declarations and actual_head not in declarations)
    return {
        "path": str(path.relative_to(ROOT)),
        "available": bool(body),
        "current_head_declaration_count": len(declarations),
        "declared_current_heads": declarations[:20],
        "matches_observed_head": matches,
        "head_mismatch": mismatch,
    }


def extract_section(text: str, heading: str) -> str | None:
    marker = f"## {heading}"
    if marker not in text:
        return None
    tail = text.split(marker, 1)[1]
    return tail.split("\n## ", 1)[0].strip()


def latest_handoff() -> dict[str, Any] | None:
    """Select the latest tracked handoff deterministically.

    Filesystem mtimes are not stable across Git checkout/clone operations, so
    Git commit history is preferred. Filesystem mtime is only a fallback for
    untracked/local handoffs.
    """
    if not HANDOFF_DIR.exists():
        return None
    files = [p for p in HANDOFF_DIR.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".json"}]
    if not files:
        return None
    ranked: list[tuple[str, str, Path]] = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        committed = run_git("log", "-1", "--format=%cI", "--", rel)
        if committed:
            ranked.append((committed, "git", path))
    if ranked:
        _, _, path = max(ranked, key=lambda item: (item[0], item[2].as_posix()))
    else:
        path = max(files, key=lambda p: (p.stat().st_mtime_ns, p.as_posix()))
    return {"path": str(path.relative_to(ROOT)), "content": read_text(path)}


def orientation_snapshot(repo: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    actual = repo.get("head_sha")
    briefing = read_text(BRIEFING_PATH)
    feed = read_text(FEED_PATH)
    project = read_text(PROJECT_PATH)
    start = read_text(START_PATH)
    projections = [orientation_projection(p, actual) for p in (BRIEFING_PATH, FEED_PATH, PROJECT_PATH, START_PATH)]
    state_head = (((state.get("current_main") or {}).get("commit")) if isinstance(state, dict) else None)
    mismatches = [p["path"] for p in projections if p["head_mismatch"]]
    if state_head and actual and state_head != actual:
        mismatches.append(str(STATE_PATH.relative_to(ROOT)))
    contradictions: list[str] = []
    if not briefing:
        contradictions.append("missing Runtime Briefing")
    if not feed:
        contradictions.append("missing Intelligent Feed")
    if not project:
        contradictions.append("missing CURRENT-PROJECT")
    if not start:
        contradictions.append("missing START-HERE")
    if actual and mismatches:
        contradictions.append("current-head projection mismatch")
    if "MaxRESULTS" in start and "NayaPOWER" in briefing and "central" in briefing.lower():
        if "central Superbrain" not in start and "central" not in start.lower():
            contradictions.append("START-HERE does not explicitly distinguish NayaPOWER Superbrain from MAXESS project authority")
    next_actions = []
    for label, body in (("briefing", briefing), ("feed", feed), ("project", project)):
        section = extract_section(body, "NEXT ACTION") or extract_section(body, "NEXT EXECUTION")
        if section:
            next_actions.append({"source": label, "text": section})
    return {
        "canonical_identity": "SoulSchoolAcademy/NayaPOWER",
        "observed_head": actual,
        "state_declared_head": state_head,
        "projections": projections,
        "mismatches": sorted(set(mismatches)),
        "contradictions": contradictions,
        "next_actions": next_actions,
        "latest_handoff": latest_handoff(),
    }


def note_is_visible(note: dict[str, Any], at: datetime | None) -> bool:
    status = note.get("status")
    if status == "SUPERSEDED" and note.get("superseded_at"):
        return False if at is None else parse_time(note["superseded_at"]) <= at
    if status == "STALE" and at is None:
        return False
    if at is None:
        return status not in {"SUPERSEDED", "STALE"}
    effective = parse_time(note.get("effective_at"))
    if effective and effective > at:
        return False
    if note.get("superseded_at") and parse_time(note["superseded_at"]) <= at:
        return False
    return True


def memory_snapshot(query: str, at: datetime | None, limit: int) -> dict[str, Any]:
    visible = []
    for _, note in notes():
        if "__parse_error__" in note or not note_is_visible(note, at):
            continue
        visible.append(note)
    if query:
        ranked = [(score, note) for score, note in retrieve(query, max(limit * 3, 10)) if note in visible]
        ranked.sort(key=lambda item: (-item[0], item[1].get("effective_at", ""), item[1].get("id", "")))
        selected = [n for _, n in ranked[:limit]]
    else:
        selected = sorted(visible, key=lambda n: (n.get("effective_at", ""), n.get("id", "")), reverse=True)[:limit]
    counts: dict[str, int] = {}
    for note in visible:
        status = note.get("status", "UNKNOWN")
        counts[status] = counts.get(status, 0) + 1
    conflicts = [n for n in visible if n.get("status") == "CONFLICTED"]
    return {"count_visible": len(visible), "counts_by_status": counts, "conflicts": [n.get("id") for n in conflicts], "selected": selected}


def stale_memory() -> list[dict[str, Any]]:
    out = []
    for path, note in notes():
        if "__parse_error__" in note:
            out.append({"path": str(path), "reason": "parse_error"})
        elif note.get("status") in {"STALE", "CONFLICTED", "SUPERSEDED"}:
            out.append({"id": note.get("id"), "title": note.get("title"), "status": note.get("status"), "path": str(path)})
    return out


def proof_target(project_text: str, state: dict[str, Any]) -> str | None:
    section = extract_section(project_text, "NEXT EXECUTION")
    if section:
        return section
    value = state.get("proof_target")
    return value if isinstance(value, str) else None


def build_restore(query: str = "", at: str | None = None, limit: int = 10) -> dict[str, Any]:
    target = parse_time(at)
    state = load_state()
    manifest = load_manifest()
    structural_errors = validate()
    repo = repository_reality(target)
    orientation = orientation_snapshot(repo, state) if not target else {"historical": True}
    project_text = read_text(PROJECT_PATH)
    memory = memory_snapshot(query, target, limit)
    reconciliation_required = bool(orientation.get("contradictions") or orientation.get("mismatches")) if not target else False
    status = "RECONCILIATION_REQUIRED" if reconciliation_required else ("VERIFIED" if not structural_errors and repo["available"] else "UNKNOWN")
    return {
        "schema": "naya-power-restore-context/v3",
        "status": status,
        "generated_at": now().isoformat(),
        "mode": "RESTORE-TIME" if target else "RESTORE-STANDARD",
        "requested_at": target.isoformat() if target else None,
        "authority": manifest.get("authority_rules", {}),
        "current_state": state,
        "repository_reality": repo,
        "orientation": orientation,
        "memory": memory,
        "stale_or_superseded": stale_memory(),
        "validation": {"passed": not structural_errors, "errors": structural_errors},
        "mission": state.get("current_mission"),
        "protected": state.get("protected", []),
        "known": ["Canonical repository is SoulSchoolAcademy/NayaPOWER", "Runtime Briefing + Intelligent Feed + Current Project are orientation projections; observed repository reality is primary"],
        "unknown": state.get("unknown", []),
        "what_changed": state.get("recent_changes", []),
        "what_is_unfinished": state.get("unknown", []),
        "current_project": state.get("current_project"),
        "next_best_action": state.get("next_best_action"),
        "proof_target": proof_target(project_text, state),
        "latest_handoff": orientation.get("latest_handoff"),
        "reconciliation": {"required": reconciliation_required, "reasons": orientation.get("contradictions", []) + orientation.get("mismatches", [])},
    }


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def write_artifact(directory: Path, prefix: str, payload: dict[str, Any]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    stamp = now().strftime("%Y%m%dT%H%M%SZ")
    path = directory / f"{prefix}-{stamp}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def checkpoint(restore: dict[str, Any]) -> dict[str, Any]:
    payload = {"schema": "naya-power-checkpoint/v2", "created_at": now().isoformat(), "restore_status": restore["status"], "repository_reality": restore["repository_reality"], "orientation": restore["orientation"], "mission": restore["mission"], "current_state": restore["current_state"], "memory_summary": {"count_visible": restore["memory"]["count_visible"], "counts_by_status": restore["memory"]["counts_by_status"], "conflicts": restore["memory"]["conflicts"]}, "protected": restore["protected"], "unknown": restore["unknown"], "next_best_action": restore["next_best_action"], "proof_target": restore["proof_target"], "reconciliation": restore["reconciliation"], "integrity_sha256": hashlib.sha256(canonical_json(restore).encode("utf-8")).hexdigest()}
    path = write_artifact(CHECKPOINT_DIR, "checkpoint", payload)
    return {"path": str(path.relative_to(ROOT)), "checkpoint": payload}


def handoff(restore: dict[str, Any]) -> dict[str, Any]:
    payload = {"schema": "naya-power-handoff/v3", "created_at": now().isoformat(), "mission": restore["mission"], "current_state": restore["current_state"], "what_changed": restore["what_changed"], "verified": restore["status"] == "VERIFIED", "unknown": restore["unknown"], "protected_elements": restore["protected"], "repository": restore["repository_reality"], "orientation": restore["orientation"], "memory_conflicts": restore["memory"]["conflicts"], "next_best_action": restore["next_best_action"], "proof_target": restore["proof_target"], "reconciliation": restore["reconciliation"]}
    path = write_artifact(HANDOFF_DIR, "handoff", payload)
    return {"path": str(path.relative_to(ROOT)), "handoff": payload}


def main() -> int:
    ap = argparse.ArgumentParser(description="NayaPOWER Superbrain Restore Context runtime")
    sub = ap.add_subparsers(dest="command", required=True)
    r = sub.add_parser("restore"); r.add_argument("query", nargs="?", default=""); r.add_argument("--at"); r.add_argument("--limit", type=int, default=10); r.add_argument("--pretty", action="store_true")
    c = sub.add_parser("checkpoint"); c.add_argument("query", nargs="?", default=""); c.add_argument("--at")
    h = sub.add_parser("handoff"); h.add_argument("query", nargs="?", default=""); h.add_argument("--at")
    args = ap.parse_args()
    result = build_restore(args.query, args.at, getattr(args, "limit", 10))
    if args.command == "restore":
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
        return 0 if result["status"] == "VERIFIED" else 2
    artifact = checkpoint(result) if args.command == "checkpoint" else handoff(result)
    print(json.dumps(artifact, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "VERIFIED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
