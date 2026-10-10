#!/usr/bin/env python3
"""C5.6 — Mechanical Enforcement Rate: behavioral proof tests.

Proves the audit measures what it claims:
- laws mentioned in mechanism files within 30 days of ratification count
- a mention landing AFTER the 30-day enforcement window does not count
  (reported under late_mentions, never silently counted)
- the law's own prose/definition files (excluded substrings) never count
- enforcement predating ratification counts (landing early is fine)
- whole-token matching: L1 does not match L12
- zero in-window laws -> FAIL (an audit of nothing proves nothing)
- exit-code contract (0 pass / 1 fail / 2 bad input) and determinism
"""

import json
import os
from datetime import datetime, timezone

import pytest

from tools.longitudinal import enforcement_audit as mer

NOW = "2026-10-09T12:00:00Z"


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _law(law_id, ratified_at="2026-09-20T12:00:00Z", title=""):
    return {"law_id": law_id, "ratified_at": ratified_at, "title": title}


def _epoch(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()


def _run(tmp_path, laws, code_files=(), **kwargs):
    lp = _write_json(tmp_path / "laws.json", {"laws": laws})
    croot = tmp_path / "code"
    for name, text, mtime in code_files:
        p = croot / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        epoch = _epoch(mtime)
        os.utime(p, (epoch, epoch))
    argv = ["--laws-json", str(lp), "--code-roots", str(croot), "--now", NOW]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return mer.main(argv)


def test_pass_three_of_four_enforced(tmp_path, capsys):
    laws = [_law("L10"), _law("L11"), _law("L12"), _law("L13")]
    files = [
        ("tests/test_l10.py", "# enforces L10\n", "2026-09-25T00:00:00Z"),
        ("tools/gate_l11.py", "# enforces L11\n", "2026-09-26T00:00:00Z"),
        ("scripts/check_l12.py", "# enforces L12\n", "2026-09-27T00:00:00Z"),
        ("tests/test_other.py", "# nothing\n", "2026-09-25T00:00:00Z"),
    ]
    rc = _run(tmp_path, laws, files)
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["laws_in_window"] == 4
    assert report["laws_enforced"] == 3
    assert report["rate"] == 0.75


def test_fail_one_of_four_enforced(tmp_path, capsys):
    laws = [_law("L10"), _law("L11"), _law("L12"), _law("L13")]
    files = [("tests/test_l10.py", "# enforces L10\n", "2026-09-25T00:00:00Z")]
    rc = _run(tmp_path, laws, files)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["rate"] == 0.25
    assert any("threshold" in r for r in report["fail_reasons"])


def test_late_mention_does_not_count(tmp_path, capsys):
    laws = [_law("L10", ratified_at="2026-08-20T12:00:00Z")]
    files = [("tests/test_l10.py", "# enforces L10, finally\n", "2026-10-01T00:00:00Z")]
    rc = _run(tmp_path, laws, files, window_days=90)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    law = report["laws"][0]
    assert law["enforced"] is False
    assert len(law["late_mentions"]) == 1  # seen, but too late: reported, not counted
    assert law["mention_count"] == 1


def test_excluded_prose_path_does_not_count(tmp_path, capsys):
    laws = [_law("L10")]
    files = [("BRAIN/01-GOVERNANCE/laws.md", "# L10: the law itself\n",
              "2026-09-25T00:00:00Z")]
    rc = _run(tmp_path, laws, files, exclude_substrings="BRAIN/01-GOVERNANCE")
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["laws"][0]["enforced"] is False
    assert report["laws"][0]["mention_count"] == 0


def test_pre_ratification_enforcement_counts(tmp_path, capsys):
    laws = [_law("L10", ratified_at="2026-09-20T12:00:00Z"),
            _law("L11", ratified_at="2026-09-20T12:00:00Z")]
    files = [("tests/test_l10.py", "# enforces L10\n", "2026-09-10T00:00:00Z"),
             ("tests/test_l11.py", "# enforces L11\n", "2026-09-10T00:00:00Z")]
    rc = _run(tmp_path, laws, files)
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["laws"][0]["days_to_enforcement"] == -10.5


def test_whole_token_matching(tmp_path, capsys):
    laws = [_law("L1"), _law("L12")]
    files = [("tests/test_x.py", "# enforces L12 only\n", "2026-09-25T00:00:00Z")]
    rc = _run(tmp_path, laws, files)
    assert rc == 0  # 1/2 = 0.5 meets the 0.50 threshold exactly
    report = json.loads(capsys.readouterr().out)
    by_id = {l["law_id"]: l for l in report["laws"]}
    assert by_id["L12"]["enforced"] is True
    assert by_id["L1"]["enforced"] is False  # "L12" must not count as "L1"


def test_no_laws_in_window_fails(tmp_path, capsys):
    laws = [_law("L10", ratified_at="2026-01-01T00:00:00Z")]
    rc = _run(tmp_path, laws, [])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert any("nothing proves nothing" in r for r in report["fail_reasons"])
    assert report["out_of_window"] == ["L10"]


def test_mechanism_files_listed(tmp_path, capsys):
    laws = [_law("L10")]
    files = [
        ("tests/test_l10.py", "# L10\n", "2026-09-25T00:00:00Z"),
        ("tools/gate_l10.py", "# L10\n", "2026-09-26T00:00:00Z"),
    ]
    rc = _run(tmp_path, laws, files)
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert len(report["laws"][0]["mechanism_files"]) == 2


def test_threshold_override(tmp_path):
    laws = [_law("L10"), _law("L11")]
    files = [("tests/test_l10.py", "# L10\n", "2026-09-25T00:00:00Z")]
    rc = _run(tmp_path, laws, files, threshold=0.9)
    assert rc == 1


def test_malformed_manifest_is_input_error(tmp_path):
    bad = tmp_path / "laws.json"
    bad.write_text("nope", encoding="utf-8")
    rc = mer.main(["--laws-json", str(bad), "--code-roots", str(tmp_path),
                   "--now", NOW])
    assert rc == 2


def test_missing_law_id_is_input_error(tmp_path):
    lp = _write_json(tmp_path / "laws.json", [{"ratified_at": NOW}])
    rc = mer.main(["--laws-json", str(lp), "--code-roots", str(tmp_path),
                   "--now", NOW])
    assert rc == 2


def test_deterministic_given_now(tmp_path, capsys):
    laws = [_law("L10"), _law("L11")]
    files = [("tests/test_l10.py", "# L10\n", "2026-09-25T00:00:00Z")]
    _run(tmp_path, laws, files)
    first = capsys.readouterr().out
    _run(tmp_path, laws, files)
    second = capsys.readouterr().out
    assert json.loads(first) == json.loads(second)
