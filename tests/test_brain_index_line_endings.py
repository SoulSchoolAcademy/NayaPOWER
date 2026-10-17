"""Regression test: the brain-index regen must write LF, never CRLF.

Why this test exists
--------------------
`tools/regenerate_brain_index.py` is the only generator whose output is
compared against committed bytes by a registered gate
(`BRAIN-INDEX-FRESHNESS`, `tools/protocol/checks/brain_index_freshness.py`).

It originally wrote via `Path.write_text(..., encoding="utf-8")` with no
`newline=`. Python's text mode defaults to newline=None, which translates
"\n" to `os.linesep` — CRLF on Windows. Measured on a clean checkout of
main@dc858ecdc6f3314ae1ec4c0b2dffd14954932a5a:

    regenerated BRAIN/REAL-TREE.json : 302,374 bytes, 6,669 CRLF
    committed  BRAIN/REAL-TREE.json : 604,750 bytes,     0 CRLF

Exactly 2x. Regenerating on Windows therefore produced a ~8,400-line diff
across the three index files where the true change was ~15 lines.

The gate does not catch this, and cannot: `brain_index_freshness.py`
normalizes both sides through `normalize_json`/`normalize_md` before
comparing. That is correct for cross-platform comparison and it is exactly
why the churn stayed invisible — CI stayed green, and only the contributor
drowning in a phantom diff could see it. Nine separate branches named
variations on "fix brain index drift" failed before the cause was found.

What this test proves
---------------------
That the module's write seam emits LF bytes on every platform, independent
of the host's os.linesep. That is the property whose absence produced the
defect.

What this test does NOT prove
-----------------------------
That the committed index is fresh (that is `test_brain_index_freshness.py`),
nor that regeneration is semantically correct (the gate says out loud that a
wrong-but-consistent index still passes).
"""

import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGEN_PATH = ROOT / "tools" / "regenerate_brain_index.py"


def load_regen():
    spec = importlib.util.spec_from_file_location(
        "regenerate_brain_index_under_test", REGEN_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_write_lf_emits_lf_bytes(tmp_path):
    """The write seam produces LF-only bytes whatever the host platform."""
    regen = load_regen()
    target = tmp_path / "probe.txt"
    regen.write_lf(target, "alpha\nbeta\ngamma\n")
    assert target.read_bytes() == b"alpha\nbeta\ngamma\n"


def test_write_lf_contains_no_carriage_return(tmp_path):
    """No CR byte may appear, even where os.linesep is CRLF (Windows)."""
    regen = load_regen()
    target = tmp_path / "probe.txt"
    regen.write_lf(target, "one\ntwo\n")
    assert b"\r" not in target.read_bytes()


def test_write_lf_differs_from_the_bare_default_on_crlf_platforms(tmp_path):
    """Falsifier for the fix itself.

    The bare `write_text` default translates "\n" to os.linesep. On a
    CRLF platform that produces different bytes than write_lf. This asserts
    the two genuinely diverge there — so the fix is load-bearing, not
    cosmetic. On an LF platform the assertion is skipped because the two
    are correctly identical and the bug cannot manifest there.
    """
    if os.linesep != "\r\n":
        import pytest
        pytest.skip("default-translation divergence only observable on "
                    "a CRLF platform (os.linesep == CRLF)")

    regen = load_regen()
    default_path = tmp_path / "default.txt"
    fixed_path = tmp_path / "fixed.txt"

    default_path.write_text("alpha\nbeta\n", encoding="utf-8")
    regen.write_lf(fixed_path, "alpha\nbeta\n")

    assert default_path.read_bytes() != fixed_path.read_bytes(), (
        "the bare write_text default produced the same bytes as write_lf; "
        "the newline= parameter is not doing anything on this platform"
    )


def test_no_bare_write_text_outside_the_lf_seam():
    """Structural guard, resolved with the AST so prose cannot satisfy it.

    Every real `.write_text(...)` call in the module must be either the one
    inside `write_lf` (which passes newline="\\n") or carry an explicit
    newline= argument. A comment or docstring mentioning write_text is not a
    call and must not count — hence the AST instead of a text search.
    """
    import ast

    tree = ast.parse(REGEN_PATH.read_text(encoding="utf-8"))
    offenders = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "write_text"):
            continue
        # the single sanctioned call inside write_lf()
        if isinstance(node.func, ast.Attribute) and \
                isinstance(node.func.value, ast.Name) and \
                node.func.value.id == "path":
            continue
        has_newline = any(kw.arg == "newline" for kw in node.keywords)
        if not has_newline:
            offenders.append(f"line {node.lineno}: write_text without newline=")

    assert not offenders, (
        "these write_text calls can emit CRLF on Windows:\n  "
        + "\n  ".join(offenders)
    )


def test_write_lf_is_the_only_sanctioned_write_seam():
    """The three index files must be written through write_lf()."""
    src = REGEN_PATH.read_text(encoding="utf-8")
    for rel in (
        "REAL-TREE.json",
        "REAL-TREE.md",
        "NAYAPOWER-BRAIN-INDEX.json",
    ):
        assert f'write_lf(root / "BRAIN" / "{rel}"' in src, (
            f"{rel} is not written through write_lf()"
        )