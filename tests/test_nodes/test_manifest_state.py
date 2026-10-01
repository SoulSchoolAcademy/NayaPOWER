"""Manifest state honesty: the declared package status must match reality.

CANDIDATE — NOT RATIFIED — NOT MERGED. These tests guard against stale
declared state (e.g. the pre-build "SCAFFOLD" status lingering after all
nine nodes were implemented and integrated). Evidence-law honesty: the
manifest must say what the branch actually holds.
"""
import json
import os

import pytest

MANIFEST_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "naya_kernel", "manifest.json")
)

NINE = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]


@pytest.fixture(scope="module")
def manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_manifest_exists_and_parses(manifest):
    assert isinstance(manifest, dict)


def test_status_is_candidate_not_scaffold(manifest):
    # Tick 18 fix: 9/9 nodes implemented + kernel integrated; "SCAFFOLD"
    # no longer describes reality and must never return.
    assert manifest["status"] == "CANDIDATE"
    assert manifest["status"] != "SCAFFOLD"


def test_candidate_banner_names_not_ratified_not_merged(manifest):
    banner = manifest["candidate_banner"]
    assert "NOT RATIFIED" in banner
    assert "NOT MERGED" in banner


def test_all_nine_nodes_implemented_candidate(manifest):
    impl = manifest["implementation_status"]
    for node in NINE:
        assert impl[node] == "implemented-candidate", f"{node}: {impl.get(node)}"
        assert "stub" not in impl[node].lower()


def test_kernel_is_graph_integrated(manifest):
    assert manifest["implementation_status"]["KERNEL"] == "kernel-integrated-graph"


def test_topology_declares_thirteen_edges(manifest):
    topo = manifest["topology"]
    assert topo["edges"] == 13
    assert topo["kind"] == "canonical-runtime-graph-v1"
    order = topo["evaluation_order"]
    assert set(order) == set(NINE) and len(order) == 9


def test_lock_reconciliation_records_all_three(manifest):
    lock_rec = manifest["lock_reconciliation"]
    assert set(lock_rec.keys()) == {"graph_topology", "KNOW", "calculus"}
    # Each entry must state what was actually done, not a bare status word.
    for key, value in lock_rec.items():
        assert len(value) >= 40, f"lock_reconciliation[{key}] too thin to be evidence"
