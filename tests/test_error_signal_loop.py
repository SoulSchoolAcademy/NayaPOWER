"""Tests for the error-signal loop.

Red path: a planted violation is caught with exact provenance.
Green path: a clean artifact passes with zero events.
Fail-safe: malformed input fails safe (exit 2), never guesses.
"""
import json
import subprocess
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent / "tools" / "learning" / "error_signal_loop.py"
PY = sys.executable


def run_scan(artifact: Path, kind: str, out: Path, source_ref: str = "test"):
    return subprocess.run(
        [PY, str(TOOL), "scan", "--artifact", str(artifact), "--kind", kind,
         "--source-ref", source_ref, "--out", str(out)],
        capture_output=True, text=True)


def read_events(out: Path):
    return [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines() if line.strip()]


# ------------------------------------------------------------------ red path
PLANTED = """[NAYA ALPHA — SIGN IN]
Built the widget. Final score: 10/10. Done.
I will comment on #1354 with the results.
Next: git push origin main to publish.
Token for later: ghp_TESTTOKEN0123456789abcdef
Planning a production deploy tonight.
"""


def test_red_path_catches_planted_violations(tmp_path):
    artifact = tmp_path / "report.txt"
    artifact.write_text(PLANTED, encoding="utf-8")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "lane-report", out)
    assert result.returncode == 0, result.stderr
    events = read_events(out)
    rule_ids = {e["principle"]["rule_id"] for e in events}
    # P1 self-declared 10/10, P2 direct-main, P3 comment-1354,
    # P4 raw credential, P5 no briefing proof, P6 protected gate
    assert {"P1", "P2", "P3", "P4", "P5", "P6"} <= rule_ids, rule_ids
    summary = json.loads(result.stdout)
    assert summary["violations"] == len(events) >= 6
    # provenance: every event quotes evidence with file + line
    for e in events:
        assert e["schema"] == "learning-event-candidate/v1"
        assert e["violation"]["evidence_quote"], e
        loc = e["violation"]["evidence_location"]
        assert loc["file"] == str(artifact)
        assert isinstance(loc["line"], int)
        assert e["principle"]["briefing_line"] > 0
        assert e["checklist_fingerprint"] == \
            "4baaa440db4dc799bee17ac3ed7bdc0d1d43a73856441fc0cc6e8a96b1251992"
        assert e["suggested_lesson"].strip()
        assert e["severity"] in ("high", "medium", "low")
        assert e["source"]["kind"] == "lane-report"


def test_red_path_line_numbers_point_at_evidence(tmp_path):
    artifact = tmp_path / "report.txt"
    artifact.write_text(PLANTED, encoding="utf-8")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "lane-report", out)
    assert result.returncode == 0, result.stderr
    events = read_events(out)
    lines = PLANTED.splitlines()
    for e in events:
        lineno = e["violation"]["evidence_location"]["line"]
        if lineno == 0:
            continue  # artifact-level rule P5
        quoted = e["violation"]["evidence_quote"]
        assert quoted in lines[lineno - 1], (quoted, lines[lineno - 1])


# ---------------------------------------------------------------- green path
CLEAN = """[NAYA ALPHA — SIGN IN]
briefing_proof.py verify: ok, 3/3 quotes. Load recorded.
Built the widget. Honest self-score: 8.5 — independently validated by Naya 1.
Branch naya5/error-signal-loop pushed; PR opened for review.
Coordinating on lane feed #1713. Sign out with receipts attached.
"""


def test_green_path_clean_artifact_passes(tmp_path):
    artifact = tmp_path / "clean.txt"
    artifact.write_text(CLEAN, encoding="utf-8")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "lane-report", out)
    assert result.returncode == 0, result.stderr
    events = read_events(out)
    assert events == []
    summary = json.loads(result.stdout)
    assert summary["violations"] == 0


def test_positive_context_exonerates_line_wise(tmp_path):
    # 10/10 with independent validation on the same line: no P1 event.
    artifact = tmp_path / "ok.txt"
    artifact.write_text(
        "Self-score 10/10, independently validated by Naya 1.\n"
        "briefing_proof.py verified ok, recorded.\n",
        encoding="utf-8")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "text-file", out)
    assert result.returncode == 0, result.stderr
    events = read_events(out)
    assert {e["principle"]["rule_id"] for e in events} == set()


# --------------------------------------------------------------- fail safe
def test_fail_safe_on_binary_input(tmp_path):
    artifact = tmp_path / "blob.bin"
    artifact.write_bytes(b"\x89PNG\r\n\x1a\n\x00\xff\xfe garbage")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "text-file", out)
    assert result.returncode == 2
    assert "FAIL-SAFE" in result.stderr


def test_fail_safe_on_missing_file(tmp_path):
    out = tmp_path / "events.jsonl"
    result = run_scan(tmp_path / "nope.txt", "text-file", out)
    assert result.returncode == 2
    assert "FAIL-SAFE" in result.stderr


def test_fail_safe_on_empty_file(tmp_path):
    artifact = tmp_path / "empty.txt"
    artifact.write_text("   \n", encoding="utf-8")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "text-file", out)
    assert result.returncode == 2
    assert "FAIL-SAFE" in result.stderr


def test_fail_safe_on_bad_checklist(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("esl", str(TOOL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for bad_content in ('{"checklist": "nope", "rules": []}',
                        'not json at all',
                        '{"checklist": "briefed-principles/v1", "rules": []}'):
        bad = tmp_path / "bad.json"
        bad.write_text(bad_content, encoding="utf-8")
        try:
            mod.load_checklist(bad)
        except mod.FailSafe:
            pass
        else:
            raise AssertionError(f"bad checklist did not raise FailSafe: {bad_content!r}")


def test_commit_diff_kind_scans_added_lines(tmp_path):
    artifact = tmp_path / "change.diff"
    artifact.write_text(
        "--- a/report.md\n+++ b/report.md\n"
        "@@ -1 +1 @@\n"
        "-old line\n"
        "+I claim 10/10 with no validation at all.\n"
        "+briefing proof recorded: verify ok.\n",
        encoding="utf-8")
    out = tmp_path / "events.jsonl"
    result = run_scan(artifact, "commit-diff", out)
    assert result.returncode == 0, result.stderr
    events = read_events(out)
    assert any(e["principle"]["rule_id"] == "P1" for e in events)
