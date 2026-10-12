#!/usr/bin/env python3
"""
Decision Output — Layer 5 of the Ultimate Decision Machine.

MATH → PLAIN WORDS. Takes Layer 4's ranked, scored options and speaks like
a trusted advisor. Shawn's laws, as code:

  - Gates first: if REQUIRES_SHAWN is present, the FIRST sentence is
    "This needs Shawn's word: <reason>." Never buried.
  - "I don't know yet" is a complete, honorable answer. Never manufacture
    confidence.
  - Confidence is shown ALWAYS, rounded to whole percent (82%, not 81.73%).
  - The "why" cites evidence, never bare scores ("because X", not
    "because 0.87").
  - Never recommend an option whose total_confidence is below 0.5 —
    instead ask for the missing evidence.
  - Zero network calls. Local reasoning only.

Three modes:
  HUMAN (default): plain words. Recommendation first, why in one or two
    sentences citing real evidence, honest caveat with confidence, then
    what it beats and by how much.
  WORKER: full structured JSON — recommendation, ranked options with
    scores/confidences/evidence, gates, uncertainties, questions. Auditable.
  QUESTIONS: clarifying questions instead of a recommendation — never a
    guess dressed as an answer.

Input contract: Layer 4's score_options() result dict. Parsed DEFENSIVELY —
Layer 4's independent validation was still in flight when this was written,
so missing keys degrade to honest UNKNOWN, never KeyError.

Usage:
  python3 tools/decision_output.py decide --scored '<json>' [--mode human|worker|questions] [--plain]
  python3 tools/decision_output.py decide --stdin < scored.json

Exit codes:
  0 — a verdict was rendered (recommendation or honest "too close to call")
  2 — clarifying questions / "I don't know yet" (no recommendation made)
  3 — REQUIRES_SHAWN: a hard gate is present; the gate is the message
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DIMENSION_LABELS = {
    "mission_value": "mission value",
    "evidence": "proof",
    "risk": "risk",
    "cost": "cost",
    "urgency": "urgency",
}

DIMENSION_ORDER = ["mission_value", "evidence", "risk", "cost", "urgency"]

# Action verbs per Layer 2 intent type — so "Do X" reads like advice.
INTENT_VERBS = {
    "should_merge": "Merge",
    "should_build": "Build",
    "what_next": "Do next",
    "which_option": "Choose",
    "what_blocking": "Unblock first",
    "status_check": None,
}

CONFIDENCE_FLOOR = 0.5   # never recommend below this
CLOSE_CALL_MARGIN = 0.05  # below this, it's honestly "too close to call"

# Per-dimension questions for the missing-evidence case. The machine asks
# for the evidence it lacks instead of guessing.
DIMENSION_QUESTIONS = {
    "mission_value": "Does this actually close a real gap? Which gap, exactly?",
    "evidence": "What proof exists — green tests, an independent validation score, or CI?",
    "risk": "Is it reversible? Does it touch anything protected (production, credentials, money)?",
    "cost": "What is the real cost — measured, not guessed?",
    "urgency": "What does it block, and what blocks it?",
}

NEGATIVE_MARKERS = (
    "not mergeable", "not proven", "no test evidence", "no cost evidence",
    "red", "blocked", "draft", "unknown", "cannot be verified", "zero mechanical",
)


# ---------------------------------------------------------------------------
# Defensive input parsing — Layer 4's schema may drift. Never KeyError.
# ---------------------------------------------------------------------------

def _as_dict(v):
    return v if isinstance(v, dict) else {}


def _as_list(v):
    return v if isinstance(v, list) else []


def _as_num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _as_str(v, default=""):
    return v if isinstance(v, str) else default


def normalize_dim(d):
    """One scored dimension, defensively normalized. Missing → UNKNOWN."""
    d = _as_dict(d)
    ev = _as_list(d.get("evidence"))
    return {
        "value": _as_num(d.get("value")),
        "evidence": [_as_str(e) for e in ev],
        "confidence": _as_num(d.get("confidence")) or 0.0,
    }


def normalize_option(o, position):
    """One scored option, defensively normalized. Never throws."""
    o = _as_dict(o)
    dims = _as_dict(o.get("dimensions"))
    norm_dims = {k: normalize_dim(dims.get(k)) for k in DIMENSION_ORDER}
    # Tolerate extra dimensions Layer 4 might add later.
    for k, v in dims.items():
        if k not in norm_dims:
            norm_dims[k] = normalize_dim(v)
    gated = bool(o.get("gated", False))
    verdict = _as_str(o.get("gate_verdict"), "")
    if verdict == "REQUIRES_SHAWN":
        gated = True
    return {
        "id": o.get("id"),
        "title": _as_str(o.get("title")) or "unnamed option",
        "source": _as_str(o.get("source")),
        "source_type": _as_str(o.get("source_type")),
        "gated": gated,
        "gate_verdict": "REQUIRES_SHAWN" if gated else "clear",
        "gate_reasons": [_as_str(r) for r in _as_list(o.get("gate_reasons"))],
        "dimensions": norm_dims,
        "total": _as_num(o.get("total")),
        "total_confidence": _as_num(o.get("total_confidence")) or 0.0,
        "unknown_dimensions": [_as_str(u) for u in _as_list(o.get("unknown_dimensions"))],
        "rank": o.get("rank") if isinstance(o.get("rank"), int) else None,
        "_position": position,
    }


def normalize_scored(scored):
    """Normalize Layer 4's full result. Returns (norm, warnings)."""
    warnings = []
    if not isinstance(scored, dict):
        return None, ["input is not a JSON object — cannot decide"]
    if "ok" not in scored:
        warnings.append("schema drift: 'ok' missing from Layer 4 output — assumed true")
    if "options" not in scored:
        warnings.append("schema drift: 'options' missing from Layer 4 output")
    raw_options = _as_list(scored.get("options"))
    options = [normalize_option(o, i) for i, o in enumerate(raw_options)]
    return {
        "ok": bool(scored.get("ok", True)),
        "exit_hint": scored.get("exit_hint", 0),
        "intent_type": _as_str(scored.get("intent_type")),
        "objective": _as_str(scored.get("objective")),
        "options": options,
        "recommendation": _as_dict(scored.get("recommendation")) or None,
        "notes": [_as_str(n) for n in _as_list(scored.get("notes"))],
        "warnings": [_as_str(w) for w in _as_list(scored.get("warnings"))],
    }, warnings


# ---------------------------------------------------------------------------
# Decision core — mode-independent. Returns (verdict, exit_code).
# ---------------------------------------------------------------------------

def rankable_options(options):
    """Options the machine is allowed to recommend: not gated, total known."""
    ranked = [o for o in options
              if not o["gated"] and o["total"] is not None]
    ranked.sort(key=lambda o: (
        o["rank"] is None,
        o["rank"] if o["rank"] is not None else 0,
        -(o["total"] or 0),
        -(o["total_confidence"] or 0),
    ))
    return ranked


def weakest_dimension(option):
    """The dimension dragging confidence down — for the honest caveat."""
    dims = option["dimensions"]
    known = [(k, d) for k, d in dims.items()
             if d["value"] is not None and k in DIMENSION_LABELS]
    if not known:
        return None, None
    return min(known, key=lambda kv: kv[1]["confidence"])


def driving_dimension(best, runner):
    """Which dimension separates winner from runner-up, and by how much."""
    best_gap, best_k = 0.0, None
    for k in DIMENSION_ORDER:
        bv = best["dimensions"].get(k, {}).get("value")
        rv = runner["dimensions"].get(k, {}).get("value")
        if bv is None or rv is None:
            continue
        gap = bv - rv
        if gap > best_gap:
            best_gap, best_k = gap, k
    return best_k, best_gap


def decide(norm):
    """The decision. Returns (verdict_dict, exit_code).

    verdict_dict keys: verdict, best, runner_up, gated, questions,
    notes, sub_verdict (for the gated branch's non-gated section).
    Mode renderers only translate — they never re-decide.
    """
    base = {
        "verdict": None, "best": None, "runner_up": None,
        "gated": [], "questions": [], "notes": [], "sub_verdict": None,
    }

    if norm is None:
        base.update(verdict="cannot_decide",
                    notes=["Layer 4's output was not usable — refusing to guess."])
        return base, 2

    if not norm["ok"] or norm.get("exit_hint") == 2:
        base.update(verdict="cannot_decide")
        base["notes"].extend(norm["notes"] or
                             ["Layer 4 could not score — nothing to decide from."])
        base["questions"].extend(questions_for_unscored(norm))
        return base, 2

    options = norm["options"]
    gated = [o for o in options if o["gated"]]
    base["gated"] = gated

    ranked = rankable_options(options)
    base["best"] = ranked[0] if ranked else None
    base["runner_up"] = ranked[1] if len(ranked) > 1 else None

    if gated:
        # GATES ARE WALLS. Exit 3. The gate is the first and loudest thing.
        # The non-gated section gets the same honesty as the main path.
        base.update(verdict="gated")
        sub, questions = ranked_outcome(ranked)
        base["sub_verdict"] = sub
        base["questions"] = questions
        cross_check_recommendation(norm, base)
        return base, 3

    sub, questions = ranked_outcome(ranked)
    if sub == "needs_evidence":
        base.update(verdict="needs_evidence")
        if not ranked:
            base["notes"].append(
                "No rankable option: every option is gated or its total is "
                "UNKNOWN. The machine refuses to recommend — refreshing the "
                "world model or re-running the scorer may unblock it.")
            base["questions"].extend(questions_for_unranked(norm))
        else:
            base["questions"].extend(questions)
        return base, 2

    if sub == "too_close_to_call":
        base.update(verdict="too_close_to_call")
        base["questions"].extend(questions)
        cross_check_recommendation(norm, base)
        return base, 0

    base.update(verdict="recommend")
    cross_check_recommendation(norm, base)
    return base, 0


def ranked_outcome(ranked):
    """Honest outcome for a rankable list.

    Returns (outcome, questions) where outcome is one of
    "recommend", "too_close_to_call", "needs_evidence".
    """
    if not ranked:
        return "needs_evidence", []
    best = ranked[0]
    if best["total_confidence"] < CONFIDENCE_FLOOR:
        return "needs_evidence", questions_for_low_confidence(best)
    if len(ranked) > 1 and (best["total"] - ranked[1]["total"]) < CLOSE_CALL_MARGIN:
        return "too_close_to_call", questions_for_close_call(best, ranked[1])
    return "recommend", []


def cross_check_recommendation(norm, base):
    """If Layer 4 named a recommendation that disagrees with the option data,
    say so — schema drift is a fact, not a suspicion to hide."""
    rec = (norm.get("recommendation") or {}) if norm else {}
    rec_id = rec.get("option_id")
    best = base.get("best")
    if rec_id is not None and best is not None and rec_id != best["id"]:
        base["notes"].append(
            f"Layer 4 named '{rec.get('title', rec_id)}' but the option data "
            f"ranks '{best['title']}' first — possible schema drift; "
            "trusting the option data.")


# ---------------------------------------------------------------------------
# Question generation — ask for the missing evidence, never guess it.
# ---------------------------------------------------------------------------

def questions_for_unscored(norm):
    qs = []
    for n in norm.get("notes", []):
        qs.append(n)
    if not qs:
        qs.append("What should I decide between? I need options with evidence.")
    return qs


def questions_for_unranked(norm):
    qs = []
    unknowns = set()
    for o in norm.get("options", []):
        unknowns.update(o.get("unknown_dimensions", []))
    for u in sorted(unknowns):
        label = DIMENSION_LABELS.get(u, u)
        qs.append(f"For the {label} dimension: "
                  f"{DIMENSION_QUESTIONS.get(u, 'What evidence is missing?')}")
    if norm.get("warnings"):
        qs.append("The world-model cache may be stale — refresh it and re-run "
                  "the scorer, then ask me again.")
    if not qs:
        qs.append("Every option came back UNKNOWN or gated — what changed since "
                  "the world model was last refreshed?")
    return qs


def questions_for_low_confidence(best):
    title = best["title"]
    qs = []
    for u in best.get("unknown_dimensions", []):
        label = DIMENSION_LABELS.get(u, u)
        qs.append(f"For '{title}': {label} is UNKNOWN — "
                  f"{DIMENSION_QUESTIONS.get(u, 'What evidence is missing?')}")
    for k in DIMENSION_ORDER:
        d = best["dimensions"].get(k, {})
        if d.get("value") is not None and d.get("confidence", 0) < 0.5:
            label = DIMENSION_LABELS.get(k, k)
            qs.append(f"For '{title}': {label} confidence is only "
                      f"{pct(d['confidence'])} — "
                      f"{DIMENSION_QUESTIONS.get(k, 'What evidence is missing?')}")
    if not qs:
        qs.append(f"For '{title}': overall confidence is below the floor — "
                  "what evidence would raise it?")
    return qs


def questions_for_close_call(best, runner):
    qs = []
    for opt in (best, runner):
        for u in opt.get("unknown_dimensions", []):
            label = DIMENSION_LABELS.get(u, u)
            qs.append(f"'{opt['title']}' has UNKNOWN {label} — settling that "
                      "could decide it.")
    for k in DIMENSION_ORDER:
        b = best["dimensions"].get(k, {})
        r = runner["dimensions"].get(k, {})
        if (b.get("value") is None) != (r.get("value") is None):
            known_side = best["title"] if b.get("value") is not None else runner["title"]
            label = DIMENSION_LABELS.get(k, k)
            qs.append(f"Only '{known_side}' has a {label} score — scoring the "
                      f"other side's {label} would decide it.")
    if not qs:
        qs.append("Both options are well-evidenced and nearly tied — "
                  "a fresh independent validation of either would break the tie.")
    return qs


# ---------------------------------------------------------------------------
# Human rendering — plain words, evidence cited, confidence always shown.
# ---------------------------------------------------------------------------

def pct(conf):
    """Whole-percent, honest. 0.82 → '82%'. Never 81.73%."""
    try:
        return f"{int(round(float(conf) * 100))}%"
    except (TypeError, ValueError):
        return "unknown"


def humanize_evidence(text):
    """Strip machine-only annotations for human ears."""
    t = re.sub(r"\s*\(mechanical\)", "", text or "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def _evidence_priority(text):
    t = (text or "").lower()
    if "independent validation" in t and ">=" in t:
        return 5
    if "tests reported green" in t or "can land and close" in t:
        return 4
    if "closes a known gap" in t or "open todo item" in t:
        return 4
    if "not a draft" in t or ("mergeable" in t and "unknown" not in t):
        return 3
    if any(m in t for m in NEGATIVE_MARKERS):
        return 0
    return 1


def why_sentences(option, max_sentences=2):
    """The 'why' — top evidence fragments, humanized. Never bare numbers."""
    scored = []
    for k in DIMENSION_ORDER:
        d = option["dimensions"].get(k, {})
        for e in d.get("evidence", []):
            e = humanize_evidence(e)
            if e:
                scored.append((_evidence_priority(e), e))
    scored.sort(key=lambda p: -p[0])
    picked = []
    seen = set()
    for _, e in scored:
        key = e.lower()[:40]
        if key not in seen:
            seen.add(key)
            picked.append(e)
        if len(picked) >= max_sentences:
            break
    if not picked:
        return "the evidence on file supports it, though no single fact stands out."
    s = "; ".join(picked)
    return s[0].upper() + s[1:] if s else s


def caveat_sentence(option):
    """The honest caveat — weakest link, in plain words.

    An UNKNOWN dimension caps the honesty of any confidence number:
    the machine says what's provisional instead of sounding certain.
    """
    unknowns = [DIMENSION_LABELS.get(u, u)
                for u in option.get("unknown_dimensions", [])]
    if unknowns:
        return (f"I couldn't verify {', '.join(unknowns)} — treat this as "
                f"provisional. {pct(option['total_confidence'])} confident "
                "in the rest.")
    k, d = weakest_dimension(option)
    if k is None:
        return f"I'm {pct(option['total_confidence'])} confident."
    label = DIMENSION_LABELS.get(k, k)
    ev = d.get("evidence", [])
    detail = humanize_evidence(ev[0]) if ev else "thin evidence"
    return (f"I'm {pct(option['total_confidence'])} confident — "
            f"the weakest part is {label}: {detail}.")


# Gate reasons arrive from Layer 4 in machine dialect
# ("protected gate pattern '<regex>' in action: <text>"). Humans get the
# plain-English version; WORKER mode keeps the raw reason for audit.
GATE_LABELS = [
    ("production deploy", ("deploy", "production")),
    ("database write", ("database write", "db write")),
    ("credentials", ("credential",)),
    ("money", ("money", "payment")),
    ("destructive action", ("destruct", "delete", "force push", "forcepush")),
    ("constitutional change", ("constitution", "ratif")),
]


def humanize_gate_reason(reason):
    r = _as_str(reason)
    m = re.search(r"in action:\s*(.+)$", r)
    action = m.group(1).strip() if m else r
    label = "protected action"
    low = r.lower()
    for lab, keys in GATE_LABELS:
        if any(k in low for k in keys):
            label = lab
            break
    if m and action:
        return f"'{action}' is a {label}"
    return f"{r} ({label})" if r else label


def recommendation_line(intent_type, title):
    verb = INTENT_VERBS.get(intent_type)
    if verb and not title.lower().startswith(verb.lower()):
        return f"{verb}: {title}."
    return f"{title}."


def margin_line(best, runner):
    """What it beats and by how much — in plain points, never bare scores."""
    margin = int(round((best["total"] - runner["total"]) * 100))
    k, _ = driving_dimension(best, runner)
    if k:
        return (f"Beats '{runner['title']}' by {margin} points — "
                f"the difference is {DIMENSION_LABELS[k]}.")
    return f"Beats '{runner['title']}' by {margin} points overall."


def close_call_text(best, runner):
    margin = int(round((best["total"] - runner["total"]) * 100))
    return (f"Too close to call between '{best['title']}' and "
            f"'{runner['title']}' — {margin} points apart.")


def render_human(norm, verdict):
    v = verdict["verdict"]
    lines = []

    if v == "gated":
        reasons = []
        for g in verdict["gated"]:
            hr = "; ".join(humanize_gate_reason(r)
                           for r in g["gate_reasons"]) or "protected action"
            reasons.append(f"{hr}")
        lead = "; ".join(humanize_gate_reason(r)
                         for g in verdict["gated"]
                         for r in g["gate_reasons"]) or "a protected action"
        lines.append(f"This needs Shawn's word: {lead}.")
        lines.append("")
        lines.append("Gated " + ("option" if len(reasons) == 1 else "options")
                     + ": " + "; ".join(reasons) + ".")
        lines.append("Gates are walls, not scores — these are not ranked.")
        best = verdict.get("best")
        if best is not None:
            lines.append("")
            lines.append("For the rest (nothing gated there):")
            sub = verdict.get("sub_verdict")
            if sub == "recommend":
                lines.append(recommendation_line(norm["intent_type"], best["title"]))
                lines.append(caveat_sentence(best))
                runner = verdict.get("runner_up")
                if runner is not None:
                    lines.append(margin_line(best, runner))
            elif sub == "too_close_to_call":
                runner = verdict.get("runner_up")
                lines.append(close_call_text(best, runner))
                lines.append("")
                lines.append("What would decide it:")
                for q in verdict["questions"]:
                    lines.append(f"- {q}")
            else:
                lines.append("I don't have enough evidence on these either.")
                for q in verdict["questions"]:
                    lines.append(f"- {q}")
        return "\n".join(lines)

    if v == "cannot_decide":
        lines.append("I don't know yet.")
        for n in verdict["notes"]:
            lines.append(n)
        if verdict["questions"]:
            lines.append("")
            lines.append("What I'd need:")
            for q in verdict["questions"]:
                lines.append(f"- {q}")
        return "\n".join(lines)

    if v == "needs_evidence":
        best = verdict.get("best")
        subject = f" '{best['title']}'" if best else ""
        lines.append(f"I don't have enough evidence to recommend{subject} yet.")
        if best:
            lines.append(caveat_sentence(best))
        lines.append("")
        lines.append("To decide, I'd need:")
        for q in verdict["questions"]:
            lines.append(f"- {q}")
        return "\n".join(lines)

    if v == "too_close_to_call":
        best, runner = verdict["best"], verdict["runner_up"]
        lines.append(close_call_text(best, runner))
        lines.append("")
        lines.append("What would decide it:")
        for q in verdict["questions"]:
            lines.append(f"- {q}")
        return "\n".join(lines)

    # v == "recommend"
    best = verdict["best"]
    lines.append(recommendation_line(norm["intent_type"], best["title"]))
    lines.append("")
    lines.append(f"Why: {why_sentences(best)}.")
    lines.append("")
    lines.append(caveat_sentence(best))
    runner = verdict.get("runner_up")
    if runner is not None:
        lines.append(margin_line(best, runner))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Worker rendering — full structured JSON, auditable.
# ---------------------------------------------------------------------------

def render_worker(norm, verdict, exit_code, warnings):
    def opt_json(o):
        return {
            "id": o["id"], "title": o["title"], "source": o["source"],
            "source_type": o["source_type"], "gated": o["gated"],
            "gate_verdict": o["gate_verdict"], "gate_reasons": o["gate_reasons"],
            "dimensions": o["dimensions"], "total": o["total"],
            "total_confidence": o["total_confidence"],
            "unknown_dimensions": o["unknown_dimensions"], "rank": o["rank"],
        }

    best = verdict.get("best")
    runner = verdict.get("runner_up")
    margin = None
    dk = None
    if best is not None and runner is not None:
        margin = round(best["total"] - runner["total"], 3)
        dk, _ = driving_dimension(best, runner)

    uncertainties = []
    for o in norm["options"]:
        for u in o.get("unknown_dimensions", []):
            uncertainties.append({"option": o["title"], "dimension": u,
                                  "status": "UNKNOWN"})
        for k in DIMENSION_ORDER:
            d = o["dimensions"].get(k, {})
            if d.get("value") is not None and d.get("confidence", 0) < 0.5:
                uncertainties.append({"option": o["title"], "dimension": k,
                                      "status": "low_confidence",
                                      "confidence": d["confidence"]})

    return {
        "verdict": verdict["verdict"],
        "exit_hint": exit_code,
        "intent_type": norm["intent_type"],
        "objective": norm["objective"],
        "recommendation": opt_json(best) if best else None,
        "ranked_options": [opt_json(o) for o in rankable_options(norm["options"])],
        "runner_up_margin": margin,
        "driving_dimension": dk,
        "gates": [
            {"title": g["title"], "reasons": g["gate_reasons"]}
            for g in verdict["gated"]
        ],
        "uncertainties": uncertainties,
        "questions": verdict["questions"],
        "notes": verdict["notes"] + norm["notes"],
        "warnings": warnings + norm["warnings"],
        "decided_utc": datetime.now(timezone.utc).isoformat(),
    }


def render_questions(verdict):
    qs = list(verdict["questions"])
    if verdict["verdict"] in ("recommend", "too_close_to_call"):
        qs.append("No clarifying questions — the evidence supports a verdict. "
                  "Re-run with --mode human for the recommendation.")
    if not qs:
        qs.append("Nothing to ask — the decision inputs are complete.")
    return "\n".join(f"- {q}" for q in qs)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def run(scored_input, mode):
    """Decide and render. Returns (text, exit_code)."""
    norm, warnings = normalize_scored(scored_input)
    verdict, exit_code = decide(norm)
    if mode == "worker":
        payload = render_worker(norm or {"intent_type": "", "objective": "",
                                         "options": [], "notes": [],
                                         "warnings": []},
                                verdict, exit_code, warnings)
        return json.dumps(payload, indent=2), exit_code
    if mode == "questions":
        return render_questions(verdict), 2 if exit_code != 3 else 3
    return render_human(norm or {}, verdict), exit_code


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="decision_output.py",
        description="Layer 5: math → plain words. "
                    "Takes Layer 4's scored options, speaks like a trusted advisor.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("decide", help="render a decision from Layer 4 JSON")
    d.add_argument("--scored", help="Layer 4 result JSON string")
    d.add_argument("--stdin", action="store_true",
                   help="read Layer 4 result JSON from stdin")
    d.add_argument("--mode", choices=["human", "worker", "questions"],
                   default="human")
    d.add_argument("--plain", action="store_true",
                   help="explicit plain-text human output (no formatting codes)")

    args = ap.parse_args(argv)

    if args.cmd == "decide":
        if args.stdin:
            raw = sys.stdin.read()
        elif args.scored:
            raw = args.scored
        else:
            print("usage: decision_output.py decide --scored '<json>' | --stdin",
                  file=sys.stderr)
            return 2
        try:
            scored_input = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"couldn't read the scored input as JSON: {e}\n"
                  "I don't know yet — give me valid Layer 4 output.",
                  file=sys.stderr)
        else:
            text, code = run(scored_input, args.mode)
            print(text)
            return code
        return 2


if __name__ == "__main__":
    sys.exit(main())
