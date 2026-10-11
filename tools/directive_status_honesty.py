"""Directive status honesty gate — the PR-path enforcer for the status ladder.

Plain words: `tools/directive_status.py` is the honest way to move a directive
up the ladder (NOT_STARTED -> BUILDING -> BUILT_AS_CODE -> ENFORCED), but
nothing forced anyone to use it. A hand-edit to `directive-register.json`
could skip rungs, claim ENFORCED with no live gate, or ship a phantom gate
path — and no operating path would object. This gate objects.

It runs on every PR that touches the register and checks the *diff* between
the PR base and head:

  H1  NOT_STARTED carries no evidence_pr ("no code exists" means no evidence).
  H2  BUILT_AS_CODE / ENFORCED carry a valid evidence_pr (positive PR number).
  H3  ENFORCED carries a gate, and a gate that names a repo path must exist
      in the head tree (phantom gates refused).
  H4  Status movement obeys the ladder: exactly one rung up (no skipping),
      any distance down (a removed gate is honest news). New entries are
      judged by H1-H3 only. Removed entries are refused — directives are
      never deleted from the canon.

Fail-closed: an unloadable register (missing file, bad JSON, wrong shape,
duplicate ids, unknown status) is exit 2, never a silent pass. A missing
base file means the register is new: H1-H3 run, H4 is skipped.

This checker reuses the canonical loader (`tools/directive_register.py`) and
the ladder validators (`tools/directive_status.py`) — it adds the PR-path
enforcement, not a second copy of the rules.

Usage (CI):
    python3 tools/directive_status_honesty.py --base-ref <base-sha> --head-ref <head-sha>

Exit codes: 0 = honest; 1 = honesty violation (each names directive + rule);
2 = fail-closed (register or git state untrustworthy).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import directive_register as reg
from directive_status import LADDER, StatusError, validate_evidence_pr, validate_gate

REGISTER_REL = Path("BRAIN") / "01-GOVERNANCE" / "directive-register.json"
_HIGH_RUNGS = ("BUILT_AS_CODE", "ENFORCED")
_ZERO_SHA = "0" * 40


# ---------------------------------------------------------------------------
# Pure core: base/head register lists -> violation strings (unit-testable)
# ---------------------------------------------------------------------------

def check_invariants(head: list[dict], repo: Path) -> list[str]:
    """Rules H1-H3: every head entry must honestly carry its claimed rung."""
    violations: list[str] = []
    for entry in head:
        did = entry.get("id", "?")
        status = entry.get("status")
        evidence_pr = entry.get("evidence_pr")
        if status == "NOT_STARTED" and evidence_pr is not None:
            violations.append(
                f"{did}: H1 NOT_STARTED must not carry evidence_pr "
                f"(got {evidence_pr!r}) — no code exists, so no evidence exists"
            )
        if status in _HIGH_RUNGS:
            try:
                validate_evidence_pr(evidence_pr)
            except StatusError as exc:
                violations.append(
                    f"{did}: H2 {status} requires a valid evidence_pr — {exc}"
                )
        if status == "ENFORCED":
            gate = entry.get("gate")
            if not gate:
                violations.append(
                    f"{did}: H3 ENFORCED requires a recorded gate — name the live "
                    "mechanism (CI gate, runtime guard, workflow block)"
                )
            else:
                try:
                    validate_gate(gate, repo)
                except StatusError as exc:
                    violations.append(f"{did}: H3 ENFORCED gate invalid — {exc}")
    return violations


def check_movement(base: list[dict], head: list[dict]) -> list[str]:
    """Rule H4: status changes obey the ladder; entries are never removed."""
    violations: list[str] = []
    base_by_id = {e["id"]: e for e in base}
    head_by_id = {e["id"]: e for e in head}
    for did in sorted(set(base_by_id) - set(head_by_id)):
        violations.append(
            f"{did}: H4 directive removed from the register — entries are never "
            "deleted from the canon"
        )
    for did in sorted(set(base_by_id) & set(head_by_id)):
        old = base_by_id[did]["status"]
        new = head_by_id[did]["status"]
        if old == new:
            continue
        oi, ni = LADDER.index(old), LADDER.index(new)
        if ni == oi + 1:
            continue  # honest promotion: exactly one rung
        if ni < oi:
            continue  # honest demotion: any distance down is honest news
        violations.append(
            f"{did}: H4 status {old} -> {new} skips rungs — promotions move "
            "exactly one rung; use the status tool once per rung"
        )
    return violations


def check_registers(
    base: list[dict] | None, head: list[dict], repo: Path
) -> list[str]:
    """Full honesty verdict for a base->head register transition."""
    violations = check_invariants(head, repo)
    if base is not None:
        violations.extend(check_movement(base, head))
    return violations


# ---------------------------------------------------------------------------
# Git plumbing: materialize the register at two refs
# ---------------------------------------------------------------------------

def _git_show(repo: Path, ref: str, rel: Path) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{rel.as_posix()}"],
        capture_output=True,
    )
    return proc.stdout if proc.returncode == 0 else None


def _load_at(repo: Path, ref: str, rel: Path) -> list[dict] | None:
    """Load the register as it exists at `ref`; None if the file is absent."""
    raw = _git_show(repo, ref, rel)
    if raw is None:
        return None
    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False
    ) as tmp:
        tmp.write(raw)
        tmp_path = Path(tmp.name)
    try:
        return reg.load_register(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce directive status honesty on a base->head transition."
    )
    parser.add_argument("--base-ref", required=True,
                        help="base commit SHA (use 40 zeros when the file is new)")
    parser.add_argument("--head-ref", required=True, help="head commit SHA")
    parser.add_argument("--repo", default=None,
                        help="repo checkout (default: derived from this file)")
    parser.add_argument("--register", default=REGISTER_REL.as_posix(),
                        help="register path relative to repo root")
    args = parser.parse_args(argv)

    script = Path(__file__).resolve()
    repo = Path(args.repo).resolve() if args.repo else reg.repo_root(script)
    rel = Path(args.register)

    try:
        head = _load_at(repo, args.head_ref, rel)
    except reg.DirectiveRegisterError as exc:
        print(f"FAIL-CLOSED: head register untrustworthy: {exc}", file=sys.stderr)
        return 2
    if head is None:
        print(
            f"FAIL-CLOSED: register {rel} absent at head {args.head_ref[:12]} — "
            "the canon must exist",
            file=sys.stderr,
        )
        return 2

    base: list[dict] | None = None
    if args.base_ref != _ZERO_SHA:
        try:
            base = _load_at(repo, args.base_ref, rel)
        except reg.DirectiveRegisterError as exc:
            print(
                f"FAIL-CLOSED: base register untrustworthy: {exc}",
                file=sys.stderr,
            )
            return 2
        # base None = register is new in this PR: invariants only, no movement.

    violations = check_registers(base, head, repo)
    if violations:
        print(
            f"STATUS-HONESTY VIOLATION: {len(violations)} problem(s) in "
            f"{rel} ({args.base_ref[:12]} -> {args.head_ref[:12]}):"
        )
        for v in violations:
            print(f"  - {v}")
        return 1
    new_note = " (register is new; movement check skipped)" if base is None else ""
    print(f"STATUS-HONESTY OK: {len(head)} directives, no violations{new_note}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
