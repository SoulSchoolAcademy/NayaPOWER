"""D32 scan — wire the D32 uncertainty-discipline gate into live PR review.

The gate (tools/d32_gate.py) proves itself on its own tests. This scanner
applies it to real work: every markdown file under BRAIN/ changed in a PR.

Verdict policy (no new false precision slips through; old content is
grandfathered so the gate never becomes a permission bottleneck):
  - NEW files: full check_document. Any violation FAILs the PR.
  - MODIFIED files: R1/R3 enforced on ADDED lines only. Violations on
    pre-existing lines, and a missing DOES-NOT-CLAIM section, are WARNings:
    visible, never blocking. The corpus ratchets toward compliance as files
    are touched, without punishing typo fixes.

Usage:
    python3 tools/d32_scan.py --base <sha> --head <sha> [--scope BRAIN/]
                             [--format human|json]
    Exit 0: no FAILs. Exit 1: at least one file FAILs (blocks the PR).
    Exit 2: usage / git error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.d32_gate import check_document

_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def _git(*args: str) -> str:
    """Run git, return stdout. Raises RuntimeError on failure."""
    try:
        r = subprocess.run(
            ["git", *args], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git {' '.join(args)} failed: {e.stderr.strip()}")
    return r.stdout


def changed_md_files(base: str, head: str, scope: str) -> list[tuple[str, str]]:
    """Return [(status, path)] for .md files under scope changed base..head.

    Status is 'A' (added) or 'M' (modified, incl. renamed). Deleted files
    are skipped. Scope is a path prefix like 'BRAIN/'.
    """
    out = _git("diff", "--name-status", f"{base}", f"{head}", "--", scope)
    files: list[tuple[str, str]] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0][0]  # A, M, D, R100, ...
        if status == "D":
            continue
        # Renames: "R100\told\tnew" — scan the new path as modified.
        path = parts[-1]
        if not path.endswith(".md"):
            continue
        files.append(("A" if status == "A" else "M", path))
    return files


def added_line_numbers(base: str, head: str, path: str) -> set[int]:
    """Return 1-indexed line numbers added to path in base..head."""
    out = _git("diff", "-U0", f"{base}", f"{head}", "--", path)
    added: set[int] = set()
    new_line = 0
    for line in out.splitlines():
        m = _HUNK_RE.match(line)
        if m:
            new_line = int(m.group(1))
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue
        if line.startswith("+"):
            added.add(new_line)
            new_line += 1
        elif line.startswith("-"):
            continue  # removed line: new-file counter does not advance
        else:
            # With -U0 there should be no context lines, but be tolerant.
            new_line += 1
    return added


def scan_file(text: str, status: str, added: set[int]) -> dict:
    """Scan one file. Returns {verdict, violations, warnings}.

    Verdicts: FAIL (blocks the PR), WARN (visible, never blocks), PASS.
    """
    result = check_document(text)
    failures: list[dict] = []
    warnings: list[dict] = []
    for v in result["violations"]:
        if status == "A":
            failures.append(v)  # new files: full compliance from birth
        elif v["rule"] == "R2":
            warnings.append({**v, "note": "grandfathered: pre-existing document"})
        elif v["line"] in added:
            failures.append(v)  # new unsourced numbers / confidence: block
        else:
            warnings.append({**v, "note": "grandfathered: pre-existing line"})
    verdict = "FAIL" if failures else ("WARN" if warnings else "PASS")
    return {"verdict": verdict, "violations": failures, "warnings": warnings}


def scan_pr(base: str, head: str, scope: str) -> dict:
    """Scan all changed .md files under scope. Returns the full report."""
    files = changed_md_files(base, head, scope)
    report: dict = {"base": base, "head": head, "scope": scope, "files": []}
    for status, path in files:
        try:
            text = _git("show", f"{head}:{path}")
        except RuntimeError:
            # File unreadable at head (e.g. deleted after rename); skip.
            continue
        added = added_line_numbers(base, head, path) if status == "M" else set()
        result = scan_file(text, status, added)
        report["files"].append({"path": path, "status": status, **result})
    report["verdict"] = (
        "FAIL" if any(f["verdict"] == "FAIL" for f in report["files"]) else "PASS"
    )
    return report


def format_human(report: dict) -> str:
    """Human-readable summary."""
    lines = [
        f"D32 scan: base={report['base'][:12]} head={report['head'][:12]} "
        f"scope={report['scope']}"
    ]
    if not report["files"]:
        lines.append("No changed markdown files under scope. PASS.")
        return "\n".join(lines)
    for f in report["files"]:
        lines.append(f"[{f['verdict']}] {f['path']} ({f['status']})")
        for v in f["violations"]:
            lines.append(f"  FAIL L{v['line']} [{v['rule']}] {v['text'][:120]}")
        for w in f["warnings"]:
            lines.append(
                f"  warn L{w['line']} [{w['rule']}] {w['text'][:100]} "
                f"({w.get('note', '')})"
            )
    lines.append(f"Overall: {report['verdict']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="D32 gate: scan changed BRAIN/ docs.")
    ap.add_argument("--base", default="origin/main",
                    help="base ref (default: origin/main)")
    ap.add_argument("--head", default="HEAD", help="head ref (default: HEAD)")
    ap.add_argument("--scope", default="BRAIN/",
                    help="path scope (default: BRAIN/)")
    ap.add_argument("--format", choices=("human", "json"), default="human")
    args = ap.parse_args(argv)
    try:
        report = scan_pr(args.base, args.head, args.scope)
    except RuntimeError as e:
        print(f"d32_scan: {e}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(format_human(report))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
