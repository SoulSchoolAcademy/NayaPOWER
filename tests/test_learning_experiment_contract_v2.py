from tools.learning_experiment_contract import validate_round2_manifest


def valid_manifest():
    return {
        "schema": "NAYAPOWER_LEARNING_COMPOUNDING_EXPERIMENT_V2",
        "status": "PREREGISTERED",
        "arms": [
            {"name": "CONTROL"},
            {"name": "TREATMENT"},
            {"name": "WRONG_LESSON"},
        ],
        "minimum_trials_per_arm": 5,
        "negative_transfer": {"required": True, "minimum_trials": 5},
        "scoring": {
            "weights": {
                "accuracy": 0.4,
                "diagnostic_order": 0.2,
                "cost": 0.2,
                "consistency": 0.1,
                "negative_transfer_guard": 0.1,
            },
            "negative_transfer_is_hard_gate": True,
        },
        "answer_key": {
            "prevalidated_before_trials": True,
            "builder": "Naya 4",
            "independent_verifier": "Coda 2",
            "fixture_shas": ["a" * 40, "b" * 40],
        },
        "evidence_capture": {
            "raw_transcripts_required": True,
            "exact_tool_call_counts_required": True,
            "immutable_fixture_binding_required": True,
        },
        "hypotheses": [
            "H1 diagnostic order improves",
            "H2 accuracy improves on prevalidated keys",
            "H3 value gain is not purchased by disproportionate cost",
            "H4 unrelated tasks do not suffer negative transfer",
        ],
    }


def test_round2_preregistration_accepts_hard_abc_design():
    result = validate_round2_manifest(valid_manifest())
    assert result.ok, result.errors


def test_round2_rejects_builder_self_validation():
    m = valid_manifest()
    m["answer_key"]["independent_verifier"] = m["answer_key"]["builder"]
    result = validate_round2_manifest(m)
    assert not result.ok
    assert "ANSWER_KEY_VERIFIER_MUST_BE_INDEPENDENT" in result.errors


def test_round2_rejects_underpowered_or_missing_wrong_lesson_arm():
    m = valid_manifest()
    m["arms"] = [{"name": "CONTROL"}, {"name": "TREATMENT"}]
    m["minimum_trials_per_arm"] = 4
    result = validate_round2_manifest(m)
    assert "EXACT_ABC_ARMS_REQUIRED" in result.errors
    assert "MINIMUM_FIVE_TRIALS_PER_ARM" in result.errors


def test_round2_rejects_weak_negative_transfer_design():
    m = valid_manifest()
    m["negative_transfer"]["minimum_trials"] = 1
    m["scoring"]["negative_transfer_is_hard_gate"] = False
    result = validate_round2_manifest(m)
    assert "MINIMUM_FIVE_NEGATIVE_TRANSFER_TRIALS" in result.errors
    assert "NEGATIVE_TRANSFER_HARD_GATE_REQUIRED" in result.errors


def test_round2_requires_raw_transcripts_tool_counts_and_fixture_binding():
    m = valid_manifest()
    m["evidence_capture"] = {
        "raw_transcripts_required": False,
        "exact_tool_call_counts_required": False,
        "immutable_fixture_binding_required": False,
    }
    result = validate_round2_manifest(m)
    assert "RAW_TRANSCRIPTS_REQUIRED" in result.errors
    assert "EXACT_TOOL_CALL_COUNTS_REQUIRED" in result.errors
    assert "IMMUTABLE_FIXTURE_BINDING_REQUIRED" in result.errors


def test_round2_rejects_outcome_leakage_before_trials():
    m = valid_manifest()
    m["winner"] = "TREATMENT"
    m["results"] = {"treatment": 10}
    result = validate_round2_manifest(m)
    assert not result.ok
    assert any(e.startswith("OUTCOME_LEAKAGE_BEFORE_TRIALS:") for e in result.errors)


def test_round2_weights_must_be_complete_and_sum_to_one():
    m = valid_manifest()
    m["scoring"]["weights"]["accuracy"] = 0.9
    result = validate_round2_manifest(m)
    assert "SCORING_WEIGHTS_MUST_SUM_TO_ONE" in result.errors


def test_round2_fixture_ids_are_content_bound():
    m = valid_manifest()
    m["answer_key"]["fixture_shas"] = ["not-a-sha"]
    result = validate_round2_manifest(m)
    assert "FIXTURE_SHA_MUST_BE_40_HEX" in result.errors
