#!/usr/bin/env python3
"""C5.4 — Behavioral-Change Evidence: behavioral proof tests.

Proves the scanner measures what it claims:
- zero recurrences across >= 5 tracked lessons -> PASS
- a pattern match inside a lesson's post window is a recurrence -> FAIL,
  reported with pattern + excerpt
- artifacts outside the window (before capture, after post_days) don't count
- the lesson's own capture artifact is excluded (self-match is not recurrence)
- lessons without failure-class patterns are untracked, reported, not counted
- matching is case-insensitive; any of several patterns can fire
- exit-code contract (0 pass / 1 fail / 2 bad input); --artifacts-dir mode works
"""

import json

import pytest

from tools.longitudinal import recurrence_scan as bce

NOW = "2026-10-09T12:00:00Z"


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _lesson(sn, captured_at="2026-09-15T12:00:00Z", patterns=("tree=head-tree",),
            name="merge-tree-drop", capture_artifact_id=""):
    return {
        "sn_id": sn,
        "captured_at": captured_at,
        "seat": "Naya 4",
        "failure_class": {"name": name, "patterns": list(patterns),
                          "description": "test failure class"},
        "capture_artifact_id": capture_artifact_id,
    }


def _artifact(aid, date, text, kind="commit"):
    return {"id": aid, "date": date, "kind": kind, "text": text}


def _run(tmp_path, lessons, artifacts=None, artifacts_dir_files=(), use_git=False, **kwargs):
    lp = _write_json(tmp_path / "lessons.json", {"lessons": lessons})
    argv = ["--lessons-json", str(lp), "--now", NOW]
    if use_git:
        argv += ["--git-repo", str(tmp_path)]
    elif artifacts_dir_files:
        adir = tmp_path / "artifacts"
        adir.mkdir()
        for i, batch in enumerate(artifacts_dir_files):
            _write_json(adir / f"a{i}.json", {"artifacts": batch})
        argv += ["--artifacts-dir", str(adir)]
    else:
        ap = _write_json(tmp_path / "artifacts.json", {"artifacts": artifacts or []})
        argv += ["--artifacts-json", str(ap)]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return bce.main(argv)


def _five_clean():
    lessons = [_lesson(f"SN-06{i:02d}") for i in range(5)]
    artifacts = [_artifact(f"c{i}", "2026-09-20T10:00:00Z",
                           "Routine refactor, nothing related.")
                 for i in range(5)]
    return lessons, artifacts


def test_pass_zero_recurrences(tmp_path, capsys):
    lessons, artifacts = _five_clean()
    rc = _run(tmp_path, lessons, artifacts)
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["lessons_tracked"] == 5
    assert report["recurrence_count"] == 0
    assert report["pass"] is True


def test_fail_recurrence_detected(tmp_path, capsys):
    lessons, artifacts = _five_clean()
    artifacts.append(_artifact("bad1", "2026-09-25T10:00:00Z",
                               "Merged with tree=head-tree again, dropped 3 files."))
    rc = _run(tmp_path, lessons, artifacts)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    # the bad artifact matches all 5 identical lessons -> 5 recurrences
    assert report["recurrence_count"] == 5
    assert {r["artifact_id"] for r in report["recurrences"]} == {"bad1"}
    rec = report["recurrences"][0]
    assert rec["matched_pattern"] == "tree=head-tree"
    assert "excerpt" in rec and rec["excerpt"]


def test_fail_fewer_than_five_tracked(tmp_path, capsys):
    lessons = [_lesson(f"SN-06{i:02d}") for i in range(3)]
    rc = _run(tmp_path, lessons, [])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert any("minimum" in r for r in report["fail_reasons"])


def test_artifact_before_capture_not_counted(tmp_path, capsys):
    lessons = [_lesson("SN-0600")]
    artifacts = [_artifact("old", "2026-09-01T10:00:00Z",
                           "tree=head-tree was used here long ago")]
    rc = _run(tmp_path, lessons * 5, artifacts, min_lessons=5)
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["recurrence_count"] == 0


def test_artifact_after_post_window_not_counted(tmp_path, capsys):
    lessons = [_lesson("SN-0600", captured_at="2026-09-01T12:00:00Z")]
    artifacts = [_artifact("late", "2026-10-05T10:00:00Z",
                           "tree=head-tree slipped in after the window")]
    rc = _run(tmp_path, lessons * 5, artifacts, min_lessons=5, post_days=30)
    assert rc == 0


def test_capture_artifact_self_match_excluded(tmp_path, capsys):
    lessons = [_lesson("SN-0600", capture_artifact_id="note-sn-0600")]
    artifacts = [_artifact("note-sn-0600", "2026-09-16T10:00:00Z",
                           "Lesson: never use tree=head-tree; it drops files.")]
    rc = _run(tmp_path, lessons * 5, artifacts, min_lessons=5)
    assert rc == 0


def test_lesson_without_patterns_is_untracked(tmp_path, capsys):
    lessons = [_lesson(f"SN-06{i:02d}") for i in range(4)]
    lessons.append(_lesson("SN-0699", patterns=()))
    rc = _run(tmp_path, lessons, [], min_lessons=5)
    assert rc == 1  # only 4 tracked
    report = json.loads(capsys.readouterr().out)
    assert report["lessons_without_failure_class"] == ["SN-0699"]


def test_case_insensitive_match(tmp_path, capsys):
    lessons = [_lesson("SN-0600")]
    artifacts = [_artifact("ci", "2026-09-20T10:00:00Z", "TREE=HEAD-TREE strikes again")]
    rc = _run(tmp_path, lessons * 5, artifacts, min_lessons=5)
    assert rc == 1


def test_any_of_several_patterns_fires(tmp_path, capsys):
    lessons = [_lesson("SN-0600", patterns=("zzz-nope", "dropped\\s+\\d+\\s+files"))]
    artifacts = [_artifact("m", "2026-09-20T10:00:00Z", "merge dropped 12 files oops")]
    rc = _run(tmp_path, lessons * 5, artifacts, min_lessons=5)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["recurrences"][0]["matched_pattern"] == "dropped\\s+\\d+\\s+files"


def test_artifacts_dir_mode(tmp_path, capsys):
    lessons, artifacts = _five_clean()
    rc = _run(tmp_path, lessons, artifacts_dir_files=(artifacts[:3], artifacts[3:]))
    assert rc == 0


def test_future_artifacts_ignored(tmp_path, capsys):
    lessons = [_lesson("SN-0600")]
    artifacts = [_artifact("future", "2026-12-01T10:00:00Z", "tree=head-tree")]
    rc = _run(tmp_path, lessons * 5, artifacts, min_lessons=5)
    assert rc == 0  # beyond --now: cannot scan the future


def test_bad_regex_is_input_error(tmp_path):
    lessons = [_lesson("SN-0600", patterns=("([unclosed",))]
    rc = _run(tmp_path, lessons * 5, [], min_lessons=5)
    assert rc == 2


def test_malformed_artifacts_is_input_error(tmp_path):
    lp = _write_json(tmp_path / "lessons.json", {"lessons": [_lesson("SN-0600")]})
    bad = tmp_path / "artifacts.json"
    bad.write_text("[{bad", encoding="utf-8")
    rc = bce.main(["--lessons-json", str(lp), "--artifacts-json", str(bad),
                   "--now", NOW])
    assert rc == 2


def test_git_repo_mode(tmp_path, capsys):
    # hermetic git repo: one clean commit inside the window
    import subprocess
    subprocess.run(["git", "init", "-q", str(tmp_path / "repo")], check=True)
    repo = tmp_path / "repo"
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "GIT_AUTHOR_DATE": "2026-09-20T10:00:00Z",
           "GIT_COMMITTER_DATE": "2026-09-20T10:00:00Z"}
    import os
    full_env = dict(os.environ, **env)
    (repo / "f.txt").write_text("hello", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "routine change"],
                   check=True, env=full_env)
    lessons = [_lesson(f"SN-06{i:02d}") for i in range(5)]
    lp = _write_json(tmp_path / "lessons.json", {"lessons": lessons})
    rc = bce.main(["--lessons-json", str(lp), "--git-repo", str(repo), "--now", NOW])
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["lessons_tracked"] == 5
