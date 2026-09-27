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


def test_brain_population_validates_manifest_registry_index_and_object_envelopes():
    root = Path(__file__).resolve().parents[1]
    report = load_and_validate_brain(root)

    assert report["ok"] is True
    assert report["manifest_registry_index_parity"] is True
    assert report["object_envelope_errors"] == []


def test_brain_population_rejects_graph_edges_that_reference_unknown_nodes(tmp_path):
    import json
    import shutil

    source = Path(__file__).resolve().parents[1]
    for relative in (
        "BRAIN/03-KERNEL/MANIFEST.json",
        "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json",
        "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
        "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json",
        "BRAIN/04-INTELLIGENCE/GRAPH/0002-KNOWLEDGE-TO-NODE-MAP-V1.json",
        "BRAIN/11-KNOWLEDGE/0003-KNOWLEDGE-POPULATION-MAP-V1.json",
        "BRAIN/11-KNOWLEDGE/0004-HUMAN-AI-MACHINE-REPRESENTATION-V1.md",
    ):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)
    for node_id in ("NAYA-KERNEL-SELF", "NAYA-KERNEL-LAW", "NAYA-KERNEL-ACT", "NAYA-KERNEL-KNOW", "NAYA-KERNEL-PROVE", "NAYA-KERNEL-CONNECT", "NAYA-KERNEL-VERIFY", "NAYA-KERNEL-LEARN", "NAYA-KERNEL-EVOLVE"):
        src = source / "BRAIN/04-INTELLIGENCE/OBJECTS" / f"{node_id}.json"
        dst = tmp_path / "BRAIN/04-INTELLIGENCE/OBJECTS" / f"{node_id}.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    graph_path = tmp_path / "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    graph["edges"][0]["target_id"] = "NAYA-KERNEL-NOT-REAL"
    graph_path.write_text(json.dumps(graph), encoding="utf-8")

    report = load_and_validate_brain(source, root_override=tmp_path)

    assert report["ok"] is False
    assert any("unknown_graph_node" in error for error in report["errors"])


def test_brain_manifest_runtime_binding_is_explicit_and_canonical():
    from pathlib import Path
    import json

    root = Path(__file__).resolve().parents[1]
    manifest = json.loads(
        (root / "BRAIN/03-KERNEL/MANIFEST.json").read_text(encoding="utf-8")
    )

    assert manifest["runtime_entrypoint"] == "runtime/cold_runtime.py"
    assert manifest["runtime_loader"] == "Kernel.from_brain"
    assert manifest["canonical_persistence_adapter"] == "runtime/canonical_memory.py"
