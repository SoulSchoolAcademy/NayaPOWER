#!/usr/bin/env python3
"""PR-scoped wrapper for the Brain Index Freshness gate (law BRAIN-INDEX-FRESHNESS).

Why this wrapper exists (Shawn's P0, 2026-10-11): the `brain-index-freshness`
check is destined to become a REQUIRED status check on main. GitHub
documents that a check marked REQUIRED which is skipped by a
paths-filtered workflow stays Pending forever — blocking every PR the
workflow does not run on. So the workflow trigger is UNCONDITIONAL (every
pull_request); the BRAIN-scope decision happens INSIDE the job, cheaply:

  - PR touches nothing under BRAIN/ -> NOT_APPLICABLE, cheap success
    (exit 0; no regen run, no heavy work).
  - PR touches BRAIN/            -> run the full freshness gate on the
    checked-out tree; its verdict decides the job.
  - anything unknown (missing/invalid SHAs, git diff failure, bad record,
    not a NayaPOWER checkout) -> FAIL CLOSED: run the full gate.

Fail-closed: a broken scope detector must never bless a tree it could not
inspect. The wrapper propagates the underlying gate's exact pass/fail and
never invents its own green.

Input record:
    {
      "repo_root": "<absolute path>"   # optional; default = this checkout
      "base_sha":  "<40-hex>",         # optional; default = $BASE_SHA
      "head_sha":  "<40-hex>",         # optional; default = $HEAD_SHA
    }

The `check(record)` contract mirrors the other law checks:
    {"pass": bool, "reasons": [...], "details": {...}}
with details["verdict"] in {"FULL_CHECK", "NOT_APPLICABLE"} so the workflow
(and any auditor) can see which path was taken.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

CHECK_DIR = Path(__file__).resolve().parent
# tools/protocol/checks/__init__.py is the `checks` helper package, so its
# parent (tools/protocol/) goes on sys.path — the same pattern the
# underlying gate uses.
sys.path.insert(0, str(CHECK_DIR.parent))

from checks import emit, fail, load_record, result  # noqa: E402

LAW_ID = "BRAIN-INDEX-FRESHNESS"
VERDICTS = ("FULL_CHECK", "NOT_APPLICABLE")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _resolve_repo_root(record: dict) -> Path:
    """repo_root from the record, else the checkout this file lives in."""
    raw = record.get("repo_root")
    if raw:
        root = Path(raw)
    else:
        # tools/protocol/checks/ -> repo root is three levels up
        root = Path(__file__).resolve().parents[2]
    if not (root / "BRAIN").is_dir() or not (root / ".git").exists():
        raise ValueError(
            f"repo_root is not a NayaPOWER checkout: {root}"
        )
    return root


def _resolve_shas(record: dict) -> tuple[str | None, str | None]:
    """base/head SHAs from the record, falling back to the CI environment."""
    base = record.get("base_sha") or os.environ.get("BASE_SHA")
    head = record.get("head_sha") or os.environ.get("HEAD_SHA")
    base = base.strip() if isinstance(base, str) else None
    head = head.strip() if isinstance(head, str) else None
    if not base or not _SHA_RE.match(base):
        return None, None
    if not head or not _SHA_RE.match(head):
        return None, None
    return base, head


def _changed_paths(repo_root: Path, base: str, head: str) -> list[str]:
    """NUL-separated, rename-free name list of what the PR changed.

    -z avoids quoting ambiguity for unusual filenames; --no-renames makes
    every touched path appear individually. Raises on any git failure so
    the caller can fail closed.
    """
    proc = subprocess.run(
        ["git", "-C", str(repo_root), "diff", "-z", "--no-renames",
         "--name-only", base, head],
        capture_output=True,
        check=True,
    )
    raw = proc.stdout.decode("utf-8", errors="strict")
    return [p for p in raw.split("\x00") if p]


def decide(record: dict) -> dict:
    """Pure scope decision: FULL_CHECK or NOT_APPLICABLE (pass=True)."""
    details: dict = {"law": LAW_ID}
    try:
        root = _resolve_repo_root(record)
    except ValueError as exc:
        details["verdict"] = "FULL_CHECK"
        details["fail_closed"] = "repo_root"
        return fail(
            f"UNKNOWN scope: {exc} — failing closed to the full gate, "
            "which will fail on the unrecognized tree rather than pass it.",
            details,
        )
    details["repo_root"] = str(root)

    base, head = _resolve_shas(record)
    details["base_sha"] = base
    details["head_sha"] = head
    if base is None or head is None:
        details["verdict"] = "FULL_CHECK"
        details["fail_closed"] = "sha"
        return fail(
            "UNKNOWN scope: base/head SHAs missing or not 40-hex "
            "(record base_sha/head_sha or $BASE_SHA/$HEAD_SHA) — failing "
            "closed to the full gate rather than guessing.",
            details,
        )

    try:
        paths = _changed_paths(root, base, head)
    except Exception as exc:
        details["verdict"] = "FULL_CHECK"
        details["fail_closed"] = "git-diff"
        return fail(
            f"UNKNOWN scope: git diff failed ({type(exc).__name__}: {exc}) — "
            "failing closed to the full gate rather than blessing an "
            "uninspected tree.",
            details,
        )

    brain_paths = [p for p in paths if p.startswith("BRAIN/")]
    details["changed_file_count"] = len(paths)
    details["brain_touched_paths"] = brain_paths
    if brain_paths:
        details["verdict"] = "FULL_CHECK"
        return result(
            True,
            [f"PR touches BRAIN/ ({len(brain_paths)} file(s)): "
             "the full freshness gate decides."],
            details,
        )
    details["verdict"] = "NOT_APPLICABLE"
    return result(
        True,
        [f"NOT_APPLICABLE: PR changes {len(paths)} file(s), none under "
         "BRAIN/ — the freshness gate does not apply to this PR."],
        details,
    )


def _load_gate_module():
    """Import the underlying freshness gate by file path (no package
    dependence — the same pattern the gate's own tests use)."""
    gate_path = CHECK_DIR / "brain_index_freshness.py"
    spec = importlib.util.spec_from_file_location(
        "brain_index_freshness", gate_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(record: dict) -> dict:
    """Execute the wrapper: decide, then run the full gate when in scope.

    The full gate's verdict is propagated unchanged — this wrapper never
    invents green. NOT_APPLICABLE never invokes the gate (that is the
    cheap path), and its pass is honest: the gate has nothing to verify
    on a PR that cannot drift the index.
    """
    decision = decide(record)
    if decision["details"].get("verdict") != "FULL_CHECK":
        return decision
    gate = _load_gate_module()
    gate_result = gate.check(
        {"repo_root": decision["details"]["repo_root"]})
    reasons = list(decision["reasons"]) + list(gate_result["reasons"])
    details = dict(decision["details"])
    details.update(gate_result.get("details", {}))
    details["verdict"] = "FULL_CHECK"
    return result(gate_result["pass"], reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="PR-scoped brain-index freshness gate")
    parser.add_argument(
        "--record", default="{}",
        help="JSON record (or @file); base_sha/head_sha default to "
             "$BASE_SHA/$HEAD_SHA")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW_ID}),
                    args.json)
    try:
        return emit(run(record), args.json)
    except Exception as exc:  # nothing may pass silently
        return emit(fail(f"wrapper raised {type(exc).__name__}: {exc} "
                         "— a broken gate fails closed, never open",
                         {"law": LAW_ID, "verdict": "FULL_CHECK"}),
                    args.json)


if __name__ == "__main__":
    sys.exit(main())
