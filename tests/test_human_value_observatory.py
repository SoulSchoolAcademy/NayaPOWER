"""Tests for the Human Value Observatory live-run loop (tools/human_value/observatory.py).

The observatory is the loop that keeps measurement running live:
scan (mechanical drafts, no judgment) -> promote (explicit lane act, fail
closed) -> recompute -> trend snapshot -> pinned report.

These tests prove the honesty seams, not just the happy path:
- drafts are deliberately NOT ledgerable (the machine cannot credit itself)
- promote refuses THIN/NO VALUE/DISQUALIFIED, duplicates, and missing --confirm
- the report is byte-deterministic from ledger+trend bytes alone
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.human_value import compute_hv, observatory  # noqa: E402
from tools.human_value.schema import SchemaError, validate_event  # noqa: E402


# ---------------------------------------------------------------- fixtures

def _git(repo: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, timeout=60)
    assert p.returncode == 0, f"git {' '.join(args)} failed: {p.stderr[:300]}"
    return p.stdout


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A small git repo: linear commits interleaved with two merges."""
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "test@example.com")
    _git(r, "config", "user.name", "Test")
    _git(r, "config", "commit.gpgsign", "false")

    def commit(name: str, text: str = "x"):
        (r / name).write_text(text)
        _git(r, "add", name)
        _git(r, "commit", "-q", "-m", f"add {name}")

    commit("a.txt")
    base = _git(r, "rev-parse", "HEAD").strip()  # scan base: before M1
    commit("b.txt")
    _git(r, "checkout", "-q", "-b", "feature-a")
    commit("feat-a.txt", "feature a work")
    _git(r, "checkout", "-q", "-")
    _git(r, "merge", "-q", "--no-ff", "-m",
         "Merge pull request #9001 from test/feature-a", "feature-a")
    m1 = _git(r, "rev-parse", "HEAD").strip()
    commit("c.txt")
    _git(r, "checkout", "-q", "-b", "feature-b")
    commit("feat-b.txt", "feature b work")
    _git(r, "checkout", "-q", "-")
    _git(r, "merge", "-q", "--no-ff", "-m", "Merge branch 'feature-b'",
         "feature-b")
    m2 = _git(r, "rev-parse", "HEAD").strip()
    (r / ".base").write_text(base)
    (r / ".m1").write_text(m1)
    (r / ".m2").write_text(m2)
    return r


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8").strip()


def make_ledger(tmp_path: Path, n: int = 2) -> Path:
    ledger = tmp_path / "ledger.jsonl"
    lines = []
    for i in range(n):
        lines.append(json.dumps({
            "schema_version": "1",
            "event_id": f"HV-TEST-{i:03d}",
            "recorded_at": f"2026-10-0{1 + i}",
            "value_type": "useful_outcome",
            "value_units": 1,
            "unit_description": f"test event {i}",
            "evidence": [{"kind": "url",
                          "ref": f"https://example.com/ev/{i}"}],
        }, sort_keys=True))
    ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return ledger


def make_scorecard(tmp_path: Path, verdict: str = "REAL VALUE",
                   score: float = 8.0, change_id: str = "PR-9001",
                   disqualified: bool = False) -> Path:
    card = {
        "packet_version": 1,
        "change_id": change_id,
        "title": "test change",
        "merge_sha": "abc123def456",
        "grader": "test-seat",
        "disqualified": disqualified,
        "score": score,
        "verdict": verdict,
        "why_not_10": "test why-not",
        "judgments": [],
    }
    p = tmp_path / f"scorecard-{verdict.replace(' ', '_')}.json"
    p.write_text(json.dumps(card, indent=2, sort_keys=True), encoding="utf-8")
    return p


# ---------------------------------------------------------------- scan

def test_scan_lists_only_merges_in_order(repo: Path, tmp_path: Path):
    base, m1, m2 = _read(repo / ".base"), _read(repo / ".m1"), _read(repo / ".m2")
    drafts = tmp_path / "drafts"
    summary = observatory.scan(str(repo), base, drafts, tmp_path / "wm.json")
    assert summary["merges_found"] == 2
    assert summary["drafts_written"] == 2
    assert summary["watermark"] == m2
    d1 = json.loads((drafts / f"{m1}.json").read_text())
    d2 = json.loads((drafts / f"{m2}.json").read_text())
    assert d1["merge_sha"] == m1 and len(d1["parents"]) == 2
    assert d1["pr_number"] == 9001
    assert d1["pr_url"] is None or d1["pr_url"].endswith("/pull/9001")
    assert d2["pr_number"] is None
    assert d1["diffstat"]["files"] >= 1
    assert "feat-a.txt" not in str(d1["diffstat"])  # top_dirs only
    assert set(d1["diffstat"]) == {"files", "insertions", "deletions", "top_dirs"}
    # chronological order: m1's merge date <= m2's
    assert d1["merged_at"] <= d2["merged_at"]


def test_scan_rejects_base_not_ancestor(repo: Path, tmp_path: Path):
    _git(repo, "checkout", "-q", "-b", "orphan-branch", _read(repo / ".base"))
    (repo / "o.txt").write_text("o")
    _git(repo, "add", "o.txt")
    _git(repo, "commit", "-q", "-m", "orphan")
    orphan = _git(repo, "rev-parse", "HEAD").strip()
    _git(repo, "checkout", "-q", "-")
    with pytest.raises(observatory.ObservatoryError):
        observatory.scan(str(repo), orphan, tmp_path / "d", None)


def test_scan_zero_merges(repo: Path, tmp_path: Path):
    tip = _git(repo, "rev-parse", "HEAD").strip()
    drafts = tmp_path / "drafts"
    summary = observatory.scan(str(repo), tip, drafts, tmp_path / "wm.json")
    assert summary["merges_found"] == 0
    assert summary["drafts_written"] == 0
    assert list(drafts.iterdir()) == []
    assert summary["watermark"] == tip


def test_scan_is_idempotent(repo: Path, tmp_path: Path):
    base = _read(repo / ".base")
    drafts = tmp_path / "drafts"
    first = observatory.scan(str(repo), base, drafts, None)
    second = observatory.scan(str(repo), base, drafts, None)
    assert first["drafts_written"] == 2
    assert second["drafts_written"] == 0
    assert second["drafts_skipped"] == 2


def test_drafts_are_not_ledgerable(repo: Path, tmp_path: Path):
    """The machine observes; it must be structurally unable to credit itself."""
    base = _read(repo / ".base")
    drafts = tmp_path / "drafts"
    observatory.scan(str(repo), base, drafts, None)
    draft = json.loads(next(drafts.iterdir()).read_text())
    with pytest.raises(SchemaError):
        validate_event(draft)


# ---------------------------------------------------------------- promote

def _promote_kwargs(tmp_path: Path, ledger: Path, card: Path, **over):
    kw = dict(ledger_path=ledger, scorecard_path=card,
              event_id="HV-20261012-PR-9001", recorded_at="2026-10-12",
              trend_path=tmp_path / "trend.jsonl",
              receipts_dir=tmp_path / "receipts",
              pr_url="https://example.com/pull/9001", confirm=True)
    kw.update(over)
    return kw


def test_promote_real_value_appends_recomputes_snapshots(tmp_path: Path):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    before = ledger.read_bytes()
    rep = observatory.promote(**_promote_kwargs(tmp_path, ledger, card))

    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    event = json.loads(lines[-1])
    assert event["event_id"] == "HV-20261012-PR-9001"
    assert event["value_type"] == "useful_outcome"
    # full ledger still validates (fail-closed revalidation inside promote)
    compute_hv.load_ledger(ledger)

    # trend snapshot matches an independent recompute
    snap = json.loads((tmp_path / "trend.jsonl").read_text().splitlines()[-1])
    raw, events = compute_hv.load_ledger(ledger)
    expect = compute_hv.compute(events, 7,
                                date.fromisoformat(max(e["recorded_at"] for e in events)))
    assert snap["hv_per_day_total"] == expect["hv_per_day_total"]
    assert snap["hv_per_day_by_type"] == expect["hv_per_day_by_type"]
    assert snap["dai_per_day"] == expect["dai_per_day"]
    assert snap["snapshot_ledger_sha256"] == rep["ledger_sha256"]

    # promotion receipt: provenance, before/after hashes
    receipt = json.loads((tmp_path / "receipts" / "HV-20261012-PR-9001.json").read_text())
    assert receipt["ledger_sha256_before"] == compute_hv.ledger_sha256(
        [ln for ln in before.decode().splitlines() if ln.strip()])
    assert receipt["ledger_sha256_after"] == rep["ledger_sha256"]
    assert receipt["verdict"] == "REAL VALUE"


def test_promote_never_moves_the_observation_watermark(tmp_path: Path):
    """Scan owns the cursor. A promotion (possibly of an older merge) must
    not move it backwards."""
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    wm = tmp_path / "wm.json"
    wm.write_text(json.dumps({"last_observed_merge": "newer-merge-sha"}))
    before = wm.read_bytes()
    observatory.promote(**_promote_kwargs(tmp_path, ledger, card))
    assert wm.read_bytes() == before


def test_promote_duplicate_event_id_refused(tmp_path: Path):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    kw = _promote_kwargs(tmp_path, ledger, card)
    observatory.promote(**kw)
    before = ledger.read_bytes()
    with pytest.raises(observatory.ObservatoryError):
        observatory.promote(**kw)
    assert ledger.read_bytes() == before  # untouched on refusal


def test_promote_thin_refused(tmp_path: Path):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path, verdict="THIN", score=6.0)
    before = ledger.read_bytes()
    with pytest.raises(observatory.ObservatoryError):
        observatory.promote(**_promote_kwargs(tmp_path, ledger, card))
    assert ledger.read_bytes() == before
    assert not (tmp_path / "trend.jsonl").exists()


def test_promote_disqualified_refused(tmp_path: Path):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path, verdict="DISQUALIFIED",
                          disqualified=True)
    before = ledger.read_bytes()
    with pytest.raises(observatory.ObservatoryError):
        observatory.promote(**_promote_kwargs(tmp_path, ledger, card))
    assert ledger.read_bytes() == before


def test_promote_needs_confirm(tmp_path: Path):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    before = ledger.read_bytes()
    with pytest.raises(observatory.ObservatoryError):
        observatory.promote(**_promote_kwargs(tmp_path, ledger, card,
                                              confirm=False))
    assert ledger.read_bytes() == before


def test_promote_cli_exit_codes(tmp_path: Path, capsys):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    kw = _promote_kwargs(tmp_path, ledger, card)
    argv = ["promote", "--ledger", str(kw["ledger_path"]),
            "--scorecard", str(kw["scorecard_path"]),
            "--event-id", kw["event_id"], "--recorded-at", kw["recorded_at"],
            "--pr-url", kw["pr_url"],
            "--trend", str(kw["trend_path"]),
            "--receipts-dir", str(kw["receipts_dir"])]
    assert observatory.main(argv) == 2  # no --confirm: refused
    assert observatory.main(argv + ["--confirm"]) == 0


# ---------------------------------------------------------------- report / trend

def test_report_byte_deterministic(tmp_path: Path):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    observatory.promote(**_promote_kwargs(tmp_path, ledger, card))
    r1 = observatory.build_report(ledger, tmp_path / "trend.jsonl", None)
    r2 = observatory.build_report(ledger, tmp_path / "trend.jsonl", None)
    assert r1 == r2
    raw, _ = compute_hv.load_ledger(ledger)
    digest = compute_hv.ledger_sha256(raw)
    assert digest in r1
    assert "does NOT claim" in r1
    assert "wall-clock" in r1


def test_report_cli_defaults_trend_and_is_deterministic(tmp_path: Path, capsys):
    """Regression: `report` without --trend must resolve the default trend
    path instead of crashing (found in the first live run)."""
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    observatory.promote(**_promote_kwargs(tmp_path, ledger, card))
    out = tmp_path / "report.md"
    assert observatory.main(["report", "--ledger", str(ledger),
                             "--out", str(out)]) == 0
    text1 = out.read_text()
    assert observatory.main(["report", "--ledger", str(ledger),
                             "--out", str(out)]) == 0
    assert out.read_text() == text1
    assert "does NOT claim" in text1


def test_trend_cli_prints_snapshots(tmp_path: Path, capsys):
    ledger = make_ledger(tmp_path)
    card = make_scorecard(tmp_path)
    observatory.promote(**_promote_kwargs(tmp_path, ledger, card))
    assert observatory.main(["trend", "--trend", str(tmp_path / "trend.jsonl")]) == 0
    out = capsys.readouterr().out
    assert "HV/day" in out and "2026-10-12" in out
