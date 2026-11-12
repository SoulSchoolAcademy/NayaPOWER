#!/usr/bin/env python3
"""Fail closed if newly published Smart Note paths collide on a human-visible SN ID.

Scope of publication is the added/renamed files in base..head, but compare
against the complete head tree; historical unrelated duplicates are reported
only when their identifier is touched. No deletion, renumbering, or mutation.
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict

ROOT = "BRAIN/05-MEMORY/SMART-NOTES/"
ID = re.compile(r"^SN-0*([0-9]+)$", re.I)


def note_id(path):
    if not path.startswith(ROOT) or not path.endswith(".md"):
        return None
    for part in path.split("/"):
        m = ID.fullmatch(part)
        if m:
            return int(m.group(1))
    return None


def check(all_paths, added_paths):
    by_id = defaultdict(set)
    for path in all_paths:
        number = note_id(path)
        if number is not None:
            by_id[number].add(path)
    touched = {note_id(p) for p in added_paths}
    collisions = {n: sorted(paths) for n, paths in by_id.items()
                  if n in touched and len(paths) > 1}
    return collisions


def git(*args):
    return subprocess.check_output(["git", *args], text=True).splitlines()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="base revision of publication")
    ap.add_argument("--head", default="HEAD")
    args = ap.parse_args(argv)
    try:
        all_paths = git("ls-tree", "-r", "--name-only", args.head)
        # --diff-filter=AR includes both new names of renames and additions
        added_paths = git("diff", "--name-only", "--diff-filter=AR",
                          args.base, args.head, "--", ROOT)
        collisions = check(all_paths, added_paths)
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"SN UNIQUE ID GATE: UNKNOWN — {exc}", file=sys.stderr)
        return 2
    if collisions:
        for number, paths in sorted(collisions.items()):
            print(f"DENY SN-{number:04d}: {len(paths)} distinct projection paths on publication head")
            for path in paths:
                print(f"  {path}")
        return 1
    print(f"PASS: no newly introduced Smart Note ID collisions ({len(added_paths)} added paths)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
