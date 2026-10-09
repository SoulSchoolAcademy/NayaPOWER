#!/usr/bin/env python3
"""Delegated Merge Authority (Shawn, 2026-10-08 — ratified delegation).

"Naya 5 may merge to main WITHOUT Shawn's per-merge approval iff ALL hold:
(1) built + tests green; (2) honest evidence-backed self-scorecard >= 9.0
with value-calculus run ('most intelligent thing wins'); (3) independent
validation by a DIFFERENT seat; (4) intent + scorecard + validation posted
on #1354, team consensus (no seat objects); (5) merge, then report after:
what, why, scorecard, who validated.

Below 9.0, no independent validation, or any team objection → still needs
Shawn's word. Other protected gates (production deploys, credentials/money,
destructive actions, security/privacy/consent/authority changes) are
UNCHANGED — this delegation covers merges to main ONLY."

This check verifies a merge-to-main packet carries every condition of the
delegation. Every field the delegation's hard line depends on is REQUIRED:
absence fails closed, never defaults to permitted. The check never grants
authority — it verifies the packet that claims it.

Input record:
    {
      "target": "main",              # the ref being merged into
      "branch": "<branch name>",
      "seat": "<merging seat>",
      "tests_green": true,
      "test_evidence": "<CI run / command output ref — the proof>",
      "self_scorecard": {
        "score": 9.2,
        "evidence_backed": true,
        "value_calculus_run": true
      },
      "independent_validator": "<different seat id>",
      "posted_to_1354": true,
      "team_objections": 0,
      "post_merge_report_planned": true
    }

Checks:
  1. Scope: target != "main" → PASS (not applicable; the delegation covers
     merges to main only). This is the law's own scope, not a loophole.
  2. tests_green is True AND test_evidence non-empty AND reference-shaped —
     "built + tests green" needs the proof, not the claim. test_evidence
     must name something a validator can resolve (a URL, a CI run/job id,
     a command transcript with counts, an artifact path) — "trust me,
     green" names nothing resolvable and is unfalsifiable, which is not
     proof.
  3. self_scorecard: score finite and within the 0–10 scale, >= 9.0,
     evidence_backed true, value_calculus_run true — honest,
     evidence-backed, and the math was run. Infinity, NaN, and
     out-of-range scores fail: no isfinite bound means no bar at all.
  4. independent_validator named and, after seat-identity normalization,
     != seat — validation by a DIFFERENT seat; self-validation is not
     validation. "naya5" vs "naya-5" is the same seat wearing different
     punctuation; string inequality is not identity.
  5. posted_to_1354 true AND team_objections == 0 — intent + scorecard +
     validation posted, team consensus, no seat objects.
  6. post_merge_report_planned true — merge, THEN report after.

Honest bounds:
  - The evidence-shape gate verifies test_evidence is REFERENCE-SHAPED
    (resolvable in principle); it cannot verify the run actually went
    green or that the id is real. Forged-but-plausible ids are a different
    exploit class, caught by condition (3)'s independent validator and
    condition (4)'s #1354 posting — the check makes the claim falsifiable,
    which is what turns "trust me" into evidence.
  - Seat normalization covers case and separators plus the KNOWN_SEAT_ALIASES
    map below. A genuinely new alias observed in the wild goes in that map
    with its evidence; the check is never weakened to accommodate one.

Usage:
    python3 tools/protocol/checks/merge_authority.py \
        --record '{"target": "main", ...}' [--json]
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402
from checks.confusables_table import FOLD as _CONFUSABLE_FOLD  # noqa: E402

MIN_SELF_SCORE = 9.0
MAX_SELF_SCORE = 10.0  # scorecards are scored on the 0–10 scale


# Seat identities: "naya5" vs "naya-5" vs "Naya 5" are the same seat wearing
# different punctuation. Normalization collapses case and separators;
# KNOWN_SEAT_ALIASES covers names that differ by more than punctuation
# (post-normalization keys -> canonical seat key). No such aliases are
# currently observed in the team's records — the map is the extension
# point: add an entry with its evidence when one appears, never weaken
# the comparison instead.
KNOWN_SEAT_ALIASES: dict[str, str] = {}


def _seat_key_folded(seat: str) -> tuple[str, bool]:
    # Identity normalization pipeline, in order:
    #   1. NFKC-fold (the b61229d03 micro-fix: fullwidth/compatibility first)
    #   2. Confusable-fold (this fix: Cyrillic/Greek/Armenian/Latin/Other
    #      look-alikes -> canonical ASCII, per Unicode confusables.txt)
    #   3. Strip everything outside [a-z0-9]
    # The confusable fold must come AFTER NFKC (it operates on canonical
    # forms), BEFORE case-folding (U+039D GREEK CAPITAL LETTER NU folds to
    # 'n' in the table, but lowercasing first would turn it into U+03BD,
    # which folds to 'v' — the wrong seat), and BEFORE the strip (so a
    # folded letter survives comparison instead of being erased — erasing
    # the unknown is never a comparison).
    # Returns (key, confusables_seen): the flag says the raw text carried
    # look-alike characters, so the caller can surface it in the record.
    normalized = unicodedata.normalize("NFKC", seat).strip()
    folded = normalized.translate(_CONFUSABLE_FOLD)
    key = re.sub(r"[^a-z0-9]", "", folded.lower())
    return key, folded != normalized


def _seat_key(seat: str) -> str:
    # NFKC-fold FIRST: normalization must translate before it compares.
    # Fullwidth "ｎａｙａ５" folds to "naya5"; the old strip-everything-
    # non-ASCII regex turned it into "" which matches nothing — fail-open
    # by deletion. Erasing the unknown is never a comparison.
    #
    # Confusable-fold SECOND (this fix): "nаya-5" with U+0430 CYRILLIC
    # SMALL LETTER A folds to "naya5" too. NFKC cannot fold it — U+0430 is
    # a distinct letter, not a compatibility form — so it needs its own
    # class mapping (Unicode confusables.txt, 1453 entries), not a bigger
    # hammer. A fully Cyrillic "nауа-5" is single-script (digits and the
    # hyphen are Script=Common), so reject-on-mixed-script would miss it;
    # folding is script-agnostic and closes the whole class.
    key, _ = _seat_key_folded(seat)
    return KNOWN_SEAT_ALIASES.get(key, key)


# test_evidence must be REFERENCE-SHAPED: it must name something an
# independent validator can actually resolve — a URL, a run/job/build/
# artifact/PR/commit identifier, a command transcript with counts, or an
# artifact path. "trust me, green" matches none of these: it is
# unfalsifiable, and unfalsifiable is not proof.
_EVIDENCE_PATTERNS = (
    re.compile(r"https?://\S+"),
    re.compile(
        r"\b(?:ci|test|pytest|workflow|action|run|job|build|suite|artifact|"
        r"pr|commit|sha|log)s?\b[^\n]{0,60}?\d",
        re.IGNORECASE,
    ),
    re.compile(r"(?:^|[\s(\[])(?:[\w.~][\w.~\-]*/)+[\w.~\-]+"),
    re.compile(r"\b\d+\s*(?:passed|failed|skipped|green|ok)\b", re.IGNORECASE),
)


def _is_evidence_shaped(text: str) -> bool:
    return any(p.search(text) for p in _EVIDENCE_PATTERNS)


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "DELEGATED-MERGE-AUTHORITY", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    target = _nonempty_str(record.get("target"))
    branch = _nonempty_str(record.get("branch"))
    seat = _nonempty_str(record.get("seat"))
    tests_green = record.get("tests_green")
    test_evidence = _nonempty_str(record.get("test_evidence"))
    scorecard = record.get("self_scorecard")
    independent_validator = _nonempty_str(record.get("independent_validator"))
    posted_to_1354 = record.get("posted_to_1354")
    team_objections = record.get("team_objections")
    report_planned = record.get("post_merge_report_planned")

    # 1. Scope: the delegation covers merges to main ONLY.
    if not target:
        return fail(
            "target missing — the delegation's scope is merges to main; "
            "an unnamed target fails closed",
            details,
        )
    if target != "main":
        reasons.append(f"target is {target!r}, not main — delegation not "
                       "applicable (it covers merges to main only); PASS "
                       "by scope, not by permission")
        details["target"] = target
        return result(True, reasons, details)
    details["target"] = "main"

    if not branch:
        return fail("branch missing — the merge packet must name the branch", details)
    if not seat:
        return fail(
            f"{branch}: seat unnamed — delegated authority is granted to a "
            "named seat, not to an anonymous merge",
            details,
        )
    details["branch"] = branch
    details["seat"] = seat

    # 2. Built + tests green — with the proof, not the claim.
    if tests_green is not True:
        return fail(
            f"{branch}: tests_green is not true — condition (1) 'built + "
            "tests green' is not met; below the bar, the merge still needs "
            "Shawn's word",
            details,
        )
    if not test_evidence:
        return fail(
            f"{branch}: test_evidence missing — 'tests green' without a CI "
            "run or command-output reference is a claim, not proof",
            details,
        )
    if not _is_evidence_shaped(test_evidence):
        return fail(
            f"{branch}: test_evidence {test_evidence!r} is not "
            "reference-shaped — it names no URL, run/job id, command "
            "transcript, or artifact a validator can resolve. 'trust me, "
            "green' is unfalsifiable, and unfalsifiable is not proof. "
            "Name the run, the command, or the artifact.",
            details,
        )
    reasons.append(f"built + tests green ({test_evidence})")

    # 3. Honest evidence-backed self-scorecard >= 9.0, value calculus run.
    if not isinstance(scorecard, dict):
        return fail(
            f"{branch}: self_scorecard missing — condition (2) requires an "
            "honest evidence-backed self-scorecard >= 9.0 with the value "
            "calculus run. Absence fails closed.",
            details,
        )
    score = scorecard.get("score")
    evidence_backed = scorecard.get("evidence_backed")
    vc_run = scorecard.get("value_calculus_run")
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        return fail(
            f"{branch}: self_scorecard.score is not a number — the 9.0 bar "
            "cannot be evaluated on a non-number",
            details,
        )
    if not math.isfinite(score) or not 0.0 <= score <= MAX_SELF_SCORE:
        return fail(
            f"{branch}: self_scorecard.score {score!r} is not a finite "
            f"score on the 0–{MAX_SELF_SCORE:g} scale — Infinity, NaN, and "
            "out-of-range scores fail closed. The 9.0 bar is meaningless "
            "without a bounded numeric underneath it.",
            details,
        )
    if score < MIN_SELF_SCORE:
        return fail(
            f"{branch}: self_scorecard.score {score} < {MIN_SELF_SCORE} — "
            "below 9.0 the merge still needs Shawn's word",
            details,
        )
    if evidence_backed is not True:
        return fail(
            f"{branch}: self_scorecard.evidence_backed is not true — 'honest "
            "EVIDENCE-BACKED self-scorecard'; scores move only on evidence, "
            "never optimism",
            details,
        )
    if vc_run is not True:
        return fail(
            f"{branch}: self_scorecard.value_calculus_run is not true — the "
            "delegation requires the value calculus run ('most intelligent "
            "thing wins')",
            details,
        )
    reasons.append(f"self-scorecard {score} >= 9.0, evidence-backed, value "
                   "calculus run")
    details["self_score"] = score

    # 4. Independent validation by a DIFFERENT seat.
    if not independent_validator:
        return fail(
            f"{branch}: independent_validator unnamed — condition (3) "
            "'independent validation by a different seat'; without it, the "
            "merge still needs Shawn's word",
            details,
        )
    if independent_validator.lower() == seat.lower():
        return fail(
            f"{branch}: independent_validator == seat ({seat}) — "
            "self-validation is not independent validation; 10/10 is never "
            "self-declared",
            details,
        )
    seat_key, seat_confused = _seat_key_folded(seat)
    val_key, val_confused = _seat_key_folded(independent_validator)
    seat_key = KNOWN_SEAT_ALIASES.get(seat_key, seat_key)
    val_key = KNOWN_SEAT_ALIASES.get(val_key, val_key)
    details["seat_key"] = seat_key
    details["validator_key"] = val_key
    details["confusables_folded"] = seat_confused or val_confused
    if val_key == seat_key:
        fold_note = (" Confusable look-alike characters were folded to "
                     "their canonical forms before comparison."
                     if details["confusables_folded"] else "")
        return fail(
            f"{branch}: independent_validator {independent_validator!r} is "
            f"the same seat as {seat!r} after identity normalization "
            f"(both -> {seat_key!r}) — 'naya5' vs 'naya-5' is one "
            "seat wearing different punctuation, not two seats; "
            "'n\u0430ya-5' (Cyrillic \u0430, U+0430) is the same trick in "
            "another alphabet." + fold_note + " Self-validation is not "
            "independent validation; 10/10 is never self-declared",
            details,
        )
    reasons.append(f"independently validated by {independent_validator}")
    details["independent_validator"] = independent_validator

    # 5. Posted on #1354, team consensus, no objections.
    if posted_to_1354 is not True:
        return fail(
            f"{branch}: posted_to_1354 is not true — condition (4) 'intent + "
            "scorecard + validation posted on #1354'; unposted intent is "
            "not team consensus",
            details,
        )
    if not isinstance(team_objections, int) or isinstance(team_objections, bool):
        return fail(
            f"{branch}: team_objections is not an integer count — 'no seat "
            "objects' must be an explicit zero, not an absent field",
            details,
        )
    if team_objections != 0:
        return fail(
            f"{branch}: team_objections = {team_objections} — a seat "
            "objects; the delegation requires team consensus, so this merge "
            "still needs Shawn's word",
            details,
        )
    reasons.append("intent + scorecard + validation posted on #1354; no "
                   "team objections")

    # 6. Report after.
    if report_planned is not True:
        return fail(
            f"{branch}: post_merge_report_planned is not true — condition "
            "(5) 'merge, then report after: what, why, scorecard, who "
            "validated'",
            details,
        )
    reasons.append("post-merge report planned (what, why, scorecard, who "
                   "validated)")

    reasons.append(f"{branch}: all 5 delegation conditions met — merge to "
                   "main authorized under the delegation")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Delegated Merge Authority check")
    parser.add_argument("--record", required=True,
                        help="JSON merge packet (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "DELEGATED-MERGE-AUTHORITY"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
