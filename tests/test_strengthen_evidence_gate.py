"""Tests for the strengthen() evidence gate — Phase 1 of the wiring.

Wires the evidence-level predicates of the error-defense falsification spec
(spec branch naya5/error-defense-falsification, qualify_lesson) into
kernel/memory_metabolism.py strengthen() fail-closed.

The falsification suite proved the bare-string evidence API accepted ANY
non-empty string: a self-citing false lesson reached weight 6.0 and
outranked a genuine trial-verified lesson (weight 1.0). These tests prove
that attack is dead while legitimate independent verification still works.
"""

import hashlib

import pytest

from kernel import memory_metabolism as mm

NOW = "2026-10-10T19:30:00+00:00"
DOER = "attacker"  # mirrors the falsification drill


def _h(s):
    return hashlib.sha256(s.encode()).hexdigest()


def _ev(eid, content, origin="independent-trial", verifier="coda-1",
        source=None, family=None, content_hash=None):
    return mm.EvidenceDescriptor(
        evidence_id=eid,
        content=content,
        content_hash=_h(content) if content_hash is None else content_hash,
        origin=origin,
        verifier=verifier,
        source_record_id=source,
        evidence_family=family,
    )


def _rec(content="the sky is plaid", doer=DOER):
    return mm.create_record(
        content,
        epistemic_state="LEARNING",
        provenance={"doer": doer, "situation": "drill"},
        now=NOW,
    )


# --- the legitimate path still works -----------------------------------------

def test_legitimate_evidence_accepted():
    r = _rec()
    receipt = mm.strengthen(r, _ev("E1", "trial result: plaid confirmed"), now=NOW)
    assert r.verification_weight == 1.0
    assert len(r.evidence) == 1
    assert receipt["evidence_id"] == "E1"
    assert receipt["gate_verdict"] == "EVIDENCE_ACCEPTED"
    assert "weight=1.0" in receipt["detail"]


def test_five_independent_verifiers_accumulate():
    r = _rec()
    for i in range(5):
        mm.strengthen(
            r,
            _ev(f"E{i}", f"independent verification {i}",
                origin=f"trial-{i}", verifier=f"verifier-{i}"),
            now=NOW,
        )
    assert r.verification_weight == 5.0


def test_evidence_from_other_record_accepted():
    r = _rec()
    mm.strengthen(
        r, _ev("E1", "derived from an earlier trial", source="MEM-older-record"),
        now=NOW,
    )
    assert r.verification_weight == 1.0


def test_no_doer_provenance_still_enforces_attribution():
    r = mm.create_record("x", epistemic_state="LEARNING",
                         provenance={}, now=NOW)
    mm.strengthen(r, _ev("E1", "attributed evidence"), now=NOW)
    assert r.verification_weight == 1.0
    with pytest.raises(mm.MemoryMetabolismError,
                       match="INSUFFICIENT_INDEPENDENT_EVIDENCE"):
        mm.strengthen(r, _ev("E2", "no origin", origin=""), now=NOW)


# --- the falsification attacks are dead --------------------------------------

def test_self_citation_refused():
    """The drill's attack #1: a record citing itself as its own proof."""
    r = _rec()
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_CIRCULAR_PROOF"):
        mm.strengthen(
            r,
            _ev("E1", "proof: trust me", source=r.record_id),
            now=NOW,
        )
    assert r.verification_weight == 0.0
    assert r.evidence == []


def test_self_citation_case_insensitive():
    r = _rec()
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_CIRCULAR_PROOF"):
        mm.strengthen(
            r,
            _ev("E1", "proof: trust me", source=r.record_id.upper()),
            now=NOW,
        )
    assert r.verification_weight == 0.0


def test_evidence_restating_record_refused():
    """Evidence that merely restates the record's own content is self-proof."""
    r = _rec(content="the sky is plaid")
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_CIRCULAR_PROOF"):
        mm.strengthen(r, _ev("E1", "the sky is plaid"), now=NOW)
    assert r.verification_weight == 0.0


def test_doer_echo_chamber_refused():
    """The drill's attack #2: the doer manufacturing its own 'evidence'."""
    r = _rec(doer="attacker")
    with pytest.raises(mm.MemoryMetabolismError,
                       match="INSUFFICIENT_INDEPENDENT_EVIDENCE"):
        mm.strengthen(
            r, _ev("E1", "I verified myself", origin="attacker",
                   verifier="coda-1"),
            now=NOW,
        )
    assert r.verification_weight == 0.0


def test_doer_identity_case_insensitive():
    r = _rec(doer="attacker")
    with pytest.raises(mm.MemoryMetabolismError,
                       match="INSUFFICIENT_INDEPENDENT_EVIDENCE"):
        mm.strengthen(
            r, _ev("E1", "I verified myself", origin="ATTACKER",
                   verifier="coda-1"),
            now=NOW,
        )
    assert r.verification_weight == 0.0


def test_duplicate_evidence_refused():
    """The same evidence twice is echo inflation, not verification."""
    r = _rec()
    mm.strengthen(r, _ev("E1", "trial result"), now=NOW)
    with pytest.raises(mm.MemoryMetabolismError,
                       match="INSUFFICIENT_INDEPENDENT_EVIDENCE"):
        mm.strengthen(r, _ev("E2", "trial result"), now=NOW)  # same content
    assert r.verification_weight == 1.0


def test_verifier_is_doer_refused():
    r = _rec(doer="attacker")
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_SELF_CERTIFICATION"):
        mm.strengthen(
            r, _ev("E1", "independent trial", origin="trial-x",
                   verifier="attacker"),
            now=NOW,
        )
    assert r.verification_weight == 0.0


def test_missing_verifier_refused():
    r = _rec()
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_SELF_CERTIFICATION"):
        mm.strengthen(r, _ev("E1", "anonymous verification", verifier=""),
                      now=NOW)
    assert r.verification_weight == 0.0


def test_tampered_content_hash_refused():
    r = _rec()
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_INTEGRITY"):
        mm.strengthen(
            r, _ev("E1", "real content", content_hash=_h("different content")),
            now=NOW,
        )
    assert r.verification_weight == 0.0


def test_bare_string_evidence_refused_fail_closed():
    """The old API shape is refused, never silently coerced."""
    r = _rec()
    with pytest.raises(mm.MemoryMetabolismError,
                       match="BLOCKED_INTEGRITY"):
        mm.strengthen(r, "just a string", now=NOW)  # type: ignore[arg-type]
    assert r.verification_weight == 0.0


def test_none_evidence_refused():
    r = _rec()
    with pytest.raises(mm.MemoryMetabolismError,
                       match="strengthen_evidence_missing"):
        mm.strengthen(r, None, now=NOW)  # type: ignore[arg-type]
    assert r.verification_weight == 0.0


def test_weight_inflation_attack_killed():
    """End-to-end reproduction of the falsification: self-cite + 5
    doer-sourced items must leave the record at weight 0.0."""
    r = _rec(doer="attacker")
    attacks = [
        _ev("E-self", "proof: trust me", source=r.record_id),
        *(_ev(f"E{i}", f"attacker evidence {i}", origin="attacker",
              verifier="attacker")
          for i in range(1, 6)),
    ]
    refused = 0
    for ev in attacks:
        with pytest.raises(mm.MemoryMetabolismError):
            mm.strengthen(r, ev, now=NOW)
        refused += 1
    assert refused == 6
    assert r.verification_weight == 0.0
    assert r.evidence == []
    # The record is untouched and still promotable by honest evidence.
    mm.strengthen(r, _ev("E-real", "genuine trial result"), now=NOW)
    assert r.verification_weight == 1.0


# --- existing machinery preserved --------------------------------------------

def test_dead_record_still_refused():
    r = _rec()
    r2 = _rec(content="replacement")
    mm.supersede(r, r2, now=NOW)
    with pytest.raises(mm.MemoryMetabolismError,
                       match="strengthen_refused_not_active"):
        mm.strengthen(r, _ev("E1", "late evidence"), now=NOW)


def test_integrity_checked_first():
    r = _rec()
    r.content = "tampered"
    with pytest.raises(mm.MemoryMetabolismError,
                       match="memory_integrity_failed"):
        mm.strengthen(r, _ev("E1", "evidence"), now=NOW)


def test_evidence_entries_are_structured():
    r = _rec()
    mm.strengthen(r, _ev("E1", "trial result", origin="trial-x",
                         verifier="coda-1"), now=NOW)
    entry = r.evidence[0]
    assert entry["evidence_id"] == "E1"
    assert entry["origin"] == "trial-x"
    assert entry["verifier"] == "coda-1"
    assert entry["content_hash"] == _h("trial result")
    # The integrity seal covers the structured evidence.
    assert mm.integrity_ok(r)


def test_evidence_summary_renders():
    r = _rec()
    mm.strengthen(r, _ev("E1", "trial result", origin="trial-x",
                         verifier="coda-1"), now=NOW)
    summary = mm.evidence_summary(r.evidence[0])
    assert "E1" in summary and "trial-x" in summary and "coda-1" in summary


def test_receipt_deterministic():
    r1 = _rec()
    r2 = mm.create_record("the sky is plaid", epistemic_state="LEARNING",
                          provenance={"doer": DOER, "situation": "drill"},
                          now=NOW)
    rec1 = mm.strengthen(r1, _ev("E1", "trial result"), now=NOW)
    rec2 = mm.strengthen(r2, _ev("E1", "trial result"), now=NOW)
    assert rec1["receipt_id"] == rec2["receipt_id"]
