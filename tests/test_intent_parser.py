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
    check("  no questions asked", r.get("clarifying_questions") == [])


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


def test_pr_extraction_variants():
    print("F1: PR extraction without '#':")
    check("'merge PR 2412' → [2412]",
          extract_references("merge PR 2412").get("pr_numbers") == [2412],
          str(extract_references("merge PR 2412")))
    check("'merge pull request 2412' → [2412]",
          extract_references("merge pull request 2412").get("pr_numbers") == [2412])
    check("bare 'should we merge 2412?' → [2412]",
          extract_references("should we merge 2412?").get("pr_numbers") == [2412])
    check("'ship 2412 now' → [2412]",
          extract_references("ship 2412 now").get("pr_numbers") == [2412])
    check("year not grabbed: 'ship 2026 plan' → no PR numbers",
          extract_references("ship 2026 plan").get("pr_numbers") in (None, []),
          str(extract_references("ship 2026 plan")))
    check("year not grabbed: 'merge the 2026 roadmap' → no PR numbers",
          extract_references("merge the 2026 roadmap").get("pr_numbers") in (None, []))
    check("explicit marker wins: 'merge PR #1999' → [1999] even though year-like",
          extract_references("merge PR #1999").get("pr_numbers") == [1999])
    check("deduped: 'merge PR #2412' → [2412] once",
          extract_references("merge PR #2412").get("pr_numbers") == [2412])
    # End-to-end: the IV's headline case — the ref must survive to grounding
    r = parse_intent("merge PR 2412")
    check("end-to-end 'merge PR 2412' keeps the ref",
          r["references"].get("pr_numbers") == [2412],
          json.dumps(r["references"]))
    check("end-to-end 'merge PR 2412' → should_merge ok",
          r["ok"] is True and r["intent_type"] == "should_merge")
    r = parse_intent("merge pull request 2412")
    check("end-to-end 'merge pull request 2412' → should_merge ok",
          r["ok"] is True and r["intent_type"] == "should_merge"
          and r["references"].get("pr_numbers") == [2412],
          json.dumps({k: r.get(k) for k in ("ok", "intent_type", "references")}))
    r = parse_intent("pull-request 2412 should merge")
    check("end-to-end 'pull-request 2412 should merge' → should_merge",
          r["ok"] is True and r["intent_type"] == "should_merge")
    check("'merge 2412 and 2413' → both numbers",
          extract_references("merge 2412 and 2413").get("pr_numbers") == [2412, 2413])
    r = parse_intent("merge 2412 and 2413")
    check("end-to-end 'merge 2412 and 2413' → should_merge ok, both refs",
          r["ok"] is True and r["intent_type"] == "should_merge"
          and r["references"].get("pr_numbers") == [2412, 2413])
    r = parse_intent("merge 2026")
    check("'merge 2026' (year, no ref) → asks which PR, doesn't proceed",
          r["ok"] is False and r["exit_hint"] == 2
          and any("PR" in q for q in r["clarifying_questions"]))


def test_negation():
    print("F2: negation → clarifying question, never silent proceed:")
    r = parse_intent("I don't want to merge PR 2412")
    check("negated merge → not ok", r["ok"] is False)
    check("negated merge → exit 2", r["exit_hint"] == 2)
    check("negated merge → asks what instead",
          any("instead" in q for q in r["clarifying_questions"]),
          str(r["clarifying_questions"]))
    check("negated merge → names the PR",
          any("2412" in q for q in r["clarifying_questions"]),
          str(r["clarifying_questions"]))
    r = parse_intent("should we NOT ship this")
    check("'should we NOT ship this' → not ok", r["ok"] is False)
    check("'should we NOT ship this' → exit 2", r["exit_hint"] == 2)
    r = parse_intent("should we not build the dashboard")
    check("'should we not build the dashboard' → not ok", r["ok"] is False)
    # The 'or not' tag question is NOT a negation — it still decides
    r = parse_intent("Should PR #2410 merge or not?")
    check("'merge or not?' → still should_merge ok",
          r["ok"] is True and r["intent_type"] == "should_merge",
          json.dumps({k: r.get(k) for k in ("ok", "intent_type")}))
    # 'not' inside a problem description is not intent negation
    r = parse_intent("What's blocking the team? Nothing is moving.")
    check("'not' in problem description → not flipped",
          r["ok"] is True and r["intent_type"] == "what_blocking"
          and not any("instead" in q for q in r.get("clarifying_questions", [])),
          json.dumps({k: r.get(k) for k in ("ok", "intent_type")})[:150])


def test_schema_consistency():
    print("F3: same schema on every path:")
    paths = {
        "empty": parse_intent(""),
        "unknown": parse_intent("flibberty gibbet"),
        "ambiguous": parse_intent("should this merge?"),
        "negated": parse_intent("I don't want to merge PR 2412"),
        "ok": parse_intent("Should PR #2410 merge?"),
    }
    required = {"ok", "exit_hint", "intent_type", "intent_description",
                "objective", "constraints", "decision_weight", "weight_reason",
                "reversibility", "stakes", "references", "grounded_references",
                "world_context", "world_warnings", "clarifying_questions",
                "confidence", "note", "parsed_utc"}
    for name, r in paths.items():
        missing = required - set(r.keys())
        check(f"{name} path has all schema keys", not missing,
              f"missing: {sorted(missing)}")
        try:
            json.dumps(r)
            serializable = True
        except (TypeError, ValueError):
            serializable = False
        check(f"{name} path is JSON-serializable (Layer 4/5 safe)", serializable)
    # Honest nulls, not fabricated values, on the ambiguous path
    r = paths["ambiguous"]
    check("ambiguous → decision_weight is null (unknown, not guessed)",
          r["decision_weight"] is None)
    check("ambiguous → constraints empty (unknown, not fabricated)",
          r["constraints"] == [])
    check("ambiguous → refs still carried (known info kept)",
          r["references"] == {} or isinstance(r["references"], dict))


def test_cli_bare_text():
    print("CLI: bare-text shortcut and exit codes:")
    import subprocess
    tool = str(Path(__file__).resolve().parent.parent / "tools" / "intent_parser.py")
    p = subprocess.run([sys.executable, tool, "I don't want to merge PR 2412"],
                       capture_output=True, text=True)
    check("bare negated text → exit 2", p.returncode == 2, f"exit {p.returncode}")
    check("bare negated text → asks instead",
          "instead" in p.stdout, p.stdout[:120])
    p = subprocess.run([sys.executable, tool, "parse", "Should PR #2410 merge?"],
                       capture_output=True, text=True)
    check("parse subcommand → exit 0", p.returncode == 0, f"exit {p.returncode}")
    r = json.loads(p.stdout)
    check("parse subcommand → valid intent JSON",
          r["ok"] is True and r["intent_type"] == "should_merge")


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
    test_pr_extraction_variants()
    test_negation()
    test_schema_consistency()
    test_cli_bare_text()
    print(f"\n{PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
