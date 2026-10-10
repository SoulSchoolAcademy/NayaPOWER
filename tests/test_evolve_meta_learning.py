#!/usr/bin/env python3
"""Hermetic tests for tools/evolve_meta_learning.py.

Every test builds its own fixture learn-state under tmp_path; the repository
is never touched. The tool is invoked at the CLI level (subprocess) so the
fail-closed exit codes are exercised exactly as a user would see them.
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parent.parent / "tools" / "evolve_meta_learning.py"

NOW = datetime.now(timezone.utc)


def iso(days_ago: int) -> str:
    return (NOW - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def entry(status="INGESTED", days_ago=1, integrations=None, supersedes=None,
          classification="REUSABLE"):
    e = {
        "ingested_at": iso(days_ago),
        "status": status,
        "classification": classification,
        "blob_sha": "0" * 40,
        "content_sha256": "1" * 64,
        "repo_path": "BRAIN/05-MEMORY/SMART-NOTES/x.md",
        "run_id": "20261009T024500Z",
    }
    if integrations is not None:
        e["integrations"] = [{"anchor": "## x", "target": t} for t in integrations]
    if supersedes is not None:
        e["supersedes"] = supersedes
    return e


def write_learn_root(root: Path, entries: dict, receipts: dict | None = None) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "ledger.json").write_text(json.dumps({
        "version": 1,
        "branch": "fixture",
        "branch_sha_at_scan": "abc",
        "updated_at": iso(0),
        "entries": entries,
    }), encoding="utf-8")
    if receipts:
        rdir = root / "receipts"
        rdir.mkdir(exist_ok=True)
        for sn_id, payload in receipts.items():
            (rdir / f"{sn_id}.json").write_text(json.dumps(payload), encoding="utf-8")
    return root


def run_scan(learn_root: Path, out: Path, extra: list[str] | None = None):
    cmd = [sys.executable, str(TOOL), "scan",
           "--learn-root", str(learn_root), "--out", str(out)]
    if extra:
        cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


def load_bundle(out: Path) -> dict:
    return json.loads(out.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Happy path: the metrics are actually measured
# ---------------------------------------------------------------------------

def test_scan_fixture_metrics(tmp_path):
    """Six-entry fixture: statuses, velocity, coverage, churn, staleness."""
    entries = {
        "SN-A": entry("INGESTED", days_ago=1, integrations=["learn/lessons.md"]),
        "SN-B": entry("INGESTED", days_ago=1, integrations=["learn/lessons.md", "AGENTS.md"]),
        "SN-C": entry("FLAGGED_AUTHORITY", days_ago=2),
        "SN-D": entry("RATIFIED", days_ago=3, integrations=["learn/doctrine.md"]),
        "SN-E": entry("INGESTED", days_ago=30),                      # stale debt
        "SN-F": entry("INGESTED", days_ago=2, supersedes="SN-A"),    # churn
    }
    root = write_learn_root(tmp_path / "learn", entries)
    out = tmp_path / "bundle.json"
    proc = run_scan(root, out)
    assert proc.returncode == 0, proc.stderr
    b = load_bundle(out)
    m = b["metrics"]

    assert m["total_entries"] == 6
    assert m["learnable_entries"] == 6
    assert m["status_mix"]["counts"] == {"INGESTED": 4, "FLAGGED_AUTHORITY": 1, "RATIFIED": 1}
    assert m["status_mix"]["fractions"]["INGESTED"] == pytest.approx(4 / 6, abs=1e-4)

    # Velocity buckets keyed by UTC date; SN-E backfilled 30 days ago.
    vel = m["ingestion_velocity"]["per_day"]
    assert sum(vel.values()) == 6
    assert m["ingestion_velocity"]["days_covered"] == len(vel)

    # Coverage: 3 integrated of 6.
    assert m["integration_coverage"]["integrated"] == 3
    assert m["integration_coverage"]["fraction"] == pytest.approx(0.5, abs=1e-4)

    # Targets counted per integration, not per entry.
    assert m["integration_targets"]["learn/lessons.md"] == 2
    assert m["integration_targets"]["AGENTS.md"] == 1
    assert m["integration_targets"]["learn/doctrine.md"] == 1

    # Staleness: only SN-E (30 days, unintegrated). SN-F is 2 days old.
    assert m["stale_unintegrated"]["ids"] == ["SN-E"]
    assert m["stale_unintegrated"]["threshold_days"] == 7

    # Churn: only SN-F supersedes.
    assert m["calibration_churn"]["ids"] == ["SN-F"]
    assert m["calibration_churn"]["count"] == 1

    # Authority gate load.
    assert m["authority_gate_load"]["flagged"] == 1


def test_duplicates_excluded_from_coverage_denominator(tmp_path):
    entries = {
        "SN-A": entry("INGESTED", integrations=["learn/lessons.md"]),
        "SN-B": entry("DUPLICATE_OF"),
    }
    root = write_learn_root(tmp_path / "learn", entries)
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    cov = load_bundle(out)["metrics"]["integration_coverage"]
    assert cov["denominator"] == 1
    assert cov["fraction"] == pytest.approx(1.0, abs=1e-4)


def test_stale_boundary_is_strictly_greater(tmp_path):
    entries = {
        "SN-OLD": entry("INGESTED", days_ago=8),
        "SN-EDGE": entry("INGESTED", days_ago=7),
    }
    root = write_learn_root(tmp_path / "learn", entries)
    out = tmp_path / "bundle.json"
    assert run_scan(root, out, ["--stale-days", "7"]).returncode == 0
    ids = load_bundle(out)["metrics"]["stale_unintegrated"]["ids"]
    assert ids == ["SN-OLD"]


def test_calibration_churn_accepts_string_and_list(tmp_path):
    entries = {
        "SN-A": entry("INGESTED", supersedes="SN-OLD1"),
        "SN-B": entry("INGESTED", supersedes=["SN-OLD2", "SN-OLD3"]),
        "SN-C": entry("INGESTED", supersedes=None),
    }
    root = write_learn_root(tmp_path / "learn", entries)
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    churn = load_bundle(out)["metrics"]["calibration_churn"]
    assert churn["count"] == 2
    assert churn["ids"] == ["SN-A", "SN-B"]


# ---------------------------------------------------------------------------
# Receipt health
# ---------------------------------------------------------------------------

def test_receipt_health_counts(tmp_path):
    entries = {
        "SN-A": entry("INGESTED", integrations=["learn/lessons.md"]),
        "SN-B": entry("INGESTED"),
        "SN-C": entry("INGESTED"),
    }
    receipts = {
        "SN-A": {"sn_id": "SN-A", "checks": [
            {"check": "file_contains", "result": "PASS"},
            {"check": "template_render_check", "result": "PASS"}]},
        "SN-B": {"sn_id": "SN-B", "checks": [
            {"check": "file_contains", "result": "FAIL"}]},
    }
    root = write_learn_root(tmp_path / "learn", entries, receipts)
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    rh = load_bundle(out)["metrics"]["receipt_health"]
    assert rh["receipts_dir_present"] is True
    assert rh["found"] == 2
    assert rh["missing"] == 1
    assert rh["missing_ids"] == ["SN-C"]
    assert rh["checks_pass"] == 2
    assert rh["checks_fail"] == 1


def test_no_receipts_dir_is_not_a_crash(tmp_path):
    root = write_learn_root(tmp_path / "learn", {"SN-A": entry()})
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    rh = load_bundle(out)["metrics"]["receipt_health"]
    assert rh["receipts_dir_present"] is False
    assert rh["missing"] == 0


# ---------------------------------------------------------------------------
# Fail-closed input handling
# ---------------------------------------------------------------------------

def test_missing_learn_root_fail_closed(tmp_path):
    out = tmp_path / "bundle.json"
    proc = run_scan(tmp_path / "nope", out)
    assert proc.returncode == 2
    assert not out.exists()


def test_missing_ledger_fail_closed(tmp_path):
    root = tmp_path / "learn"
    root.mkdir()
    out = tmp_path / "bundle.json"
    proc = run_scan(root, out)
    assert proc.returncode == 2
    assert "ledger.json" in proc.stderr


def test_malformed_ledger_fail_closed(tmp_path):
    root = tmp_path / "learn"
    root.mkdir()
    (root / "ledger.json").write_text("{not json", encoding="utf-8")
    out = tmp_path / "bundle.json"
    proc = run_scan(root, out)
    assert proc.returncode == 2
    assert not out.exists()


def test_ledger_without_entries_mapping_fail_closed(tmp_path):
    root = tmp_path / "learn"
    root.mkdir()
    (root / "ledger.json").write_text(json.dumps({"version": 1}), encoding="utf-8")
    out = tmp_path / "bundle.json"
    proc = run_scan(root, out)
    assert proc.returncode == 2
    assert "entries" in proc.stderr


def test_negative_stale_days_refused(tmp_path):
    root = write_learn_root(tmp_path / "learn", {"SN-A": entry()})
    out = tmp_path / "bundle.json"
    proc = run_scan(root, out, ["--stale-days", "-1"])
    assert proc.returncode == 2


# ---------------------------------------------------------------------------
# Honesty boundaries
# ---------------------------------------------------------------------------

def _walk(obj):
    if isinstance(obj, dict):
        yield from obj.keys()
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def test_bundle_carries_no_score(tmp_path):
    root = write_learn_root(tmp_path / "learn", {"SN-A": entry("RATIFIED", integrations=["x"])})
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    keys = {k.lower() for k in _walk(load_bundle(out))}
    assert "score" not in keys, "the instrument must never score its own learning"


def test_caveats_present_and_nonempty(tmp_path):
    root = write_learn_root(tmp_path / "learn", {"SN-A": entry()})
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    caveats = load_bundle(out)["metrics"] and load_bundle(out)["caveats"]
    assert isinstance(caveats, list) and len(caveats) >= 3


def test_scan_is_read_only_on_learn_root(tmp_path):
    entries = {"SN-A": entry("INGESTED", integrations=["learn/lessons.md"])}
    receipts = {"SN-A": {"sn_id": "SN-A", "checks": []}}
    root = write_learn_root(tmp_path / "learn", entries, receipts)
    before = {p.relative_to(root) for p in root.rglob("*")}
    out = tmp_path / "bundle.json"
    assert run_scan(root, out).returncode == 0
    after = {p.relative_to(root) for p in root.rglob("*")}
    assert before == after, "scan must not write into --learn-root"
