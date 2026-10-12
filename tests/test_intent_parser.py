#!/usr/bin/env python3
"""Tests for tools/intent_parser.py — Layer 2 of the Ultimate Decision Machine."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from intent_parser import (
    parse_intent,
    classify_intent,
    classify_weight,
    infer_reversibility_stakes,
    detect_ambiguity,
    extract_references,
    plain_words,
)

PASS = 0
FAIL = 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name} {detail}")


def test_classification():
    print("classification:")
    cases = [
        ("What's the most intelligent thing to do next?", "what_next"),
        ("What should we do next?", "what_next"),
        ("Should PR #2410 merge?", "should_merge"),
        ("Is this ready to merge?", "should_merge"),
        ("Which of these three designs?", "which_option"),
        ("What's blocking the team right now?", "what_blocking"),
        ("What's the status of the decision engine?", "status_check"),
        ("Should we build a dashboard?", "should_build"),
    ]
    for text, expected in cases:
        itype, conf, _ = classify_intent(text)
        check(f"classify '{text[:40]}' → {expected}", itype == expected,
              f"got {itype} (conf {conf})")
        check(f"  confidence > 0 for '{text[:30]}'", conf > 0)


def test_weight_classification():
    print("weight classification (Wisdom Spending):")
    # (reversibility, stakes) → expected weight
    cases = [
        (("high", "low"), "five-minute"),
        (("high", "medium"), "standard"),
        (("high", "high"), "standard"),
        (("medium", "high"), "standard"),
        (("low", "low"), "foundational"),      # irreversible → foundational
        (("high", "consequential"), "foundational"),
        (("low", "consequential"), "foundational"),
    ]
    for (rev, stakes), expected in cases:
        weight, reason = classify_weight(rev, stakes)
        check(f"({rev}, {stakes}) → {expected}", weight == expected,
              f"got {weight}: {reason}")
        check(f"  reason is plain words", len(reason) > 20 and "revers" in reason.lower() or "stakes" in reason.lower())


def test_infer_reversibility_stakes():
    print("reversibility/stakes inference:")
    rev, stakes = infer_reversibility_stakes("should_merge", "Should PR #2410 merge?", {})
    check("merge → medium/high", (rev, stakes) == ("medium", "high"), f"got {(rev, stakes)}")
    rev, stakes = infer_reversibility_stakes("status_check", "What's the status?", {})
    check("status → high/low", (rev, stakes) == ("high", "low"), f"got {(rev, stakes)}")
    rev, stakes = infer_reversibility_stakes("should_build", "Should we deploy to production?", {})
    check("production wording → low/consequential", (rev, stakes) == ("low", "consequential"),
          f"got {(rev, stakes)}")
    rev, stakes = infer_reversibility_stakes("what_next", "What's next? urgent!", {})
    check("urgent raises stakes", stakes in ("high", "consequential"), f"got {stakes}")


def test_references():
    print("reference extraction:")
    refs = extract_references('Should PR #2410 merge? Also check naya5/world-model branch.')
    check("PR number extracted", refs.get("pr_numbers") == [2410], str(refs))
    check("branch extracted", refs.get("branches") == ["naya5/world-model"], str(refs))
    refs = extract_references('Which is best: "minimal", "full", "hybrid"?')
    check("quoted options extracted", len(refs.get("quoted_options", [])) == 3, str(refs))


def test_ambiguity():
    print("ambiguity → clarifying questions:")
    # Unknown intent
    r = parse_intent("flibberty gibbet")
    check("unknown intent → not ok", r["ok"] is False)
    check("unknown intent → exit 2", r["exit_hint"] == 2)
    check("unknown intent → has questions", len(r["clarifying_questions"]) > 0)

    # Bare demonstrative
    r = parse_intent("should this merge?")
    check("'should this merge?' → not ok", r["ok"] is False)
    check("'should this merge?' → asks which PR", any("PR" in q for q in r["clarifying_questions"]),
          str(r["clarifying_questions"]))

    # Empty input
    r = parse_intent("")
    check("empty → not ok", r["ok"] is False)

    # Concrete reference → no ambiguity
    r = parse_intent("Should PR #2410 merge?")
    check("'Should PR #2410 merge?' → ok", r["ok"] is True, json.dumps(r)[:200])
    check("  no questions", "clarifying_questions" not in r)


def test_full_parse():
    print("full parse:")
    r = parse_intent("Should PR #2410 merge?")
    check("ok", r["ok"] is True)
    check("intent_type should_merge", r["intent_type"] == "should_merge")
    check("objective mentions PR #2410", "2410" in r["objective"], r["objective"])
    check("has constraints", len(r["constraints"]) >= 2)
    check("merge constraints mention CI", any("CI" in c for c in r["constraints"]))
    check("weight is standard or foundational", r["decision_weight"] in ("standard", "foundational"),
          r["decision_weight"])
    check("has weight_reason", len(r.get("weight_reason", "")) > 10)
    check("confidence in (0,1]", 0 < r["confidence"] <= 1)

    r = parse_intent("What's the status of the lanes?")
    check("status → five-minute or standard", r["decision_weight"] in ("five-minute", "standard"),
          r["decision_weight"])

    # Foundational triggers human review flag
    r = parse_intent("Should we deploy the new engine to production?")
    check("production → foundational", r["decision_weight"] == "foundational",
          r["decision_weight"])
    check("foundational → human review flag", r.get("human_review_recommended") is True)


def test_plain_words():
    print("plain-words output:")
    r = parse_intent("Should PR #2410 merge?")
    out = plain_words(r)
    check("mentions objective", "Objective:" in out)
    check("mentions weight", "Weight:" in out)
    check("mentions constraints", "Constraints:" in out)
    check("no raw JSON", not out.strip().startswith("{"))

    r = parse_intent("should this merge?")
    out = plain_words(r)
    check("ambiguous → questions in plain words", "clarification" in out.lower())


def test_no_network():
    print("no network / no crash without world model:")
    # Should not throw even with no world model file; warns instead
    import intent_parser
    orig = intent_parser.WORLD_MODEL_PATH
    intent_parser.WORLD_MODEL_PATH = Path("/tmp/definitely-not-here-wm.json")
    try:
        r = parse_intent("Should PR #2410 merge?")
        check("parses without world model", r["ok"] is True)
        check("warns about missing model", len(r.get("world_warnings", [])) > 0,
              str(r.get("world_warnings")))
        check("world_context marked unavailable",
              r["world_context"].get("available") is False)
    finally:
        intent_parser.WORLD_MODEL_PATH = orig


def test_grounding():
    print("reference grounding:")
    from intent_parser import ground_references
    # World model with one known PR
    wctx = {"available": True, "open_prs": [
        {"number": 2410, "title": "consolidation", "mergeable": True}
    ], "open_pr_count": 1}
    g = ground_references({"pr_numbers": [2410]}, wctx)
    check("known PR grounded", g["prs"][0]["found"] is True)
    check("known PR title carried", g["prs"][0]["title"] == "consolidation")
    g = ground_references({"pr_numbers": [9999]}, wctx)
    check("unknown PR flagged", g["prs"][0]["found"] is False)
    check("unknown PR warns", len(g["warnings"]) == 1, str(g["warnings"]))
    # No world model → no false warnings
    g = ground_references({"pr_numbers": [2410]}, {"available": False})
    check("no model → no warnings", len(g["warnings"]) == 0)
    check("no model → not found=False alarm", g["prs"][0]["found"] is False)


def test_which_option_letters():
    print("which_option letter handling:")
    r = parse_intent('Should we pick A vs B?')
    check("A vs B → which_option", r["intent_type"] == "which_option",
          r.get("intent_type"))
    check("A vs B → ok (2 options)", r["ok"] is True)
    r = parse_intent('Which option is best?')
    check("bare 'which option' → asks for options", r["ok"] is False)
    # False positive check: normal sentence with capital A shouldn't trigger
    itype, _, _ = classify_intent("A new dashboard would help the team")
    check("'A new dashboard...' not which_option", itype != "which_option",
          f"got {itype}")


if __name__ == "__main__":
    test_classification()
    test_weight_classification()
    test_infer_reversibility_stakes()
    test_references()
    test_ambiguity()
    test_full_parse()
    test_plain_words()
    test_no_network()
    test_grounding()
    test_which_option_letters()
    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
