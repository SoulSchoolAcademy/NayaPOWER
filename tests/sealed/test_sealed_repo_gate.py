#!/usr/bin/env python3
"""CI gate: the repo must never hold sealed answer material.

Three rules, all enforced here (this file runs under `python -m pytest -q`
like every other tests/ file, so the gate rides the existing kernel-tests CI):

Rule 1 — SENTINEL: no file in the repo may contain the sealed-key sentinel
    except the two files that are allowed to NAME it (the spec README and
    this gate itself). A hit anywhere else means a raw answer-key file was
    committed — FAIL the build.

Rule 2 — MANIFEST SCHEMA: every tests/sealed/manifests/*.json must validate
    clean under sealed_convention.validate_manifest_file (commitments only,
    sha256 hex, no answer-material fields).

Rule 3 — FILENAME: no file under tests/sealed/ may look like a key file
    (name containing both "answer" and "key", or "unsealed").

Bounded and cheap: the walk skips .git/, reads as bytes with errors ignored,
and skips files > 5 MiB.
"""

from pathlib import Path

from sealed_convention import SENTINEL, validate_manifest_file

REPO_ROOT = Path(__file__).resolve().parents[2]
SEALED_DIR = REPO_ROOT / "tests" / "sealed"

# The only files allowed to NAME the sentinel (documentation + the gate).
SENTINEL_ALLOWLIST = {
    SEALED_DIR / "README.md",
    Path(__file__).resolve(),
}

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
MAX_SCAN_BYTES = 5 * 1024 * 1024


def _iter_repo_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def _readable_bytes(path: Path):
    try:
        if path.stat().st_size > MAX_SCAN_BYTES:
            return None
        return path.read_bytes()
    except OSError:
        return None


def test_no_sealed_answer_blob_in_repo():
    """Rule 1: the sentinel must appear nowhere outside the allowlist."""
    sentinel = SENTINEL.encode("utf-8")
    offenders = []
    for path in _iter_repo_files():
        blob = _readable_bytes(path)
        if blob is None:
            continue
        if sentinel in blob and path.resolve() not in SENTINEL_ALLOWLIST:
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert not offenders, (
        "SEALED ANSWER MATERIAL IN REPO — a file carrying the sealed-key "
        f"sentinel was committed: {offenders}. Keys live OUTSIDE the repo "
        "(director's hidden_files, interim). Remove the file from the tree."
    )


def test_sentinel_allowlist_names_marker_only():
    """The allowlisted files may name the sentinel but must hold no key file.

    The README documents the literal marker. This gate references it only via
    the SENTINEL symbol (built by concatenation) so the gate's own source
    never carries the literal it scans for.
    """
    readme = SEALED_DIR / "README.md"
    gate = Path(__file__).resolve()
    assert readme.exists() and gate.exists()
    assert SENTINEL in readme.read_text(encoding="utf-8", errors="ignore"), \
        "README must document the literal sentinel"
    gate_src = gate.read_text(encoding="utf-8", errors="ignore")
    assert "SENTINEL" in gate_src, "gate must reference the SENTINEL symbol"
    assert SENTINEL not in gate_src, \
        "gate source must not carry the literal sentinel"


def test_manifests_validate():
    """Rule 2: every sealed manifest is commitments-only."""
    manifests_dir = SEALED_DIR / "manifests"
    assert manifests_dir.is_dir(), "tests/sealed/manifests/ missing"
    files = sorted(manifests_dir.glob("*.json"))
    assert files, "no manifests to check — the gate would be vacuous"
    violations = []
    for mf in files:
        violations.extend(validate_manifest_file(mf))
    assert not violations, "sealed manifest violations:\n" + "\n".join(violations)


def test_no_key_like_filenames_under_sealed():
    """Rule 3: no answer-key-looking filenames under tests/sealed/."""
    offenders = []
    for path in SEALED_DIR.rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if ("answer" in name and "key" in name) or "unsealed" in name:
            offenders.append(str(path.relative_to(REPO_ROOT)))
    assert not offenders, (
        "key-like filenames under tests/sealed/: "
        f"{offenders}. Raw keys never enter the repo."
    )
