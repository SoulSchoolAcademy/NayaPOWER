#!/usr/bin/env python3
"""brief-compiler.py — Machine 1 of the Ultimate Operating System.

Takes a task spec (JSON) and produces a complete, self-contained brief
(markdown). REFUSES an incomplete brief: if a required field is missing,
or a scope file does not exist on disk, it prints the missing fields and
exits non-zero. No brief without an outcome, a checkpoint path, and the law.

Usage:
  python3 brief-compiler.py --spec task.json --out brief.md
  python3 brief-compiler.py --spec task.json            (prints brief to stdout)

Spec fields (required unless noted):
  title            — short name of the task
  outcome          — done defined FIRST: exact element, exact change, exact
                     measurement, what must not be there
  owner            — the named seat (one owner, one mechanism)
  checkpoint_path  — where progress is written incrementally (the file IS
                     the handoff; a killed seat resumes from it)
  scope_files      — files the seat must read first (must exist on disk)
  report_format    — what the seat returns (path + sha + self-scorecard +
                     DONE + NOT-DONE)
  bullseye         — the bullseye for this area, in one sentence, from his seat
  law_refs         — the law named in the brief: Bullseye, Brand, North Star,
                     the five gates, the three-step verification
  forbidden        — (optional) what the seat must NOT do (file to GitHub,
                     show Shawn, delete, merge, ...)
"""
import argparse
import json
import os
import sys

REQUIRED = [
    "title",
    "outcome",
    "owner",
    "checkpoint_path",
    "scope_files",
    "report_format",
    "bullseye",
    "law_refs",
]

LAW_MINIMUM = ["bullseye", "brand", "north star", "five gates",
               "three-step verification"]


def compile_brief(spec):
    missing = []
    for field in REQUIRED:
        value = spec.get(field)
        if value is None or value == "" or value == []:
            missing.append(field)
    # scope files must exist on disk (harvest, don't invent)
    scope = spec.get("scope_files") or []
    if isinstance(scope, str):
        scope = [scope]
    for path in scope:
        if not os.path.isfile(os.path.expanduser(path)):
            missing.append("scope_file missing on disk: %s" % path)
    # the law must be named, not assumed
    law = (spec.get("law_refs") or "").lower()
    for ref in LAW_MINIMUM:
        if ref not in law:
            missing.append("law_refs must name: %s" % ref)
    return missing


def render_brief(spec):
    lines = []
    lines.append("# BRIEF — %s" % spec["title"])
    lines.append("")
    lines.append("**Owner (one owner, one mechanism):** %s" % spec["owner"])
    lines.append("")
    lines.append("## Outcome — done defined FIRST")
    lines.append("")
    lines.append(spec["outcome"])
    lines.append("")
    lines.append("## Bullseye")
    lines.append("")
    lines.append(spec["bullseye"])
    lines.append("")
    lines.append("## Law")
    lines.append("")
    lines.append(spec["law_refs"])
    lines.append("")
    lines.append("## Read first (harvest, don't invent)")
    lines.append("")
    for path in spec["scope_files"]:
        lines.append("- %s" % path)
    lines.append("")
    lines.append("## Checkpoint — write as you go, or the work does not exist")
    lines.append("")
    lines.append("Progress goes to `%s`, incrementally, section by section." % spec["checkpoint_path"])
    lines.append("A restart must cost minutes, never the task. A killed seat resumes from this file.")
    lines.append("")
    lines.append("## Report back")
    lines.append("")
    lines.append(spec["report_format"])
    lines.append("")
    forbidden = spec.get("forbidden") or []
    if forbidden:
        lines.append("## Forbidden")
        lines.append("")
        for item in forbidden:
            lines.append("- %s" % item)
        lines.append("")
    lines.append("## Gates — before every consequential action")
    lines.append("")
    lines.append("Is it right? Is it what they truly need? Is it mine to do? Is now the time? Can I prove it?")
    lines.append("Any gate no → stop, say why, propose the wise path.")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compile a complete brief or refuse.")
    parser.add_argument("--spec", required=True, help="JSON task spec file")
    parser.add_argument("--out", help="Write the brief to this file (else stdout)")
    args = parser.parse_args()

    try:
        with open(args.spec) as f:
            spec = json.load(f)
    except (OSError, ValueError) as exc:
        print("BRIEF INCOMPLETE: cannot read spec: %s" % exc, file=sys.stderr)
        return 2

    missing = compile_brief(spec)
    if missing:
        print("BRIEF INCOMPLETE — refused. Missing:")
        for item in missing:
            print("  - %s" % item)
        return 1

    brief = render_brief(spec)
    if args.out:
        with open(args.out, "w") as f:
            f.write(brief)
        print("BRIEF COMPLETE: %s" % args.out)
    else:
        print(brief)
    return 0


if __name__ == "__main__":
    sys.exit(main())
