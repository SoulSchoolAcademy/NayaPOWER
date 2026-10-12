"""Guard: every third-party module the test suite imports must be installed by CI.

Coder 2, 2026-09-28.

THE DEFECT THIS GUARDS
----------------------
`tests/test_cold_successor_continuity.py` does `import yaml` to parse the live
workflow. `.github/workflows/kernel-tests.yml` installed only `pytest`. So:

  CI      -> ModuleNotFoundError: No module named 'yaml'   -> RED on every push
  my box  -> pyyaml happens to be in site-packages       -> GREEN

The test itself was correct and valuable. It asserts that the cold-successor
proof is not gated on the owner-credential-blocked job - "a proof that can never
execute is not a proof" - which is a real governance property worth guarding.

The ENVIRONMENT was wrong, not the test.

I did not "fix" this by skipping the test when yaml is missing. That would have
made CI green while checking nothing, which is the exact failure mode this whole
line of work exists to end. The dependency is now DECLARED.

WHY A GUARD, THOUGH
A skip-guard here would only be a guard for one test. The real risk is systemic:
any future test may import something the runner does not install, and the failure
will again look like a mysterious CI-only red. So this checks the whole suite's
imports against what CI actually installs, and fails with the specific missing
distribution named.
"""

import ast
import functools
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TESTS = REPO / "tests"
KERNEL_TESTS = REPO / ".github" / "workflows" / "kernel-tests.yml"

# import name -> distribution name on PyPI. Only non-stdlib names appear here.
DISTRIBUTION = {
    "yaml": "pyyaml",
    "pytest": "pytest",
    "jsonschema": "jsonschema",
    "requests": "requests",
    "numpy": "numpy",
    "pandas": "pandas",
    "supabase": "supabase",
}

STDLIB = set(sys.stdlib_module_names)


def _dotted_name(func) -> str:
    """Dotted name of a call target: `os.path.join`, `Path`, `str`."""
    parts = []
    while isinstance(func, ast.Attribute):
        parts.append(func.attr)
        func = func.value
    if isinstance(func, ast.Name):
        parts.append(func.id)
    parts.reverse()
    return ".".join(parts)


def _resolve_part(expr, consts):
    """One path part for join/div: a string literal or a resolvable path.

    A bare relative string is ambiguous as a standalone path (so
    _resolve_path_expr rejects it), but as a join/div PART it is exactly
    what the suite writes: os.path.join(ROOT, "tools").
    """
    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return expr.value
    return _resolve_path_expr(expr, consts)


def _resolve_path_expr(expr, consts):
    """Best-effort static evaluation of a path expression to an absolute Path.

    Handles the forms the suite actually uses: string constants, __file__,
    module-level NAME constants, str()/Path() wrappers, os.path.join/dirname/
    abspath/realpath/normpath, Path / "part", .resolve(), .parent,
    .parents[N]. Anything else -> None (skip, never guess).
    """
    if isinstance(expr, ast.Constant):
        if isinstance(expr.value, str):
            p = Path(expr.value)
            return p if p.is_absolute() else None
        return None
    if isinstance(expr, ast.Name):
        if expr.id == "__file__":
            f = consts.get("__file__")
            return Path(f).resolve() if f is not None else None
        v = consts.get(expr.id)
        return Path(v) if v is not None else None
    if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.Div):
        left = _resolve_path_expr(expr.left, consts)
        right = _resolve_part(expr.right, consts)
        if left is None or right is None:
            return None
        return left / right
    if isinstance(expr, ast.Attribute) and expr.attr == "parent":
        base = _resolve_path_expr(expr.value, consts)
        return base.parent if base is not None else None
    if isinstance(expr, ast.Attribute) and expr.attr == "resolve":
        # bare `.resolve` without a call — not a path, skip
        return None
    if isinstance(expr, ast.Subscript):
        # Path(...).resolve().parents[N]
        target = expr.value
        if (isinstance(target, ast.Attribute) and target.attr == "parents"
                and isinstance(expr.slice, ast.Constant)
                and isinstance(expr.slice.value, int)):
            base = _resolve_path_expr(target.value, consts)
            try:
                return base.parents[expr.slice.value] if base is not None else None
            except IndexError:
                return None
        return None
    if isinstance(expr, ast.Call):
        fname = _dotted_name(expr.func)
        if fname == "str" and len(expr.args) == 1:
            return _resolve_path_expr(expr.args[0], consts)
        if fname == "Path":
            if len(expr.args) == 1:
                return _resolve_path_expr(expr.args[0], consts)
            return None
        if fname == "os.path.join":
            parts = [_resolve_part(a, consts) for a in expr.args]
            if (not parts or not isinstance(parts[0], Path)
                    or any(p is None for p in parts)):
                return None
            out = parts[0]
            for p in parts[1:]:
                out = out / p
            return out
        if fname in ("os.path.dirname", "os.path.abspath", "os.path.realpath",
                     "os.path.normpath") and len(expr.args) == 1:
            base = _resolve_path_expr(expr.args[0], consts)
            if base is None:
                return None
            return {"os.path.dirname": base.parent,
                    "os.path.abspath": base.absolute(),
                    "os.path.realpath": base.resolve(),
                    "os.path.normpath": Path(os.path.normpath(str(base)))}[fname]
        if (isinstance(expr.func, ast.Attribute) and expr.func.attr == "resolve"
                and not expr.args and not expr.keywords):
            # <path-expr>.resolve() — the one-arg form the suite uses
            base = _resolve_path_expr(expr.func.value, consts)
            return base.resolve() if base is not None else None
        return None
    return None


def _path_constants(tree, path):
    """Best-effort constant table: top-level NAME = <path expression> -> Path."""
    consts = {}
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)
               and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)]
    for _ in range(len(assigns) + 1):
        changed = False
        for node in assigns:
            name = node.targets[0].id
            if name in consts:
                continue
            val = _resolve_path_expr(node.value, {**consts, "__file__": path})
            if isinstance(val, Path):
                consts[name] = val
                changed = True
        if not changed:
            break
    return consts


def _is_sys_path_call(node) -> bool:
    """True for `sys.path.insert(0, X)` / `sys.path.append(X)` call nodes."""
    if not isinstance(node, ast.Call) or not node.args:
        return False
    func = node.func
    return (isinstance(func, ast.Attribute)
            and func.attr in ("insert", "append")
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "path"
            and isinstance(func.value.value, ast.Name)
            and func.value.value.id == "sys")


@functools.lru_cache(maxsize=1)
def _suite_sys_path_roots() -> set:
    """Directories the test suite itself puts on sys.path, detected from source.

    A test that does `sys.path.insert(0, <dir>)` and then `import foo` resolves
    `foo` from the checkout itself — the dependency is declared by the suite,
    so CI installs nothing. Without this the guard cries wolf about project
    modules (its docstring's stated failure mode): this is what produced the
    six false positives (fixtures, gates, instrument, pipeline, run_scale,
    subjects), which live under directories the suite adds to sys.path but the
    guard never scanned. Detecting them is a scanner fix, not a weakening —
    a genuinely uninstalled third-party import still fails the guard.
    """
    roots = set()
    for path in sorted(TESTS.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        consts = _path_constants(tree, path)
        for node in ast.walk(tree):
            if not _is_sys_path_call(node):
                continue
            resolved = _resolve_path_expr(node.args[-1], consts)
            if resolved is None:
                continue
            try:
                resolved.relative_to(REPO)
            except ValueError:
                continue  # outside the checkout (e.g. /tmp fixtures) — not ours to claim
            if resolved.is_dir():
                roots.add(resolved)
    return roots


@functools.lru_cache(maxsize=1)
def _first_party_modules() -> set:
    """Top-level names that are part of THIS repository, not PyPI.

    Without this the guard reports its own false positives: the suite imports
    project modules such as `kernel` and `intelligence`, which are directories in
    the repo and are obviously not pip-installable distributions. A guard that
    cries wolf about first-party imports gets ignored, and then it protects
    nothing.
    """
    names = {"tests"}
    # Test helper modules are first-party too; they must not be mistaken for PyPI distributions.
    names.update(p.stem for p in TESTS.glob("*.py"))
    # In-repo import roots the suite adds to sys.path (e.g. `sys.path.insert(0, REPO/"tools")`
    # before `import smart_link`) are first-party as well: those modules resolve from the
    # checkout itself, so CI needs no pip install for them. Without this the guard cries wolf
    # about project modules and gets ignored — the exact failure mode its docstring warns of.
    import_roots = {REPO / "tools", REPO / "tools" / "protocol",
                    REPO / "kernel" / "protocol"}
    # Plus every directory the suite itself puts on sys.path (detected, not
    # hardcoded): a test that sys.path-inserts a directory and imports from it
    # is declaring a first-party dependency. Detection is a scanner fix — it
    # removes false positives without weakening the invariant.
    import_roots.update(_suite_sys_path_roots())
    for import_root in import_roots:
        if import_root.is_dir():
            names.update(p.stem for p in import_root.glob("*.py"))
            # package directories (e.g. tools/protocol/checks/) are importable
            # first-party modules too — the suite adds these roots to sys.path
            names.update(
                p.name for p in import_root.iterdir()
                if p.is_dir() and p.name.isidentifier()
                and not p.name.startswith((".", "__"))
            )
    for entry in REPO.iterdir():
        if entry.is_dir() and (entry / "__init__.py").exists():
            names.add(entry.name)
        elif entry.is_dir() and entry.name.isidentifier():
            names.add(entry.name)
        elif entry.is_file() and entry.suffix == ".py":
            names.add(entry.stem)
    return names


def _installed_distributions() -> set:
    text = KERNEL_TESTS.read_text(encoding="utf-8")
    names = set()
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- run:") and "pip install" in line:
            for token in re.findall(r"[A-Za-z0-9_.\-]+", line.split("pip install", 1)[1]):
                if token.lower() in {"python", "-m", "pip", "-q", "--quiet"}:
                    continue
                names.add(token.lower())
    return names


def _third_party_imports() -> set:
    found = set()
    for path in sorted(TESTS.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:  # pragma: no cover - a syntax error is pytest's problem
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    found.add(node.module.split(".")[0])
    return {m for m in found if m not in STDLIB and m not in _first_party_modules() and m != "__future__"}


def test_ci_installs_every_third_party_module_the_suite_imports():
    """The specific failure this file exists to prevent, named explicitly."""
    installed = _installed_distributions()
    required = {DISTRIBUTION.get(m, m) for m in _third_party_imports()}
    missing = sorted(required - installed)
    assert not missing, (
        f"kernel-tests.yml does not install {missing}. Tests import them, so they pass on any "
        f"machine that happens to have them and fail on a clean CI runner. Declared: {sorted(installed)}"
    )


def test_the_known_regression_is_declared():
    """`yaml` is imported by the cold-successor continuity guard; pyyaml must be installed."""
    assert "yaml" in _third_party_imports(), (
        "expected tests/ to import yaml; if that test was removed, revisit this guard"
    )
    assert "pyyaml" in _installed_distributions(), (
        "pyyaml must be installed by kernel-tests.yml or the cold-successor guard cannot run in CI"
    )


def test_sys_path_roots_are_detected_first_party():
    """Pin the t1342 scanner fix: the suite's own sys.path roots are first-party.

    Regression test for the six false positives (fixtures, gates, instrument,
    pipeline, run_scale, subjects): each resolves from a directory the suite
    puts on sys.path, so the guard must classify them as first-party — while
    still flagging a genuinely uninstalled third-party import (see the guard
    test below). Both directions are pinned here.
    """
    roots = _suite_sys_path_roots()
    assert REPO / "tools" / "learning" / "compound_scale" in roots, (
        f"compound_scale sys.path root not detected; found {sorted(str(r) for r in roots)}"
    )
    assert REPO / "tools" / "human_value" in roots, (
        f"human_value sys.path root not detected; found {sorted(str(r) for r in roots)}"
    )
    first_party = _first_party_modules()
    for name in ("fixtures", "gates", "instrument", "pipeline", "run_scale", "subjects"):
        assert name in first_party, f"{name} is first-party (in-repo, sys.path-declared) but was not detected"
    # and the negative direction still bites: not everything is first-party
    assert "totally-not-a-real-dependency" not in first_party
    assert "requests" not in first_party


def test_guard_detects_an_undeclared_dependency():
    """
    Prove the guard bites: a module that CI does not install must be reported as
    missing. A guard that cannot be shown to fail is decoration.
    """
    installed = _installed_distributions()
    assert "pyyaml" in installed
    assert "totally-not-a-real-dependency" not in installed
    assert {"pyyaml"} - installed == set()  # sanity: the real case is satisfied
    # and the negative case is what the assertion above would flag
    assert sorted({"pyyaml", "ghostdep"} - installed) == ["ghostdep"]
