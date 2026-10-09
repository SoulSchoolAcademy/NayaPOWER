"""Tests for elite engineering gates (CANDIDATE standards).

Each gate is tested for: true positive (catches the defect) and
true negative (clean code passes). A gate that cannot catch its own
defect in a test is theater, not engineering.
"""

import sys
import tempfile
from pathlib import Path

# Import the gates from this repo (canonical home: kernel/protocol per
# kernel/protocol/SYNTHESIS.md) — never from a machine-local ~/workspace path,
# which does not exist in CI and broke collection there (SN-0575 fix).
_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "kernel" / "protocol"))

from engineering_gates import (
    check_test_the_seam,
    check_no_dead_code,
    check_smallest_change,
    check_evidence_not_confidence,
    check_no_duplicate_systems,
)


def _tmp_py(tmp: Path, name: str, content: str) -> str:
    p = tmp / name
    p.write_text(content)
    return str(p)


# ------------------------------------------------------- gate 1: test the seam
def test_seam_pass_when_test_imports_module(tmp_path):
    src = _tmp_py(tmp_path, "mymod.py", "def foo():\n    return 1\n")
    tst = _tmp_py(tmp_path, "test_mymod.py", "from mymod import foo\ndef test_x():\n    assert foo() == 1\n")
    r = check_test_the_seam([src], [tst])
    assert r["pass"], r["failures"]


def test_seam_fail_when_no_test_imports(tmp_path):
    src = _tmp_py(tmp_path, "orphan.py", "def bar():\n    return 2\n")
    tst = _tmp_py(tmp_path, "test_other.py", "# mentions orphan in a comment only\n")
    r = check_test_the_seam([src], [tst])
    assert not r["pass"], "comment mention is not execution"
    assert any("orphan" in f for f in r["failures"])


def test_seam_skips_non_python(tmp_path):
    r = check_test_the_seam(["README.md", "style.css"], [])
    assert r["pass"]


# ------------------------------------------------------- gate 2: no dead code
def test_deadcode_pass_clean(tmp_path):
    src = _tmp_py(tmp_path, "clean.py",
                  "def used():\n    return 1\n\ndef main():\n    print(used())\n")
    r = check_no_dead_code([src])
    assert r["pass"], r["failures"]


def test_deadcode_fail_unused_function(tmp_path):
    src = _tmp_py(tmp_path, "waste.py",
                  "def never_called():\n    return 99\n\ndef main():\n    print('hi')\n")
    r = check_no_dead_code([src])
    assert not r["pass"]
    assert any("never_called" in f for f in r["failures"])


def test_deadcode_fail_if_false(tmp_path):
    src = _tmp_py(tmp_path, "br.py", "def f():\n    if False:\n        return 1\n    return 2\n")
    r = check_no_dead_code([src])
    assert not r["pass"]
    assert any("if False" in f for f in r["failures"])


def test_deadcode_fail_nan_comparison(tmp_path):
    src = _tmp_py(tmp_path, "nan.py",
                  "def f(x):\n    if x == NaN:\n        return 0\n    return 1\n")
    r = check_no_dead_code([src])
    assert not r["pass"]
    assert any("NaN" in f for f in r["failures"])


def test_deadcode_fail_unreachable(tmp_path):
    src = _tmp_py(tmp_path, "unr.py",
                  "def f():\n    return 1\n    print('never')\n")
    r = check_no_dead_code([src])
    assert not r["pass"]
    assert any("unreachable" in f for f in r["failures"])


# ------------------------------------------------- gate 3: smallest change
def test_small_diff_passes():
    r = check_smallest_change(added=40, removed=10)
    assert r["pass"]


def test_large_diff_with_justification_passes():
    r = check_smallest_change(added=600, removed=100,
                              commit_msg="refactor: split module\n\nJUSTIFICATION: extracting 3 modules, mechanical move")
    assert r["pass"]


def test_large_diff_without_justification_fails():
    r = check_smallest_change(added=600, removed=100, commit_msg="big refactor")
    assert not r["pass"]
    assert any("JUSTIFICATION" in f for f in r["failures"])


# ------------------------------------------- gate 4: evidence not confidence
def test_evidence_pass_with_links_and_counts():
    body = ("## Tests\n11/11 tests pass\n"
            "Run: https://github.com/org/repo/actions/runs/123\n"
            "Receipt: abc123")
    r = check_evidence_not_confidence(body)
    assert r["pass"], r["failures"]


def test_evidence_fail_empty():
    r = check_evidence_not_confidence("Fixed the bug.")
    assert not r["pass"]


def test_evidence_fail_confidence_assertion():
    r = check_evidence_not_confidence("Works perfectly, fully tested, trust me.")
    assert not r["pass"]
    assert len(r["failures"]) >= 2  # no evidence + confidence assertions


# ------------------------------------------- gate 5: no duplicate systems
def test_nodup_pass_unique(tmp_path):
    # Search a tiny isolated root so repo contents don't interfere
    (tmp_path / "a.py").write_text("def alpha_processor():\n    pass\n")
    r = check_no_duplicate_systems(["zeta_transformer"], search_root=tmp_path)
    assert r["pass"], r["failures"]


def test_nodup_fail_exact_duplicate(tmp_path):
    (tmp_path / "a.py").write_text("def alpha_processor():\n    pass\n")
    r = check_no_duplicate_systems(["alpha_processor"], search_root=tmp_path)
    assert not r["pass"]
    assert any("duplicates" in f for f in r["failures"])


def test_nodup_fail_fuzzy_similar(tmp_path):
    (tmp_path / "a.py").write_text("def retrieve_intelligence_blocks():\n    pass\n")
    r = check_no_duplicate_systems(["retrieve_intelligence_block"], search_root=tmp_path)
    assert not r["pass"]
    assert any("similar" in f for f in r["failures"])
