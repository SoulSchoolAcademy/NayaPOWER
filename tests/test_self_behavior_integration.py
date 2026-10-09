"""WO5b — SELF behavior integration: verified lessons change behavior patterns.

Module under test: kernel/self_integration.py + kernel/behavior_policy.py,
plus the ACT post-execution hook seam in kernel/act_pipeline.py.

Acceptance gates covered:
  - a valid verified lesson integrates and changes a subsequent decision in
    the same situation (before/after transcripts);
  - an invalid verifier chain is rejected and touches nothing;
  - the policy store is versioned and rollback restores prior behavior;
  - the ACT pipeline records completed executions as SELF experience.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.behavior_policy import BehaviorPolicyError, BehaviorPolicyStore
from kernel.self_integration import (
    IntegrationError,
    integrate_verified_lesson,
    lesson_from_evidence_row,
    load_active_lessons,
    make_act_experience_hook,
    validate_verifier_chain,
)
from kernel.self_node import JsonContinuityStore, RuntimeIdentity, SelfNode
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0
SITUATION = "dispatch:duplicate-learning-write"
DEFAULT_BEHAVIOR = "write the candidate row directly"
LESSON_BEHAVIOR = "run the admission gate before writing any candidate row"


def _valid_lesson(**kw):
    base = {
        "lesson_id": "SN-0601",
        "claim": "Unverified candidates must never enter the learning system",
        "situation": SITUATION,
        "prescribed_behavior": LESSON_BEHAVIOR,
        "doer": "naya-5",
        "scorer": "naya-1",
        "verifier": "naya-2",
        "verdict": "VERIFIED",
        "admission_admitted_as": "CANDIDATE",
    }
    base.update(kw)
    return base


def _booted_node(tmp_path):
    node = SelfNode(JsonContinuityStore(tmp_path / "self.json"))
    node.cold_boot(
        RuntimeIdentity("naya-2", "NayaPOWER", "naya"),
        "Preserve intelligence across Naya generations",
        "Prove verified lessons change behavior",
        "kernel",
    )
    return node


# ---------------- verifier chain ----------------

def test_verifier_chain_accepts_three_distinct_seats():
    validate_verifier_chain(doer="naya-5", scorer="naya-1", verifier="naya-2")


def test_verifier_chain_normalizes_identity_case_and_whitespace():
    # B6b contract: "Naya-5", "naya-5 " and "NAYA-5" are one seat.
    with pytest.raises(IntegrationError, match="verifier_equals_doer"):
        validate_verifier_chain(doer="Naya-5", scorer="naya-1", verifier="naya-5 ")


@pytest.mark.parametrize(
    "doer,scorer,verifier,code",
    [
        ("naya-5", "naya-5", "naya-2", "doer_equals_scorer"),
        ("naya-5", "naya-1", "naya-5", "verifier_equals_doer"),
        ("naya-5", "naya-1", "naya-1", "verifier_equals_scorer"),
    ],
)
def test_verifier_chain_rejects_collisions(doer, scorer, verifier, code):
    with pytest.raises(IntegrationError, match=code):
        validate_verifier_chain(doer=doer, scorer=scorer, verifier=verifier)


def test_verifier_chain_requires_all_three_identities():
    with pytest.raises(IntegrationError, match="verifier_required"):
        validate_verifier_chain(doer="naya-5", scorer="naya-1", verifier=" ")


# ---------------- lesson integration ----------------

def test_valid_lesson_integrates_and_changes_decision(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    assert store.current_version == 0

    receipt = integrate_verified_lesson(_valid_lesson(), store)

    assert receipt["status"] == "INTEGRATED"
    assert receipt["policy_version"] == 1
    assert receipt["prior_version"] == 0
    assert receipt["verifier_chain"] == "doer!=scorer!=verifier OK"

    advised = store.advise(SITUATION, DEFAULT_BEHAVIOR)
    assert advised["behavior"] == LESSON_BEHAVIOR
    assert advised["source"] == "lesson:SN-0601"
    assert advised["policy_version"] == 1


def test_integration_records_self_experience_when_node_given(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    node = _booted_node(tmp_path)
    receipt = integrate_verified_lesson(_valid_lesson(), store, self_node=node)
    # #2062 hardened record_experience: the raw-text legacy path is preserved
    # as PRESERVED_UNVERIFIED (it cannot masquerade as governed truth).
    assert receipt["experience_receipt"]["status"] == "PRESERVED_UNVERIFIED"
    assert node.state.experience_count == 1
    assert any("Unverified candidates must never enter" in k for k in node.state.known)


def test_invalid_verifier_chain_rejects_and_touches_nothing(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match="verifier_equals_doer"):
        integrate_verified_lesson(_valid_lesson(verifier="naya-5"), store)
    assert store.current_version == 0
    assert store.advise(SITUATION, DEFAULT_BEHAVIOR)["source"] == "default"


@pytest.mark.parametrize(
    "override,code",
    [
        ({"verdict": "NOT_VERIFIED"}, "lesson_not_verified"),
        ({"verdict": ""}, "lesson_not_verified"),
        ({"situation": " "}, "lesson_incomplete"),
        ({"prescribed_behavior": ""}, "lesson_incomplete"),
        ({"admission_admitted_as": "REJECTED"}, "lesson_not_admitted"),
        ({"doer": "naya-1", "scorer": "naya-1"}, "doer_equals_scorer"),
    ],
)
def test_invalid_lessons_reject_fail_closed(tmp_path, override, code):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(IntegrationError, match=code):
        integrate_verified_lesson(_valid_lesson(**override), store)
    assert store.current_version == 0


def test_integration_is_rejected_for_non_object(tmp_path):
    with pytest.raises(IntegrationError, match="lesson_must_be_object"):
        integrate_verified_lesson("not a lesson", BehaviorPolicyStore(tmp_path / "p.json"))


# ---------------- before / after / rollback transcript ----------------

def test_before_after_transcripts_prove_behavior_change_and_rollback(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    transcript = []

    before = store.advise(SITUATION, DEFAULT_BEHAVIOR)
    transcript.append(f"BEFORE  v{before['policy_version']} [{before['source']}]: {before['behavior']}")

    receipt = integrate_verified_lesson(_valid_lesson(), store)
    after = store.advise(SITUATION, DEFAULT_BEHAVIOR)
    transcript.append(f"AFTER   v{after['policy_version']} [{after['source']}]: {after['behavior']}")

    assert before["behavior"] == DEFAULT_BEHAVIOR
    assert before["source"] == "default"
    assert after["behavior"] == LESSON_BEHAVIOR
    assert after["source"] == "lesson:SN-0601"
    assert before["behavior"] != after["behavior"]

    rolled = store.rollback(0)
    restored = store.advise(SITUATION, DEFAULT_BEHAVIOR)
    transcript.append(
        f"ROLLBACK v{restored['policy_version']} [{restored['source']}]: {restored['behavior']}"
    )

    assert rolled == 2
    assert restored["behavior"] == DEFAULT_BEHAVIOR
    assert restored["source"] == "default"

    # The transcript is the proof artifact: three distinct decision states.
    assert len(transcript) == 3
    assert transcript[0] != transcript[1]
    assert transcript[2].startswith("ROLLBACK")


def test_version_history_is_append_only_and_retained(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    integrate_verified_lesson(_valid_lesson(), store)
    integrate_verified_lesson(_valid_lesson(lesson_id="SN-0602", situation="other"), store)
    store.rollback(1)
    history = store.history()
    assert [h["version"] for h in history] == [0, 1, 2, 3]
    assert [h["kind"] for h in history] == ["genesis", "integrate", "integrate", "rollback"]
    assert history[1]["lesson_id"] == "SN-0601"
    # Rollback restored v1's policies (SN-0601 only), not v2's.
    assert store.get(SITUATION)["lesson_id"] == "SN-0601"
    assert store.get("other") is None


def test_rollback_to_unknown_version_fails(tmp_path):
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    with pytest.raises(BehaviorPolicyError, match="unknown_policy_version:9"):
        store.rollback(9)


def test_corrupt_policy_store_fails_closed(tmp_path):
    path = tmp_path / "policy.json"
    store = BehaviorPolicyStore(path)
    integrate_verified_lesson(_valid_lesson(), store)
    path.write_text('{"tampered": true}', encoding="utf-8")
    with pytest.raises(BehaviorPolicyError):
        BehaviorPolicyStore(path)


# ---------------- ACTIVE-row loading ----------------

def _evidence_row(**kw):
    row = {
        "id": "11111111-2222-3333-4444-555555555555",
        "member_id": "99999999-8888-7777-6666-555555555555",
        "target_id": "learning-loop",
        "level": "E4_TRANSFER",
        "provenance": "VERIFICATION",
        "status": "ACTIVE",
        "claim": "Unverified candidates must never enter the learning system",
        "observed_value": {
            "situation": SITUATION,
            "prescribed_behavior": LESSON_BEHAVIOR,
            "doer": "naya-5",
            "scorer": "naya-1",
            "verifier": "naya-2",
            "verdict": "VERIFIED",
            "admission_admitted_as": "CANDIDATE",
        },
        "verification_method": "independent seat replay of treatment/control arms",
        "source_event_id": "VQ-SN-0601",
    }
    row.update(kw)
    return row


def test_active_row_maps_to_lesson_record():
    lesson = lesson_from_evidence_row(_evidence_row())
    assert lesson is not None
    assert lesson["lesson_id"] == "11111111-2222-3333-4444-555555555555"
    assert lesson["situation"] == SITUATION
    assert lesson["verdict"] == "VERIFIED"
    assert lesson["verifier"] == "naya-2"


@pytest.mark.parametrize("status", ["STALE", "SUPERSEDED", "CONFLICTED", "EXPIRED"])
def test_inactive_rows_never_become_lessons(status):
    assert lesson_from_evidence_row(_evidence_row(status=status)) is None


def test_load_active_lessons_filters_to_active_only():
    rows = [_evidence_row(), _evidence_row(status="STALE"), _evidence_row(status="EXPIRED")]
    lessons = load_active_lessons(lambda: rows)
    assert len(lessons) == 1
    assert lessons[0]["verdict"] == "VERIFIED"


def test_full_chain_row_to_integrated_policy(tmp_path):
    # The acceptance loop in one call chain: ACTIVE row -> lesson -> policy.
    store = BehaviorPolicyStore(tmp_path / "policy.json")
    (lesson,) = load_active_lessons(lambda: [_evidence_row()])
    receipt = integrate_verified_lesson(lesson, store)
    assert receipt["status"] == "INTEGRATED"
    assert store.advise(SITUATION, DEFAULT_BEHAVIOR)["behavior"] == LESSON_BEHAVIOR


# ---------------- ACT post-execution hook ----------------

def _profile():
    return QualityProfile(profile_id="wo5b-test", version="1", objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(**kw):
    base = dict(
        candidate_id="p1",
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 8.0, "evidence_sufficiency": 7.0,
                 "applicability": 8.0, "robustness": 7.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.8,
                    "applicability": 0.9, "robustness": 0.8},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated, previous state restorable",
        proof_requirements=("execution_receipt",),
        stakes="low",
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def test_act_completion_records_self_experience_via_hook(tmp_path):
    node = _booted_node(tmp_path)
    plan, plan_receipt = ap.plan_action(_authority(), [_candidate()], _profile(), now=NOW)
    assert plan_receipt.phase == "PLAN_ACCEPTED"

    receipt = ap.execute_plan(
        plan,
        executor=lambda p: "observed: node state updated",
        re_resolve=lambda: _authority(),
        now=NOW,
        profile=_profile(),
        on_executed=make_act_experience_hook(node),
    )

    assert receipt.phase == "EXECUTION_COMPLETED"
    assert node.state.experience_count == 1
    saved = node.state.known[0]
    assert "ACT executed 'naya_node_apply'" in saved
    assert "expected 'node state updated, previous state restorable'" in saved


def test_act_refusal_does_not_record_experience(tmp_path):
    node = _booted_node(tmp_path)
    plan, _ = ap.plan_action(_authority(), [_candidate()], _profile(), now=NOW)
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: "never reached",
        re_resolve=lambda: None,  # LAW unavailable -> refusal, executor never fires
        now=NOW,
        profile=_profile(),
        on_executed=make_act_experience_hook(node),
    )
    assert receipt.phase == "EXECUTION_REFUSED"
    assert node.state.experience_count == 0


def test_act_completion_without_hook_preserves_prior_behavior(tmp_path):
    node = _booted_node(tmp_path)
    plan, _ = ap.plan_action(_authority(), [_candidate()], _profile(), now=NOW)
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: "ok",
        re_resolve=lambda: _authority(),
        now=NOW,
        profile=_profile(),
    )
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert node.state.experience_count == 0  # hook is opt-in; nothing recorded
