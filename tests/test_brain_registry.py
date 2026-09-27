from pathlib import Path

from kernel.brain_registry import load_and_validate_brain


def test_brain_population_has_exactly_nine_canonical_kernel_objects():
    root = Path(__file__).resolve().parents[1]

    report = load_and_validate_brain(root)

    assert report["ok"] is True
    assert report["node_count"] == 9
    assert report["source_count"] == 15
    assert report["graph_edge_count"] >= 9
    assert report["errors"] == []


def test_brain_population_rejects_missing_node_object(tmp_path):
    root = Path(__file__).resolve().parents[1]
    report = load_and_validate_brain(root, root_override=tmp_path)

    assert report["ok"] is False
    assert report["errors"]
