"""Executable invariants for the constitutional self-declaration audit.

A gate that cannot detect a rival constitution cannot govern one. These tests
pin the detection behavior of `.naya/runtime/constitutional_claim_audit.py`
against synthetic repositories, so the gate itself is trustworthy before it is
pointed at the real tree.

They do not replace the constitutional law; they make the audit's own contract
checkable.
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

_MODULE = Path(__file__).resolve().parents[1] / "runtime" / "constitutional_claim_audit.py"
_spec = importlib.util.spec_from_file_location("constitutional_claim_audit", _MODULE)
assert _spec and _spec.loader
audit_mod = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = audit_mod
_spec.loader.exec_module(audit_mod)


SUPREME = "# Amendment\n\n**Status:** CANONICAL / CONSTITUTIONAL / ACTIVE\n"
POINTER = "# Pointer\n\n**Status:** CANONICAL POINTER\n"
PRIVATE_VOCAB = "# Charter\n\n**Status:** SUPREME GOVERNING AUTHORITY\n"
PROPOSED = "# Draft\n\n**Status:** PROPOSED — REVIEW REQUIRED\n"
ORDINARY = "# Project log\n\n**Status:** ACTIVE\n\nSome work happened.\n"


def _kinds(report: dict) -> set[str]:
    return {f["kind"] for f in report["findings"]}


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _repo(files: dict[str, str], registry: str | None) -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    for rel, text in files.items():
        _write(root, rel, text)
    if registry is not None:
        _write(root, audit_mod.REGISTRY_RELPATH, registry)
    tmp.files = files  # type: ignore[attr-defined]
    return tmp


# --- claim extraction -------------------------------------------------------

def test_detects_supreme_authority_claim() -> None:
    claim = audit_mod.claim_of(SUPREME)
    assert claim is not None
    assert claim["supreme"] is True
    assert "CANONICAL" in claim["authority_tokens"]
    assert "ACTIVE" in claim["active_tokens"]
    assert claim["vocabulary_ok"] is True  # ACTIVE is a section 16 status


def test_ordinary_active_document_is_a_claim_but_never_supreme() -> None:
    """Negative control: 'ACTIVE' alone is not a constitutional claim.

    Scope is enforced by ``is_governance_surface``, not by ``claim_of``, so a
    project log does yield a (non-supreme) claim record. What must never happen
    is that it counts as an in-force constitutional claim.
    """
    claim = audit_mod.claim_of(ORDINARY)
    assert claim is not None
    assert claim["supreme"] is False
    assert claim["authority_tokens"] == []


def test_proposed_document_is_a_claim_but_not_supreme() -> None:
    """PROPOSED alone carries no authority token, so it is not in force."""
    assert audit_mod.claim_of(PROPOSED) is None


def test_authority_without_in_force_token_is_not_supreme() -> None:
    """A canonical pointer does not claim to be the supreme law in force."""
    claim = audit_mod.claim_of(POINTER)
    assert claim is not None
    assert claim["supreme"] is False
    assert "CANONICAL" in claim["authority_tokens"]


def test_private_vocabulary_status_is_detected() -> None:
    claim = audit_mod.claim_of(PRIVATE_VOCAB)
    assert claim is not None
    assert claim["vocabulary_ok"] is False


# --- governance surface -----------------------------------------------------

def test_governance_surface_by_filename() -> None:
    assert audit_mod.is_governance_surface(
        Path("a/CONSTITUTIONAL-AMENDMENT-01.md"), "a/CONSTITUTIONAL-AMENDMENT-01.md"
    )


def test_governance_surface_by_contract_library_membership() -> None:
    assert audit_mod.is_governance_surface(
        Path(".naya/contracts/anything.md"), ".naya/contracts/anything.md"
    )


def test_project_log_is_outside_governance_surface() -> None:
    assert not audit_mod.is_governance_surface(
        Path(".naya/logs/2026-09-26-run.md"), ".naya/logs/2026-09-26-run.md"
    )


# --- fingerprint stability --------------------------------------------------

def test_fingerprint_is_stable_across_content_edits() -> None:
    """Editing a claimant must not silently reset its debt record."""
    a = audit_mod.finding("KIND", "d", ["x.md"])
    b = audit_mod.finding("KIND", "totally different detail", ["x.md"])
    assert a["fingerprint"] == b["fingerprint"]


def test_fingerprint_changes_when_locations_change() -> None:
    """Adding a rival claimant is new drift, not a re-baseline."""
    a = audit_mod.finding("KIND", "d", ["x.md"])
    b = audit_mod.finding("KIND", "d", ["x.md", "y.md"])
    assert a["fingerprint"] != b["fingerprint"]


def test_fingerprint_changes_with_kind() -> None:
    assert audit_mod.finding("A", "d", ["x.md"])["fingerprint"] != audit_mod.finding(
        "B", "d", ["x.md"]
    )["fingerprint"]


# --- end to end on synthetic repositories -----------------------------------

def test_two_rival_supreme_claims_are_flagged_as_unresolvable() -> None:
    tmp = _repo(
        {
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME,
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-BETA.md": SUPREME,
        },
        registry="# Registry\n",
    )
    try:
        report = audit_mod.audit(Path(tmp.name))
        assert "CONCURRENT_SUPREME_CLAIM" in _kinds(report)
        assert "UNMAPPED_AUTHORITY_CLAIM" in _kinds(report)
        assert len(report["unmapped_supreme_claims"]) == 2
    finally:
        tmp.cleanup()


def test_supersession_resolves_the_concurrent_claim() -> None:
    """A real supersession edge naming a real artifact collapses the conflict."""
    tmp = _repo(
        {
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME,
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-BETA.md": (
                "# Amendment\n\n"
                "**Status:** CANONICAL / CONSTITUTIONAL / ACTIVE\n\n"
                "This amendment supersedes CONSTITUTIONAL-AMENDMENT-ALPHA.\n"
            ),
        },
        registry="# Registry\n",
    )
    try:
        report = audit_mod.audit(Path(tmp.name))
        assert "CONCURRENT_SUPREME_CLAIM" not in _kinds(report)
    finally:
        tmp.cleanup()


def test_supersession_word_without_a_real_artifact_does_not_resolve() -> None:
    """A bare 'supersedes' in prose is not an authority grant."""
    tmp = _repo(
        {
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME,
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-BETA.md": (
                "# Amendment\n\n"
                "**Status:** CANONICAL / CONSTITUTIONAL / ACTIVE\n\n"
                "This amendment supersedes some document that does not exist.\n"
            ),
        },
        registry="# Registry\n",
    )
    try:
        report = audit_mod.audit(Path(tmp.name))
        assert "CONCURRENT_SUPREME_CLAIM" in _kinds(report)
    finally:
        tmp.cleanup()


def test_missing_registry_fails_closed() -> None:
    tmp = _repo({".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME}, registry=None)
    try:
        report = audit_mod.audit(Path(tmp.name))
        assert "REGISTRY_UNREACHABLE" in _kinds(report)
    finally:
        tmp.cleanup()


def test_registry_mapping_clears_the_unmapped_finding() -> None:
    """Mapping a claimant in the registry is what resolves it. Authority is
    still the Director's decision; this only proves the map is complete."""
    tmp = _repo(
        {".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME},
        registry="# Registry\n\n- maps `.naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md`\n",
    )
    try:
        report = audit_mod.audit(Path(tmp.name))
        assert "UNMAPPED_AUTHORITY_CLAIM" not in _kinds(report)
        assert report["unmapped_supreme_claims"] == []
    finally:
        tmp.cleanup()


def test_clean_repository_produces_no_findings() -> None:
    """One mapped, properly superseded constitution is a conforming system."""
    tmp = _repo(
        {
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": (
                "# Amendment\n\n"
                "**Status:** CANONICAL / CONSTITUTIONAL / ACTIVE\n\n"
                "Supersedes CONSTITUTIONAL-AMENDMENT-OLD.\n"
            ),
            ".naya/codex/CONSTITUTIONAL-AMENDMENT-OLD.md": (
                "# Amendment\n\n**Status:** SUPERSEDED\n"
            ),
        },
        registry="# Registry\n\n- `.naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md`\n"
        "- `.naya/codex/CONSTITUTIONAL-AMENDMENT-OLD.md`\n",
    )
    try:
        report = audit_mod.audit(Path(tmp.name))
        assert report["findings"] == []
    finally:
        tmp.cleanup()


def test_non_governance_churn_cannot_trigger_the_gate() -> None:
    """Adding ordinary active project logs must never fail this gate.

    Also pins the audit's own scope: unrelated file churn must not widen the
    reported claim set either, or the audit would silently start treating
    project logs as governance instruments.
    """
    tmp = _repo(
        {".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME},
        registry="# Registry\n\n- `.naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md`\n",
    )
    try:
        root = Path(tmp.name)
        before = audit_mod.audit(root)
        for i in range(25):
            _write(root, f".naya/logs/2026-09-{i}-ACTIVE-RUN.md", ORDINARY)
            _write(root, f"docs/smart-notes/2026/09/note-{i}.md", ORDINARY)
        after = audit_mod.audit(root)
        assert after["findings"] == before["findings"] == []
        assert (
            after["self_declaring_artifacts"] == before["self_declaring_artifacts"]
        ), "audit scope widened to include non-governance documents"
        assert after["artifacts_scanned"] > before["artifacts_scanned"]
    finally:
        tmp.cleanup()


# --- baseline fail-closed behavior -----------------------------------------

def test_baseline_absent_means_every_finding_is_new_drift() -> None:
    tmp = _repo({".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME}, registry="# R\n")
    try:
        report = audit_mod.audit(Path(tmp.name))
        code, text = audit_mod.render(report, audit_mod.load_baseline(Path(tmp.name)))
        assert code == 1
        assert "NEW DRIFT" in text
    finally:
        tmp.cleanup()


def test_baselined_finding_is_known_debt_and_does_not_fail() -> None:
    tmp = _repo({".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME}, registry="# R\n")
    try:
        root = Path(tmp.name)
        report = audit_mod.audit(root)
        baseline = {f["fingerprint"] for f in report["findings"]}
        code, text = audit_mod.render(report, baseline)
        assert code == 0
        assert "KNOWN DEBT" in text
        assert "CONSTITUTIONAL_CLAIMS_NO_NEW_DRIFT" in text
        # Critical: known debt must never read as a clean bill of health.
        assert "NOT a pass" in text
    finally:
        tmp.cleanup()


def test_a_new_claimant_fails_even_when_prior_debt_is_baselined() -> None:
    """The anti-washout property: baselining must not absorb future rivals."""
    tmp = _repo({".naya/codex/CONSTITUTIONAL-AMENDMENT-ALPHA.md": SUPREME}, registry="# R\n")
    try:
        root = Path(tmp.name)
        baseline = {f["fingerprint"] for f in audit_mod.audit(root)["findings"]}
        _write(root, ".naya/codex/CONSTITUTIONAL-AMENDMENT-BETA.md", SUPREME)
        code, text = audit_mod.render(audit_mod.audit(root), baseline)
        assert code == 1
        assert "NEW DRIFT" in text
    finally:
        tmp.cleanup()
