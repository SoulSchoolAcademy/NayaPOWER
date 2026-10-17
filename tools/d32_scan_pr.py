"""D32 PR document scanner — the wiring that makes the D32 gate live.

The D32 gate (tools/d32_gate.py) judges markdown documents. This script is
the wire between that mechanism and the live operating path: on every pull
request it lists the markdown documents the PR adds or changes and runs the
gate on each one. A single FAIL blocks the check.

Usage (exactly as CI invokes it):
    python3 tools/d32_scan_pr.py --base <base_rev> --head <head_rev>

    base_rev should be a REF (e.g. origin/main), not a recorded SHA — the
    merge-base is resolved live at scan time, so a stale recorded base SHA
    can never widen the diff to include the base branch's own progress.

Exit codes:
    0  all changed documents PASS (or no markdown changed) — check green
    1  at least one document FAILs — check red, violation blocks
    2  scanner error (bad args, git failure, unreadable tree) — fail closed

Design notes:
- Whole-file scanning: a PR that touches a document brings that document
  under D32. Drive-by edits to legacy docs must add the humility section.
- Fail-closed on scanner errors: a gate that cannot run must never report
  green. Transient git failures are rare (fetch-depth: 0 checkout) and a
  red check with an explicit scanner error is honest, not noisy.
- Only files present in the working tree are scanned (handles renames and
  mid-flight deletions without crashing).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.d32_gate import check_document


def _resolve_merge_base(base: str, head: str) -> str:
    """Resolve the live merge-base. Never trust a recorded base SHA.

    GitHub's pull_request.base.sha can be stale relative to the merge commit
    it builds (observed 2026-10-11: base.sha named f2c614a while the merge
    commit was built on b461609b — the scan then judged main's own progress
    as the PR's changes). Resolving the merge-base at scan time from a base
    REF (e.g. origin/main) is immune to that staleness.
    """
    out = subprocess.run(
        ["git", "merge-base", base, head],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        raise RuntimeError(f"git merge-base failed: {out.stderr.strip()[:300]}")
    return out.stdout.strip()


def _git_diff_names(base: str, head: str) -> tuple[str, list[str]]:
    """Markdown files changed between the live merge-base and head.

    Returns (merge_base_sha, names). The three-dot form makes the merge-base
    explicit so a stale recorded base can never widen the diff.
    """
    merge_base = _resolve_merge_base(base, head)
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT",
         f"{merge_base}...{head}", "--", "*.md"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        raise RuntimeError(f"git diff failed: {out.stderr.strip()[:300]}")
    names = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
    return merge_base, names


def scan(base: str, head: str) -> dict:
    """Run the D32 gate over every changed markdown document. Returns summary."""
    try:
        merge_base, names = _git_diff_names(base, head)
    except RuntimeError as exc:
        return {"verdict": "SCANNER_ERROR", "error": str(exc),
                "base": base, "head": head, "documents": []}

    documents: list[dict] = []
    for name in names:
        path = Path(name)
        if not path.is_file():
            documents.append({"path": name, "verdict": "SKIPPED",
                              "note": "not present in working tree"})
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            documents.append({"path": name, "verdict": "SCANNER_ERROR",
                              "note": f"unreadable: {exc}"})
            continue
        result = check_document(text)
        documents.append({"path": name, "verdict": result["verdict"],
                          "violations": result["violations"]})

    if any(d["verdict"] == "SCANNER_ERROR" for d in documents):
        verdict = "SCANNER_ERROR"
    elif any(d["verdict"] == "FAIL" for d in documents):
        verdict = "FAIL"
    else:
        verdict = "PASS"
    failed = sum(1 for d in documents if d["verdict"] == "FAIL")
    return {
        "verdict": verdict,
        "base": base,
        "head": head,
        "merge_base": merge_base,
        "documents": documents,
        "summary": (f"{len(documents)} document(s) scanned, {failed} failed"
                    if documents else "no markdown documents changed — nothing to scan"),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Scan PR documents with the D32 gate.")
    parser.add_argument("--base", required=True,
                        help="base rev — prefer a ref like origin/main (merge-base resolved live)")
    parser.add_argument("--head", required=True, help="head rev (PR merge commit)")
    args = parser.parse_args(argv[1:])

    result = scan(args.base, args.head)
    print(json.dumps(result, indent=2))
    for doc in result["documents"]:
        v = doc["verdict"]
        extra = ""
        if v == "FAIL":
            rules = sorted({x["rule"] for x in doc["violations"]})
            extra = f" — rules violated: {', '.join(rules)} ({len(doc['violations'])} violations)"
        print(f"[{v}] {doc['path']}{extra}", file=sys.stderr)

    if result["verdict"] == "PASS":
        return 0
    if result["verdict"] == "FAIL":
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
