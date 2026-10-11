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
6. It has posted and independently verified a structured SIGN_IN receipt on its live feed

This gate does NOT grant authority. It verifies readiness.
Authority still comes from Shawn's grants, not from passing this gate.

Usage — activate before governed work:
    python3 tools/protocol/cold_start_gate.py --agent-id <id> \
      --answers-json answers.json --write-read-receipt read-receipt.json \
      --sign-in-record sign-in.json --json

Usage — close the work cycle:
    python3 tools/protocol/cold_start_gate.py --agent-id <id> --mode close \
      --sign-in-record sign-in.json --sign-out-record sign-out.json --json

The input JSON must represent answers/receipts truthfully. The gate verifies
source blob SHAs and fetches the actual GitHub comment using GH_TOKEN or
GITHUB_TOKEN. Missing evidence or unavailable verification fails closed.

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
    REQUIRED_SOURCE_PATHS, ReadReceipt, issue_receipt,
)
from kernel.protocol.cold_start_gate import ColdStartState, run_cold_start  # noqa: E402
from kernel.protocol.work_cycle_receipt import check_sign_in, check_sign_out  # noqa: E402

RECONCILIATION_PREFIX = (
    "NAYA-ACTIVATION/CURRENT-REALITY/"
    "SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-"
)
RECONCILIATION_RE = re.compile(
    r"^SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-\d{4}-\d{2}-\d{2}\.md$"
)


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
    payload = b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    return hashlib.sha1(payload).hexdigest()


def current_source_revisions() -> dict:
    """Bind the required boot packet to the exact bytes in the checkout."""
    revisions = {}
    for rel in REQUIRED_SOURCE_PATHS:
        full = ROOT / rel
        if not full.is_file():
            raise FileNotFoundError(f"mandatory boot source missing: {rel}")
        revisions[rel] = git_blob_sha(full)
    recon_dir = ROOT / "NAYA-ACTIVATION" / "CURRENT-REALITY"
    candidates = sorted(
        path for path in recon_dir.glob("SOURCE-PRECEDENCE-AND-NAVIGATION-RECONCILIATION-*.md")
        if RECONCILIATION_RE.fullmatch(path.name)
    )
    if not candidates:
        raise FileNotFoundError("no dated source-precedence/navigation reconciliation exists")
    newest = candidates[-1]
    revisions[newest.relative_to(ROOT).as_posix()] = git_blob_sha(newest)
    return revisions


def load_json_record(path: str | None, label: str) -> dict:
    if not path:
        raise ValueError(f"{label} JSON path is required")
    with open(path, "r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def mint_read_receipt(answers_path: str, output_path: str, agent_id: str, current_main_sha: str) -> ReadReceipt:
    with open(answers_path, "r", encoding="utf-8") as f:
        answers = json.load(f)
    if not isinstance(answers, dict):
        raise ValueError("answer sheet must be a JSON object mapping q1...q13 to answer text")
    receipt = issue_receipt(
        agent_id=agent_id,
        answers=answers,
        source_revisions=current_source_revisions(),
        current_main_sha=current_main_sha,
    )
    if not receipt.verify():
        raise ValueError("read receipt failed protocol-version, comprehension, source, or SHA checks")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "agent_id": receipt.agent_id,
            "protocol_version": receipt.protocol_version,
            "answers": receipt.answers,
            "answer_text": receipt.answer_text,
            "passed": receipt.passed,
            "source_revisions": receipt.source_revisions,
            "current_main_sha": receipt.current_main_sha,
            "issued_at": receipt.issued_at,
            "receipt_hash": receipt.receipt_hash,
        }, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
    return receipt


def load_read_receipt(path: str, expected_agent: str, expected_main_sha: str) -> ReadReceipt:
    raw = load_json_record(path, "read receipt")
    receipt = ReadReceipt(
        agent_id=raw.get("agent_id", ""),
        protocol_version=raw.get("protocol_version", ""),
        answers=raw.get("answers", {}),
        passed=raw.get("passed") is True,
        answer_text=raw.get("answer_text", {}),
        source_revisions=raw.get("source_revisions", {}),
        current_main_sha=raw.get("current_main_sha", ""),
        issued_at=raw.get("issued_at", 0.0),
        receipt_hash=raw.get("receipt_hash", ""),
    )
    if receipt.agent_id != expected_agent:
        raise ValueError("read receipt belongs to a different agent identity")
    if receipt.current_main_sha != expected_main_sha:
        raise ValueError("read receipt is stale relative to current origin/main")
    actual_sources = current_source_revisions()
    if receipt.source_revisions != actual_sources:
        raise ValueError("read receipt source revisions do not match the actual checkout bytes")
    if not receipt.verify():
        raise ValueError("read receipt failed version, comprehension, source, or digest validation")
    return receipt


def fetch_actual_github_comment(record: dict, token: str) -> dict:
    """Fetch the purported feed comment; never trust a caller's observed=true flag."""
    issue = record.get("feed_issue")
    comment_id = record.get("comment_id")
    if not isinstance(issue, int) or not str(comment_id).isdigit():
        raise ValueError("feed_issue and numeric comment_id are required")
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
        raise RuntimeError(f"cannot independently fetch GitHub sign-in/out comment: {exc}") from exc
    expected_url = (
        f"https://github.com/SoulSchoolAcademy/NayaPOWER/issues/{issue}"
        f"#issuecomment-{comment_id}"
    )
    if actual.get("html_url") != expected_url:
        raise ValueError("comment ID/URL do not resolve to the expected issue comment")
    if actual.get("body") != record.get("comment_body"):
        raise ValueError("recorded comment body differs from the actual GitHub comment")
    if not str(actual.get("issue_url", "")).endswith(f"/issues/{issue}"):
        raise ValueError("GitHub comment belongs to a different issue/feed")
    verified = dict(record)
    verified["github_comment_observed"] = True
    return verified


def configured_live_feeds() -> set[int]:
    """Resolve feed IDs from the protocol navigation map, not old memory."""
    path = ROOT / "BRAIN" / "01-GOVERNANCE" / "naya-protocol-v1.machine.json"
    with open(path, "r", encoding="utf-8") as f:
        machine = json.load(f)
    feeds = {2154, 2175}
    for item in machine.get("navigation_links", {}).get("specialist_feeds", []):
        issue = item.get("issue")
        if isinstance(issue, int):
            feeds.add(issue)
    feeds.discard(1354)
    return feeds


def _append_check(checks: list, name: str, passed: bool, detail: str) -> None:
    checks.append({"name": name, "pass": bool(passed), "detail": detail})


def run_gate(
    agent_id: str = "unknown",
    mode: str = "activate",
    read_receipt_path: str | None = None,
    sign_in_record_path: str | None = None,
    sign_out_record_path: str | None = None,
    answers_path: str | None = None,
    write_receipt_path: str | None = None,
    github_token: str | None = None,
) -> dict:
    manifest = load_manifest()
    checks = []

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

    if mode == "activate":
        if answers_path and write_receipt_path and main_sha:
            try:
                minted = mint_read_receipt(answers_path, write_receipt_path, agent_id, main_sha)
                _append_check(checks, "read_receipt_minted", minted.verify(),
                              f"wrote versioned receipt to {write_receipt_path}")
                read_receipt_path = write_receipt_path
            except Exception as exc:
                _append_check(checks, "read_receipt_minted", False, str(exc))

        receipt = None
        if not read_receipt_path:
            _append_check(checks, "read_comprehension_receipt", False,
                          "required: --read-receipt PATH, or both --answers-json PATH and --write-read-receipt PATH")
        elif main_sha:
            try:
                receipt = load_read_receipt(read_receipt_path, agent_id, main_sha)
                _append_check(checks, "read_comprehension_receipt", True,
                              "protocol version, thirteen answers, required source blob SHAs, and current main SHA verified")
            except Exception as exc:
                _append_check(checks, "read_comprehension_receipt", False, str(exc))
        else:
            _append_check(checks, "read_comprehension_receipt", False,
                          "cannot verify receipt without current main SHA")

        sign_in = None
        if not sign_in_record_path:
            _append_check(checks, "live_feed_sign_in", False,
                          "required before governed work: --sign-in-record PATH")
        else:
            try:
                raw_sign_in = load_json_record(sign_in_record_path, "sign-in record")
                if not token:
                    raise ValueError("GH_TOKEN or GITHUB_TOKEN is required to fetch the posted sign-in comment")
                sign_in = fetch_actual_github_comment(raw_sign_in, token)
                feed_ids = configured_live_feeds()
                result = check_sign_in(sign_in, main_sha, feed_ids)
                if not result.passed:
                    raise ValueError("; ".join(result.failures))
                _append_check(checks, "live_feed_sign_in", True,
                              f"observed GitHub comment verified on live feed #{sign_in['feed_issue']}")
            except Exception as exc:
                sign_in = None
                _append_check(checks, "live_feed_sign_in", False, str(exc))

        if receipt is not None and sign_in is not None and main_sha:
            try:
                state = ColdStartState(
                    agent_id=agent_id,
                    human_director="Shawn Vibert",
                    lane=str(sign_in.get("task") or sign_in.get("owner") or "unknown"),
                    authority_summary="Readiness only. Passing this gate grants no new action authority.",
                    current_truth_location="mission issue #2154, current coordination board #2175, and live main",
                    next_action=str(sign_in.get("first_action") or "continue in the assigned lane"),
                    receipt=receipt,
                    current_main_sha=main_sha,
                    sign_in_record=sign_in,
                    live_feed_issues=sorted(configured_live_feeds()),
                )
                gate_result = run_cold_start(state)
                _append_check(checks, "kernel_cold_start_gate", gate_result.passed,
                              "passed" if gate_result.passed else "; ".join(gate_result.failures))
            except Exception as exc:
                _append_check(checks, "kernel_cold_start_gate", False, str(exc))
    elif mode == "close":
        try:
            if not sign_in_record_path or not sign_out_record_path:
                raise ValueError("cycle closure requires --sign-in-record PATH and --sign-out-record PATH")
            if not token:
                raise ValueError("GH_TOKEN or GITHUB_TOKEN is required to fetch sign-in/out comments")
            sign_in = fetch_actual_github_comment(
                load_json_record(sign_in_record_path, "sign-in record"), token
            )
            sign_out = fetch_actual_github_comment(
                load_json_record(sign_out_record_path, "sign-out record"), token
            )
            result = check_sign_out(sign_in, sign_out, main_sha, configured_live_feeds())
            if not result.passed:
                raise ValueError("; ".join(result.failures))
            _append_check(checks, "cycle_sign_out", True,
                          f"same-feed sign-out verified on feed #{sign_out['feed_issue']}")
        except Exception as exc:
            _append_check(checks, "cycle_sign_out", False, str(exc))
    else:
        _append_check(checks, "mode", False, f"unsupported mode {mode!r}; expected activate or close")

    failures = [check for check in checks if not check["pass"]]
    return {
        "gate": "cold_start" if mode == "activate" else "work_cycle_close",
        "agent_id": agent_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pass": not failures,
        "checks": checks,
        "failures": failures,
        "note": "Passing verifies protocol readiness and receipt structure only. It does not grant authority or prove production outcomes."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed Naya boot and work-cycle gate")
    parser.add_argument("--agent-id", required=True, help="Canonical Naya seat/agent identifier")
    parser.add_argument("--mode", choices=("activate", "close"), default="activate",
                        help="activate before governed work; close to validate sign-out")
    parser.add_argument("--read-receipt", help="Path to serialized read/comprehension receipt JSON")
    parser.add_argument("--answers-json", help="Path to q1...q13 answer-text JSON to mint a receipt")
    parser.add_argument("--write-read-receipt", help="Where to write the newly minted receipt JSON")
    parser.add_argument("--sign-in-record", help="Path to the live-feed SIGN_IN receipt JSON")
    parser.add_argument("--sign-out-record", help="Path to the live-feed SIGN_OUT receipt JSON (close mode)")
    parser.add_argument("--github-token", help="GitHub API token; prefer GH_TOKEN/GITHUB_TOKEN environment")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    result = run_gate(
        agent_id=args.agent_id,
        mode=args.mode,
        read_receipt_path=args.read_receipt,
        sign_in_record_path=args.sign_in_record,
        sign_out_record_path=args.sign_out_record,
        answers_path=args.answers_json,
        write_receipt_path=args.write_read_receipt,
        github_token=args.github_token,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if result["pass"] else "FAIL"
        print(f"Naya protocol gate ({args.mode}): {status}")
        for check in result["checks"]:
            mark = "✓" if check["pass"] else "✗"
            print(f"  {mark} {check['name']}: {check['detail']}")
        if not result["pass"]:
            print(f"\n{result['note']}")

    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
