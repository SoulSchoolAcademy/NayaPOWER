"""Directive status promotion — the honest accounting mechanism for the register.

The promotion ladder (strictly ordered):
    NOT_STARTED -> BUILDING -> BUILT_AS_CODE -> ENFORCED

Rung meanings (standing law: BUILT-AS-CODE requires wired enforcement):
  - NOT_STARTED:   no code exists for this directive.
  - BUILDING:      a lane is actively building it in a numbered PR (draft counts).
  - BUILT_AS_CODE: code exists and is tested, but no live mechanism enforces it yet.
  - ENFORCED:      a live mechanism (CI gate, runtime guard, workflow block) on an
                   operating path blocks a real violation. Proven, not claimed.

Rules (fail-closed — the whole point of this tool):
  - Promotions move exactly ONE rung forward. No skipping: you cannot claim
    ENFORCED without passing through BUILT_AS_CODE. The ladder is the receipt.
  - Every promotion requires --evidence-pr: the PR that did the work (positive int).
    No PR, no promotion — a branch is a claim, a merged PR number is evidence.
    NEVER promote on unmerged PRs: branch state is not production truth.
  - Promotion to ENFORCED additionally requires --gate: the live enforcement
    mechanism. If it names a repo path, that path must exist at promotion time.
  - Demotions may drop any number of rungs (a removed gate is honest news) but
    require --reason. Demoting to NOT_STARTED clears evidence_pr — the evidence
    belonged to a state that no longer holds.
  - Unknown directive id, malformed id, unknown target status, corrupt or missing
    register -> error, nothing is written. There are no defaults here by design.

Writes are atomic (temp file + os.replace) and canonical (indent=2,
ensure_ascii=True, no trailing newline — the register's on-disk format), so a
promotion never reformats unrelated entries.

CLI:
    python3 tools/directive_status.py promote D26 --to BUILDING --evidence-pr 2228
    python3 tools/directive_status.py promote D32 --to ENFORCED --evidence-pr 2224 \\
        --gate .github/workflows/d32-doc-scan.yml
    python3 tools/directive_status.py demote D32 --to BUILT_AS_CODE --reason "gate removed in #2300"
    python3 tools/directive_status.py show D26
    python3 tools/directive_status.py ladder

Exit codes: 0 = done (receipt JSON on stdout); 1 = usage/validation error;
2 = register untrustworthy (fail-closed, mirrors directive_register_sync.py).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import directive_register as reg

LADDER = ("NOT_STARTED", "BUILDING", "BUILT_AS_CODE", "ENFORCED")

# Statuses that carry build evidence. Dropping below BUILT_AS_CODE keeps the
# evidence_pr (the code existed); dropping to NOT_STARTED clears it.
_EVIDENCE_KEPT_FROM = {"BUILDING", "BUILT_AS_CODE", "ENFORCED"}


class StatusError(Exception):
    """A promotion/demotion request that the honesty rules refuse."""


def next_rung(status: str) -> str | None:
    """The single rung a promotion from `status` may target, or None at the top."""
    idx = LADDER.index(status)
    return LADDER[idx + 1] if idx + 1 < len(LADDER) else None


def validate_evidence_pr(value: object) -> int:
    """Evidence must be a real PR number: a positive integer. No zero, no negatives."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise StatusError(f"--evidence-pr must be a positive PR number, got {value!r}")
    return value


def validate_gate(gate: str, repo: Path) -> str:
    """A gate must be named. If it looks like a repo path, it must exist.

    Named non-path gates (e.g. 'branch protection rule') are accepted as names —
    the reviewer judges whether the mechanism is real; the tool only refuses
    phantom paths.
    """
    gate = (gate or "").strip()
    if not gate:
        raise StatusError("--gate is required for promotion to ENFORCED: name the live mechanism")
    if "/" in gate:
        candidate = (repo / gate).resolve()
        repo_resolved = repo.resolve()
        if repo_resolved not in candidate.parents and candidate != repo_resolved:
            raise StatusError(f"--gate path escapes the repo: {gate!r}")
        if not candidate.exists():
            raise StatusError(f"--gate path does not exist in this checkout: {gate!r}")
    return gate


def promote_entry(entry: dict, to_status: str, evidence_pr: int, gate: str | None = None) -> dict:
    """Move one entry exactly one rung forward, with evidence. Returns the entry."""
    did = entry["id"]
    if to_status not in LADDER:
        raise StatusError(f"Unknown target status {to_status!r}; the ladder is {' -> '.join(LADDER)}")
    expected = next_rung(entry["status"])
    if expected is None:
        raise StatusError(f"{did} is already ENFORCED — the top of the ladder; nothing to promote to")
    if to_status != expected:
        raise StatusError(
            f"{did}: promotions move exactly one rung ({entry['status']} -> {expected}); "
            f"requested {to_status}. No skipping rungs."
        )
    validate_evidence_pr(evidence_pr)
    if to_status == "ENFORCED":
        if gate is None:
            raise StatusError(
                f"{did}: promotion to ENFORCED requires --gate — name the live mechanism "
                "(CI gate, runtime guard, workflow block) that blocks a real violation"
            )
    entry["status"] = to_status
    entry["evidence_pr"] = evidence_pr
    return entry


def demote_entry(entry: dict, to_status: str, reason: str) -> dict:
    """Move one entry any distance down the ladder, with a recorded reason."""
    did = entry["id"]
    if to_status not in LADDER:
        raise StatusError(f"Unknown target status {to_status!r}; the ladder is {' -> '.join(LADDER)}")
    reason = (reason or "").strip()
    if not reason:
        raise StatusError(f"{did}: demotion requires --reason — honest accounting goes both ways")
    if LADDER.index(to_status) >= LADDER.index(entry["status"]):
        raise StatusError(
            f"{did}: demote moves DOWN the ladder from {entry['status']}; "
            f"use 'promote' for {to_status}"
        )
    entry["status"] = to_status
    if to_status not in _EVIDENCE_KEPT_FROM:
        entry["evidence_pr"] = None
    return entry


def save_register(register_path: Path, directives: list[dict]) -> None:
    """Atomically rewrite the register in canonical format.

    Canonical = indent=2, ensure_ascii=True, no trailing newline — the format the
    register ships in. On canonical input, untouched entries stay byte-identical.
    """
    text = json.dumps(directives, indent=2, ensure_ascii=True)
    register_path = Path(register_path)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(register_path.parent), prefix=register_path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(tmp_name, register_path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def receipt(action: str, directive_id: str, from_status: str, to_status: str,
            evidence_pr: int | None, gate: str | None, reason: str | None,
            note: str | None, register_path: Path) -> dict:
    return {
        "tool": "directive_status",
        "action": action,
        "directive_id": directive_id,
        "from": from_status,
        "to": to_status,
        "evidence_pr": evidence_pr,
        "gate": gate,
        "reason": reason,
        "note": note,
        "register": str(register_path),
        "at": _utc_now(),
    }


def resolve_register_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    return reg.default_register_path()


def cmd_promote(args: argparse.Namespace) -> int:
    register_path = resolve_register_path(args.register)
    try:
        directives = reg.load_register(register_path)
    except reg.DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    try:
        reg.directive_number(args.directive_id)
        entry = reg.get_directive(directives, args.directive_id)
        from_status = entry["status"]
        if args.to == "ENFORCED":
            try:
                repo = reg.repo_root(register_path.resolve())
            except reg.DirectiveRegisterError as exc:
                print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
                return 2
            gate = validate_gate(args.gate, repo)
        else:
            gate = None
        promote_entry(entry, args.to, args.evidence_pr, gate)
        save_register(register_path, directives)
    except reg.DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    except StatusError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt("promote", args.directive_id, from_status, entry["status"],
                             entry["evidence_pr"], gate,
                             None, args.note, register_path)))
    return 0


def cmd_demote(args: argparse.Namespace) -> int:
    register_path = resolve_register_path(args.register)
    try:
        directives = reg.load_register(register_path)
    except reg.DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    try:
        reg.directive_number(args.directive_id)
        entry = reg.get_directive(directives, args.directive_id)
        from_status = entry["status"]
        demote_entry(entry, args.to, args.reason)
        save_register(register_path, directives)
    except reg.DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    except StatusError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt("demote", args.directive_id, from_status, entry["status"],
                             entry["evidence_pr"], None,
                             args.reason, args.note, register_path)))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    register_path = resolve_register_path(args.register)
    try:
        directives = reg.load_register(register_path)
        reg.directive_number(args.directive_id)
        entry = reg.get_directive(directives, args.directive_id)
    except reg.DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(entry, indent=2))
    return 0


def cmd_ladder(_args: argparse.Namespace) -> int:
    print(" -> ".join(LADDER))
    print()
    print("NOT_STARTED   no code exists")
    print("BUILDING      lane actively building in a numbered PR (draft counts); --evidence-pr required")
    print("BUILT_AS_CODE code exists and is tested, no live enforcement yet; --evidence-pr required")
    print("ENFORCED      a live mechanism on an operating path blocks a real violation;")
    print("              --evidence-pr AND --gate required (a repo path must exist)")
    print()
    print("Promotions move exactly one rung. Demotions need --reason.")
    print("Never promote on unmerged PRs: branch state is not production truth.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Honest status promotion for the directive register."
    )
    parser.add_argument("--register", default=None,
                        help="Path to directive-register.json (default: repo BRAIN/01-GOVERNANCE/)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("promote", help="Move one directive exactly one rung up the ladder")
    p.add_argument("directive_id", help="e.g. D26")
    p.add_argument("--to", required=True, help="Target rung (must be the next one)")
    p.add_argument("--evidence-pr", required=True, type=int, help="PR that did the work")
    p.add_argument("--gate", default=None, help="Live enforcement mechanism (required for ENFORCED)")
    p.add_argument("--note", default=None, help="Free-text note, recorded in the receipt only")
    p.set_defaults(func=cmd_promote)

    d = sub.add_parser("demote", help="Move one directive down the ladder with a reason")
    d.add_argument("directive_id", help="e.g. D32")
    d.add_argument("--to", required=True, help="Lower rung")
    d.add_argument("--reason", required=True, help="Why the status is dropping")
    d.add_argument("--note", default=None, help="Free-text note, recorded in the receipt only")
    d.set_defaults(func=cmd_demote)

    s = sub.add_parser("show", help="Print one directive's register entry")
    s.add_argument("directive_id", help="e.g. D26")
    s.set_defaults(func=cmd_show)

    l = sub.add_parser("ladder", help="Print the promotion ladder and its rules")
    l.set_defaults(func=cmd_ladder)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except BrokenPipeError:
        return 0


if __name__ == "__main__":
    sys.exit(main())
