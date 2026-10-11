"""Adversarial tests for UD-05 unknown_guard.py.

Positive: genuinely resolved items certify.
Negative: every laundering pattern is refused or detected by name.
"""

import pytest

from unknown_guard import (
    EvidenceState, EvidenceItem, Operation, UnresolvedItem,
    UnknownGuardRefusal, CertificationReceipt,
    guard_certify, guard_allow, resolve_unknown,
    request_permission, check_use,
    derive, scan_report,
    LAUNDER_UNKNOWN_TO_PASS, LAUNDER_UNKNOWN_TO_ALLOW,
    LAUNDER_DROPPED_UNKNOWN, LAUNDER_ABSENCE_AS_SAFETY,
    LAUNDER_ACCESS_AS_CREDIBILITY, LAUNDER_EXCLUDED_AS_SUPPORT,
    PERMIT_DENIED_UNKNOWN, USE_BINDING_VIOLATION,
    RESOLUTION_WITHOUT_EVIDENCE,
)


def ev(eid, state, load_bearing=True, evaluated=True):
    return EvidenceItem(id=eid, state=state, load_bearing=load_bearing,
                        evaluated=evaluated)


def unres(uid):
    return UnresolvedItem(
        id=uid, what_unknown="whether the deployed config matches the repo",
        why_matters="a mismatch would invalidate every test result",
        what_would_resolve="read-only dump of the deployed config",
        owner="deploy-credential holder")


# ---------------------------------------------------------------------------
# Positive: genuinely resolved items certify
# ---------------------------------------------------------------------------

def test_all_confirmed_certifies():
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED),
                "t2": ev("t2", EvidenceState.CONFIRMED)}
    r = guard_certify("merge-gate", "PASS", evidence, [])
    assert isinstance(r, CertificationReceipt)
    assert r.verdict == "PASS"


def test_resolved_unknown_then_certifies():
    item = unres("u1")
    resolve_unknown(item, "deployed-config-dump-2026-10-10.txt")
    assert item.status == "RESOLVED"
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED)}
    r = guard_certify("merge-gate", "PASS", evidence, [item])
    assert r.verdict == "PASS"


def test_undetermined_non_load_bearing_does_not_block():
    # Undetermined on a dimension nothing rests on: honest, not blocking.
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED),
                "cosmetic": ev("cosmetic", EvidenceState.UNDETERMINED,
                               load_bearing=False)}
    r = guard_certify("merge-gate", "PASS", evidence, [])
    assert r.verdict == "PASS"


def test_allow_with_clean_evidence():
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED)}
    assert guard_allow("deploy", evidence, []) == "ALLOWED"


# ---------------------------------------------------------------------------
# Negative: unknown -> PASS refused, item named
# ---------------------------------------------------------------------------

def test_unknown_to_pass_refused_and_named():
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED),
                "safety": ev("safety", EvidenceState.UNDETERMINED)}
    with pytest.raises(UnknownGuardRefusal) as e:
        guard_certify("merge-gate", "PASS", evidence, [])
    assert e.value.code == LAUNDER_UNKNOWN_TO_PASS
    assert "safety" in e.value.items  # the unresolved item is named


def test_open_unresolved_item_blocks_certify():
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED)}
    with pytest.raises(UnknownGuardRefusal) as e:
        guard_certify("merge-gate", "CERTIFIED", evidence, [unres("u1")])
    assert e.value.code == LAUNDER_UNKNOWN_TO_PASS
    assert "u1" in e.value.items


def test_resolution_without_evidence_refused():
    item = unres("u1")
    with pytest.raises(UnknownGuardRefusal) as e:
        resolve_unknown(item, "")
    assert e.value.code == RESOLUTION_WITHOUT_EVIDENCE
    assert item.status == "OPEN"  # still open


# ---------------------------------------------------------------------------
# Negative: default-allow on unknown refused
# ---------------------------------------------------------------------------

def test_default_allow_on_unknown_refused():
    evidence = {"safety": ev("safety", EvidenceState.UNDETERMINED)}
    with pytest.raises(UnknownGuardRefusal) as e:
        guard_allow("deploy", evidence, [])
    assert e.value.code == LAUNDER_UNKNOWN_TO_ALLOW
    assert "safety" in e.value.items


# ---------------------------------------------------------------------------
# Negative: dropped unknowns detected in reports
# ---------------------------------------------------------------------------

def test_dropped_unknown_detected():
    report = {
        "subject": "merge-gate",
        "claimed": "PASS",
        "evidence": {"t1": EvidenceState.CONFIRMED,
                     "safety": EvidenceState.UNDETERMINED},
        "unresolved_declared": ["u-safety"],
        "unresolved_in_report": [],   # declared, then silently dropped
        "statements": [],
    }
    findings = scan_report(report)
    codes = [f.code for f in findings]
    assert LAUNDER_UNKNOWN_TO_PASS in codes
    assert LAUNDER_DROPPED_UNKNOWN in codes
    dropped = [f for f in findings if f.code == LAUNDER_DROPPED_UNKNOWN][0]
    assert "u-safety" in dropped.items or "safety" in dropped.items


def test_clean_report_has_no_findings():
    report = {
        "subject": "merge-gate",
        "claimed": "PASS",
        "evidence": {"t1": EvidenceState.CONFIRMED},
        "unresolved_declared": [],
        "unresolved_in_report": [],
        "statements": [{"text": "All checks passed with measured evidence.",
                        "cites_positive_evidence": True}],
    }
    assert scan_report(report) == []


# ---------------------------------------------------------------------------
# Negative: "no evidence of harm" != "evidence of safety"
# ---------------------------------------------------------------------------

def test_absence_as_safety_flagged():
    report = {
        "subject": "deploy-review",
        "claimed": "SAFE",
        "evidence": {"t1": EvidenceState.CONFIRMED},
        "unresolved_declared": [],
        "unresolved_in_report": [],
        "statements": [{
            "text": "No evidence of harm was found, so the deploy is safe.",
            "cites_positive_evidence": False}],
    }
    findings = scan_report(report)
    assert any(f.code == LAUNDER_ABSENCE_AS_SAFETY for f in findings)


def test_absence_with_real_evidence_not_flagged():
    report = {
        "subject": "deploy-review",
        "claimed": "SAFE",
        "evidence": {"t1": EvidenceState.CONFIRMED},
        "unresolved_declared": [],
        "unresolved_in_report": [],
        "statements": [{
            "text": "No evidence of harm was found; penetration test PT-9 "
                    "passed all 40 cases, so the deploy is safe.",
            "cites_positive_evidence": True}],
    }
    findings = scan_report(report)
    assert not any(f.code == LAUNDER_ABSENCE_AS_SAFETY for f in findings)


# ---------------------------------------------------------------------------
# Negative: access is not credibility (D13)
# ---------------------------------------------------------------------------

def test_access_without_evaluation_refused():
    evidence = {"t1": ev("t1", EvidenceState.CONFIRMED, evaluated=False)}
    with pytest.raises(UnknownGuardRefusal) as e:
        guard_certify("merge-gate", "PASS", evidence, [])
    assert e.value.code == LAUNDER_ACCESS_AS_CREDIBILITY


def test_excluded_evidence_cannot_support():
    evidence = {"t1": ev("t1", EvidenceState.EXCLUDED)}
    with pytest.raises(UnknownGuardRefusal) as e:
        guard_certify("merge-gate", "PASS", evidence, [])
    assert e.value.code == LAUNDER_EXCLUDED_AS_SUPPORT


# ---------------------------------------------------------------------------
# Purpose-bound gate: CERTIFY/ACT fail closed, INSPECT allowed with marker
# ---------------------------------------------------------------------------

def test_certify_denied_on_undetermined():
    evidence = {"safety": ev("safety", EvidenceState.UNDETERMINED)}
    with pytest.raises(UnknownGuardRefusal) as e:
        request_permission("naya-4", "release review", Operation.CERTIFY,
                           evidence, influences="production deploy")
    assert e.value.code == PERMIT_DENIED_UNKNOWN


def test_act_denied_on_undetermined():
    evidence = {"rights": ev("rights", EvidenceState.UNDETERMINED)}
    with pytest.raises(UnknownGuardRefusal) as e:
        request_permission("naya-4", "takedown", Operation.ACT,
                           evidence, influences="user content")
    assert e.value.code == PERMIT_DENIED_UNKNOWN


def test_inspect_allowed_with_undetermined_but_marked():
    evidence = {"safety": ev("safety", EvidenceState.UNDETERMINED)}
    binding = request_permission("naya-4", "investigation", Operation.INSPECT,
                                 evidence, influences="incident report")
    assert binding.identity == "naya-4"
    derived = derive("incident-summary", list(evidence.values()))
    assert derived.derived_from_undetermined is True
    assert derived.undetermined_sources == ["safety"]


def test_use_time_binding_drift_fails_closed():
    evidence = {"safety": ev("safety", EvidenceState.UNDETERMINED)}
    binding = request_permission("naya-4", "investigation", Operation.INSPECT,
                                 evidence, influences="incident report")
    # Same binding at use: fine.
    assert check_use(binding, "naya-4", "investigation", "incident report")
    # Different purpose at use: fail closed.
    with pytest.raises(UnknownGuardRefusal) as e:
        check_use(binding, "naya-4", "production deploy", "incident report")
    assert e.value.code == USE_BINDING_VIOLATION


def test_marker_propagates_through_derivation():
    inputs = [ev("a", EvidenceState.CONFIRMED),
              ev("b", EvidenceState.UNDETERMINED)]
    d = derive("lesson-note", inputs)
    assert d.derived_from_undetermined
    # Clean inputs: no marker.
    d2 = derive("lesson-note-2", [ev("a", EvidenceState.CONFIRMED)])
    assert not d2.derived_from_undetermined
