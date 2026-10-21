#!/usr/bin/env python3
"""Single risk-tiered paperwork gate for PR evidence.

Substantive tests/spec checks remain separate. This gate only validates the
cross-seat scorecard/evidence paperwork and routes pure content PRs to the
canonical content door. It never changes repository protection settings.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import sys
import urllib.error

try:
    import check_merge_consensus as consensus
    import check_pr_receipt as receipt
    from pr_flow_tier import classify_tier
except ModuleNotFoundError:  # support import from repository tests
    from tools import check_merge_consensus as consensus
    from tools import check_pr_receipt as receipt
    from tools.pr_flow_tier import classify_tier


CURRENT_HEAD = ""
CURRENT_TIER = ""


def _emit(code: str, message: str, cure: str, owner: str = "PR authoring lane") -> int:
    if code == "PASS":
        missing = "none — all required paperwork predicates passed"
        cure = "none"
        owner = "none"
    else:
        missing = message
    print(f"UNIFIED PAPERWORK GATE: {code}")
    print(f"MISSING: {missing}")
    print(f"CURE: {cure} (owner: {owner})")

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        values = {
            "verdict": code,
            "missing": missing,
            "cure": cure,
            "owner": owner,
            "head": CURRENT_HEAD,
            "tier": CURRENT_TIER,
        }
        with open(output_path, "a", encoding="utf-8") as fh:
            for key, value in values.items():
                safe = str(value).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
                fh.write(f"{key}={safe}\n")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write("## Unified paperwork gate\n\n")
            fh.write(f"- **Verdict:** {code}\n")
            fh.write(f"- **Tier:** {CURRENT_TIER or 'unknown'}\n")
            fh.write(f"- **Head:** {CURRENT_HEAD or 'unavailable'}\n")
            fh.write(f"- **Missing:** {missing}\n")
            fh.write(f"- **Cure:** {cure} (owner: {owner})\n")

    return 0 if code == "PASS" else 1


def _read_event() -> dict:
    path = os.environ.get("GITHUB_EVENT_PATH", "")
    if not path:
        raise RuntimeError("GITHUB_EVENT_PATH is missing")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _live_pr(event: dict, repo: str, token: str) -> tuple[dict, int]:
    number = os.environ.get("PR_NUMBER")
    if not number:
        issue = event.get("issue") or {}
        number = str(issue.get("number") or "")
    if not number:
        pr_event = event.get("pull_request") or {}
        number = str(pr_event.get("number") or "")
    if not number:
        raise RuntimeError("could not identify PR number from event")
    # Always refresh the live PR: event payloads and previous check runs can be stale.
    pr = consensus.api_get(f"/repos/{repo}/pulls/{number}", token)
    return pr, int(number)


def _seat_key(seat: str) -> str:
    value = (seat or "").strip().casefold()
    return value[5:].strip() if value.startswith("naya ") else value


_DIFF_SHA_FIELD_RE = re.compile(
    r"(?im)^\s*diff(?:[\s_-]*sha256|[\s_-]*fingerprint)\s*[:=]\s*([a-f0-9]{64})\s*$"
)
_VERIFICATION_FIELD_RE = re.compile(
    r"(?im)^\s*(?:verification|tests\s+run|behavior\s+verified)\s*[:=]\s*(.+?)\s*$"
)


def scorecard_diff_hash_of(body: str) -> str | None:
    matches = [m.group(1).lower() for m in _DIFF_SHA_FIELD_RE.finditer(body or "")]
    return matches[0] if matches and len(set(matches)) == 1 else None


def _verification_attestation_present(body: str) -> bool:
    for match in _VERIFICATION_FIELD_RE.finditer(body or ""):
        value = match.group(1).strip()
        if len(value) >= 12 and value.casefold() not in {"n/a", "none", "unknown", "todo", "not run"}:
            return True
    return False


def compute_diff_fingerprint(files: list[dict]) -> str | None:
    """Stable SHA-256 of material PR diff, independent of commit identity."""
    if not files:
        return None
    material = []
    for item in files:
        if not isinstance(item, dict) or not item.get("filename") or not item.get("status") or not item.get("sha"):
            return None
        material.append({
            "filename": item.get("filename"),
            "status": item.get("status"),
            "previous_filename": item.get("previous_filename"),
            "blob_sha": item.get("sha"),
            "additions": item.get("additions"),
            "deletions": item.get("deletions"),
            "patch": item.get("patch"),
        })
    material.sort(key=lambda item: (item["filename"], item["status"], item.get("previous_filename") or ""))
    canonical = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _scorecard_for_current_head(comments: list[dict], head: str,
                                author_seat: str, minimum: float, *, tier: str = "A", diff_hash: str | None = None) -> tuple[bool, str]:
    for comment in comments:
        body = comment.get("body") or ""
        low = body.lower()
        # Require a parsed head field, not a SHA mentioned anywhere in prose.
        # Seat is an explicit declaration; the repo currently does not
        # cryptographically bind declared seat labels to agent identities.
        if "scorecard" not in low and "verdict" not in low:
            continue
        pinned_head = consensus.scorecard_head_of(body)
        if not pinned_head:
            continue
        diff_pin = scorecard_diff_hash_of(body)
        same_head = pinned_head == head.lower()
        same_diff = bool(diff_hash and diff_pin and diff_pin == diff_hash)
        if tier == "A" and not same_head:
            continue
        if tier == "B" and (not same_diff or not diff_hash):
            continue
        seat = consensus.author_seat_of(body)
        if not seat or _seat_key(seat) == _seat_key(author_seat):
            continue
        if tier == "B" and not _verification_attestation_present(body):
            continue
        score = consensus._score_of(body)
        if score is not None and minimum <= score <= 10:
            if same_head:
                return True, f"scorecard {score:g}/10 from different declared seat {seat} pins current head {head[:12]}"
            return True, f"scorecard {score:g}/10 from different declared seat {seat}; material diff fingerprint matches despite head moving ({pinned_head[:12]} -> {head[:12]})"
    return False, f"no numeric scorecard >= {minimum:g}/10 from a different declared seat with an explicit head field and valid Tier-B diff fingerprint/verification attestation (current head {head[:12]})"


def run() -> int:
    global CURRENT_HEAD, CURRENT_TIER
    event = _read_event()
    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or ""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not repo or not token:
        return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                     "repository or read token is unavailable",
                     "restore the workflow's read-only GitHub token and re-run",
                     owner="Gate maintainer")

    try:
        pr, number = _live_pr(event, repo, token)
        head = ((pr.get("head") or {}).get("sha") or "").strip()
        title = pr.get("title") or ""
        body = pr.get("body") or ""
        CURRENT_HEAD = head
        if len(head) != 40 or any(ch not in "0123456789abcdef" for ch in head):
            return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                         "GitHub did not return a valid current head SHA",
                         "retry after GitHub's PR API returns the current 40-character SHA",
                         owner="Gate maintainer")

        files = consensus.api_get(f"/repos/{repo}/pulls/{number}/files", token)
        paths = [item.get("filename", "") for item in files if item.get("filename")]
        expected_files = pr.get("changed_files")
        tier = classify_tier(title, paths, changed_files=files, expected_changed_files=expected_files)
        CURRENT_TIER = tier["tier"]
        print(f"Tier: {tier['tier']} — {tier['reason']}")
        print(f"PR: #{number}; current head: {head}")

        if tier["tier"] == "C":
            return _emit(
                "BLOCKED — CONTENT_DOOR_NOT_PROVEN",
                "all changed paths appear to be mechanical content/index data, but the current canonical content door is not proven healthy: main's latest full test run reports missing Smart Note capture/registry entries and stale generated indexes",
                "repair the canonical capture → registry → index/sync path and make its schema, collision, registry-drift, and index-freshness checks green before routing note-only work through that door; do not substitute scorecard ceremony or merge a mega-PR to hide the content-door defect",
                owner="Content-door lane",
            )

        author_seat = consensus.author_seat_of(body)
        if not author_seat:
            return _emit("BLOCKED — AUTHOR_SEAT_MISSING",
                         "the PR body does not declare its authoring seat",
                         "add exactly one explicit 'Seat: Naya <seat>' declaration to the PR body")

        comments = consensus.api_get(f"/repos/{repo}/issues/{number}/comments", token)
        diff_hash = compute_diff_fingerprint(files)
        minimum = 9.5 if tier["tier"] == "A" else 9.0
        ok, score_detail = _scorecard_for_current_head(
            comments, head, author_seat, minimum, tier=tier["tier"], diff_hash=diff_hash
        )
        if not ok:
            cure = f"post a scorecard from a different declared seat with `Head SHA: {head}`, `Diff-SHA256: {diff_hash or '<unavailable>'}`, and `Verification: <tests run or behavior observed>`; score >= {minimum:g}/10"
            return _emit("BLOCKED — SCORECARD_MISSING_OR_STALE",
                         f"Tier {tier['tier']} requires {minimum:g}/10; {score_detail}",
                         cure)

        # The existing receipt checker is the source of truth for Evidence
        # heading and URL/SHA/path liveness; don't duplicate its parser.
        os.environ["PR_BODY"] = body
        receipt.URL_CHECK_RESULTS.clear()
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                receipt.main()
        except SystemExit:
            lines = [line.strip() for line in output.getvalue().splitlines() if line.strip()]
            reason = next((line for line in lines if "FAILED:" in line), "Evidence receipt did not pass")
            cure = next((line.replace("Fix: ", "") for line in lines if line.startswith("Fix: ")),
                        "add a ## Evidence section containing at least one live URL, existing commit SHA, or existing repository path and explain what it proves")
            states = [item.get("state") for item in receipt.URL_CHECK_RESULTS.values()]
            if "UNAVAILABLE" in states and "DEAD" not in states:
                details = "; ".join(
                    f"{url}: {item.get('detail')}"
                    for url, item in receipt.URL_CHECK_RESULTS.items()
                    if item.get("state") == "UNAVAILABLE"
                )
                return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                             f"evidence URL check could not complete: {details}",
                             "retry when the URL host/network is reachable; do not change or replace the evidence unless a retry confirms it is dead",
                             owner="Gate maintainer")
            return _emit("BLOCKED — EVIDENCE_INVALID", reason, cure)

        return _emit(
            "PASS",
            f"Tier {tier['tier']}; {score_detail}; evidence receipt resolves. Declared-seat separation is repository convention, not cryptographic actor binding.",
            "none",
            owner="none",
        )

    except (consensus.GateAPIError, urllib.error.URLError, TimeoutError) as exc:
        return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                     f"GitHub/evidence verification unavailable: {type(exc).__name__}: {exc}",
                     "restore API/network availability and re-run; do not interpret this as a quality failure",
                     owner="Gate maintainer")
    except Exception as exc:
        return _emit("ERROR — VERIFICATION_UNAVAILABLE",
                     f"unexpected verification error: {type(exc).__name__}: {exc}",
                     "inspect the named integration error, repair the verifier, and re-run; do not bypass the gate",
                     owner="Gate maintainer")


if __name__ == "__main__":
    raise SystemExit(run())
