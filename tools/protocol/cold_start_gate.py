#!/usr/bin/env python3
"""Cold-start gate: prove a fresh agent can begin safe, governed work.

Enforces the Agent Boot Contract (AGENTS.md) in executable form.
A protocol document is prose. This is proof.

A cold agent passes only when it can demonstrate:
1. It knows the current repository tip (not a stale memory of it)
2. It can locate the team coordination surface
3. It can identify its area feed
4. It can state the five protected gates (authority boundaries)
5. It can distinguish the six truth states
6. It has signed in on its feed (or declares its intent to)

This gate does NOT grant authority. It verifies readiness.
Authority still comes from Shawn's grants, not from passing this gate.

Usage:
    python3 tools/protocol/cold_start_gate.py --agent-id <id> --feed <feed-url>
    Returns JSON: {pass: bool, checks: [...], failures: [...]}

CI: This gate runs against every protocol change. If the manifest
    and the gate disagree, the gate wins (executable > documentary).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "kernel" / "protocol" / "protocol_manifest.json"
sys.path.insert(0, str(ROOT))

from kernel.protocol.read_receipt import (  # noqa: E402
    PROTOCOL_VERSION, REQUIRED_SOURCE_PATHS, RECONCILIATION_RE,
    ReadReceipt, issue_receipt,
)
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start  # noqa: E402
from kernel.protocol.work_cycle_receipt import check_sign_in, check_sign_out  # noqa: E402


def load_manifest() -> dict:
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def check_manifest_valid(manifest: dict) -> tuple[bool, str]:
    """The manifest itself must be well-formed."""
    required = ["laws", "protected_gates", "truth_states", "operating_loop",
                "never_do", "law_conflict_hierarchy", "cold_start_required"]
    missing = [k for k in required if k not in manifest]
    if missing:
        return False, f"manifest missing keys: {missing}"
    if len(manifest["protected_gates"]) != 5:
        return False, f"expected 5 protected gates, found {len(manifest['protected_gates'])}"
    if len(manifest["truth_states"]) != 6:
        return False, f"expected 6 truth states, found {len(manifest['truth_states'])}"
    return True, "manifest well-formed"


def check_tip_resolvable() -> tuple[bool, str]:
    """The agent must be able to resolve the current tip. Stale SHA = stale decision."""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "origin", "main"],
            capture_output=True, text=True, timeout=30, cwd=ROOT
        )
        if result.returncode != 0:
            return False, "cannot resolve origin/main"
        sha = result.stdout.split()[0] if result.stdout.strip() else ""
        if len(sha) != 40:
            return False, f"invalid SHA from origin/main: {sha[:12]}"
        return True, f"tip resolvable: {sha[:12]}"
    except Exception as e:
        return False, f"tip resolution failed: {e}"


def check_law_ids_unique(manifest: dict) -> tuple[bool, str]:
    """Every law must have a unique ID. Duplicate law IDs = ambiguous authority."""
    ids = [law["id"] for law in manifest["laws"]]
    if len(ids) != len(set(ids)):
        dupes = [i for i in ids if ids.count(i) > 1]
        return False, f"duplicate law IDs: {set(dupes)}"
    return True, f"{len(ids)} laws, all unique IDs"


def check_conflict_hierarchy_complete(manifest: dict) -> tuple[bool, str]:
    """The conflict hierarchy must cover the protected gates as highest priority."""
    hierarchy = manifest.get("law_conflict_hierarchy", [])
    if not hierarchy:
        return False, "no conflict hierarchy defined"
    if hierarchy[0] != "protected_gates":
        return False, "protected_gates must be first in conflict hierarchy"
    return True, "conflict hierarchy valid: gates first"


def check_truth_states_distinct(manifest: dict) -> tuple[bool, str]:
    """Truth states must not collapse. Each must have distinct non-equivalences."""
    rules = manifest.get("truth_state_rules", {})
    states = manifest.get("truth_states", [])
    for state in states:
        if state not in rules:
            return False, f"truth state {state} has no non-equivalence rules"
    return True, f"{len(states)} truth states, all with distinct rules"


def check_never_do_nonempty(manifest: dict) -> tuple[bool, str]:
    """The never-do list must exist and be non-trivial."""
    never = manifest.get("never_do", [])
    if len(never) < 10:
        return False, f"never-do list too short ({len(never)}), expected comprehensive"
    return True, f"{len(never)} prohibitions defined"


def resolve_current_main_sha() -> str:
    result = subprocess.run(
        ["git", "ls-remote", "origin", "main"],
        capture_output=True, text=True, timeout=30, cwd=ROOT,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError("cannot resolve current origin/main")
    sha = result.stdout.split()[0]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise RuntimeError(f"origin/main returned invalid SHA: {sha!r}")
    return sha


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def current_source_revisions() -> dict:
    revisions = {}
    for relative in REQUIRED_SOURCE_PATHS:
        full = ROOT / relative
        if not full.is_file():
            raise FileNotFoundError(f"mandatory boot source missing: {relative}")
        revisions[relative] = git_blob_sha(full)
    directory = ROOT / "NAYA-ACTIVATION" / "CURRENT-REALITY"
    candidates = sorted(
        p for p in directory.glob("SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md")
        if RECONCILIATION_RE.fullmatch(p.relative_to(ROOT).as_posix())
    )
    if not candidates:
        raise FileNotFoundError("newest dated source-precedence/navigation reconciliation is missing")
    newest = candidates[-1]
    revisions[newest.relative_to(ROOT).as_posix()] = git_blob_sha(newest)
    return revisions


def load_json_record(path: str | None, label: str) -> dict:
    if not path:
        raise ValueError(f"{label} path is required")
    with open(path, "r", encoding="utf-8") as handle:
        record = json.load(handle)
    if not isinstance(record, dict):
        raise ValueError(f"{label} must be a JSON object")
    return record


def mint_read_receipt(answers_path: str, output_path: str, agent_id: str, main_sha: str) -> ReadReceipt:
    answers = load_json_record(answers_path, "comprehension answers")
    receipt = issue_receipt(
        agent_id=agent_id,
        answers=answers,
        source_revisions=current_source_revisions(),
        current_main_sha=main_sha,
    )
    if not receipt.verify():
        raise ValueError("comprehension answers or source-revision requirements failed")
    serialized = {
        "agent_id": receipt.agent_id,
        "protocol_version": receipt.protocol_version,
        "answers": receipt.answers,
        "answer_text": receipt.answer_text,
        "passed": receipt.passed,
        "source_revisions": receipt.source_revisions,
        "current_main_sha": receipt.current_main_sha,
        "issued_at": receipt.issued_at,
        "receipt_hash": receipt.receipt_hash,
    }
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(serialized, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
    return receipt


def load_read_receipt(path: str, expected_agent: str, main_sha: str) -> ReadReceipt:
    raw = load_json_record(path, "read receipt")
    receipt = ReadReceipt(
        agent_id=raw.get("agent_id", ""),
        protocol_version=raw.get("protocol_version", ""),
        answers=raw.get("answers", {}),
        answer_text=raw.get("answer_text", {}),
        passed=raw.get("passed") is True,
        source_revisions=raw.get("source_revisions", {}),
        current_main_sha=raw.get("current_main_sha", ""),
        issued_at=raw.get("issued_at", 0.0),
        receipt_hash=raw.get("receipt_hash", ""),
    )
    if receipt.agent_id != expected_agent:
        raise ValueError("receipt agent ID does not match the activating seat")
    if receipt.current_main_sha != main_sha:
        raise ValueError("receipt is stale relative to current origin/main")
    if receipt.source_revisions != current_source_revisions():
        raise ValueError("receipt source SHAs do not match the actual current checkout")
    if not receipt.verify():
        raise ValueError("receipt version, answers, source revisions, or integrity digest invalid")
    return receipt


def fetch_actual_github_comment(record: dict, token: str) -> dict:
    issue = record.get("feed_issue")
    comment_id = str(record.get("comment_id", ""))
    if not isinstance(issue, int) or not comment_id.isdigit():
        raise ValueError("numeric feed_issue and comment_id are required")
    request = urllib.request.Request(
        f"https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER/issues/comments/{comment_id}",
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "NayaPOWER-Protocol-Gate",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            actual = json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"cannot fetch the actual GitHub feed comment: {exc}") from exc

    expected_url = f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/{issue}#issuecomment-{comment_id}"
    if actual.get("html_url") != expected_url:
        raise ValueError("GitHub returned a different comment URL")
    if not str(actual.get("issue_url", "")).endswith(f"/issues/{issue}"):
        raise ValueError("GitHub comment belongs to a different feed")
    if not isinstance(actual.get("body"), str):
        raise ValueError("GitHub comment has no textual body")
    if record.get("comment_body") != actual["body"]:
        raise ValueError("recorded body differs from the actual GitHub post")
    expected_digest = hashlib.sha256(actual["body"].encode("utf-8")).hexdigest()
    if record.get("comment_body_sha256") != expected_digest:
        raise ValueError("recorded body SHA-256 differs from the actual GitHub post")
    verified = dict(record)
    verified["github_comment_observed"] = True
    return verified


def configured_live_feeds() -> set[int]:
    # PROTOCOL.md is the navigation source; stale #1354 and the #1599 index
    # are not posting destinations. Mission #2154 is a record, not a work feed.
    protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
    issues = {int(value) for value in re.findall(
        r"https://github\.com/SoulSchoolAcademy/NayaPOWER/issues/(\d+)", protocol
    )}
    issues.update({1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 2175})
    issues.difference_update({1354, 1599, 2154})
    return issues


def _append_check(checks: list, name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "pass": bool(passed), "detail": detail})


def run_gate(
    agent_id: str = "",
    mode: str = "activate",
    read_receipt_path: str | None = None,
    sign_in_record_path: str | None = None,
    sign_out_record_path: str | None = None,
    answers_path: str | None = None,
    write_receipt_path: str | None = None,
    github_token: str | None = None,
) -> dict:
    checks = []
    try:
        manifest = load_manifest()
    except Exception as exc:
        manifest = {}
        _append_check(checks, "manifest_load", False, str(exc))

    check_fns = [
        ("manifest_valid", lambda: check_manifest_valid(manifest)),
        ("tip_resolvable", check_tip_resolvable),
        ("law_ids_unique", lambda: check_law_ids_unique(manifest)),
        ("conflict_hierarchy", lambda: check_conflict_hierarchy_complete(manifest)),
        ("truth_states_distinct", lambda: check_truth_states_distinct(manifest)),
        ("never_do_complete", lambda: check_never_do_nonempty(manifest)),
    ]
    for name, fn in check_fns:
        try:
            passed, detail = fn()
        except Exception as exc:
            passed, detail = False, f"check raised: {exc}"
        _append_check(checks, name, passed, detail)

    try:
        main_sha = resolve_current_main_sha()
        _append_check(checks, "current_main_sha", True, main_sha)
    except Exception as exc:
        main_sha = ""
        _append_check(checks, "current_main_sha", False, str(exc))

    token = github_token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not isinstance(agent_id, str) or not agent_id.strip():
        _append_check(checks, "agent_identity", False, "--agent-id is required")
    if mode == "activate":
        if answers_path and write_receipt_path and main_sha:
            try:
                minted = mint_read_receipt(answers_path, write_receipt_path, agent_id, main_sha)
                _append_check(checks, "read_receipt_minted", minted.verify(), "source- and version-bound receipt written")
                read_receipt_path = write_receipt_path
            except Exception as exc:
                _append_check(checks, "read_receipt_minted", False, str(exc))

        receipt = None
        if not read_receipt_path:
            _append_check(checks, "read_comprehension_receipt", False,
                          "provide --read-receipt, or both --answers-json and --write-read-receipt")
        elif main_sha:
            try:
                receipt = load_read_receipt(read_receipt_path, agent_id, main_sha)
                _append_check(checks, "read_comprehension_receipt", True,
                              "answer text, protocol version, required source SHAs, and current main verified")
            except Exception as exc:
                _append_check(checks, "read_comprehension_receipt", False, str(exc))
        else:
            _append_check(checks, "read_comprehension_receipt", False, "cannot verify receipt without current main")

        sign_in = None
        if not sign_in_record_path:
            _append_check(checks, "live_feed_sign_in", False, "--sign-in-record is required before governed work")
        else:
            try:
                raw = load_json_record(sign_in_record_path, "sign-in record")
                if not token:
                    raise ValueError("set GH_TOKEN or GITHUB_TOKEN with GitHub issue-comment read access")
                sign_in = fetch_actual_github_comment(raw, token)
                check = check_sign_in(sign_in, main_sha, configured_live_feeds())
                if not check.passed:
                    raise ValueError("; ".join(check.failures))
                _append_check(checks, "live_feed_sign_in", True,
                              f"actual GitHub SIGN_IN verified on live feed #{sign_in['feed_issue']}")
            except Exception as exc:
                sign_in = None
                _append_check(checks, "live_feed_sign_in", False, str(exc))

        if receipt is not None and sign_in is not None and main_sha:
            try:
                state = ColdStartState(
                    agent_id=agent_id,
                    human_director="Shawn",
                    lane=str(sign_in.get("task") or sign_in.get("owner") or ""),
                    authority_summary="protected production, credentials, money, destructive actions, ratification, security, privacy, consent, and authority changes remain gated",
                    current_truth_location="mission issue #2154, current coordination board #2175, live main",
                    next_action=str(sign_in.get("first_action") or ""),
                    receipt=receipt,
                    current_main_sha=main_sha,
                    sign_in_record=sign_in,
                    live_feed_issues=sorted(configured_live_feeds()),
                )
                result = run_cold_start(state)
                _append_check(checks, "kernel_cold_start", result.passed,
                              "passed" if result.passed else "; ".join(result.failures))
            except Exception as exc:
                _append_check(checks, "kernel_cold_start", False, str(exc))
    elif mode == "close":
        try:
            if not sign_in_record_path or not sign_out_record_path:
                raise ValueError("both --sign-in-record and --sign-out-record are required to close a cycle")
            if not token:
                raise ValueError("set GH_TOKEN or GITHUB_TOKEN with GitHub issue-comment read access")
            sign_in = fetch_actual_github_comment(load_json_record(sign_in_record_path, "sign-in record"), token)
            sign_out = fetch_actual_github_comment(load_json_record(sign_out_record_path, "sign-out record"), token)
            result = check_sign_out(sign_in, sign_out, main_sha, configured_live_feeds())
            if not result.passed:
                raise ValueError("; ".join(result.failures))
            _append_check(checks, "cycle_sign_out", True,
                          f"actual same-feed SIGN_OUT verified on feed #{sign_out['feed_issue']}")
        except Exception as exc:
            _append_check(checks, "cycle_sign_out", False, str(exc))
    else:
        _append_check(checks, "mode", False, "supported modes are activate and close")

    failures = [item for item in checks if not item["pass"]]
    return {
        "gate": "cold_start" if mode == "activate" else "work_cycle_close",
        "agent_id": agent_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pass": not failures,
        "checks": checks,
        "failures": failures,
        "note": "Gate PASS validates boot/source/comprehension/feed receipt checks only. It grants no authority and proves no production outcome."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed Naya protocol activation and cycle-close gate")
    parser.add_argument("--agent-id", required=True, help="Canonical Naya seat/agent identifier")
    parser.add_argument("--mode", choices=("activate", "close"), default="activate")
    parser.add_argument("--read-receipt", help="Existing serialized read/comprehension receipt JSON")
    parser.add_argument("--answers-json", help="JSON object with free-text answers q1...q13")
    parser.add_argument("--write-read-receipt", help="Output path for a newly checked receipt")
    parser.add_argument("--sign-in-record", help="Local record containing exact metadata/body of the posted SIGN_IN comment")
    parser.add_argument("--sign-out-record", help="Local record containing exact metadata/body of the posted SIGN_OUT comment")
    parser.add_argument("--github-token", help="Prefer GH_TOKEN or GITHUB_TOKEN environment variables")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    result = run_gate(
        agent_id=args.agent_id, mode=args.mode, read_receipt_path=args.read_receipt,
        sign_in_record_path=args.sign_in_record, sign_out_record_path=args.sign_out_record,
        answers_path=args.answers_json, write_receipt_path=args.write_read_receipt,
        github_token=args.github_token,
    )
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Naya protocol gate ({args.mode}): {'PASS' if result['pass'] else 'FAIL'}")
        for item in result["checks"]:
            print(f"  {'✓' if item['pass'] else '✗'} {item['name']}: {item['detail']}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
