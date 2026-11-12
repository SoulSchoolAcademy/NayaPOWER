#!/usr/bin/env python3
"""The Scorecard Loop — completion-receipt form (PROTOCOL.md Step 15).

PROTOCOL.md (ratified 2026-10-20), Step 15, THE SCORECARD LOOP:

  1. Score it against the ultimate objective — honestly, with evidence.
  2. Ask why it is not a 10. Name the specific reasons, not a feeling.
  3. List the most valuable fixes, ranked by value. Fewer when fewer are
     real; never invent fixes to fill the list.
  4. Apply them in value order, until the score moves. A list that
     changes nothing is theater, not a scorecard.
  5. Re-score. Three rounds. The bar is 9+.

The loop runs at two weights, and the weight is never ambiguous:
compressed, on the output of each consequential action, and in full, on
a cycle's whole output. Below a 9 after three rounds does not ship:
something was seriously wrong with the approach itself, and the failure
itself becomes the smart note. Who scores: the producer runs the loop on
her own work — the loop's 9+ is a production standard, never a
verification. Shipping still requires independent verification by a
different mind; this check never replaces that, and never grants it.

Sibling, not duplicate: tools/protocol/checks/builder_scorer_loop.py
already enforces the 3-round loop on structured MERGE packets (rounds
with score / what_changed / why_score_moved / gaps_found, final >= 9.0,
the merge-gate form of the law). This module is the COMPLETION-RECEIPT +
free-text-claim form of the same law, using Step 15's own fields
(why_not_10, fixes_applied, rescore). The merge packet goes to
builder_scorer_loop; a completion claim — a receipt saying work is done,
or free text claiming it — goes here. One quality loop, two record
shapes, never two loops.

Input record:
    {
      "claim": "<what is claimed complete>",
      "seat": "<producing seat>",
      "objective": "<the named ultimate objective scored against>",
      "weight": "full" | "compressed",        # default "full"
      "compression_reason": "<why compressed is the honest weight>",
                                              # required when compressed
      "rounds": [
        {
          "round": 1,
          "score": 7.0,
          "why_not_10": ["<specific reason>", ...],
          "fixes_applied": ["<fix applied, in value order>", ...],
          "rescore": 8.5
        },
        ...
      ],
      "final_score": 9.5,
      "failure_note_ref": "<smart-note / board ref>"   # optional; see 9
    }

The final_score rule (one rule, stated here, enforced below):
final_score must equal the LAST round's rescore when the last round
carries a rescore, and must equal the last round's score when it does
not. Every non-final round MUST carry a rescore, and that rescore must
equal the next round's score — the chain is how the receipt proves each
re-score started from the previous round's honest result instead of
being assembled after the fact.

Checks:
  1. claim, seat, and objective are present and non-empty. Anonymous
     claims, and scores with no named objective they were scored
     against, are void — a score without its objective is a number,
     not a scorecard.
  2. weight is "full" or "compressed" (absent means "full"). Full
     weight requires >= 3 rounds. Compressed requires >= 1 round AND a
     non-empty compression_reason — the weight is never ambiguous, so
     choosing the light weight must itself be justified on the record.
  3. Rounds are numbered sequentially from 1. Skipped or renumbered
     rounds fail: the loop runs in order, it is not assembled later.
  4. Every score and every rescore is a finite number in [0, 10].
     Infinity, NaN, booleans, strings, and out-of-range values fail
     closed: the 9.0 bar is meaningless without a bounded number.
  5. Every round's why_not_10 is a non-empty list of non-empty strings
     (Step 15: always name why it is not a 10 — a round that names no
     reason learned nothing).
  6. Every round's fixes_applied is a list, and it is non-empty for
     every non-final round. Step 15: a list that changes nothing is
     theater — and a round that applies nothing while claiming the
     score then moved is exactly that theater.
  7. The rescore chain holds: each round's rescore equals the next
     round's score when a next round exists.
  8. final_score obeys the final_score rule stated above.
  9. final_score >= 9.0 passes (the bar is met). final_score < 9.0
     FAILS — unless failure_note_ref is non-empty, in which case the
     check passes with details["shipped"] = false and a reason stating
     the honest-failure path: below 9 does not ship; the failure was
     filed as the note. The loop passing on that path certifies the
     honesty of the receipt, never the shippability of the work.

scan_text(text) is the free-text companion: a done-claim (done /
complete / completed / shipped / merged / landed) with no scorecard-
loop markers at all returns ["DONE_CLAIM_WITHOUT_SCORECARD_LOOP"];
anything else returns []. It detects an ABSENT loop in prose, nothing
more — a text that merely says the word "scorecard" passes scan_text
and still fails check() on shape. That bound is honest and stated:
scan_text is a tripwire, check() is the gate.

Honest bounds: this check verifies the receipt's shape and arithmetic —
rounds exist, are ordered, name why-not-10 reasons, name fixes, and the
score chain is internally consistent. It cannot tell whether a named
fix really happened, whether a score was honest, or whether the
objective named was the right one. Those are caught by independent
verification (Step 11), which this loop never replaces.

Usage:
    python3 tools/protocol/checks/scorecard_loop.py \
        --record '{"claim": "...", "seat": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

FULL_MIN_ROUNDS = 3
COMPRESSED_MIN_ROUNDS = 1
BAR = 9.0
MAX_SCORE = 10.0

_DONE_CLAIM_RE = re.compile(
    r"\b(done|complete|completed|shipped|merged|landed)\b", re.IGNORECASE
)
_LOOP_MARKER_RE = re.compile(
    r"scorecard|score[:\s]*[0-9]|why not (a )?10|round\s*\d", re.IGNORECASE
)


def scan_text(text) -> list[str]:
    """Flag a free-text done-claim carrying no scorecard-loop markers."""
    if not isinstance(text, str) or not text:
        return []
    if _DONE_CLAIM_RE.search(text) and not _LOOP_MARKER_RE.search(text):
        return ["DONE_CLAIM_WITHOUT_SCORECARD_LOOP"]
    return []


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _valid_score(value) -> bool:
    return _is_number(value) and math.isfinite(value) and 0.0 <= value <= MAX_SCORE


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {
        "law": "SCORECARD-LOOP",
        "law_status": "RATIFIED (PROTOCOL.md Step 15, 2026-10-20)",
        "bar": BAR,
        "sibling": "builder_scorer_loop.py (merge-packet form)",
    }

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    claim = _nonempty_str(record.get("claim"))
    seat = _nonempty_str(record.get("seat"))
    objective = _nonempty_str(record.get("objective"))
    weight = record.get("weight", "full")
    compression_reason = _nonempty_str(record.get("compression_reason"))
    rounds = record.get("rounds")
    final_score = record.get("final_score")
    failure_note_ref = _nonempty_str(record.get("failure_note_ref"))

    # 1. The claim, its producer, and the objective it was scored against.
    if not claim:
        return fail(
            "claim missing or empty — a scorecard loop with no claim "
            "attached scores nothing and completes nothing",
            details,
        )
    if not seat:
        return fail(
            f"{claim}: seat missing or empty — the producer scores her "
            "own work, so the producer must be named; an anonymous loop "
            "is no loop",
            details,
        )
    if not objective:
        return fail(
            f"{claim}: objective missing or empty — Step 15 scores "
            "against the named ultimate objective; a score with no named "
            "objective is a number, not a scorecard",
            details,
        )
    details["claim"] = claim
    details["seat"] = seat
    details["objective"] = objective

    # 2. Weight: never ambiguous, and compressed must justify itself.
    if weight not in ("full", "compressed"):
        return fail(
            f"{claim}: weight {weight!r} is not 'full' or 'compressed' — "
            "the loop runs at exactly two weights and the weight is "
            "never ambiguous",
            details,
        )
    details["weight"] = weight
    if not isinstance(rounds, list):
        return fail(
            f"{claim}: rounds is not a list — the loop receipt must "
            "carry its recorded rounds",
            details,
        )
    if weight == "full" and len(rounds) < FULL_MIN_ROUNDS:
        return fail(
            f"{claim}: full weight requires at least {FULL_MIN_ROUNDS} "
            f"rounds, got {len(rounds)} — three rounds is the loop; "
            "fewer is a first look claiming to be a finish",
            details,
        )
    if weight == "compressed":
        if len(rounds) < COMPRESSED_MIN_ROUNDS:
            return fail(
                f"{claim}: compressed weight requires at least "
                f"{COMPRESSED_MIN_ROUNDS} round, got 0 — compressed is "
                "lighter, never absent",
                details,
            )
        if not compression_reason:
            return fail(
                f"{claim}: weight is 'compressed' but compression_reason "
                "is missing or empty — the light weight must be justified "
                "on the record, or the loop could shrink itself to "
                "nothing by declaration",
                details,
            )
        details["compression_reason"] = compression_reason
    details["rounds_recorded"] = len(rounds)
    reasons.append(
        f"{weight} weight: {len(rounds)} round(s) recorded"
        + (" with compression reason stated" if weight == "compressed" else "")
    )

    last_index = len(rounds) - 1
    for i, r in enumerate(rounds):
        label = f"round {i + 1}"
        is_final_round = i == last_index

        if not isinstance(r, dict):
            return fail(
                f"{claim}: {label} is not a record object — a malformed "
                "round fails closed",
                details,
            )

        # 3. Rounds run in sequence from 1.
        rn = r.get("round")
        if type(rn) is not int or rn != i + 1:
            return fail(
                f"{claim}: {label} is numbered {rn!r}, not {i + 1} — "
                "rounds run sequentially from 1; skipped or renumbered "
                "rounds mean the loop was assembled after the fact",
                details,
            )

        # 4. Scores / rescores are finite numbers in [0, 10].
        score = r.get("score")
        if not _valid_score(score):
            return fail(
                f"{claim}: {label} score {score!r} is not a finite "
                f"number in [0, {MAX_SCORE:g}] — the {BAR:g} bar cannot "
                "be evaluated on a non-number or an out-of-range number",
                details,
            )
        has_rescore = "rescore" in r and r.get("rescore") is not None
        rescore = r.get("rescore")
        if has_rescore and not _valid_score(rescore):
            return fail(
                f"{claim}: {label} rescore {rescore!r} is not a finite "
                f"number in [0, {MAX_SCORE:g}] — a re-score must be a "
                "real score on the same scale",
                details,
            )
        if not is_final_round and not has_rescore:
            return fail(
                f"{claim}: {label} has no rescore — every non-final round "
                "must record its re-score after fixes were applied, and "
                "that rescore is the next round's starting score",
                details,
            )

        # 5. Why it is not a 10 — always named, never a feeling alone.
        why_not_10 = r.get("why_not_10")
        if not isinstance(why_not_10, list) or not why_not_10:
            return fail(
                f"{claim}: {label} why_not_10 is not a non-empty list — "
                "Step 15 always asks why it is not a 10 and names the "
                "specific reasons; an empty answer is no loop",
                details,
            )
        for entry in why_not_10:
            if not _nonempty_str(entry):
                return fail(
                    f"{claim}: {label} why_not_10 contains a blank or "
                    "non-string entry — each reason must be a real, "
                    "named reason",
                    details,
                )

        # 6. Fixes applied: a list, and non-empty before the final round.
        fixes = r.get("fixes_applied")
        if not isinstance(fixes, list):
            return fail(
                f"{claim}: {label} fixes_applied is not a list — Step 15 "
                "applies fixes in value order; the receipt must list "
                "what was actually applied",
                details,
            )
        for entry in fixes:
            if not _nonempty_str(entry):
                return fail(
                    f"{claim}: {label} fixes_applied contains a blank "
                    "or non-string entry — each applied fix must be named",
                    details,
                )
        if not is_final_round and not fixes:
            return fail(
                f"{claim}: {label} fixes_applied is empty on a non-final "
                "round — a list that changes nothing is theater, not a "
                "scorecard; if the score moved, something was applied",
                details,
            )

        # 7. The rescore chain: this round's rescore is the next score.
        if not is_final_round:
            nxt = rounds[i + 1]
            next_score = nxt.get("score") if isinstance(nxt, dict) else None
            if _valid_score(next_score) and float(rescore) != float(next_score):
                return fail(
                    f"{claim}: {label} rescore {rescore!r} does not equal "
                    f"round {i + 2} score {next_score!r} — each round's "
                    "re-score is the next round's starting score; a "
                    "broken chain means the rounds were not one loop",
                    details,
                )

        reasons.append(
            f"{label}: score {score}, {len(why_not_10)} why-not-10 "
            f"reason(s) named, {len(fixes)} fix(es) applied"
            + (f", rescore {rescore}" if has_rescore else "")
        )

    # 8. final_score obeys the one stated rule.
    if not _valid_score(final_score):
        return fail(
            f"{claim}: final_score {final_score!r} is not a finite "
            f"number in [0, {MAX_SCORE:g}] — the loop's verdict must be "
            "a real score",
            details,
        )
    final_score_f = float(final_score)
    last_round = rounds[-1]
    last_has_rescore = (
        "rescore" in last_round and last_round.get("rescore") is not None
    )
    expected = (
        float(last_round["rescore"])
        if last_has_rescore
        else float(last_round["score"])
    )
    expected_kind = "rescore" if last_has_rescore else "score"
    if final_score_f != expected:
        return fail(
            f"{claim}: final_score {final_score_f!r} does not equal the "
            f"last round's {expected_kind} {expected!r} — the stated "
            "rule: final_score equals the last round's rescore when it "
            "carries one, otherwise its score",
            details,
        )
    details["final_score"] = final_score_f

    # 9. The bar — and the honest-failure path when it is not met.
    if final_score_f >= BAR:
        details["shipped"] = True
        reasons.append(
            f"final score {final_score_f} >= {BAR:g} — the loop's bar "
            "is met (a production standard; independent verification "
            "still ships it, this loop never replaces that)"
        )
        return result(True, reasons, details)

    if failure_note_ref:
        details["shipped"] = False
        details["failure_note_ref"] = failure_note_ref
        reasons.append(
            f"final score {final_score_f} < {BAR:g} — below 9 does not "
            f"ship; the failure was filed as the note "
            f"({failure_note_ref}), per Step 15's honest-failure path: "
            "stop improving the output, diagnose the approach, and the "
            "failure itself becomes the smart note. This pass certifies "
            "the honest receipt, not shippable work."
        )
        return result(True, reasons, details)

    return fail(
        f"{claim}: final score {final_score_f} < {BAR:g} and no "
        "failure_note_ref — below 9 after the loop does not ship, and "
        "the failure itself must become the smart note; file it and "
        "name its ref, or keep looping",
        details,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scorecard Loop check")
    parser.add_argument("--record", required=True,
                        help="JSON scorecard-loop record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "SCORECARD-LOOP"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
