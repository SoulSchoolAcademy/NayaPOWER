"""Tests for tools/check_no_test_weakening.py.

Planted weakening cases MUST be caught (exit 1 / fails non-empty).
Legitimate refactors MUST pass with zero false positives.
"""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_no_test_weakening import (  # noqa: E402
    FileChange,
    analyze_changes,
)


def check(old: dict, new: dict):
    """old/new: {path: source} dicts. None source = file absent on that side."""
    paths = set(old) | set(new)
    changes = [
        FileChange(p, p, old.get(p), new.get(p))
        for p in sorted(paths)
    ]
    return analyze_changes(changes)


BASE_TEST = '''\
import pytest


def test_alpha():
    assert 1 + 1 == 2
    assert 2 + 2 == 4


def test_beta():
    assert "x".upper() == "X"


class TestGamma:
    def test_one(self):
        assert True

    def test_two(self):
        assert False is False
'''


# --------------------------------------------------------------------------
# Must catch: planted weakening
# --------------------------------------------------------------------------

def test_added_pytest_mark_skip_fails():
    new = BASE_TEST.replace(
        "def test_beta():",
        "@pytest.mark.skip\ndef test_beta():",
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails, "added @pytest.mark.skip must fail"
    assert any("pytest.mark.skip" in f for f in res.fails)


def test_added_pytest_mark_skipif_no_ticket_fails():
    new = BASE_TEST.replace(
        "def test_beta():",
        '@pytest.mark.skipif(True, reason="flaky")\ndef test_beta():',
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails, "added @pytest.mark.skipif without ticket must fail"


def test_added_unittest_skip_fails():
    new = "import unittest\n" + BASE_TEST.replace(
        "def test_beta():",
        "@unittest.skip\ndef test_beta():",
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails, "added @unittest.skip must fail"


def test_added_bare_pytest_skip_call_fails():
    new = BASE_TEST.replace(
        '    assert "x".upper() == "X"',
        '    pytest.skip("giving up")\n    assert "x".upper() == "X"',
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails, "added bare pytest.skip() must fail"


def test_deleted_test_function_fails():
    new = BASE_TEST.replace(
        '''def test_beta():
    assert "x".upper() == "X"


''',
        "",
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails, "deleted test with no replacement must fail"
    assert any("test_beta" in f for f in res.fails)


def test_deleted_test_class_fails():
    new = BASE_TEST.split("class TestGamma:")[0]
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails, "deleted test class must fail"
    assert any("TestGamma" in f for f in res.fails)
    # No noisy per-method duplicates for the deleted class.
    assert not any("TestGamma.test_" in f for f in res.fails)


def test_deleted_test_file_fails():
    res = check({"t.py": BASE_TEST}, {"t.py": None})
    assert res.fails, "deleted test file must fail"
    assert len(res.fails) >= 3  # test_alpha, test_beta, TestGamma


def test_new_file_with_unticketed_skip_fails():
    src = 'import pytest\n\n\n@pytest.mark.skip\ndef test_new():\n    assert True\n'
    res = check({}, {"new_test.py": src})
    assert res.fails, "new file with unticketed skip must fail"


# --------------------------------------------------------------------------
# Must pass: legitimate patterns, zero false positives
# --------------------------------------------------------------------------

def test_moved_test_same_file_ok():
    # Rename with identical body.
    new = BASE_TEST.replace("def test_beta():", "def test_beta_renamed():")
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == [], f"rename must not fail: {res.fails}"


def test_moved_test_other_file_ok():
    beta = 'def test_beta():\n    assert "x".upper() == "X"\n'
    new_a = BASE_TEST.replace(beta, "")
    new_b = "import pytest\n\n\n" + beta
    res = check(
        {"a_test.py": BASE_TEST},
        {"a_test.py": new_a, "b_test.py": new_b},
    )
    assert res.fails == [], f"cross-file move must not fail: {res.fails}"


def test_refactored_assertions_same_count_ok():
    new = BASE_TEST.replace("assert 1 + 1 == 2", "assert (1 + 1) == (2)")
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == []
    assert res.warns == [], f"same-count refactor must not warn: {res.warns}"


def test_skip_with_issue_reference_ok():
    new = BASE_TEST.replace(
        "def test_beta():",
        "#issue: 1234\n@pytest.mark.skip\ndef test_beta():",
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == [], f"ticketed skip must pass: {res.fails}"


def test_skip_with_github_url_ok():
    new = BASE_TEST.replace(
        "def test_beta():",
        "# https://github.com/org/repo/issues/42\n"
        "@pytest.mark.skipif(True, reason='x')\ndef test_beta():",
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == [], f"URL-ticketed skipif must pass: {res.fails}"


def test_preexisting_skip_ok():
    old = BASE_TEST.replace(
        "def test_beta():",
        "@pytest.mark.skip\ndef test_beta():",
    )
    new = old.replace("assert 1 + 1 == 2", "assert 1 + 1 == 2  # touch")
    res = check({"t.py": old}, {"t.py": new})
    assert res.fails == [], f"pre-existing skip must pass: {res.fails}"


def test_new_test_file_ok():
    src = 'def test_fresh():\n    assert 1 == 1\n    assert 2 == 2\n'
    res = check({}, {"fresh_test.py": src})
    assert res.fails == []
    assert res.warns == []


def test_skip_travels_with_renamed_test_ok():
    old = BASE_TEST.replace(
        "def test_beta():",
        "@pytest.mark.skip\ndef test_beta():",
    )
    new = old.replace("def test_beta():", "def test_beta_v2():")
    res = check({"t.py": old}, {"t.py": new})
    assert res.fails == [], f"skip traveling with rename must pass: {res.fails}"


def test_split_test_ok():
    # One test split into two: union of statements still covers the original.
    new = BASE_TEST.replace(
        '''def test_alpha():
    assert 1 + 1 == 2
    assert 2 + 2 == 4
''',
        '''def test_alpha_part1():
    assert 1 + 1 == 2


def test_alpha_part2():
    assert 2 + 2 == 4
''',
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == [], f"split test must not fail: {res.fails}"


def test_no_changes_ok():
    res = check({"t.py": BASE_TEST}, {"t.py": BASE_TEST})
    assert res.fails == []
    assert res.warns == []


def test_assertion_decrease_warns_not_fails():
    new = BASE_TEST.replace("    assert 2 + 2 == 4\n", "")
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == [], f"assertion decrease must not fail: {res.fails}"
    assert len(res.warns) == 1
    assert "assertion count decreased" in res.warns[0]


def test_comment_only_change_ok():
    new = BASE_TEST.replace(
        "def test_alpha():", "# a comment\ndef test_alpha():"
    )
    res = check({"t.py": BASE_TEST}, {"t.py": new})
    assert res.fails == []
    assert res.warns == []


# --------------------------------------------------------------------------
# End-to-end: real git repos
# --------------------------------------------------------------------------

def _git(tmp_path, *args):
    r = subprocess.run(
        ["git", "-C", str(tmp_path), *args],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    return r.stdout


@pytest.fixture
def git_repo(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "sample_test.py").write_text(BASE_TEST)
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-qm", "base")
    return tmp_path


def _run_script(repo, *args):
    script = Path(__file__).resolve().parents[1] / "tools" / "check_no_test_weakening.py"
    r = subprocess.run(
        [sys.executable, str(script), "--repo", str(repo), *args],
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout + r.stderr


def test_e2e_weakening_pr_fails(git_repo):
    p = git_repo / "tests" / "sample_test.py"
    p.write_text(p.read_text().replace(
        "def test_beta():", "@pytest.mark.skip\ndef test_beta():"
    ))
    _git(git_repo, "commit", "-qam", "weaken")
    code, out = _run_script(git_repo, "--base-ref", "HEAD~1", "--head-ref", "HEAD")
    assert code == 1, out
    assert "FAIL" in out


def test_e2e_clean_pr_passes(git_repo):
    p = git_repo / "tests" / "sample_test.py"
    p.write_text(p.read_text() + "\n\ndef test_extra():\n    assert True\n")
    _git(git_repo, "commit", "-qam", "add test")
    code, out = _run_script(git_repo, "--base-ref", "HEAD~1", "--head-ref", "HEAD")
    assert code == 0, out
    assert "OK" in out


def test_e2e_no_test_changes_passes(git_repo):
    (git_repo / "README.md").write_text("hello")
    _git(git_repo, "add", ".")
    _git(git_repo, "commit", "-qm", "docs")
    code, out = _run_script(git_repo, "--base-ref", "HEAD~1", "--head-ref", "HEAD")
    assert code == 0, out
