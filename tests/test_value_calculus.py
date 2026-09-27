import pytest

from kernel.value_calculus import Gate, ResourceCost, ValueProfile, calculate_value


@pytest.fixture
def profile():
    return ValueProfile(
        profile_id="SOFTWARE-QUALITY",
        version="1",
        objective="produce maintainable verified software",
        priorities={"U": 5, "R": 5, "A": 4, "E": 5, "C": 3, "Re": 3, "L": 2, "K": 2, "T": 4},
        critical_gates=(Gate("E", 0.70), Gate("R", 0.60)),
    )


def test_deterministic_and_normalized(profile):
    dims = {d: 0.8 for d in ("U", "R", "A", "E", "C", "Re", "L", "K", "T")}
    a = calculate_value(dims, profile)
    b = calculate_value(dims, profile)
    assert a == b
    assert sum(a["profile"]["weights"].values()) == pytest.approx(1.0)
    assert a["score_10"] == pytest.approx(8.0)


def test_critical_gate_blocks(profile):
    dims = {d: 1.0 for d in ("U", "R", "A", "E", "C", "Re", "L", "K", "T")}
    dims["E"] = 0.69
    result = calculate_value(dims, profile)
    assert result["status"] == "BLOCKED"


def test_harm_reduces_value(profile):
    dims = {d: 1.0 for d in ("U", "R", "A", "E", "C", "Re", "L", "K", "T")}
    result = calculate_value(dims, profile, harm=0.25)
    assert result["score_10"] == pytest.approx(7.5)


def test_missing_is_not_perfect(profile):
    dims = {d: 1.0 for d in ("U", "R", "A", "E", "C", "Re", "L", "K")}
    result = calculate_value(dims, profile)
    assert "T" in result["missing_dimensions"]
    assert result["score_10"] < 10


def test_not_applicable_is_excluded(profile):
    p = ValueProfile("TEST", "1", "objective", {"U": 1, "R": 1, "T": 1}, not_applicable=("T",))
    result = calculate_value({"U": 1, "R": 1}, p)
    assert result["score_10"] == pytest.approx(10.0)


def test_resource_metrics(profile):
    dims = {d: 1.0 for d in ("U", "R", "A", "E", "C", "Re", "L", "K", "T")}
    result = calculate_value(
        dims, profile, verification_state="VERIFIED", verified_value=100,
        resources=ResourceCost(attention=2, time=3, compute=5)
    )
    assert result["mvpa"] == pytest.approx(10.0)
    assert result["mvpm"] == pytest.approx(10.0)
    assert result["learning_efficiency"] == pytest.approx(0.2)


def test_sensitivity_is_bounded_and_reproducible(profile):
    dims = {d: 0.7 + i * 0.01 for i, d in enumerate(("U","R","A","E","C","Re","L","K","T"))}
    a = calculate_value(dims, profile, sensitivity=True)
    b = calculate_value(dims, profile, sensitivity=True)
    assert a["sensitivity"] == b["sensitivity"]
    assert a["sensitivity"]["minimum"] <= a["sensitivity"]["baseline"] <= a["sensitivity"]["maximum"]
    assert a["sensitivity"]["spread"] > 0
