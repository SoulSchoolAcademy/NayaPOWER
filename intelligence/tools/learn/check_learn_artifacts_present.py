#!/usr/bin/env python3
"""LEARN artifact presence check (2026-10-13, Naya Alpha).

P-013 mechanization: the wave-32 retention drill found the verb-sense guard
and the EXERCISE practice harness were AUTHORED but never COMMITTED — they
existed only in the goal workspace, so the retention test silently measured
local copies instead of the codebase. This script makes absence loud:
it exits nonzero with a named list of any missing artifact.

Mechanized counterpart of the retention drill's presence requirement:
run it (and test_verb_sense_guard.py) from CI on every PR.

Usage:  python intelligence/tools/learn/check_learn_artifacts_present.py
Exit 0: all artifacts present. Exit 1: at least one missing (fails loud).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# The artifacts the wave-32 drill ran against local bytes. If any of these
# is absent from the repo tree, a "retention" measurement would be measuring
# nothing — and must fail instead of passing silently.
REQUIRED = [
    "exercise.py",              # v1.1 practice-round harness (rubric + groove ledger)
    "violation-bank.json",      # bank of real past violations (drill scenarios)
    "test_verb_sense_guard.py", # 8-check verb-sense guard pinning the P-008 artifact
]


def main() -> int:
    missing = [name for name in REQUIRED if not (HERE / name).is_file()]
    if missing:
        print("LEARN ARTIFACT PRESENCE CHECK: FAIL — "
              f"{len(missing)} of {len(REQUIRED)} artifacts missing from the "
              "repo tree. Retention would be untestable by construction:",
              file=sys.stderr)
        for name in missing:
            print(f"  MISSING: {HERE / name}", file=sys.stderr)
        print("Restore the files before claiming any retention result.",
              file=sys.stderr)
        return 1
    print(f"LEARN ARTIFACT PRESENCE CHECK: PASS — "
          f"all {len(REQUIRED)} artifacts present under {HERE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
