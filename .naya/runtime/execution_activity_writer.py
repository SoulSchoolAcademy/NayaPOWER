#!/usr/bin/env python3
"""Write-authorized execution-boundary Team Naya Activity writer."""
from __future__ import annotations

import os
import re
import tempfile
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
ACTIVITY_ROOT = ROOT / "NAYA-TEAM"
VANCOUVER = ZoneInfo("America/Vancouver")
EVENT_ID_RE = re.compile(r"^SE-[0-9]{8}-[0-9]{6}-[a-z0-9-]+$")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_authorized_execution(execution: dict[str, Any]) -> None:
    required = ("claim_id", "action_id", "decision_id", "authority_id",
                "actor_id", "run_id", "session_id")
    missing = [key for key in required if not execution.get(key)]
    if missing:
        raise AssertionError(
            "Activity writer refused: missing authorized execution binding: "
            + ", ".join(missing)
        )
    state = execution.get("governance_state")
    if state not in (None, "AUTHORIZED"):
        raise AssertionError("Activity writer refused: execution is not AUTHORIZED")
    if execution.get("authorization_verified") is not True:
        raise AssertionError(
            "Activity writer refused: Universal Execution Gate authorization was not verified"
        )


def _local_stamp(effective_at: str) -> datetime:
    stamp = datetime.fromisoformat(effective_at.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise AssertionError("Activity writer refused: effective_at must include timezone")
    return stamp.astimezone(VANCOUVER)


def _slug(subject: str, event_id: str) -> str:
    raw = re.sub(r"[^A-Za-z0-9]+", "-", subject).strip("-").lower()
    raw = raw[:60] or "execution"
    return f"{raw}-{event_id.rsplit('-', 1)[-1]}"


def _record_path(effective_at: str, subject: str, event_id: str, root: Path) -> Path:
    stamp = _local_stamp(effective_at)
    filename = (
        f"{stamp:%Y-%m-%dT%H-%M-%S%z}__NAYA-EXECUTION-"
        f"{_slug(subject, event_id)}.md"
    )
    return root / f"{stamp:%Y/%m/%d}" / filename
def _section(*, effective_at: str, event_id: str, execution: dict[str, Any],
             subject: str, summary: str, evidence: list[str],
             next_action: str, successor: str) -> str:
    evidence_lines = "\n".join("- " + item for item in evidence) or "- none recorded"
    return (
        "\n\n---\n\n"
        "# " + effective_at[:10] + " — Team Naya Automatic Execution Activity\n\n"
        "**Session:** " + execution["session_id"] + "  \n"
        "**Claim:** " + execution["claim_id"] + "  \n"
        "**Action:** " + execution["action_id"] + "  \n"
        "**Run:** " + execution["run_id"] + "  \n"
        "**Authority:** " + execution["authority_id"] + "  \n"
        "**Actor:** " + execution["actor_id"] + "  \n"
        "**EVENT:** `" + event_id + "`\n\n"
        "## WHAT HAPPENED\n\n"
        "- " + subject + "\n"
        "- " + summary + "\n\n"
        "## VERIFIED EVIDENCE\n\n"
        + evidence_lines + "\n"
        "- canonical Activity event: `" + event_id + "`\n\n"
        "## HANDOFF\n\n"
        "**Next action:** " + next_action + "  \n"
        "**Successor:** " + successor + "\n\n"
        "**Activity status:** DURABLY_RECORDED\n"
    )


def _write_once(path: Path, content: str, event_id: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if f"**EVENT:** `{event_id}`" in existing:
            return False
        raise AssertionError(
            f"Activity writer conflict: target record already exists for another event: {path}"
        )
    fd, temp_name = tempfile.mkstemp(prefix=".activity-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise
    return True
def write_execution_activity(*, event: dict[str, Any],
                              execution: dict[str, Any],
                              next_action: str, successor: str,
                              evidence: list[str],
                              activity_root: Optional[Path] = None) -> dict[str, Any]:
    """Persist the durable Team Naya record for an already-authorized execution."""
    _require_authorized_execution(execution)
    event_id = str(event.get("event_id", ""))
    if not EVENT_ID_RE.match(event_id):
        raise AssertionError("Activity writer refused: invalid canonical event_id")
    if event.get("event_type") != "activity":
        raise AssertionError("Activity writer refused: event is not canonical Activity")
    if (event.get("continuity") or {}).get("execution_state") != "COMPLETED":
        raise AssertionError("Activity writer refused: execution is not COMPLETED")

    root = Path(activity_root) if activity_root else ACTIVITY_ROOT
    effective_at = str(event.get("effective_at") or _now())
    subject = str(event.get("subject") or "Consequential Naya execution completed")
    path = _record_path(effective_at, subject, event_id, root)
    section = _section(
        effective_at=effective_at,
        event_id=event_id,
        execution=execution,
        subject=subject,
        summary=str((event.get("activity_feed_projection") or {}).get("summary") or ""),
        evidence=evidence,
        next_action=next_action,
        successor=successor,
    )
    created = _write_once(path, section, event_id)
    return {"status": "CREATED" if created else "REPLAY", "event_id": event_id, "path": str(path)}


def find_daily_activity(event_id: str, *, activity_root: Optional[Path] = None) -> Optional[Path]:
    root = Path(activity_root) if activity_root else ACTIVITY_ROOT
    needle = "**EVENT:** `" + event_id + "`"
    if not root.exists():
        return None
    for path in root.rglob("*.md"):
        try:
            if needle in path.read_text(encoding="utf-8"):
                return path
        except OSError:
            continue
    return None


__all__ = ["write_execution_activity", "find_daily_activity", "ACTIVITY_ROOT"]
