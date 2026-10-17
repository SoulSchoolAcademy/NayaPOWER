"""Decision CLI — the thin command-line front door to the decision engine.

The decision calculator ALREADY EXISTS: kernel/value_calculus.py,
Decision Value Calculus V2.1 (evaluate_candidates, gates, pareto
frontier, decision receipts). Do NOT reimplement it. This file is only
the front door: Shawn's format in, the engine's math out.

Shawn's format (2026-10-14): three top decisions, pros and cons of
each, best possible decision. Check the calculator, check the math.

Usage:
    python3 tools/decision_cli.py --input decision.json
    cat decision.json | python3 tools/decision_cli.py
    python3 tools/decision_cli.py --input decision.json --json

Exit codes: 0 = engine says ACT (a selection exists), 1 = READ_MORE /
ASK / REFUSE (no auto-selection — get evidence or decide as a human),
2 = unreadable input.

Input JSON:
    {
      "situation": "what we are deciding, one line",
      "options": [
        {"name": "Option A",
         "pros": ["..."], "cons": ["..."],
         "evidence_refs": ["path / SHA / comment id"],
         "reversible": true,
         "blast_radius": "low" | "medium" | "high",
         "quality": {"objective_fit": 9, "applicability": 8, "simplicity": 7},
         "confidence": {"objective_fit": 0.9},
         "pv": {"B": 10, "H": 1, "C": 1, "R": 0,
                "confidence": {"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9}}}
      ]
    }

Translation rules (printed in every report, so the worker can check
them — nothing is silent):
  evidence_sufficiency: >=2 refs 10; 1 ref 7; 0 refs 0.
  reversibility: true 10; false 3.
  blast_containment: low 10; medium 6; high 3.
  robustness: pros-minus-cons >=2 -> 10; 1 -> 8; 0 -> 5; -1 -> 3; <=-2 -> 1.
  objective_fit / applicability / simplicity: from "quality" if given,
    else 5.0 ASSUMED (disclosed — score them yourself for a real decision).
  confidence per dimension: from "confidence" if given, else 0.8 ASSUMED.
  pv: from "pv" if given, else all zeros — the engine then correctly
    returns READ_MORE (no value numbers, no value decision). Provide
    B/H/C/R + confidence to get a selection.
  authority: the worker asserts every option is within their authorized
    scope (engine flag authorized=True). The engine still enforces its
    own hard gates (harm intent, law, rights, privacy, safety, tails).

Pros and cons are REQUIRED by the process and printed in the report as
the written reasoning behind the scores. They are not re-scored by a
second engine — the balance rule above is the only translation, and it
is printed.
"""

import argparse
import json
import sys

sys.path.insert(0, "kernel")
from value_calculus import (  # noqa: E402
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
)

BASELINE_ID = "baseline-do-nothing"
ASSUMED_QUALITY = 5.0
ASSUMED_CONFIDENCE = 0.8


def _balance(pros, cons):
    diff = len(pros or []) - len(cons or [])
    if diff >= 2:
        return 10.0
    if diff == 1:
        return 8.0
    if diff == 0:
        return 5.0
    if diff == -1:
        return 3.0
    return 1.0


def _evidence_score(refs):
    n = len(refs or [])
    if n >= 2:
        return 10.0
    if n == 1:
        return 7.0
    return 0.0


def _blast_score(radius):
    return {"low": 10.0, "medium": 6.0, "high": 3.0}.get(radius, 5.0)


def build_candidates(decision):
    """Translate Shawn's format into engine Candidates. Returns
    (candidates, assumed_notes). Nothing is silent: every default is
    recorded in assumed_notes."""
    candidates = []
    assumed = []
    for i, opt in enumerate(decision.get("options") or []):
        if not isinstance(opt, dict):
            continue
        name = opt.get("name") or "option-%d" % (i + 1)
        refs = opt.get("evidence_refs") or []
        pros = opt.get("pros") or []
        cons = opt.get("cons") or []
        quality_in = opt.get("quality") or {}
        confidence_in = opt.get("confidence") or {}
        quality = {
            "evidence_sufficiency": _evidence_score(refs),
            "reversibility": 10.0 if opt.get("reversible", True) else 3.0,
            "blast_containment": _blast_score(opt.get("blast_radius", "low")),
            "robustness": _balance(pros, cons),
        }
        for dim in ("objective_fit", "applicability", "simplicity"):
            if dim in quality_in:
                quality[dim] = float(quality_in[dim])
            else:
                quality[dim] = ASSUMED_QUALITY
                assumed.append("%s: %s assumed %.1f (not scored)"
                               % (name, dim, ASSUMED_QUALITY))
        confidence = {}
        for dim in ("objective_fit", "evidence_sufficiency", "applicability",
                    "robustness", "reversibility", "blast_containment",
                    "simplicity"):
            if dim in confidence_in:
                confidence[dim] = float(confidence_in[dim])
            else:
                confidence[dim] = ASSUMED_CONFIDENCE
                assumed.append("%s: confidence[%s] assumed %.1f"
                               % (name, dim, ASSUMED_CONFIDENCE))
        pv_in = opt.get("pv") or {}
        if pv_in:
            pv = PVEstimate(
                B=float(pv_in.get("B", 0)), H=float(pv_in.get("H", 0)),
                C=float(pv_in.get("C", 0)), R=float(pv_in.get("R", 0)),
                confidence={k: float(v) for k, v in
                            (pv_in.get("confidence") or {}).items()},
                evidence_count=len(refs))
        else:
            pv = PVEstimate(B=0, H=0, C=0, R=0, confidence={},
                             evidence_count=len(refs))
            assumed.append("%s: pv not provided — value delta is 0, engine "
                           "returns READ_MORE until B/H/C/R given" % name)
        candidates.append(Candidate(
            candidate_id=name,
            quality=quality,
            confidence=confidence,
            pv=pv,
            authorized=True,  # worker asserts: within authorized scope
            lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
            reversible=bool(opt.get("reversible", True)),
        ))
    baseline = Candidate(
        candidate_id=BASELINE_ID,
        quality={d: 0.0 for d in
                 ("objective_fit", "evidence_sufficiency", "applicability",
                  "robustness", "reversibility", "blast_containment",
                  "simplicity")},
        confidence={},
        pv=PVEstimate(B=0, H=0, C=0, R=0, confidence={}, evidence_count=0),
        authorized=True, lawful=True, rights_safe=True, privacy_safe=True,
        safety_safe=True, is_baseline=True)
    candidates.append(baseline)
    return candidates, assumed


def decide(decision):
    """Run the engine on Shawn's format. Returns the report dict."""
    if not isinstance(decision, dict):
        return {"situation": "", "decision": None, "selected": None,
                "rows": [], "assumed": [],
                "next": "Provide the decision as JSON with situation + options."}
    candidates, assumed = build_candidates(decision)
    profile = QualityProfile(
        profile_id="decision-cli", version="1.0",
        objective=decision.get("situation", ""))
    result = evaluate_candidates(candidates, BASELINE_ID, profile, RiskPolicy())
    pros_cons = {}
    for opt in decision.get("options") or []:
        if isinstance(opt, dict):
            pros_cons[opt.get("name") or ""] = {
                "pros": opt.get("pros") or [], "cons": opt.get("cons") or []}
    # This adapter has no trusted authority/safety resolver. The Candidate
    # flags above are provisional assumptions for ranking only; they must
    # never be interpreted as authorization. Preserve the engine's ranking,
    # but fail closed at the CLI boundary until a trusted resolver exists.
    decision_status = result["decision"]
    selected = result["selected"]
    governance_authorization = "UNRESOLVED_NO_TRUSTED_GATE_RESOLVER"
    # The engine's hard-gate booleans are provisional adapter assumptions.
    # Label each candidate row as unresolved so a human reader cannot mistake
    # the provisional internal calculation for an independently cleared gate.
    for row in result.get("rows", []):
        if row.get("is_baseline"):
            continue
        row["gate"] = "UNRESOLVED"
        reasons = list(row.get("gate_reasons") or [])
        reasons.append("trusted authority/law/rights/privacy/safety resolver is not connected; advisory ranking only")
        row["gate_reasons"] = reasons
    if decision_status == "ACT":
        decision_status = "READ_MORE"
        selected = None
        nxt = ("Advisory ranking only. The calculator ranked %s, but ACT is "
               "withheld: no trusted authority/law/rights/privacy/safety gate "
               "resolver is connected. Resolve those gates independently."
               % result["selected"])
    elif result["decision"] == "ASK":
        nxt = ("Engine says ASK — a human decision is needed. Bring the "
               "ranking + pros/cons, not a bare question.")
    elif result["decision"] == "REFUSE":
        nxt = "Engine says REFUSE — every option is prohibited. Do not proceed."
    else:
        nxt = ("Engine says READ_MORE — get the missing evidence / PV "
               "numbers, then re-decide.")
    return {
        "situation": decision.get("situation", ""),
        "decision": decision_status,
        "selected": selected,
        "governance_authorization": governance_authorization,
        "top3": result["top3"],
        "rows": result["rows"],
        "pros_cons": pros_cons,
        "assumed": assumed,
        "next": nxt,
    }


def render_human(report):
    lines = ["Decision: %s" % (report.get("situation") or "(unstated)")]
    lines.append("Engine: %s — selected: %s"
                 % (report.get("decision"), report.get("selected")))
    for row in report["rows"]:
        if row.get("is_baseline"):
            continue
        pc = report.get("pros_cons", {}).get(row["candidate_id"], {})
        lines.append("  %-20s gate=%s Q=%.1f delta_v=%.1f v_safe=%.1f"
                     % (row["candidate_id"][:20], row["gate"],
                        row["q"]["Q"], row["delta_v"], row["v_safe"]))
        if row["gate_reasons"]:
            lines.append("    gate reasons: %s" % "; ".join(row["gate_reasons"]))
        if pc.get("pros"):
            lines.append("    pros: %s" % "; ".join(pc["pros"]))
        if pc.get("cons"):
            lines.append("    cons: %s" % "; ".join(pc["cons"]))
    if report.get("assumed"):
        lines.append("Assumed (check these — nothing is silent):")
        for note in report["assumed"]:
            lines.append("  - %s" % note)
    lines.append("Next: %s" % report["next"])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Decision CLI (value_calculus front door).")
    parser.add_argument("--input", default=None, help="JSON file (default: stdin)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    try:
        raw = open(args.input).read() if args.input else sys.stdin.read()
        decision = json.loads(raw)
    except (OSError, ValueError):
        report = decide(None)
        print(render_human(report) if not args.json else json.dumps(report, indent=2))
        return 2
    report = decide(decision)
    print(render_human(report) if not args.json else json.dumps(report, indent=2))
    return 0 if report["decision"] == "ACT" else 1


if __name__ == "__main__":
    raise SystemExit(main())
