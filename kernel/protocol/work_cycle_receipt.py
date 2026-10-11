"""
work_cycle_receipt.py — structural validation for feed sign-in/sign-out receipts.

The GitHub specialist feed remains the canonical work log. This module creates
no ledger or second store: it validates the shape and consistency of receipt
data supplied from a live-feed read/write adapter. A caller must independently
fetch the linked comment and set github_comment_observed only after confirming
it exists; this local validator does not make network calls.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from typing import Any


REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
LIVE_FEED_ISSUES = {
    2175, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873,
}
ARCHIVED_FEED_ISSUES = {1354}
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
RECEIPT_START = "<!-- NAYA-WORK-CYCLE-RECEIPT:START -->"
RECEIPT_END = "<!-- NAYA-WORK-CYCLE-RECEIPT:END -->"


@dataclass
class ReceiptCheck:
    passed: bool
    failures: list[str] = field(default_factory=list)


SIGN_IN_FIELDS = (
    "agent_id", "task", "owner", "objective", "definition_of_done",
    "current_main_sha", "authority_and_gates", "known_unknowns_and_blockers",
    "first_action", "proof_target", "timestamp",
)
SIGN_OUT_FIELDS = (
    "agent_id", "actual_result", "tested_revision", "evidence_links",
    "truth_status", "claim_limits", "score", "score_delta",
    "failure_or_root_cause", "remaining_blockers_and_owner",
    "lesson_or_NO_CAPTURE", "next_owner", "exactly_one_next_action", "timestamp",
)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _feed_comment_ok(
    record: dict,
    failures: list[str],
    label: str,
    live_feed_issues: set[int],
) -> None:
    issue = record.get("feed_issue")
    comment_id = record.get("comment_id")
    if not isinstance(issue, int) or issue in ARCHIVED_FEED_ISSUES or issue not in live_feed_issues:
        failures.append(f"{label}: feed_issue must be in the feed registry resolved from current mission/navigation state, not an archive.")
        return
    if not isinstance(comment_id, (str, int)) or not str(comment_id).isdigit():
        failures.append(f"{label}: a numeric GitHub comment_id is required.")
        return
    expected_url = (
        f"https://github.com/{REPOSITORY}/issues/{issue}#issuecomment-{comment_id}"
    )
    if record.get("comment_url") != expected_url:
        failures.append(f"{label}: comment_url must identify this exact issue and comment.")


def _comment_body_ok(record: dict, failures: list[str], label: str) -> None:
    body = record.get("comment_body")
    digest = record.get("comment_body_sha256")
    if not _nonempty(body):
        failures.append(f"{label}: the observed GitHub comment body is required.")
        return
    if not isinstance(digest, str) or not _HEX64_RE.fullmatch(digest):
        failures.append(f"{label}: comment_body_sha256 must be a 64-character SHA-256.")
    elif hashlib.sha256(body.encode("utf-8")).hexdigest() != digest:
        failures.append(f"{label}: comment body does not match comment_body_sha256.")
    if record.get("github_comment_observed") is not True:
        failures.append(
            f"{label}: caller must confirm the linked comment was fetched from the live GitHub feed."
        )

    # The structured payload must be inside the actual posted comment. This
    # binds values like agent_id, main SHA, evidence, score and next action to
    # the remotely observed body rather than trusting a second JSON document.
    if not (RECEIPT_START in body and RECEIPT_END in body):
        failures.append(f"{label}: comment is missing the structured receipt markers.")
        return
    try:
        payload_text = body.split(RECEIPT_START, 1)[1].split(RECEIPT_END, 1)[0].strip()
        payload = json.loads(payload_text)
    except (ValueError, IndexError, TypeError):
        failures.append(f"{label}: structured receipt block is not valid JSON.")
        return
    if not isinstance(payload, dict):
        failures.append(f"{label}: structured receipt block must be a JSON object.")
        return

    event_type = record.get("event_type")
    required = set(SIGN_IN_FIELDS) if event_type == "SIGN_IN" else set(SIGN_OUT_FIELDS)
    required.update({"event_type", "feed_issue"})
    if event_type == "SIGN_OUT":
        required.update({"sign_in_comment_id", "current_main_sha"})
    for field_name in sorted(required):
        if field_name not in payload:
            failures.append(f"{label}: structured comment payload omits {field_name}.")
        elif payload[field_name] != record.get(field_name):
            failures.append(f"{label}: structured comment payload disagrees on {field_name}.")


def check_sign_in(
    record: dict,
    current_main_sha: str,
    live_feed_issues: set[int] | None = None,
) -> ReceiptCheck:
    """Validate sign-in against a current feed registry before work can start."""
    failures: list[str] = []
    allowed_feeds = set(LIVE_FEED_ISSUES if live_feed_issues is None else live_feed_issues)
    allowed_feeds.difference_update(ARCHIVED_FEED_ISSUES)
    if not isinstance(record, dict):
        return ReceiptCheck(False, ["Sign-in receipt must be a mapping."])
    if record.get("event_type") != "SIGN_IN":
        failures.append("Sign-in receipt event_type must be SIGN_IN.")
    for field_name in SIGN_IN_FIELDS:
        if not _nonempty(record.get(field_name)):
            failures.append(f"Sign-in receipt missing required field: {field_name}.")
    _feed_comment_ok(record, failures, "Sign-in receipt", allowed_feeds)
    _comment_body_ok(record, failures, "Sign-in receipt")
    sha = record.get("current_main_sha")
    if not isinstance(sha, str) or not _SHA_RE.fullmatch(sha):
        failures.append("Sign-in receipt must bind to a full current-main SHA.")
    elif not _SHA_RE.fullmatch(current_main_sha or "") or sha != current_main_sha:
        failures.append("Sign-in receipt is stale or does not match the current-main SHA.")
    return ReceiptCheck(not failures, failures)


def check_sign_out(
    sign_in: dict,
    sign_out: dict,
    current_main_sha: str,
    live_feed_issues: set[int] | None = None,
) -> ReceiptCheck:
    """Validate sign-out against the same current feed as the matching sign-in."""
    failures: list[str] = []
    allowed_feeds = set(LIVE_FEED_ISSUES if live_feed_issues is None else live_feed_issues)
    allowed_feeds.difference_update(ARCHIVED_FEED_ISSUES)
    if not isinstance(sign_in, dict) or not isinstance(sign_out, dict):
        return ReceiptCheck(False, ["Sign-in and sign-out receipts must both be mappings."])
    sign_in_check = check_sign_in(sign_in, sign_in.get("current_main_sha", ""), allowed_feeds)
    failures.extend(f"Referenced sign-in invalid: {why}" for why in sign_in_check.failures)
    if sign_out.get("event_type") != "SIGN_OUT":
        failures.append("Sign-out receipt event_type must be SIGN_OUT.")
    for field_name in SIGN_OUT_FIELDS:
        value = sign_out.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            failures.append(f"Sign-out receipt missing required field: {field_name}.")
    if sign_out.get("agent_id") != sign_in.get("agent_id"):
        failures.append("Sign-out agent identity does not match sign-in.")
    if sign_out.get("feed_issue") != sign_in.get("feed_issue"):
        failures.append("Sign-out must be posted to the same specialist feed as sign-in.")
    if str(sign_out.get("sign_in_comment_id", "")) != str(sign_in.get("comment_id", "")):
        failures.append("Sign-out must reference the exact sign-in comment.")
    _feed_comment_ok(sign_out, failures, "Sign-out receipt", allowed_feeds)
    _comment_body_ok(sign_out, failures, "Sign-out receipt")
    if sign_out.get("current_main_sha") != current_main_sha:
        failures.append("Sign-out must state the current main SHA observed at sign-out.")
    if not isinstance(sign_out.get("tested_revision"), str) or not _SHA_RE.fullmatch(
        sign_out.get("tested_revision", "")
    ):
        failures.append("Sign-out tested_revision must be a full commit SHA.")
    score = sign_out.get("score")
    if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 10:
        failures.append("Sign-out score must be a numeric value from 0 to 10.")
    lesson = sign_out.get("lesson_or_NO_CAPTURE")
    if _nonempty(lesson) and lesson != "NO_CAPTURE" and not (
        "http://" in lesson or "https://" in lesson or lesson.startswith("SN-")
    ):
        failures.append("Sign-out lesson must be NO_CAPTURE or a canonical lesson link/ID.")
    return ReceiptCheck(not failures, failures)
