"""P0-B: ADVISE influence-bridge proof tests.

Proves the Superbrain Report's bottleneck #1 is closed: an applicable,
legitimately retrieved lesson CAN change a LAW-authorized action plan before
ACT constructs it — while irrelevant, unauthorized, untrusted, and unsafe
lessons provably cannot.
"""
import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "BRAIN" / "12-ENGINEERING" / "kernel_behavior_engine.py"


def load_engine():
    spec = importlib.util.spec_from_file_location("naya_kernel_advise_bridge", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.KernelBehaviorEngine


def base_input():
    return {
        "identity": {"actor_id": "naya-test", "owner_id": "owner-1", "system_id": "NayaPOWER"},
        "mission": {"mission": "preserve truth", "objective": "test"},
        "proposed_action": {
            "type": "consequential_action",
            "expected_outcome": "expected",
            "proof_requirements": ["independent"],
        },
        "authority": {"grant_id": "grant-1", "revoked": False, "expires_at": None},
        "claim": "the action works",
        "evidence": [{"provenance": "test://evidence/1"}],
        "intelligent_block_id": "IB-NAYA-NODE-0001-0001",
        "independent_evidence": [{"provenance": "test://independent/1"}],
        "observed_outcome": "expected",
        "holdout_result": True,
        "next_action": "continue",
    }


def applicable_lesson():
    return {
        "id": "IB-APPLICABLE-1",
        "principle": "Consequential actions require blast-radius limits",
        "owner_id": "owner-1",
        "truth_state": "PROMOTED",
        "applies_to_action_types": ["consequential_action"],
        "advisory": {
            "add_proof_requirements": ["blast_radius_assessment"],
            "add_constraints": ["max_blast_radius:low"],
            "note": "IB-APPLICABLE-1 applied",
        },
    }


# (a) BASELINE: no lessons -> plan unchanged, ADVISE present but NO_CHANGE
def test_baseline_no_lessons_plan_unchanged():
    Engine = load_engine()
    result = Engine().execute_cycle(base_input())
    assert result["status"] == "COMPLETED"
    advise = result["node_receipts"]["ADVISE"]
    assert advise["status"] == "NO_CHANGE"
    act = result["node_receipts"]["ACT"]
    assert act["status"] == "READY"
    # ACT output carries the action; proof requirements untouched
    act_out = result["node_receipts"]["ACT"]
    assert act_out["status"] == "READY"


# (b) APPLICABLE lesson -> plan MUST change in the right way
def test_applicable_lesson_changes_plan():
    Engine = load_engine()
    data = base_input()
    data["intelligence"] = [applicable_lesson()]
    engine = Engine()
    result = engine.execute_cycle(data)
    assert result["status"] == "COMPLETED"
    advise = result["node_receipts"]["ADVISE"]
    assert advise["status"] == "ADVISED"

    # END-TO-END: ACT's constructed action carries the lesson's additions
    act_action = engine.outputs["ACT"]["action"]
    assert "blast_radius_assessment" in act_action["proof_requirements"]
    assert "max_blast_radius:low" in act_action["constraints"]
    assert "independent" in act_action["proof_requirements"]  # original preserved
    assert act_action["type"] == "consequential_action"  # type untouched

    # The proof receipt: which lesson affected which choice, before/after
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "ADVISED"
    assert len(advise_out["influences"]) == 1
    inf = advise_out["influences"][0]
    assert inf["lesson_id"] == "IB-APPLICABLE-1"
    assert inf["before"]["proof_requirements"] == ["independent"]
    assert "blast_radius_assessment" in inf["after"]["proof_requirements"]
    assert "max_blast_radius:low" in inf["after"]["constraints"]
    # Original requirement preserved (monotonic-additive, never removed)
    assert "independent" in inf["after"]["proof_requirements"]
    # Action type untouched
    assert advise_out["advised_action"]["type"] == "consequential_action"


# (c) IRRELEVANT lesson -> plan MUST NOT change (negative control)
def test_irrelevant_lesson_does_not_change_plan():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-IRRELEVANT-1"
    lesson["applies_to_action_types"] = ["totally_different_action"]
    data = base_input()
    data["intelligence"] = [lesson]
    result = Engine().execute_cycle(data)
    advise = result["node_receipts"]["ADVISE"]
    assert advise["status"] == "NO_CHANGE"

    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["influences"] == []
    assert advise_out["excluded"] == [
        {"lesson_id": "IB-IRRELEVANT-1", "reason": "not_applicable"}
    ]
    assert advise_out["advised_action"]["proof_requirements"] == ["independent"]
    assert "constraints" not in advise_out["advised_action"]


# (d) UNAUTHORIZED lesson (cross-owner) -> MUST NOT change plan (negative control)
def test_unauthorized_cross_owner_lesson_rejected():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-FOREIGN-1"
    lesson["owner_id"] = "owner-2"  # different owner
    data = base_input()
    data["intelligence"] = [lesson]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["influences"] == []
    assert advise_out["excluded"] == [
        {"lesson_id": "IB-FOREIGN-1", "reason": "unauthorized_cross_owner"}
    ]


# (e) UNTRUSTED lesson (superseded) -> MUST NOT change plan
def test_superseded_lesson_rejected():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-STALE-1"
    lesson["truth_state"] = "SUPERSEDED"
    data = base_input()
    data["intelligence"] = [lesson]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["excluded"] == [
        {"lesson_id": "IB-STALE-1", "reason": "truth_state_not_trusted"}
    ]


# (f) CANDIDATE lesson (not yet proven) -> MUST NOT steer actions
def test_candidate_lesson_rejected():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-CANDIDATE-1"
    lesson["truth_state"] = "CANDIDATE"
    data = base_input()
    data["intelligence"] = [lesson]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["excluded"][0]["reason"] == "truth_state_not_trusted"


# (g) UNSAFE advisory (tries to change action type) -> rejected wholesale
def test_unsafe_advisory_rejected_wholesale():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-EVIL-1"
    lesson["advisory"] = {
        "add_proof_requirements": ["independent"],
        "change_type": "unrestricted_action",  # NOT in allowlist
    }
    data = base_input()
    data["intelligence"] = [lesson]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["influences"] == []
    assert advise_out["excluded"] == [
        {"lesson_id": "IB-EVIL-1", "reason": "advisory_rejected_unsafe"}
    ]
    # Even the innocent part of the advisory is rejected (wholesale)
    assert advise_out["advised_action"]["proof_requirements"] == ["independent"]


# (h) Advisory attempting to REMOVE a requirement -> not in allowlist -> rejected
def test_advisory_cannot_remove_requirements():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-SNEAKY-1"
    lesson["advisory"] = {"remove_proof_requirements": ["independent"]}
    data = base_input()
    data["intelligence"] = [lesson]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["excluded"][0]["reason"] == "advisory_rejected_unsafe"
    assert advise_out["advised_action"]["proof_requirements"] == ["independent"]


# (i) FAIL-CLOSED: LAW blocked -> ADVISE never runs, ACT never built
def test_law_blocked_means_no_advise_no_act():
    Engine = load_engine()
    data = base_input()
    data["authority"] = {}
    data["intelligence"] = [applicable_lesson()]
    result = Engine().execute_cycle(data)
    assert result["status"] == "BLOCKED"
    assert result["node_receipts"]["LAW"]["status"] == "BLOCKED"
    assert "ADVISE" not in result["node_receipts"]
    assert "ACT" not in result["node_receipts"]


# (j) Mixed batch: one applicable + one irrelevant + one unauthorized ->
#     only the applicable one influences, others explicitly excluded
def test_mixed_batch_only_applicable_influences():
    Engine = load_engine()
    good = applicable_lesson()
    irrelevant = applicable_lesson()
    irrelevant["id"] = "IB-IRR-2"
    irrelevant["applies_to_action_types"] = ["other"]
    foreign = applicable_lesson()
    foreign["id"] = "IB-FOR-2"
    foreign["owner_id"] = "owner-9"
    data = base_input()
    data["intelligence"] = [irrelevant, foreign, good]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "ADVISED"
    assert [i["lesson_id"] for i in advise_out["influences"]] == ["IB-APPLICABLE-1"]
    excluded = {e["lesson_id"]: e["reason"] for e in advise_out["excluded"]}
    assert excluded == {"IB-IRR-2": "not_applicable", "IB-FOR-2": "unauthorized_cross_owner"}


# (k) Reader path: ADVISE evaluates the same lessons KNOW's reader returns
def test_reader_lessons_influence_plan():
    Engine = load_engine()
    lesson = applicable_lesson()

    def reader(block_id, owner_id):
        assert block_id == "IB-NAYA-NODE-0001-0001"
        assert owner_id == "owner-1"
        return [lesson]

    data = base_input()  # no "intelligence" key; reader is the source
    engine = Engine(intelligence_reader=reader)
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "ADVISED"
    assert advise_out["influences"][0]["lesson_id"] == "IB-APPLICABLE-1"
    assert "blast_radius_assessment" in advise_out["advised_action"]["proof_requirements"]


# (l) Reader path with missing identity -> fail closed, no lessons evaluated
def test_reader_without_identity_evaluates_nothing():
    Engine = load_engine()

    def reader(block_id, owner_id):
        raise AssertionError("reader must not be called without identity")

    data = base_input()
    data["identity"] = {"system_id": "NayaPOWER"}  # no actor_id/owner_id -> SELF blocks
    engine = Engine(intelligence_reader=reader)
    self_out = engine.process_self(data)
    # SELF blocked means cycle stops; advise with empty self output degrades safely
    advise_out = engine.process_advise(data, {"action_context": {}}, {"identity_context": {}})
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["influences"] == []


# (m) Mistyped advisory values (string instead of list) -> rejected wholesale
def test_mistyped_advisory_rejected():
    Engine = load_engine()
    lesson = applicable_lesson()
    lesson["id"] = "IB-TYPEBUG-1"
    lesson["advisory"] = {"add_proof_requirements": "independent"}  # string, not list
    data = base_input()
    data["intelligence"] = [lesson]
    engine = Engine()
    self_out = engine.process_self(data)
    law_out = engine.process_law(data, self_out)
    advise_out = engine.process_advise(data, law_out, self_out)
    assert advise_out["status"] == "NO_CHANGE"
    assert advise_out["influences"] == []
    assert advise_out["excluded"] == [
        {"lesson_id": "IB-TYPEBUG-1", "reason": "advisory_rejected_unsafe"}
    ]
    # Nothing half-applied
    assert advise_out["advised_action"]["proof_requirements"] == ["independent"]
