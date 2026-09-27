#!/usr/bin/env python3
"""Tests for the Phase 2 fail-closed kernel boot.

The most important test here is `test_no_credentials_is_unknown_not_pass`:
with no receiver credentials the module must report UNKNOWN and refuse. That
is the current real-world state, and it must never be reported as healthy.
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))

import kernel_boot as kb  # noqa: E402


def healthy_nodes(today: date | None = None) -> list[dict]:
    today = today or date(2026, 9, 26)
    nodes = []
    for idx, spec in enumerate(kb.MASTER_NODES):
        terminal = idx == len(kb.MASTER_NODES) - 1
        nodes.append({
            "node_id": spec["node_id"],
            "name": spec["name"],
            "kernel_version": kb.EXPECTED_KERNEL_VERSION,
            "status": "ACTIVE",
            "verified": True,
            "observed_at": today.isoformat(),
            "relationships": {"next": None if terminal else kb.EXPECTED_SEQUENCE[idx + 1]},
            "governance_bindings": [f"RULE-{spec['node_id']}-01"],
            "enforcement_point": f"enforce_{spec['node_id'].lower().replace('-', '_')}",
            "conflicts": [],
        })
    return nodes


HEALTHY_PAYLOAD = {"next_action": "Merge PR #801 and reconcile the 12 claimants."}


def test_kernel_spec_is_exactly_nine_and_ordered():
    assert len(kb.MASTER_NODES) == 9
    assert kb.EXPECTED_SEQUENCE == (
        "MN-01", "MN-02", "MN-03", "MN-04", "MN-05",
        "MN-06", "MN-07", "MN-08", "MN-09",
    )
    assert kb.MASTER_NODES[0]["name"] == "Constitution, Mission & Scope"
    assert kb.MASTER_NODES[-1]["name"].startswith("NayaNET Architecture")


def test_no_credentials_is_unknown_not_pass(monkeypatch):
    """THE critical test: absent credentials must be UNKNOWN + refuse."""
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE_KEY", raising=False)
    report = kb.boot_kernel(kb.receiver_source)
    assert report.conclusive is True
    assert report.boot_permitted is False
    assert [f.status for f in report.findings] == ["UNKNOWN"]
    assert report.findings[0].check == "KERNEL_SOURCE"
    assert "credentials absent" in report.findings[0].detail
    assert report.loaded == []


def test_authority_is_never_granted_even_on_healthy_kernel():
    report = kb.boot_kernel(lambda: healthy_nodes(), HEALTHY_PAYLOAD)
    assert report.boot_permitted is True
    assert report.authority == "NONE"


def test_healthy_kernel_permits_boot():
    report = kb.boot_kernel(lambda: healthy_nodes(), HEALTHY_PAYLOAD)
    assert report.boot_permitted is True, report.unresolved
    assert report.conclusive is True
    assert len(report.loaded) == 9
    assert report.next_action.startswith("Merge PR #801")


def test_healthy_kernel_passes_every_check():
    report = kb.boot_kernel(lambda: healthy_nodes(), HEALTHY_PAYLOAD)
    assert {f.status for f in report.findings} == {"PASS"}
    # KERNEL_SOURCE, NODE_PRESENCE, KERNEL_VERSION, NODE_STATUS,
    # NODE_RELATIONSHIPS, GOVERNANCE_BINDINGS, ENFORCEMENT_COVERAGE,
    # NODE_CONFLICTS, NODE_FRESHNESS, NEXT_ACTION
    assert len(report.findings) == 10


@pytest.mark.parametrize("idx", range(9))
def test_missing_any_single_node_fails_closed(idx):
    nodes = healthy_nodes()
    nodes.pop(idx)
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "NODE_PRESENCE" and f.status == "FAIL"
               for f in report.findings)


def test_missing_node_is_named_in_evidence():
    nodes = [n for n in healthy_nodes() if n["node_id"] != "MN-07"]
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    presence = next(f for f in report.findings if f.check == "NODE_PRESENCE")
    assert "MN-07" in presence.detail


def test_unexpected_node_fails_closed():
    nodes = healthy_nodes()
    nodes.append({**copy.deepcopy(nodes[0]), "node_id": "MN-99"})
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any("MN-99" in f.detail for f in report.failed)


def test_duplicate_node_ids_fail_closed():
    nodes = healthy_nodes()
    nodes[8] = copy.deepcopy(nodes[7])
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False


def test_wrong_kernel_version_fails_closed():
    nodes = healthy_nodes()
    nodes[3]["kernel_version"] = "0.9.0"
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "KERNEL_VERSION" for f in report.failed)


def test_inactive_node_fails_closed():
    nodes = healthy_nodes()
    nodes[2]["status"] = "DRAFT"
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "NODE_STATUS" for f in report.failed)


def test_unverified_node_fails_closed():
    nodes = healthy_nodes()
    nodes[5]["verified"] = False
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any("MN-06" in f.detail for f in report.failed)


def test_broken_relationship_chain_fails_closed():
    nodes = healthy_nodes()
    nodes[3]["relationships"]["next"] = "MN-09"
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "NODE_RELATIONSHIPS" for f in report.failed)


def test_terminal_node_with_next_fails_closed():
    nodes = healthy_nodes()
    nodes[8]["relationships"]["next"] = "MN-01"
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False


def test_node_without_governance_binding_fails_closed():
    nodes = healthy_nodes()
    nodes[0]["governance_bindings"] = []
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "GOVERNANCE_BINDINGS" for f in report.failed)


def test_node_without_enforcement_point_fails_closed():
    """A governing node with no machine enforcement is documentation only."""
    nodes = healthy_nodes()
    nodes[6]["enforcement_point"] = None
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "ENFORCEMENT_COVERAGE" for f in report.failed)


def test_declared_conflict_fails_closed():
    nodes = healthy_nodes()
    nodes[4]["conflicts"] = ["MN-04 redefines intelligence_atom"]
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "NODE_CONFLICTS" for f in report.failed)


def test_stale_node_fails_closed():
    # Absolute past date, deliberately NOT derived from MAX_AGE_DAYS: a test
    # computed from the constant it protects cannot detect constant tampering.
    nodes = healthy_nodes()
    nodes[0]["observed_at"] = "2020-01-01"
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    assert any(f.check == "NODE_FRESHNESS" for f in report.failed)


def test_recent_node_is_not_stale():
    nodes = healthy_nodes()
    nodes[0]["observed_at"] = "2026-09-25"
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert any(f.check == "NODE_FRESHNESS" and f.status == "PASS"
               for f in report.findings)


def test_missing_observed_at_is_unknown_not_pass():
    nodes = healthy_nodes()
    nodes[1].pop("observed_at")
    report = kb.boot_kernel(lambda: nodes, HEALTHY_PAYLOAD)
    assert report.boot_permitted is False
    freshness = next(f for f in report.findings if f.check == "NODE_FRESHNESS")
    assert freshness.status == "UNKNOWN"


def test_missing_next_action_fails_closed():
    report = kb.boot_kernel(lambda: healthy_nodes(), {})
    assert report.boot_permitted is False
    assert any(f.check == "NEXT_ACTION" for f in report.failed)


def test_multiple_next_actions_fail_closed():
    payload = {"next_action": "Merge #801. Then also deploy the Hub."}
    report = kb.boot_kernel(lambda: healthy_nodes(), payload)
    assert report.boot_permitted is False
    assert any(f.check == "NEXT_ACTION" and "ONE action" in f.detail
               for f in report.failed)


def test_assert_bootable_raises_on_unproven_kernel():
    report = kb.boot_kernel(lambda: healthy_nodes(), {})
    with pytest.raises(kb.KernelIntegrityError):
        kb.assert_bootable(report)


def test_assert_bootable_passes_on_healthy_kernel():
    report = kb.boot_kernel(lambda: healthy_nodes(), HEALTHY_PAYLOAD)
    kb.assert_bootable(report)


def test_source_exception_never_yields_empty_healthy_kernel():
    def exploding_source():
        raise RuntimeError("receiver timeout")

    report = kb.boot_kernel(exploding_source)
    assert report.boot_permitted is False
    assert report.loaded == []
    assert report.findings[0].status == "UNKNOWN"
    assert "receiver timeout" in report.findings[0].detail


def test_repo_mirror_source_absent_is_filenotfound(tmp_path):
    with pytest.raises(FileNotFoundError):
        kb.repo_mirror_source(tmp_path)


def test_repo_mirror_source_rejects_malformed(tmp_path):
    bad = tmp_path / ".naya/control-plane/MASTER-NODE-KERNEL.json"
    bad.parent.mkdir(parents=True)
    bad.write_text(json.dumps({"nodes": "not-a-list"}), encoding="utf-8")
    with pytest.raises(ValueError):
        kb.repo_mirror_source(tmp_path)


def test_repo_mirror_source_roundtrip(tmp_path):
    path = tmp_path / ".naya/control-plane/MASTER-NODE-KERNEL.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"nodes": healthy_nodes()}), encoding="utf-8")
    loaded = kb.repo_mirror_source(tmp_path)
    assert len(loaded) == 9
    report = kb.boot_kernel(lambda: kb.repo_mirror_source(tmp_path), HEALTHY_PAYLOAD)
    assert report.boot_permitted is True


def test_non_dict_records_are_filtered_not_trusted():
    report = kb.boot_kernel(lambda: healthy_nodes() + ["junk", None], HEALTHY_PAYLOAD)
    assert report.boot_permitted is True          # 9 real records survived
    assert len(report.loaded) == 9


def test_report_serializes_for_receipt():
    report = kb.boot_kernel(lambda: healthy_nodes(), HEALTHY_PAYLOAD)
    blob = json.dumps(report.to_dict(), sort_keys=True)
    assert '"boot_permitted": true' in blob
    assert json.loads(blob)["authority"] == "NONE"
