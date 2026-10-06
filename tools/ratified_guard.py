#!/usr/bin/env python3
"""Ratified-object guard (SN-0408 enforcement).

A ratified object (law, code, protocol Shawn spoke into existence) must never
disappear through ordinary cleanup, deduplication, or schema repair. This tool
builds the manifest of ratified objects from a tree and fails if a proposed
diff deletes any of them without explicit retirement authorization.

Usage:
  python tools/ratified_guard.py --manifest <tree-root>
      Print the ratified manifest (one path per line).

  python tools/ratified_guard.py --check-diff --base-ref <ref> --head-ref <ref>
      Fail (exit 1) if the diff deletes a ratified object without a
      RATIFIED-RETIREMENT record. Must run inside a git checkout.

Ratified = any capture/note whose metadata records ratification by the Human
Director (source.ratification.by present, or Truth state RATIFIED/IMMUTABLE).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RATIFIED_MARKERS_MD = (
    "truth state:** ratified",
    "truth state: ratified",
    "**truth state:** ratified",
)

RETIREMENT_PREFIX = "RATIFIED-RETIREMENT-"


def _load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def is_ratified_capture(data: dict) -> bool:
    """v2: source.ratification.by present. v1: truth_state RATIFIED/IMMUTABLE."""
    if not isinstance(data, dict):
        return False
    source = data.get("source")
    if isinstance(source, dict):
        rat = source.get("ratification")
        if isinstance(rat, dict) and rat.get("by"):
            return True
    ts = str(data.get("truth_state", "")).upper()
    return ts in ("RATIFIED", "IMMUTABLE")


def is_ratified_markdown(text: str) -> bool:
    low = text.lower()
    return any(m in low for m in RATIFIED_MARKERS_MD)


def build_manifest(root: Path) -> set[str]:
    """Return repo-relative paths of ratified objects under root."""
    root = Path(root)
    manifest: set[str] = set()

    capture_dir = root / ".naya" / "capture"
    if capture_dir.is_dir():
        for path in sorted(capture_dir.glob("*.json")):
            data = _load_json(path)
            if data is not None and is_ratified_capture(data):
                manifest.add(path.relative_to(root).as_posix())

    # Smart-note markdown trees (both numbering streams).
    for base in (root / "BRAIN", root / "smart-notes-2026-09-30"):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if is_ratified_markdown(text):
                manifest.add(path.relative_to(root).as_posix())

    return manifest


def deleted_paths_in_diff(base_ref: str, head_ref: str, repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=D", f"{base_ref}...{head_ref}"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line.strip()]


def added_paths_in_diff(base_ref: str, head_ref: str, repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=A", f"{base_ref}...{head_ref}"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line.strip()]


def check_diff(
    manifest: set[str],
    deleted: list[str],
    added: list[str],
) -> list[str]:
    """Return human-readable violations. Empty list = pass."""
    violations: list[str] = []
    retired = {p for p in added if Path(p).name.startswith(RETIREMENT_PREFIX)}
    for path in deleted:
        if path in manifest and not retired:
            violations.append(
                f"RATIFIED OBJECT DELETED WITHOUT RETIREMENT RECORD: {path}\n"
                f"  Per SN-0408 (Deletion Discipline): understand fully before deleting.\n"
                f"  A ratified object is never 'cleanup'. To retire one, add a\n"
                f"  {RETIREMENT_PREFIX}<id>.md record documenting what it is,\n"
                f"  what purpose it served, what supersedes it, and the Human\n"
                f"  Director's explicit word."
            )
    return violations


def _git_show_tree(ref: str, repo: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(
        ["git", "archive", ref], cwd=repo, capture_output=True, check=True
    )
    subprocess.run(
        ["tar", "-x", "-C", str(dest)], input=archive.stdout, check=True
    )


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Ratified-object deletion guard")
    ap.add_argument("--manifest", metavar="ROOT", help="print ratified manifest")
    ap.add_argument("--check-diff", action="store_true", help="check a diff")
    ap.add_argument("--base-ref", default="origin/main")
    ap.add_argument("--head-ref", default="HEAD")
    ap.add_argument("--repo", default=".")
    args = ap.parse_args(argv)

    if args.manifest:
        for path in sorted(build_manifest(Path(args.manifest))):
            print(path)
        return 0

    if args.check_diff:
        import tempfile

        repo = Path(args.repo)
        with tempfile.TemporaryDirectory() as tmp:
            base_tree = Path(tmp) / "base"
            _git_show_tree(args.base_ref, repo, base_tree)
            manifest = build_manifest(base_tree)
        deleted = deleted_paths_in_diff(args.base_ref, args.head_ref, repo)
        added = added_paths_in_diff(args.base_ref, args.head_ref, repo)
        violations = check_diff(manifest, deleted, added)
        if violations:
            print("RATIFIED GUARD: FAIL", file=sys.stderr)
            for v in violations:
                print(v, file=sys.stderr)
            return 1
        print(f"RATIFIED GUARD: PASS ({len(manifest)} ratified objects, "
              f"{len(deleted)} deletions checked)")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
