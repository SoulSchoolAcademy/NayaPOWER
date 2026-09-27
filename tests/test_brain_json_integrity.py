"""Integrity guard: canonical BRAIN artifacts must be machine-parseable.

Why this exists: on canonical main, BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json
contained a LITERAL backslash-n typed into the text instead of a real newline, so no
JSON reader could parse it. The test suite still reported green, because the code
paths that read that artifact were never reached in a way that surfaced the parse
failure. A passing test was covering a corrupt canonical file.

This test makes that class of failure impossible to hide again. It is deliberately
small and has no dependencies beyond the standard library.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

# Artifacts the runtime loader and the BRAIN contracts treat as canonical.
CANONICAL = [
    "BRAIN/03-KERNEL/MANIFEST.json",
    "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json",
    "BRAIN/04-INTELLIGENCE/MASTER-INDEX.json",
    "BRAIN/04-INTELLIGENCE/GRAPH/0001-KERNEL-GRAPH-SEED-V1.json",
    "BRAIN/04-INTELLIGENCE/GRAPH/0002-KNOWLEDGE-TO-NODE-MAP-V1.json",
    "BRAIN/11-KNOWLEDGE/0003-KNOWLEDGE-POPULATION-MAP-V1.json",
    "BRAIN/NAYAPOWER-BRAIN-INDEX.json",
    "BRAIN/REAL-TREE.json",
]

NODE_OBJECTS = sorted((REPO / "BRAIN/04-INTELLIGENCE/OBJECTS").glob("NAYA-KERNEL-*.json"))


def _all_brain_json() -> list[Path]:
    return sorted((REPO / "BRAIN").rglob("*.json"))


def test_every_brain_json_artifact_parses():
    """No canonical artifact may be unreadable by a JSON reader."""
    broken = []
    for path in _all_brain_json():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report every failure mode
            broken.append(f"{path.relative_to(REPO).as_posix()}: {exc}")
    assert not broken, "unparseable canonical JSON artifacts:\n" + "\n".join(broken)


@pytest.mark.parametrize("rel", CANONICAL)
def test_canonical_artifact_parses_and_declares_identity(rel: str):
    path = REPO / rel
    assert path.is_file(), f"missing canonical artifact: {rel}"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(doc, dict), f"{rel} must be a JSON object"
    assert doc, f"{rel} must not be empty"


def test_canonical_manifest_and_registry_agree_on_nine_nodes():
    manifest = json.loads((REPO / "BRAIN/03-KERNEL/MANIFEST.json").read_text(encoding="utf-8"))
    registry = json.loads(
        (REPO / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text(encoding="utf-8")
    )
    manifest_ids = [n.get("id") for n in manifest.get("nodes", [])]
    assert len(manifest_ids) == 9, f"manifest must declare 9 nodes, found {len(manifest_ids)}"
    assert registry.get("node_ids") == manifest_ids, (
        "the runtime registry and the manifest disagree on node identity; "
        "the registry is what a loader consumes, so this is a live divergence"
    )
    assert len(NODE_OBJECTS) == 9, f"expected 9 materialized node objects, found {len(NODE_OBJECTS)}"


def test_runtime_loader_can_consume_the_canonical_artifacts():
    """The loader must be able to read what it claims to load."""
    import sys

    sys.path.insert(0, str(REPO))
    from kernel.brain_registry import load_and_validate_brain

    report = load_and_validate_brain(REPO)
    assert report.get("ok") is True, f"brain population did not validate: {report.get('errors')}"
    assert report.get("node_count") == 9
    assert report.get("graph_edge_count", 0) > 0
