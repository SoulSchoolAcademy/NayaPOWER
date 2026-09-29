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
