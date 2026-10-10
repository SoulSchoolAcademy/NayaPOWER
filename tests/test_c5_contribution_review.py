#!/usr/bin/env python3
"""C5.7 — Contribution Signal Integrity: behavioral proof tests.

Proves the review instrument measures what it claims:
- every contribution dispositioned (mixed accept/reject) -> PASS
- a pending/undispositioned contribution is UNREVIEWED -> FAIL, named
- 100% acceptance over >= 5 decided means no effective review -> FAIL
- below the min review sample, 100% acceptance is too small to judge -> PASS
- state claims without evidence refs are auto-flagged (findings, not gate)
- claims WITH evidence refs are not flagged
- near-duplicate contributions vs the corpus are reported as possible duplicates
- duplicate contrib_ids fail the gate (registry integrity)
- without a corpus, dedup is reported SKIPPed, never silently passed
- exit-code contract (0 pass / 1 fail / 2 bad input)
"""

import json

import pytest

from tools.longitudinal import contribution_review as csi

NOW = "2026-10-09T12:00:00Z"


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _contrib(cid, contributed_at="2026-10-02T12:00:00Z", disposition="accepted",
             text="Routine note, reviewed against tools/review.py.", seat="Naya 4",
             reason="meets the bar", reviewer="Naya 1"):
    return {
        "contrib_id": cid,
        "contributed_at": contributed_at,
        "seat": seat,
        "text": text,
        "disposition": disposition,
        "review_reason": reason,
        "reviewer_seat": reviewer,
    }


def _run(tmp_path, contributions, corpus=None, **kwargs):
    cp = _write_json(tmp_path / "contributions.json", {"contributions": contributions})
    argv = ["--contributions-json", str(cp), "--now", NOW]
    if corpus is not None:
        cor_p = _write_json(tmp_path / "corpus.json", {"notes": corpus})
        argv += ["--corpus-json", str(cor_p)]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return csi.main(argv)


def _six_mixed():
    contribs = [_contrib(f"SN-07{i:02d}", disposition="accepted") for i in range(4)]
    contribs += [_contrib(f"SN-07{i:02d}", disposition="rejected",
                          reason="duplicate of SN-0700", reviewer="Naya 2")
                 for i in range(4, 6)]
    return contribs


def test_pass_all_dispositioned_mixed_review(tmp_path, capsys):
    rc = _run(tmp_path, _six_mixed())
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["pass"] is True
    assert report["unreviewed"] == []
    assert report["review_health_ok"] is True


def test_fail_pending_is_unreviewed(tmp_path, capsys):
    contribs = _six_mixed()
    contribs[0]["disposition"] = "pending"
    rc = _run(tmp_path, contribs)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["unreviewed"] == ["SN-0700"]


def test_fail_missing_disposition_is_unreviewed(tmp_path):
    contribs = _six_mixed()
    del contribs[1]["disposition"]
    rc = _run(tmp_path, contribs)
    assert rc == 1


def test_fail_full_acceptance_means_no_review(tmp_path, capsys):
    contribs = [_contrib(f"SN-07{i:02d}", disposition="accepted") for i in range(6)]
    rc = _run(tmp_path, contribs)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["review_health_ok"] is False
    assert report["acceptance_rate"] == 1.0
    assert any("no effective review" in r for r in report["fail_reasons"])


def test_small_sample_full_acceptance_not_judged(tmp_path):
    contribs = [_contrib(f"SN-07{i:02d}", disposition="accepted") for i in range(3)]
    rc = _run(tmp_path, contribs)
    assert rc == 0


def test_evidence_less_claim_auto_flagged(tmp_path, capsys):
    contribs = [_contrib("SN-0700", disposition="accepted",
                         text="9.4% of notes integrated into doctrine. The pipeline works."),
                _contrib("SN-0701", disposition="rejected", reason="thin")]
    rc = _run(tmp_path, contribs)
    assert rc == 0  # flags are findings for the reviewer, not gate failures
    report = json.loads(capsys.readouterr().out)
    assert report["flagged_claim_count"] == 1
    flag = report["flagged_evidence_less_claims"][0]
    assert flag["contrib_id"] == "SN-0700"
    assert "9.4%" in flag["sentence"]


def test_claim_with_evidence_ref_not_flagged(tmp_path, capsys):
    contribs = [_contrib("SN-0700", disposition="accepted",
                         text="9.4% of notes integrated, per tools/longitudinal/note_integration_rate.py."),
                _contrib("SN-0701", disposition="rejected", reason="thin")]
    rc = _run(tmp_path, contribs)
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["flagged_claim_count"] == 0


def test_neighbour_sentence_evidence_counts(tmp_path, capsys):
    contribs = [_contrib("SN-0700", disposition="accepted",
                         text="14 of 14 tests pass. See tests/test_x.py for the full matrix."),
                _contrib("SN-0701", disposition="rejected", reason="thin")]
    rc = _run(tmp_path, contribs)
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["flagged_claim_count"] == 0


def test_near_duplicate_flagged_against_corpus(tmp_path, capsys):
    corpus = [{"note_id": "SN-0100",
               "text": "The merge gate must verify the tree before moving the ref, always."}]
    contribs = [_contrib("SN-0700", disposition="accepted",
                         text="The merge gate must verify the tree before moving the ref, always!"),
                _contrib("SN-0701", disposition="rejected", reason="thin")]
    rc = _run(tmp_path, contribs, corpus=corpus)
    assert rc == 0  # duplicate flag is a finding, reported not hidden
    report = json.loads(capsys.readouterr().out)
    assert len(report["possible_duplicates"]) == 1
    dup = report["possible_duplicates"][0]
    assert dup["matched_note"] == "SN-0100"
    assert dup["similarity"] >= 0.85


def test_dissimilar_text_not_flagged(tmp_path, capsys):
    corpus = [{"note_id": "SN-0100",
               "text": "The merge gate must verify the tree before moving the ref, always."}]
    contribs = [_contrib("SN-0700", disposition="accepted",
                         text="Completely unrelated note about hub color tokens and spacing."),
                _contrib("SN-0701", disposition="rejected", reason="thin")]
    rc = _run(tmp_path, contribs, corpus=corpus)
    assert rc == 0
    assert json.loads(capsys.readouterr().out)["possible_duplicates"] == []


def test_no_corpus_dedup_skipped_not_silent(tmp_path, capsys):
    rc = _run(tmp_path, _six_mixed())
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["dedup_status"].startswith("skipped")


def test_duplicate_contrib_ids_fail_gate(tmp_path, capsys):
    contribs = _six_mixed()
    contribs[1]["contrib_id"] = "SN-0700"  # duplicate id
    rc = _run(tmp_path, contribs)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert report["duplicate_ids"] == ["SN-0700"]


def test_out_of_window_excluded(tmp_path, capsys):
    contribs = _six_mixed()
    contribs.append(_contrib("SN-0800", contributed_at="2026-01-01T00:00:00Z",
                             disposition="pending"))
    rc = _run(tmp_path, contribs)
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["out_of_window"] == ["SN-0800"]
    assert report["unreviewed"] == []


def test_empty_text_no_crash(tmp_path):
    contribs = [_contrib("SN-0700", disposition="accepted", text=""),
                _contrib("SN-0701", disposition="rejected", reason="thin")]
    rc = _run(tmp_path, contribs)
    assert rc == 0


def test_malformed_manifest_is_input_error(tmp_path):
    bad = tmp_path / "contributions.json"
    bad.write_text("[[[", encoding="utf-8")
    rc = csi.main(["--contributions-json", str(bad), "--now", NOW])
    assert rc == 2


def test_missing_contrib_id_is_input_error(tmp_path):
    cp = _write_json(tmp_path / "contributions.json",
                     [{"contributed_at": NOW, "text": "x"}])
    rc = csi.main(["--contributions-json", str(cp), "--now", NOW])
    assert rc == 2
