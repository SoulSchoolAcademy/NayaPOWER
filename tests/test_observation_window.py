"""T-07: delayed-harm observation windows with stop conditions.

Proves the machine form of Naya 1's Law 11 intel: "Observation windows +
stop conditions established BEFORE execution. Monitoring failure = pause
rollout. Contradictory later evidence reopens outcomes."

Two layers tested:
  1. kernel/protocol/observation_window.py — the mechanism itself
     (declaration validation, registry authority, review semantics).
  2. kernel/act_pipeline.py wiring — the pipeline actually walks through
     the doors (plan gate + execution door). The library existing is not
     enough.
"""
import dataclasses

import pytest

from kernel import act_pipeline as ap
from kernel.protocol import observation_window as ow
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


# --- fixtures ---------------------------------------------------------------

def _profile():
    return QualityProfile(profile_id="obs-window-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _window(window_id="w1", **kw):
    base = dict(
        window_id=window_id,
        action="naya_node_apply",
        actor_id="naya-test",
        declared_at=NOW - 10,
        window_end=NOW + 300,
        review_dates=(NOW + 100, NOW + 200),
        indicators=(ow.ObservationIndicator(
            name="error_rate_5xx", low=0.1, high=5.0, unit="errors/min"),),
        stop_triggers=(ow.StopTrigger(
            name="error spike", indicator="error_rate_5xx",
            threshold=10.0, direction=ow.DIRECTION_ABOVE),),
        harm_type=ow.HARM_DELAYED,
    )
    base.update(kw)
    return ow.ObservationWindow(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.0, "evidence_sufficiency": 9.0,
                 "applicability": 9.0, "robustness": 9.0,
                 "reversibility": 9.0, "blast_containment": 9.0,
                 "simplicity": 9.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.9,
                    "applicability": 0.9, "robustness": 0.9,
                    "reversibility": 0.9, "blast_containment": 0.9,
                    "simplicity": 0.9},
        reversibility="REVERSIBLE",
        expected_outcome="done",
        proof_requirements=("receipt",),
        stakes="low",
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0, value_harm=1.0, value_cost=1.0, value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _execute(plan, authority=None, calls=None, registry=None, now=NOW):
    calls = calls if calls is not None else []
    auth = authority or _authority()
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: auth,
        now=now,
        profile=_profile(),
        observation_registry=registry,
    )
    return receipt, calls


# --- 1. declaration validation -------------------------------------------------

def test_valid_window_passes_validation():
    ok, problems = ow.validate_window(_window(), action="naya_node_apply", now=NOW)
    assert ok and problems == ()


def test_window_missing_indicators_rejected():
    ok, problems = ow.validate_window(
        _window(indicators=()), action="naya_node_apply", now=NOW)
    assert not ok and any("NO_INDICATORS" in p for p in problems)


def test_window_missing_review_dates_rejected():
    ok, problems = ow.validate_window(
        _window(review_dates=()), action="naya_node_apply", now=NOW)
    assert not ok and any("NO_REVIEW_DATES" in p for p in problems)


def test_window_missing_stop_triggers_rejected():
    ok, problems = ow.validate_window(
        _window(stop_triggers=()), action="naya_node_apply", now=NOW)
    assert not ok and any("NO_STOP_TRIGGERS" in p for p in problems)


def test_window_declared_in_future_rejected():
    # Observation cannot be invented retroactively: a window declared
    # after plan time is invalid.
    ok, problems = ow.validate_window(
        _window(declared_at=NOW + 100), action="naya_node_apply", now=NOW)
    assert not ok and any("DECLARED_IN_FUTURE" in p for p in problems)


def test_window_end_in_past_rejected():
    ok, problems = ow.validate_window(
        _window(window_end=NOW - 1), action="naya_node_apply", now=NOW)
    assert not ok and any("WINDOW_END_NOT_IN_FUTURE" in p for p in problems)


def test_trigger_referencing_unknown_indicator_rejected():
    bad = ow.StopTrigger(name="x", indicator="nope", threshold=1.0)
    ok, problems = ow.validate_window(
        _window(stop_triggers=(bad,)), action="naya_node_apply", now=NOW)
    assert not ok and any("TRIGGER_UNKNOWN_INDICATOR" in p for p in problems)


def test_window_bound_to_wrong_action_rejected():
    ok, problems = ow.validate_window(
        _window(), action="other_action", now=NOW)
    assert not ok and any("ACTION_MISMATCH" in p for p in problems)


# --- 2. registry authority ----------------------------------------------------

def test_duplicate_window_id_rejected():
    reg = ow.ObservationRegistry()
    reg.declare(_window("w1"))
    with pytest.raises(ValueError):
        reg.declare(_window("w1"))


def test_window_record_is_frozen():
    w = _window()
    with pytest.raises(dataclasses.FrozenInstanceError):
        w.status = ow.STATUS_ACTIVE  # type: ignore[misc]


def test_no_public_status_setter_on_registry():
    reg = ow.ObservationRegistry()
    assert not hasattr(reg, "set_status")
    assert not hasattr(reg, "status")


# --- 3. review semantics -------------------------------------------------------

def test_monitoring_failure_pauses():
    # A review date passes with no report filed -> PAUSE. Monitoring
    # failure = pause rollout. Never silently continue.
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    verdict = reg.review("w1", NOW + 150)
    assert verdict.verdict == ow.VERDICT_PAUSE
    assert verdict.status == ow.STATUS_PAUSED
    assert any("MONITORING_FAILURE" in r for r in verdict.reasons)


def test_paused_window_resumes_on_clean_report():
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    reg.review("w1", NOW + 150)  # -> PAUSED
    report = ow.ObservationReport(readings={"error_rate_5xx": 2.0})
    verdict = reg.review("w1", NOW + 160, report)
    assert verdict.verdict == ow.VERDICT_CONTINUE
    assert verdict.status == ow.STATUS_ACTIVE


def test_stop_trigger_fires_terminal():
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    report = ow.ObservationReport(readings={"error_rate_5xx": 50.0})
    verdict = reg.review("w1", NOW + 150, report)
    assert verdict.verdict == ow.VERDICT_STOP
    assert verdict.status == ow.STATUS_STOPPED
    assert any("STOP_TRIGGER_FIRED" in r for r in verdict.reasons)
    # Terminal: nothing resumes it, even with a clean report later.
    clean = ow.ObservationReport(readings={"error_rate_5xx": 1.0})
    again = reg.review("w1", NOW + 250, clean)
    assert again.verdict == ow.VERDICT_STOP
    assert again.status == ow.STATUS_STOPPED


def test_contradictory_evidence_reopens_not_stops():
    # Reading outside the expected band but below the stop trigger:
    # contradictory later evidence REOPENS the outcome; the window stays
    # ACTIVE so observation continues under the flag.
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    report = ow.ObservationReport(readings={"error_rate_5xx": 7.0})
    verdict = reg.review("w1", NOW + 150, report)
    assert verdict.verdict == ow.VERDICT_REOPEN
    assert verdict.status == ow.STATUS_ACTIVE
    assert any("CONTRADICTORY_EVIDENCE" in r for r in verdict.reasons)


def test_unmeasured_indicator_neither_fires_nor_clears():
    # The neutrality trap (T-06): a missing indicator is UNMEASURED, not
    # zero. A report with zero known-indicator readings is a monitoring
    # failure, not an observation — the window PAUSES and the review date
    # stays due. It can neither fire a trigger nor clear the date.
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    verdict = reg.review("w1", NOW + 150,
                         ow.ObservationReport(readings={"other": 1.0}))
    assert verdict.verdict == ow.VERDICT_PAUSE
    assert verdict.status == ow.STATUS_PAUSED
    assert any("MONITORING_FAILURE" in r for r in verdict.reasons)
    assert reg.due_review_dates("w1", NOW + 150) == (NOW + 100,)


def test_window_completes_clean():
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    reg.review("w1", NOW + 150,
               ow.ObservationReport(readings={"error_rate_5xx": 2.0}))
    reg.review("w1", NOW + 250,
               ow.ObservationReport(readings={"error_rate_5xx": 1.5}))
    verdict = reg.review("w1", NOW + 400)
    assert verdict.verdict == ow.VERDICT_COMPLETE
    assert verdict.status == ow.STATUS_COMPLETED


def test_review_unknown_window_pauses_fail_closed():
    reg = ow.ObservationRegistry()
    verdict = reg.review("nope", NOW + 150)
    assert verdict.verdict == ow.VERDICT_PAUSE
    assert ow.OBSERVATION_WINDOW_MISSING in verdict.reasons


# --- 4. execution door ----------------------------------------------------------

def test_door_permitted_when_active():
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    permitted, code = reg.execution_permitted("w1", "naya_node_apply", NOW)
    assert permitted and code == ""


def test_door_refused_when_paused_or_stopped():
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    reg.review("w1", NOW + 150)  # PAUSED: monitoring failure
    permitted, code = reg.execution_permitted("w1", "naya_node_apply", NOW + 150)
    assert not permitted and code == ow.OBSERVATION_PAUSED


def test_door_refused_for_wrong_action():
    reg = ow.ObservationRegistry()
    reg.declare(_window())
    permitted, code = reg.execution_permitted("w1", "other_action", NOW)
    assert not permitted and code == ow.OBSERVATION_WINDOW_INVALID


def test_door_refused_for_unknown_window():
    reg = ow.ObservationRegistry()
    permitted, code = reg.execution_permitted("nope", "naya_node_apply", NOW)
    assert not permitted and code == ow.OBSERVATION_WINDOW_MISSING


# --- 5. plan_action gate --------------------------------------------------------

def test_delayed_harm_without_window_refused_at_plan():
    plan, receipt = ap.plan_action(
        _authority(), [_candidate("p1", delayed_harm=True)],
        _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_OBSERVATION_WINDOW_REQUIRED in receipt.codes


def test_delayed_harm_with_valid_window_accepted():
    reg = ow.ObservationRegistry()
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True, observation_window=_window())],
        _profile(), now=NOW, observation_registry=reg)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"
    joined = " ".join(receipt.evidence)
    assert "w1" in joined and "review_dates" in joined
    assert reg.get("w1") is not None  # registered for the execution door


def test_delayed_harm_with_future_declared_window_refused():
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True,
                    observation_window=_window(declared_at=NOW + 100))],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_OBSERVATION_WINDOW_REQUIRED in receipt.codes


def test_delayed_harm_excluded_but_clean_candidate_proceeds():
    delayed = _candidate("p-delayed", delayed_harm=True)  # no window
    clean = _candidate("p-clean")
    plan, receipt = ap.plan_action(
        _authority(), [delayed, clean], _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-clean"
    joined = " ".join(receipt.evidence)
    assert "p-delayed" in joined and "observation" in joined


# --- 6. execute_plan door --------------------------------------------------------

def test_execute_refused_without_registry():
    plan, _ = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True, observation_window=_window())],
        _profile(), now=NOW)
    receipt, calls = _execute(plan, registry=None)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_OBSERVATION_REGISTRY_UNAVAILABLE in receipt.codes
    assert calls == []  # executor never fired


def test_execute_refused_when_window_paused():
    reg = ow.ObservationRegistry()
    plan, _ = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True, observation_window=_window())],
        _profile(), now=NOW, observation_registry=reg)
    reg.review("w1", NOW + 150)  # monitoring failure -> PAUSED
    receipt, calls = _execute(plan, registry=reg, now=NOW + 150)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_OBSERVATION_PAUSED in receipt.codes
    assert calls == []


def test_execute_refused_when_window_stopped():
    reg = ow.ObservationRegistry()
    plan, _ = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True, observation_window=_window())],
        _profile(), now=NOW, observation_registry=reg)
    reg.review("w1", NOW + 150,
               ow.ObservationReport(readings={"error_rate_5xx": 50.0}))
    receipt, calls = _execute(plan, registry=reg, now=NOW + 150)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_OBSERVATION_STOPPED in receipt.codes
    assert calls == []


def test_execute_allowed_when_window_active():
    reg = ow.ObservationRegistry()
    plan, _ = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True, observation_window=_window())],
        _profile(), now=NOW, observation_registry=reg)
    receipt, calls = _execute(plan, registry=reg)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == [plan.plan_id]


def test_execute_refused_on_retroactive_declaration():
    # Sabotage: a hand-crafted plan whose window was declared AFTER the
    # plan. The door must catch the retroactive declaration even when the
    # registry holds the window as ACTIVE.
    reg_plan = ow.ObservationRegistry()
    plan, _ = ap.plan_action(
        _authority(),
        [_candidate("p1", delayed_harm=True, observation_window=_window())],
        _profile(), now=NOW, observation_registry=reg_plan)
    assert plan is not None
    reg_exec = ow.ObservationRegistry()
    late = _window(declared_at=NOW + 50)  # after plan time NOW
    reg_exec.declare(late)
    tampered = dataclasses.replace(plan.chosen, observation_window=late)
    plan = dataclasses.replace(plan, chosen=tampered)
    receipt, calls = _execute(plan, registry=reg_exec)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_OBSERVATION_WINDOW_INVALID in receipt.codes
    assert calls == []


def test_non_delayed_candidate_unaffected_by_observation_door():
    # A candidate with delayed_harm=False flows through exactly as before:
    # no registry needed, no window needed.
    plan, _ = ap.plan_action(
        _authority(), [_candidate("p1")], _profile(), now=NOW)
    receipt, calls = _execute(plan, registry=None)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == [plan.plan_id]
