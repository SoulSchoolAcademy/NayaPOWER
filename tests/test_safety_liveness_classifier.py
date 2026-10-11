"""D55 — Safe Recovery Holds vs. Liveness Failures: real tests + negative controls.

Every positive test has a sabotage twin: if the classifier cannot be broken by
the named mutation, the test is theater.
"""
import itertools
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from safety_liveness_classifier import (  # noqa: E402
    AuthState, Classification, Diagnosis, Event, Obligation, TriFact,
    ValidDisposition, SERVICE, PROGRESS,
    classify, escalate, trifacts, run_aer_live_001, run_history,
    verify_aer_live_001, main,
)


def svc(n=1, detail="heartbeat"):
    return [Event(SERVICE, f"{detail} #{i}") for i in range(1, n + 1)]


def prog(detail="state advanced"):
    return [Event(PROGRESS, detail)]


# ---------------------------------------------------------------------------
# Positive: tri-fact separation
# ---------------------------------------------------------------------------

def test_tri_fact_tracks_three_separate_facts():
    ob = Obligation("o", AuthState.GRANTED, svc(3) + prog())
    tf = trifacts(ob)
    assert (tf.enabled, tf.serviced, tf.progressed) == (True, True, True)


def test_heartbeat_is_service_never_progress():
    # Heartbeats — even many — establish S_o only. P_o stays False.
    ob = Obligation("o", AuthState.GRANTED, svc(50, detail="heartbeat"))
    tf = trifacts(ob)
    assert tf.serviced is True
    assert tf.progressed is False
    assert classify(ob).classification == Classification.RECOVERY_DEFECT


def test_enabled_requires_granted_auth():
    for auth, expected in [(AuthState.GRANTED, True),
                          (AuthState.WITHDRAWN, False),
                          (AuthState.MISSING_DECISION, False)]:
        ob = Obligation("o", auth, [])
        assert trifacts(ob).enabled is expected, auth


# ---------------------------------------------------------------------------
# Positive: AER-LIVE-001 three histories
# ---------------------------------------------------------------------------

def test_aer_live_001_control_is_healthy():
    results = run_aer_live_001()
    v = results["H1"]
    prim = next(d for d in v.diagnoses if d.obligation == "reconciliation-task")
    assert prim.classification == Classification.HEALTHY
    assert prim.tri_fact.progressed is True


def test_aer_live_001_defective_fails_progress_requirement():
    results = run_aer_live_001()
    v = results["H2"]
    prim = next(d for d in v.diagnoses if d.obligation == "committed-publication-replay")
    assert prim.classification == Classification.RECOVERY_DEFECT
    assert prim.tri_fact.serviced is True and prim.tri_fact.progressed is False


def test_aer_live_001_missing_decision_is_waiting_authority_not_starvation():
    results = run_aer_live_001()
    v = results["H3"]
    prim = next(d for d in v.diagnoses if d.obligation == "reconciliation-task")
    assert prim.classification == Classification.WAITING_AUTHORITY
    assert prim.classification != Classification.RECOVERY_DEFECT
    assert prim.classification != Classification.SCHEDULER_DEFECT


def test_authorization_stays_withdrawn_in_all_three_histories():
    results = run_aer_live_001()
    for hid, v in results.items():
        assert v.authorization_proof["retry-blocked-action"] == "withdrawn", hid


def test_three_simultaneous_truths_independently_classified():
    # The directive: retry correctly blocked + authorized reconciliation
    # runnable-and-ignored + committed publication replay lost — three things
    # true at once, each classified on its own facts.
    v = run_history("H2")
    by_name = {d.obligation: d for d in v.diagnoses}
    assert by_name["retry-blocked-action"].classification == Classification.VALID_HOLD
    assert by_name["retry-blocked-action"].scheduler_defect is True
    assert by_name["reconciliation-task"].classification == Classification.SCHEDULER_DEFECT
    assert by_name["committed-publication-replay"].classification == Classification.RECOVERY_DEFECT


def test_verify_aer_live_001_passes_on_real_classifier():
    assert verify_aer_live_001(run_aer_live_001()) == []


def test_escalation_changes_responsibility_never_safety():
    v = run_history("H2")
    d = next(x for x in v.diagnoses if x.obligation == "committed-publication-replay")
    esc = escalate(d, "incident-commander")
    assert esc.classification == d.classification
    assert esc.auth == d.auth == AuthState.GRANTED
    assert esc.tri_fact == d.tri_fact
    assert "incident-commander" in esc.note
    # input untouched
    assert "incident-commander" not in d.note


def test_valid_disposition_requires_evidence_or_reason():
    assert ValidDisposition("held", evidence="LAW decision L-1").is_valid()
    assert ValidDisposition("waiting", reason="no decision exists").is_valid()
    assert not ValidDisposition("held").is_valid()
    assert not ValidDisposition("held", evidence="   ").is_valid()


def test_cli_experiment_passes_fail_closed_exit_codes(tmp_path):
    r = subprocess.run([sys.executable, "tools/safety_liveness_classifier.py",
                        "--run-experiment"], capture_output=True, text=True,
                       cwd=Path(__file__).resolve().parent.parent)
    assert r.returncode == 0, r.stderr
    payload = json.loads(r.stdout)
    assert payload["experiment"] == "AER-LIVE-001"
    assert payload["pass"] is True
    assert payload["violations"] == []


def test_cli_exit_2_when_verification_fails(monkeypatch, capsys):
    # Fail-closed: if the experiment ever fails verification, the CLI must
    # exit 2 (not 0). Proven by feeding it the mutant's failing results.
    import safety_liveness_classifier as mod
    mutant_results = mod.run_aer_live_001(classifier=classify_progress_blind)
    assert mod.verify_aer_live_001(mutant_results, classifier=classify_progress_blind)
    monkeypatch.setattr(mod, "run_aer_live_001",
                        lambda classifier=mod.classify: mutant_results)
    rc = mod.main(["--run-experiment"])
    assert rc == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["pass"] is False
    assert payload["violations"]


# ---------------------------------------------------------------------------
# Negative controls: the directive-named adversarial mutation
# ---------------------------------------------------------------------------

def classify_progress_blind(ob: Obligation) -> Diagnosis:
    """MUTANT: the directive's named sabotage — progress-on-service check
    removed, so serviced implies progressed. Declares success from mere
    activity."""
    tf = trifacts(ob)
    blind = TriFact(tf.enabled, tf.serviced, progressed=tf.serviced or tf.progressed)
    base = classify(ob)
    if base.auth == AuthState.GRANTED and blind.progressed and not tf.progressed:
        return Diagnosis(ob.name, Classification.HEALTHY, blind, ob.auth,
                         note="MUTANT: success declared from mere activity")
    return base


def test_mutant_declares_success_from_mere_activity():
    # The mutant itself must exhibit the fraud: H2's defective publication
    # (5 heartbeats, zero progress) comes back HEALTHY.
    v = run_history("H2", classifier=classify_progress_blind)
    prim = next(d for d in v.diagnoses if d.obligation == "committed-publication-replay")
    assert prim.classification == Classification.HEALTHY
    assert prim.tri_fact.progressed is True  # fraud: no PROGRESS event exists


def test_verifier_catches_the_mutant():
    # The experiment harness must CATCH the mutant — not pass it.
    results = run_aer_live_001(classifier=classify_progress_blind)
    violations = verify_aer_live_001(results, classifier=classify_progress_blind)
    assert violations, "verifier failed to catch success-from-activity"
    assert any("H2" in v and "RECOVERY_DEFECT" in v for v in violations)


def test_heartbeat_fraud_fixture_never_healthy():
    ob = Obligation("fraud", AuthState.GRANTED, svc(100, detail="heartbeat"))
    assert classify(ob).classification != Classification.HEALTHY
    assert classify(ob).classification == Classification.RECOVERY_DEFECT


def test_always_pass_verdict_fails_verification():
    # A tampered verdict claiming everything healthy must not verify.
    results = run_aer_live_001()
    for v in results.values():
        for d in v.diagnoses:
            d.classification = Classification.HEALTHY
    violations = verify_aer_live_001(results)
    assert violations, "always-pass verdict slipped through verification"


def test_missing_proof_fails_verification():
    results = run_aer_live_001()
    results["H2"].authorization_proof = {}  # sabotage: proof stripped
    violations = verify_aer_live_001(results)
    # H2's retry proof is gone; the verifier must demand the proof, not just
    # scan it when present.
    assert any("H2" in v and "proof missing" in v for v in violations), violations
    # And the intact run still passes, proving the check ran rather than
    # always failing.
    assert verify_aer_live_001(run_aer_live_001()) == []


# ---------------------------------------------------------------------------
# Property: withdrawn auth is NEVER a liveness failure, over the full matrix
# ---------------------------------------------------------------------------

def test_withdrawn_never_liveness_failure_full_matrix():
    liveness_failures = {Classification.RECOVERY_DEFECT, Classification.SCHEDULER_DEFECT}
    for n_svc, n_prog in itertools.product([0, 1, 5], [0, 1]):
        ob = Obligation("m", AuthState.WITHDRAWN,
                        svc(n_svc) + ([Event(PROGRESS, "x")] * n_prog))
        got = classify(ob).classification
        assert got == Classification.VALID_HOLD, (n_svc, n_prog, got)
        assert got not in liveness_failures


def test_missing_decision_never_collapses_to_healthy_or_defect():
    for n_svc in (0, 3):
        ob = Obligation("m", AuthState.MISSING_DECISION, svc(n_svc))
        got = classify(ob).classification
        assert got == Classification.WAITING_AUTHORITY, (n_svc, got)


def test_granted_matrix_matches_spec():
    # (serviced, progressed) -> classification under GRANTED
    cases = {(False, False): Classification.SCHEDULER_DEFECT,
             (True, False): Classification.RECOVERY_DEFECT,
             (False, True): Classification.HEALTHY,
             (True, True): Classification.HEALTHY}
    for (n_svc, n_prog), expected in cases.items():
        events = svc(n_svc) + ([Event(PROGRESS, "x")] * n_prog)
        ob = Obligation("m", AuthState.GRANTED, events)
        assert classify(ob).classification == expected, (n_svc, n_prog)


def test_unknown_history_rejected():
    with pytest.raises(KeyError):
        run_history("H9")
