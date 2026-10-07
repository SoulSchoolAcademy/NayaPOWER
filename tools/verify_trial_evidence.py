#!/usr/bin/env python3
"""Verify a trial claim's raw evidence is durably preserved.

Implements BRAIN/03-KERNEL/SCHEMA/TRIAL-EVIDENCE-V1.json.

Usage:
    python3 tools/verify_trial_evidence.py <descriptor.json> [--repo ROOT] [--committed]

The descriptor names raw_evidence_paths. Every path must resolve to real,
durable bytes inside the repository. Fails closed (exit 2) when any path is:

  - shaped like an ephemeral location (/tmp, /var/tmp, /dev/shm, ...), or
  - a symlink or `..` traversal whose RESOLVED target escapes the repo, or
  - an absolute path outside the repository root, or
  - missing from the working tree, or
  - (with --committed) not tracked by git at HEAD,
  - (always) when the repository root itself lives on ephemeral storage.

A verifier that cannot fail is not a verifier: this tool is MEANT to reject
claims like Trial-4's, whose raw data lived at /tmp/trial4/RESULTS.md and was
wiped before independent verification could run.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "BRAIN" / "03-KERNEL" / "SCHEMA" / "TRIAL-EVIDENCE-V1.json"

EPHEMERAL_PREFIXES = ("/tmp/", "/tmp", "/var/tmp/", "/dev/shm/")


def is_ephemeral(path: str) -> bool:
    p = path.strip()
    return p == "/tmp" or p.startswith(EPHEMERAL_PREFIXES)


def check(descriptor: dict, repo: Path, require_committed: bool) -> list[str]:
    """Return a list of failure strings; empty means the claim's evidence is sound."""
    failures: list[str] = []
    paths = descriptor.get("raw_evidence_paths")
    if not isinstance(paths, list) or not paths:
        return ["descriptor must contain a non-empty raw_evidence_paths list"]
    for raw in paths:
        if not isinstance(raw, str) or not raw.strip():
            failures.append(f"evidence path is empty: {raw!r}")
            continue
        p = raw.strip()
        if is_ephemeral(p):
            failures.append(
                f"ephemeral evidence location (TRIAL-EVIDENCE-V1 forbids /tmp): {p}"
            )
            continue
        candidate = Path(p)
        if not candidate.is_absolute():
            candidate = repo / p
        # Resolve symlinks and `..` BEFORE any trust decision. A bare string
        # check cannot see through a symlink or a traversal: without this,
        # an in-repo symlink -> /tmp or a `../../tmp/...` relative path sails
        # through every check below while pointing at ephemeral bytes.
        try:
            resolved = candidate.resolve()
        except OSError as exc:
            failures.append(f"evidence path cannot be resolved: {p} ({exc})")
            continue
        try:
            rel = resolved.relative_to(repo)
        except ValueError:
            failures.append(
                f"evidence path escapes the repository root {repo}: {p}"
            )
            continue
        if not resolved.is_file():
            failures.append(f"evidence path does not resolve to a file: {p}")
            continue
        if require_committed:
            r = subprocess.run(
                ["git", "ls-files", "--error-unmatch", rel.as_posix()],
                cwd=repo,
                capture_output=True,
            )
            if r.returncode != 0:
                failures.append(
                    f"evidence not committed to the repository (uncommitted at HEAD): {p}"
                )
    return failures


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Verify trial evidence durability.")
    ap.add_argument("descriptor", help="JSON trial-claim descriptor file")
    ap.add_argument("--repo", default=".", help="repository root (default: cwd)")
    ap.add_argument(
        "--committed",
        action="store_true",
        help="also require each evidence path to be git-tracked",
    )
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    # A repository checked out under ephemeral storage is not durable storage.
    if is_ephemeral(str(repo)):
        print(
            f"FAIL: repository root itself is ephemeral storage: {repo}",
            file=sys.stderr,
        )
        return 2
    try:
        descriptor = json.loads(Path(args.descriptor).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read descriptor: {exc}", file=sys.stderr)
        return 2

    failures = check(descriptor, repo, args.committed)
    if failures:
        print("FAIL: trial evidence unverifiable", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 2
    print("OK: all trial evidence resolves to durable repository bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
