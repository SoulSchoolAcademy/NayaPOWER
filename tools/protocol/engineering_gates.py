#!/usr/bin/env python3
"""Elite engineering gates: enforceable standards, not advice.

STATUS: CANDIDATE (proposed 2026-10-08 by Naya 5). Not ratified law.
These gates operationalize the ENGINEERING section of AGENTS.md:
  - "Test the actual seam being changed."
  - "Make the smallest effective change."
  - "Record evidence, not confidence."
  - "Do not create duplicate brains, stores, graphs, pipelines, or authority systems."

Each gate returns PASS/FAIL with specifics. They are heuristics, not proofs:
a gate that passes is not automatically excellent, but a gate that fails has
identified a concrete defect to address or justify.

The five gates:
  1. test_the_seam      — changed code must be executed by tests, not just named
  2. no_dead_code       — no unreachable branches or unused functions in changed files
  3. smallest_change    — diff proportional to fix; large diffs need justification
  4. evidence_not_confidence — PR/commit must link evidence, not assert quality
  5. no_duplicate_systems    — new symbols must not duplicate existing seams

Usage:
    python3 tools/protocol/engineering_gates.py --changed a.py,b.py --tests tests/test_a.py
    python3 tools/protocol/engineering_gates.py --diff-file /tmp/d.diff --pr-body /tmp/body.md
    Returns JSON. Exit 0 = all pass, 1 = any fail.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

LARGE_DIFF_LINES = 500
JUSTIFICATION_MARKERS = ["JUSTIFICATION:", "WHY-LARGE:", "JUSTIFY-LARGE-DIFF:"]

# Evidence markers: patterns that indicate real verification, not assertion.
EVIDENCE_PATTERNS = [
    re.compile(r"https?://\S+"),                          # links to runs/artifacts
    re.compile(r"\b\d+\s*/\s*\d+\s*(tests?\s+)?(pass|green|ok)\b", re.I),  # "11/11 pass"
    re.compile(r"\btests?\s+pass(ed|ing)?\b", re.I),
    re.compile(r"\breceipt\b", re.I),                     # scorecard receipts
    re.compile(r"\bverified\b", re.I),
    re.compile(r"^#{1,3}\s*evidence", re.I | re.M),        # Evidence: section
    re.compile(r"exit\s*code\s*[:=]?\s*0", re.I),
]

# Confidence markers: assertions without evidence. Flagged, not failed alone.
CONFIDENCE_PATTERNS = [
    re.compile(r"\bworks? (perfectly|great|fine|well)\b", re.I),
    re.compile(r"\bfully (tested|verified)\b", re.I),
    re.compile(r"\btrust me\b", re.I),
    re.compile(r"\bobviously correct\b", re.I),
]


def _gate(name: str, passed: bool, details: str, failures: list = None) -> dict:
    return {
        "gate": name,
        "pass": passed,
        "details": details,
        "failures": failures or [],
    }


# ---------------------------------------------------------------- gate 1: seam
def _module_imports_test(test_path: Path, module_stem: str) -> bool:
    """AST check: does the test file actually import the module (execute it)?"""
    try:
        tree = ast.parse(test_path.read_text())
    except (SyntaxError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[-1] == module_stem or alias.name == module_stem:
                    return True
        elif isinstance(node, ast.ImportFrom):
            mod = (node.module or "").split(".")[-1]
            if mod == module_stem:
                return True
    return False


def check_test_the_seam(changed_files: list[str], test_files: list[str]) -> dict:
    """Every changed Python source file must be imported by at least one test.

    Importing executes the module. Merely naming it in a comment does not.
    Non-Python files and test files themselves are skipped.
    """
    failures = []
    checked = 0
    for f in changed_files:
        p = Path(f)
        if p.suffix != ".py":
            continue
        if "test" in p.name.lower() or "/tests/" in str(p):
            continue
        checked += 1
        stem = p.stem
        if not any(_module_imports_test(Path(t), stem) for t in test_files if Path(t).exists()):
            failures.append(f"{f}: no test imports module '{stem}' (not executed by tests)")
    if checked == 0:
        return _gate("test_the_seam", True, "no Python source files changed")
    passed = not failures
    return _gate(
        "test_the_seam", passed,
        f"{checked - len(failures)}/{checked} changed modules imported by tests",
        failures,
    )


# ------------------------------------------------------------ gate 2: dead code
class _DeadCodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defined_funcs: set[str] = set()
        self.called_names: set[str] = set()
        self.dead_branches: list[str] = []
        self.unreachable: list[str] = []

    def visit_FunctionDef(self, node):
        self.defined_funcs.add(node.name)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node):
        func = node.func
        if isinstance(func, ast.Name):
            self.called_names.add(func.id)
        self.generic_visit(node)

    def visit_If(self, node):
        # if False: / while-style constants that never execute
        if isinstance(node.test, ast.Constant) and node.test.value is False:
            self.dead_branches.append(f"line {node.lineno}: 'if False' never executes")
        self.generic_visit(node)

    def visit_Compare(self, node):
        # x == NaN is always False — dead guard (real defect from repo history)
        for op, comp in zip(node.ops, node.comparators):
            if isinstance(op, ast.Eq):
                if (isinstance(comp, ast.Attribute) and comp.attr == "NaN") or \
                   (isinstance(comp, ast.Name) and comp.id == "NaN"):
                    self.dead_branches.append(f"line {node.lineno}: '== NaN' is always False")
        self.generic_visit(node)


def _find_unreachable(tree: ast.AST) -> list[str]:
    """Code after return/raise/break/continue in the same block never runs."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for i, stmt in enumerate(node.body):
                if isinstance(stmt, (ast.Return, ast.Raise)) and i < len(node.body) - 1:
                    found.append(f"line {node.body[i+1].lineno}: unreachable after "
                                 f"{type(stmt).__name__.lower()} at line {stmt.lineno}")
    return found


def check_no_dead_code(changed_files: list[str]) -> dict:
    """No unreachable branches or unused functions in changed Python files."""
    failures = []
    checked = 0
    for f in changed_files:
        p = Path(f)
        if p.suffix != ".py" or not p.exists():
            continue
        if "/tests/" in str(p) or "test" in p.name.lower():
            continue
        checked += 1
        try:
            tree = ast.parse(p.read_text())
        except SyntaxError as e:
            failures.append(f"{f}: syntax error: {e}")
            continue
        v = _DeadCodeVisitor()
        v.visit(tree)
        for d in v.dead_branches:
            failures.append(f"{f}: {d}")
        for u in _find_unreachable(tree):
            failures.append(f"{f}: {u}")
        # Unused functions: defined but never called. Ignore dunder/private helpers
        # and functions likely used as entry points (main, handlers).
        entry = {"main"}
        unused = {fn for fn in v.defined_funcs
                  if fn not in v.called_names
                  and not fn.startswith("_")
                  and fn not in entry}
        for fn in sorted(unused):
            failures.append(f"{f}: function '{fn}' defined but never called")
    if checked == 0:
        return _gate("no_dead_code", True, "no Python source files to check")
    passed = not failures
    return _gate("no_dead_code", passed,
                 f"{checked} files checked, {len(failures)} dead-code findings",
                 failures)


# ------------------------------------------------------- gate 3: smallest change
def check_smallest_change(added: int, removed: int, commit_msg: str = "") -> dict:
    """Diff must be proportional to the fix. Large diffs need explicit justification."""
    total = added + removed
    if total <= LARGE_DIFF_LINES:
        return _gate("smallest_change", True,
                      f"diff {total} lines (added {added}, removed {removed}) within budget")
    justified = any(m in commit_msg for m in JUSTIFICATION_MARKERS)
    if justified:
        return _gate("smallest_change", True,
                      f"diff {total} lines exceeds {LARGE_DIFF_LINES} but justification present")
    return _gate(
        "smallest_change", False,
        f"diff {total} lines exceeds {LARGE_DIFF_LINES} without justification",
        [f"add JUSTIFICATION: to commit message explaining why {total} lines are the smallest effective change"],
    )


# ------------------------------------------------- gate 4: evidence not confidence
def check_evidence_not_confidence(pr_body: str) -> dict:
    """PR/commit description must contain evidence markers, not just confidence."""
    body = pr_body or ""
    evidence_hits = [p.pattern for p in EVIDENCE_PATTERNS if p.search(body)]
    confidence_hits = [p.pattern for p in CONFIDENCE_PATTERNS if p.search(body)]
    failures = []
    if not evidence_hits:
        failures.append("no evidence markers found: link test output, runs, receipts, or verification")
    for c in confidence_hits:
        failures.append(f"confidence assertion without evidence: pattern '{c}'")
    passed = not failures
    return _gate(
        "evidence_not_confidence", passed,
        f"{len(evidence_hits)} evidence markers, {len(confidence_hits)} bare confidence assertions",
        failures,
    )


# ------------------------------------------------- gate 5: no duplicate systems
def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def check_no_duplicate_systems(new_symbols: list[str], search_root: Path = None) -> dict:
    """New function/class/file names must not duplicate existing seams.

    Searches the codebase for similar names. A similarity hit is a prompt to
    check the existing seam first — not an automatic failure of the concept,
    but a failure of the check until the author confirms or reuses.
    """
    root = search_root or ROOT
    # Collect existing top-level function/class names from Python files
    existing: dict[str, str] = {}  # normalized -> "file:line:name"
    for py in root.rglob("*.py"):
        if ".git" in str(py) or "__pycache__" in str(py):
            continue
        try:
            tree = ast.parse(py.read_text())
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                norm = _normalize(node.name)
                if norm and norm not in existing:
                    existing[norm] = f"{py.relative_to(root)}:{node.lineno}:{node.name}"

    failures = []
    for sym in new_symbols:
        norm = _normalize(sym)
        if not norm:
            continue
        # Exact normalized match = likely duplicate
        if norm in existing:
            failures.append(f"'{sym}' duplicates existing {existing[norm]} — reuse or justify")
            continue
        # Fuzzy: high similarity suggests overlapping purpose
        for ename, loc in existing.items():
            if len(norm) > 5 and len(ename) > 5:
                ratio = difflib.SequenceMatcher(None, norm, ename).ratio()
                if ratio > 0.85:
                    failures.append(f"'{sym}' similar to existing {loc} (ratio {ratio:.2f}) — check seam first")
                    break
    passed = not failures
    return _gate(
        "no_duplicate_systems", passed,
        f"{len(new_symbols)} new symbols checked against {len(existing)} existing",
        failures,
    )


# ------------------------------------------------------------------ driver
def run_all(changed=None, tests=None, added=0, removed=0,
            commit_msg="", pr_body="", new_symbols=None) -> dict:
    changed = changed or []
    tests = tests or []
    new_symbols = new_symbols or []
    results = [
        check_test_the_seam(changed, tests),
        check_no_dead_code(changed),
        check_smallest_change(added, removed, commit_msg),
        check_evidence_not_confidence(pr_body),
        check_no_duplicate_systems(new_symbols),
    ]
    return {
        "gates": "engineering_excellence",
        "status": "CANDIDATE — proposed 2026-10-08, not ratified law",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pass": all(r["pass"] for r in results),
        "results": results,
        "failures": [r for r in results if not r["pass"]],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Elite engineering gates (CANDIDATE)")
    parser.add_argument("--changed", default="", help="comma-separated changed files")
    parser.add_argument("--tests", default="", help="comma-separated test files")
    parser.add_argument("--added", type=int, default=0)
    parser.add_argument("--removed", type=int, default=0)
    parser.add_argument("--commit-msg", default="")
    parser.add_argument("--pr-body", default="")
    parser.add_argument("--pr-body-file", default="")
    parser.add_argument("--new-symbols", default="", help="comma-separated new function/class names")
    args = parser.parse_args()

    pr_body = args.pr_body
    if args.pr_body_file:
        pr_body = Path(args.pr_body_file).read_text()

    result = run_all(
        changed=[c for c in args.changed.split(",") if c],
        tests=[t for t in args.tests.split(",") if t],
        added=args.added, removed=args.removed,
        commit_msg=args.commit_msg, pr_body=pr_body,
        new_symbols=[s for s in args.new_symbols.split(",") if s],
    )
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
