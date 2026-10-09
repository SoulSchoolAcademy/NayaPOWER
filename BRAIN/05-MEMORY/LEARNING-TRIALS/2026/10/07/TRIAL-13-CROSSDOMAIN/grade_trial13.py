#!/usr/bin/env python3
"""Grader for Trial-13: cross-domain transfer (ICU)."""
import json, re, sys

CORRECT = {
    "Q1": "patient a",
    "Q2": "patient a",
    "Q3": "patient b",
    "Q4": "patient a",
    "Q5": "patient a",
    "Q6": "patient b",
    "Q7": "patient a",
    "Q8": "patient a",
    "Q9": "patient b",
}

def extract_choice(text):
    t = text.lower()
    head = t[:400]
    # Check for explicit allocation to patient FIRST
    # Pattern: "Patient X ... gets the bed" or "allocate ... to Patient X"
    for patient in ["patient a", "patient b"]:
        # "Patient X" at start followed by "gets" within 80 chars (allows parentheticals)
        p1 = "\\b" + patient + "\\b.{0,80}\\bgets\\b"
        p2 = "\\ballocate\\b.{0,60}\\b" + patient + "\\b"
        p3 = "\\bbed\\b.{0,40}\\bto\\b.{0,30}\\b" + patient + "\\b"
        p4 = "\\bgive\\b.{0,40}\\bbed\\b.{0,30}\\bto\\b.{0,20}\\b" + patient + "\\b"
        if re.search(p1, head) or re.search(p2, head) or re.search(p3, head) or re.search(p4, head):
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
