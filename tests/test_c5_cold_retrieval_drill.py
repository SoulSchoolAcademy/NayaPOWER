#!/usr/bin/env python3
"""C5.3 — Retrieval Precision on Contributed Knowledge: behavioral proof tests.

Proves the drill measures what it claims:
- retrieved+applied lessons score 1.0; the gate needs >= 20 lessons and >= 0.80
- a lesson whose knowledge file is missing is NOT retrievable (honest miss)
- a query term absent from the corpus is a retrieval miss
- application evidence must exist AND cite the SN id (reality beats paperwork)
- bare refs without paths are recorded, never counted
- per-lesson coldness receipts are written with machine-recorded provenance
- out-of-window lessons are excluded from the sample
- exit-code contract (0 pass / 1 fail / 2 bad input) and determinism
"""

import json
import os

import pytest

from tools.longitudinal import cold_retrieval_drill as rpck

NOW = "2026-10-09T12:00:00Z"
TERMS = ["merge", "tree", "verify"]


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _lesson(sn, contributed_at="2026-10-01T12:00:00Z", terms=None,
            knowledge_file="knowledge/lessons/sn.md", evidence=("__auto__",)):
    if evidence == ("__auto__",):
        evidence = [{"ref": "applied in a team PR",
                     "path": f"evidence/{sn}.md"}]
    return {
        "sn_id": sn,
        "contributed_at": contributed_at,
        "knowledge_file": knowledge_file,
        "query_terms": list(terms or TERMS),
        "success_criteria": "a cold Naya states the merge-tree verification rule",
        "application_evidence": evidence,
    }


def _run(tmp_path, lessons, knowledge_files=(), evidence_files=(), **kwargs):
    lessons_p = _write_json(tmp_path / "lessons.json", {"lessons": lessons})
    kroot = tmp_path / "knowledge"
    kroot.mkdir(exist_ok=True)
    # knowledge files are repo-relative (they live inside the corpus root);
    # evidence files are repo-relative too. The manifest itself stays outside
    # the corpus so the drill cannot "retrieve" a lesson from its own manifest.
    for name, text in knowledge_files:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    # evidence + knowledge files resolve against repo-root = tmp_path
    for name, text in evidence_files:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    receipts = tmp_path / "receipts"
    argv = [
        "--lessons-json", str(lessons_p),
        "--knowledge-roots", str(kroot),
        "--repo-root", str(tmp_path),
        "--receipts-dir", str(receipts),
        "--now", NOW,
    ]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return rpck.main(argv), receipts


def _corpus(sn, terms=TERMS, extra=""):
    body = " ".join(terms)
    return [
        ("knowledge/lessons/sn.md", f"# Lesson {sn}\n{body} {extra}\n"),
        (f"evidence/{sn}.md", f"Applied {sn} here.\n"),
    ]


def _twenty(prefix="SN-05"):
    return [f"{prefix}{i:02d}" for i in range(20)]


def test_full_pass_twenty_lessons(tmp_path, capsys):
    lessons = [_lesson(sn) for sn in _twenty()]
    files = []
    for sn in _twenty():
        files += _corpus(sn)
    rc, receipts = _run(tmp_path, lessons, knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
                        evidence_files=[f for f in files if f[0].startswith("evidence/")])
    assert rc == 0
    out = capsys.readouterr().out
    report = json.loads(out)
    assert report["sampled_lessons"] == 20
    assert report["rate"] == 1.0
    assert report["pass"] is True


def test_fail_below_threshold(tmp_path, capsys):
    # only 10 of 20 lessons applied -> rate 0.5 < 0.80
    lessons = [_lesson(sn, evidence=[]) if i >= 10 else _lesson(sn)
               for i, sn in enumerate(_twenty())]
    files = []
    for sn in _twenty():
        files += _corpus(sn)
    rc, _ = _run(tmp_path, lessons,
                 knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
                 evidence_files=[f for f in files if f[0].startswith("evidence/")])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["rate"] == 0.5
    assert any("threshold" in r for r in report["fail_reasons"])


def test_fail_sample_below_minimum(tmp_path, capsys):
    lessons = [_lesson(sn) for sn in _twenty()[:5]]
    files = []
    for sn in _twenty()[:5]:
        files += _corpus(sn)
    rc, _ = _run(tmp_path, lessons,
                 knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
                 evidence_files=[f for f in files if f[0].startswith("evidence/")])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert any("minimum" in r for r in report["fail_reasons"])


def test_missing_knowledge_file_is_retrieval_miss(tmp_path, capsys):
    lessons = [_lesson(sn, knowledge_file="lessons/missing.md") for sn in _twenty()]
    rc, _ = _run(tmp_path, lessons, knowledge_files=[], evidence_files=[])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["rate"] == 0.0
    assert report["lessons"][0]["retrieved"] is False


def test_absent_query_term_is_retrieval_miss(tmp_path, capsys):
    lessons = [_lesson(sn, terms=["merge", "tree", "zxqv-nonexistent"]) for sn in _twenty()]
    files = []
    for sn in _twenty():
        files += _corpus(sn)
    rc, _ = _run(tmp_path, lessons,
                 knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
                 evidence_files=[f for f in files if f[0].startswith("evidence/")])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["lessons"][0]["missing_terms"] == ["zxqv-nonexistent"]


def test_evidence_path_must_exist_and_cite_sn(tmp_path, capsys):
    # evidence file exists but does NOT cite the SN -> not applied
    lessons = [_lesson(sn) for sn in _twenty()]
    kfiles, efiles = [], []
    for sn in _twenty():
        kfiles.append(("lessons/sn.md", "# Lesson\nmerge tree verify\n"))
        efiles.append((f"evidence/{sn}.md", "Some change with no SN citation.\n"))
    rc, _ = _run(tmp_path, lessons, knowledge_files=kfiles, evidence_files=efiles)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["lessons"][0]["applied"] is False
    assert "does not cite" in report["lessons"][0]["evidence"][0]["reason"]


def test_bare_ref_without_path_is_recorded_not_counted(tmp_path, capsys):
    lessons = [_lesson(sn, evidence=[{"ref": "someone said it worked"}])
               for sn in _twenty()]
    files = []
    for sn in _twenty():
        files.append(("lessons/sn.md", "# Lesson\nmerge tree verify\n"))
    rc, _ = _run(tmp_path, lessons, knowledge_files=files, evidence_files=[])
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["lessons"][0]["applied"] is False
    assert "not machine-checkable" in report["lessons"][0]["evidence"][0]["reason"]


def test_coldness_receipts_written(tmp_path):
    lessons = [_lesson(sn) for sn in _twenty()[:20]]
    files = []
    for sn in _twenty()[:20]:
        files += _corpus(sn)
    rc, receipts = _run(tmp_path, lessons,
                        knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
                        evidence_files=[f for f in files if f[0].startswith("evidence/")])
    assert rc == 0
    written = sorted(receipts.glob("*.json"))
    assert len(written) == 20
    receipt = json.loads(written[0].read_text(encoding="utf-8"))
    assert receipt["query_terms"] == TERMS
    assert receipt["corpus_files_examined"], "must record examined corpus files"
    assert all("sha256" in f for f in receipt["corpus_files_examined"])
    assert "attestation_limit" in receipt


def test_out_of_window_lessons_excluded(tmp_path, capsys):
    lessons = ([_lesson(sn) for sn in _twenty()] +
               [_lesson("SN-0600", contributed_at="2026-01-01T00:00:00Z")])
    files = []
    for sn in _twenty():
        files += _corpus(sn)
    rc, _ = _run(tmp_path, lessons,
                 knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
                 evidence_files=[f for f in files if f[0].startswith("evidence/")])
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["sampled_lessons"] == 20
    assert report["out_of_window"] == ["SN-0600"]


def test_bad_input_malformed_json_real(tmp_path):
    bad = tmp_path / "lessons.json"
    bad.write_text("{not json", encoding="utf-8")
    rc = rpck.main(["--lessons-json", str(bad),
                    "--knowledge-roots", str(tmp_path),
                    "--now", NOW])
    assert rc == 2


def test_bad_input_missing_query_terms(tmp_path):
    lesson = _lesson("SN-0500")
    del lesson["query_terms"]
    lp = _write_json(tmp_path / "lessons.json", [lesson])
    rc = rpck.main(["--lessons-json", str(lp),
                    "--knowledge-roots", str(tmp_path),
                    "--now", NOW])
    assert rc == 2


def test_bad_input_bad_sn_id(tmp_path):
    lesson = _lesson("NOT-A-SN")
    lp = _write_json(tmp_path / "lessons.json", [lesson])
    rc = rpck.main(["--lessons-json", str(lp),
                    "--knowledge-roots", str(tmp_path),
                    "--now", NOW])
    assert rc == 2


def test_deterministic_given_now(tmp_path, capsys):
    lessons = [_lesson(sn) for sn in _twenty()]
    files = []
    for sn in _twenty():
        files += _corpus(sn)
    kwargs = dict(
        knowledge_files=[f for f in files if f[0].startswith("knowledge/")],
        evidence_files=[f for f in files if f[0].startswith("evidence/")],
    )
    _run(tmp_path, lessons, **kwargs)
    first = capsys.readouterr().out
    _run(tmp_path, lessons, **kwargs)
    second = capsys.readouterr().out
    r1, r2 = json.loads(first), json.loads(second)
    r1.pop("drill_id"), r2.pop("drill_id")
    assert r1 == r2
