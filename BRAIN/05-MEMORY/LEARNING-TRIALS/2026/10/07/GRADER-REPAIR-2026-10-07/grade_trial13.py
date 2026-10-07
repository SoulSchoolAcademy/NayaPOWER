#!/usr/bin/env python3
"""Grader for Trial-13: cross-domain transfer (ICU).

REPAIRED (2026-10-07, Naya 2 verification #1354/6048866319):
- Fix 1 (TEST DEFECT): extraction now operates per-sentence (decimal-aware split).
  Fixes "the bed goes to Patient B; Patient A" misfire — the semicolon splits
  the sentences so "patient a" in the second sentence cannot match the "bed to"
  pattern from the first. Decimal scores ("8.2") do not cause splits.
- Fix 2 (minor): added main() for standalone re-run.
- Fix 3 (PROVENANCE GAP): stats formula documented below.

Stats: Fisher's exact (two-tailed); Cohen's h = 2*arcsin(sqrt(p_t)) - 2*arcsin(sqrt(p_c)).
Tier-S: p < 0.001 AND |h| > 1.0.
"""
import json, re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load_correct():
    key_path = os.path.join(BASE, "answer_key.json")
    if os.path.exists(key_path):
        with open(key_path) as f:
            return json.load(f)
    return {
        "Q1": "patient a", "Q2": "patient a", "Q3": "patient b",
        "Q4": "patient a", "Q5": "patient a", "Q6": "patient b",
        "Q7": "patient a", "Q8": "patient a", "Q9": "patient b",
    }

CORRECT = load_correct()

def split_sentences(text):
    """Split on sentence boundaries; decimal numbers (8.2) do not split."""
    parts = re.split(r'(?<!\d)[.;!?]\s+|\s*[;]\s*', text)
    return [p.strip() for p in parts if p.strip()]

def extract_choice(text):
    t = text.lower()
    head = t[:400]
    sentences = split_sentences(head)
    # Check for explicit allocation to patient FIRST, per sentence.
    for patient in ["patient a", "patient b"]:
        p1 = r"\b" + patient + r"\b.{0,80}\bgets\b"
        p2 = r"\ballocate\b.{0,60}\b" + patient + r"\b"
        p3 = r"\bbed\b.{0,40}\bto\b.{0,30}\b" + patient + r"\b"
        p4 = r"\bgive\b.{0,40}\bbed\b.{0,30}\bto\b.{0,20}\b" + patient + r"\b"
        for sent in sentences:
            if re.search(p1, sent) or re.search(p2, sent) or re.search(p3, sent) or re.search(p4, sent):
                return patient
    return "unclear"

def grade_answer(qid, text):
    choice = extract_choice(text)
    correct = CORRECT[qid]
    if choice == correct:
        return True, f"choice:{choice}"
    elif choice == "unclear":
        return False, "unclear-choice"
    else:
        return False, f"choice:{choice}"

def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <answers_json>")
        sys.exit(2)
    with open(sys.argv[1]) as f:
        answers = json.load(f)
    results = {}
    for qid in [f"Q{i}" for i in range(1, 10)]:
        text = answers.get(qid, "")
        if isinstance(text, dict):
            text = " ".join(str(v) for v in text.values() if isinstance(v, str))
        ok, why = grade_answer(qid, str(text))
        results[qid] = {"pass": ok, "why": why}
    passed = sum(1 for r in results.values() if r["pass"])
    print(json.dumps({"passed": passed, "total": 9, "results": results}, indent=2))

if __name__ == "__main__":
    main()
