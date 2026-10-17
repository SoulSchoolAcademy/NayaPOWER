#!/usr/bin/env python3
"""EVOLVE improvement receipt (CANDIDATE).

EVOLVE = the system getting better at getting better, with *measured*
improvement and proof. This tool assembles the evidence; it never scores.

Honesty boundary: a machine that emits a 0-10 score from a formula it
invented is theater. This tool emits an evidence ledger — every claim cites
a commit SHA, a file path, or a test. The score is made by a human (or a
seat) from this evidence, on #1725, in the open.

Usage:
  python3 tools/evolve_receipt.py build --repo <gitdir> \\
      --since <rev> --until <rev> --out <receipt.json>
  --until defaults to HEAD. --since is required.

Self-improvement surfaces (a commit counts as an improvement candidate only
if it touches at least one):
  tools/, kernel/, tests/, supabase/migrations/,
  BRAIN/03-KERNEL/, BRAIN/04-INTELLIGENCE/,
  .naya/proof/, .naya/capture/

Exit codes: 0 = receipt written; 1 = usage/repo error; 2 = git failure.

Status: CANDIDATE (Naya 4, EVOLVE driver, 2026-10-08). Not verified, not
merged, not deployed. Landing requires the Scorecard Law merge protocol
after the base CI wave heals.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Files under these prefixes are where self-improvement lands.
SURFACES = (
    "tools/",
    "kernel/",
    "tests/",
    "supabase/migrations/",
    "BRAIN/03-KERNEL/",
    "BRAIN/04-INTELLIGENCE/",
    ".naya/proof/",
    ".naya/capture/",
)

MAX_COMMITS = 2000


def _git(repo: str, *args: str) -> str:
    """Run git in repo; raise RuntimeError on failure (caller maps to exit 2)."""
    try:
        proc = subprocess.run(
            ["git", "-C", repo, *args],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git executable not found") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()[:300]}")
    return proc.stdout


def _is_repo(repo: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", repo, "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def _on_surface(path: str) -> bool:
    return any(path.startswith(prefix) or path == prefix.rstrip("/") for prefix in SURFACES)


def _list_commits(repo: str, since: str, until: str) -> list[str]:
    out = _git(
        repo, "log", "--no-merges", f"--max-count={MAX_COMMITS}",
        "--format=%H", f"{since}..{until}",
    )
    return [line.strip() for line in out.splitlines() if line.strip()]


def _describe_commit(repo: str, sha: str) -> dict:
    meta = _git(repo, "show", "-s", "--format=%H|%aI|%an|%s", sha)
    parts = meta.strip().split("|", 3)
    full, date, author, subject = (parts + ["", "", "", ""])[:4]
    files_out = _git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", sha)
    files = [f for f in files_out.splitlines() if f.strip()]
    surface_files = sorted(f for f in files if _on_surface(f))
    return {
        "sha": full,
        "date": date,
        "author": author,
        "subject": subject,
        "files_total": len(files),
        "surface_files": surface_files,
        "has_tests": any(f.startswith("tests/") for f in files),
    }


def build(repo: str, since: str, until: str) -> dict:
    if not _is_repo(repo):
        raise ValueError(f"not a git work tree: {repo}")
    tip = _git(repo, "rev-parse", until).strip()
    commits = _list_commits(repo, since, until)
    improvements = []
    for sha in commits:
        desc = _describe_commit(repo, sha)
        if desc["surface_files"]:
            desc["evidence"] = (
                f"commit {desc['sha']} touched {len(desc['surface_files'])} "
                f"self-improvement-surface file(s); tests: "
                f"{'present' if desc['has_tests'] else 'absent'}"
            )
            improvements.append(desc)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "tool": "tools/evolve_receipt.py",
        "status": "CANDIDATE",
        "generated_at": now,
        "repo": str(Path(repo).resolve()),
        "since": since,
        "until": until,
        "tip": tip,
        "commits_scanned": len(commits),
        "improvements": improvements,
        "summary": {
            "improvement_commits": len(improvements),
            "improvement_commits_with_tests": sum(1 for i in improvements if i["has_tests"]),
        },
        "caveats": [
            "Landing a file under a self-improvement surface is NOT proof of improvement.",
            "This receipt assembles evidence; the EVOLVE score is made by a human from it.",
            "CI verdicts are not read locally — verify check-runs on the cited SHAs remotely.",
            f"Scan capped at {MAX_COMMITS} commits; windows larger than that are truncated.",
        ],
    }


def cmd_build(args: argparse.Namespace) -> int:
    repo = args.repo
    if not repo:
        print("error: --repo is required", file=sys.stderr)
        return 1
    try:
        receipt = build(repo, args.since, args.until)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"receipt: {receipt['summary']['improvement_commits']} improvement commits "
          f"of {receipt['commits_scanned']} scanned -> {out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="EVOLVE improvement-receipt generator")
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build", help="assemble an improvement receipt for a rev window")
    b.add_argument("--repo", required=True, help="git work tree to scan")
    b.add_argument("--since", required=True, help="start rev (exclusive)")
    b.add_argument("--until", default="HEAD", help="end rev (inclusive, default HEAD)")
    b.add_argument("--out", required=True, help="receipt JSON path to write")
    b.set_defaults(func=cmd_build)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
