"""Tests for Law 12 proof expiry (kernel/protocol/proof_expiry.py).

Law 12: "Proofs expire when world changes."

Each test covers a true positive (staleness detected) and a true negative
(clean proof passes). A check that cannot catch its own defect is theater.
"""

import sys
import time
from pathlib import Path

# Repo-relative import (see test_engineering_gates.py): never machine-absolute.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "kernel" / "protocol"))

from proof_expiry import (
    BoundaryCheck,
    ProofDependency,
    ProofRecord,
    ProofStatus,
    ProofValidation,
    check_execution_boundary,
    mark_invalid,
    proof_from_authority,
    proof_from_read_receipt,
    proof_from_scorecard,
    reverify,
    validate_proof,
    DEP_SOURCE_SHA,
    DEP_POLICY_REF,
    DEP_AUTHORITY_RECEIPT,
)


def _proof(**kw):
    deps = kw.pop("dependencies", [
        ProofDependency(DEP_SOURCE_SHA, "aaa"),
        ProofDependency(DEP_POLICY_REF, "v1"),
    ])
    kw.setdefault("proof_id", "p1")
    return ProofRecord(proof_type="test",
                       dependencies=deps, **kw)


# --- validate_proof: true negatives ---------------------------------------

def test_current_when_all_dependencies_match():
    p = _proof()
    v = validate_proof(p, {DEP_SOURCE_SHA: "aaa", DEP_POLICY_REF: "v1"})
    assert v.is_current
    assert v.status == ProofStatus.CURRENT_UNTIL_RECHECK
    assert p.status == ProofStatus.CURRENT_UNTIL_RECHECK


def test_precise_invalidation_unrelated_change_ignored():
    """A world change in a kind the proof does not depend on cannot stale it."""
    p = _proof()
    v = validate_proof(p, {
        DEP_SOURCE_SHA: "aaa",
        DEP_POLICY_REF: "v1",
        "unrelated_kind": "changed-value",
        "another_unrelated": "xyz",
    })
    assert v.is_current, "unrelated changes must not invalidate the proof"


# --- validate_proof: true positives ----------------------------------------

def test_stale_when_source_sha_moves():
    p = _proof()
    v = validate_proof(p, {DEP_SOURCE_SHA: "bbb", DEP_POLICY_REF: "v1"})
    assert not v.is_current
    assert v.status == ProofStatus.STALE
    assert len(v.stale_dependencies) == 1
    assert v.stale_dependencies[0].kind == DEP_SOURCE_SHA
    assert "changed" in v.reason()


def test_stale_when_policy_version_moves():
    p = _proof()
    v = validate_proof(p, {DEP_SOURCE_SHA: "aaa", DEP_POLICY_REF: "v2"})
    assert not v.is_current
    assert v.stale_dependencies[0].kind == DEP_POLICY_REF


def test_stale_when_current_value_unknown():
    """Missing current value = cannot confirm freshness = STALE, not current."""
    p = _proof()
    v = validate_proof(p, {DEP_SOURCE_SHA: "aaa"})  # no policy_ref provided
    assert not v.is_current
    assert DEP_POLICY_REF in v.missing_dependencies


def test_multiple_stale_dependencies_all_reported():
    p = _proof()
    v = validate_proof(p, {DEP_SOURCE_SHA: "bbb", DEP_POLICY_REF: "v2"})
    assert len(v.stale_dependencies) == 2


# --- mark_invalid / reverify -------------------------------------------------

def test_mark_invalid_is_terminal():
    p = _proof()
    mark_invalid(p, "grant revoked by Shawn")
    assert p.status == ProofStatus.INVALID
    try:
        reverify(p, {DEP_SOURCE_SHA: "aaa", DEP_POLICY_REF: "v1"})
    except ValueError as e:
        assert "INVALID" in str(e)
    else:
        raise AssertionError("reverify on INVALID proof must raise")


def test_reverify_refreshes_changed_dependency():
    p = _proof()
    v1 = validate_proof(p, {DEP_SOURCE_SHA: "bbb", DEP_POLICY_REF: "v1"})
    assert not v1.is_current
    v2 = reverify(p, {DEP_SOURCE_SHA: "bbb", DEP_POLICY_REF: "v1"},
                  new_values={DEP_SOURCE_SHA: "bbb"})
    assert v2.is_current, "after refresh, proof must be current again"


def test_reverify_without_refresh_stays_stale():
    p = _proof()
    validate_proof(p, {DEP_SOURCE_SHA: "bbb", DEP_POLICY_REF: "v1"})
    v2 = reverify(p, {DEP_SOURCE_SHA: "bbb", DEP_POLICY_REF: "v1"})
    assert not v2.is_current, "reverify without new values must stay stale"


# --- execution boundary -----------------------------------------------------

def test_boundary_proceeds_when_all_current():
    p1 = _proof(proof_id="a")
    p2 = _proof(proof_id="b")
    b = check_execution_boundary(
        [p1, p2], {DEP_SOURCE_SHA: "aaa", DEP_POLICY_REF: "v1"})
    assert b.proceed
    assert b.blockers() == []


def test_boundary_blocks_when_any_stale():
    p1 = _proof(proof_id="a")
    p2 = _proof(proof_id="b")
    b = check_execution_boundary(
        [p1, p2], {DEP_SOURCE_SHA: "CHANGED", DEP_POLICY_REF: "v1"})
    assert not b.proceed
    blockers = b.blockers()
    assert len(blockers) == 2
    assert any("a:" in x for x in blockers)
    assert isinstance(b, BoundaryCheck)


def test_boundary_empty_proof_list_proceeds():
    b = check_execution_boundary([], {})
    assert b.proceed


# --- adapters ----------------------------------------------------------------

class _FakeReceipt:
    agent_id = "naya-5"
    protocol_version = "2026-10-08-ULTIMATE"
    receipt_hash = "deadbeef1234"
    issued_at = time.time()


class _FakeScorecard:
    what = "test deliverable"


def test_adapter_read_receipt_tracks_protocol_version():
    p = proof_from_read_receipt(_FakeReceipt(), source_sha="tip123")
    kinds = p.dependency_kinds()
    assert DEP_POLICY_REF in kinds
    assert DEP_SOURCE_SHA in kinds
    # Protocol version change stales the receipt (re-read required).
    v = validate_proof(p, {DEP_POLICY_REF: "2026-10-09-NEW",
                           DEP_SOURCE_SHA: "tip123"})
    assert not v.is_current


def test_adapter_scorecard_tracks_scored_code():
    s = _FakeScorecard()
    p = proof_from_scorecard(s, source_sha="code-sha-1", policy_ref="rubric-v3")
    v = validate_proof(p, {DEP_SOURCE_SHA: "code-sha-2",
                           DEP_POLICY_REF: "rubric-v3"})
    assert not v.is_current
    assert v.stale_dependencies[0].kind == DEP_SOURCE_SHA


def test_adapter_authority_tracks_grant():
    p = proof_from_authority("grant-42", source_sha="s1", policy_ref="pol1")
    assert DEP_AUTHORITY_RECEIPT in p.dependency_kinds()
    v = validate_proof(p, {DEP_AUTHORITY_RECEIPT: "grant-42",
                           DEP_SOURCE_SHA: "s1",
                           DEP_POLICY_REF: "pol1"})
    assert v.is_current
