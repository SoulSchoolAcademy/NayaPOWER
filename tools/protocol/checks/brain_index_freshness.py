#!/usr/bin/env python3
"""The Brain Index Regen Habit (mechanical gate).

The brain is the product; a silently stale index is silent corruption of the
thing we are proving learns. The habit is not a reminder — it is law, and
law here means code that fails:

    Every BRAIN/ change lands with a matching index regen.

This check runs the canonical regeneration machinery
(tools/regenerate_brain_index.py) in --check mode against the COMMITTED git
tree at HEAD — never the working tree — and fails on drift. It is the
protocol-law wrapper around the same machinery CI runs; the manifest
registers it as law BRAIN-INDEX-FRESHNESS so the habit lives in the
protocol, not in someone's memory.

What it proves:
  1. The index layer (BRAIN/REAL-TREE.json, BRAIN/REAL-TREE.md,
     BRAIN/NAYAPOWER-BRAIN-INDEX.json) matches what regeneration from the
     committed tree would produce, ignoring only the provenance stamps
     (generated_at date, basis-commit SHAs), which record the verification
     event rather than tree-derived data.
  2. Domain file counts sit at or above their ledger floors (the deletion
     ratchet — deletions are never blessed silently).
  3. Every declared pointer in the index layer resolves in the git tree,
     plus a backstop scan for undeclared path-like strings.

What it does NOT prove (said out loud): the semantic sections of
NAYAPOWER-BRAIN-INDEX.json are preserved untouched by the regen, not
verified for correctness — the gate checks the mechanical layer (counts,
blob SHAs, pointers), never the meaning. A wrong-but-consistent index
still passes; that is a different exploit class, caught by review.

Fail-closed: a malformed record, a repo_root that is not a NayaPOWER
checkout, or any git/machinery error fails the check — never silently
checks the wrong tree.

Input record:
    {
      "repo_root": "<absolute path to the NayaPOWER checkout>"  # optional;
          # default = the repo root derived from this file's location
    }

Checks:
  1. The record is a JSON object; repo_root (when given) names a directory
     containing BRAIN/ and a git repo. Anything else fails closed.
  2. The regen check runs against the committed tree. Drift (any BRAIN/
     change without a matching regen) FAILS, naming each drifted item and
     the exact command that fixes it.
  3. Structural corruption (counts below the deletion floor, dangling
     pointers) FAILS as corruption, not drift — the fix is to restore the
     tree (or deliberately lower the floor with a named PR), not to
     regenerate. The regen machinery refuses to bless deletions silently,
     so the gate never advises regenerating over them.

The check verifies compliance; it never grants authority.

Usage:
    python3 tools/protocol/checks/brain_index_freshness.py \
        --record '{"repo_root": "/path/to/NayaPOWER"}' [--json]
    # or, from anywhere inside the checkout:
    python3 tools/protocol/checks/brain_index_freshness.py --record '{}' [--json]
"""

from __future__ import annotations

import argparse
import contextlib
import io
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))            # tools/protocol/checks/ -> helpers
sys.path.insert(0, str(TOOLS_DIR.parent))     # tools/ -> regenerate_brain_index

from checks import emit, fail, load_record, result  # noqa: E402

import regenerate_brain_index as regen  # noqa: E402

LAW_ID = "BRAIN-INDEX-FRESHNESS"
REGEN_FIX_COMMAND = "python3 tools/regenerate_brain_index.py"


def _repo_root(record: dict) -> Path:
    """Resolve the checkout to check. Fail closed on anything that is not one."""
    raw = record.get("repo_root")
    if raw is None:
        root = TOOLS_DIR.parent.parent  # tools/protocol/checks/x.py -> repo root
    elif isinstance(raw, str) and raw.strip():
        root = Path(raw.strip()).expanduser().resolve()
    else:
        raise ValueError("repo_root must be a non-empty path string")
    if not root.is_dir():
        raise ValueError(f"repo_root {root} is not a directory")
    if not (root / "BRAIN").is_dir():
        raise ValueError(f"repo_root {root} has no BRAIN/ directory — "
                         "not a NayaPOWER checkout")
    if not (root / ".git").exists():
        raise ValueError(f"repo_root {root} has no .git — "
                         "the check runs against the committed git tree, "
                         "never a loose directory")
    return root


def _run_regen_check(root: Path) -> tuple[int, str]:
    """Run the regen machinery in --check mode, capturing its output.

    Returns (exit_code, captured_output). exit 0 = fresh, 1 = drift,
    2 = structural/usage error (counts below floor, dangling pointer, git).
    """
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = regen.check(root)
    return code, buf.getvalue()


def _drift_items(output: str) -> list[str]:
    """Extract the named drift items from the regen's DRIFT report."""
    items: list[str] = []
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("- ") or line.startswith(" - "):
            items.append(line.lstrip("- ").strip())
    return items


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {
        "law": LAW_ID,
        # Honest status: the habit is Shawn's standing order (night-shift
        # dispatch 2026-10-11); this encoding is new, not a ratified law.
        "law_status": "ENCODED 2026-10-11 from Shawn's standing brain-index "
                      "habit (night-shift dispatch); not independently ratified",
        "index_files": sorted(regen.RECEIPT_PATHS),
    }

    if not isinstance(record, dict):
        return fail("record is not a JSON object — fail closed, "
                    "never check an unnamed tree", details)

    try:
        root = _repo_root(record)
    except ValueError as exc:
        return fail(f"bad repo_root: {exc}", details)
    details["repo_root"] = str(root)
    reasons.append(f"repo_root resolved to a NayaPOWER checkout: {root}")

    try:
        code, output = _run_regen_check(root)
    except Exception as exc:  # the machinery itself broke — fail, don't pass
        return fail(f"regeneration machinery raised {type(exc).__name__}: {exc} "
                    "— a broken gate fails closed, never open", details)

    if code == 0:
        file_count = None
        for line in output.splitlines():
            if "matches git tree" in line:
                file_count = line.strip()
        reasons.append(
            f"index layer matches the committed git tree — "
            f"{file_count or 'no drift'}"
        )
        reasons.append(
            "domain counts at or above ledger floors (deletion ratchet "
            "holds); every declared pointer resolves; backstop scan clean"
        )
        details["drift_items"] = []
        return result(True, reasons, details)

    if code == 1:
        items = _drift_items(output)
        details["drift_items"] = items
        named = "; ".join(items) if items else "unnamed drift (see regen output)"
        # A floor violation is a DELETION, not drift: the regen machinery
        # refuses to bless it (exit 2), so "just regenerate" is wrong advice.
        if any("below baseline floor" in i for i in items):
            return fail(
                f"STRUCTURAL: BRAIN/ files were deleted below the ledger "
                f"floor — {named}. Do NOT regenerate over this: restore the "
                f"deleted files, or lower BASELINE_DOMAIN_FLOORS in "
                f"tools/regenerate_brain_index.py deliberately with a comment "
                f"naming the PR and the reason. The regen command refuses to "
                f"bless deletions silently.",
                details,
            )
        return fail(
            f"DRIFT: the index layer does not match the committed git tree — "
            f"{named}. A BRAIN/ change landed without a matching index regen. "
            f"Fix: run `{REGEN_FIX_COMMAND}` from the repo root, review the "
            f"diff (counts, blob SHAs, pointers only — never semantic claims), "
            f"commit the regenerated files.",
            details,
        )

    # code == 2 (or anything else): structural corruption, not mere drift.
    items = _drift_items(output)
    details["drift_items"] = items
    named = "; ".join(items) if items else output.strip()[:500]
    return fail(
        f"STRUCTURAL: the brain tree itself is unhealthy — {named}. "
        f"Do NOT regenerate over this: restore the deleted files or fix the "
        f"dangling pointers first (the regen machinery refuses to bless "
        f"deletions silently). Regeneration is the fix for drift, not for "
        f"corruption.",
        details,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Brain index freshness check")
    parser.add_argument("--record", required=True,
                        help="JSON record (or @file); {} checks this checkout")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW_ID}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
