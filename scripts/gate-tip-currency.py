#!/usr/bin/env python3
"""SN-0493 Gate — Tip Currency Enforcement (machine-falsifiable).

Ratified law: "a decision computed on tip T is inadmissible after the tip
moves; re-verify tip currency at action time."

Incident: 2026-10-06 — Naya 2's flawless merge decision for PR #1661 was
computed on a tip that PR #1660 had already moved 3 minutes earlier. The
decision was perfect for a world that no longer existed.

Operational definition:
  T1  BASE TIP PRESENT — the decision record carries base_tip_sha
      (40-hex). Missing, empty, or malformed = FAIL CLOSED.
  T2  LIVE TIP RESOLVABLE — the gate determines the current main tip.
      Unresolvable = FAIL CLOSED (cannot verify currency -> block).
  T3  CURRENCY — base_tip_sha == live tip. Moved -> FAIL; re-verify
      the decision against the new tip, then re-stamp and proceed.

Usage:
    python3 scripts/gate-tip-currency.py <decision.json> [options]
    python3 scripts/gate-tip-currency.py --self-test
        (runs the gate against fabricated current/stale/missing-tip
         records with an injected live tip; stale and missing MUST fail)
    python3 scripts/gate-tip-currency.py --stamp <decision.json>
        (writes the current live tip into the record as base_tip_sha;
         use at decision time, re-stamp after any re-verification)

Options:
    --live-tip SHA   use this as the live tip instead of resolving it
                     (testing / offline use)
    --repo URL       remote for `git ls-remote` resolution
                     (default: https://github.com/SoulSchoolAcademy/NayaPOWER.git)
    --branch NAME    branch whose tip is "live" (default: main)

Live-tip resolution order (first success wins):
    1. --live-tip override
    2. `git ls-remote <repo> refs/heads/<branch>`
    3. local git: `git rev-parse <branch>` / origin/<branch> / HEAD
    4. GitHub API (needs GITHUB_TOKEN or GH_TOKEN in env)

Exit 0 = currency verified, action may proceed.
Exit 1 = BLOCKED: stale tip, missing/malformed base tip, or live tip
         unresolvable. Fail closed — the action does not proceed silently.
Exit 2 = usage / input error.

Falsifier: craft a decision record whose base_tip_sha differs from the
injected --live-tip. This gate MUST exit 1. If it exits 0, the gate
is broken. A record with no base_tip_sha MUST also exit 1.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

LAW_ID = "SN-0493"

# Field aliases: decision records use slightly different shapes; normalize.
BASE_TIP_FIELDS = (
    "base_tip_sha",
    "main_tip_sha",
    "decided_on_tip",
    "tip_sha",
    "basis_commit",
    "verified_main_tip_sha",
)

SHA_RE = re.compile(r"^[0-9a-f]{40}$")

DEFAULT_REPO = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"


def _base_tip(record: dict) -> str | None:
    for f in BASE_TIP_FIELDS:
        v = record.get(f)
        if isinstance(v, str) and v.strip():
            return v.strip().lower()
    # also look one level down in common envelopes
    for envelope in ("decision", "receipt", "state"):
        sub = record.get(envelope)
        if isinstance(sub, dict):
            for f in BASE_TIP_FIELDS:
                v = sub.get(f)
                if isinstance(v, str) and v.strip():
                    return v.strip().lower()
    return None


def _valid_sha(s: str | None) -> bool:
    return isinstance(s, str) and bool(SHA_RE.match(s))


def _resolve_live_tip(repo: str, branch: str, override: str | None) -> tuple[str | None, str]:
    """Return (sha_or_None, method_description)."""
    if override:
        if _valid_sha(override.lower()):
            return override.lower(), "--live-tip override"
        return None, "--live-tip override malformed (not 40-hex)"
    # 2. git ls-remote (no clone needed)
    try:
        out = subprocess.run(
            ["git", "ls-remote", repo, f"refs/heads/{branch}"],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode == 0 and out.stdout.strip():
            sha = out.stdout.split()[0].lower()
            if _valid_sha(sha):
                return sha, f"git ls-remote {branch}"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # 3. local git
    for ref in (branch, f"origin/{branch}", "HEAD"):
        try:
            out = subprocess.run(
                ["git", "rev-parse", "--verify", ref],
                capture_output=True, text=True, timeout=15,
            )
            if out.returncode == 0:
                sha = out.stdout.strip().lower()
                if _valid_sha(sha):
                    return sha, f"local git {ref}"
        except (FileNotFoundError, subprocess.TimeoutExpired):
            break
    # 4. GitHub API
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        try:
            req = urllib.request.Request(
                "https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER"
                f"/git/refs/heads/{branch}",
                headers={"Authorization": f"Bearer {token}",
                         "Accept": "application/vnd.github+json"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            sha = str(data["object"]["sha"]).lower()
            if _valid_sha(sha):
                return sha, "GitHub API"
        except Exception:
            pass
    return None, "all resolution methods failed"


def check(record: dict, live_tip: str | None, live_method: str) -> tuple[bool, list[str]]:
    """Return (may_proceed, reasons). Fail closed on every unknown."""
    reasons: list[str] = []

    # T1: base tip present and well-formed
    base = _base_tip(record)
    if not base:
        reasons.append(
            "T1 FAIL CLOSED: decision record carries no base tip "
            f"(checked fields: {', '.join(BASE_TIP_FIELDS)} and one envelope "
            "level down). A decision with no recorded tip is inadmissible. "
            "Stamp it with --stamp at decision time."
        )
        return False, reasons
    if not _valid_sha(base):
        reasons.append(
            f"T1 FAIL CLOSED: base_tip_sha is malformed ({base[:20]}...); "
            "expected 40-hex SHA."
        )
        return False, reasons

    # T2: live tip resolvable
    if not live_tip or not _valid_sha(live_tip):
        reasons.append(
            f"T2 FAIL CLOSED: live tip unresolvable ({live_method}). "
            "Currency cannot be verified -> action blocked. Fix resolution "
            "(network, git, or --live-tip) and re-run."
        )
        return False, reasons

    # T3: currency
    if base != live_tip:
        reasons.append(
            "T3 BLOCKED: tip moved since the decision was computed. "
            f"Decision base tip: {base[:12]}; live tip: {live_tip[:12]} "
            f"(via {live_method}). Re-verify the decision against the new "
            "tip, re-stamp with --stamp, then proceed."
        )
        return False, reasons

    reasons.append(
        f"T1-T3 PASS: decision base tip {base[:12]} == live tip "
        f"(via {live_method}). Currency verified; action may proceed."
    )
    return True, reasons


def _self_test() -> int:
    """Falsifier battery. Returns 0 if the gate behaves, 1 if broken."""
    live = "b" * 40
    moved = "a" * 40
    cases = [
        ("current tip passes",
         {"decision_id": "d1", "base_tip_sha": live}, True),
        ("stale tip FAILS (the #1661 incident)",
         {"decision_id": "d2", "base_tip_sha": moved}, False),
        ("missing base tip FAILS CLOSED",
         {"decision_id": "d3"}, False),
        ("malformed base tip FAILS CLOSED",
         {"decision_id": "d4", "base_tip_sha": "not-a-sha"}, False),
        ("alias field accepted (decided_on_tip)",
         {"decision_id": "d5", "decided_on_tip": live}, True),
        ("enveloped record accepted",
         {"receipt": {"base_tip_sha": live}}, True),
        ("unresolvable live tip FAILS CLOSED",
         {"decision_id": "d6", "base_tip_sha": live}, False,
         None),  # live=None
    ]
    failures = 0
    for case in cases:
        name, record, expect_pass = case[0], case[1], case[2]
        use_live = live if len(case) < 4 else case[3]
        ok, reasons = check(record, use_live,
                            "--live-tip override" if use_live else "simulated outage")
        status = "ok" if ok == expect_pass else "BROKEN"
        if ok != expect_pass:
            failures += 1
        print(f"[{status}] {name}: expected "
              f"{'PASS' if expect_pass else 'FAIL'}, got "
              f"{'PASS' if ok else 'FAIL'}")
        if ok != expect_pass:
            print(f"    reasons: {reasons}")
    if failures:
        print(f"\nSELF-TEST FAILED: {failures} case(s) broken.")
        return 1
    print("\nSELF-TEST PASSED: all 7 cases behave (stale/missing/malformed/"
          "unresolvable all fail closed).")
    return 0


def _stamp(path: str, repo: str, branch: str, live_override: str | None) -> int:
    try:
        with open(path) as f:
            record = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read decision record: {e}", file=sys.stderr)
        return 2
    if not isinstance(record, dict):
        print("error: decision record must be a JSON object", file=sys.stderr)
        return 2
    live_tip, method = _resolve_live_tip(repo, branch, live_override)
    if not live_tip:
        print(f"error: cannot resolve live tip ({method}); not stamping.",
              file=sys.stderr)
        return 1
    record["base_tip_sha"] = live_tip
    record["base_tip_resolved_via"] = method
    try:
        with open(path, "w") as f:
            json.dump(record, f, indent=2)
            f.write("\n")
    except OSError as e:
        print(f"error: cannot write decision record: {e}", file=sys.stderr)
        return 2
    print(f"stamped {path}: base_tip_sha={live_tip[:12]} (via {method})")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=f"{LAW_ID} tip-currency gate")
    ap.add_argument("decision", nargs="?",
                    help="path to decision record JSON")
    ap.add_argument("--self-test", action="store_true",
                    help="run the falsifier battery")
    ap.add_argument("--stamp", action="store_true",
                    help="stamp the decision record with the current live tip")
    ap.add_argument("--live-tip", default=None,
                    help="use as live tip instead of resolving")
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--branch", default="main")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()

    if not args.decision:
        ap.print_usage(sys.stderr)
        return 2

    if args.stamp:
        return _stamp(args.decision, args.repo, args.branch, args.live_tip)

    try:
        with open(args.decision) as f:
            record = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: cannot read decision record: {e}", file=sys.stderr)
        return 2
    if not isinstance(record, dict):
        print("error: decision record must be a JSON object", file=sys.stderr)
        return 2

    live_tip, method = _resolve_live_tip(args.repo, args.branch, args.live_tip)
    ok, reasons = check(record, live_tip, method)
    for r in reasons:
        print(r)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
