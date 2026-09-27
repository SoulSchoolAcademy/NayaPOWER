from pathlib import Path

from kernel.brain_registry import load_and_validate_brain


def test_brain_population_has_exactly_nine_canonical_kernel_objects():
    root = Path(__file__).resolve().parents[1]

    report = load_and_validate_brain(root)

    assert report["ok"] is True, report
    assert report["node_count"] == 9
    assert report["source_count"] == 15
    assert report["graph_edge_count"] >= 9
    assert report["errors"] == []


def test_brain_population_rejects_missing_node_object(tmp_path):
    root = Path(__file__).resolve().parents[1]
    report = load_and_validate_brain(root, root_override=tmp_path)

    assert report["ok"] is False
    assert report["errors"]


def test_brain_population_rejects_node_relationship_drift(tmp_path):
    root = Path(__file__).resolve().parents[1]

    # Copy the canonical BRAIN tree into an isolated fixture so the test can
    # mutate one object without touching the repository source.
    import shutil

    shutil.copytree(root / "BRAIN", tmp_path / "BRAIN")
    object_path = tmp_path / "BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-KERNEL-SELF.json"
    data = object_path.read_text(encoding="utf-8")
    data = data.replace('"REL-KERNEL-SELF-LAW"', '"REL-KERNEL-SELF-LAW-BROKEN"', 1)
    object_path.write_text(data, encoding="utf-8")

    report = load_and_validate_brain(root, root_override=tmp_path)

    assert report["ok"] is False
    assert any("relationship" in error for error in report["errors"])
