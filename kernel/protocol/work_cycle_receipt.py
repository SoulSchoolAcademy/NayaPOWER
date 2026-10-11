"""
work_cycle_receipt.py — validates pre-work sign-in and end-of-cycle sign-out.

GitHub comments remain the canonical work record. This module validates a
record whose linked comment has already been fetched from GitHub; it does not
perform network I/O and does not trust the boolean "observed" flag by itself.
The calling boot CLI must compare the exact fetched comment body and URL.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from typing import Any


REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
ARCHIVED_FEED_ISSUES = {1354}
BOOTSTRAP_LIVE_FEEDS = {
    1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 2175,
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
RECEIPT_START = "<!-- NAYA-WORK-CYCLE-RECEIPT:START -->"
RECEIPT_END = "<!-- NAYA-WORK-CYCLE-RECEIPT:END -->"


SIGN_IN_FIELDS = (
    "task", "owner", "objective", "definition_of_done", "current_main_sha",
    "authority_and_gates", "known_unknowns_and_blockers", "first_action",
    "proof_target", "timestamp",
)
SIGN_OUT_FIELDS = (
    "actual_result", "tested_revision", "evidence_links", "truth_status",
    "claim_limits", "score", "score_delta", "failure_or_root_cause",
    "remaining_blockers_and_owner", "lesson_or_NO_CAPTURE", "next_owner",
    "exactly_one_next_action", "timestamp", "sign_in_comment_id",
    "current_main_sha",
)


@dataclass
class ReceiptCheck:
    passed: bool
    failures: list[str] = field(default_factory=list)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _allowed_feeds(live_feed_issues: set[int] | None) -> set[int]:
    feeds = set(BOOTSTRAP_LIVE_FEEDS if live_feed_issues is None else live_feed_issues)
    feeds.difference_update(ARCHIVED_FEED_ISSUES)
    return feeds


def _body_payload(record: dict, failures: list[str], label: str) -> dict | None:
    body = record.get("comment_body")
    if not _nonempty(body):
        failures.append(f"{label}: actual fetched GitHub comment body is required.")
        return None
    body_sha = record.get("comment_body_sha256")
    if not isinstance(body_sha, str) or not SHA256.fullmatch(body_sha):
        failures.append(f"{label}: comment_body_sha256 must be a 64-character SHA-256.")
    elif hashlib.sha256(body.encode("utf-8")).hexdigest() != body_sha:
        failures.append(f"{label}: body does not match its SHA-256.")
    if record.get("github_comment_observed") is not True:
        failures.append(f"{label}: caller must fetch and compare the actual GitHub comment.")
    if RECEIPT_START not in body or RECEIPT_END not in body:
        failures.append(f"{label}: structured receipt markers are missing from the posted comment.")
        return None
    try:
        raw = body.split(RECEIPT_START, 1)[1].split(RECEIPT_END, 1)[0].strip()
        payload = json.loads(raw)
    except (ValueError, IndexError, TypeError):
        failures.append(f"{label}: structured receipt payload is not valid JSON.")
        return None
    if not isinstance(payload, dict):
        failures.append(f"{label}: structured receipt payload must be a JSON object.")
        return None
    return payload


def _comment_link(record: dict, payload: dict, failures: list[str], label: str, allowed: set[int]) -> None:
    issue = record.get("feed_issue")
    comment_id = record.get("comment_id")
    expected_url = f"https://github.com/{REPOSITORY}/issues/{issue}#issuecomment-{comment_id}"
    if not isinstance(issue, int) or issue in ARCHIVED_FEED_ISSUES or issue not in allowed:
        failures.append(f"{label}: feed is not in the current live-feed registry; archived #1354 is never valid.")
    if not isinstance(comment_id, (str, int)) or not str(comment_id).isdigit():
        failures.append(f"{label}: actual GitHub comment ID is required.")
    if record.get("comment_url") != expected_url:
        failures.append(f"{label}: comment URL must bind the exact issue and comment ID.")
    if payload.get("feed_issue") != issue:
        failures.append(f"{label}: posted payload feed_issue differs from the resolved live feed.")
    if payload.get("agent_id") != record.get("agent_id"):
        failures.append(f"{label}: posted payload agent_id differs from receipt metadata.")
    if payload.get("event_type") != record.get("event_type"):
        failures.append(f"{label}: posted payload event_type differs from receipt metadata.")


def _compare_payload(record: dict, payload: dict, fields: tuple[str, ...], failures: list[str], label: str) -> None:
    required = set(fields) | {"event_type", "feed_issue", "agent_id"}
    for key in sorted(required):
        if key not in payload:
            failures.append(f"{label}: structured comment payload is missing {key}.")
        elif payload[key] != record.get(key):
            failures.append(f"{label}: structured comment payload disagrees on {key}.")


def check_sign_in(
    record: dict,
    current_main_sha: str,
    live_feed_issues: set[int] | None = None,
) -> ReceiptCheck:
    failures: list[str] = []
    label = "SIGN_IN"
    if not isinstance(record, dict):
        return ReceiptCheck(False, [f"{label}: receipt must be a JSON object."])
    if record.get("event_type") != "SIGN_IN":
        failures.append(f"{label}: event_type must equal SIGN_IN.")
    for field_name in SIGN_IN_FIELDS:
        if not _nonempty(record.get(field_name)):
            failures.append(f"{label}: required field {field_name} is empty or missing.")
    if not isinstance(record.get("current_main_sha"), str) or not SHA40.fullmatch(record.get("current_main_sha", "")):
        failures.append(f"{label}: current_main_sha must be a full Git SHA.")
    elif record.get("current_main_sha") != current_main_sha:
        failures.append(f"{label}: sign-in is stale relative to current origin/main.")
    allowed = _allowed_feeds(live_feed_issues)
    payload = _body_payload(record, failures, label)
    if payload is not None:
        _comment_link(record, payload, failures, label, allowed)
        _compare_payload(record, payload, SIGN_IN_FIELDS, failures, label)
    return ReceiptCheck(not failures, failures)


def check_sign_out(
    sign_in: dict,
    sign_out: dict,
    current_main_sha: str,
    live_feed_issues: set[int] | None = None,
) -> ReceiptCheck:
    failures: list[str] = []
    if not isinstance(sign_in, dict) or not isinstance(sign_out, dict):
        return ReceiptCheck(False, ["SIGN_OUT: matching sign-in and sign-out receipts are required."])
    sign_in_result = check_sign_in(sign_in, sign_in.get("current_main_sha", ""), live_feed_issues)
    failures.extend(f"Referenced SIGN_IN invalid: {item}" for item in sign_in_result.failures)
    label = "SIGN_OUT"
    if sign_out.get("event_type") != "SIGN_OUT":
        failures.append(f"{label}: event_type must equal SIGN_OUT.")
    for field_name in SIGN_OUT_FIELDS:
        value = sign_out.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            failures.append(f"{label}: required field {field_name} is empty or missing.")
    if sign_out.get("agent_id") != sign_in.get("agent_id"):
        failures.append(f"{label}: agent_id differs from SIGN_IN.")
    if sign_out.get("feed_issue") != sign_in.get("feed_issue"):
        failures.append(f"{label}: must use the same live specialist feed as SIGN_IN.")
    if str(sign_out.get("sign_in_comment_id", "")) != str(sign_in.get("comment_id", "")):
        failures.append(f"{label}: must reference the exact SIGN_IN GitHub comment ID.")
    if sign_out.get("current_main_sha") != current_main_sha or not SHA40.fullmatch(str(sign_out.get("current_main_sha", ""))):
        failures.append(f"{label}: current_main_sha must match the current origin/main.")
    if not SHA40.fullmatch(str(sign_out.get("tested_revision", ""))):
        failures.append(f"{label}: tested_revision must be a full Git SHA.")
    evidence = sign_out.get("evidence_links")
    if not isinstance(evidence, list) or not evidence or not all(_nonempty(link) for link in evidence):
        failures.append(f"{label}: evidence_links must be a non-empty list of evidence URLs/paths.")
    score = sign_out.get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool) or not math.isfinite(score) or not 0 <= score <= 10:
        failures.append(f"{label}: score must be finite and in [0, 10].")
    delta = sign_out.get("score_delta")
    if not isinstance(delta, (int, float)) or isinstance(delta, bool) or not math.isfinite(delta):
        failures.append(f"{label}: score_delta must be finite numeric and must not treat unknown as zero.")
    lesson = sign_out.get("lesson_or_NO_CAPTURE")
    if _nonempty(lesson) and lesson != "NO_CAPTURE" and not (lesson.startswith("SN-") or lesson.startswith("http://") or lesson.startswith("https://")):
        failures.append(f"{label}: lesson must be NO_CAPTURE or a canonical lesson link/ID.")
    allowed = _allowed_feeds(live_feed_issues)
    payload = _body_payload(sign_out, failures, label)
    if payload is not None:
        _comment_link(sign_out, payload, failures, label, allowed)
        _compare_payload(sign_out, payload, SIGN_OUT_FIELDS, failures, label)
    return ReceiptCheck(not failures, failures)
