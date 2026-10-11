#!/usr/bin/env python3
"""Directive Register — status change gate.

Refuses silent hand-edits to directive statuses. Every status change between
the base ref and HEAD must carry a matching audit record (written by
tools/directive_register_promote.py) in the same PR:

  - a status change with no audit entry        -> VIOLATION
  - an audit entry with no status change       -> VIOLATION
  - an audit entry whose from/to do not match
    the actual old/new statuses                -> VIOLATION
  - a malformed audit line                     -> VIOLATION
  - the register itself unloadable at HEAD     -> FAIL-CLOSED (never a pass)

If the base ref has no register (the initial-registration PR), transition
checks are skipped and only the new register's own validity is enforced.

Exit codes: 0 = clean, 1 = violations found, 2 = fail-closed error.

Usage:
  python3 tools/directive_register_status_check.py --repo . --base-ref origin/main
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from directive_register import (  # noqa: E402
    DirectiveRegisterError,
    default_register_path,
    load_register,
)
from directive_register_promote import (  # noqa: E402
    AUDIT_KEYS,
    STATUS_ORDER,
    default_audit_path,
)

REGISTER_REL = Path("BRAIN") / "01-GOVERNANCE" / "directive-register.json"
AUDIT_REL = Path("BRAIN") / "01-GOVERNANCE" / "directive-register-audit.log"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True
    )


def read_at_ref(repo: Path, ref: str, rel: Path) -> str | None:
    """File content at a git ref, or None if the file does not exist there."""
    out = _git(repo, "show", f"{ref}:{rel.as_posix()}")
    if out.returncode != 0:
        return None
    return out.stdout


def added_audit_lines(repo: Path, base_ref: str, head_ref: str) -> tuple[list[str], str | None]:
    """Added (non-context) lines of the audit log in base...head.

    Returns (lines, error). Lines starting with '+' minus the '+++' header.
    """
    out = _git(repo, "diff", f"{base_ref}...{head_ref}", "--", AUDIT_REL.as_posix())
    if out.returncode != 0:
        return [], f"git diff failed: {out.stderr.strip()}"
    lines = [
        line[1:]
        for line in out.stdout.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    return lines, None


def parse_audit_line(line: str, lineno: int) -> tuple[dict | None, str | None]:
    try:
        rec = json.loads(line)
    except json.JSONDecodeError as exc:
        return None, f"audit line {lineno}: not valid JSON: {exc}"
    if not isinstance(rec, dict):
        return None, f"audit line {lineno}: not an object"
    missing = AUDIT_KEYS - set(rec.keys())
    if missing:
        return None, f"audit line {lineno}: missing keys {sorted(missing)}"
    extra = set(rec.keys()) - AUDIT_KEYS
    if extra:
        return None, f"audit line {lineno}: unexpected keys {sorted(extra)}"
    if rec["to"] not in STATUS_ORDER or rec["from"] not in STATUS_ORDER:
        return None, (
            f"audit line {lineno}: from/to outside the taxonomy "
            f"({rec['from']!r} -> {rec['to']!r})"
        )
    return rec, None


def run(repo: Path, base_ref: str, head_ref: str) -> int:
    head_text = read_at_ref(repo, head_ref, REGISTER_REL)
    if head_text is None:
        print(f"FAIL-CLOSED: register missing at {head_ref}", file=sys.stderr)
        return 2
    try:
        head_dirs = json.loads(head_text)
    except json.JSONDecodeError as exc:
        print(f"FAIL-CLOSED: register at {head_ref} is not valid JSON: {exc}",
              file=sys.stderr)
        return 2
    # The authority validates shape, ids, duplicates, and the taxonomy.
    tmp = repo / ".directive-register-status-check-tmp.json"
    try:
        tmp.write_text(head_text, encoding="utf-8")
        load_register(tmp)
    except DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    finally:
        tmp.unlink(missing_ok=True)

    base_text = read_at_ref(repo, base_ref, REGISTER_REL)
    if base_text is None:
        # Initial-registration PR: no transitions to check.
        print(
            "directive-register-status: no register at base ref "
            f"({base_ref}); transition checks skipped, register valid at HEAD"
        )
        return 0
    try:
        base_dirs = json.loads(base_text)
    except json.JSONDecodeError as exc:
        print(f"FAIL-CLOSED: register at {base_ref} is not valid JSON: {exc}",
              file=sys.stderr)
        return 2

    base_status = {e["id"]: e["status"] for e in base_dirs if isinstance(e, dict)}
    head_status = {e["id"]: e["status"] for e in head_dirs if isinstance(e, dict)}
    changed = {
        did: (base_status.get(did), head_status.get(did))
        for did in set(base_status) | set(head_status)
        if base_status.get(did) != head_status.get(did)
    }

    lines, err = added_audit_lines(repo, base_ref, head_ref)
    if err is not None:
        print(f"FAIL-CLOSED: {err}", file=sys.stderr)
        return 2

    violations: list[str] = []
    records: list[dict] = []
    for i, line in enumerate(lines, start=1):
        rec, verr = parse_audit_line(line, i)
        if verr is not None:
            violations.append(f"VIOLATION: {verr}")
            continue
        records.append(rec)

    # Every changed status needs a matching audit record.
    for did, (old, new) in sorted(changed.items()):
        match = [
            r for r in records
            if r["directive_id"] == did and r["from"] == old and r["to"] == new
        ]
        if not match:
            violations.append(
                f"VIOLATION: {did} status {old} -> {new} has no matching audit "
                f"record in this PR (promote via tools/directive_register_promote.py)"
            )
    # Every audit record needs a matching status change.
    for r in records:
        actual = changed.get(r["directive_id"])
        if actual is None:
            violations.append(
                f"VIOLATION: audit record for {r['directive_id']} "
                f"({r['from']} -> {r['to']}) matches no status change in this PR"
            )
        elif (r["from"], r["to"]) != actual:
            violations.append(
                f"VIOLATION: audit record for {r['directive_id']} claims "
                f"{r['from']} -> {r['to']} but the register moved "
                f"{actual[0]} -> {actual[1]}"
            )

    for v in violations:
        print(v)
    print(
        f"directive-register-status: changed={len(changed)} "
        f"audit_records={len(records)} violations={len(violations)}"
    )
    return 1 if violations else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Directive register status change gate")
    ap.add_argument("--repo", default=".", help="repo root")
    ap.add_argument("--base-ref", default="origin/main", help="git ref to diff against")
    ap.add_argument("--head-ref", default="HEAD", help="git ref to check")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    # Imported names above keep linters honest about the seam we extend.
    _ = (default_register_path, default_audit_path)
    return run(repo, args.base_ref, args.head_ref)


if __name__ == "__main__":
    sys.exit(main())
