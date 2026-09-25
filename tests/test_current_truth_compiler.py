from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / ".naya/runtime/current_truth_compiler.py"
spec = importlib.util.spec_from_file_location("current_truth_compiler", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_current_truth_packet_is_derived_and_contains_cold_successor_fields():
    packet = module.compile_current_truth()
    assert packet["schema"] == "NAYAPOWER_CURRENT_TRUTH_PACKET_V1"
    assert packet["status"] == "DERIVED"
    assert packet["repository_reality"]["head_source"] == "git:HEAD"
    assert packet["repository_reality"]["recorded_head_is_authoritative"] is False
    assert packet["identity"]["mission"]
    assert packet["identity"]["north_star"]
    assert packet["unknown"]
    assert packet["next"]
    assert packet["canonical_sources"]["smart_note_ib_contract"]


def test_current_truth_does_not_create_a_second_store():
    packet = module.compile_current_truth()
    assert packet["authority"]["control_plane"] == ".naya/control-plane/"
    assert packet["canonical_sources"]["current_truth"].endswith(
        "DISTILL-PROJECT-INTELLIGENCE-CURRENT-TRUTH.md"
    )
