from copy import deepcopy
from datetime import datetime, timezone

import pytest

from tools.standing_production_promotion_policy import evaluate_policy, load_policy, REQUIRED_CONTEXT

NOW = datetime(2026, 9, 29, 21, tzinfo=timezone.utc)

def candidate():
    policy = deepcopy(load_policy())
    policy['expiry'] = {'expires_at': '2026-10-29T00:00:00Z', 'review_after': '2026-10-15T00:00:00Z', 'automatic_renewal': False}
    context = {field: True for field in REQUIRED_CONTEXT}
    context.update(repository='SoulSchoolAcademy/NayaPOWER', source_branch='main', target_branch='production',
                   source_sha='a'*40, resolved_main_sha='a'*40, changed_paths=['supabase/functions/example/index.ts'],
                   requested_operation='PROMOTE_PRODUCTION', no_unresolved_production_blocker=True)
    return policy, context

def test_unresolved_blocker_is_an_enforced_precondition():
    policy, context = candidate()
    context['no_unresolved_production_blocker'] = False
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'DENY'

@pytest.mark.parametrize('path', ['tools/standing_production_promotion_policy.py', '.github/workflows/kernel-tests.yml',
                                  '.github/workflows/live-supabase-runtime-proof.yml', 'supabase/config.toml'])
def test_enforcement_and_proof_changes_cannot_authorize_their_own_promotion(path):
    policy, context = candidate()
    context['changed_paths'] = [path]
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'DENY'

@pytest.mark.parametrize('dates', [
    {'expires_at': None, 'review_after': None},
    {'expires_at': 'not-a-date', 'review_after': 'not-a-date'},
    {'expires_at': '2020-01-01T00:00:00Z', 'review_after': '2019-12-01T00:00:00Z'},
])
def test_policy_dates_are_checked_even_when_context_claims_unexpired(dates):
    policy, context = candidate()
    policy['expiry'].update(dates)
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'DENY'

def test_non_promotion_operation_cannot_use_promotion_authority():
    policy, context = candidate()
    context['requested_operation'] = 'DROP_DATABASE'
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'DENY'

def test_resolved_main_sha_drift_is_not_an_exact_candidate():
    policy, context = candidate()
    context['resolved_main_sha'] = 'b'*40
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'DENY'

def test_absent_changed_path_evidence_cannot_hide_protected_changes():
    policy, context = candidate()
    del context['changed_paths']
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'DENY'


def test_bounded_routine_candidate_is_allowed():
    policy, context = candidate()
    assert evaluate_policy(policy, context, now=NOW) == {'decision': 'ALLOW', 'reason': 'all_policy_gates_pass'}


def test_ratified_canonical_activation_is_finite_and_stops_at_review_and_expiry():
    _, context = candidate()
    policy = load_policy()
    assert policy['expiry'] == {
        'review_after': '2026-10-15T00:00:00-07:00',
        'expires_at': '2026-10-29T00:00:00-07:00',
        'automatic_renewal': False,
    }
    assert policy['activation']['authority'] == 'HUMAN_DIRECTOR'
    assert evaluate_policy(policy, context, now=NOW)['decision'] == 'ALLOW'
    assert evaluate_policy(policy, context, now=datetime(2026, 10, 15, 7, tzinfo=timezone.utc))['reason'] == 'policy_review_due'
    assert evaluate_policy(policy, context, now=datetime(2026, 10, 29, 7, tzinfo=timezone.utc))['reason'] == 'policy_expired'


@pytest.mark.parametrize('now,reason', [
    (datetime(2026, 10, 15, tzinfo=timezone.utc), 'policy_review_due'),
    (datetime(2026, 10, 29, tzinfo=timezone.utc), 'policy_expired'),
])
def test_review_and_expiry_boundaries_are_inclusive(now, reason):
    policy, context = candidate()
    assert evaluate_policy(policy, context, now=now) == {'decision': 'DENY', 'reason': reason}
