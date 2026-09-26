#!/usr/bin/env python3
"""Deterministic repository-side Smart Link verifier for INT-001."""
from __future__ import annotations
import re
from pathlib import Path

IB_RE = re.compile(r"^IB-\d{6}$")
SMART_NOTES_ROOT = ".naya/memory/smart-notes"
GITHUB_BASE = "https://github.com/SoulSchoolAcademy/NayaPOWER/blob"


def _valid_ib(value: str) -> bool:
    return bool(IB_RE.fullmatch(value))


def _repo_relative(path: Path) -> str:
    candidate = path.resolve()
    root = Path.cwd().resolve()
    try:
        return candidate.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix().lstrip("/")


def build_smart_link(repo_path: Path, canonical_ref: str = "main") -> str:
    path = _repo_relative(repo_path)
    if not path.startswith(SMART_NOTES_ROOT + "/") or not path.endswith("/smart-note.md"):
        raise ValueError("path is not a canonical Smart Note projection")
    return f"{GITHUB_BASE}/{canonical_ref}/{path}"


def classify_smart_link(
    repo_path: Path,
    reported_ib: str,
    receiver_persisted: bool,
    projection_expected: bool,
    canonical_ref: str = "main",
) -> str:
    if not _valid_ib(reported_ib) or not receiver_persisted:
        return "UNKNOWN"

    normalized = _repo_relative(repo_path)
    expected_suffix = f"/{reported_ib}/smart-note.md"

    if not repo_path.exists():
        return "MISSING" if projection_expected else "PENDING"

    if not normalized.startswith(SMART_NOTES_ROOT + "/") or not normalized.endswith(expected_suffix):
        return "CONFLICTED"

    try:
        content = repo_path.read_text(encoding="utf-8")
    except OSError:
        return "UNKNOWN"

    if reported_ib not in content:
        return "CONFLICTED"

    build_smart_link(repo_path, canonical_ref)
    return "VERIFIED"


__all__ = ["build_smart_link", "classify_smart_link"]
