#!/usr/bin/env python3
"""Real Naya Session records (Permanent Temporal Operating Contract, Priority 1).

A SESSION is a real execution period of the Naya runtime: it is opened
automatically when an execution is CLAIMED, records the approved preflight when
that execution reaches EXECUTING, is bound to every Activity the runtime
auto-emits at VERIFIED, and is closed -- with results, evidence, and a successor
handoff -- when the execution is HANDED_OFF.

Sessions live outside the canonical event store on purpose: they are mutable
envelopes (OPEN -> COMPLETED), while the canonical event store stays
append-only. The enforceable law is:
    * do not create an Activity without a real Session (VERIFIED enforces it);
    * do not close a Session that was never opened, and never close twice
      (HANDED_OFF enforces it);
    * a completed execution must have a fully bound, completed Session
      (validate() enforces it).
"""
from __future__ import annotations

import json
import re
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
SESSIONS_ROOT = ROOT / ".naya" / "memory" / "sessions"
SESSIONS_INDEX_PATH = SESSIONS_ROOT / "INDEX.json"

SESSION_ID_RE = re.compile(r"^NAYA-[0-9]{8}-[0-9]{6}-[0-9A-F]{4}$")
SCHEMA = "naya-session/v1"
DEFAULT_PROJECT_ID = "NayaPOWER"
DEFAULT_REPOSITORY = "SoulSchoolAcademy/NayaPOWER"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _real_timestamp(value: str, label: str, problems: list[str]) -> None:
    if not value or not isinstance(value, str):
        problems.append(f"{label} is not a real timestamp")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        problems.append(f"{label} is not a real timestamp")


def _git(command: list[str]) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", *command],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
            timeout=10,
        )
    except Exception:
        return None
    value = result.stdout.strip() if result.returncode == 0 else ""
    return value or None


def _git_branch() -> Optional[str]:
    return _git(["branch", "--show-current"])


def _git_head() -> Optional[str]:
    return _git(["rev-parse", "HEAD"])


def _session_id() -> str:
    stamp = datetime.now(timezone.utc)
    for _ in range(64):
        candidate = f"NAYA-{stamp:%Y%m%d-%H%M%S}-{secrets.token_hex(2).upper()}"
        if not (SESSIONS_ROOT / f"{candidate}.json").exists():
            return candidate
    raise AssertionError("session id collision")


def _paths(sessions_root: Optional[Path], index_path: Optional[Path]) -> tuple[Path, Path]:
    root = Path(sessions_root) if sessions_root else SESSIONS_ROOT
    index = Path(index_path) if index_path else root / "INDEX.json"
    return root, index


def _write(envelope: dict[str, Any], sessions_root: Path, index_path: Path) -> dict[str, Any]:
    sessions_root.mkdir(parents=True, exist_ok=True)
    envelope["updated_at"] = _now()
    path = sessions_root / f"{envelope['session_id']}.json"
    path.write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # The index always lives beside the envelope root it describes; callers that
    # supply only a root (preflight/activity binding) never touch a store-wide
    # (possibly real) index with rows drawn from a temporary root.
    index_path = Path(index_path) if index_path is not None else sessions_root / "INDEX.json"
    _rebuild_index(sessions_root, index_path)
    return envelope


def _rebuild_index(sessions_root: Path, index_path: Path) -> None:
    rows: list[dict[str, Any]] = []
    for candidate in sorted(sessions_root.glob("NAYA-*.json")):
        try:
            session = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows.append(
            {
                "session_id": session.get("session_id", candidate.stem),
                "claim_id": session.get("execution", {}).get("claim_id"),
                "action_id": session.get("execution", {}).get("action_id"),
                "run_id": session.get("execution", {}).get("run_id"),
                "entered_at": session.get("entered_at"),
                "status": session.get("status"),
                "path": str(candidate.relative_to(sessions_root)),
            }
        )
    rows.sort(key=lambda row: (row.get("entered_at") or "", row["session_id"]))
    data = {
        "version": "1.0.0",
        "status": "CANONICAL",
        "organization": "SESSIONS",
        "session_count": len(rows),
        "sessions": rows,
    }
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_session(session_id: str, *, sessions_root: Optional[Path] = None) -> Optional[dict[str, Any]]:
    root, _ = _paths(sessions_root, None)
    candidate = root / f"{session_id}.json"
    if not candidate.exists():
        return None
    try:
        session = json.loads(candidate.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return session if session.get("session_id") == session_id else None


def find_session_by_execution(
    *,
    claim_id: str,
    run_id: str,
    sessions_root: Optional[Path] = None,
) -> Optional[dict[str, Any]]:
    root, _ = _paths(sessions_root, None)
    if not root.exists():
        return None
    for candidate in root.glob("NAYA-*.json"):
        try:
            session = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
        execution = session.get("execution") or {}
        if execution.get("claim_id") == claim_id and execution.get("run_id") == run_id:
            return session
    return None


def open_session(
    *,
    claim_id: str,
    run_id: str,
    owner: str,
    scope: list[str],
    start_head: str,
    block_id: Optional[str] = None,
    action_id: Optional[str] = None,
    project_id: str = DEFAULT_PROJECT_ID,
    repository: str = DEFAULT_REPOSITORY,
    branch: Optional[str] = None,
    restored_context: Any = None,
    sessions_root: Optional[Path] = None,
    index_path: Optional[Path] = None,
) -> dict[str, Any]:
    if not claim_id or not run_id or not owner or not start_head:
        raise AssertionError("session requires claim_id, run_id, owner, and start_head")
    root, index = _paths(sessions_root, index_path)
    existing = find_session_by_execution(claim_id=claim_id, run_id=run_id, sessions_root=root)
    if existing is not None:
        return {"status": "REPLAY", "session_id": existing["session_id"], "session": existing}
    session_id = _session_id()
    entered_at = _now()
    envelope = {
        "schema": SCHEMA,
        "event_type": "session",
        "session_id": session_id,
        "status": "OPEN",
        "entered_at": entered_at,
        "exited_at": None,
        "actor": {"actor_id": owner},
        "execution": {
            "claim_id": claim_id,
            "block_id": block_id,
            "action_id": action_id,
            "run_id": run_id,
        },
        "project": {
            "project_id": project_id,
            "repository": repository,
            "branch": branch or _git_branch(),
            "head_before": start_head,
            "head_after": None,
        },
        "restored_context": restored_context,
        "preflight": None,
        "preflight_verdict": None,
        "actions": [],
        "evidence": [],
        "results": [],
        "handoff": None,
        "next_action": None,
        "successor": None,
        "created_at": entered_at,
        "updated_at": entered_at,
    }
    envelope = _write(envelope, root, index)
    return {"status": "CREATED", "session_id": session_id, "session": envelope}


def _require_open(session_id: str, *, sessions_root: Optional[Path] = None) -> dict[str, Any]:
    session = load_session(session_id, sessions_root=sessions_root)
    if session is None:
        raise AssertionError(f"session integrity: no Session record found for {session_id!r}")
    if session.get("status") != "OPEN":
        raise AssertionError(f"session integrity: Session {session_id} is not OPEN (status={session.get('status')!r})")
    return session


def record_preflight(
    session_id: str,
    preflight: Any,
    verdict: str = "APPROVED",
    *,
    action_id: Optional[str] = None,
    sessions_root: Optional[Path] = None,
) -> dict[str, Any]:
    root, index = _paths(sessions_root, None)
    session = _require_open(session_id, sessions_root=root)
    session["preflight"] = preflight
    session["preflight_verdict"] = verdict
    if action_id:
        session["execution"]["action_id"] = action_id
    return _write(session, root, index)


def bind_activity(
    session_id: str,
    activity_event_id: str,
    action_id: Optional[str] = None,
    *,
    sessions_root: Optional[Path] = None,
) -> dict[str, Any]:
    if not activity_event_id:
        raise AssertionError("session integrity: cannot bind an empty activity_event_id")
    root, index = _paths(sessions_root, None)
    session = _require_open(session_id, sessions_root=root)
    actions = session.setdefault("actions", [])
    if not any(item.get("activity_event_id") == activity_event_id for item in actions):
        actions.append(
            {
                "activity_event_id": activity_event_id,
                "action_id": action_id,
                "recorded_at": _now(),
            }
        )
    if action_id:
        session["execution"]["action_id"] = action_id
    return _write(session, root, index)


def close_session(
    session_id: str,
    *,
    evidence: list[str],
    next_action: str,
    successor: str,
    results: Optional[list[Any]] = None,
    head_after: Optional[str] = None,
    sessions_root: Optional[Path] = None,
    index_path: Optional[Path] = None,
) -> dict[str, Any]:
    root, index = _paths(sessions_root, index_path)
    session = _require_open(session_id, sessions_root=root)
    if not evidence:
        raise AssertionError("session integrity: closing a Session requires evidence")
    if not next_action:
        raise AssertionError("session integrity: closing a Session requires a next action")
    if not successor:
        raise AssertionError("session integrity: closing a Session requires a successor")
    exited_at = _now()
    session.update(
        {
            "status": "COMPLETED",
            "exited_at": exited_at,
            "evidence": evidence,
            "results": results or [],
            "handoff": {"next_action": next_action, "successor": successor},
            "next_action": next_action,
            "successor": successor,
            "project": dict(session.get("project") or {}, head_after=head_after or _git_head()),
        }
    )
    session = _write(session, root, index)
    return {"status": "COMPLETED", "session_id": session_id, "session": session}


def session_integrity(
    session: dict[str, Any],
    *,
    expected_claim_id: str,
    expected_run_id: str,
    need_closed: bool,
) -> tuple[bool, list[str]]:
    problems: list[str] = []
    session_id = session.get("session_id")
    if not SESSION_ID_RE.match(str(session_id or "")):
        problems.append("session_id has an invalid format")
    if session.get("status") not in {"OPEN", "COMPLETED"}:
        problems.append("session has an invalid status")
    _real_timestamp(session.get("entered_at"), "entered_at", problems)
    execution = session.get("execution") or {}
    if execution.get("claim_id") != expected_claim_id:
        problems.append("session is not bound to this execution claim")
    if execution.get("run_id") != expected_run_id:
        problems.append("session is not bound to this execution run")
    if not session.get("actor") or not session.get("actor", {}).get("actor_id"):
        problems.append("session has no actor")
    project = session.get("project") or {}
    if not project.get("head_before"):
        problems.append("session has no head_before")
    if need_closed:
        if session.get("status") != "COMPLETED":
            problems.append("closed execution has no COMPLETED Session record")
        else:
            _real_timestamp(session.get("exited_at"), "exited_at", problems)
            if not session.get("evidence"):
                problems.append("completed Session has no evidence")
            if not session.get("next_action"):
                problems.append("completed Session has no next action")
            if not session.get("successor"):
                problems.append("completed Session has no successor")
            if not project.get("head_after"):
                problems.append("completed Session has no head_after")
    else:
        if session.get("status") != "OPEN":
            problems.append("active execution Session is already closed")
    return (not problems), problems


__all__ = [
    "open_session",
    "close_session",
    "record_preflight",
    "bind_activity",
    "load_session",
    "find_session_by_execution",
    "session_integrity",
    "SESSIONS_ROOT",
    "SESSIONS_INDEX_PATH",
    "SESSION_ID_RE",
    "SCHEMA",
]