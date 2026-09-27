from pathlib import Path

import pytest

from kernel.runtime_boot import load_runtime_manifest, load_functional_contract


def test_runtime_boot_consumes_complete_nine_node_functional_contract():
    root = Path(__file__).resolve().parents[1]

    manifest = load_runtime_manifest(root)
    contract = load_functional_contract(root)

    assert manifest["functional_contract"] == "BRAIN/03-KERNEL/0004-NINE-NODE-FUNCTIONAL-CONTRACT-V1.json"
    assert tuple(node["name"] for node in contract["nodes"]) == tuple(
        node["name"] for node in manifest["nodes"]
    )
    assert all(
        {
            "id",
            "name",
            "purpose",
            "owns",
            "must_accept",
            "must_return",
            "invariants",
            "fail_closed",
            "proof_requirements",
            "handoff",
            "optimization",
        }.issubset(node)
        for node in contract["nodes"]
    )


def test_runtime_boot_fails_closed_when_functional_contract_is_incomplete(tmp_path):
    root = Path(__file__).resolve().parents[1]
    source = root / "BRAIN/03-KERNEL/MANIFEST.json"
    target = tmp_path / "BRAIN/03-KERNEL"
    target.mkdir(parents=True)

    manifest = source.read_text(encoding="utf-8")
    manifest = manifest.replace(
        '"functional_contract": "BRAIN/03-KERNEL/0004-NINE-NODE-FUNCTIONAL-CONTRACT-V1.json"',
        '"functional_contract": "BRAIN/03-KERNEL/MISSING.json"',
    )
    (target / "MANIFEST.json").write_text(manifest, encoding="utf-8")

    with pytest.raises(RuntimeError, match="functional contract"):
        load_runtime_manifest(tmp_path)
