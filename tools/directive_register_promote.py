#!/usr/bin/env python3
"""Directive Register — status promotion authority.

The register's statuses are facts, not free text. The ONLY honest way to move
a directive forward is through this tool:

  promote --id D60 --to BUILDING \\
      --evidence-comment 6107866014 --actor naya2
  promote --id D60 --to BUILT_AS_CODE \\
      --evidence-pr 2315 --evidence-comment 6107942578 --actor naya2
  promote --id D60 --to ENFORCED \\
      --evidence-pr 2328 --evidence-comment 6107921353 --actor naya2

TRANSITIONS (the register's own taxonomy, one step forward, never back):
  NOT_STARTED -> BUILDING -> BUILT_AS_CODE -> ENFORCED

  - unknown id          -> error (the register authority refuses to certify)
  - corrupt register    -> error (fail-closed, via the register authority)
  - skip-level jump     -> error (NOT_STARTED -> BUILT_AS_CODE is a lie)
  - backward move       -> error (demotion is a separate reviewed action)
  - same-status re-run  -> no-op, exit 0, warning to stderr (idempotent)

EVIDENCE (a promotion without evidence is a claim, not a fact):
  BUILDING      -> --evidence-comment required (the sign-in comment id)
  BUILT_AS_CODE -> --evidence-pr + --evidence-comment required
                   (the build PR and the build sign-out comment id)
  ENFORCED      -> --evidence-pr + --evidence-comment required
                   (the wire PR and the wire sign-out comment id)

AUDIT: every promotion appends one JSONL record to
BRAIN/01-GOVERNANCE/directive-register-audit.log. The register JSON and the
audit log are committed together; the status-check gate refuses any register
status change that has no matching audit record in the same PR.

Exit codes: 0 = promoted (or idempotent no-op), 1 = usage/validation error,
            2 = fail-closed error (register untrustworthy),
            3 = register written but audit append failed (exact recovery
                record is printed — append it manually, then commit).
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from directive_register import (  # noqa: E402
    DirectiveRegisterError,
    UnknownDirectiveError,
    default_register_path,
    get_directive,
    load_register,
)

AUDIT_REL_PATH = Path("BRAIN") / "01-GOVERNANCE" / "directive-register-audit.log"

# The register's taxonomy, in promotion order. Forward one step only.
STATUS_ORDER = ["NOT_STARTED", "BUILDING", "BUILT_AS_CODE", "ENFORCED"]

AUDIT_KEYS = frozenset(
    {
        "directive_id",
        "from",
        "to",
        "evidence_pr",
        "evidence_comment",
        "actor",
        "at",
        "register_sha256",
    }
)


def default_audit_path() -> Path:
    return Path(__file__).resolve().parent.parent / AUDIT_REL_PATH


def _positive_int(value: str, name: str) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    if n <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    return n


def validate_evidence(to_status: str, evidence_pr, evidence_comment) -> tuple[int | None, int]:
    """Return (evidence_pr, evidence_comment) or raise ValueError.

    BUILDING needs only the sign-in comment. BUILT_AS_CODE and ENFORCED need
    the PR and the sign-out comment. Format is validated here; existence is
    the reviewer's job (the audit record links straight to both).
    """
    if to_status == "BUILDING":
        if evidence_comment is None:
            raise ValueError(
                "BUILDING requires --evidence-comment (the sign-in comment id)"
            )
        return None, _positive_int(str(evidence_comment), "--evidence-comment")
    # BUILT_AS_CODE / ENFORCED
    if evidence_pr is None:
        raise ValueError(f"{to_status} requires --evidence-pr (the build/wire PR number)")
    if evidence_comment is None:
        raise ValueError(
            f"{to_status} requires --evidence-comment (the sign-out comment id)"
        )
    return _positive_int(str(evidence_pr), "--evidence-pr"), _positive_int(
        str(evidence_comment), "--evidence-comment"
    )


def build_audit_record(
    directive_id: str,
    from_status: str,
    to_status: str,
    evidence_pr: int | None,
    evidence_comment: int,
    actor: str,
    register_bytes: bytes,
) -> dict:
    return {
        "directive_id": directive_id,
        "from": from_status,
        "to": to_status,
        "evidence_pr": evidence_pr,
        "evidence_comment": evidence_comment,
        "actor": actor,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "register_sha256": hashlib.sha256(register_bytes).hexdigest(),
    }


def promote(
    directive_id: str,
    to_status: str,
    evidence_pr=None,
    evidence_comment=None,
    actor: str = "",
    register_path: Path | None = None,
    audit_path: Path | None = None,
    dry_run: bool = False,
) -> int:
    """Promote one directive. Returns an exit code (0/1/2/3)."""
    reg_path = Path(register_path) if register_path else default_register_path()
    log_path = Path(audit_path) if audit_path else default_audit_path()

    if to_status not in STATUS_ORDER:
        print(f"ERROR: unknown target status {to_status!r} (want one of {STATUS_ORDER})",
              file=sys.stderr)
        return 1
    if not actor or not actor.strip() or any(c.isspace() for c in actor):
        print("ERROR: --actor is required (seat id, e.g. naya2; no whitespace)",
              file=sys.stderr)
        return 1

    try:
        ev_pr, ev_comment = validate_evidence(to_status, evidence_pr, evidence_comment)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        register_bytes = reg_path.read_bytes()
    except OSError as exc:
        print(f"FAIL-CLOSED: cannot read register {reg_path}: {exc}", file=sys.stderr)
        return 2
    try:
        directives = load_register(reg_path)
    except DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2

    try:
        entry = get_directive(directives, directive_id)
    except UnknownDirectiveError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    from_status = entry["status"]
    from_idx, to_idx = STATUS_ORDER.index(from_status), STATUS_ORDER.index(to_status)
    if from_idx == to_idx:
        print(
            f"NO-OP: {directive_id} is already {to_status}; "
            f"no write, no audit line (idempotent)",
            file=sys.stderr,
        )
        return 0
    if to_idx < from_idx:
        print(
            f"ERROR: refusing demotion {directive_id} {from_status} -> {to_status}; "
            f"demotion is a separate reviewed action, never a promotion",
            file=sys.stderr,
        )
        return 1
    if to_idx != from_idx + 1:
        print(
            f"ERROR: refusing skip-level jump {directive_id} "
            f"{from_status} -> {to_status}; promote one step at a time "
            f"({' -> '.join(STATUS_ORDER)})",
            file=sys.stderr,
        )
        return 1

    record = build_audit_record(
        directive_id, from_status, to_status, ev_pr, ev_comment,
        actor.strip(), register_bytes,
    )
    if set(record.keys()) != AUDIT_KEYS:
        # Programming error, never user error.
        print(f"FAIL-CLOSED: audit record keys drifted: {sorted(record.keys())}",
              file=sys.stderr)
        return 2

    new_directives = []
    for e in directives:
        if e["id"] == directive_id:
            e = dict(e)
            e["status"] = to_status
            if ev_pr is not None:
                e["evidence_pr"] = ev_pr
        new_directives.append(e)
    new_text = json.dumps(new_directives, indent=2, ensure_ascii=False) + "\n"

    if dry_run:
        print(json.dumps(record, indent=2))
        print(f"DRY-RUN: would write {reg_path} and append to {log_path}")
        return 0

    try:
        reg_path.write_text(new_text, encoding="utf-8")
    except OSError as exc:
        print(f"FAIL-CLOSED: cannot write register {reg_path}: {exc}", file=sys.stderr)
        return 2
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        # The register moved but the audit did not. Loud, exact recovery.
        print(
            f"ERROR(3): register was updated but the audit append failed: {exc}\n"
            f"RECOVERY: append exactly this line to {log_path}, then commit both files:\n"
            f"{json.dumps(record, ensure_ascii=False)}",
            file=sys.stderr,
        )
        return 3

    print(
        f"promoted {directive_id}: {from_status} -> {to_status} "
        f"(pr={ev_pr}, comment={ev_comment}, actor={actor.strip()})"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Directive register status promotion")
    ap.add_argument("--id", required=True, help="directive id, e.g. D60")
    ap.add_argument("--to", required=True, choices=STATUS_ORDER, help="target status")
    ap.add_argument("--evidence-pr", default=None, help="build/wire PR number")
    ap.add_argument("--evidence-comment", default=None, help="sign-in/sign-out comment id")
    ap.add_argument("--actor", default="", help="seat id, e.g. naya2")
    ap.add_argument("--register", default=None, help="override register JSON path")
    ap.add_argument("--audit-log", default=None, help="override audit log path")
    ap.add_argument("--dry-run", action="store_true", help="validate only, write nothing")
    args = ap.parse_args(argv)
    return promote(
        directive_id=args.id,
        to_status=args.to,
        evidence_pr=args.evidence_pr,
        evidence_comment=args.evidence_comment,
        actor=args.actor,
        register_path=Path(args.register) if args.register else None,
        audit_path=Path(args.audit_log) if args.audit_log else None,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
