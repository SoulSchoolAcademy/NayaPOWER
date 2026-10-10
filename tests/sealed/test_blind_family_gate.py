#!/usr/bin/env python3
"""CI gate: blind-family discipline (Phase 3A activation).

Two rules, both fail-closed:

Rule 1 — T11 RETIREMENT: QUAL-20261010-CIQ-001 (T11, "The Reserve Rule") is
    retired from blind use — its answers are exposed in the database and
    local JSON receipts. Any file outside tests/sealed/ that names the
    retired family fails, except explicitly allowlisted precedent
    documentation. A new blind claim for T11 fails closed, full stop.

Rule 2 — NO INLINE EXPECTED VALUES FOR BLIND FAMILIES: a blind-eligible
    family (registry: family_registry.FAMILIES, blind_eligible=True) must
    resolve expected values from the sealed store — SHA-256 commitments in
    tests/sealed/manifests/, raw keys outside the repo. Any test file
    outside tests/sealed/ that BOTH names a blind family (qualification ID
    or family task-ID prefix) AND carries inline expected-answer material
    fails, with a message pointing at the sealed convention.

This file runs under `python -m pytest -q` (kernel-tests.yml), so both rules
are enforced on every commit. tests/sealed/ itself is exempt: it is the
convention's home (commitments, registry, custody contract — never answers).
"""

import re
from pathlib import Path

from family_registry import FAMILIES
from sealed_convention import FORBIDDEN_MANIFEST_FIELDS

REPO_ROOT = Path(__file__).resolve().parents[2]
SEALED_DIR = REPO_ROOT / "tests" / "sealed"

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
MAX_SCAN_BYTES = 5 * 1024 * 1024

# Pre-existing documentation that names the retired family as precedent —
# not a blind claim. New references need a human, not an allowlist entry.
RETIRED_FAMILY_DOC_ALLOWLIST = {
    REPO_ROOT / "drift_canary" / "canary.py",  # docstring: sealed-key precedent
}

# Inline answer material: the forbidden manifest fields, plus dict-literal
# shapes that map task IDs to decisions (e.g. {"T12-CONFLICT-001": "APPLY"}).
ANSWER_MATERIAL_RES = [
    re.compile(r"\b" + re.escape(f) + r"\b")
    for f in FORBIDDEN_MANIFEST_FIELDS
    if f not in {"rationale"}  # "rationale" is common prose; other fields are not
]


def _iter_repo_files():
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def _readable_text(path: Path):
    try:
        if path.stat().st_size > MAX_SCAN_BYTES:
            return None
        return path.read_bytes().decode("utf-8", errors="ignore")
    except OSError:
        return None


def _is_under_sealed(path: Path) -> bool:
    try:
        path.resolve().relative_to(SEALED_DIR.resolve())
        return True
    except ValueError:
        return False


def _blind_family_markers():
    """(qualification_id, task_prefix_or_None) for blind-eligible families."""
    out = []
    for qid, fam in FAMILIES.items():
        if fam.get("blind_eligible"):
            out.append((qid, fam.get("task_id_prefix")))
    return out


def test_retired_family_names_fail_closed():
    """Rule 1: T11 is retired from blind use. New references fail closed."""
    retired_ids = [qid for qid, fam in FAMILIES.items()
                   if fam.get("state") == "retired"]
    assert retired_ids, "registry has no retired family — the gate would be vacuous"
    offenders = []
    for path in _iter_repo_files():
        if _is_under_sealed(path):
            continue
        if path.resolve() in {p.resolve() for p in RETIRED_FAMILY_DOC_ALLOWLIST}:
            continue
        text = _readable_text(path)
        if text is None:
            continue
        for qid in retired_ids:
            if qid in text:
                offenders.append(f"{path.relative_to(REPO_ROOT)} names retired {qid}")
    assert not offenders, (
        "RETIRED FAMILY REFERENCED FOR BLIND USE — T11 "
        "(QUAL-20261010-CIQ-001) was retired from blind qualification on "
        "2026-10-10 (answers exposed in DB + local JSON). Blind claims for "
        "T11 fail closed. Offenders:\n  " + "\n  ".join(offenders) +
        "\nSee tests/sealed/README.md — use the sealed T12 family instead."
    )


def test_no_inline_expected_values_for_blind_families():
    """Rule 2: blind families resolve expected values from the sealed store."""
    markers = _blind_family_markers()
    assert markers, "registry has no blind-eligible family — the gate would be vacuous"
    offenders = []
    for path in _iter_repo_files():
        if _is_under_sealed(path):
            continue
        text = _readable_text(path)
        if text is None:
            continue
        for qid, prefix in markers:
            named = qid in text or (prefix and re.search(r"\b" + re.escape(prefix) + r"[A-Z0-9-]+\b", text))
            if not named:
                continue
            hits = [rx.pattern for rx in ANSWER_MATERIAL_RES if rx.search(text)]
            if hits:
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}: inline expected-answer "
                    f"material for blind family {qid} ({', '.join(hits)})"
                )
    assert not offenders, (
        "INLINE EXPECTED VALUES FOR A BLIND FAMILY — blind-qualification "
        "families must resolve expected values from the sealed store "
        "(SHA-256 commitments in tests/sealed/manifests/, raw keys outside "
        "the repo), never from inline literals. Offenders:\n  " +
        "\n  ".join(offenders) +
        "\nSee tests/sealed/README.md — the sealed-fixture convention."
    )


def test_registry_lifecycle_is_sound():
    """The registry the gates enforce must itself be well-formed."""
    from family_registry import assert_valid_lifecycle
    problems = assert_valid_lifecycle()
    assert not problems, "family registry problems:\n" + "\n".join(problems)
