from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / ".naya/runtime/cold_successor_test.py"

spec = importlib.util.spec_from_file_location("cold_successor_test", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_cold_successor_answers_must_bind_to_live_control_plane_values():
    harness = module.ColdSuccessorTest()

    q2 = harness.q2_what_are_we_building()
    q4 = harness.q4_what_does_success_mean()
    q11 = harness.q11_what_should_happen_next()

    expected_next = harness.state["single_next_action"]
    expected_block = harness.blocks["active_block"]["id"]

    assert expected_block != "P0"
    assert q2["next_responsible_action"] == expected_next
    assert q4["next_responsible_action"] == expected_next
    assert q11["status"] == "ACTIVE_NEXT_ACTION"
    assert q11["next_responsible_action"] == expected_next
