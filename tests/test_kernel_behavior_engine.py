import importlib.util
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "BRAIN" / "12-ENGINEERING" / "kernel_behavior_engine.py"


def load_engine():
    spec = importlib.util.spec_from_file_location("naya_kernel_behavior_engine", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.KernelBehaviorEngine


def base_input():
    return {
        "identity": {"actor_id": "naya-test", "system_id": "NayaPOWER"},
        "mission": {"mission": "preserve truth", "objective": "test"},
        "proposed_action": {
            "type": "test_action",
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


def test_missing_identity_blocks_self():
    Engine = load_engine()
    data = base_input()
    data["identity"] = {}
    result = Engine().execute_cycle(data)
    assert result["status"] == "BLOCKED"
    assert result["node_receipts"]["SELF"]["status"] == "BLOCKED"


def test_missing_authority_blocks_law_and_act():
    Engine = load_engine()
    data = base_input()
    data["authority"] = {}
    result = Engine().execute_cycle(data)
    assert result["status"] == "BLOCKED"
    assert result["node_receipts"]["LAW"]["status"] == "BLOCKED"
    assert "ACT" not in result["node_receipts"]


def test_no_independent_evidence_cannot_verify():
    Engine = load_engine()
    data = base_input()
    data["independent_evidence"] = []
    result = Engine().execute_cycle(data)
    assert result["status"] == "INCONCLUSIVE"
    assert result["node_receipts"]["VERIFY"]["status"] == "INCONCLUSIVE"
    assert result["node_receipts"]["LEARN"]["status"] == "DEFERRED"


def test_verified_outcome_can_promote_only_with_holdout():
    Engine = load_engine()
    data = base_input()
    result = Engine().execute_cycle(data)
    assert result["status"] == "COMPLETED"
    assert result["node_receipts"]["VERIFY"]["status"] == "VERIFIED"
    assert result["node_receipts"]["LEARN"]["status"] == "PROMOTED"


def test_verified_without_holdout_does_not_promote():
    Engine = load_engine()
    data = base_input()
    data["holdout_result"] = False
    result = Engine().execute_cycle(data)
    assert result["status"] == "COMPLETED"
    assert result["node_receipts"]["VERIFY"]["status"] == "VERIFIED"
    assert result["node_receipts"]["LEARN"]["status"] == "DEFERRED"
    assert result["node_receipts"]["EVOLVE"]["status"] == "READY"


def test_reader_is_owner_and_block_bound():
    Engine = load_engine()
    calls = []

    def reader(block_id, owner_id):
        calls.append((block_id, owner_id))
        return [{"id": block_id, "owner_id": owner_id, "provenance": "test://block"}]

    data = base_input()
    data["identity"]["owner_id"] = "owner-1"
    data["intelligence"] = []
    result = Engine(intelligence_reader=reader).execute_cycle(data)

    assert result["status"] == "COMPLETED"
    assert calls == [("IB-NAYA-NODE-0001-0001", "owner-1")]


def test_successor_strips_inherited_authority():
    Engine = load_engine()
    data = base_input()
    data["authority"] = {"grant_id": "grant-1", "revoked": False, "expires_at": None}
    result = Engine().execute_cycle(data)
    successor = result["node_receipts"]["EVOLVE"]
    assert successor["status"] == "READY"
    output_hash = successor["output_hash"]
    assert output_hash
