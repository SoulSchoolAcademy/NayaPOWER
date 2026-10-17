#!/usr/bin/env python3
"""Read-only fail-closed parity of the team directory, mission, directive and main.

Run: python3 tools/current_state_parity.py --json
Offline: --directory-file FILE --mission-file FILE --directive-file FILE --main-sha SHA
Exit 0 PASS, 1 contradictory FAIL, 2 missing UNKNOWN. A PASS creates no authority.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = "SoulSchoolAcademy/NayaPOWER"
ISSUES = {"directory": 1599, "mission": 2154, "directive": 2601}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def get_directory_venue(body: str) -> str | None:
    m = re.search(r"(?im)^\*\*Live coordination board:\*\*\s*\[#(\d+)\b", body)
    return m.group(1) if m else None


def get_mission_venue(body: str) -> str | None:
    m = re.search(r"(?im)\bLive board\s*=\s*#(\d+)\b", body)
    return m.group(1) if m else None


def get_directive_venue(body: str) -> str | None:
    m = re.search(r"(?im)^Live venue:\s*#(\d+)\b", body)
    return m.group(1) if m else None


def get_directive_sha(body: str) -> str | None:
    m = re.search(r"(?im)^Main tip:\s*\x60([0-9a-f]{40})\x60", body)
    return m.group(1) if m else None


def evaluate(sources: Mapping[str, str], main_sha: str, now: datetime | None = None) -> dict:
    """Pure parity check. Contradictions FAIL; missing proof is UNKNOWN, never PASS."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    body = sources.get("directive", "")
    compiled = re.search(r"(?im)^\*Compiled\s+(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)Z\b", body)
    observations = {
        "directory_venue": get_directory_venue(sources.get("directory", "")),
        "mission_venue": get_mission_venue(sources.get("mission", "")),
        "directive_venue": get_directive_venue(body),
        "directive_main_sha": get_directive_sha(body),
        "actual_main_sha": main_sha,
    }
    missing = [k for k, v in observations.items() if not v]
    if not SHA_RE.fullmatch(main_sha):
        missing.append("valid_main_sha")
    errors = []
    if observations["directory_venue"] and observations["mission_venue"] and observations["directory_venue"] != observations["mission_venue"]:
        errors.append("DIRECTORY_MISSION_VENUE_CONFLICT")
    if observations["directory_venue"] and observations["directive_venue"] and observations["directory_venue"] != observations["directive_venue"]:
        errors.append("DIRECTIVE_VENUE_STALE")
    if SHA_RE.fullmatch(main_sha) and observations["directive_main_sha"] and observations["directive_main_sha"] != main_sha:
        errors.append("DIRECTIVE_MAIN_SHA_STALE")
    age_minutes = None
    if compiled:
        try:
            at = datetime.fromisoformat(compiled.group(1)).replace(tzinfo=timezone.utc)
            age_minutes = round((now.astimezone(timezone.utc) - at).total_seconds() / 60, 2)
            if not -2 <= age_minutes <= 60:
                errors.append("DIRECTIVE_COMPILATION_STALE")
        except ValueError:
            missing.append("valid_compile_timestamp")
    else:
        missing.append("compile_timestamp")
    state = "FAIL" if errors else ("UNKNOWN" if missing else "PASS")
    return {
        "state": state,
        "errors": errors,
        "missing": sorted(set(missing)),
        "observations": observations,
        "directive_age_minutes": age_minutes,
        "note": "Read-only source parity; not production, consent, or user-outcome proof",
    }


def github_get(path: str, token: str | None, api_url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "NayaPOWER-current-state-parity/1",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(api_url.rstrip("/") + path, headers=headers), timeout=20) as response:
        return json.load(response)


def load_live(repo: str, api_url: str) -> tuple[dict[str, str], str]:
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
        raise ValueError("invalid repo identifier")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    sources = {}
    for name, issue_id in ISSUES.items():
        result = github_get(f"/repos/{repo}/issues/{issue_id}", token, api_url)
        if not isinstance(result.get("body"), str):
            raise ValueError(f"missing source issue {issue_id}")
        sources[name] = result["body"]
    ref = github_get(f"/repos/{repo}/git/ref/heads/main", token, api_url)
    sha = (ref.get("object") or {}).get("sha")
    if not isinstance(sha, str):
        raise ValueError("missing main SHA")
    return sources, sha


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repository", default=REPO)
    p.add_argument("--api-url", default="https://api.github.com")
    for name in ISSUES:
        p.add_argument("--" + name + "-file", type=Path)
    p.add_argument("--main-sha")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    offline = any([args.main_sha, *(getattr(args, name + "_file") for name in ISSUES)])
    try:
        if offline:
            if not args.main_sha or any(not getattr(args, name + "_file") for name in ISSUES):
                raise ValueError("offline requires all files and main SHA")
            sources = {name: getattr(args, name + "_file").read_text(encoding="utf-8") for name in ISSUES}
            main_sha = args.main_sha
        else:
            sources, main_sha = load_live(args.repository, args.api_url)
        result = evaluate(sources, main_sha)
    except (OSError, ValueError, KeyError, HTTPError, URLError, TimeoutError) as ex:
        # Never expose API responses or credentials, including when GitHub is down.
        result = {"state": "UNKNOWN", "errors": ["SOURCE_UNAVAILABLE"],
                  "missing": [type(ex).__name__], "note": "Fail closed; reread sources"}
    result["sources"] = {k: f"{args.repository}#{v}" for k, v in ISSUES.items()}
    if args.json:
        print(json.dumps(result, sort_keys=True, indent=2))
    else:
        print("CURRENT_STATE_PARITY " + result["state"] + " " + ",".join(result["errors"]))
    return {"PASS": 0, "FAIL": 1, "UNKNOWN": 2}[result["state"]]


if __name__ == "__main__":
    sys.exit(main())
