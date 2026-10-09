#!/usr/bin/env python3
"""The Base-Lineage Rule (design-gate lane standing rule, 2026-10-09).

"Every repair branch's first proof is its lineage — verify the base, not
just the diff. A branch that forks the wrong ancestor silently discards
prior repairs."

A branch that forks an old ancestor and is then merged, rebased, or
squash-pushed onto the live line can silently drop the repairs that landed
in between. This check verifies the lineage BEFORE the diff:

  1. F = merge-base(branch_tip, live_line) must exist — no common
     ancestor means the lineage is unverifiable, and unverifiable fails
     closed.
  2. If a claimed_base is declared, it must EXACTLY equal F. A claimed
     base that is not the true fork point is a dishonest lineage claim.
  3. Every required prior-round marker must exist in F's tree AND in the
     branch tip's tree.
       - absent at F  -> "forked the wrong ancestor": the fork point
         predates repairs the work claims to build on. Rebase onto the
         live line first.
       - present at F, absent at tip -> "silent discard": a prior repair
         was dropped between base and tip.

Only read-only git commands are used (rev-parse, merge-base, ls-tree):
this check verifies lineage; it never mutates the repo and never grants
authority.

Record:
    {
      "branch_tip": "<sha>",
      "live_line": "origin/main",          # optional, default
      "repo": "/path/to/repo",             # optional, derived if omitted
      "required_markers": [                # paths of prior-round markers
        "tools/protocol/checks/two_layer.py"
      ],
      "claimed_base": "<sha>"              # optional; must equal the true fork point
    }

HONEST BOUND (what this check provably does NOT do):
  - It proves the LINEAGE is honest and the prior markers are PRESENT —
    not that the repairs they mark are correct, complete, or current.
  - It proves the fork point is what was claimed, not that the fork point
    was the wisest one. A branch honestly forked from a stale ancestor
    passes shape but must still rebase before building on newer repairs.
  - Marker presence is tree presence, not semantic presence: a path that
    exists but was gutted passes this check.

Usage:
    python3 tools/protocol/checks/base_lineage.py \\
        --record '{"branch_tip": "<sha>", "required_markers": [...]}' [--json]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402
from checks.shape_closed import validate_shape  # noqa: E402

LAW_ID = "BASE-LINEAGE-LAW"
DEFAULT_LIVE_LINE = "origin/main"


def _git(repo: str, *args: str) -> tuple[bool, str]:
    """Run a read-only git command. Returns (ok, stdout-or-error)."""
    try:
        proc = subprocess.run(
            ["git", "-C", repo, *args],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"git unavailable: {e}"
    if proc.returncode != 0:
        return False, (proc.stderr.strip() or proc.stdout.strip())[:200]
    return True, proc.stdout.strip()


def _default_repo() -> str:
    """Walk up from this file until a .git (or gitdir worktree file) is found."""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / ".git").exists():
            return str(parent)
    return str(here.parents[3])


def _resolve(repo: str, ref: str) -> tuple[bool, str]:
    ok, out = _git(repo, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    return ok, out


def _tree_has(repo: str, commit: str, path: str) -> bool:
    ok, out = _git(repo, "ls-tree", commit, "--", path)
    return ok and bool(out.strip())


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": LAW_ID, "law_status": "RATIFIED"}
    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    ok, shape_reasons = validate_shape(
        record,
        {
            "required": ["branch_tip", "required_markers"],
            "types": {
                "branch_tip": "str",
                "live_line": "str",
                "repo": "str",
                "claimed_base": "str",
                "required_markers": "list",
            },
            "non_empty": ["branch_tip", "required_markers"],
        },
    )
    if not ok:
        return fail(
            "shape failure: " + shape_reasons[0]
            + " — the first proof is the lineage; an unshaped claim fails closed",
            details,
        )
    reasons.extend(shape_reasons)

    branch_tip = str(record["branch_tip"]).strip()
    live_line = str(record.get("live_line") or DEFAULT_LIVE_LINE).strip()
    repo = str(record.get("repo") or _default_repo()).strip()
    markers = [str(m).strip() for m in record["required_markers"]]
    claimed_base = record.get("claimed_base")
    details["repo"] = repo
    details["live_line"] = live_line

    # Resolve the tip and the live line. Unresolvable refs fail closed.
    ok, tip_sha = _resolve(repo, branch_tip)
    if not ok:
        return fail(
            f"branch_tip {branch_tip!r} does not resolve in {repo} — "
            "cannot verify the base of an unresolvable tip",
            details,
        )
    details["branch_tip"] = tip_sha

    ok, live_sha = _resolve(repo, live_line)
    if not ok:
        return fail(
            f"live_line {live_line!r} does not resolve in {repo} — "
            "the live line is the anchor; without it there is no lineage",
            details,
        )
    details["live_line_sha"] = live_sha

    # The true fork point: merge-base of the tip and the live line.
    ok, fork_point = _git(repo, "merge-base", tip_sha, live_sha)
    if not ok:
        return fail(
            f"no common ancestor between branch tip {tip_sha[:12]} and "
            f"live line {live_line} ({live_sha[:12]}) — lineage is "
            "unverifiable, and unverifiable fails closed",
            details,
        )
    details["fork_point"] = fork_point
    reasons.append(f"true fork point resolved: {fork_point[:12]}")

    # Honest base: a declared claimed_base must BE the fork point.
    if claimed_base is not None:
        ok, claimed_sha = _resolve(repo, str(claimed_base).strip())
        if not ok:
            return fail(
                f"claimed_base {claimed_base!r} does not resolve — "
                "a lineage claim that cannot be resolved is not a lineage",
                details,
            )
        if claimed_sha != fork_point:
            return fail(
                f"claimed_base {claimed_sha[:12]} is not the true fork point "
                f"{fork_point[:12]} — verify the BASE, not just the diff; "
                "a branch that misstates its ancestor misstates its lineage",
                details,
            )
        reasons.append("claimed_base equals the true fork point")

    # Marker lineage: every prior-round marker must exist at the fork
    # point AND at the tip.
    for marker in markers:
        at_base = _tree_has(repo, fork_point, marker)
        at_tip = _tree_has(repo, tip_sha, marker)
        if not at_base:
            return fail(
                f"marker {marker!r} is absent at fork point "
                f"{fork_point[:12]} — the branch forked the wrong ancestor: "
                "its fork point predates a prior repair it claims to build "
                "on. Rebase onto the live line first.",
                details,
            )
        if not at_tip:
            return fail(
                f"marker {marker!r} is present at fork point "
                f"{fork_point[:12]} but ABSENT from branch tip "
                f"{tip_sha[:12]} — a prior repair was silently discarded "
                "between base and tip",
                details,
            )
    reasons.append(
        f"all {len(markers)} prior-round marker(s) present at fork point "
        "and at tip — no repair silently discarded"
    )

    reasons.append(
        f"Base-Lineage Rule honored: tip {tip_sha[:12]} honestly forks "
        f"{live_line} at {fork_point[:12]}"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Base-Lineage Rule check")
    parser.add_argument("--record", required=True,
                        help="JSON lineage record (or @file)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW_ID}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
