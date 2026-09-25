from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
HEALTH = ROOT / ".naya" / "memory" / "superbrain_health.py"

spec = importlib.util.spec_from_file_location("superbrain_health", HEALTH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def test_entity_relationship_labels_do_not_become_orphan_event_edges():
    result = module.report()
    assert result["orphan_relationship_count"] == 0, result
    assert result["unresolved_relationship_count"] == 2, result
    assert result["status"] == "UNKNOWN", result
