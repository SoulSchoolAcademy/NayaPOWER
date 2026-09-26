#!/usr/bin/env python3
"""Deterministic repository-side Smart Link verifier for INT-001."""
from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

IB_RE = re.compile(r"^IB-\d{6}$")
SMART_NOTES_ROOT = ".naya/memory/smart-notes"
GITHUB_BASE = "https://github.com/SoulSchoolAcademy/NayaPOWER/blob"
CANONICAL_RECEIVER = "v7-smart-note-canonical"

REQUIRED_SMART_NOTE_SECTIONS = (
    "IN A NUTSHELL", "DATE / TIME", "WHAT", "WHY IT MATTERS", "HUMAN",
    "CHILD", "GRANDMA", "NAYA", "MACHINE", "WHAT WE LEARNED",
    "CONNECTIONS", "HOW TO APPLY", "WHAT IT ULTIMATELY MEANS",
    "WHAT'S IN IT FOR YOU / US", "NEXT ACTION",
)

def validate_smart_note_structure(content: str) -> tuple[bool, list[str]]:
    """Validate the required 15-section order without changing IB identity."""
    headings = re.findall(r"^##\s+(.+?)\s*$", content, flags=re.MULTILINE)
    errors = []
    cursor = -1
    for section in REQUIRED_SMART_NOTE_SECTIONS:
        matches = [i for i, heading in enumerate(headings) if heading == section]
        if not matches:
            errors.append(f"missing required section: {section}")
            continue
        position = matches[0]
        if position <= cursor:
            errors.append(f"section order violation at: {section}")
        cursor = position
    return (not errors, errors)

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
    return GITHUB_BASE + "/" + canonical_ref + "/" + path

def classify_link_kind(url: str) -> str:
    """Classify link vocabulary without upgrading its verification state."""
    parsed = urlparse(url)
    path = parsed.path or ""
    query = parse_qs(parsed.query)
    if path == "/hub" and "ib" in query and len(query["ib"]) == 1 and _valid_ib(query["ib"][0]):
        return "HUB_DEEP_LINK"
    if (parsed.scheme == "https" and parsed.netloc == "github.com" and
        path.startswith("/SoulSchoolAcademy/NayaPOWER/blob/") and
        "/.naya/memory/smart-notes/" in path and
        re.search(r"/IB-\d{6}/smart-note\.md$", path)):
        return "SMART_LINK"
    if (parsed.scheme == "https" and parsed.netloc == "github.com" and
        any(token in path for token in ("/commit/", "/pull/", "/issues/", "/actions/"))):
        return "EVIDENCE_LINK"
    return "UNKNOWN"


def verify_remote_smart_link(
    smart_link: str,
    expected_path: str,
    expected_ref: str,
    observed_path: str,
    observed_ref: str,
    observed_ib: str,
) -> bool:
    """Verify an observed remote GitHub target matches the claimed canonical Smart Link."""
    parsed = urlparse(smart_link)
    prefix = "/SoulSchoolAcademy/NayaPOWER/blob/"
    if parsed.scheme != "https" or parsed.netloc != "github.com" or not parsed.path.startswith(prefix):
        return False
    target = parsed.path[len(prefix):].split("/", 1)
    if len(target) != 2:
        return False
    claimed_ref, claimed_path = target
    if claimed_ref != expected_ref or claimed_path != expected_path:
        return False
    if observed_ref != expected_ref or observed_path != expected_path:
        return False
    expected_ib = Path(expected_path).parent.name
    return _valid_ib(expected_ib) and observed_ib == expected_ib

def classify_smart_link(repo_path: Path, reported_ib: str, receiver_persisted: bool, projection_expected: bool, canonical_ref: str = "main") -> str:
    if not _valid_ib(reported_ib) or not receiver_persisted:
        return "UNKNOWN"
    normalized = _repo_relative(repo_path)
    expected_suffix = "/" + reported_ib + "/smart-note.md"
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

def receiver_link_correspondence(repo_path: Path, receiver_record: dict, canonical_ref: str = "main") -> bool:
    """Require the projection to join to the receiver-issued identity and event."""
    if not repo_path.exists():
        return False
    ib_id = receiver_record.get("intelligent_block_id")
    source_event_id = receiver_record.get("source_event_id")
    receiver = receiver_record.get("canonical_receiver", CANONICAL_RECEIVER)
    if not _valid_ib(ib_id) or not source_event_id or not receiver:
        return False
    try:
        content = repo_path.read_text(encoding="utf-8")
    except OSError:
        return False
    normalized = _repo_relative(repo_path)
    if not normalized.endswith("/" + ib_id + "/smart-note.md"):
        return False
    required_fields = (
        "**Intelligent Block ID:** `" + ib_id + "`",
        "**Canonical Source Event:** `" + source_event_id + "`",
        "**Canonical Receiver:** `" + receiver + "`",
    )
    if not all(field in content for field in required_fields):
        return False
    link = build_smart_link(repo_path, canonical_ref)
    return classify_link_kind(link) == "SMART_LINK"

__all__ = ["build_smart_link", "classify_link_kind", "classify_smart_link", "receiver_link_correspondence", "validate_smart_note_structure", "verify_remote_smart_link"]