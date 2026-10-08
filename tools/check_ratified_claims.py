#!/usr/bin/env python3
"""check_ratified_claims.py — LAW rung 1: ratified-claim integrity (advisory).

Prime 2 (Law Is the Code): a RATIFIED marking is structure, not decoration.
CONSTITUTION/0003-AUTOMATIC-SUPER-BRAIN-AMENDMENT-V1.md says it plainly:
"this amendment becomes constitutional law ONLY on the Human Director's
explicit word." A bare `RATIFIED` claim with no ratification record is exactly
what #1853 had to correct by hand ("correct false ratification claim").

This tool scans the ADDED lines of a unified diff and flags any assertion of
`RATIFIED` / `RATIFICATION` that is not accompanied by a ratification record.
A record is the canonical marker:

    RATIFICATION-RECORD: <authority> <reference> <date>
    e.g. RATIFICATION-RECORD: Shawn Vibert (Human Director), #1354 comment 6056195765, 2026-10-08

The marker must carry an authority citation: an issue/PR/comment reference
(#NNNN) or a date (YYYY-MM-DD). Scope: the file's added lines — the record
belongs to the artifact being ratified.

Fail-closed: unreadable or malformed diff input is a FAIL, never a pass.
UNKNOWN != PASS.

This check is ADVISORY ONLY. In CI it runs with `|| true` and never blocks a
merge. Promotion to a required gate needs the Human Director's explicit word.

Known limitation (honest rung boundary): the tool verifies a record EXISTS and
is cited — it does not authenticate the record (a fabricated #NNNN reference
would pass). Record-authenticity verification is rung 2, not this tool.

Exit codes: 0 = PASS (no unrecorded claims), 1 = FAIL (unrecorded claims found,
or input unreadable), 2 = usage error.

Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOOL_ID = "RATIFIED-CLAIM-GATE-V1"

# Assertion forms: "RATIFIED", "ratified", "RATIFICATION", "ratification".
CLAIM_RE = re.compile(r"(?i)\bratifi(?:ed|cation)\b")

# Canonical record marker, case-insensitive: RATIFICATION-RECORD: <citation>
RECORD_RE = re.compile(r"(?i)\bratification-record\s*:")

# Authority citation inside the marker: #NNNN issue/PR/comment ref or YYYY-MM-DD.
CITATION_RE = re.compile(r"#\d{3,}|20\d\d-\d\d-\d\d")

# Machinery that must talk about ratified claims to do its job is exempt from
# flagging itself. Paths are matched as substrings of the diff's file path.
SELF_EXEMPT_SUBSTRINGS = (
    "check_ratified_claims",
    "test_check_ratified_claims",
    "ratified-claim-gate",
)

# Diff metadata lines that are never content.
META_PREFIXES = ("--- ", "@@ ", "diff ", "index ", "new file", "old mode",
                 "new mode", "similarity", "rename ")


def parse_diff_files(diff_text: str) -> dict[str, list[str]]:
    """Map each file path in a unified diff to its ADDED lines (no '+' prefix)."""
    files: dict[str, list[str]] = {}
    current: str | None = None
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            path = raw[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            if path in ("/dev/null", "dev/null"):
                current = None
                continue
            current = path
            files.setdefault(current, [])
        elif current is not None and raw.startswith("+"):
            if any(raw.startswith(p) for p in META_PREFIXES):
                continue
            files[current].append(raw[1:])
    return files


def is_exempt(path: str) -> bool:
    return any(s in path for s in SELF_EXEMPT_SUBSTRINGS)


def file_has_valid_record(added_lines: list[str]) -> tuple[bool, str]:
    """True if any added line carries a RATIFICATION-RECORD: with citation."""
    saw_marker = False
    for line in added_lines:
        if RECORD_RE.search(line):
            saw_marker = True
            if CITATION_RE.search(line):
                return True, line.strip()
    if saw_marker:
        return False, ("RATIFICATION-RECORD marker present but lacks authority "
                       "citation (#NNNN or YYYY-MM-DD)")
    return False, ""


def check(diff_text: str) -> dict:
    files = parse_diff_files(diff_text)
    violations: list[dict] = []
    files_scanned = 0
    for path, added in files.items():
        if is_exempt(path):
            continue
        files_scanned += 1
        claim_lines = [ln for ln in added if CLAIM_RE.search(ln)]
        if not claim_lines:
            continue
        ok, detail = file_has_valid_record(added)
        if not ok:
            reason = detail or (
                "RATIFIED/RATIFICATION asserted with no RATIFICATION-RECORD marker "
                "(authority citation: #NNNN or YYYY-MM-DD) in the same file's added lines"
            )
            violations.append({
                "path": path,
                "reason": reason,
                "claim_lines": [ln.strip() for ln in claim_lines[:5]],
            })
    return {
        "tool": TOOL_ID,
        "pass": not violations,
        "files_scanned": files_scanned,
        "violations": violations,
    }


def read_diff(spec: str) -> str:
    if spec == "-":
        return sys.stdin.read()
    p = Path(spec[1:] if spec.startswith("@") else spec)
    try:
        return p.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot read diff input {spec!r}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Advisory gate: unrecorded RATIFIED claims fail.")
    ap.add_argument("--diff", required=True,
                    help="unified diff file (prefix @), or - for stdin")
    ap.add_argument("--json", action="store_true", help="emit JSON result")
    args = ap.parse_args(argv)
    try:
        diff_text = read_diff(args.diff)
    except ValueError as exc:
        # Fail closed: unreadable input is a FAIL, never a pass.
        msg = str(exc)
        if args.json:
            print(json.dumps({"tool": TOOL_ID, "pass": False,
                              "reason": msg, "violations": []}, indent=2))
        else:
            print(f"FAIL: {msg}")
        return 1
    result = check(diff_text)
    if args.json:
        print(json.dumps(result, indent=2))
    elif result["pass"]:
        print(f"PASS: {result['files_scanned']} file(s) scanned, no unrecorded RATIFIED claims.")
    else:
        print(f"FAIL: {len(result['violations'])} file(s) assert RATIFIED without a ratification record.")
        for v in result["violations"]:
            print(f"  - {v['path']}: {v['reason']}")
            for ln in v["claim_lines"]:
                print(f"      > {ln[:160]}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
