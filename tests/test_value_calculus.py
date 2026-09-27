import pytest
from kernel.value_calculus import ValueCalculusError, adaptive_weights, mvpa, mvpm, normalize_weights, score, sensitivity

def test_normalize_weights_sum_to_one():
    weights = normalize_weights({'utility': 2, 'reliability': 1})
    assert sum(weights.values()) == pytest.approx(1.0)
    assert weights['utility'] == pytest.approx(2 / 3)

def test_adaptive_weights_are_objective_driven():
    weights = adaptive_weights({'utility': 1, 'reliability': 1}, objective_multipliers={'utility': 2})
    assert weights['utility'] == pytest.approx(2 / 3)
    assert weights['reliability'] == pytest.approx(1 / 3)

def test_score_is_deterministic_and_receipted():
    kwargs = dict(objective='CODE_QUALITY', dimensions={'utility': 0.9, 'reliability': 0.8}, weights={'utility': 2, 'reliability': 1})
    first = score(**kwargs)
    second = score(**kwargs)
    assert first == second
    assert first.gross_value == pytest.approx(0.8666666667)
    assert first.status == 'MEASURED'

def test_critical_failure_cannot_be_averaged_away():
    receipt = score('SYSTEM_READINESS', {'correctness': 1.0, 'security': 1.0}, {'correctness': 1, 'security': 1}, required_dimensions=('security',), critical_failures=('security-proof-missing',))
    assert receipt.net_value == pytest.approx(1.0)
    assert receipt.status == 'BLOCKED'

def test_harm_reduces_net_value():
    receipt = score('USER_VALUE', {'utility': 0.9, 'reliability': 0.9}, {'utility': 1, 'reliability': 1}, harm_cost=0.2)
    assert receipt.net_value == pytest.approx(0.7)

def test_missing_dimension_fails_closed():
    with pytest.raises(ValueCalculusError):
        score('CODE_QUALITY', {'utility': 0.9}, {'utility': 1, 'reliability': 1})

def test_resource_efficiency_metrics():
    assert mvpa(8, 2) == pytest.approx(4)
    assert mvpm(10, 2, 3, 5) == pytest.approx(1)
    with pytest.raises(ValueCalculusError):
        mvpa(1, 0)
def test_sensitivity_exposes_all_approved_profiles():
    results = sensitivity(
        "CODE_QUALITY",
        {"utility": 0.9, "reliability": 0.6},
        {"balanced": {"utility": 1, "reliability": 1}, "reliability_first": {"utility": 1, "reliability": 3}},
    )
    assert set(results) == {"balanced", "reliability_first"}
    assert results["balanced"].gross_value == pytest.approx(0.75)
    assert results["reliability_first"].gross_value == pytest.approx(0.675)
