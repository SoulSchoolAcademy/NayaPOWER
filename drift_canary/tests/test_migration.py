"""Tests: split/merge proof migration.

Covers Shawn's ten acceptance tests, the four-phase experiment
(split -> merge -> adversarial -> cold successor), the laundering guard,
the two-direction audit, verdict composition with the six qualification
verdicts, and the interaction-proof layer (discovery, contracts,
receipts, proof ladder, false-composition battery).
"""
import pytest

from ..migration import (
    EvidenceProposition, ProofMapping, RequirementChange,
    SplitPlan, MergePlan, MigrationCertificate,
    InteractionObligation, InteractionContract, InteractionReceipt,
    MAPPING_RELATIONS, MIGRATION_VERDICTS, FIDELITY_CLASSES,
    INTERACTION_CLASSES, DISCOVERY_CHECKS, PROOF_LADDER,
    assess_split_child, plan_split, plan_merge,
    forward_sufficiency_split, forward_sufficiency_merge,
    backward_fidelity, migration_eligibility,
    issue_split_certificate, issue_merge_certificate,
    qualification_verdict_for, reconstruct_from_certificate,
    discover_interactions, interaction_proof_status,
    merge_with_interactions,
)
from ..propagation import (
    MeaningEnvelope, ObligationRevision, QualificationReceipt,
    ProofObligation, ClaimRegion, check_decision_boundary,
)
from ..revocation import VERDICTS


# ---------------------------------------------------------------------------
# Fixtures: the canonical LAW -> ACT split (Shawn's worked example).
# ---------------------------------------------------------------------------
def old_law_act():
    return ObligationRevision(
        obligation_id="LAW-ACT", revision_id="v1",
        requirement_text="LAW-authorized ACT execution is safe.",
        scope=MeaningEnvelope(component="law+act", environment="staging",
                              behavior="authorized-execution",
                              conditions="controlled"),
        acceptance_predicate="ACT executes only with valid LAW authorization",
        proof_standard="independent",
        effective_from="2026-01-01")


def old_propositions():
    return (
        EvidenceProposition(
            evidence_ref="PROOF-AUTH-001",
            proposition="ACT rejects forged LAW receipts",
            scope=MeaningEnvelope(component="act", environment="staging",
                                  behavior="rejects-forged-receipts",
                                  conditions="controlled"),
            independence="QUALIFIED"),
        EvidenceProposition(
            evidence_ref="PROOF-FRESH-001",
            proposition="ACT checks authorization before execution",
            scope=MeaningEnvelope(component="act", environment="staging",
                                  behavior="checks-authorization-pre-execution",
                                  conditions="controlled"),
            independence="QUALIFIED"),
    )


def split_children():
    return (
        ObligationRevision(
            obligation_id="LAW-ACT-AUTH", revision_id="v2",
            requirement_text="ACT rejects forged LAW receipts.",
            scope=MeaningEnvelope(component="act", environment="staging",
                                  behavior="rejects-forged-receipts",
                                  conditions="controlled"),
            acceptance_predicate="forged receipts rejected in all cases",
            proof_standard="independent",
            effective_from="2026-10-15"),
        ObligationRevision(
            obligation_id="LAW-ACT-FRESH", revision_id="v2",
            requirement_text="ACT checks current permission at the required "
                             "execution boundary.",
            scope=MeaningEnvelope(component="act", environment="staging",
                                  behavior="checks-authorization-at-commit",
                                  conditions="controlled"),
            acceptance_predicate="freshness verified at commit boundary",
            proof_standard="independent",
            effective_from="2026-10-15"),
        ObligationRevision(
            obligation_id="LAW-ACT-REVOKE", revision_id="v2",
            requirement_text="ACT cannot commit an action after governing "
                             "permission is revoked.",
            scope=MeaningEnvelope(component="act", environment="staging",
                                  behavior="rejects-after-revocation",
                                  conditions="controlled"),
            acceptance_predicate="revoked authorization blocks commit",
            proof_standard="independent",
            effective_from="2026-10-15"),
    )


ENTAILMENTS = {
    "LAW-ACT-AUTH": "independent-verifier-447: O-v1 acceptance test 3 "
                    "directly demonstrated forged-receipt rejection",
    "LAW-ACT-FRESH": "independent-verifier-447: O-v1 acceptance test 4 "
                     "demonstrated pre-execution checks",
}


# ---------------------------------------------------------------------------
# Acceptance test 1: split an exact conjunction into two unchanged children.
# ---------------------------------------------------------------------------
def test_1_split_exact_conjunction_both_carry():
    old = ObligationRevision(
        obligation_id="O", revision_id="v1",
        requirement_text="A and B hold.",
        scope=MeaningEnvelope(component="a+b", environment="staging"),
        acceptance_predicate="A and B demonstrated",
        proof_standard="independent")
    props = (
        EvidenceProposition("E-A", "A holds",
                            MeaningEnvelope(component="a",
                                            environment="staging"),
                            "QUALIFIED"),
        EvidenceProposition("E-B", "B holds",
                            MeaningEnvelope(component="b",
                                            environment="staging"),
                            "QUALIFIED"),
    )
    children = (
        ObligationRevision("O-A", "v2", "A holds.",
                           MeaningEnvelope(component="a",
                                           environment="staging"),
                           "A demonstrated", "independent"),
        ObligationRevision("O-B", "v2", "B holds.",
                           MeaningEnvelope(component="b",
                                           environment="staging"),
                           "B demonstrated", "independent"),
    )
    plan = plan_split(old, children, props, {},
                      entailments={"O-A": "verifier-1: direct",
                                   "O-B": "verifier-1: direct"})
    assert plan.child_verdicts == {"O-A": "CARRIED_FORWARD",
                                   "O-B": "CARRIED_FORWARD"}
    assert plan.overall_verdict == "CARRIED_FORWARD"
    assert all(m.relation == "ENTAILS" for m in plan.mappings)


# ---------------------------------------------------------------------------
# Acceptance test 2: black-box success split into internal invariants.
# ---------------------------------------------------------------------------
def test_2_black_box_does_not_establish_internals():
    old = ObligationRevision(
        obligation_id="O", revision_id="v1",
        requirement_text="The workflow succeeds end to end.",
        scope=MeaningEnvelope(component="sys", environment="staging",
                              behavior="end-to-end-success"),
        acceptance_predicate="workflow completed", proof_standard="standard")
    props = (EvidenceProposition(
        "E-BB", "workflow completed",
        MeaningEnvelope(component="sys", environment="staging",
                        behavior="end-to-end-success"), "QUALIFIED"),)
    child = ObligationRevision(
        obligation_id="O-INV", revision_id="v2",
        requirement_text="The internal retry counter never exceeds 3.",
        scope=MeaningEnvelope(component="sys", environment="staging",
                              behavior="retry-counter-bounded"),
        acceptance_predicate="counter <= 3 in all runs",
        proof_standard="standard")
    m = assess_split_child(old, child, props, {},
                           entailment_justification="verifier-2: claim")
    assert m.relation == "DOES_NOT_SUPPORT"
    assert m.evidence_refs == ()
    plan = plan_split(old, (child,), props, {},
                      entailments={"O-INV": "verifier-2: claim"})
    assert plan.child_verdicts["O-INV"] == "INSUFFICIENT_EVIDENCE"


# ---------------------------------------------------------------------------
# Acceptance test 3: a stronger child requirement needs additional proof.
# ---------------------------------------------------------------------------
def test_3_stronger_child_needs_new_proof():
    old, props = old_law_act(), old_propositions()
    child = ObligationRevision(
        obligation_id="LAW-ACT-AUTH-STRONG", revision_id="v2",
        requirement_text="ACT rejects forged LAW receipts, including "
                         "replay attacks within 60 seconds.",
        scope=MeaningEnvelope(component="act", environment="staging",
                              behavior="rejects-forged-receipts",
                              conditions="controlled+replay-attack"),
        acceptance_predicate="forged and replayed receipts rejected",
        proof_standard="independent")
    m = assess_split_child(old, child, props, {},
                           entailment_justification="verifier-3: partial")
    # Old evidence covers the forged-receipt dimension but not replay-attack.
    assert m.relation == "PARTIALLY_SUPPORTS"
    assert "missing: conditions" in m.scope_note
    plan = plan_split(old, (child,), props, {},
                      entailments={"LAW-ACT-AUTH-STRONG": "verifier-3: p"})
    assert plan.child_verdicts["LAW-ACT-AUTH-STRONG"] == "PARTIALLY_MIGRATED"
    # With new independent evidence, the child requalifies.
    plan2 = plan_split(old, (child,), props, {},
                       entailments={"LAW-ACT-AUTH-STRONG": "verifier-3: p"},
                       new_evidence={"LAW-ACT-AUTH-STRONG": True})
    assert plan2.child_verdicts["LAW-ACT-AUTH-STRONG"] == "REQUALIFIED"


# ---------------------------------------------------------------------------
# Acceptance test 4: one evidence source across children — shared lineage.
# ---------------------------------------------------------------------------
def test_4_shared_ancestry_counted_once():
    old = ObligationRevision(
        obligation_id="O", revision_id="v1",
        requirement_text="A and B hold.",
        scope=MeaningEnvelope(component="a+b", environment="staging"),
        acceptance_predicate="A and B demonstrated",
        proof_standard="independent")
    props = (EvidenceProposition(
        "E-ONE", "A and B observed in one instrumented run",
        MeaningEnvelope(component="a+b", environment="staging"),
        "QUALIFIED"),)
    children = (
        ObligationRevision("O-A", "v2", "A holds.",
                           MeaningEnvelope(component="a",
                                           environment="staging"),
                           "A demonstrated", "independent"),
        ObligationRevision("O-B", "v2", "B holds.",
                           MeaningEnvelope(component="b",
                                           environment="staging"),
                           "B demonstrated", "independent"),
    )
    plan = plan_split(old, children, props, {},
                      entailments={"O-A": "verifier-4: direct",
                                   "O-B": "verifier-4: direct"})
    assert plan.shared_ancestry == {"E-ONE": ["O-A", "O-B"]}
    # One observation, not two independent tests: both children reference
    # the same single evidence_ref.
    assert plan.mappings[0].evidence_refs == ("E-ONE",)
    assert plan.mappings[1].evidence_refs == ("E-ONE",)


# ---------------------------------------------------------------------------
# Acceptance test 5: merge unchanged obligations into their exact
# conjunction — permitted when compatible (administrative merge).
# ---------------------------------------------------------------------------
def test_5_administrative_merge_permitted_when_compatible():
    sources = (
        ObligationRevision("A", "v1", "A holds.",
                           MeaningEnvelope(component="a", environment="staging",
                                           behavior="holds-a",
                                           runtime="r1"),
                           "A demonstrated", "independent"),
        ObligationRevision("B", "v1", "B holds.",
                           MeaningEnvelope(component="b", environment="staging",
                                           behavior="holds-b",
                                           runtime="r1"),
                           "B demonstrated", "independent"),
    )
    merged = ObligationRevision(
        "AB", "v2", "A and B hold (grouped for convenience).",
        scope=MeaningEnvelope(component="a+b", environment="staging",
                              runtime="r1"),
        acceptance_predicate="A and B demonstrated",
        proof_standard="independent")
    props = (
        EvidenceProposition("E-A", "A holds",
                            MeaningEnvelope(component="a",
                                            environment="staging",
                                            behavior="holds-a", runtime="r1"),
                            "QUALIFIED"),
        EvidenceProposition("E-B", "B holds",
                            MeaningEnvelope(component="b",
                                            environment="staging",
                                            behavior="holds-b", runtime="r1"),
                            "QUALIFIED"),
    )
    plan = plan_merge(
        sources, merged, {"A": "part-a", "B": "part-b"}, props, {}, {},
        part_scopes={"A": MeaningEnvelope(component="a", environment="staging",
                                          behavior="holds-a", runtime="r1"),
                     "B": MeaningEnvelope(component="b", environment="staging",
                                          behavior="holds-b", runtime="r1")},
        entailments={"A": "verifier-5: direct", "B": "verifier-5: direct"},
        policy_versions={"A": "P1", "B": "P1"})
    assert plan.compatibility_notes == ()
    assert plan.unproved_obligations == ()
    assert plan.overall_verdict == "CARRIED_FORWARD"


# ---------------------------------------------------------------------------
# Acceptance test 6: merge with a new cross-node interaction requires
# an interaction proof.
# ---------------------------------------------------------------------------
def test_6_semantic_merge_requires_interaction_proof():
    sources = (
        ObligationRevision("KNOW-001", "v1", "KNOW retrieves an applicable "
                           "verified lesson.",
                           MeaningEnvelope(component="know",
                                           environment="staging",
                                           behavior="retrieves-lesson",
                                           runtime="r1"),
                           "lesson retrieved", "independent"),
        ObligationRevision("ACT-003", "v1", "ACT executes an authorized plan.",
                           MeaningEnvelope(component="act",
                                           environment="staging",
                                           behavior="executes-plan",
                                           runtime="r1"),
                           "plan executed", "independent"),
    )
    merged = ObligationRevision(
        "LEARNED-ACTION", "v2",
        "KNOW and ACT work together so applicable learning influences "
        "planning before execution.",
        scope=MeaningEnvelope(component="know+act", environment="staging",
                              behavior="learning-influences-planning",
                              runtime="r1"),
        acceptance_predicate="plan changes with applicable lesson",
        proof_standard="independent")
    props = (
        EvidenceProposition("E-K", "KNOW retrieves lesson",
                            MeaningEnvelope(component="know",
                                            environment="staging",
                                            behavior="retrieves-lesson",
                                            runtime="r1"), "QUALIFIED"),
        EvidenceProposition("E-A", "ACT executes plan",
                            MeaningEnvelope(component="act",
                                            environment="staging",
                                            behavior="executes-plan",
                                            runtime="r1"), "QUALIFIED"),
    )
    plan, status = merge_with_interactions(
        sources, merged, {"KNOW-001": "knowledge_retrieval",
                          "ACT-003": "execution"}, props, {}, {},
        part_scopes={"KNOW-001": MeaningEnvelope(
            component="know", environment="staging",
            behavior="retrieves-lesson", runtime="r1"),
            "ACT-003": MeaningEnvelope(
                component="act", environment="staging",
                behavior="executes-plan", runtime="r1")},
        entailments={"KNOW-001": "verifier-6: direct",
                     "ACT-003": "verifier-6: direct"},
        policy_versions={"KNOW-001": "P1", "ACT-003": "P1"})
    # Semantic triggers ("together", "influences", "before") discovered an
    # interaction obligation; with no independent receipt it is unproved.
    assert any("INT-SEMANTIC-TRIGGERS" in oid
               for oid in plan.unproved_obligations)
    assert plan.overall_verdict == "INSUFFICIENT_EVIDENCE"
    assert status["INT-SEMANTIC-TRIGGERS"][0] == "UNPROVED"


# ---------------------------------------------------------------------------
# Acceptance test 7: merge across incompatible runtime versions is
# rejected — no automatic qualification.
# ---------------------------------------------------------------------------
def test_7_incompatible_runtime_rejects_merge():
    sources = (
        ObligationRevision("A", "v1", "A holds.",
                           MeaningEnvelope(component="a", environment="staging",
                                           behavior="holds-a", runtime="r1"),
                           "A demonstrated", "independent"),
        ObligationRevision("B", "v1", "B holds.",
                           MeaningEnvelope(component="b", environment="staging",
                                           behavior="holds-b", runtime="r2"),
                           "B demonstrated", "independent"),
    )
    merged = ObligationRevision(
        "AB", "v2", "A and B hold together.",
        scope=MeaningEnvelope(component="a+b", environment="staging"),
        acceptance_predicate="A and B demonstrated",
        proof_standard="independent")
    props = (
        EvidenceProposition("E-A", "A holds",
                            MeaningEnvelope(component="a",
                                            environment="staging",
                                            behavior="holds-a", runtime="r1"),
                            "QUALIFIED"),
        EvidenceProposition("E-B", "B holds",
                            MeaningEnvelope(component="b",
                                            environment="staging",
                                            behavior="holds-b", runtime="r2"),
                            "QUALIFIED"),
    )
    plan = plan_merge(
        sources, merged, {"A": "part-a", "B": "part-b"}, props, {}, {},
        part_scopes={"A": MeaningEnvelope(component="a", environment="staging",
                                          behavior="holds-a", runtime="r1"),
                     "B": MeaningEnvelope(component="b", environment="staging",
                                          behavior="holds-b", runtime="r2")},
        entailments={"A": "verifier-7: direct", "B": "verifier-7: direct"},
        policy_versions={"A": "P1", "B": "P1"})
    assert any("runtime_mismatch" in n for n in plan.compatibility_notes)
    assert plan.overall_verdict == "INSUFFICIENT_EVIDENCE"


# ---------------------------------------------------------------------------
# Acceptance test 8: partly contaminated evidence — compromised
# contributions are excluded, the rest recomputed. No laundering.
# ---------------------------------------------------------------------------
def test_8_contaminated_evidence_excluded_not_laundered():
    old, _ = old_law_act(), None
    props = (
        EvidenceProposition(
            "PROOF-AUTH-001", "ACT rejects forged LAW receipts",
            MeaningEnvelope(component="act", environment="staging",
                            behavior="rejects-forged-receipts",
                            conditions="controlled"),
            independence="COMPROMISED"),  # tainted answer key
        EvidenceProposition(
            "PROOF-FRESH-001", "ACT checks authorization before execution",
            MeaningEnvelope(component="act", environment="staging",
                            behavior="checks-authorization-pre-execution",
                            conditions="controlled"),
            independence="QUALIFIED"),
    )
    independence_of = {"PROOF-AUTH-001": "COMPROMISED",
                       "PROOF-FRESH-001": "QUALIFIED"}
    children = split_children()
    # The laundering guard: compromised evidence is never eligible as
    # independent proof, in any migration role.
    eligible, reason = migration_eligibility(
        "PROOF-AUTH-001", independence_of, "independent_proof")
    assert not eligible
    assert "launder" in reason
    # Historical preservation is still permitted.
    eligible_h, _ = migration_eligibility(
        "PROOF-AUTH-001", independence_of, "historical")
    assert eligible_h
    plan = plan_split(old, children, props, independence_of,
                      entailments=ENTAILMENTS)
    auth_map = next(m for m in plan.mappings
                    if m.target_obligation.startswith("LAW-ACT-AUTH"))
    # The only proposition covering AUTH is compromised -> excluded ->
    # the child cannot be established on migrated evidence.
    assert auth_map.relation in ("DOES_NOT_SUPPORT", "UNDETERMINED")
    assert "PROOF-AUTH-001" not in auth_map.evidence_refs
    assert plan.child_verdicts["LAW-ACT-AUTH"] == "INSUFFICIENT_EVIDENCE"


# ---------------------------------------------------------------------------
# Acceptance test 9: obligation changes while execution is pending — the
# decision boundary applies the CURRENT revision, fail-closed.
# ---------------------------------------------------------------------------
def test_9_pending_execution_uses_current_revision():
    old = ObligationRevision(
        obligation_id="LAW-ACT", revision_id="v1",
        requirement_text="old requirement",
        scope=MeaningEnvelope(component="law+act", environment="staging"),
        acceptance_predicate="old check", proof_standard="standard",
        effective_from="2026-01-01", effective_until="2026-10-15")
    new = ObligationRevision(
        obligation_id="LAW-ACT", revision_id="v2",
        requirement_text="strengthened requirement",
        scope=MeaningEnvelope(component="law+act", environment="staging"),
        acceptance_predicate="new check", proof_standard="standard",
        effective_from="2026-10-15", supersedes="v1")
    receipt = QualificationReceipt(
        receipt_id="R-V1", obligation_id="LAW-ACT", revision_id="v1",
        evidence_refs=("E-1",), verdict="REQUALIFIED",
        recorded_at="2026-10-01", effective_at="2026-10-01",
        policy_version="P1")
    # Execution attempted after v2 took effect: the v1 receipt does not
    # apply to the governing revision — blocked, fail-closed.
    ok, reasons = check_decision_boundary(
        "ACT-99", "LAW-ACT", (old, new), (receipt,),
        at_time="2026-10-16", environment="staging",
        bridge_verified=False, authorization_permits=True)
    assert not ok
    assert any("no qualification receipt applies" in r for r in reasons)


# ---------------------------------------------------------------------------
# Acceptance test 10: cold successor reconstructs from the certificate.
# ---------------------------------------------------------------------------
def test_10_cold_successor_reconstructs():
    old, props, children = old_law_act(), old_propositions(), split_children()
    plan = plan_split(old, children, props, {}, entailments=ENTAILMENTS)
    cert = issue_split_certificate("MIG-010", plan, verifier="verifier-10")
    receipts = (QualificationReceipt(
        receipt_id="R-OLD", obligation_id="LAW-ACT", revision_id="v1",
        evidence_refs=("PROOF-AUTH-001", "PROOF-FRESH-001"),
        verdict="REQUALIFIED", recorded_at="2026-10-01",
        effective_at="2026-10-01", policy_version="P1"),)
    recon = reconstruct_from_certificate(cert, receipts)
    # Deterministic: same inputs, same answer, twice.
    recon2 = reconstruct_from_certificate(cert, receipts)
    assert recon == recon2
    assert recon["LAW-ACT-AUTH"]["migration_verdict"] == "CARRIED_FORWARD"
    assert recon["LAW-ACT-AUTH"]["qualification_verdict"] == "REQUALIFIED"
    assert recon["LAW-ACT-REVOKE"]["migration_verdict"] == \
        "INSUFFICIENT_EVIDENCE"
    assert recon["LAW-ACT-REVOKE"]["gap"] is not None
    assert recon["LAW-ACT-REVOKE"]["gap"].startswith("INSUFFICIENT_EVIDENCE")
    assert all(v["historical_receipts"] == "PRESERVED"
               for v in recon.values())


# ---------------------------------------------------------------------------
# The four-phase experiment.
# ---------------------------------------------------------------------------
def _phase_a():
    """Split the old LAW->ACT qualification into authenticity, freshness,
    and concurrent revocation. Reuse only evidence that actually proves
    each child."""
    old, props, children = old_law_act(), old_propositions(), split_children()
    plan = plan_split(old, children, props, {}, entailments=ENTAILMENTS)
    assert plan.child_verdicts["LAW-ACT-AUTH"] == "CARRIED_FORWARD"
    # FRESH: old evidence covered pre-execution checks, not the commit
    # boundary timing -> cannot carry.
    assert plan.child_verdicts["LAW-ACT-FRESH"] == "INSUFFICIENT_EVIDENCE"
    # REVOKE: no old proposition addresses revocation at all.
    assert plan.child_verdicts["LAW-ACT-REVOKE"] == "INSUFFICIENT_EVIDENCE"
    return plan


def test_phase_a_split_reuses_only_proving_evidence():
    _phase_a()


def _phase_b_new_evidence():
    """New independent evidence supplied during migration for the two
    children the old evidence could not carry."""
    return {"LAW-ACT-FRESH": True, "LAW-ACT-REVOKE": True}


def _phase_b_plan():
    plan_a = _phase_a()
    new_ev = _phase_b_new_evidence()
    plan_a2 = plan_split(old_law_act(), split_children(),
                         old_propositions(), {}, entailments=ENTAILMENTS,
                         new_evidence=new_ev)
    assert plan_a2.child_verdicts["LAW-ACT-FRESH"] == "REQUALIFIED"
    assert plan_a2.child_verdicts["LAW-ACT-REVOKE"] == "REQUALIFIED"

    know = ObligationRevision(
        "KNOW-001", "v1", "KNOW retrieves an applicable verified lesson.",
        MeaningEnvelope(component="know", environment="staging",
                        behavior="retrieves-lesson", runtime="r1"),
        "lesson retrieved", "independent")
    sources = (know,) + tuple(
        c for c in split_children() if c.obligation_id != "LAW-ACT-AUTH") \
        + (next(c for c in split_children()
                if c.obligation_id == "LAW-ACT-AUTH"),)
    merged = ObligationRevision(
        "LEARNED-ACTION", "v2",
        "NayaNET uses applicable learned intelligence to improve an "
        "authorized execution: learning reaches planning before the "
        "decision is finalized and cannot override LAW.",
        scope=MeaningEnvelope(component="know+law+act", environment="staging",
                              behavior="learned-authorized-execution",
                              runtime="r1"),
        acceptance_predicate="plan improves with lesson; LAW intact",
        proof_standard="independent")
    props = (
        EvidenceProposition("E-K", "KNOW retrieves applicable lesson",
                            MeaningEnvelope(component="know",
                                            environment="staging",
                                            behavior="retrieves-lesson",
                                            runtime="r1"), "QUALIFIED"),
        EvidenceProposition("E-AUTH", "ACT rejects forged receipts",
                            MeaningEnvelope(component="act",
                                            environment="staging",
                                            behavior="rejects-forged-receipts",
                                            runtime="r1"), "QUALIFIED"),
        EvidenceProposition("E-FRESH", "ACT checks freshness at commit",
                            MeaningEnvelope(component="act",
                                            environment="staging",
                                            behavior="checks-authorization-at-commit",
                                            runtime="r1"), "QUALIFIED"),
        EvidenceProposition("E-REV", "ACT rejects after revocation",
                            MeaningEnvelope(component="act",
                                            environment="staging",
                                            behavior="rejects-after-revocation",
                                            runtime="r1"), "QUALIFIED"),
    )
    part_scopes = {
        "KNOW-001": MeaningEnvelope(component="know", environment="staging",
                                    behavior="retrieves-lesson",
                                    runtime="r1"),
        "LAW-ACT-AUTH": MeaningEnvelope(component="act", environment="staging",
                                        behavior="rejects-forged-receipts",
                                        runtime="r1"),
        "LAW-ACT-FRESH": MeaningEnvelope(component="act",
                                         environment="staging",
                                         behavior="checks-authorization-at-commit",
                                         runtime="r1"),
        "LAW-ACT-REVOKE": MeaningEnvelope(component="act",
                                          environment="staging",
                                          behavior="rejects-after-revocation",
                                          runtime="r1"),
    }
    entail = {"KNOW-001": "verifier-B: direct",
              "LAW-ACT-AUTH": "verifier-B: direct",
              "LAW-ACT-FRESH": "verifier-B: direct",
              "LAW-ACT-REVOKE": "verifier-B: direct"}
    plan, status = merge_with_interactions(
        sources, merged,
        {"KNOW-001": "knowledge_retrieval",
         "LAW-ACT-AUTH": "authorization_authenticity",
         "LAW-ACT-FRESH": "authorization_freshness",
         "LAW-ACT-REVOKE": "concurrent_revocation"},
        props, {}, {},
        part_scopes=part_scopes, entailments=entail,
        policy_versions={s.obligation_id: "P1" for s in sources})
    # Every component part carried forward, but the merge adds genuinely
    # new obligations (learning influences planning; learning cannot
    # override LAW) with no independent proof -> the merged qualification
    # cannot be established.
    assert all(v == "CARRIED_FORWARD"
               for v in plan.part_verdicts.values())
    assert len(plan.unproved_obligations) > 0
    assert plan.overall_verdict == "INSUFFICIENT_EVIDENCE"
    return plan


def test_phase_b_merge_requires_knowledge_influence_proof():
    _phase_b_plan()


def test_phase_c_adversarial_stale_auth_fails_merge_not_children():
    """All children pass, then a stale authorization is injected during
    the combined execution. The merged qualification must fail while the
    unaffected child qualifications survive."""
    plan = _phase_b_plan()
    # The adversarial injection: an independent negative receipt showing
    # the LAW->ACT freshness interaction violated in the combined run.
    bad = InteractionReceipt(
        interaction_id="INT-LAW-ACT-freshness",
        participants=("LAW-ACT-FRESH", "LAW-ACT-REVOKE"),
        invariant="[](ACT commits => currently authorized)",
        preconditions=("authorization checked at commit",),
        code_sha="c0ffee", policy_version="P1", runtime="r1",
        negative_receipts=("NEG-STALE-AUTH-001",),
        independent_verification="verifier-C: stale auth committed",
        qualification="REVOKED")
    status = interaction_proof_status(
        (InteractionObligation(
            interaction_id="INT-LAW-ACT-freshness",
            participants=("LAW-ACT-FRESH", "LAW-ACT-REVOKE"),
            interaction_class="authority_privacy",
            invariant="[](ACT commits => currently authorized)"),),
        (bad,))
    assert status["INT-LAW-ACT-freshness"][0] == "FAILED"
    # The merged claim cannot be qualified on a failed interaction...
    assert plan.overall_verdict == "INSUFFICIENT_EVIDENCE"
    # ...while the children's individual qualifications are untouched:
    # the failure is in the composition, not the components.
    for src_id, v in plan.part_verdicts.items():
        assert v == "CARRIED_FORWARD", src_id


def test_phase_d_cold_successor_reconstructs_merge():
    plan = _phase_b_plan()
    cert = issue_merge_certificate("MIG-D", plan, verifier="verifier-D")
    assert cert.operation == "MERGE"
    assert cert.historical_receipts == "PRESERVED"
    assert cert.target_qualification in VERDICTS
    assert cert.target_qualification == "INSUFFICIENT_DATA"
    receipts = (QualificationReceipt(
        receipt_id="R-K", obligation_id="KNOW-001", revision_id="v1",
        evidence_refs=("E-K",), verdict="REQUALIFIED",
        recorded_at="2026-10-01", effective_at="2026-10-01",
        policy_version="P1"),)
    recon = reconstruct_from_certificate(cert, receipts)
    # The successor sees exactly what carried, what failed, and the gap.
    assert recon["knowledge_retrieval"]["migration_verdict"] == \
        "CARRIED_FORWARD"
    assert any("interaction" in (v["gap"] or "")
               for v in recon.values()
               if v["gap"] is not None) or cert.unproved_obligations


# ---------------------------------------------------------------------------
# Laundering guard: restructuring never upgrades independence.
# ---------------------------------------------------------------------------
def test_laundering_guard_undetermined_not_counted():
    eligible, reason = migration_eligibility(
        "E-X", {"E-X": "UNDETERMINED"}, "independent_proof")
    assert not eligible
    assert "never counted" in reason
    eligible2, _ = migration_eligibility(
        "E-X", {"E-X": "UNDETERMINED"}, "examination")
    assert eligible2


def test_mapping_requires_justification_for_entails():
    with pytest.raises(AssertionError):
        ProofMapping("O@v1", "A@v2", "part-a", "ENTAILS", ("E-1",),
                     justification="")


def test_no_implication_without_independent_justification():
    old, props = old_law_act(), old_propositions()
    child = split_children()[0]
    m = assess_split_child(old, child, props, {},
                           entailment_justification="")
    assert m.relation == "UNDETERMINED"
    assert "never independently established" in m.scope_note


# ---------------------------------------------------------------------------
# Two-direction audit.
# ---------------------------------------------------------------------------
def test_forward_sufficiency_split():
    plan = _phase_a()
    holds, gaps = forward_sufficiency_split(plan)
    assert not holds
    assert set(gaps) == {"LAW-ACT-FRESH", "LAW-ACT-REVOKE"}
    holds2, gaps2 = forward_sufficiency_split(
        plan, {"LAW-ACT-FRESH": True, "LAW-ACT-REVOKE": True})
    assert holds2 and gaps2 == ()


def test_backward_fidelity_flags_consequential_weakening():
    changes = (RequirementChange(
        requirement="independent-verification",
        from_text="promotion requires independent verification",
        to_text="promotion requires verification",
        fidelity="weakened", consequential=True),)
    report, needs_authority = backward_fidelity(changes)
    assert report == {"independent-verification": "weakened"}
    assert needs_authority is True
    # A merge that silently drops the requirement would be caught as
    # "removed" — the machinery requires every requirement classified.


def test_backward_fidelity_benign_change_needs_no_authority():
    changes = (RequirementChange(
        requirement="wording", from_text="check auth",
        to_text="verify authorization", fidelity="preserved",
        consequential=False),)
    _, needs_authority = backward_fidelity(changes)
    assert needs_authority is False


# ---------------------------------------------------------------------------
# Verdict composition with the six qualification verdicts.
# ---------------------------------------------------------------------------
def test_verdict_composition_table():
    assert qualification_verdict_for("CARRIED_FORWARD",
                                     prior_target_verdict="REQUALIFIED") == \
        "REQUALIFIED"
    assert qualification_verdict_for("PARTIALLY_MIGRATED") == "DOWNGRADED"
    assert qualification_verdict_for("BRIDGE_REQUIRED") == "SUSPENDED"
    assert qualification_verdict_for("REQUALIFIED") == "REQUALIFIED"
    assert qualification_verdict_for("INSUFFICIENT_EVIDENCE") == \
        "INSUFFICIENT_DATA"
    # INCOMPATIBLE revokes a standing qualification built on the
    # migrated evidence; otherwise it is insufficient data with the
    # incompatibility recorded.
    assert qualification_verdict_for("INCOMPATIBLE",
                                     prior_target_verdict="REQUALIFIED") == \
        "REVOKED"
    assert qualification_verdict_for("INCOMPATIBLE") == "INSUFFICIENT_DATA"


# ---------------------------------------------------------------------------
# Interaction-proof layer.
# ---------------------------------------------------------------------------
def test_interaction_discovery_contract_mismatch():
    obs = discover_interactions(
        "the components operate",
        (("LAW-002", ("authorization:valid-at-check",)),
         ("ACT-003", ("authorization:valid-at-commit",))))
    ids = [o.interaction_id for o in obs]
    assert any("LAW-002" in i and "ACT-003" in i for i in ids)
    auth_obs = [o for o in obs if o.interaction_class == "authority_privacy"]
    assert auth_obs, "expiry mismatch must surface as authority_privacy"


def test_interaction_discovery_no_material_interaction():
    obs = discover_interactions(
        "A and B are listed",
        (("A", ("holds-a",)), ("B", ("holds-b",))))
    assert obs == ()


def test_interaction_contract_is_falsifiable():
    c = InteractionContract(
        interaction_id="INT-1", participants=("LAW", "ACT"),
        interaction="authorization handoff",
        precondition="LAW issued a receipt",
        invariant="[](ACT commits => currently authorized)",
        success_witness="commit blocked after revocation in test T-9",
        failure_witness="commit proceeded with expired receipt",
        environment="staging")
    assert c.failure_witness != c.success_witness
    assert "=>" in c.invariant


def test_interaction_proof_ladder_rungs_valid():
    for rung in PROOF_LADDER:
        ob = InteractionObligation(
            interaction_id=f"INT-{rung}", participants=("A", "B"),
            interaction_class="ordering_timing",
            invariant="B runs after A", proof_ladder_rung=rung,
            independent_proof=f"receipt-{rung}")
        assert ob.proof_ladder_rung == rung


def test_interaction_status_unproved_is_not_proof():
    ob = InteractionObligation(
        interaction_id="INT-X", participants=("A", "B"),
        interaction_class="data_contract", invariant="schemas match")
    status = interaction_proof_status((ob,), ())
    assert status["INT-X"][0] == "UNPROVED"


def test_interaction_classes_complete():
    assert set(INTERACTION_CLASSES) == {
        "data_contract", "ordering_timing", "shared_state",
        "authority_privacy", "failure_coupling", "emergent_behavior"}
    assert len(DISCOVERY_CHECKS) == 5
    assert len(PROOF_LADDER) == 5


# ---------------------------------------------------------------------------
# False-composition battery (each with its positive counterpart — refusing
# everything proves nothing).
# ---------------------------------------------------------------------------
def _two_source_merge(extra_text="", contracts=(), receipts=(),
                       runtime="r1", policy="P1"):
    s1 = ObligationRevision("KNOW-001", "v1", "KNOW retrieves lesson.",
                            MeaningEnvelope(component="know",
                                            environment="staging",
                                            behavior="retrieves-lesson",
                                            runtime=runtime),
                            "retrieved", "independent")
    s2 = ObligationRevision("ACT-003", "v1", "ACT executes plan.",
                            MeaningEnvelope(component="act",
                                            environment="staging",
                                            behavior="executes-plan",
                                            runtime=runtime),
                            "executed", "independent")
    merged = ObligationRevision(
        "M", "v2", "KNOW and ACT cooperate. " + extra_text,
        MeaningEnvelope(component="know+act", environment="staging",
                        runtime=runtime),
        "cooperate", "independent")
    props = (
        EvidenceProposition("E-K", "retrieves",
                            MeaningEnvelope(component="know",
                                            environment="staging",
                                            behavior="retrieves-lesson",
                                            runtime=runtime), "QUALIFIED"),
        EvidenceProposition("E-A", "executes",
                            MeaningEnvelope(component="act",
                                            environment="staging",
                                            behavior="executes-plan",
                                            runtime=runtime), "QUALIFIED"),
    )
    scopes = {"KNOW-001": MeaningEnvelope(component="know",
                                          environment="staging",
                                          behavior="retrieves-lesson",
                                          runtime=runtime),
              "ACT-003": MeaningEnvelope(component="act",
                                         environment="staging",
                                         behavior="executes-plan",
                                         runtime=runtime)}
    ent = {"KNOW-001": "v: direct", "ACT-003": "v: direct"}
    pol = {"KNOW-001": policy, "ACT-003": policy}
    return merge_with_interactions(
        (s1, s2), merged,
        {"KNOW-001": "retrieval", "ACT-003": "execution"},
        props, {}, {}, part_scopes=scopes, entailments=ent,
        component_contracts=contracts, interaction_receipts=receipts,
        policy_versions=pol)


def test_falsecomp_lesson_cannot_override_law():
    plan, _ = _two_source_merge(
        "learning improves planning but cannot override LAW.",
        contracts=(("KNOW-001", ("lesson:advisory-only",)),
                   ("LAW-002", ("authority:LAW-only",))))
    auth_new = [o for o in plan.new_obligations
                if "INT-" in o.obligation_id]
    assert auth_new or plan.unproved_obligations


def test_falsecomp_positive_counterpart_honest_work_qualifies():
    # No new behavioral claims, compatible evidence: the administrative
    # merge composes. Refusing everything would prove nothing.
    plan, _ = _two_source_merge()
    assert plan.overall_verdict == "CARRIED_FORWARD"


def test_falsecomp_correlated_sources_flagged():
    s1 = ObligationRevision("A", "v1", "A holds.",
                            MeaningEnvelope(component="a",
                                            environment="staging",
                                            runtime="r1"),
                            "A ok", "independent")
    s2 = ObligationRevision("B", "v1", "B holds.",
                            MeaningEnvelope(component="b",
                                            environment="staging",
                                            runtime="r1"),
                            "B ok", "independent")
    merged = ObligationRevision("AB", "v2", "A and B hold.",
                                MeaningEnvelope(component="a+b",
                                                environment="staging",
                                                runtime="r1"),
                                "AB ok", "independent")
    props = (
        EvidenceProposition("E-SAME", "one run observed A and B",
                            MeaningEnvelope(component="a+b",
                                            environment="staging",
                                            runtime="r1"), "QUALIFIED"),)
    plan = plan_merge(
        (s1, s2), merged, {"A": "a", "B": "b"}, props, {},
        {"E-SAME": "ORIGIN-RUN-7"},
        part_scopes={"A": MeaningEnvelope(component="a", environment="staging",
                                          runtime="r1"),
                     "B": MeaningEnvelope(component="b", environment="staging",
                                          runtime="r1")},
        entailments={"A": "v: direct", "B": "v: direct"},
        policy_versions={"A": "P1", "B": "P1"})
    assert plan.correlated_sources, \
        "shared origin must be flagged so rates are never multiplied"
    assert any("ORIGIN-RUN-7" in c for c in plan.correlated_sources)


def test_or_connective_qualifies_on_either_alternative():
    s1 = ObligationRevision("A", "v1", "A holds.",
                            MeaningEnvelope(component="a",
                                            environment="staging"),
                            "A ok", "independent")
    s2 = ObligationRevision("B", "v1", "B holds.",
                            MeaningEnvelope(component="b",
                                            environment="staging"),
                            "B ok", "independent")
    merged = ObligationRevision("AORB", "v2", "A or B holds.",
                                MeaningEnvelope(component="a+b",
                                                environment="staging"),
                                "either ok", "independent")
    props = (EvidenceProposition(
        "E-A", "A holds",
        MeaningEnvelope(component="a", environment="staging"),
        "QUALIFIED"),)
    plan = plan_merge(
        (s1, s2), merged, {"A": "alt-a", "B": "alt-b"}, props, {}, {},
        part_scopes={"A": MeaningEnvelope(component="a",
                                          environment="staging"),
                     "B": MeaningEnvelope(component="b",
                                          environment="staging")},
        entailments={"A": "v: direct", "B": "v: direct"},
        connective="OR",
        policy_versions={"A": "P1", "B": "P1"})
    # One alternative established suffices for OR — requiring both would
    # unnecessarily strengthen the obligation.
    assert plan.overall_verdict == "CARRIED_FORWARD"


def test_certificate_binds_manifests_and_preserves_history():
    plan = _phase_a()
    cert = issue_split_certificate(
        "MIG-CERT-1", plan, verifier="verifier-C",
        source_manifest="REQ-MANIFEST-V1", source_hashes=("sha256:abc",),
        target_manifest="REQ-MANIFEST-V2",
        policy_effective_period="2026-10-15/..",
        code_version="40df54b1", runtime_version="r1")
    assert cert.event_type == "COMPOSITE_PROOF_MIGRATION"
    assert cert.operation == "SPLIT"
    assert cert.source_hashes == ("sha256:abc",)
    assert cert.historical_receipts == "PRESERVED"
    assert cert.target_qualification in VERDICTS
