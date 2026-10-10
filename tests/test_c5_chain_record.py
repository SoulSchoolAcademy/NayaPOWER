#!/usr/bin/env python3
"""C5.5 — Lesson→Outcome Chain Completion: behavioral proof tests.

Proves the recorder measures what it claims:
- >= 3 complete, independently-verified, in-window chains -> PASS
- a chain with a missing/misordered link or empty evidence_ref is incomplete
  (reported with diagnostics, never rounded up)
- evidence_path must resolve to an existing file
- verifier == author is NOT independent -> incomplete
- empty verification statement / missing verifier / bad verified_at -> incomplete
- chains verified outside the window are reported, not counted
- exit-code contract (0 pass / 1 fail / 2 bad input)
"""

import json

import pytest

from tools.longitudinal import chain_record as locc

WS, WE = "2026-10-01T00:00:00Z", "2026-10-14T23:59:59Z"


def _write_json(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _link(stage, ref="ref", path=None):
    return {"stage": stage, "evidence_ref": ref,
            "evidence_path": path, "note": ""}


def _chain(cid, author="Naya 4", verifier="Naya 1", verified_at="2026-10-05T12:00:00Z",
           statement="verified: all four links check out", links="__auto__",
           window=True, sn_id="SN-0500"):
    if links == "__auto__":
        links = [_link("captured", "SN-0500 §failure-class"),
                 _link("retrieved", "RPCK receipt RPCK-SN-0500"),
                 _link("applied", "PR #2071"),
                 _link("outcome", "C5.4 scan: zero recurrences")]
    return {
        "chain_id": cid,
        "window_id": "W-2026-10-01",
        "window_start": WS if window else None,
        "window_end": WE if window else None,
        "sn_id": sn_id,
        "author_seat": author,
        "links": links,
        "verification": {"verifier_seat": verifier,
                         "verified_at": verified_at,
                         "statement": statement},
    }


def _run(tmp_path, chains, evidence_files=(), **kwargs):
    cp = _write_json(tmp_path / "chains.json", {"chains": chains})
    for name, text in evidence_files:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    argv = ["--chains-json", str(cp), "--repo-root", str(tmp_path)]
    for k, v in kwargs.items():
        argv += [f"--{k.replace('_', '-')}", str(v)]
    return locc.main(argv)


def test_pass_three_complete_chains(tmp_path, capsys):
    chains = [_chain(f"LOCC-{i}", sn_id=f"SN-05{i:02d}") for i in range(3)]
    rc = _run(tmp_path, chains)
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report["chains_complete"] == 3
    assert report["pass"] is True


def test_fail_two_chains_below_minimum(tmp_path, capsys):
    chains = [_chain(f"LOCC-{i}") for i in range(2)]
    rc = _run(tmp_path, chains)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    assert any("minimum 3" in r for r in report["fail_reasons"])


def test_missing_outcome_link_is_incomplete(tmp_path, capsys):
    links = [_link("captured", "r1"), _link("retrieved", "r2"), _link("applied", "r3")]
    chains = [_chain("LOCC-0", links=links),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    bad = next(c for c in report["chains"] if c["chain_id"] == "LOCC-0")
    assert bad["complete"] is False
    assert any("outcome" in d for d in bad["diagnostics"])


def test_misordered_links_are_incomplete(tmp_path):
    links = [_link("captured", "r1"), _link("applied", "r3"),
             _link("retrieved", "r2"), _link("outcome", "r4")]
    rc = _run(tmp_path, [_chain("LOCC-0", links=links),
                         _chain("LOCC-1"), _chain("LOCC-2")])
    assert rc == 1


def test_empty_evidence_ref_is_incomplete(tmp_path):
    links = [_link("captured", ""), _link("retrieved", "r2"),
             _link("applied", "r3"), _link("outcome", "r4")]
    rc = _run(tmp_path, [_chain("LOCC-0", links=links),
                         _chain("LOCC-1"), _chain("LOCC-2")])
    assert rc == 1


def test_evidence_path_must_exist(tmp_path, capsys):
    links = [_link("captured", "r1", path="proofs/missing.md"),
             _link("retrieved", "r2"), _link("applied", "r3"),
             _link("outcome", "r4")]
    chains = [_chain("LOCC-0", links=links),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    bad = next(c for c in report["chains"] if c["chain_id"] == "LOCC-0")
    assert any("does not exist" in d for d in bad["diagnostics"])


def test_existing_evidence_path_counts(tmp_path):
    links = [_link("captured", "r1", path="proofs/real.md"),
             _link("retrieved", "r2"), _link("applied", "r3"),
             _link("outcome", "r4")]
    chains = [_chain(f"LOCC-{i}", links=links) for i in range(3)]
    rc = _run(tmp_path, chains, evidence_files=[("proofs/real.md", "proof\n")])
    assert rc == 0


def test_verifier_same_as_author_is_not_independent(tmp_path, capsys):
    chains = [_chain("LOCC-0", author="Naya 4", verifier="Naya 4"),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    bad = next(c for c in report["chains"] if c["chain_id"] == "LOCC-0")
    assert any("not independent" in d for d in bad["diagnostics"])


def test_empty_verification_statement_is_incomplete(tmp_path):
    chains = [_chain("LOCC-0", statement="   "),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1


def test_missing_verifier_seat_is_incomplete(tmp_path):
    chains = [_chain("LOCC-0", verifier=""),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1


def test_chain_verified_outside_window_not_counted(tmp_path, capsys):
    chains = [_chain("LOCC-0", verified_at="2026-11-01T12:00:00Z"),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1
    report = json.loads(capsys.readouterr().out)
    bad = next(c for c in report["chains"] if c["chain_id"] == "LOCC-0")
    assert bad["in_window"] is False
    assert bad["counted"] is False


def test_bad_verified_at_is_incomplete_not_crash(tmp_path):
    chains = [_chain("LOCC-0", verified_at="not-a-date"),
              _chain("LOCC-1"), _chain("LOCC-2")]
    rc = _run(tmp_path, chains)
    assert rc == 1


def test_min_chains_override(tmp_path):
    chains = [_chain("LOCC-0"), _chain("LOCC-1")]
    rc = _run(tmp_path, chains, min_chains=2)
    assert rc == 0


def test_malformed_manifest_is_input_error(tmp_path):
    bad = tmp_path / "chains.json"
    bad.write_text('{"chains": "nope"}', encoding="utf-8")
    rc = locc.main(["--chains-json", str(bad)])
    assert rc == 2


def test_chain_without_id_is_input_error(tmp_path):
    cp = _write_json(tmp_path / "chains.json", {"chains": [{"links": []}]})
    rc = locc.main(["--chains-json", str(cp)])
    assert rc == 2
