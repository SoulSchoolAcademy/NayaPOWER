#!/usr/bin/env python3
"""Tests for the learning convergence audit (B/C/D cross-check).

Fixture-log tests: synthetic clock + meta logs prove the predicate logic.
The live-log run is a separate demonstration (see the run log), not a
unit test — tests must stay hermetic.

Cases:
  - full T0-T7 chain, all typed evidence present, judge != author
    -> B PASS, C PASS, D PASS, E earned E0, DIVERGENCE flagged (the
    honest convergence hole: T6 meta carries no ladder-shaped evidence,
    so the ladder cannot agree the lesson is verified).
  - gap (missing T1) -> B GAP, E UNPROVEN.
  - clock row without meta row -> B CLOCK_WITHOUT_META.
  - orphan meta row -> B META_WITHOUT_CLOCK.
  - duplicate clock row -> B DUPLICATE_CLOCK.
  - ts regression -> B TS_REGRESSION.
  - T6 judge == author -> C FAIL at T6 (Inviolable), D not PASS.
  - T6_PROBE FAIL + no T6 -> D ABSENT, probe recorded, not verified.
  - T3 enforcement < 20 chars -> C FAIL at T3.
  - T4 principle_ids missing this lesson -> C FAIL at T4.
  - bulk ts: 3 lessons sharing one (stage, ts) -> BULK_TS signal.
  - malformed JSONL line -> counted, not fatal.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from learning_convergence_audit import audit  # noqa: E402

HEX64 = "a" * 64
HEX40 = "b" * 40
T0 = "2026-10-14T04:00:00+00:00"


def _clock(lid, stage, ts):
    return {"lesson_id": lid, "stage": stage,
            "stage_name": f"T{stage}", "ts": ts}


def _meta(lid, stage, **kw):
    row = {"lesson_id": lid, "stage": stage,
           "stage_name": f"T{stage}", "ts": kw.pop("ts", T0),
           "title": kw.pop("title", "t"), "evidence": kw.pop("evidence", "ev")}
    row.update(kw)
    return row


def _full_chain(lid, t6_judge="Naya Beta", t6_author="Naya Alpha",
                t6_verdict="PASS"):
    clock = [_clock(lid, s, f"2026-10-14T04:0{s}:00+00:00") for s in range(8)]
    meta = [
        _meta(lid, 0, title="principle title"),
        _meta(lid, 1),
        _meta(lid, 2),
        _meta(lid, 3, principle="One sentence only.",
              enforcement="without this the next worker repeats it"),
        _meta(lid, 4, brief_hash=HEX64, principle_ids=[lid]),
        _meta(lid, 5, changed_decision="I checked ls -la first"),
        _meta(lid, 6, judge_seat=t6_judge, author_seat=t6_author,
              verdict=t6_verdict),
        _meta(lid, 7, pr=1234, merge_sha=HEX40),
    ]
    return clock, meta


def _run(clock_rows, meta_rows):
    with tempfile.TemporaryDirectory() as d:
        cp = Path(d) / "clock.jsonl"
        mp = Path(d) / "meta.jsonl"
        cp.write_text("".join(json.dumps(r) + "\n" for r in clock_rows))
        mp.write_text("".join(json.dumps(r) + "\n" for r in meta_rows))
        return audit(cp, mp)


def test_full_chain_passes_b_c_d_and_flags_divergence():
    clock, meta = _full_chain("LC-20261014-001")
    result = _run(clock, meta)
    (entry,) = result["lessons"]
    assert entry["B_lineage"] == "PASS", entry["B_failures"]
    assert entry["C_evidence"] == "PASS", entry["C_failures"]
    assert entry["D_receipt"] == "PASS"
    assert entry["D_latency_min"] == 6.0
    assert entry["E_earned"] == "E0_EXPOSED"
    assert entry["E_divergence"], "T6 + ladder E0 must flag divergence"
    assert result["summary"]["bulk_ts_signals"] == []


def test_gap_missing_t1():
    clock, meta = _full_chain("LC-20261014-001")
    clock = [r for r in clock if r["stage"] != 1]
    meta = [r for r in meta if r["stage"] != 1]
    (entry,) = _run(clock, meta)["lessons"]
    assert entry["B_lineage"] == "FAIL"
    assert any("GAP" in f for f in entry["B_failures"])
    assert entry["E_earned"] == "UNPROVEN"


def test_clock_without_meta():
    clock, meta = _full_chain("LC-20261014-001")
    meta = [r for r in meta if r["stage"] != 2]
    (entry,) = _run(clock, meta)["lessons"]
    assert any("CLOCK_WITHOUT_META" in f for f in entry["B_failures"])


def test_orphan_meta():
    clock, meta = _full_chain("LC-20261014-001")
    clock = [r for r in clock if r["stage"] != 7]
    (entry,) = _run(clock, meta)["lessons"]
    assert any("META_WITHOUT_CLOCK" in f for f in entry["B_failures"])


def test_duplicate_clock_row():
    clock, meta = _full_chain("LC-20261014-001")
    clock.append(_clock("LC-20261014-001", 2, "2026-10-14T04:02:00+00:00"))
    (entry,) = _run(clock, meta)["lessons"]
    assert entry["B_lineage"] == "FAIL"
    assert any("DUPLICATE_CLOCK" in f for f in entry["B_failures"])


def test_ts_regression():
    clock, meta = _full_chain("LC-20261014-001")
    for r in clock:
        if r["stage"] == 3:
            r["ts"] = "2026-10-14T03:00:00+00:00"
    (entry,) = _run(clock, meta)["lessons"]
    assert any("TS_REGRESSION" in f for f in entry["B_failures"])


def test_t6_self_judge_fails_c_and_blocks_d():
    clock, meta = _full_chain("LC-20261014-001",
                              t6_judge="Naya Alpha", t6_author="Naya Alpha")
    (entry,) = _run(clock, meta)["lessons"]
    assert entry["C_evidence"] == "FAIL"
    assert any("Inviolable" in f for f in entry["C_failures"])
    assert entry["D_receipt"] == "PARTIAL"  # T5 exists, T6 not credited


def test_failed_probe_is_not_verification():
    clock, meta = _full_chain("LC-20261014-001")
    clock = [r for r in clock if r["stage"] not in (6, 7)]
    meta = [r for r in meta if r["stage"] not in (6, 7)]
    probe = {"lesson_id": "LC-20261014-001", "stage": "T6_PROBE",
             "stage_name": "T6_PROBE (verdict recorded, no T6 emitted)",
             "ts": "2026-10-14T04:06:00+00:00", "written_ts": "2026-10-14T04:06:00+00:00",
             "title": None, "evidence": "judge transcript",
             "judge_seat": "Naya Beta", "author_seat": "Naya Alpha",
             "verdict": "FAIL"}
    meta.append(probe)
    (entry,) = _run(clock, meta)["lessons"]
    assert entry["D_receipt"] == "PARTIAL"  # T5 exists, no T6 emitted
    assert entry["D_probes"] == [{"verdict": "FAIL", "judge_seat": "Naya Beta",
                                  "author_seat": "Naya Alpha",
                                  "ts": "2026-10-14T04:06:00+00:00"}]
    assert entry["E_divergence"] == ""  # no T6 claimed, no divergence


def test_t3_short_enforcement_fails_c():
    clock, meta = _full_chain("LC-20261014-001")
    for r in meta:
        if r["stage"] == 3:
            r["enforcement"] = "too short"
    (entry,) = _run(clock, meta)["lessons"]
    assert entry["C_evidence"] == "FAIL"
    assert any("T3 enforcement" in f for f in entry["C_failures"])


def test_t4_missing_self_id_fails_c():
    clock, meta = _full_chain("LC-20261014-001")
    for r in meta:
        if r["stage"] == 4:
            r["principle_ids"] = ["LC-20261014-999"]
    (entry,) = _run(clock, meta)["lessons"]
    assert entry["C_evidence"] == "FAIL"
    assert any("T4 principle_ids" in f for f in entry["C_failures"])


def test_bulk_ts_signal():
    clock, meta = [], []
    for i in (1, 2, 3):
        lid = f"LC-20261014-00{i}"
        clock.append(_clock(lid, 0, f"2026-10-14T04:00:0{i}+00:00"))
        clock.append(_clock(lid, 1, T0))  # same (stage, ts) x3
        meta.append(_meta(lid, 0, title="t"))
        meta.append(_meta(lid, 1))
    result = _run(clock, meta)
    assert result["summary"]["bulk_ts_signals"] == [
        {"stage": 1, "ts": T0,
         "lessons": ["LC-20261014-001", "LC-20261014-002", "LC-20261014-003"],
         "count": 3}
    ]


def test_malformed_lines_counted_not_fatal():
    with tempfile.TemporaryDirectory() as d:
        cp = Path(d) / "clock.jsonl"
        mp = Path(d) / "meta.jsonl"
        cp.write_text('{"lesson_id": "LC-20261014-001", "stage": 0, "ts": "'
                      + T0 + '"}\nNOT JSON\n')
        mp.write_text('{"lesson_id": "LC-20261014-001", "stage": 0, "ts": "'
                      + T0 + '", "title": "t", "evidence": "ev"}\n')
        result = audit(cp, mp)
    assert result["malformed_lines"] == {"clock": 1, "meta": 0}
    (entry,) = result["lessons"]
    assert entry["B_lineage"] == "PASS"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-q"]))
