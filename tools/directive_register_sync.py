#!/usr/bin/env python3
"""Directive Register Sync scanner.

Wires the machine-readable directive register into the PR merge path.

CONTRACT: every master-directive reference (D<n>) appearing in a changed
governance document must resolve against the machine register. A reference
to a directive the register does not know is a stale/phantom reference
(the D35 stale-publication class) and blocks the PR.

Scope (deliberately tight):
  - Files: markdown under BRAIN/01-GOVERNANCE/ (the register's domain).
  - Tokens: \\bD(\\d{1,3})\\b
  - D1..D7   -> OUT_OF_SCOPE (meta-governance / predate the register; excluded
                from the register per Shawn's scoping). Not violations.
  - D8..D65  -> must resolve via the register loader. Unknown -> VIOLATION.
  - D66+     -> VIOLATION (references a directive outside the registered set;
                register it first, then reference it).

FAIL-CLOSED: if the register itself cannot be loaded and validated, the
scanner exits 2 (error) — never 0. A broken authority must block, not pass.

Exit codes: 0 = clean, 1 = violations found, 2 = fail-closed error.

Usage:
  python3 tools/directive_register_sync.py --repo . --files a.md b.md
  python3 tools/directive_register_sync.py --repo . --diff-base origin/main
  python3 tools/directive_register_sync.py --repo . --all   # whole scope
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from directive_register import (  # noqa: E402
    DirectiveRegisterError,
    UnknownDirectiveError,
    default_register_path,
    get_directive,
    load_register,
)

SCOPE_DIR = Path("BRAIN") / "01-GOVERNANCE"
TOKEN_RE = re.compile(r"\bD(\d{1,3})\b")
# D1..D7 are out of scope: meta-governance / predate the register.
IN_SCOPE_MIN = 8


def changed_files(repo: Path, diff_base: str) -> list[Path]:
    """Files changed between diff_base and HEAD, restricted to the scope dir."""
    merge_base = subprocess.run(
        ["git", "merge-base", "HEAD", diff_base],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    base = merge_base.stdout.strip() if merge_base.returncode == 0 else diff_base
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if out.returncode != 0:
        raise DirectiveRegisterError(f"git diff failed: {out.stderr.strip()}")
    files = []
    for line in out.stdout.splitlines():
        p = Path(line.strip())
        if p.suffix.lower() == ".md" and SCOPE_DIR in p.parents:
            files.append(repo / p)
    return files


def scan_file(path: Path, directives: list[dict]) -> tuple[list[str], list[str]]:
    """Return (violations, out_of_scope_notes) for one file.

    Each violation names file:line and the unknown directive id (the witness).
    """
    violations: list[str] = []
    notes: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DirectiveRegisterError(f"Cannot read {path}: {exc}") from exc
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in TOKEN_RE.finditer(line):
            num = int(match.group(1))
            did = f"D{num}"
            if num < IN_SCOPE_MIN:
                notes.append(f"{path}:{lineno}: {did} out of scope (D1-D7 meta-governance)")
                continue
            try:
                get_directive(directives, did)
            except UnknownDirectiveError:
                violations.append(
                    f"{path}:{lineno}: unknown directive {did} — "
                    f"not in the machine register (stale/phantom reference)"
                )
    return violations, notes


def run(repo: Path, files: list[Path], register_path: Path | None) -> int:
    try:
        directives = load_register(register_path)
    except DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    all_violations: list[str] = []
    out_of_scope = 0
    scanned = 0
    for f in files:
        if not f.is_file():
            continue
        scanned += 1
        violations, notes = scan_file(f, directives)
        all_violations.extend(violations)
        out_of_scope += len(notes)
    for v in all_violations:
        print(f"VIOLATION: {v}")
    print(
        f"directive-register-sync: scanned={scanned} "
        f"violations={len(all_violations)} out_of_scope_refs={out_of_scope} "
        f"register_entries={len(directives)}"
    )
    return 1 if all_violations else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Directive register sync gate")
    ap.add_argument("--repo", default=".", help="repo root")
    ap.add_argument("--files", nargs="*", default=None, help="explicit files to scan")
    ap.add_argument("--diff-base", default=None, help="git ref to diff HEAD against")
    ap.add_argument("--all", action="store_true", help="scan the whole scope dir")
    ap.add_argument("--register", default=None, help="override register JSON path")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    register_path = Path(args.register) if args.register else default_register_path()

    if args.files is not None:
        files = [repo / f if not Path(f).is_absolute() else Path(f) for f in args.files]
    elif args.diff_base:
        try:
            files = changed_files(repo, args.diff_base)
        except DirectiveRegisterError as exc:
            print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
            return 2
    elif args.all:
        files = sorted((repo / SCOPE_DIR).rglob("*.md"))
    else:
        ap.error("one of --files, --diff-base, or --all is required")
        return 2
    return run(repo, files, register_path)


if __name__ == "__main__":
    sys.exit(main())
