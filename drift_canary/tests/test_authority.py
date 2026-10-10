"""Tests: evidence access & authority governance — incl. adversarial tests."""
from ..authority import (
    CapabilityGrant, AccessDecision, UndeterminedProvenance, UseTimeCheck,
    CAPABILITIES, ROLES, NODE_AUTHORITY, ADVERSARIAL_TESTS,
)


def _grant(role, capability, assessment_holder="INC-1", evidence_version="v7",
           purpose="diagnose-failure", operation="read", expires_at=""):
    return CapabilityGrant(
        grant_id="g1", identity="agent-1", role=role, capability=capability,
        evidence_ref="FAMILY-B", evidence_version=evidence_version,
        purpose=purpose, project="NayaNET", operation=operation,
        expires_at=expires_at)


def test_five_capabilities_distinct():
    assert CAPABILITIES == ("inspect", "analyze", "test", "certify", "act")


def test_researcher_may_investigate_but_not_certify_undetermined():
    dec = AccessDecision(grant=_grant("researcher", "analyze"),
                         evidence_assessment="possibly_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "PERMIT"
    dec = AccessDecision(grant=_grant("researcher", "certify"),
                         evidence_assessment="possibly_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "DENY"


def test_verifier_may_investigate_but_not_count_as_independent_proof():
    dec = AccessDecision(grant=_grant("independent_verifier", "certify"),
                         evidence_assessment="possibly_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == \
        "DENY_AS_INDEPENDENT_PROOF"


def test_executor_needs_law_receipt_and_current_eligibility():
    dec = AccessDecision(grant=_grant("executor", "act"),
                         evidence_assessment="independently_cleared")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == \
        "PERMIT_ONLY_WITH_LAW_RECEIPT_AND_CURRENT_ELIGIBILITY"


def test_cleared_evidence_certify_opens_act_still_needs_law():
    dec = AccessDecision(grant=_grant("researcher", "certify"),
                         evidence_assessment="independently_cleared")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "PERMIT"
    dec = AccessDecision(grant=_grant("researcher", "act"),
                         evidence_assessment="independently_cleared")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "DENY"


def test_expired_grant_is_dead():
    dec = AccessDecision(
        grant=_grant("researcher", "inspect", expires_at="2026-10-09T00:00:00Z"),
        evidence_assessment="possibly_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "DENY"


def test_confirmed_compromised_historical_reading_only():
    dec = AccessDecision(grant=_grant("researcher", "inspect"),
                         evidence_assessment="confirmed_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == \
        "PERMIT_LABELED_HISTORICAL"
    dec = AccessDecision(grant=_grant("builder", "test"),
                         evidence_assessment="confirmed_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "DENY"


# --- Adversarial test 1: purpose laundering via summary ---
def test_adv_purpose_laundering_via_summary():
    src = UndeterminedProvenance(artifact_ref="EVID-B-v3",
                                original_incident="CCI-017")
    summary = src.transform("SUMMARY-B")       # summarize
    successor_pkg = summary.transform("SPKG-B")  # embed in successor package
    assert successor_pkg.derived_from_undetermined is True
    assert successor_pkg.derivation_chain == ("EVID-B-v3", "SUMMARY-B")
    assert not successor_pkg.may_serve_as_independent_proof()
    # No wash cycle: re-summarizing never drops the marker.
    again = successor_pkg.transform("SUMMARY-B-2")
    assert again.derived_from_undetermined is True
    # Marker does not mean false — only cleared packet lifts it.
    cleared = successor_pkg.clear("CLEARED")
    assert cleared.may_serve_as_independent_proof()


# --- Adversarial test 2: role-switching for broader permissions ---
def test_adv_role_switching_strictest_bound_wins():
    # Same identity, two roles: verifier may inspect broadly, builder may test
    # in sandbox. Certify-as-independent-proof is denied in BOTH roles.
    for role in ("builder", "independent_verifier"):
        dec = AccessDecision(
            grant=_grant(role, "certify"),
            evidence_assessment="possibly_compromised")
        assert "DENY" in dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision
    # A capability granted under one purpose does not transfer to another:
    # scope keys differ by purpose and operation.
    g1 = _grant("researcher", "analyze", purpose="diagnose-failure",
                operation="read")
    g2 = _grant("researcher", "analyze", purpose="publish-benchmark",
                operation="read")
    assert g1.scope_key() != g2.scope_key()


# --- Adversarial test 3: stale cache at ACT ---
def test_adv_stale_cache_at_act_fails_closed():
    check = UseTimeCheck(
        claim_id="Q-AGG", evidence_refs=("FAMILY-B",),
        evidence_eligibility_version="elig-v3",   # cached before incident
        law_receipt="LAW-2026-1001",
        current_eligibility_version="elig-v4",    # current, post-incident
        revocation_state="SUSPENDED")
    result = check.evaluate()
    assert result["permitted"] is False
    assert "stale eligibility version" in result["reason"]


def test_adv_use_time_undetermined_lineage_denied():
    check = UseTimeCheck(
        claim_id="Q-AGG", evidence_refs=("FAMILY-B",),
        evidence_eligibility_version="elig-v4",
        law_receipt="LAW-2026-1001",
        current_eligibility_version="elig-v4",
        revocation_state="REQUALIFIED",
        undetermined_markers=("SPKG-B",))
    assert check.evaluate()["permitted"] is False


def test_adv_use_time_no_law_receipt_denied():
    check = UseTimeCheck(
        claim_id="Q-AGG", evidence_refs=("FAMILY-C",),
        evidence_eligibility_version="elig-v4",
        law_receipt="",   # no LAW authorization
        current_eligibility_version="elig-v4",
        revocation_state="REQUALIFIED")
    assert check.evaluate()["permitted"] is False
    assert "LAW receipt" in check.evaluate()["reason"]


def test_adv_use_time_permitted_path():
    check = UseTimeCheck(
        claim_id="Q-AGG", evidence_refs=("FAMILY-C",),
        evidence_eligibility_version="elig-v4",
        law_receipt="LAW-2026-1001",
        current_eligibility_version="elig-v4",
        revocation_state="REQUALIFIED")
    assert check.evaluate()["permitted"] is True


# --- Adversarial test 4: debug submitted as blind proof ---
def test_adv_debug_submitted_as_blind_proof_denied():
    # A sandbox diagnostic run (capability=test) can never upgrade itself to
    # certify: separate grants, and the test-capability grant's purpose
    # ("sandbox-diagnostic") does not authorize certification.
    test_grant = CapabilityGrant(
        grant_id="g-debug", identity="builder-1", role="builder",
        capability="test", evidence_ref="FAMILY-B", evidence_version="v3",
        purpose="sandbox-diagnostic", project="NayaNET", operation="run")
    certify_grant = CapabilityGrant(
        grant_id="g-cert", identity="builder-1", role="builder",
        capability="certify", evidence_ref="FAMILY-B", evidence_version="v3",
        purpose="sandbox-diagnostic", project="NayaNET", operation="run")
    assert test_grant.scope_key() != certify_grant.scope_key()
    dec = AccessDecision(grant=certify_grant,
                         evidence_assessment="possibly_compromised")
    assert dec.evaluate(now_iso="2026-10-10T18:00:00Z").decision == "DENY"


def test_node_separation_no_self_granted_authority():
    assert NODE_AUTHORITY["KNOW"].startswith("expose uncertainty")
    assert NODE_AUTHORITY["VERIFY"].startswith("investigate")
    assert NODE_AUTHORITY["LAW"].startswith("determine permission")
    assert NODE_AUTHORITY["ACT"].startswith("enforce current eligibility")
    assert set(NODE_AUTHORITY) == {"KNOW", "VERIFY", "LAW", "ACT"}
    assert len(ADVERSARIAL_TESTS) == 4
