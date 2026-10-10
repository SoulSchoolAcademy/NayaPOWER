#!/usr/bin/env python3
"""
validate_receipt.py — Layer 2 engagement-receipt validator (fail-closed).

Usage:
    validate_receipt.py <receipt.json> --assignment-file <assignment.txt>
    validate_receipt.py <receipt.json> --assignment-text "<assignment text>"

Exit 0  -> receipt is VALID (all gates passed).
Exit 1  -> receipt is INVALID. Every failure reason is printed; nothing is
           hidden. Fix the receipt, not the validator.

Gates (all must pass):
  1. All required sections present and non-empty (with minimum lengths).
  2. Exactly 3 DISTINCT domains, each one of the 8 Operating Law domains.
  3. Mission objective is not identical to a canned mission string.
  4. Each domain "why" references assignment-specific terms (keyword overlap
     against the assignment text). Zero overlap = parroting = reject.
  5. Timestamp parses as ISO-8601. Schema identifier matches.
  6. If --expect-assignment-ref is given, the receipt's assignment_ref must
     match it exactly (receipt-to-assignment binding; receipts are not
     transferable).

Stdlib only. No network. No exceptions swallowed: unexpected input fails
closed.
"""

import argparse
import json
import re
import sys
from datetime import datetime

SCHEMA_ID = "naya.activation.engagement_receipt.v1"

VALID_DOMAINS = {
    "decision", "communication", "execution", "learning",
    "authority", "constitution", "design", "code",
}

MIN_MISSION_LEN = 40
MIN_WHY_LEN = 40
MIN_PROOF_LEN = 40
MIN_OVERLAP_PER_WHY = 1      # each "why" must share >=1 content word with assignment
MIN_OVERLAP_TOTAL = 3        # the three "why"s together must share >=3 distinct ones

# Canned mission strings. Compared normalized (lowercase, whitespace-collapsed).
# Dispatchers: extend this list with your canonical mission lines and with prior
# receipts' mission texts (Layer C freshness rule).
CANNED_MISSION_STRINGS = [
    "think once. capture it. learn from it. remember it. use it again. get smarter.",
    "create. connect. grow with us.",
    "nayapower is the governed intelligence and continuity substrate.",
    "nayanet is the governed network of naya experiences.",
    "we do the most intelligent thing possible in any moment, anytime. we ask "
    "what it is. we weigh our options. we identify the highest-ranking option. "
    "we execute it. that's how we roll. always.",
    "build the conditions for intelligence to compound.",
]

STOPWORDS = frozenset("""
a an the and or but if then else when while of at by for with about into
through during before after above below to from up down in out on off over
under again further once here there all any both each few more most other
some such no nor not only own same so than too very can will just don should
now is are was were be been being have has had having do does did doing would
could ought i you he she it we they them his her its our their this that
these those as s t re ve ll d m ll
""".split())


def normalize(text):
    """Lowercase, collapse all whitespace, strip. For canned-string comparison."""
    return re.sub(r"\s+", " ", text.strip().lower())


def content_words(text):
    """Distinct content-bearing words: lowercase alnum tokens, len>=4, not stopwords."""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in tokens if len(t) >= 4 and t not in STOPWORDS}


class Gate:
    """Collects failure reasons. Any failure => invalid (fail-closed)."""

    def __init__(self):
        self.failures = []

    def reject(self, reason):
        self.failures.append(reason)

    def check(self, condition, reason):
        if not condition:
            self.reject(reason)

    @property
    def passed(self):
        return not self.failures


def validate(receipt, assignment_text, expect_assignment_ref=None):
    gate = Gate()

    # --- structural: must be an object ---
    if not isinstance(receipt, dict):
        gate.reject("receipt is not a JSON object")
        return gate

    # --- schema identifier ---
    gate.check(receipt.get("schema") == SCHEMA_ID,
               f"schema must be exactly '{SCHEMA_ID}'")

    # --- seat ---
    seat = receipt.get("seat")
    gate.check(isinstance(seat, str) and seat.strip(),
               "seat is missing or empty")

    # --- timestamp: must parse as ISO-8601 ---
    ts = receipt.get("timestamp")
    if not (isinstance(ts, str) and ts.strip()):
        gate.reject("timestamp is missing or empty")
    else:
        try:
            datetime.fromisoformat(ts.strip().replace("Z", "+00:00"))
        except ValueError:
            gate.reject(f"timestamp is not valid ISO-8601: {ts!r}")

    # --- assignment_ref ---
    aref = receipt.get("assignment_ref")
    gate.check(isinstance(aref, str) and aref.strip(),
               "assignment_ref is missing or empty")
    if expect_assignment_ref is not None:
        gate.check(aref == expect_assignment_ref,
                   f"assignment_ref {aref!r} does not match the expected "
                   f"{expect_assignment_ref!r} — a receipt is bound to exactly "
                   f"one assignment and is not transferable")

    # --- mission objective: present, long enough, not canned ---
    mission = receipt.get("mission_objective_own_words")
    if not (isinstance(mission, str) and mission.strip()):
        gate.reject("mission_objective_own_words is missing or empty")
    else:
        gate.check(len(mission.strip()) >= MIN_MISSION_LEN,
                   f"mission_objective_own_words is too short "
                   f"({len(mission.strip())} chars, minimum {MIN_MISSION_LEN})")
        norm = normalize(mission)
        for canned in CANNED_MISSION_STRINGS:
            if norm == canned:
                gate.reject("mission_objective_own_words is identical to a "
                            "canned mission string — state it fresh, in your own words")
                break

    # --- proof standard: present and long enough ---
    proof = receipt.get("proof_standard")
    if not (isinstance(proof, str) and proof.strip()):
        gate.reject("proof_standard is missing or empty")
    else:
        gate.check(len(proof.strip()) >= MIN_PROOF_LEN,
                   f"proof_standard is too short ({len(proof.strip())} chars, "
                   f"minimum {MIN_PROOF_LEN}) — name the evidence")

    # --- relevant_domains: exactly 3, distinct, valid ---
    domains = receipt.get("relevant_domains")
    if not isinstance(domains, list):
        gate.reject("relevant_domains is missing or not a list")
        domains = []
    else:
        gate.check(len(domains) == 3,
                   f"relevant_domains must contain exactly 3 entries, "
                   f"found {len(domains)}")
        names = []
        for i, entry in enumerate(domains):
            if not isinstance(entry, dict):
                gate.reject(f"relevant_domains[{i}] is not an object")
                continue
            name = entry.get("domain")
            why = entry.get("why_this_task")
            if name in VALID_DOMAINS:
                names.append(name)
            else:
                gate.reject(f"relevant_domains[{i}].domain {name!r} is not one of "
                            f"the 8 Operating Law domains: {sorted(VALID_DOMAINS)}")
            if not (isinstance(why, str) and why.strip()):
                gate.reject(f"relevant_domains[{i}].why_this_task is missing or empty")
            elif len(why.strip()) < MIN_WHY_LEN:
                gate.reject(f"relevant_domains[{i}].why_this_task is too short "
                            f"({len(why.strip())} chars, minimum {MIN_WHY_LEN})")
        distinct = set(names)
        gate.check(len(distinct) == 3,
                   f"relevant_domains must name 3 DISTINCT domains, "
                   f"found {len(distinct)} distinct: {sorted(distinct)}")

    # --- anti-parroting: keyword overlap of each "why" vs assignment text ---
    assignment_words = content_words(assignment_text or "")
    if not assignment_words:
        gate.reject("assignment text has no content-bearing words to check against")
    else:
        total_overlap = set()
        for i, entry in enumerate(domains):
            if not isinstance(entry, dict):
                continue
            why = entry.get("why_this_task") or ""
            overlap = content_words(why) & assignment_words
            total_overlap |= overlap
            gate.check(len(overlap) >= MIN_OVERLAP_PER_WHY,
                       f"relevant_domains[{i}].why_this_task shares no "
                       f"content-bearing words with the assignment text "
                       f"(parroting check) — reference the actual assignment")
        gate.check(len(total_overlap) >= MIN_OVERLAP_TOTAL,
                   f"the three why_this_task texts together reference only "
                   f"{len(total_overlap)} distinct assignment term(s) "
                   f"{sorted(total_overlap)}; minimum {MIN_OVERLAP_TOTAL} "
                   f"— argue THIS task, not any task")

    return gate


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Fail-closed validator for Layer 2 activation receipts.")
    parser.add_argument("receipt", help="Path to the receipt JSON file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--assignment-file",
                       help="Path to a file containing the assignment text.")
    group.add_argument("--assignment-text",
                       help="The assignment text, inline.")
    parser.add_argument("--expect-assignment-ref",
                        help="The assignment_ref this receipt must be bound to. "
                             "If given, the receipt's assignment_ref must match "
                             "exactly — a receipt written for another assignment "
                             "is rejected even if it is otherwise valid.")
    args = parser.parse_args(argv)

    try:
        with open(args.receipt, "r", encoding="utf-8") as f:
            receipt = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL: cannot read/parse receipt JSON: {e}")
        return 1

    if args.assignment_file:
        try:
            with open(args.assignment_file, "r", encoding="utf-8") as f:
                assignment_text = f.read()
        except OSError as e:
            print(f"FAIL: cannot read assignment file: {e}")
            return 1
    else:
        assignment_text = args.assignment_text

    gate = validate(receipt, assignment_text,
                      expect_assignment_ref=args.expect_assignment_ref)

    if gate.passed:
        domains = [d["domain"] for d in receipt["relevant_domains"]]
        print(f"VALID: receipt from seat '{receipt['seat']}' "
              f"for assignment_ref '{receipt['assignment_ref']}' "
              f"— domains: {', '.join(domains)}")
        return 0

    print(f"INVALID: {len(gate.failures)} gate failure(s) — "
          f"fix the receipt, not the validator:")
    for reason in gate.failures:
        print(f"  FAIL: {reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
