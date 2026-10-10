#!/usr/bin/env python3
"""Fail the gate when a PR weakens tests to manufacture a pass.

Prime 2: THE LAW IS THE CODE. "Never weaken tests to make a score pass"
(Operating Protocol, WHAT WE NEVER DO) is enforced here as a machine check
on the PR diff — not as advice.

FAIL (exit 1):
  - the PR ADDS @pytest.mark.skip / @pytest.mark.skipif /
    @unittest.skip / @unittest.skipIf / @unittest.skipUnless without a
    ticket reference (#issue: / ticket / gh- / TODO(#nnn) /
    github.com/.../issues/nnn) in a nearby comment
  - the PR ADDS a bare pytest.skip(...) call inside a test
  - the PR DELETES a test function/class with no replacement

WARN (exit 0): net assertion count decreased in a modified test file.

Zero-false-positive design:
  - Skips are found by AST on the NEW file and diffed against the OLD file:
    a skip that already existed (or traveled with a renamed test) is never
    flagged. Only newly added skips without a ticket reference fail.
  - Deletions are matched by statement coverage across ALL changed test
    files: renames, moves across files, refactors, and test splits are
    never flagged. Only a test whose statements vanish fails.
  - Assertion counting is count-based: refactored assertions with the same
    count never warn.

Usage:
  python3 tools/check_no_test_weakening.py [--base-ref REF] [--head-ref REF]
      [--pathspec PAT]... [--repo PATH]
  Compares merge-base(base-ref, head-ref)..head-ref, parsing the unified
  diff (not grepping files).

Exit 0: no weakening (warnings may print). Exit 1: weakening detected.
Exit 2: usage / git errors.
"""

import ast
import difflib
import fnmatch
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------
# Patterns
# --------------------------------------------------------------------------

# A comment counts as a ticket reference when it matches one of these.
TICKET_RE = re.compile(
    r"#\s*(issue|ticket|gh-|gh:|todo|fixme)\b|github\.com/\S+/(issues|pull)/\d+",
    re.IGNORECASE,
)

# Statement-coverage thresholds for deletion matching.
# single_best: one new test covers this much of the deleted test -> moved/renamed
# union_cov:   all new tests together cover this much -> split/refactored
SINGLE_BEST_OK = 0.6
UNION_COV_OK = 0.85

DEFAULT_PATHSPECS = ("*test*.py",)


# --------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------

@dataclass
class TestDef:
    """One test function or test class found by AST."""
    qname: str            # qualified name: test_x or TestFoo.test_y
    kind: str             # "func" or "class"
    stmts: list          # ast.dump() of each body statement (rename-agnostic)
    lineno: int


@dataclass
class FileChange:
    old_path: str | None
    new_path: str | None
    old_text: str | None   # None when the file is added
    new_text: str | None   # None when the file is deleted


@dataclass
class CheckResult:
    fails: list = field(default_factory=list)
    warns: list = field(default_factory=list)


# --------------------------------------------------------------------------
# Git plumbing
# --------------------------------------------------------------------------

def run_git(repo: str, *args: str) -> str:
    r = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


# --------------------------------------------------------------------------
# Diff parsing
# --------------------------------------------------------------------------

def parse_diff(diff_text: str, pathspecs: tuple) -> list[tuple]:
    """Parse unified diff -> [(old_path, new_path, status)]. status in
    {modified, added, deleted, renamed}."""
    files = []
    old_path = new_path = None
    status = "modified"
    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            if old_path is not None:
                if _matches(old_path, new_path, pathspecs):
                    files.append((old_path, new_path, status))
            parts = line.split(" ")
            old_path = _strip_ab(parts[2])
            new_path = _strip_ab(parts[3])
            status = "modified"
        elif line.startswith("new file"):
            status = "added"
        elif line.startswith("deleted file"):
            status = "deleted"
        elif line.startswith("rename from "):
            old_path = line[len("rename from "):]
            status = "renamed"
        elif line.startswith("rename to "):
            new_path = line[len("rename to "):]
            status = "renamed"
    if old_path is not None and _matches(old_path, new_path, pathspecs):
        files.append((old_path, new_path, status))
    return files


def _strip_ab(p: str) -> str:
    return p[2:] if p[:2] in ("a/", "b/") else p


def _matches(old_path: str, new_path: str, pathspecs: tuple) -> bool:
    target = new_path if new_path != "/dev/null" else old_path
    return any(fnmatch.fnmatch(target, pat) for pat in pathspecs)


# --------------------------------------------------------------------------
# AST analysis
# --------------------------------------------------------------------------

def _body_stmts(node: ast.AST) -> list:
    """Rename-agnostic statement dumps of a function/class body."""
    out = []
    for stmt in getattr(node, "body", []):
        # Skip the docstring: editing docs is not weakening.
        if (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)):
            continue
        out.append(ast.dump(stmt))
    return out


def get_test_defs(source: str) -> dict:
    """Qualified test names -> TestDef, via AST."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    defs = {}

    def add_func(node, prefix):
        name = node.name
        if not name.startswith("test"):
            return
        qname = f"{prefix}.{name}" if prefix else name
        defs[qname] = TestDef(qname, "func", _body_stmts(node), node.lineno)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add_func(node, "")
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            # The class itself, with rename-agnostic method-body statements.
            cls_stmts = []
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and sub.name.startswith("test"):
                    cls_stmts.extend(_body_stmts(sub))
                    add_func(sub, node.name)
            defs[node.name] = TestDef(node.name, "class", cls_stmts, node.lineno)
    return defs


def _decorator_kind(deco: ast.AST) -> str | None:
    """Classify a skip decorator, or None if it isn't one."""
    func = deco.func if isinstance(deco, ast.Call) else deco
    if not isinstance(func, ast.Attribute):
        return None
    attr = func.attr
    val = func.value
    if isinstance(val, ast.Attribute) and val.attr == "mark" \
            and isinstance(val.value, ast.Name) and val.value.id == "pytest" \
            and attr in ("skip", "skipif"):
        return f"pytest.mark.{attr}"
    if isinstance(val, ast.Name) and val.id == "unittest" \
            and attr in ("skip", "skipIf", "skipUnless"):
        return f"unittest.{attr}"
    return None


def get_skips(source: str) -> dict:
    """(qname, skip-kind) -> decorator/call lineno, via AST.

    Only skips attached to tests (or bare pytest.skip() calls inside tests)
    are collected. Module-level skips are out of scope for this check.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}
    skips = {}

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.stack = []  # enclosing test qnames

        def _qname(self):
            return self.stack[-1] if self.stack else None

        def visit_FunctionDef(self, node):
            self._visit_testish(node, "")

        def visit_AsyncFunctionDef(self, node):
            self._visit_testish(node, "")

        def visit_ClassDef(self, node):
            is_test_cls = node.name.startswith("Test")
            if is_test_cls:
                for deco in node.decorator_list:
                    kind = _decorator_kind(deco)
                    if kind:
                        skips[(node.name, kind)] = deco.lineno
                self.stack.append(node.name)
                self.generic_visit(node)
                self.stack.pop()
            else:
                self.generic_visit(node)

        def _visit_testish(self, node, prefix):
            is_test = node.name.startswith("test")
            qname = None
            if is_test:
                # qualified by enclosing test class, if any
                qname = f"{self.stack[-1]}.{node.name}" if self.stack else node.name
                for deco in node.decorator_list:
                    kind = _decorator_kind(deco)
                    if kind:
                        skips[(qname, kind)] = deco.lineno
                self.stack.append(qname)
                self.generic_visit(node)
                self.stack.pop()
            else:
                self.generic_visit(node)

        def visit_Call(self, node):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "skip" \
                    and isinstance(func.value, ast.Name) \
                    and func.value.id == "pytest":
                qname = self._qname()
                if qname:  # only bare pytest.skip() inside a test
                    skips[(qname, "pytest.skip()")] = node.lineno
            self.generic_visit(node)

    Visitor().visit(tree)
    return skips


def ticket_near(lines: list, anchor_lineno: int, def_lineno: int) -> bool:
    """Is there a ticket reference in the comment window around a skip?"""
    start = max(0, anchor_lineno - 3)          # 1-based -> 0-based, minus 2
    end = min(len(lines), def_lineno)          # up to and including def line
    for line in lines[start:end]:
        if TICKET_RE.search(line):
            return True
    return False


def stmt_coverage(del_stmts: list, target: str) -> float:
    if not del_stmts:
        return 1.0
    hit = sum(1 for s in del_stmts if s in target)
    return hit / len(del_stmts)


def count_assertions(source: str) -> int:
    """Count assert statements + unittest-style assert* calls."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 0
    n = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            n += 1
        elif isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and f.attr.lower().startswith("assert"):
                n += 1
            elif isinstance(f, ast.Name) and f.id.lower().startswith("assert"):
                n += 1
    return n


# --------------------------------------------------------------------------
# Per-file analysis
# --------------------------------------------------------------------------

def analyze_file(change: FileChange, all_new_defs: dict) -> CheckResult:
    """all_new_defs: qname -> TestDef across ALL changed test files (for
    cross-file move detection)."""
    res = CheckResult()
    label = change.new_path or change.old_path
    old_text, new_text = change.old_text, change.new_text

    old_defs = get_test_defs(old_text) if old_text is not None else {}
    new_defs = get_test_defs(new_text) if new_text is not None else {}

    # ---- 1. Deleted tests with no replacement ----
    new_blob = "".join(
        "".join(d.stmts) for d in all_new_defs.values()
    )
    deleted = [q for q in old_defs if q not in new_defs]
    failed_classes = set()
    for q in sorted(deleted):
        d = old_defs[q]
        single_best = 0.0
        for nd in all_new_defs.values():
            cov = stmt_coverage(d.stmts, "".join(nd.stmts))
            single_best = max(single_best, cov)
        union_cov = stmt_coverage(d.stmts, new_blob)
        if single_best >= SINGLE_BEST_OK or union_cov >= UNION_COV_OK:
            continue  # moved / renamed / refactored / split
        kind_word = "class" if d.kind == "class" else "test"
        res.fails.append(
            f"{label}: deleted {kind_word} '{q}' with no replacement "
            f"(best match {single_best:.0%}, union {union_cov:.0%})"
        )
        if d.kind == "class":
            failed_classes.add(q)

    # Drop method-level fails whose whole class was already failed (no noise).
    res.fails = [
        f for f in res.fails
        if not any(
            f.startswith(f"{label}: deleted test '{c}.")
            for c in failed_classes
        )
    ]

    # ---- 2. Newly added skips without ticket reference ----
    if new_text is not None:
        new_lines = new_text.splitlines()
        old_skips = get_skips(old_text) if old_text is not None else {}
        new_skips = get_skips(new_text)
        # qname -> body dump for skip-travel detection
        new_bodies = {q: "".join(d.stmts) for q, d in new_defs.items()}
        for (qname, kind), anchor in sorted(new_skips.items()):
            if (qname, kind) in old_skips:
                continue  # pre-existing skip, not added by this PR
            # Did the skip travel with a renamed/moved test?
            traveled = False
            if qname in new_bodies:
                for (oq, okind) in old_skips:
                    if okind != kind or oq not in old_defs:
                        continue
                    if stmt_coverage(old_defs[oq].stmts, new_bodies[qname]) >= 0.6:
                        traveled = True
                        break
            if traveled:
                continue
            def_lineno = new_defs[qname].lineno if qname in new_defs else anchor
            if not ticket_near(new_lines, anchor, def_lineno):
                res.fails.append(
                    f"{label}:{anchor}: added '{kind}' on '{qname}' "
                    f"with no ticket reference (#issue:/ticket/gh-/TODO(#n)/"
                    f"github.com/.../issues/n)"
                )

    # ---- 3. Assertion count decrease -> WARN ----
    if old_text is not None and new_text is not None:
        old_n = count_assertions(old_text)
        new_n = count_assertions(new_text)
        if new_n < old_n:
            res.warns.append(
                f"{label}: net assertion count decreased {old_n} -> {new_n}"
            )

    return res


def analyze_changes(changes: list) -> CheckResult:
    """Analyze a list of FileChange. Importable for tests."""
    # Pass 1: all new test defs (cross-file move detection).
    all_new_defs = {}
    for ch in changes:
        if ch.new_text is not None:
            for q, d in get_test_defs(ch.new_text).items():
                all_new_defs.setdefault(q, d)
    # Pass 2: per-file analysis.
    res = CheckResult()
    for ch in changes:
        r = analyze_file(ch, all_new_defs)
        res.fails.extend(r.fails)
        res.warns.extend(r.warns)
    return res


# --------------------------------------------------------------------------
# Main: git plumbing
# --------------------------------------------------------------------------

def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base-ref", default="origin/main")
    ap.add_argument("--head-ref", default="HEAD")
    ap.add_argument("--pathspec", action="append", default=None)
    ap.add_argument("--repo", default=".")
    args = ap.parse_args(argv)
    pathspecs = tuple(args.pathspec) if args.pathspec else DEFAULT_PATHSPECS

    try:
        mb = run_git(args.repo, "merge-base", args.base_ref, args.head_ref).strip()
        diff_text = run_git(
            args.repo, "diff", "--no-color", "--no-ext-diff",
            mb, args.head_ref, "--", *pathspecs,
        )
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    parsed = parse_diff(diff_text, pathspecs)
    changes = []
    for old_path, new_path, status in parsed:
        old_text = new_text = None
        try:
            if status != "added":
                old_text = run_git(args.repo, "show", f"{mb}:{old_path}")
        except RuntimeError:
            old_text = None
        try:
            if status != "deleted":
                new_text = run_git(args.repo, "show", f"{args.head_ref}:{new_path}")
        except RuntimeError:
            new_text = None
        changes.append(FileChange(old_path, new_path, old_text, new_text))

    res = analyze_changes(changes)
    for w in res.warns:
        print(f"WARN: {w}")
    if res.fails:
        print("FAIL: test weakening detected:")
        for f in res.fails:
            print(f"  {f}")
        print("Never weaken tests to make a score pass. Fix the code, not the test.")
        return 1
    print("OK: no test weakening detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
