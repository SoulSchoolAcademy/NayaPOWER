from pathlib import Path

import pytest

from kernel.runtime_boot import CANONICAL_NODE_NAMES, load_runtime_manifest


def test_runtime_boot_consumes_canonical_brain_manifest():
    root = Path(__file__).resolve().parents[1]

    manifest = load_runtime_manifest(root)

    assert tuple(node["name"] for node in manifest["nodes"]) == CANONICAL_NODE_NAMES
    assert tuple(node["id"] for node in manifest["nodes"]) == tuple(
        f"NAYA-KERNEL-{name}" for name in CANONICAL_NODE_NAMES
    )


def test_runtime_boot_fails_closed_on_invalid_manifest(tmp_path):
    brain = tmp_path / "BRAIN/03-KERNEL"
    brain.mkdir(parents=True)
    (brain / "MANIFEST.json").write_text("{not-json", encoding="utf-8")

    with pytest.raises(RuntimeError, match="invalid BRAIN manifest JSON"):
        load_runtime_manifest(tmp_path)


def test_runtime_boot_fails_closed_on_node_order_drift(tmp_path):
    root = Path(__file__).resolve().parents[1]
    source = root / "BRAIN/03-KERNEL/MANIFEST.json"
    target = tmp_path / "BRAIN/03-KERNEL"
    target.mkdir(parents=True)

    text = source.read_text(encoding="utf-8")
    text = text.replace('"name": "SELF"', '"name": "LAW"', 1)
    (target / "MANIFEST.json").write_text(text, encoding="utf-8")

    with pytest.raises(RuntimeError, match="canonical nine-node kernel"):
        load_runtime_manifest(tmp_path)
