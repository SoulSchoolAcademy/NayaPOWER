"""Hermetic tests for tools/evolve_meta_trend.py.

CLI-level; the repo is never mutated. Fixture bundles are synthesized in tmp
dirs with the exact evolve_meta_learning.py v1 envelope schema.
"""

import hashlib
import json
import os
import subprocess
import sys

TOOL = os.path.join(
    os.path.dirname(__file__), "..", "tools", "evolve_meta_trend.py"
)


def _bundle(**over):
    metrics = {
        "total_entries": 100,
        "ingestion_velocity": {
            "per_day": {"2026-10-08": 40, "2026-10-09": 10},
            "days_covered": 2,
            "peak_day": "2026-10-08",
        },
        "status_mix": {
            "counts": {"FLAGGED_AUTHORITY": 10, "INGESTED": 89, "RATIFIED": 1},
            "fractions": {"FLAGGED_AUTHORITY": 0.1, "INGESTED": 0.89, "RATIFIED": 0.01},
        },
        "integration_coverage": {
            "integrated": 99,
            "denominator": 99,
            "fraction": 1.0,
            "note": "",
        },
        "stale_unintegrated": {
            "threshold_days": 7,
            "count": 2,
            "ids": ["SN-0001", "SN-0002"],
            "note": "",
        },
        "calibration_churn": {
            "count": 3,
            "fraction_of_total": 0.03,
            "ids": ["SN-0010", "SN-0011", "SN-0012"],
            "note": "",
        },
        "receipt_health": {
            "receipts_dir_present": True,
            "found": 99,
            "missing": 1,
            "checks_pass": 200,
            "checks_fail": 0,
            "missing_ids": ["SN-0099"],
        },
        "authority_gate_load": {
            "flagged": 10,
            "fraction_of_total": 0.1,
            "note": "",
        },
    }
    metrics.update(over.get("metrics", {}))
    return {
        "tool": "evolve_meta_learning",
        "version": 1,
        "generated_at": over.get("generated_at", "2026-10-09T14:00:00+00:00"),
        "learn_root": "/tmp/learn",
        "ledger": {"version": 1},
        "metrics": metrics,
        "caveats": [],
    }


def _write(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)


def _run(*args):
    return subprocess.run(
        [sys.executable, TOOL, *args],
        capture_output=True,
        text=True,
    )


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def test_delta_math_exact(tmp_path):
    b = _bundle()
    c = _bundle(
        generated_at="2026-10-09T20:00:00+00:00",
        metrics={
            **_bundle()["metrics"],
            "total_entries": 130,
            "ingestion_velocity": {
                "per_day": {"2026-10-08": 40, "2026-10-09": 46, "2026-10-10": 5},
                "days_covered": 3,
                "peak_day": "2026-10-09",
            },
            "status_mix": {
                "counts": {"FLAGGED_AUTHORITY": 12, "INGESTED": 116, "RATIFIED": 2},
                "fractions": {
                    "FLAGGED_AUTHORITY": 12 / 130,
                    "INGESTED": 116 / 130,
                    "RATIFIED": 2 / 130,
                },
            },
            "integration_coverage": {
                "integrated": 129,
                "denominator": 129,
                "fraction": 1.0,
                "note": "",
            },
        },
    )
    bp, cp, op = tmp_path / "a.json", tmp_path / "b.json", tmp_path / "t.json"
    _write(bp, b)
    _write(cp, c)
    r = _run("--baseline", str(bp), "--current", str(cp), "--out", str(op))
    assert r.returncode == 0, r.stderr
    t = json.loads(op.read_text())
    d = t["deltas"]
    assert d["entries_delta"] == 30
    assert d["ingestion_velocity_per_day"] == {
        "2026-10-08": 0,
        "2026-10-09": 36,
        "2026-10-10": 5,
    }
    assert d["status_mix"]["RATIFIED"]["count_delta"] == 1
    assert d["status_mix"]["INGESTED"]["fraction_delta"] == round(116 / 130 - 0.89, 6)
    assert d["integration_coverage_fraction_delta"] == 0.0


def test_id_set_deltas(tmp_path):
    b = _bundle()
    m = dict(_bundle()["metrics"])
    m["stale_unintegrated"] = {
        "threshold_days": 7,
        "count": 1,
        "ids": ["SN-0002"],
        "note": "",
    }
    m["calibration_churn"] = {
        "count": 4,
        "fraction_of_total": 0.04,
        "ids": ["SN-0010", "SN-0011", "SN-0012", "SN-0020"],
        "note": "",
    }
    m["receipt_health"] = {
        "receipts_dir_present": True,
        "found": 100,
        "missing": 0,
        "checks_pass": 210,
        "checks_fail": 0,
        "missing_ids": [],
    }
    c = _bundle(metrics=m)
    bp, cp, op = tmp_path / "a.json", tmp_path / "b.json", tmp_path / "t.json"
    _write(bp, b)
    _write(cp, c)
    r = _run("--baseline", str(bp), "--current", str(cp), "--out", str(op))
    assert r.returncode == 0, r.stderr
    t = json.loads(op.read_text())
    d = t["deltas"]
    assert d["stale_learning_debt"]["count_delta"] == -1
    assert d["stale_learning_debt"]["newly_stale"] == []
    assert d["stale_learning_debt"]["resolved"] == ["SN-0001"]
    assert d["calibration_churn"]["new_self_corrections"] == ["SN-0020"]
    assert d["receipt_health"]["newly_missing"] == []
    assert d["receipt_health"]["recovered"] == ["SN-0099"]
    assert d["receipt_health"]["checks_pass_delta"] == 10


def test_threshold_mismatch_warns_not_fails(tmp_path):
    b = _bundle()
    m = dict(_bundle()["metrics"])
    m["stale_unintegrated"] = dict(m["stale_unintegrated"], threshold_days=14)
    c = _bundle(metrics=m)
    bp, cp, op = tmp_path / "a.json", tmp_path / "b.json", tmp_path / "t.json"
    _write(bp, b)
    _write(cp, c)
    r = _run("--baseline", str(bp), "--current", str(cp), "--out", str(op))
    assert r.returncode == 0, r.stderr
    t = json.loads(op.read_text())
    assert t["threshold_mismatch"] is True
    assert any("WARNING" in cv for cv in t["caveats"])


def test_fail_closed_paths(tmp_path):
    good = tmp_path / "good.json"
    _write(good, _bundle())
    out = tmp_path / "t.json"

    # missing baseline file
    r = _run("--baseline", str(tmp_path / "nope.json"), "--current", str(good),
             "--out", str(out))
    assert r.returncode == 2 and "not found" in r.stderr

    # malformed JSON
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    r = _run("--baseline", str(bad), "--current", str(good), "--out", str(out))
    assert r.returncode == 2 and "not valid JSON" in r.stderr

    # no metrics mapping
    nomet = tmp_path / "nomet.json"
    _write(nomet, {"tool": "x", "version": 1})
    r = _run("--baseline", str(nomet), "--current", str(good), "--out", str(out))
    assert r.returncode == 2 and "no metrics mapping" in r.stderr

    # envelope version mismatch
    v2 = tmp_path / "v2.json"
    b = _bundle()
    b["version"] = 2
    _write(v2, b)
    r = _run("--baseline", str(v2), "--current", str(good), "--out", str(out))
    assert r.returncode == 2 and "envelope version" in r.stderr

    # missing metric block
    thin = tmp_path / "thin.json"
    b = _bundle()
    del b["metrics"]["receipt_health"]
    _write(thin, b)
    r = _run("--baseline", str(thin), "--current", str(good), "--out", str(out))
    assert r.returncode == 2 and "missing metric blocks" in r.stderr


def test_no_score_anywhere_and_inputs_untouched(tmp_path):
    b = _bundle()
    c = _bundle()
    bp, cp, op = tmp_path / "a.json", tmp_path / "b.json", tmp_path / "t.json"
    _write(bp, b)
    _write(cp, c)
    sha_b, sha_c = _sha(bp), _sha(cp)
    r = _run("--baseline", str(bp), "--current", str(cp), "--out", str(op))
    assert r.returncode == 0, r.stderr
    assert _sha(bp) == sha_b and _sha(cp) == sha_c  # read-only
    raw = op.read_text()
    assert '"score"' not in raw  # honesty boundary: no machine scoring
    t = json.loads(raw)
    assert t["tool"] == "evolve_meta_trend"
    assert t["version"] == 1
    assert t["baseline"]["total_entries"] == 100
    assert "caveats" in t and len(t["caveats"]) >= 4
