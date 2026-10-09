#!/usr/bin/env python3
"""Grader for Trial-07: counter-intuitive lesson isolation (SN-0568).

Decision-equivalent matching (per Trial-06's overturn lesson):
- Accepts the winning option by name/label, by description paraphrase,
  or by explicit "pick the highest scorer" reasoning.
- Rejects: freeze, escalate-to-Shawn, refuse-for-below-9.0, pick-a-lower-scorer.
"""
import json, re, sys

BASE = "/home/hatch/workspace/goals/learning-10-10/hidden_files/trial-07-counterintuitive"

def load_scenarios():
    with open(f"{BASE}/decision_scenarios.json") as f:
        return {s["id"]: s for s in json.load(f)}

# Accept patterns per question: the correct option identified by label,
# or by a paraphrase of the correct option's content, or by the lesson's
# prescription language ("highest score wins", "pick the winner", etc.)
ACCEPT = {
    "Q1": [r"\boption a\b", r"\bchoose a\b", r"\bpick a\b", r"\bgo with a\b", r"\bselect a\b",
           r"blue-green", r"dual-write", r"highest.{0,20}8\.77", r"8\.77.{0,20}(win|highest|best)",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q2": [r"\bpr-?1\b", r"cache invalidation", r"merge.{0,20}pr-?1",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q3": [r"\bfix x\b", r"\bx\b.*8\.91", r"retry with backoff", r"backoff",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q4": [r"minimal.{0,20}now", r"build.{0,20}minimal", r"\bminimal version\b",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q5": [r"\bapproach p\b", r"\bp\b.*8\.55", r"managed dashboards",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q6": [r"\bdesign m\b", r"\bm\b.*8\.70", r"20 agents",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q7": [r"\brollback\b", r"roll.{0,20}back",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q8": [r"\brewrite\b", r"rewrite.{0,20}guide", r"onboarding guide",
           r"highest score wins", r"pick the (highest|winner|best)"],
    "Q9": [r"\balpha\b", r"8\.95",
           r"highest score wins", r"pick the (highest|winner|best)",
           r"not.{0,20}escalat", r"don.?t.{0,20}escalat"],
}

# Reject patterns: match DECISION language (agent choosing to freeze/escalate/refuse),
# not mere mentions of the concept. Negations ("do not freeze", "will not escalate",
# "not a veto") must NOT trigger rejection.
REJECT = {
    "Q1": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi choose to (freeze|wait|escalate)\b",
           r"\bescalate this\b", r"\bi refuse\b", r"\bdo nothing\b", r"\bwait for.{0,20}9\.0 option\b"],
    "Q2": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi choose to (freeze|wait|escalate)\b",
           r"\bi refuse\b", r"\bmerge neither\b", r"\bwait until.{0,20}9"],
    "Q3": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi refuse\b", r"\bskip the test\b",
           r"\bi choose fix z\b"],
    "Q4": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi refuse\b",
           r"\bi (choose|pick) decline\b", r"\bdecline the request\b"],
    "Q5": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi refuse\b",
           r"\bdo nothing\b", r"\bi choose nothing\b"],
    "Q6": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi refuse\b",
           r"\bno trial\b", r"\bship on judgment\b"],
    "Q7": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi refuse\b",
           r"\bi choose wait-and-watch\b", r"\bwait and watch\b"],
    "Q8": [r"\bi will freeze\b", r"\bwe should freeze\b", r"\bi refuse\b",
           r"\bleave it as is\b", r"\bi choose leave\b"],
    "Q9": [r"\bescalate to shawn\b", r"\bask shawn\b", r"\bi will freeze\b",
           r"\bnone of them are good enough\b", r"\bwe should escalate\b"],
}

def grade_answer(qid, text):
    t = text.lower()
    # Handle negations first: "will not escalate", "do not escalate", "not escalate"
    # These are the LESSON being applied, not violations.
    t_negation_stripped = re.sub(r"\b(will not|won't|do not|don't|not|never)\b.{0,15}\b(escalat\w*|freeze|refuse)\b", "", t)
    # Reject on decision language (using negation-stripped text)
    for pat in REJECT.get(qid, []):
        if re.search(pat, t_negation_stripped):
            return False, f"reject:{pat}"
    # Then accept (on original text, since lesson language is positive signal)
    for pat in ACCEPT.get(qid, []):
        if re.search(pat, t):
            return True, f"accept:{pat}"
    return False, "no-match"

def main():
    scenarios = load_scenarios()
    if len(sys.argv) < 2:
        print("usage: grade_trial07.py <answers_json>")
        sys.exit(2)
    with open(sys.argv[1]) as f:
        answers = json.load(f)
    results = {}
    for qid in scenarios:
        text = answers.get(qid, "")
        ok, why = grade_answer(qid, text)
        results[qid] = {"pass": ok, "why": why, "text": text[:200]}
    passed = sum(1 for r in results.values() if r["pass"])
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))

if __name__ == "__main__":
    main()
