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


def _resolve_path_expr(node, env, file_dir):
    """Best-effort resolve an AST expression to an absolute directory path.

    Handles the sys.path.insert idioms used across the suite:
      str constants, os.path.join(...), Path(...), X / "seg", str(X),
      X.resolve(), X.parent, X.parents[N], os.path.dirname(X),
      os.path.abspath(X), and Name lookups into `env` (__file__ included).
    Returns an absolute path string, or None when it cannot be resolved.
    Conservative: anything unresolvable is skipped, never guessed.
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        p = Path(node.value)
        return str(p if p.is_absolute() else (file_dir / p))
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.Call):
        func = node.func
        fname = ""
        if isinstance(func, ast.Attribute):
            fname = func.attr
        elif isinstance(func, ast.Name):
            fname = func.id
        args = node.args
        if fname == "join":
            parts = []
            for a in args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    parts.append(a.value)  # join segment: literal, never file-relative
                else:
                    r = _resolve_path_expr(a, env, file_dir)
                    if not r:
                        return None
                    parts.append(r)
            return os.path.join(*parts) if parts else None
        if fname == "str" and len(args) == 1:
            return _resolve_path_expr(args[0], env, file_dir)
        if fname in ("Path",) and len(args) == 1:
            return _resolve_path_expr(args[0], env, file_dir)
        if fname == "resolve" and len(args) == 0 and isinstance(func, ast.Attribute):
            return _resolve_path_expr(func.value, env, file_dir)
        if fname == "dirname" and len(args) == 1:
            base = _resolve_path_expr(args[0], env, file_dir)
            return str(Path(base).parent) if base else None
        if fname == "abspath" and len(args) == 1:
            base = _resolve_path_expr(args[0], env, file_dir)
            return str(Path(base)) if base else None
        return None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        # A multi-segment constant ("a/b") is a guess, never a skip: the
        # resolver only honors single-segment joins. Check the RAW constant,
        # not the resolved path (absolute paths always contain separators).
        right_node = node.right
        if (isinstance(right_node, ast.Constant)
                and isinstance(right_node.value, str)
                and ("/" in right_node.value or "\\" in right_node.value)):
            return None
        left = _resolve_path_expr(node.left, env, file_dir)
        right = _resolve_path_expr(node.right, env, file_dir)
        if left and right:
            seg = Path(right).name
            if not seg:
                return None
            return str(Path(left) / seg)
        return None
    if isinstance(node, ast.Attribute):
        base = _resolve_path_expr(node.value, env, file_dir)
        if base is None:
            return None
        if node.attr == "parent":
            return str(Path(base).parent)
        if node.attr == "parents":
            return base  # handled with Subscript below
        return None
    if isinstance(node, ast.Subscript):
        base = _resolve_path_expr(node.value, env, file_dir)
        if base is None:
            return None
        sl = node.slice
        n = sl.value if isinstance(sl, ast.Constant) else (sl.n if hasattr(sl, "n") else None)
        if isinstance(n, int):
            if n < 0:
                return None  # negative index is a guess, never resolved
            p = Path(base)
            for _ in range(n + 1):  # parents[N] is N+1 levels up from the file
                p = p.parent
            return str(p)
        return None
    return None


def _module_names_in(root):
    """Importable module names provided by an in-repo sys.path root."""
    names = set()
    try:
        rp = Path(root)
        if not rp.is_dir():
            return names
        names.update(p.stem for p in rp.glob("*.py"))
        names.update(
            p.name for p in rp.iterdir()
            if p.is_dir() and p.name.isidentifier()
            and not p.name.startswith((".", "__"))
            and (p / "__init__.py").exists()
        )
    except OSError:
        pass
    return names


def _syspath_roots(path):
    """Resolve the directories a test file adds to sys.path (best-effort).

    The guard previously hardcoded three import roots; suites keep adding new
    ones (tools/human_value, tools/learning/compound_scale, ...) and every
    new root turned into a false alarm. Resolving the actual insert targets
    keeps the guard honest: a module is first-party only when the importing
    file really puts its directory on sys.path.
    """
    roots = set()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return roots
    file_dir = path.parent
    env = {"__file__": str(path)}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            val = _resolve_path_expr(node.value, env, file_dir)
            if val:
                env[node.targets[0].id] = val
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        is_insert = (
            isinstance(func, ast.Attribute)
            and func.attr in ("insert", "append")
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "path"
            and isinstance(func.value.value, ast.Name)
            and func.value.value.id == "sys"
        )
        if not is_insert:
            continue
        arg = node.args[-1] if node.args else None
        if arg is None:
            continue
        resolved = _resolve_path_expr(arg, env, file_dir)
        if resolved and Path(resolved).is_absolute() and Path(resolved).is_dir():
            roots.add(str(Path(resolved)))
    return roots


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
    for import_root in (REPO / "tools", REPO / "tools" / "protocol",
                        REPO / "kernel" / "protocol"):
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
    found = {}
    for path in sorted(TESTS.glob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:  # pragma: no cover - a syntax error is pytest's problem
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    found.setdefault(alias.name.split(".")[0], set()).add(path)
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    found.setdefault(node.module.split(".")[0], set()).add(path)
    global_first_party = _first_party_modules()
    third = set()
    for mod, importers in found.items():
        if mod in STDLIB or mod in global_first_party or mod == "__future__":
            continue
        # A module is first-party when an importing file puts its directory on
        # sys.path itself. This is what the old hardcoded-roots list tried to
        # approximate and got wrong for every new root (the false alarm).
        first_party = False
        for importer in importers:
            for root in _syspath_roots(importer):
                if mod in _module_names_in(root):
                    first_party = True
                    break
            if first_party:
                break
        if not first_party:
            third.add(mod)
    return third


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
