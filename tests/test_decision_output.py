#!/usr/bin/env python3
"""Tests for Layer 5 — decision_output.py (math → plain words)."""

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import decision_output as d


# ---------------------------------------------------------------------------
# Fixture builders — Layer-4-shaped payloads
# ---------------------------------------------------------------------------

def dim(value, evidence, confidence):
    return {"value": value, "evidence": list(evidence), "confidence": confidence}


def opt(title, total, conf, oid="o1", source_type="pr", gated=False,
        unknowns=(), dim_conf_overrides=None, rank=1, extra_dims=None):
    dims = {
        "mission_value": dim(0.85, ["PR #2410 mergeable, non-draft — can land and close its gap",
                                    "option text indicates it closes a known gap/RED"], 0.9),
        "evidence": dim(0.9, ["independent validation 9.5 >= 9.5 (mechanical)",
                               "tests reported green on the option",
                               "not a draft"], 0.9),
        "risk": dim(0.2, ["no protected-gate patterns matched"], 0.8),
        "cost": dim(0.3, ["files_changed=3 — small blast radius"], 0.7),
        "urgency": dim(0.6, ["unblocks 2 other PRs in the queue"], 0.8),
    }
    if dim_conf_overrides:
        for k, c in dim_conf_overrides.items():
            dims[k] = dim(dims[k]["value"], dims[k]["evidence"], c)
    if extra_dims:
        dims.update(extra_dims)
    for u in unknowns:
        dims[u] = dim(None, [f"{u} could not be verified"], 0.3)
    return {
        "id": oid, "title": title, "source": "pr:2410",
        "source_type": source_type, "gated": gated,
        "gate_verdict": "REQUIRES_SHAWN" if gated else "clear",
        "gate_reasons": ["touches production deploy path"] if gated else [],
        "dimensions": dims, "total": total, "total_confidence": conf,
        "unknown_dimensions": list(unknowns), "rank": rank,
    }


def scored(options, intent_type="should_merge", ok=True, exit_hint=0,
           notes=None, recommendation=None, objective="merge the right PR first"):
    return {
        "ok": ok, "exit_hint": exit_hint, "intent_type": intent_type,
        "objective": objective, "options": options,
        "recommendation": recommendation, "notes": notes or [],
        "warnings": [], "scored_utc": "2026-10-12T04:00:00+00:00",
    }


def run_cli(payload, *args):
    p = subprocess.run(
        [sys.executable,
         os.path.join(os.path.dirname(__file__), "..", "tools", "decision_output.py"),
         "decide", "--stdin", *args],
        input=json.dumps(payload), capture_output=True, text=True)
    return p


# ---------------------------------------------------------------------------
# 1. Clear winner — golden output
# ---------------------------------------------------------------------------

def test_clear_winner_human():
    s = scored([
        opt("Merge PR #2410 (consolidation)", 0.82, 0.85, oid="p1", rank=1),
        opt("Merge PR #2420 (dep guard)", 0.61, 0.8, oid="p2", rank=2),
    ])
    text, code = d.run(s, "human")
    assert code == 0, text
    assert text.startswith("Merge PR #2410 (consolidation)."), text
    # confidence always shown, whole percent
    assert "85%" in text, text
    assert "81.73%" not in text
    # why cites evidence text, not bare scores
    assert "independent validation 9.5" in text.lower() or "tests reported green" in text.lower(), text
    # margin line present
    assert "Beats" in text and "points" in text, text
    # no bare decimals in the Why line (scores never cited alone)
    why = [l for l in text.splitlines() if l.startswith("Why:")][0]
    assert not re.search(r"\b0\.\d+", why), f"bare score in why: {why}"


def test_clear_winner_intent_verb():
    s = scored([opt("Build the learning loop", 0.8, 0.9, rank=1)],
               intent_type="should_build")
    text, code = d.run(s, "human")
    assert code == 0
    assert text.startswith("Build the learning loop."), text


def test_recommendation_line_dedupes_verb():
    # title already starts with the intent verb → no stutter
    assert d.recommendation_line("should_merge", "Merge PR #2410") == "Merge PR #2410."
    # title without the verb → verb prefixed as advice
    assert d.recommendation_line("should_merge", "Consolidation work") == "Merge: Consolidation work."
    # no verb for this intent → bare title
    assert d.recommendation_line("status_check", "Queue status") == "Queue status."


def test_single_option_no_beats_line():
    s = scored([opt("Only option", 0.8, 0.9, rank=1)])
    text, code = d.run(s, "human")
    assert code == 0
    assert "Beats" not in text, text


# ---------------------------------------------------------------------------
# 2. Close call — margin < 5 points → too close to call
# ---------------------------------------------------------------------------

def test_close_call():
    s = scored([
        opt("Merge PR #2410", 0.78, 0.85, oid="p1", rank=1),
        opt("Merge PR #2420", 0.75, 0.8, oid="p2", rank=2),
    ])
    text, code = d.run(s, "human")
    assert code == 0, text
    assert "Too close to call" in text, text
    assert "Merge PR #2410" in text and "Merge PR #2420" in text, text
    assert "What would decide it:" in text, text


def test_close_call_boundary():
    # exactly 0.05 margin → NOT a close call (>= threshold recommends)
    s = scored([
        opt("A", 0.80, 0.85, oid="p1", rank=1),
        opt("B", 0.75, 0.8, oid="p2", rank=2),
    ])
    _, code = d.run(s, "human")
    assert code == 0
    text, _ = d.run(s, "human")
    assert "Too close to call" not in text, text


# ---------------------------------------------------------------------------
# 3. Gated — REQUIRES_SHAWN is the FIRST sentence, exit 3
# ---------------------------------------------------------------------------

def test_gated_leads_with_gate():
    s = scored([
        opt("Deploy to production", 0.9, 0.9, oid="g1", gated=True, rank=None),
        opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1),
    ])
    text, code = d.run(s, "human")
    assert code == 3, text
    first = text.splitlines()[0]
    assert first.startswith("This needs Shawn's word:"), first
    assert "production" in first.lower(), first
    # gated option never recommended
    assert "Merge: Deploy to production" not in text
    # non-gated section still useful, clearly separated
    assert "nothing gated there" in text, text


def test_gated_only():
    s = scored([opt("Deploy to production", 0.9, 0.9, oid="g1", gated=True, rank=None)])
    text, code = d.run(s, "human")
    assert code == 3, text
    assert text.startswith("This needs Shawn's word:"), text
    assert "Gates are walls, not scores" in text, text


def test_gated_humanizes_machine_reason():
    s = scored([opt("Deploy to production", 0.9, 0.9, oid="g1", gated=True, rank=None)])
    s["options"][0]["gate_reasons"] = [
        "protected gate pattern '\\\\bdeploy\\\\b.{0,20}\\\\bproduction\\\\b' "
        "in action: Deploy to production"]
    text, code = d.run(s, "human")
    assert code == 3, text
    assert "production deploy" in text.lower(), text
    assert "\\bdeploy" not in text, f"raw regex leaked: {text}"
    assert "Deploy to production" in text, text


def test_caveat_provisional_on_unknown():
    o = opt("Merge PR #2410", 0.82, 0.95, oid="p1", rank=1, unknowns=("cost",))
    s = scored([o])
    text, code = d.run(s, "human")
    assert code == 0, text
    assert "provisional" in text, text
    assert "couldn't verify cost" in text, text
    # no false certainty: never "I'm 95% confident" as a bare claim here
    assert "I'm 95% confident —" not in text, text


def test_gated_close_call_in_non_gated_section():
    s = scored([
        opt("A", 0.78, 0.85, oid="p1", rank=1),
        opt("B", 0.75, 0.8, oid="p2", rank=2),
        opt("Deploy X", 0.9, 0.9, oid="g1", gated=True, rank=None),
    ])
    text, code = d.run(s, "human")
    assert code == 3, text
    assert text.startswith("This needs Shawn's word:"), text
    assert "Too close to call between 'A' and 'B'" in text, text


# ---------------------------------------------------------------------------
# 4. Low confidence — never recommend below 0.5, ask instead (exit 2)
# ---------------------------------------------------------------------------

def test_low_confidence_asks():
    s = scored([opt("Merge PR #2410", 0.82, 0.42, oid="p1", rank=1)])
    text, code = d.run(s, "human")
    assert code == 2, text
    assert "don't have enough evidence" in text, text
    assert "To decide, I'd need:" in text, text
    assert not text.startswith("Merge:"), text


def test_unknown_dimensions_ask():
    s = scored([opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1,
                    unknowns=("cost",),
                    dim_conf_overrides={"mission_value": 0.4,
                                        "evidence": 0.4, "risk": 0.4,
                                        "urgency": 0.4})])
    # force below floor via total_confidence
    s["options"][0]["total_confidence"] = 0.4
    text, code = d.run(s, "human")
    assert code == 2, text
    assert "cost" in text.lower(), text


# ---------------------------------------------------------------------------
# 5. All UNKNOWN / not ok — "I don't know yet."
# ---------------------------------------------------------------------------

def test_all_unknown():
    o = opt("Merge PR #2410", None, 0.2, oid="p1", rank=None,
            unknowns=("mission_value", "evidence", "risk", "cost", "urgency"))
    s = scored([o])
    text, code = d.run(s, "human")
    assert code == 2, text
    assert "don't have enough evidence" in text or "No rankable option" in text, text


def test_not_ok():
    s = scored([], ok=False, exit_hint=2,
               notes=["No options from Layer 3 — nothing to score."])
    text, code = d.run(s, "human")
    assert code == 2, text
    assert "I don't know yet." in text, text
    assert "No options from Layer 3" in text, text


def test_garbage_input():
    text, code = d.run("not a dict", "human")
    assert code == 2, text
    assert "I don't know yet." in text, text


# ---------------------------------------------------------------------------
# 6. Schema drift — missing keys never KeyError
# ---------------------------------------------------------------------------

def test_schema_drift_minimal_option():
    s = {"ok": True, "options": [{"title": "Bare option"}]}
    text, code = d.run(s, "human")
    assert code == 2  # total UNKNOWN → needs evidence, no crash
    assert "Bare option" in text or "evidence" in text.lower(), text


def test_schema_drift_missing_ok():
    s = {"options": [opt("Merge PR #2410", 0.8, 0.9, rank=1)]}
    text, code = d.run(s, "human")
    assert code == 0, text  # assumed true with warning


def test_schema_drift_no_options_key():
    text, code = d.run({"ok": True}, "human")
    assert code == 2, text


# ---------------------------------------------------------------------------
# 7. Worker mode — full auditable JSON
# ---------------------------------------------------------------------------

def test_worker_mode():
    s = scored([
        opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1),
        opt("Deploy to production", 0.9, 0.9, oid="g1", gated=True, rank=None),
    ])
    text, code = d.run(s, "worker")
    assert code == 3, text
    p = json.loads(text)
    assert p["verdict"] == "gated"
    assert p["exit_hint"] == 3
    # gated → no recommendation FOR THE GATED OPTION; the non-gated best
    # is still offered, clearly separated
    assert p["recommendation"]["title"] == "Merge PR #2410"
    assert len(p["gates"]) == 1
    assert p["gates"][0]["title"] == "Deploy to production"
    assert "decided_utc" in p


def weak_evidence_runner(title="Merge PR #2420", total=0.61, conf=0.8,
                         oid="p2", rank=2):
    """A runner-up that is genuinely weaker on evidence — realistic fixture."""
    o = opt(title, total, conf, oid=oid, rank=rank)
    o["dimensions"]["evidence"] = dim(
        0.4, ["mergeable UNKNOWN — GitHub had not computed it",
              "no independent-validation score on the option"], 0.5)
    o["dimensions"]["mission_value"] = dim(
        0.5, ["PR #2420 mergeability UNKNOWN — value uncertain"], 0.5)
    return o


def test_worker_mode_recommend():
    s = scored([
        opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1),
        weak_evidence_runner(),
    ])
    text, code = d.run(s, "worker")
    assert code == 0
    p = json.loads(text)
    assert p["verdict"] == "recommend"
    assert p["recommendation"]["title"] == "Merge PR #2410"
    assert len(p["ranked_options"]) == 2
    assert p["runner_up_margin"] == round(0.82 - 0.61, 3)
    assert p["driving_dimension"] in d.DIMENSION_ORDER
    # the driving dimension is genuinely the evidence gap
    assert p["driving_dimension"] == "evidence"


def test_cross_check_warns_on_drift():
    s = scored([
        opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1),
        weak_evidence_runner(),
    ], recommendation={"option_id": "p2", "title": "Merge PR #2420",
                       "total": 0.61, "total_confidence": 0.8})
    text, code = d.run(s, "worker")
    assert code == 0
    p = json.loads(text)
    assert any("schema drift" in n for n in p["notes"]), p["notes"]


def test_tied_ranks_fall_back_to_total():
    s = scored([
        opt("B", 0.75, 0.8, oid="p2", rank=1),
        opt("A", 0.82, 0.85, oid="p1", rank=1),
    ])
    text, code = d.run(s, "human")
    assert code == 0, text
    # rank tied → higher total wins honestly
    assert "Merge: A." in text or text.startswith("Merge: A"), text


# ---------------------------------------------------------------------------
# 8. Questions mode
# ---------------------------------------------------------------------------

def test_questions_mode_low_confidence():
    s = scored([opt("Merge PR #2410", 0.82, 0.4, oid="p1", rank=1)])
    text, code = d.run(s, "questions")
    assert code == 2, text
    assert text.startswith("- "), text
    assert len(text.splitlines()) >= 1


# ---------------------------------------------------------------------------
# 9. Zero network — static source check
# ---------------------------------------------------------------------------

def test_no_network_imports():
    src = open(os.path.join(os.path.dirname(__file__), "..", "tools",
                            "decision_output.py")).read()
    for mod in ("socket", "urllib", "requests", "http.client", "httpx"):
        assert f"import {mod}" not in src, f"network import found: {mod}"


# ---------------------------------------------------------------------------
# 10. CLI end to end
# ---------------------------------------------------------------------------

def test_cli_human_exit_0():
    s = scored([opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1)])
    p = run_cli(s, "--mode", "human")
    assert p.returncode == 0, p.stderr
    assert p.stdout.startswith("Merge PR #2410."), p.stdout


def test_cli_gated_exit_3():
    s = scored([opt("Deploy X", 0.9, 0.9, oid="g1", gated=True, rank=None)])
    p = run_cli(s, "--mode", "human")
    assert p.returncode == 3, p.stderr
    assert p.stdout.startswith("This needs Shawn's word:"), p.stdout


def test_cli_questions_exit_2():
    s = scored([opt("Merge PR #2410", 0.8, 0.4, oid="p1", rank=1)])
    p = run_cli(s, "--mode", "questions")
    assert p.returncode == 2, p.stderr


def test_cli_bad_json():
    p = subprocess.run(
        [sys.executable,
         os.path.join(os.path.dirname(__file__), "..", "tools", "decision_output.py"),
         "decide", "--scored", "{bad json"],
        capture_output=True, text=True)
    assert p.returncode == 2
    assert "I don't know yet" in p.stderr


def test_cli_scored_arg():
    s = scored([opt("Merge PR #2410", 0.82, 0.85, oid="p1", rank=1)])
    p = subprocess.run(
        [sys.executable,
         os.path.join(os.path.dirname(__file__), "..", "tools", "decision_output.py"),
         "decide", "--scored", json.dumps(s), "--mode", "human"],
        capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert p.stdout.startswith("Merge PR #2410."), p.stdout
