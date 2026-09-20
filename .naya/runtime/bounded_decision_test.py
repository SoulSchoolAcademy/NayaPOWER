"""Deterministic holdout and adversarial tests for Action 8 bounded decisions."""

from bounded_decision import BoundedDecisionError, DecisionCandidate, choose_candidate


def c(cid, score, probability=0.5, confidence=0.5, eligible=True):
    return DecisionCandidate(cid, cid, score, probability, confidence, eligible)


# Fixed holdout: one bounded candidate-selection question with deterministic labels.
HOLDOUT = [
    ([c("A", .90), c("B", .80)], "A"),
    ([c("A", .40), c("B", .80)], "B"),
    ([c("A", .70, .80), c("B", .70, .60)], "A"),
    ([c("A", .70, .60, .90), c("B", .70, .60, .80)], "A"),
    ([c("A", .70, .60, .80), c("B", .70, .60, .80)], "B"),  # deterministic ID tie-break
    ([c("blocked", .99, eligible=False), c("safe", .50)], "safe"),
]


def test_deterministic_holdout():
    for candidates, expected in HOLDOUT:
        first = choose_candidate("ACTION8-HOLDOUT", candidates)
        second = choose_candidate("ACTION8-HOLDOUT", candidates)
        assert first == second
        assert first.selected_candidate == expected


def test_probability_and_confidence_are_output_not_authority():
    decision = choose_candidate(
        "ACTION8-HOLDOUT",
        [c("recommended", .80, .95, .95), c("other", .90, .10, .10)],
    )
    assert decision.selected_candidate == "other"
    assert decision.authority == "RECOMMENDATION_ONLY"


def test_ineligible_candidate_cannot_win():
    decision = choose_candidate(
        "ACTION8-HOLDOUT",
        [c("forbidden", 1.0, eligible=False), c("allowed", .1)],
    )
    assert decision.selected_candidate == "allowed"


def test_empty_candidates_fail_closed():
    try:
        choose_candidate("ACTION8-HOLDOUT", [])
    except BoundedDecisionError:
        return
    raise AssertionError("empty candidate set must fail closed")


def test_all_ineligible_candidates_fail_closed():
    try:
        choose_candidate("ACTION8-HOLDOUT", [c("x", 1.0, eligible=False)])
    except BoundedDecisionError:
        return
    raise AssertionError("all-ineligible candidate set must fail closed")


def test_invalid_probability_cannot_enter():
    try:
        choose_candidate("ACTION8-HOLDOUT", [c("x", .5, probability=1.1)])
    except BoundedDecisionError:
        return
    raise AssertionError("out-of-range probability must fail closed")


def test_invalid_confidence_cannot_enter():
    try:
        choose_candidate("ACTION8-HOLDOUT", [c("x", .5, confidence=-.1)])
    except BoundedDecisionError:
        return
    raise AssertionError("out-of-range confidence must fail closed")


def test_no_authority_field_can_be_promoted():
    decision = choose_candidate("ACTION8-HOLDOUT", [c("x", .5)])
    assert decision.authority == "RECOMMENDATION_ONLY"
