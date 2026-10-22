"""Tests for tools/learning_scorecard.py (v2).

The instrument's v1 failure mode was silent blindness: the log format
moved and the parser printed zeros for days. These tests pin (a) every
format the log has actually used, and (b) the drift alarm: when the
format moves beyond the parsers, the run must fail loudly (exit 3 /
ParserDriftError), never report zeros.
"""
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
_spec = importlib.util.spec_from_file_location(
    "learning_scorecard", Path(__file__).resolve().parent.parent / "tools" / "learning_scorecard.py")
lsc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lsc)

NOW = datetime(2026, 10, 22, 0, 30, tzinfo=timezone.utc)

CURRENT_LOG = """# LEARNING-LOG — running record

## Built in the open

prose

## Distillation v2 — iteration 207 — 2026-10-21 ~23:58Z

### New lessons

- **L700 [F9] NEW FILING (promoted):** a lesson about citations.
- **L701 [F1] NEW FILING:** a second lesson.

### Repeats

- **L600 [F1] ×3 in one review (gate-integrity thread).** Not a filing.

### Intelligent events

1. **L650 → repair landed and a lesson counted as learned only after filing.**
2. **A seat verified a claim at the primary source before acting.**

## Distillation v2 — iteration 206 — 2026-10-21 ~22:00Z

### New lessons

- **WP-300 (1/3) NEW FILING [F7]:** a win pattern about cures.
"""

LEGACY_LOG = """# LEARNING-LOG

## 2026-10-21T06:15:00Z

- **L24 — Mechanical green ≠ behavioral green.** A legacy bullet lesson.
- **L25 — A second legacy lesson.**

**Intelligent events (2 adoptions):** two things were adopted.
"""

DRIFT_LOG = """# LEARNING-LOG

## Distillation v3 — cycle 9 — 2026-10-21 ~23:58Z

### Fresh learnings

- **LESSON-700 [F9]:** the format moved again.
""" + "\n".join(f"- reference to L{100 + i} in prose only" for i in range(60)) + "\n"

FAMILIES = """# LESSON FAMILIES

## F1 — CLAIMED VS VERIFIED

- **Iterations:** 100 → 207.
- **Days since repeat:** 0 (fired in iteration 207).
- **Instances (iteration 207 delta):** **L613 ×2** across one batch.

## F2 — STALE STATE SERVED AS CURRENT

- **Days since repeat:** 3 (fired in iteration 200).
- **Instances (iteration 200 delta):** **L590 ×1**.
"""


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_current_format_parses_filings_and_events(tmp_path):
    log = _write(tmp_path, "log.md", CURRENT_LOG)
    fam = _write(tmp_path, "fam.md", FAMILIES)
    agents = _write(tmp_path, "agents.md", "# none\n")
    out = lsc.compute(log, fam, agents, now=NOW)
    assert out["total_lessons_logged"] == 2          # L700, L701 — not L600 (a repeat)
    assert out["win_patterns_7d"] == 1               # WP-300
    assert out["adoption_intelligent_events_7d"] == 2
    assert out["capture_rate_per_day"] > 0
    assert out["drift_check"] == "ok"


def test_legacy_format_still_parses(tmp_path):
    log = _write(tmp_path, "log.md", LEGACY_LOG)
    fam = _write(tmp_path, "fam.md", FAMILIES)
    agents = _write(tmp_path, "agents.md", "# none\n")
    out = lsc.compute(log, fam, agents, now=NOW)
    assert out["total_lessons_logged"] == 2
    assert out["adoption_intelligent_events_7d"] == 2  # the batch's own stated count


def test_parser_drift_fails_loudly(tmp_path):
    log = _write(tmp_path, "log.md", DRIFT_LOG)
    fam = _write(tmp_path, "fam.md", FAMILIES)
    agents = _write(tmp_path, "agents.md", "# none\n")
    try:
        lsc.compute(log, fam, agents, now=NOW)
    except lsc.ParserDriftError:
        pass
    else:
        raise AssertionError("drifted format must raise ParserDriftError, not zeros")
    rc = lsc.main(["--log", str(log), "--families", str(fam),
                   "--agents-md", str(agents), "--json"])
    assert rc == 3


def test_families_current_format():
    fams = lsc.parse_families(FAMILIES)
    assert [f["id"] for f in fams] == ["F1", "F2"]
    assert fams[0]["days_since_repeat"] == 0
    assert fams[1]["days_since_repeat"] == 3
    assert fams[0]["instance_mentions"] >= 2
