"""Tests for drift_canary/fairness_audit.py — D28 independent audit protocol.

Principle under test: "every assumption earns its place or gets thrown
out" — four gates, all required, with the killer probe (two deliberately
unfair schedulers) as the non-circularity backstop.

Each negative test has a positive control. The killer test follows the
directive's case exactly: rig the assumption, watch the trace vanish,
remove the assumption, watch the counterexample come back.
"""
import pytest

from drift_canary.fairness_audit import (
    AUDIT_VERDICTS,
    GATES,
    AuditAssumption,
    AuditInputError,
    AuditVerdict,
    EvidenceLedger,
    EvidenceRecord,
    QualificationClaim,
    _filtered_starvation,
    audit_assumption_set,
    clear_lasso_cache,
    from_d27,
    killer_probe_traces,
    summarize,
)


@pytest.fixture(scope="module", autouse=True)
def _warm_cache():
    # One warm-up pays for every test: the model checker is deterministic.
    clear_lasso_cache()
    yield
    clear_lasso_cache()


def _ledger_with(*names):
    ledger = EvidenceLedger()
    for i, n in enumerate(names):
        ledger.record(EvidenceRecord(
            name=n, produced_by="independent-battery",
            produced_at=f"2026-10-11T00:00:{i:02d}Z",
            summary="independently produced evidence"))
    return ledger


def _assumption(aid, constraint="NONE", owner="ENVIRONMENT",
                status="JUSTIFIED", evidence=("EVID-1",), scope=True):
    return AuditAssumption(
        assumption_id=aid,
        statement=f"test assumption {aid}",
        owner=owner,
        status=status,
        justification=f"independent justification for {aid}",
        justification_evidence=tuple(evidence),
        model_constraint=constraint,
        in_qualification_scope=scope,
    )


def _claim(excluded=(), policy="STRONG", artifact="QUAL-RECEIPT-1",
           prop="STRONG_FAIRNESS"):
    return QualificationClaim(
        claim_id="QUAL-TEST-1",
        property_claimed=prop,
        scheduler_id="SCHED-X",
        qualification_artifact=artifact,
        prover_policy=policy,
        excluded_behaviors=tuple(excluded),
    )


# ---------------------------------------------------------------------------
# The probe itself must be armed (positive control for every killer test).
# ---------------------------------------------------------------------------
def test_killer_probe_armed():
    probes = killer_probe_traces()
    assert len(probes) == 2
    for kind, verdict, armed, lasso, reason in probes:
        assert armed, f"{kind} disarmed: {verdict} ({reason})"
        assert len(lasso.cycle) == 12


# ---------------------------------------------------------------------------
# THE KILLER TEST (directive's case): rig the assumption, the trace
# vanishes; the audit rejects at G1 — the exclusion was never
# independently proven.
# ---------------------------------------------------------------------------
def test_killer_rigged_assumption_rejected_at_g1():
    rigged = _assumption(
        "A-RIG", constraint="STABILIZED_ELIGIBILITY",
        evidence=("operator-workload-note",))  # NOT in the ledger
    ledger = _ledger_with("EVID-1")  # the note was never independently recorded
    claim = _claim(excluded=("BROKEN_SF:SF_ONLY_VIOLATION",))

    verdict = audit_assumption_set((rigged,), claim, ledger)

    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G1_INDEPENDENT_JUSTIFICATION"
    assert "operator-workload-note" in verdict.reason
    assert "independent ledger" in verdict.reason


def test_counterexample_returns_when_assumption_removed():
    # The directive's second movement: remove the assumption and the
    # counterexample comes back — now you fix the scheduler, not the model.
    starvation = _filtered_starvation("STRONG_FAIRNESS", (), "UNCONSTRAINED", 12)
    verdicts = {v for _, v in starvation}
    assert "SF_ONLY_VIOLATION" in verdicts, (
        "without the rigged assumption the intermittent-starvation trace "
        "must be visible again")
    assert "WF_VIOLATION" in verdicts


# ---------------------------------------------------------------------------
# Even with ledgered evidence, an unnamed deletion is rigging (G4).
# ---------------------------------------------------------------------------
def test_killer_with_ledger_but_unnamed_exclusion_rejected_at_g4():
    rigged = _assumption("A-RIG", constraint="STABILIZED_ELIGIBILITY")
    ledger = _ledger_with("EVID-1")
    claim = _claim(excluded=())  # prover never named the exclusion

    verdict = audit_assumption_set((rigged,), claim, ledger)

    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G4_NON_CIRCULARITY"
    assert "BROKEN_SF:SF_ONLY_VIOLATION" in verdict.reason


def test_legitimate_scoping_passes():
    # Positive control: the SAME assumption, independently evidenced AND
    # explicitly scoped in the claim, is legitimate — the audit passes.
    scoped = _assumption("A-SCOPE", constraint="STABILIZED_ELIGIBILITY")
    ledger = _ledger_with("EVID-1")
    claim = _claim(excluded=("BROKEN_SF:SF_ONLY_VIOLATION",))

    verdict = audit_assumption_set((scoped,), claim, ledger)

    assert verdict.kind == "AUDIT_PASSED", summarize(verdict)
    gates = {g: p for g, p, _ in verdict.gate_results}
    assert all(gates[g] for g in GATES)


# ---------------------------------------------------------------------------
# Circular-by-construction footprint: the assumption constrains scheduler
# behavior while the property IS scheduler behavior.
# ---------------------------------------------------------------------------
def test_circular_footprint_rejected_at_g1():
    circular = _assumption("A-CIRC", constraint="ELIGIBLE_IFF_SERVICED")
    ledger = _ledger_with("EVID-1")
    claim = _claim(excluded=("BROKEN_WF:WF_VIOLATION",
                             "BROKEN_SF:SF_ONLY_VIOLATION"))

    verdict = audit_assumption_set((circular,), claim, ledger)

    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G1_INDEPENDENT_JUSTIFICATION"
    assert "circular by construction" in verdict.reason


# ---------------------------------------------------------------------------
# Unsatisfiable assumption set: the qualification would be vacuous.
# ---------------------------------------------------------------------------
def test_contradictory_assumption_rejected_at_g2():
    impossible = _assumption("A-VAC", constraint="CONTRADICTORY")
    ledger = _ledger_with("EVID-1")
    claim = _claim()

    verdict = audit_assumption_set((impossible,), claim, ledger)

    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G2_SATISFIABILITY"
    assert "vacuously" in verdict.reason


# ---------------------------------------------------------------------------
# Minimal sufficiency: a decorative assumption earns no place.
# ---------------------------------------------------------------------------
def test_redundant_assumption_flagged():
    scoped = _assumption("A-SCOPE", constraint="STABILIZED_ELIGIBILITY")
    decorative = _assumption("A-DECO", constraint="NONE")  # changes nothing
    ledger = _ledger_with("EVID-1")
    claim = _claim(excluded=("BROKEN_SF:SF_ONLY_VIOLATION",))

    verdict = audit_assumption_set((scoped, decorative), claim, ledger)

    assert verdict.kind == "REDUNDANT_ASSUMPTIONS"
    assert verdict.failed_gate == "G3_MINIMAL_SUFFICIENCY"
    assert "A-DECO" in verdict.reason
    assert "A-SCOPE" not in verdict.reason  # the load-bearing one is kept


def test_out_of_scope_documentary_exempt():
    # Positive control: a documentary assumption relied upon by OTHER
    # components (D27's relied_upon_by) is exempt from G3 — but still
    # faces G1/G2/G4.
    scoped = _assumption("A-SCOPE", constraint="STABILIZED_ELIGIBILITY")
    documentary = _assumption("A-DOC", constraint="NONE", scope=False)
    ledger = _ledger_with("EVID-1")
    claim = _claim(excluded=("BROKEN_SF:SF_ONLY_VIOLATION",))

    verdict = audit_assumption_set((scoped, documentary), claim, ledger)

    assert verdict.kind == "AUDIT_PASSED", summarize(verdict)


# ---------------------------------------------------------------------------
# G1 structural rejections.
# ---------------------------------------------------------------------------
def test_proposed_status_rejected():
    a = _assumption("A-PROP", status="PROPOSED")
    verdict = audit_assumption_set((a,), _claim(), _ledger_with("EVID-1"))
    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G1_INDEPENDENT_JUSTIFICATION"
    assert "PROPOSED" in verdict.reason


def test_scheduler_owned_assumption_rejected():
    a = _assumption("A-SELF", owner="SCHEDULER")
    verdict = audit_assumption_set((a,), _claim(), _ledger_with("EVID-1"))
    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G1_INDEPENDENT_JUSTIFICATION"
    assert "SCHEDULER" in verdict.reason


def test_self_justification_rejected():
    # The verdict being audited cannot justify the assumptions it rests on.
    a = _assumption("A-SELFJUST", evidence=("QUAL-RECEIPT-1",))
    ledger = _ledger_with("QUAL-RECEIPT-1")
    verdict = audit_assumption_set((a,), _claim(), ledger)
    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G1_INDEPENDENT_JUSTIFICATION"
    assert "itself" in verdict.reason


def test_environment_footprint_needs_environment_owner():
    a = _assumption("A-WRONG", constraint="STABILIZED_ELIGIBILITY",
                    owner="WORKER")
    verdict = audit_assumption_set((a,), _claim(), _ledger_with("EVID-1"))
    assert verdict.kind == "REJECTED"
    assert verdict.failed_gate == "G1_INDEPENDENT_JUSTIFICATION"


# ---------------------------------------------------------------------------
# Positive controls: the honest cases pass.
# ---------------------------------------------------------------------------
def test_empty_assumption_set_passes():
    verdict = audit_assumption_set((), _claim(), _ledger_with())
    assert verdict.kind == "AUDIT_PASSED", summarize(verdict)


def test_claim_not_established():
    # The prover's own check fails on its own terms: nothing to audit.
    claim = _claim(policy="UNCONSTRAINED")
    verdict = audit_assumption_set((), claim, _ledger_with())
    assert verdict.kind == "CLAIM_NOT_ESTABLISHED"
    assert "own assumptions" in verdict.reason or "own terms" in verdict.reason


# ---------------------------------------------------------------------------
# Fail-closed inputs.
# ---------------------------------------------------------------------------
def test_unknown_constraint_fail_closed():
    with pytest.raises(AssertionError):
        _assumption("A-BOGUS", constraint="NO_SUCH_CONSTRAINT")


def test_duplicate_ids_rejected():
    a1 = _assumption("A-DUP")
    a2 = _assumption("A-DUP", constraint="STABILIZED_ELIGIBILITY")
    with pytest.raises(AuditInputError):
        audit_assumption_set((a1, a2), _claim(), _ledger_with("EVID-1"))


def test_from_d27_adapter():
    class FakeD27:
        id = "FA-A1"
        statement = "author-seat inference statement"

    adapted = from_d27(
        FakeD27(), owner="ENVIRONMENT", status="JUSTIFIED",
        justification="measured, not asserted",
        justification_evidence=("EVID-1",),
        in_qualification_scope=False,
    )
    assert isinstance(adapted, AuditAssumption)
    assert adapted.assumption_id == "FA-A1"
    assert adapted.in_qualification_scope is False

    with pytest.raises(AuditInputError):
        from_d27(FakeD27(), owner="ENVIRONMENT", status="JUSTIFIED",
                 justification="", justification_evidence=("EVID-1",))


def test_verdicts_never_collapse():
    assert len(set(AUDIT_VERDICTS)) == 4
    v = AuditVerdict(kind="AUDIT_PASSED", claim_id="Q",
                     gate_results=tuple(), model_depth=12)
    text = summarize(v)
    assert "AUDIT_PASSED" in text and "model depth 12" in text
    # A rejection names its gate; it is never a bare failure.
    r = AuditVerdict(kind="REJECTED", claim_id="Q", failed_gate="G1_X",
                     reason="why", gate_results=(("G1_X", False, "why"),))
    assert "G1_X" in summarize(r)
