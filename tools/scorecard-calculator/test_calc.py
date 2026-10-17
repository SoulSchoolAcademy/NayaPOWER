#!/usr/bin/env python3
"""Scorecard calculator agreement test — runnable by a different seat.

For each of the three hand-written HV scorecards (the calculator's ground
truth), this script:
  1. Derives the builder's claim set from the human scorecard:
     claimed scores + cited evidence + rationale (the human is the builder;
     the calculator is the mechanical judge).
  2. Runs tools/scorecard-calculator/scorecard_calc.py against the
     scorecard's merge SHA in the local repo.
  3. Compares the calculator's per-dimension APPLIED scores against the
     human's applied scores and prints an agreement/divergence table.

Pass criterion: the calculator reproduces the human's applied scores —
every divergence < 0.5 (the rubric's own agree/review band boundary is
0.5; anything at or above it is a real judge disagreement and fails).

Note on --receipt-posted-comment-id: the hand-written scorecards carry no
board comment id, so the harness passes a synthetic placeholder. Outputs
are TEST artifacts, not authority receipts — a real run must pass the real
board comment id where the receipt was posted.

Usage:
  python3 tools/scorecard-calculator/test_calc.py [--repo REPO]
  (defaults --repo to the git top-level containing this script)

Exit 0 = all three ran clean and every divergence < 0.5.
Exit 1 = a divergence >= 0.5 or a calculator failure.
Exit 2 = harness input error.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

CALC_DIR = Path(__file__).resolve().parent
CALC = CALC_DIR / "scorecard_calc.py"

SUBJECTS = [
    ("HV-20261011-PR-2188.scorecard.json",
     "312e1fd3b4f049a2ba50b29fb30e3f509cc22afa"),
    ("HV-20261011-PR-2375.scorecard.json",
     "09d9b71a313012320eb25c21aa92863884678633"),
    ("HV-20261011-PR-2383.scorecard.json",
     "b5007fd8d21a550930761b74f31c6ce9026296b7"),
]

SCORECARD_DIR_NAME = "tools/human_value/observatory/scorecards"
# Synthetic placeholder — see module docstring. Real runs need the real id.
RECEIPT_POSTED_COMMENT_ID = 6200000001

DIVERGENCE_FAIL_AT = 0.5


def repo_root(repo_arg):
    if repo_arg:
        return Path(repo_arg)
    p = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True, cwd=str(CALC_DIR))
    if p.returncode != 0:
        print("cannot find git top-level", file=sys.stderr)
        sys.exit(2)
    return Path(p.stdout.strip())


def packet_from_human_scorecard(sc):
    """The human scorecard IS the builder's claim set: claimed scores, cited
    evidence, rationale. The calculator re-verifies and re-applies the caps.

    Note: the hand-written scorecards keep evidence in a top-level
    `evidence_ledger` (grouped per dimension); the packet needs it nested
    under each judgment, so we regroup it here — no content is invented."""
    ledger_by_dim = {}
    for item in sc.get("evidence_ledger", []):
        ev = {"kind": item["kind"]}
        if item.get("lines") is not None:
            ev["lines"] = item["lines"]
        if item["kind"] in ("file", "test", "receipt"):
            ev["path"] = item["citation"]
        elif item["kind"] == "sha":
            ev["sha"] = item["citation"]
        # command / url carry no address — the grader's word only
        ledger_by_dim.setdefault(item["dimension"], []).append(ev)
    packet = {
        "packet_version": 1,
        "change_id": sc["change_id"],
        "title": sc["title"],
        "merge_sha": sc["merge_sha"],
        "grader": sc["grader"],
        "harm_check": {"found": bool(sc.get("disqualified", False)),
                       "note": sc.get("harm_note", "")},
        "judgments": [],
    }
    for j in sc["judgments"]:
        packet["judgments"].append({
            "dimension": j["dimension"],
            "score": j["claimed"],
            "evidence": ledger_by_dim.get(j["dimension"], []),
            "rationale": j.get("rationale", ""),
        })
    return packet


def run_subject(root, fname, sha):
    sc_path = root / SCORECARD_DIR_NAME / fname
    try:
        human = json.loads(sc_path.read_text(encoding="utf-8"))
    except OSError as ex:
        return {"error": f"cannot read {sc_path}: {ex}"}
    packet = packet_from_human_scorecard(human)
    packet_path = CALC_DIR / f".test-packet-{human['change_id']}.json"
    packet_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    out_path = CALC_DIR / f".test-card-{human['change_id']}.json"
    try:
        p = subprocess.run(
            [sys.executable, str(CALC),
             "--repo", str(root),
             "--sha", sha,
             "--packet", str(packet_path),
             "--receipt-posted-comment-id", str(RECEIPT_POSTED_COMMENT_ID),
             "--judge", "agreement-test-harness",
             "--out", str(out_path)],
            capture_output=True, text=True, timeout=300,
        )
    finally:
        packet_path.unlink(missing_ok=True)
    if p.returncode != 0:
        return {"error": f"calculator exit {p.returncode}: "
                         f"{(p.stdout or '')[-500:]} {(p.stderr or '')[-500:]}"}
    try:
        card = json.loads(out_path.read_text(encoding="utf-8"))
    finally:
        out_path.unlink(missing_ok=True)
    return {"human": human, "card": card}


def main(argv):
    repo_arg = argv[1] if len(argv) > 1 else None
    root = repo_root(repo_arg)
    print(f"repo: {root}")
    print(f"receipt-posted placeholder: {RECEIPT_POSTED_COMMENT_ID} (test harness, not authority)")
    print()

    failures = []
    for fname, sha in SUBJECTS:
        res = run_subject(root, fname, sha)
        if "error" in res:
            print(f"### {fname}: CALCULATOR FAILURE — {res['error']}")
            failures.append((fname, "calculator failure"))
            continue
        human, card = res["human"], res["card"]
        cid = human["change_id"]
        h_score, c_score = human["score"], card["score"]
        print(f"### {cid} — {human['title']}")
        print(f"    human score {h_score} ({human['verdict']}) | "
              f"calculator score {c_score} ({card['verdict']}) | "
              f"delta {abs(h_score - c_score):.1f}")
        h_j = {j["dimension"]: j for j in human["judgments"]}
        c_j = {d: j for d, j in card["per_area"].items()}
        worst = 0.0
        for dim in ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN"):
            ha, ca = h_j[dim]["applied"], c_j[dim]["applied"]
            dv = abs(ha - ca)
            worst = max(worst, dv)
            flag = "  <-- DIVERGENCE >= 0.5" if dv >= DIVERGENCE_FAIL_AT else ""
            print(f"    {dim:7s} human {ha:4.1f}  calc {ca:4.1f}  |div| {dv:.1f}"
                  f"  flags={','.join(c_j[dim]['flags']) or '-'}{flag}")
            if dv >= DIVERGENCE_FAIL_AT:
                reasons = "; ".join(
                    d["reason"] for d in c_j[dim]["deductions"]) or "no deduction recorded"
                print(f"             reason: {reasons}")
                failures.append((cid, dim, dv, reasons))
        # schema-conformance is enforced inside the calculator (exit 0 only on
        # valid output); double-check the frame fields exist here.
        for k in ("scope_target", "scope_action", "decided_at", "decided_by",
                  "promotion_option_id", "step1_enumerate", "step2_score",
                  "step3_gate", "step4_decide", "step5_receipt"):
            assert k in card, f"receipt frame field missing: {k}"
        assert card["promotion_option_id"] == card["step4_decide"]["winner"]
        print(f"    worst per-dimension divergence: {worst:.1f} | "
              f"receipt frame: valid (promotion_option_id == winner)")
        print()
    if failures:
        print("FAIL — disagreements at or above the 0.5 band:")
        for f in failures:
            print("   ", f)
        return 1
    print("PASS — calculator reproduces all three human scorecards within the "
          "0.5 agree band; all outputs receipt-schema-valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
