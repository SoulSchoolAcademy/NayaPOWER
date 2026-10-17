#!/usr/bin/env python3
"""Automatic Decision Calculator — the water itself.

One command in, the most intelligent decision out. Instantly.

This is a thin convenience wrapper over the canonical decision seams in
``kernel/value_calculus.py`` (gate_candidate, evaluate_candidates). It creates
NO new decision engine, NO new scorecard, NO new authority system — repo law.
All gating and scoring is the canonical engine's; this tool only translates
plain inputs into it, classifies how much thought the decision deserves
(Wisdom Spending Principle, Law 1b), and explains the answer in true words.

Usage:
    python3 tools/decision_calculator.py decide --input decision.json
    python3 tools/decision_calculator.py decide < decision.json
    python3 tools/decision_calculator.py decide --dry-run --input decision.json
    python3 tools/decision_calculator.py batch --input batch.json
    python3 tools/decision_calculator.py outcome --decision-id dc-... --actual-delta 7.0
    python3 tools/decision_calculator.py calibrate [--ledger PATH]

Input JSON (decide):
    {
      "question": "Should we merge PR #2407 now?",
      "objective": "Keep main green with minimum risk",
      "options": [
        {"id": "merge-now", "description": "...", "value_estimate": 8.0,
         "evidence": ["CI green", "IV passed"],
         "reversible": true, "authorized": true,
         "harm": {"severity": 2.0, "probability": 0.01},
         "deceptive": false, "forbidden": false}
      ],
      "context": {"reversibility": "high", "stakes": "low", "time_pressure": "low"}
    }

Exit codes: 0 = decided (ACT/READ_MORE/ASK/REFUSE are all legitimate answers),
2 = needs clarification or invalid input (questions printed, nothing decided).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from kernel.value_calculus import (  # noqa: E402
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    PVEstimate,
    Candidate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    build_decision_receipt,
    calibration_summary,
    evaluate_candidates,
)

CALCULATOR_VERSION = "1.0.0"
DEFAULT_LEDGER = os.path.expanduser("~/workspace/decision-ledger.jsonl")

EXAMPLE_JSON = """{
  "question": "Should we merge PR #2407 now or wait for independent validation?",
  "objective": "Keep main green with minimum risk",
  "options": [
    {"id": "merge-now", "description": "Merge immediately",
     "value_estimate": 8.0, "evidence": ["CI green on head", "IV passed 9.2/10"],
     "reversible": true, "authorized": true,
     "harm": {"severity": 2.0, "probability": 0.01}},
    {"id": "wait-iv", "description": "Wait for independent validation",
     "value_estimate": 6.5, "evidence": ["IV usually catches 1-2 issues"],
     "reversible": true, "authorized": true}
  ],
  "context": {"reversibility": "high", "stakes": "low", "time_pressure": "low"}
}"""

QUALITY_DIMS = (
    "objective_fit",
    "evidence_sufficiency",
    "applicability",
    "robustness",
    "reversibility",
    "blast_containment",
    "simplicity",
)

# Calculator-tuned profile: strict enough to say "I don't know yet" on thin
# evidence, lenient enough that reasonable inputs get answers.
CALCULATOR_PROFILE = QualityProfile(
    profile_id="auto-decision-calculator",
    version="1.0.0",
    objective="Automatic scored decisions with honest uncertainty",
    q_accept=6.0,
    aggregate_confidence_floor=0.60,
    critical_confidence_floor=0.50,
    min_evidence_count=1,
    relative_margin=0.05,
    min_reversibility_for_auto=6.0,
)


# --------------------------------------------------------------------------
# Wisdom check (Law 1b): how much thought does THIS decision deserve?
# --------------------------------------------------------------------------

def classify_weight(context: dict, options: list) -> tuple[str, str]:
    """Return (tier, plain_reason). Tiers: five-minute | standard | foundational."""
    reversibility = str(context.get("reversibility", "high")).lower()
    stakes = str(context.get("stakes", "low")).lower()
    # Options that will be disqualified anyway (forbidden/deceptive) don't
    # set the decision's weight — they never compete.
    live = [o for o in options if not (o.get("forbidden") or o.get("deceptive"))]
    any_irreversible = any(not o.get("reversible", True) for o in live)

    if stakes == "consequential" or any_irreversible or reversibility == "low":
        return ("foundational",
                "the stakes are consequential or the action cannot be undone")
    if stakes == "high":
        return ("standard",
                "the stakes are high but the action is reversible")
    return ("five-minute",
            "the stakes are low and the action is reversible")


# --------------------------------------------------------------------------
# Input validation → clarifying questions (never assume on critical fields)
# --------------------------------------------------------------------------

def normalize_payload(payload) -> dict:
    """Apply the same forgiving parsing as clarifying_questions."""
    if isinstance(payload, list):
        payload = {"question": "", "options": payload}
    if isinstance(payload, dict):
        options = payload.get("options")
        if isinstance(options, dict):
            payload = dict(payload, options=[options])
    return payload


def clarifying_questions(payload: dict) -> list[str]:
    questions: list[str] = []
    if isinstance(payload, list):
        # Forgiving: a bare list is treated as the options list.
        payload = {"question": "", "options": payload}
    if not isinstance(payload, dict):
        return ["Give me a JSON object with 'question' and 'options' — or run with --example to see one."]
    if not payload.get("question"):
        questions.append("What decision are you trying to make? (one sentence)")
    options = payload.get("options")
    if isinstance(options, dict):
        options = [options]  # forgiving: single option object
    if not isinstance(options, list) or len(options) == 0:
        questions.append("Give me at least one option to score (besides doing nothing).")
        return questions
    seen: set[str] = set()
    for i, o in enumerate(options):
        if not isinstance(o, dict):
            questions.append(f"Option #{i + 1} must be an object with an 'id'.")
            continue
        oid = o.get("id") or f"option-{i + 1}"
        if oid in seen:
            questions.append(f"Two options share the id '{oid}' — give each a unique id.")
        seen.add(oid)
        if o.get("value_estimate") is None and not o.get("evidence"):
            questions.append(
                f"What's the expected value of '{oid}' (0-10), and what evidence supports it? "
                "I won't guess — without either, I can't score it honestly."
            )
        ve = o.get("value_estimate")
        if ve is not None:
            try:
                ve_f = float(ve)
                if not (0.0 <= ve_f <= 10.0):
                    questions.append(
                        f"'{oid}': value_estimate must be between 0 and 10 (got {ve}). "
                        "0 = worthless, 10 = the best possible outcome.")
            except (TypeError, ValueError):
                questions.append(f"'{oid}': value_estimate must be a number (got {ve!r}).")
        harm = o.get("harm") or {}
        if isinstance(harm, dict):
            prob = harm.get("probability")
            if prob is not None:
                try:
                    if not (0.0 <= float(prob) <= 1.0):
                        questions.append(
                            f"'{oid}': harm probability must be between 0 and 1 (got {prob}).")
                except (TypeError, ValueError):
                    questions.append(f"'{oid}': harm probability must be a number (got {prob!r}).")
            sev = harm.get("severity")
            if sev is not None:
                try:
                    if float(sev) < 0:
                        questions.append(f"'{oid}': harm severity can't be negative (got {sev}).")
                except (TypeError, ValueError):
                    questions.append(f"'{oid}': harm severity must be a number (got {sev!r}).")
    return questions


# --------------------------------------------------------------------------
# Translation: plain option → kernel Candidate (the only place defaults live,
# and every default is recorded as an assumption in the receipt)
# --------------------------------------------------------------------------

def _clamp10(v) -> float:
    return max(0.0, min(10.0, float(v)))


def to_candidate(opt: dict, assumptions: list) -> Candidate:
    oid = str(opt.get("id", "option"))
    value = float(opt.get("value_estimate", 5.0))
    if "value_estimate" not in opt:
        assumptions.append(f"'{oid}': no value_estimate given — assumed 5.0 (neutral).")
    evidence = opt.get("evidence") or []
    if not isinstance(evidence, list):
        evidence = [evidence]
    n_ev = len(evidence)

    reversible = opt.get("reversible", True)
    if "reversible" not in opt:
        assumptions.append(f"'{oid}': reversibility not stated — assumed reversible.")
    authorized = bool(opt.get("authorized", True))
    if "authorized" not in opt:
        assumptions.append(f"'{oid}': authorization not stated — assumed authorized.")

    harm = opt.get("harm") or {}
    sev = float(harm.get("severity", 0.0))
    prob = float(harm.get("probability", 0.0))
    harm_class = str(harm.get("class", "general"))

    deceptive = bool(opt.get("deceptive", False))
    forbidden = bool(opt.get("forbidden", False))

    q_over = opt.get("quality") or {}
    quality = {
        "objective_fit": _clamp10(q_over.get("objective_fit", value)),
        "evidence_sufficiency": _clamp10(q_over.get("evidence_sufficiency", min(10.0, 3.0 + 2.0 * n_ev))),
        "applicability": _clamp10(q_over.get("applicability", 7.0)),
        "robustness": _clamp10(q_over.get("robustness", 6.0)),
        "reversibility": _clamp10(q_over.get("reversibility", 9.0 if reversible else 2.0)),
        "blast_containment": _clamp10(q_over.get("blast_containment", max(0.0, 10.0 - sev))),
        "simplicity": _clamp10(q_over.get("simplicity", 7.0)),
    }
    c_over = opt.get("confidence") or {}
    ev_conf = min(1.0, 0.25 + 0.25 * n_ev)  # 0 evidence → 0.25; 2+ → 0.75
    b_conf = min(1.0, 0.30 + 0.25 * n_ev)
    confidence = {
        "objective_fit": float(c_over.get("objective_fit", 0.7)),
        "evidence_sufficiency": float(c_over.get("evidence_sufficiency", ev_conf)),
        "applicability": float(c_over.get("applicability", 0.7)),
        "robustness": float(c_over.get("robustness", 0.6)),
        "reversibility": float(c_over.get("reversibility", 0.8)),
        "blast_containment": float(c_over.get("blast_containment", 0.6)),
        "simplicity": float(c_over.get("simplicity", 0.7)),
    }

    pv = PVEstimate(
        B=value, H=sev, C=1.0, R=prob * 10.0,
        confidence={"B": b_conf, "H": 0.6, "C": 0.7, "R": 0.5},
        evidence_count=n_ev,
    )
    tails = (TailRisk(severity=sev, probability=prob, harm_class=harm_class),) if (sev > 0 or prob > 0) else ()

    stakes = str(opt.get("stakes", "low")).lower()
    if stakes not in ("low", "high", "consequential"):
        stakes = "low"

    # Safety/rights/privacy/lawfulness: assumed safe unless stated otherwise.
    # One assumption line covers all four — the calculator stays usable.
    safe_flags = {}
    for flag in ("lawful", "rights_safe", "privacy_safe", "safety_safe"):
        if flag in opt:
            safe_flags[flag] = bool(opt[flag])
        else:
            safe_flags[flag] = True
    if not any(f in opt for f in ("lawful", "rights_safe", "privacy_safe", "safety_safe")):
        assumptions.append(f"'{oid}': lawfulness/rights/privacy/safety not specified — assumed safe.")
    if sev >= 9.0 and "safety_safe" not in opt:
        safe_flags["safety_safe"] = None  # high severity → safety genuinely unknown

    return Candidate(
        candidate_id=oid,
        quality=quality,
        confidence=confidence,
        pv=pv,
        tails=tails,
        authorized=authorized,
        human_authorized=bool(opt.get("human_authorized", False)),
        hard_violation=bool(deceptive or forbidden),
        lawful=safe_flags["lawful"],
        rights_safe=safe_flags["rights_safe"],
        privacy_safe=safe_flags["privacy_safe"],
        safety_safe=safe_flags["safety_safe"],
        stakes=stakes,
        reversible=reversible,
        is_baseline=False,
    )


def baseline_candidate() -> Candidate:
    conf = {d: 0.8 for d in QUALITY_DIMS}
    return Candidate(
        candidate_id="do-nothing",
        quality={d: 5.0 for d in QUALITY_DIMS},
        confidence=conf,
        pv=PVEstimate(B=2.0, H=0.0, C=0.0, R=0.0,
                      confidence={"B": 0.8, "H": 0.9, "C": 0.9, "R": 0.9},
                      evidence_count=1),
        authorized=True,
        reversible=True,
        stakes="low",
        is_baseline=True,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
    )


# --------------------------------------------------------------------------
# Plain-language explanation (true words, not fewer words)
# --------------------------------------------------------------------------

_GATE_PLAIN = {
    "JUDGMENT_RULE_HARD_STOP": "it violates a hard stop (forbidden scope or deception)",
    "LAW": "it breaks the law",
    "RIGHTS": "it violates rights",
    "PRIVACY": "it violates privacy",
    "SAFETY": "it is unsafe",
    "DISTRIBUTIONAL_HARM": "it concentrates harm on some stakeholders",
    "CONFLICT_REQUIRES_GOVERNANCE": "it has a conflict that needs governance",
    "AUTHORITY_MISSING": "no authority is recorded for it",
    "CONSEQUENTIAL_OR_IRREVERSIBLE": "it is consequential or irreversible with no human authorization",
    "HARD_GATE_UNKNOWN": "a hard gate could not be checked",
    "EVIDENCE_FLOOR": "it has too little evidence",
    "QUALITY_DIMENSION_MISSING": "a quality dimension is missing",
    "AGGREGATE_CONFIDENCE_FLOOR": "overall confidence is below the floor",
    "CRITICAL_CONFIDENCE_FLOOR": "confidence on a critical dimension is below the floor",
    "PV_COMPONENT_CONFIDENCE_FLOOR": "confidence on a value component is below the floor",
}


def _plain_reason(reason: str) -> str:
    if reason.startswith("TAIL_RISK:"):
        return f"tail risk ({reason.split(':', 1)[1]}) exceeds the safety bar"
    if reason.startswith("UNKNOWN_"):
        return f"{reason[len('UNKNOWN_'):].lower()} safety is unknown"
    return _GATE_PLAIN.get(reason, reason.lower().replace("_", " "))


def explain(evaluation: dict, winner_id: str | None, wisdom: dict) -> str:
    decision = evaluation["decision"]
    rows = {r["candidate_id"]: r for r in evaluation["rows"]}
    parts: list[str] = []

    disqualified = [(cid, r) for cid, r in rows.items()
                    if r["gate"] == PROHIBITED and cid != "do-nothing"]
    for cid, r in disqualified:
        why = "; ".join(_plain_reason(x) for x in r["gate_reasons"]) or "a hard gate"
        parts.append(f"Option '{cid}' was disqualified — not outscored, excluded — because {why}.")

    deferred = [(cid, r) for cid, r in rows.items()
                if r["gate"] in (NEEDS_AUTHORITY, NEEDS_EVIDENCE) and cid != "do-nothing"]
    for cid, r in deferred:
        why = "; ".join(_plain_reason(x) for x in r["gate_reasons"]) or "it needs something first"
        parts.append(f"Option '{cid}' is deferred, not decided: {why}.")

    if decision == "ACT" and winner_id:
        w = rows[winner_id]
        parts.append(
            f"Option '{winner_id}' won because it scored {w['q']['Q']:.1f}/10 on quality, "
            f"adds {w['v_safe']:.1f} safe value over doing nothing, and cleared every hard gate. "
            f"Confidence {w['q']['confidence_aggregate']:.2f}."
        )
        if evaluation.get("relative_margin") is not None and evaluation["relative_margin"] != float("inf"):
            parts.append(f"Winning margin over the runner-up: {evaluation['relative_margin'] * 100:.0f}%.")
    elif decision == "READ_MORE":
        missing = []
        for cid, r in deferred:
            if r["gate"] == NEEDS_EVIDENCE:
                crit = r["q"]["confidence_critical"]
                floor = CALCULATOR_PROFILE.critical_confidence_floor
                missing.append(f"'{cid}' needs more evidence (critical confidence "
                               f"{crit:.2f} is below the {floor:.2f} floor — "
                               "add at least 2 solid evidence items per option)")
        parts.append("I don't know yet — the evidence is too thin to decide honestly. " +
                     (" ".join(missing) if missing else "No admissible option is clearly better than doing nothing.") +
                     " I won't guess; bring more evidence and ask again.")
    elif decision == "ASK":
        parts.append("This needs a human decision — it crosses an authority boundary "
                     "(consequential, irreversible, or unauthorized). The calculator recommends, "
                     "it does not authorize.")
    elif decision == "REFUSE":
        parts.append("I refuse: every option was disqualified on the merits. Nothing may proceed.")

    if wisdom["tier"] == "foundational":
        parts.append("Note: this is a foundational decision — treat the answer above as a "
                     "recommendation. A human should review before acting.")
    return " ".join(parts)


# --------------------------------------------------------------------------
# The decide pipeline: wisdom → gates → score → receipt
# --------------------------------------------------------------------------

def decide_payload(payload: dict, dry_run: bool = False) -> dict:
    t0 = time.perf_counter()
    payload = normalize_payload(payload)
    questions = clarifying_questions(payload)
    if questions:
        return {"status": "needs_clarification", "questions": questions}

    context = payload.get("context") or {}
    options = payload["options"]
    tier, tier_why = classify_weight(context, options)

    assumptions: list[str] = []
    candidates = [baseline_candidate()]
    opt_by_id = {}
    for o in options:
        c = to_candidate(o, assumptions)
        candidates.append(c)
        opt_by_id[c.candidate_id] = o

    profile = CALCULATOR_PROFILE
    risk_policy = RiskPolicy()
    evaluation = evaluate_candidates(candidates, "do-nothing", profile, risk_policy)

    winner_id = evaluation.get("selected")
    rows = evaluation["rows"]
    ranking = [
        {"id": r["candidate_id"], "gate": r["gate"],
         "Q": round(r["q"]["Q"], 2), "v_safe": round(r["v_safe"], 2),
         "confidence": round(r["q"]["confidence_aggregate"], 2)}
        for r in sorted(
            [r for r in rows if r["candidate_id"] != "do-nothing"],
            key=lambda r: (r["gate"] != ADMISSIBLE, -r["v_safe"], -r["q"]["Q"]))
    ]
    disqualified = [
        {"id": r["candidate_id"], "gate": r["gate"],
         "reasons": r["gate_reasons"],
         "plain": "; ".join(_plain_reason(x) for x in r["gate_reasons"])}
        for r in rows
        if r["gate"] == PROHIBITED and r["candidate_id"] != "do-nothing"
    ]
    deferred = [
        {"id": r["candidate_id"], "gate": r["gate"],
         "reasons": r["gate_reasons"],
         "plain": "; ".join(_plain_reason(x) for x in r["gate_reasons"])}
        for r in rows
        if r["gate"] in (NEEDS_AUTHORITY, NEEDS_EVIDENCE) and r["candidate_id"] != "do-nothing"
    ]

    elapsed = time.perf_counter() - t0
    wisdom = {
        "tier": tier,
        "why": tier_why,
        "human_review_recommended": tier == "foundational",
        "thought_seconds": round(elapsed, 4),
    }
    explanation = explain(evaluation, winner_id, wisdom)

    winner_conf = None
    if winner_id and winner_id in {r["candidate_id"]: r for r in rows}:
        winner_conf = round({r["candidate_id"]: r for r in rows}[winner_id]["q"]["confidence_aggregate"], 2)

    decision_id = "dc-" + hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]

    kernel_receipt = build_decision_receipt(
        decision_id=decision_id,
        objective=str(payload.get("objective", payload.get("question", ""))),
        baseline_id="do-nothing",
        stakeholders=[],
        horizon="decision-time",
        evaluation=evaluation,
        authority_basis="calculator-convenience-wrapper; scores never create authority",
        evidence_refs=[e for o in options for e in (o.get("evidence") or [])],
        observation_window={"opened": None, "closed": None},
        verification="UNVERIFIED",
    )

    return {
        "status": "decided",
        "decision_id": decision_id,
        "question": payload.get("question", ""),
        "objective": payload.get("objective", ""),
        "engine_decision": evaluation["decision"],
        "winner": winner_id,
        "winner_confidence": winner_conf,
        "ranking": ranking,
        "disqualified": disqualified,
        "deferred": deferred,
        "explanation": explanation,
        "wisdom": wisdom,
        "assumptions": assumptions,
        "dry_run": dry_run,
        "calculator_version": CALCULATOR_VERSION,
        "engine_version": "DECISION-VALUE-CALCULUS-V2.1",
        "kernel_receipt": kernel_receipt,
    }


# --------------------------------------------------------------------------
# Learning loop: ledger + outcome + calibrate
# --------------------------------------------------------------------------

def ledger_append(record: dict, ledger_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(ledger_path)), exist_ok=True)
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def cmd_outcome(args) -> int:
    entry = {
        "type": "outcome",
        "decision_id": args.decision_id,
        "actual_delta": float(args.actual_delta),
        "note": args.note or "",
        "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    ledger_append(entry, args.ledger)
    print(f"Recorded outcome for {args.decision_id}: actual_delta={args.actual_delta}")
    return 0


def cmd_calibrate(args) -> int:
    decisions: dict[str, dict] = {}
    outcomes: dict[str, float] = {}
    try:
        with open(args.ledger, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("type") == "outcome":
                    outcomes[rec["decision_id"]] = rec["actual_delta"]
                elif rec.get("status") == "decided":
                    decisions[rec["decision_id"]] = rec
    except FileNotFoundError:
        print("No ledger yet — no decisions recorded. Nothing to calibrate.")
        return 0

    records = []
    for did, d in decisions.items():
        if did not in outcomes:
            continue
        pred = None
        for r in d.get("ranking", []):
            if r["id"] == d.get("winner"):
                pred = r["v_safe"]
        if pred is None:
            continue
        records.append({"delta_v_predicted": pred, "delta_v_actual": outcomes[did]})

    s = calibration_summary(records)
    print(f"Decisions with outcomes: {s['n']}")
    print(f"Mean absolute error: {s['mean_absolute_error']:.2f}")
    print(f"Bias (signed): {s['mean_signed_error']:.2f} "
          f"({'overpredicting' if s['overprediction_detected'] else 'no overprediction pattern'})")
    if s["n"] == 0:
        print("Record outcomes with the 'outcome' command and I'll track my own accuracy.")
    elif s["mean_absolute_error"] < 1.0:
        print("Calibration is tight — predictions are landing close to reality.")
    else:
        print("Calibration needs work — my value estimates are drifting from outcomes.")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _load_input(args) -> dict:
    if args.input:
        with open(args.input, encoding="utf-8") as f:
            return json.load(f)
    data = sys.stdin.read()
    if not data.strip():
        raise ValueError("No input: pass --input FILE or pipe JSON on stdin.")
    return json.loads(data)


def _print_result(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, indent=2, default=str))
        return
    if result.get("status") == "needs_clarification":
        print("I need a little more before I can decide honestly:\n")
        for q in result["questions"]:
            print(f"  • {q}")
        return
    print(f"Decision: {result['decision_id']}")
    print(f"Question: {result['question']}")
    print(f"Engine says: {result['engine_decision']}" +
          (f" → winner: {result['winner']}" if result.get("winner") else ""))
    print(f"Thought spent: {result['wisdom']['tier']} "
          f"({result['wisdom']['thought_seconds']}s) — {result['wisdom']['why']}")
    print()
    print(result["explanation"])
    if result.get("assumptions"):
        print("\nAssumptions I made (tell me if any are wrong):")
        for a in result["assumptions"]:
            print(f"  • {a}")
    if result.get("dry_run"):
        print("\n[dry run — nothing was recorded]")


def cmd_decide(args) -> int:
    if args.example:
        print(EXAMPLE_JSON)
        return 0
    try:
        payload = _load_input(args)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"Input error: {e}")
        print("Expected JSON like: {\"question\": \"...\", \"options\": [{\"id\": \"a\", \"value_estimate\": 7, \"evidence\": [\"...\"]}]}")
        return 2
    result = decide_payload(payload, dry_run=args.dry_run)
    if result.get("status") == "needs_clarification":
        _print_result(result, args.json)
        return 2
    if not args.dry_run and not args.no_record:
        ledger_append({**result, "type": "decision"}, args.ledger)
    _print_result(result, args.json)
    return 0


def cmd_batch(args) -> int:
    try:
        payload = _load_input(args)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"Input error: {e}")
        return 2
    decisions = payload.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        print("Batch input needs a 'decisions' list, each shaped like a single decide input.")
        return 2
    results = []
    for i, d in enumerate(decisions):
        r = decide_payload(d, dry_run=args.dry_run)
        r["batch_index"] = i
        results.append(r)
        if r.get("status") == "decided" and not args.dry_run and not args.no_record:
            ledger_append({**r, "type": "decision"}, args.ledger)
    out = {"status": "batch_complete", "count": len(results), "results": results,
           "dry_run": args.dry_run}
    if args.json:
        print(json.dumps(out, indent=2, default=str))
    else:
        for r in results:
            tag = f"[dry run] " if args.dry_run else ""
            if r.get("status") == "needs_clarification":
                print(f"{tag}#{r['batch_index']}: needs clarification — {r['questions'][0]}")
            else:
                print(f"{tag}#{r['batch_index']}: {r['engine_decision']}" +
                      (f" → {r['winner']}" if r.get("winner") else "") +
                      f" | {r['explanation'][:160]}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="decision_calculator.py",
        description="One command in, the most intelligent decision out. "
                    "Hard gates first, then value scoring, explained in plain words. "
                    "Scores never create authority.")
    sub = p.add_subparsers(dest="command", required=True)

    d = sub.add_parser("decide", help="Score one decision (JSON via --input or stdin).")
    d.add_argument("--input", help="JSON file (default: stdin).")
    d.add_argument("--json", action="store_true", help="Output the full receipt as JSON.")
    d.add_argument("--example", action="store_true",
                   help="Print an example input JSON and exit.")
    d.add_argument("--dry-run", action="store_true",
                   help="Show what would be decided — record nothing.")
    d.add_argument("--no-record", action="store_true",
                   help="Decide but don't append to the learning ledger.")
    d.add_argument("--ledger", default=DEFAULT_LEDGER, help="Learning ledger path.")
    d.set_defaults(func=cmd_decide)

    b = sub.add_parser("batch", help="Score several decisions in one call.")
    b.add_argument("--input", help="JSON file with a 'decisions' list (default: stdin).")
    b.add_argument("--json", action="store_true")
    b.add_argument("--dry-run", action="store_true")
    b.add_argument("--no-record", action="store_true")
    b.add_argument("--ledger", default=DEFAULT_LEDGER)
    b.set_defaults(func=cmd_batch)

    o = sub.add_parser("outcome", help="Record what actually happened (learning loop).")
    o.add_argument("--decision-id", required=True)
    o.add_argument("--actual-delta", required=True, type=float,
                   help="Observed value delta vs doing nothing.")
    o.add_argument("--note", default="")
    o.add_argument("--ledger", default=DEFAULT_LEDGER)
    o.set_defaults(func=cmd_outcome)

    c = sub.add_parser("calibrate", help="Report the calculator's own accuracy.")
    c.add_argument("--ledger", default=DEFAULT_LEDGER)
    c.set_defaults(func=cmd_calibrate)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
