#!/usr/bin/env python3
"""Does a staged Smart Note change anything enforceable?

Item 3 of the standing directive: stop generating notes until a claim is enforced. A
note that changes no gate, no test, and no code is tuition we pay twice -- once to write
it, once to discover it changed nothing.

This makes that checkable instead of aspirational. It reports, for each Smart Note staged
on a branch, whether the commit that introduced it also touched an enforcement surface:

  - a test file
  - a gate / CI workflow
  - a tool that gates something
  - a migration or contract

It reports. It does not fail. Reason: a refusal that fires on every legitimate note is a
refusal that gets deleted. The first useful output of this is the RATIO -- how many notes
in a cycle carried enforcement. That number is the honest measure of whether the team is
compounding or accumulating prose, and it belongs to whoever decides policy, not to a
script that cannot see context.

Usage:
  python tools/note_enforcement_check.py [--base main] [--json]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NOTE_MARKERS = ("SMART-NOTE-", "SMART_NOTE_", "IB-SMART-NOTE-")

ENFORCEMENT_PREFIXES = (
    "tests/",
    ".github/workflows/",
    "tools/",
    "supabase/migrations/",
    "kernel/",
    "supabase/functions/",
)

ENFORCEMENT_SUFFIXES = (
    "CONTRACT-V1.md",
    "SPEC-V1.md",
    "-SPEC-V1.md",
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    ).stdout


def is_note_path(path: str) -> bool:
    name = Path(path).name
    return any(m in name for m in NOTE_MARKERS)


def is_enforcement_path(path: str) -> bool:
    norm = path.replace("\\", "/")
    if norm.startswith(ENFORCEMENT_PREFIXES):
        return True
    return norm.endswith(ENFORCEMENT_SUFFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main", help="compare against this ref")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    merge_base = git("merge-base", args.base, "HEAD").strip() or args.base
    raw = git("log", "--name-only", "--pretty=format:@@@%H", f"{merge_base}..HEAD")
    if not raw.strip():
        print(f"no commits between {merge_base} and HEAD", file=sys.stderr)
        return 0

    commits: list[dict] = []
    current = None
    for line in raw.splitlines():
        if line.startswith("@@@"):
            current = {"sha": line[3:].strip(), "files": []}
            commits.append(current)
        elif line.strip() and current is not None:
            current["files"].append(line.strip())

    rows = []
    for c in commits:
        notes = [f for f in c["files"] if is_note_path(f)]
        if not notes:
            continue
        enforcement = [f for f in c["files"] if is_enforcement_path(f)]
        rows.append(
            {
                "sha": c["sha"][:9],
                "notes": notes,
                "enforcement_touched": enforcement,
                "enforced": bool(enforcement),
            }
        )

    total = len(rows)
    enforced = sum(1 for r in rows if r["enforced"])
    pct = (enforced / total * 100.0) if total else 100.0

    if args.json:
        print(json.dumps({
            "base": merge_base,
            "commits_with_notes": total,
            "commits_carrying_enforcement": enforced,
            "pct": round(pct, 1),
            "notes": rows,
        }, indent=2))
        return 0

    print("SMART NOTE ENFORCEMENT CHECK")
    print("=" * 78)
    print("A note that changes no gate, no test, and no code is tuition paid twice.")
    print("=" * 78)
    print(f"commits introducing a note      : {total}")
    print(f"commits carrying enforcement    : {enforced}")
    print(f"enforcement rate                : {pct:.1f}%")
    if rows:
        print("\nPER-COMMIT:")
        for r in rows:
            mark = "ENFORCED" if r["enforced"] else "NOTE ONLY"
            print(f"  {r['sha']}  {mark:<9} {', '.join(Path(n).name for n in r['notes'][:2])}")
            if r["enforced"]:
                print(f"              touched: {', '.join(r['enforcement_touched'][:3])}")
    print("=" * 78)
    print("Reported, not enforced. A gate that fired on every legitimate note would be")
    print("a gate that got deleted. The number is the deliverable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
