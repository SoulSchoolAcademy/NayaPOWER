#!/usr/bin/env python3
"""Tongue-coverage checker: every substantive work ships in three tongues.

The three-language standard (Shawn, 2026-10-01 — standing): everything
substantive ships as human (`*.human.md` — warm, plain), AI (`*.ai.md` —
exact values and procedures), and machine (`*.machine.json` — structured
schema). Same truth, three tongues. Until now nothing measured whether
the standard actually holds across the canon; works silently shipped in
one tongue and the gap was found by hand, late, or never.

This checker enumerates the substantive works in the canonical roots,
groups each work's tongue instances (case-insensitively — the canon
itself mixes `0021-NAYA-OATH-V1.human.md` with
`0021-naya-oath-v1.machine.json`), and reports every missing tongue and
every unparseable machine tongue. A malformed `.machine.json` is
INVALID, never MISSING — the file exists; machines just can't read it.

In-scope roots (the canon's substantive surface):
  - BRAIN/01-GOVERNANCE/  — governance sets (top-level files only)
  - BRAIN/00-ACTIVATION/  — activation sets (top-level files only)
  - NAYA-ACTIVATION/      — activation kit (top-level files only)
  - HUB/ (root level)     — spec / contract / blueprint / design works
  - repo root             — files named *PROTOCOL*.md

Exemptions are explicit, each with its reason, and are listed in
--list output (never silently skipped):
  - README.md             — an index, not a work
  - *AUDIT* dated files   — point-in-time audit snapshots, not living sets
  - THE-TUNE-IN-TEMPLATE  — a template, instantiated per use

Output contract (Balanced Machine): every defect prints one line
  MISSING: <what> — CURE: <one action> (owner: <lane>)
  INVALID: <what> — CURE: <one action> (owner: <lane>)
`--list` emits the full gap list as JSON — the fix queue as data.
Exit 0 = every in-scope work is triplet-complete and every machine
tongue parses. Exit 1 = defects found. Stdlib only, no network.
"""
import argparse
import json
import os
import re
import sys

TONGUES = ("human", "ai", "machine")

# (relative root, owner lane, filename filter or None for "all works")
def scope_roots():
    return [
        ("BRAIN/01-GOVERNANCE", "governance lane", None),
        ("BRAIN/00-ACTIVATION", "activation lane", None),
        ("NAYA-ACTIVATION", "activation lane", None),
        ("HUB", "hub lane", re.compile(r"(SPEC|CONTRACT|BLUEPRINT|DESIGN|PROJECT-INTELLIGENCE)", re.I)),
        ("", "protocol lane", re.compile(r"PROTOCOL", re.I)),
    ]

EXEMPT = [
    (re.compile(r"^README\.md$", re.I), "index file, not a work"),
    (re.compile(r"AUDIT", re.I), "point-in-time audit snapshot, not a living set"),
    (re.compile(r"THE-TUNE-IN-TEMPLATE", re.I), "template, instantiated per use"),
]


def exempt_reason(filename):
    for pat, reason in EXEMPT:
        if pat.search(filename):
            return reason
    return None


def classify(filename):
    """Return (tongue, stem) for a tongue-instance filename, else None.

    Suffix matching is case-insensitive; the stem keeps its original
    case for display and is lowercased by the caller for grouping.
    A plain `.md` whose stripped stem still contains a dot segment
    (PROJECT-INTELLIGENCE.NAYA.md, .PROOF.md) is a variant sibling of a
    work, not a tongue instance.
    """
    low = filename.lower()
    if low.endswith(".machine.json"):
        return ("machine", filename[: -len(".machine.json")])
    if low.endswith(".ai.md"):
        return ("ai", filename[: -len(".ai.md")])
    if low.endswith(".human.md"):
        return ("human", filename[: -len(".human.md")])
    if low.endswith(".human.pdf"):
        return ("human", filename[: -len(".human.pdf")])
    if low.endswith(".md"):
        stem = filename[: -len(".md")]
        if "." in stem:
            return None  # variant sibling, not a tongue instance
        return ("human", stem)
    return None


def scan_root(root, rel, name_filter):
    """Scan one scope root; return (works, invalid, exempt, siblings).

    works: {stem_lower: {"display": stem, "dir": rel,
                         "tongues": {tongue: filename}}}
    invalid: [{path, error}] for *.machine.json files that don't parse.
    """
    works = {}
    invalid = []
    exempt = []
    siblings = []
    absdir = os.path.join(root, rel) if rel else root
    if not os.path.isdir(absdir):
        return works, invalid, exempt, siblings
    for filename in sorted(os.listdir(absdir)):
        fpath = os.path.join(absdir, filename)
        if not os.path.isfile(fpath):
            continue  # top-level files only; subdirectories are out of scope
        if name_filter and not name_filter.search(filename):
            continue
        reason = exempt_reason(filename)
        if reason:
            exempt.append({"path": os.path.join(rel, filename) if rel else filename,
                           "reason": reason})
            continue
        got = classify(filename)
        if got is None:
            if filename.lower().endswith(".md"):
                siblings.append(os.path.join(rel, filename) if rel else filename)
            continue
        tongue, stem = got
        key = stem.lower()
        work = works.setdefault(key, {"display": stem, "dir": rel, "tongues": {}})
        # Prefer a human/ai file's original case for the display stem.
        if tongue in ("human", "ai"):
            work["display"] = stem
        work["tongues"].setdefault(tongue, filename)
        if tongue == "machine":
            try:
                with open(fpath, "r", encoding="utf-8") as fh:
                    json.load(fh)
            except Exception as exc:  # unreadable machine tongue
                invalid.append({
                    "path": os.path.join(rel, filename) if rel else filename,
                    "error": str(exc)[:120],
                })
    return works, invalid, exempt, siblings


def expected_name(work, tongue):
    stem = work["display"]
    if tongue == "human":
        return f"{stem}.human.md"
    if tongue == "ai":
        return f"{stem}.ai.md"
    return f"{work['display'].lower()}.machine.json"


def audit(root):
    """Full audit of a repo tree. Returns the report dict."""
    all_works = {}
    invalid = []
    exempt = []
    siblings = []
    owners = {}
    for rel, owner, name_filter in scope_roots():
        works, inv, ex, sib = scan_root(root, rel, name_filter)
        for key, work in works.items():
            gkey = f"{rel}/{key}" if rel else key
            all_works[gkey] = work
            owners[gkey] = owner
        invalid.extend({**i, "owner": owner} for i in inv)
        exempt.extend(ex)
        siblings.extend(sib)

    gaps = []
    for gkey in sorted(all_works):
        work = all_works[gkey]
        for tongue in TONGUES:
            if tongue not in work["tongues"]:
                gaps.append({
                    "work": gkey,
                    "dir": work["dir"],
                    "missing_tongue": tongue,
                    "expected_file": expected_name(work, tongue),
                    "owner": owners[gkey],
                })
    return {
        "tool": "tools/check_tongue_coverage.py",
        "works_total": len(all_works),
        "works_complete": sum(
            1 for w in all_works.values() if len(w["tongues"]) == len(TONGUES)),
        "gaps": gaps,
        "invalid": invalid,
        "exempt": exempt,
        "siblings_ignored": siblings,
        "works": {
            gkey: {"dir": w["dir"], "tongues": sorted(w["tongues"])}
            for gkey, w in sorted(all_works.items())
        },
    }


def defect_lines(report):
    lines = []
    for gap in report["gaps"]:
        where = f"{gap['dir']}/{gap['expected_file']}" if gap["dir"] else gap["expected_file"]
        lines.append(
            f"MISSING: {gap['missing_tongue']} tongue for work {gap['work']} "
            f"(expected {where}) — CURE: author the {gap['missing_tongue']} "
            f"tongue from the work's existing tongues (owner: {gap['owner']})")
    for inv in report["invalid"]:
        lines.append(
            f"INVALID: machine tongue {inv['path']} does not parse "
            f"({inv['error']}) — CURE: repair the JSON so machines can "
            f"read it (owner: {inv['owner']})")
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), help="repo tree root (default: this repo)")
    ap.add_argument("--list", action="store_true",
                    help="emit the full gap list as JSON (the fix queue as data)")
    args = ap.parse_args(argv)

    report = audit(args.root)
    defects = defect_lines(report)
    if args.list:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for line in defects:
            print(line)
        print(f"tongue coverage: {report['works_complete']}/{report['works_total']} "
              f"works triplet-complete · {len(report['gaps'])} missing tongues · "
              f"{len(report['invalid'])} invalid machine tongues · "
              f"{len(report['exempt'])} exempt files")
    return 1 if defects else 0


if __name__ == "__main__":
    sys.exit(main())
