from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

CANONICAL = ROOT / "BRAIN" / "03-KERNEL" / "0003-RUNTIME-REGISTRY-V1.json"
DUPLICATE = ROOT / "BRAIN" / "03-KERNEL" / "RUNTIME-WIRING.json"

EXPECTED_NODES = {
    "SELF", "LAW", "ACT", "KNOW", "PROVE",
    "CONNECT", "VERIFY", "LEARN", "EVOLVE",
}


def test_runtime_binding_has_one_canonical_owner():
    assert CANONICAL.exists(), "canonical runtime registry must exist"
    assert not DUPLICATE.exists(), (
        "RUNTIME-WIRING.json must not become a second runtime-binding truth owner"
    )

    registry = json.loads(CANONICAL.read_text(encoding="utf-8"))
    bindings = registry["node_runtime_bindings"]

    assert set(bindings) == EXPECTED_NODES
    assert registry["binding_truth_rule"].startswith(
        "Every one of the nine nodes must have exactly one canonical binding entry"
    )
