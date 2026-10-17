#!/usr/bin/env python3
"""Scorecard calculator fail-safety tests — stdlib only, python3.

Encodes the fail-safe behaviors the different-seat validation already
proved (2026-10-17, item 23), so they are mechanically re-checkable rather
than asserted in prose:

  (a) fabricated citation path   -> ledger verdict UNVERIFIABLE;
      claimed 9.0 -> applied 5.0 with UNCITED_CAP
  (b) attested-only evidence (kind=command) -> 5.0, UNCITED_CAP
  (c) builder-attested harm      -> DISQUALIFIED, score None
  (d) missing receipt post       -> exit 2 fail-closed, no card emitted
  (e) harm regex scan: DELETED_WORKFLOW, DELETED_GATE, SECRET_MATERIAL
      (AKIA + PEM patterns), HARDCODED_CREDENTIAL all fire; benign lines
      silent

Exit 0 = all green. Exit 1 = a fail-safe broke (this is a bug report,
not a judgment disagreement).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

CALC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CALC_DIR))
import scorecard_calc as C  # noqa: E402

REPO = Path(subprocess.run(
    ["git", "-C", str(CALC_DIR), "rev-parse", "--show-toplevel"],
    capture_output=True, text=True, check=True).stdout.strip())
REF = subprocess.run(
    ["git", "-C", str(REPO), "rev-parse", "HEAD"],
    capture_output=True, text=True, check=True).stdout.strip()
RECEIPT_ID = 6200000001  # test placeholder — test artifacts, not authority

DIMS = ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN")


def make_packet(evidence_fn, claim=9.0, harm_found=False, harm_note=""):
    return C.validate_packet({
        "packet_version": 1,
        "change_id": "NEG-TEST",
        "title": "negative-probe test",
        "merge_sha": REF,
        "grader": "test_negative",
        "harm_check": {"found": harm_found, "note": harm_note},
        "judgments": [
            {"dimension": d, "score": claim,
             "evidence": evidence_fn(d), "rationale": ""}
            for d in DIMS
        ],
    })


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))
    return cond


def test_a_fabricated_citation():
    """(a) fabricated path -> UNVERIFIABLE ledger; 9.0 capped to 5.0."""
    pkt = make_packet(
        lambda d: [{"kind": "file", "path": "tools/no-such-file-definitely-xyz.md"}])
    card = C.build_scorecard(pkt, str(REPO), REF, RECEIPT_ID, "neg-test")
    ok = True
    ok &= check("a: card emitted, not disqualified",
                card["verdict"] != "DISQUALIFIED" and card["score"] is not None,
                f"verdict={card['verdict']} score={card['score']}")
    ok &= check("a: ledger verdict UNVERIFIABLE for the fabricated path",
                any(e["status"] == "UNVERIFIABLE"
                    and "not present" in e["detail"]
                    for e in card["evidence_ledger"]))
    per = {d: j for d, j in card["per_area"].items()}
    ok &= check("a: claimed 9.0 -> applied 5.0 with UNCITED_CAP",
                all(per[d]["applied"] == 5.0
                    and per[d]["flags"] == ["UNCITED_CAP"] for d in DIMS),
                "applied=" + ",".join(str(per[d]["applied"]) for d in DIMS))
    ok &= check("a: weighted score 5.0, verdict THIN",
                card["score"] == 5.0 and card["verdict"] == "THIN",
                f"score={card['score']} verdict={card['verdict']}")
    return ok


def test_b_attested_only():
    """(b) kind=command only -> 5.0 with UNCITED_CAP (attested != verified)."""
    pkt = make_packet(
        lambda d: [{"kind": "command", "note": "ran the tests, all green — trust me"}])
    card = C.build_scorecard(pkt, str(REPO), REF, RECEIPT_ID, "neg-test")
    per = {d: j for d, j in card["per_area"].items()}
    ok = True
    ok &= check("b: ledger verdict ATTESTED (grader's word, not machine-verified)",
                any(e["status"] == "ATTESTED" for e in card["evidence_ledger"]))
    ok &= check("b: attested-only -> applied 5.0 with UNCITED_CAP",
                all(per[d]["applied"] == 5.0
                    and per[d]["flags"] == ["UNCITED_CAP"] for d in DIMS))
    ok &= check("b: score 5.0, verdict THIN", card["score"] == 5.0)
    return ok


def test_c_builder_attested_harm():
    """(c) builder-attested harm -> DISQUALIFIED, score None, no judgments."""
    pkt = make_packet(lambda d: [], harm_found=True,
                      harm_note="I shipped a credential by accident")
    card = C.build_scorecard(pkt, str(REPO), REF, RECEIPT_ID, "neg-test")
    ok = True
    ok &= check("c: verdict DISQUALIFIED",
                card["verdict"] == "DISQUALIFIED" and card["disqualified"] is True,
                f"verdict={card['verdict']}")
    ok &= check("c: score is None (a harmful change gets no score)",
                card["score"] is None)
    ok &= check("c: no judgments emitted", card["judgments"] == [])
    ok &= check("c: hit named BUILDER_ATTESTED",
                any(h["pattern"] == "BUILDER_ATTESTED" for h in card["harm"]["hits"]))
    return ok


def test_d_missing_receipt_post():
    """(d) no receipt-posted comment id -> CLI exit 2, no card file."""
    pkt = make_packet(lambda d: [])
    pkt_path = CALC_DIR / ".test-neg-packet.json"
    out_path = CALC_DIR / ".test-neg-card.json"
    pkt_path.write_text(json.dumps(pkt, indent=2), encoding="utf-8")
    try:
        p = subprocess.run(
            [sys.executable, str(CALC_DIR / "scorecard_calc.py"),
             "--repo", str(REPO), "--sha", REF,
             "--packet", str(pkt_path), "--judge", "neg-test",
             "--out", str(out_path)],   # no --receipt-posted-comment-id
            capture_output=True, text=True, timeout=120)
    finally:
        pkt_path.unlink(missing_ok=True)
    ok = True
    ok &= check("d: exit code 2 (argparse: required id missing — fail-closed)",
                p.returncode == 2, f"exit={p.returncode}")
    ok &= check("d: no card file emitted", not out_path.exists())
    return ok


def test_e_harm_regex():
    """(e) every harm pattern fires; benign lines stay silent."""
    cases = [
        ("DELETED_WORKFLOW",
         "-diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml", True),
        ("DELETED_WORKFLOW",
         "-.github/workflows/nightly.yml", True),
        ("DELETED_GATE",
         "-diff --git a/kernel/protocol/gate.md b/kernel/protocol/gate.md", True),
        ("SECRET_MATERIAL",
         "+    \"aws_key\": \"" + "AKIA" + "IOSFODNN7EXAMPLE" + "\"", True),
        ("SECRET_MATERIAL",
         "+-----BEGIN " + "RSA PRIVATE KEY-----", True),
        ("HARDCODED_CREDENTIAL",
         "+    api" + "_key = 'sk-live-1234567890'", True),
        ("HARDCODED_CREDENTIAL",
         '+pass' + 'word="hunter2secret"', True),
        ("BENIGN (silent)",
         "+def hello():\n+    return 'world'", False),
        ("BENIGN (silent)",
         "--- a/.github/workflows/ci.yml\n+++ b/.github/workflows/ci.yml", False),
        ("BENIGN (silent)",
         "+    password_hash = compute(password)", False),
    ]
    ok = True
    for want, diff, fires in cases:
        found, hits = C.harm_scan({"diff_text": diff})
        got = [h["pattern"] for h in hits]
        if fires:
            cond = want in got
        else:
            cond = not found
        ok &= check(f"e: {want} on {diff[:48]!r}",
                    cond, f"hits={got}" if not cond else f"hits={got}")
    return ok


def main():
    print(f"repo: {REPO}")
    print(f"ref:  {REF[:12]}")
    print()
    results = [
        test_a_fabricated_citation(),
        test_b_attested_only(),
        test_c_builder_attested_harm(),
        test_d_missing_receipt_post(),
        test_e_harm_regex(),
    ]
    print()
    n = sum(results)
    if all(results):
        print(f"PASS — all 5 fail-safe probes green ({n}/5).")
        return 0
    print(f"FAIL — {5 - n}/5 fail-safe probes broken; a fail-safe that fails is a bug.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
