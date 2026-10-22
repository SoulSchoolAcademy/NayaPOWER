#!/usr/bin/env python3
"""Mechanism registry: every gate the system claims, and whether it is wired.

Lesson #1627 (standing): a repair merged with zero live call sites is
MERGED-NOT-ENFORCED — the bytes arrived but the behavior never lived.
Prose inventories rot; this registry is GENERATED from the tree by this
tool, never hand-maintained, and `--check` fails when the committed
registry drifts from the generated one.

A mechanism is one of:
  - a gate/check tool in tools/ (check_*.py, *gate*.py, plus the
    explicit mechanism files below — the post-merge guardian, the door
    checker, the unified gate, the balance gauge, and this pair of
    guards, each picked up automatically once its file exists)
  - a workflow in .github/workflows/

Each record carries: name, kind, owner-file, what it guards (the module
docstring's first line, or the workflow's name), and its CALL SITES —
in-tree references from non-test code/workflow files. Docs are listed
separately as doc_refs and test files as test_refs; neither counts as
wiring — a gate only its own test invokes is not enforced anywhere.
A mechanism with zero call sites is UNWIRED: the registry prints the
cure instead of letting the claim stand. Workflows are wired by their
triggers (`on:`), which are recorded as their call sites.

Modes:
  (default)   print the summary + every UNWIRED mechanism with its cure
  --write     regenerate tools/mechanism-registry.json in place
  --check     exit 1 if the committed registry != the generated one
  --list      print the full generated registry as JSON

Stdlib only, no network. The generated file excludes volatile fields
(generation timestamp / commit) from --check comparison.
"""
import argparse
import ast
import glob
import json
import os
import re
import subprocess
import sys

REGISTRY_REL = "tools/mechanism-registry.json"
SCHEMA = "naya.mechanism-registry/v1"

# Mechanism files that don't match the check_* / *gate* globs. Existence-
# filtered: a file earns its record the moment it lands in the tree.
EXPLICIT_TOOLS = [
    "tools/post_merge_guardian.py",        # PR #2860, the house-fire loop
    "tools/check_door_obligation.py",      # PR #2862, the note-door checker
    "tools/check_unified_pr_paperwork.py",  # PR #2856, the unified gate
    "tools/balance_gauge.py",              # PR #2863, the balance gauge
    "tools/check_tongue_coverage.py",      # this build, tongue guard
    "tools/mechanism_registry.py",         # this tool
]

CODE_EXTS = {".py", ".yml", ".yaml", ".sh", ".toml", ".mjs", ".js"}
DOC_EXTS = {".md", ".json", ".txt"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}


def tool_docstring(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            tree = ast.parse(fh.read())
        doc = ast.get_docstring(tree) or ""
    except Exception:
        doc = ""
    for line in doc.splitlines():
        if line.strip():
            return line.strip()
    return ""


def workflow_name_and_triggers(path):
    name = ""
    triggers = []
    try:
        lines = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()
    except Exception:
        return name, triggers
    in_on = False
    for line in lines:
        if not name and re.match(r"^name:\s*", line):
            name = line.split(":", 1)[1].strip().strip("'\"")
            continue
        if re.match(r"^on:\s*", line):
            in_on = True
            rest = line.split(":", 1)[1].strip()
            if rest:  # inline form: on: [push] / on: push
                triggers.extend(t.strip("[] ") for t in rest.split(",") if t.strip())
            continue
        if in_on:
            m = re.match(r"^  ([A-Za-z_][\w-]*):", line)
            if m:
                triggers.append(m.group(1))
                continue
            if line and not line.startswith(" "):
                in_on = False
    return name, triggers


def enumerate_tools(root):
    found = {}
    for pat in ("tools/check_*.py", "tools/*gate*.py"):
        for path in glob.glob(os.path.join(root, pat)):
            rel = os.path.relpath(path, root)
            base = os.path.basename(rel)
            if base.startswith("test_") or base.endswith("_test.py"):
                continue  # test files are not mechanisms
            found[rel] = path
    for rel in EXPLICIT_TOOLS:
        path = os.path.join(root, rel)
        if os.path.isfile(path):
            found[rel] = path
    return sorted(found.items())


def enumerate_workflows(root):
    out = []
    for path in sorted(glob.glob(os.path.join(root, ".github/workflows/*.yml")) +
                       glob.glob(os.path.join(root, ".github/workflows/*.yaml"))):
        out.append((os.path.relpath(path, root), path))
    return out


def iter_tree_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            yield os.path.join(dirpath, fn)


PY_TOKEN = re.compile(r"([A-Za-z0-9_.\-/]+\.py)\b")
IMPORT_TOKEN = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_]+)", re.M)


def find_call_sites(root, mechanisms):
    """Grep the tree for references to each tool mechanism.

    Single pass per file: one token scan extracts every `*.py` mention
    and every imported module name, then both are matched against the
    needle set. Hits in code files count as call sites; hits in docs
    are doc_refs. The registry tool, the committed registry, the
    mechanism's own file, and its own test file never count — a
    mechanism cannot wire itself by describing itself.
    """
    by_base = {}
    by_module = {}
    for rec in mechanisms:
        if rec["kind"] != "tool":
            continue
        base = os.path.basename(rec["owner_file"])
        by_base[base] = rec["owner_file"]
        if base.endswith(".py"):
            by_module[base[:-3]] = rec["owner_file"]
    site_map = {rec["owner_file"]: {"call_sites": set(), "doc_refs": set(),
                                    "test_refs": set()}
                for rec in mechanisms if rec["kind"] == "tool"}
    for path in iter_tree_files(root):
        rel = os.path.relpath(path, root)
        if rel in (REGISTRY_REL, "tools/mechanism_registry.py"):
            continue
        ext = os.path.splitext(rel)[1].lower()
        if ext not in CODE_EXTS and ext not in DOC_EXTS:
            continue
        try:
            text = open(path, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        mentioned = {os.path.basename(tok) for tok in PY_TOKEN.findall(text)}
        mentioned &= set(by_base)
        imported = set(IMPORT_TOKEN.findall(text)) & set(by_module)
        owners = {by_base[b] for b in mentioned} | {by_module[m] for m in imported}
        base = os.path.basename(rel)
        if base.startswith("test_") or base.endswith("_test.py"):
            bucket = "test_refs"
        elif ext in CODE_EXTS:
            bucket = "call_sites"
        else:
            bucket = "doc_refs"
        for owner in owners:
            if rel == owner:
                continue
            site_map[owner][bucket].add(rel)
    for rec in mechanisms:
        if rec["kind"] != "tool":
            continue
        sites = site_map[rec["owner_file"]]
        rec["call_sites"] = sorted(sites["call_sites"])
        rec["doc_refs"] = sorted(sites["doc_refs"])
        rec["test_refs"] = sorted(sites["test_refs"])
        rec["wired"] = bool(rec["call_sites"])


def build_registry(root):
    mechanisms = []
    for rel, path in enumerate_tools(root):
        base = os.path.basename(rel)
        mechanisms.append({
            "name": base[:-3] if base.endswith(".py") else base,
            "kind": "tool",
            "owner_file": rel,
            "guards": tool_docstring(path) or "(no docstring — undocumented mechanism)",
            "call_sites": [],
            "doc_refs": [],
            "test_refs": [],
            "wired": False,
        })
    for rel, path in enumerate_workflows(root):
        name, triggers = workflow_name_and_triggers(path)
        mechanisms.append({
            "name": name or os.path.basename(rel),
            "kind": "workflow",
            "owner_file": rel,
            "guards": name or "(unnamed workflow)",
            "call_sites": [f"on: {t}" for t in triggers],
            "doc_refs": [],
            "test_refs": [],
            "wired": bool(triggers),
        })
    find_call_sites(root, mechanisms)
    mechanisms.sort(key=lambda r: r["owner_file"])
    unwired = [r["owner_file"] for r in mechanisms if not r["wired"]]
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                                capture_output=True, text=True).stdout.strip() or None
    except Exception:
        commit = None
    return {
        "schema": SCHEMA,
        "generated_by": "tools/mechanism_registry.py",
        "generated_from_commit": commit,
        "summary": {
            "total": len(mechanisms),
            "wired": len(mechanisms) - len(unwired),
            "unwired": len(unwired),
            "unwired_files": unwired,
        },
        "mechanisms": mechanisms,
    }


def comparable(registry):
    """The drift-relevant projection: volatile fields excluded."""
    return {"schema": registry["schema"],
            "summary": registry["summary"],
            "mechanisms": registry["mechanisms"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), help="repo tree root (default: this repo)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="regenerate the committed registry")
    mode.add_argument("--check", action="store_true", help="fail if the committed registry drifted")
    mode.add_argument("--list", action="store_true", help="print the full generated registry as JSON")
    args = ap.parse_args(argv)

    registry = build_registry(args.root)

    if args.list:
        print(json.dumps(registry, indent=2, sort_keys=True))
        return 0

    if args.write:
        out = os.path.join(args.root, REGISTRY_REL)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(registry, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote {REGISTRY_REL}: {registry['summary']['total']} mechanisms, "
              f"{registry['summary']['wired']} wired, {registry['summary']['unwired']} unwired")
        return 0

    if args.check:
        committed_path = os.path.join(args.root, REGISTRY_REL)
        if not os.path.isfile(committed_path):
            print(f"MISSING: {REGISTRY_REL} — CURE: run "
                  f"`python3 tools/mechanism_registry.py --write` and commit "
                  f"the result (owner: mechanism lane)")
            return 1
        committed = json.load(open(committed_path, encoding="utf-8"))
        if comparable(committed) != comparable(registry):
            old = {r["owner_file"]: r for r in committed.get("mechanisms", [])}
            new = {r["owner_file"]: r for r in registry["mechanisms"]}
            for f in sorted(set(new) - set(old)):
                print(f"DRIFT: {f} exists in the tree but not in the registry "
                      f"— CURE: run `python3 tools/mechanism_registry.py --write` "
                      f"and commit (owner: mechanism lane)")
            for f in sorted(set(old) - set(new)):
                print(f"DRIFT: {f} is in the registry but not in the tree "
                      f"— CURE: run `python3 tools/mechanism_registry.py --write` "
                      f"and commit (owner: mechanism lane)")
            for f in sorted(set(old) & set(new)):
                if old[f] != new[f]:
                    print(f"DRIFT: {f} record changed (wiring or guards) "
                          f"— CURE: run `python3 tools/mechanism_registry.py --write` "
                          f"and commit (owner: mechanism lane)")
            return 1
        print(f"mechanism registry current: {registry['summary']['total']} mechanisms, "
              f"{registry['summary']['wired']} wired, {registry['summary']['unwired']} unwired")
        return 0

    s = registry["summary"]
    print(f"mechanism registry: {s['total']} mechanisms · {s['wired']} wired · "
          f"{s['unwired']} unwired")
    for rec in registry["mechanisms"]:
        if not rec["wired"]:
            print(f"UNWIRED: {rec['owner_file']} ({rec['name']}) claims to guard "
                  f"“{rec['guards'][:80]}” but no code or workflow in the tree "
                  f"invokes it — CURE: wire a call site (workflow step or caller) "
                  f"or record the external invocation in the registry notes "
                  f"(owner: mechanism lane)")
    return 1 if s["unwired"] else 0


if __name__ == "__main__":
    sys.exit(main())
