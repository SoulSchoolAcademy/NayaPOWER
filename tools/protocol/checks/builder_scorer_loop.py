#!/usr/bin/env python3
"""The Builder-Scorer Loop (Shawn, 2026-10-11 — permanent, no exceptions).

"BUILD -> SCORE -> FIX -> SCORE -> FIX -> SCORE -> MERGE -> POST.
Three rounds minimum, then it goes. The feed is for LEARNING, never for
GATING — you do NOT hold back a merge waiting for feed feedback.
Two seats, no bottleneck. Plain English always. BE the intelligence."

This check enforces the loop as machine law. A merge packet for a work
product must carry the receipt of three honest scorecard rounds: what was
built, how each round scored it, what was fixed between rounds, and why
the score moved. Fewer than three rounds fails the gate — the merge does
not go until the loop is complete.

The anti-theater rule: a faked round must be detectable. Each round must
record, in its own words, what changed, why the score moved, and the gaps
found ("why not 10?"). Two rounds that say the same thing fail. A first
round scored perfect fails — nobody scores their own build perfect on
first look. A final round below 9.0 fails — the loop keeps going until
the work is 9+, or the merge still needs Shawn's word.

The POST step is enforced as learning, never as a gate: the check
validates a post when one is recorded (it must name the venue and carry
real content), but an absent post never blocks a merge. Holding a merge
for a feed post is the exact behavior this law forbids.

OPEN TENSION — surfaced, not resolved: this law says the feed is never a
gate, while DELEGATED-MERGE-AUTHORITY (condition 4) still requires the
posted intent + scorecard + validation with the no-objection window. This
check implements the loop only; it does not implement, alter, or waive
any condition of the delegation. Reconciling "don't gate on feed" with
"no seat objects" is for the team and Shawn — this check will not encode
a silent resolution.

Honest bounds (plain English): this gate verifies the RECEIPT's shape —
that three rounds exist, each names a distinct change, a distinct reason
the score moved, and at least one gap found. Round numbers must run in
order, and when rounds carry recorded_at timestamps those must run
forward in time — without timestamps, the numbering alone cannot prove
the rounds were written in order, which the module says out loud.
What the gate cannot catch: a round that rephrases the same fix in
different words (the comparison is textual, not semantic — "improved the
fix" vs "enhanced the fix" reads as different text), and a fabricated
round that is distinct on paper. Those are a different exploit class,
caught by the independent validator (10/10 is never self-declared) and by
the diff the merge actually carries. The check makes theater structurally
harder: three distinct, gap-naming, time-ordered rounds is what turns
"triple self-review" from a slogan into a receipt.

Input record:
    {
      "work_product": "<what was built — branch, PR, or artifact>",
      "seat": "<builder seat>",
      "rounds": [
        {
          "round": 1,
          "score": 8.2,
          "recorded_at": "2026-10-11T18:40:00Z",   # optional; when present, must run non-decreasing
          "what_changed": "<the fix since the previous state; for round 1, the build itself>",
          "why_score_moved": "<why the score is what it is / what moved it>",
          "gaps_found": ["<each 'why not 10?' answer>"]
        },
        ...at least three...
      ],
      "post": {                        # optional; absence never blocks merge
        "posted": true,
        "venue": "<where the learning note went — issue link, feed ref>",
        "content": "<the learning, for the team>"
      }
    }

Checks:
  1. work_product and seat are named — anonymous work carries no loop receipt.
  2. rounds is a list of at least MIN_ROUNDS (3). Fewer fails: the loop is
     not complete, no merge.
  3. Rounds are sequential: round number i+1 at position i, and when the
     rounds carry recorded_at timestamps they must run non-decreasing in
     time. Skipped, renumbered, or backdated rounds fail — the loop runs
     in order, it is not assembled after the fact.
  4. Every score is a finite number on the 0-10 scale. Infinity, NaN, and
     out-of-range scores fail closed: the 9.0 bar is meaningless without a
     bounded number underneath it.
  5. Round 1's score is below 10. A perfect self-score on first look is
     theater — the whole point of the loop is that the first look finds
     things.
  6. Every round's what_changed and why_score_moved carry substance
     (minimum length and word count). "fixed stuff" is not a round.
  7. Every round names at least one gap found ("why not 10?"). A round
     that found nothing learned nothing.
  8. No two rounds may say the same thing: the normalized text of
     what_changed and why_score_moved must be pairwise distinct across
     all rounds. Copy-paste rounds fail as theater.
  9. The final round's score is >= 9.0. Below 9, the loop continues —
     more rounds, more fixing, until it is 9+.
  10. post, if present, names the venue and carries content. If absent,
      the check PASSES with the post pending noted — the feed is for
      learning, never for gating.

The check verifies compliance; it never grants authority.

Usage:
    python3 tools/protocol/checks/builder_scorer_loop.py \
        --record '{"work_product": "...", "seat": "...", "rounds": [...]}' [--json]
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

MIN_ROUNDS = 3
MIN_SCORE_FOR_MERGE = 9.0
MAX_SCORE = 10.0
MIN_TEXT_CHARS = 20
MIN_TEXT_WORDS = 3


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def _normalize(text: str) -> str:
    """Collapse text to its bare meaning-shape for theater comparison."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_time(value) -> datetime | None:
    """Parse an ISO-8601 timestamp; None when unparseable."""
    if not isinstance(value, str):
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _has_substance(text: str) -> bool:
    """A round's words must carry real substance, not filler."""
    t = _nonempty_str(text)
    if len(t) < MIN_TEXT_CHARS:
        return False
    return len(t.split()) >= MIN_TEXT_WORDS


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {
        "law": "BUILDER-SCORER-LOOP",
        "law_status": "RATIFIED (Shawn, 2026-10-11)",
        "min_rounds": MIN_ROUNDS,
        "min_score_for_merge": MIN_SCORE_FOR_MERGE,
    }

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    work_product = _nonempty_str(record.get("work_product"))
    seat = _nonempty_str(record.get("seat"))
    rounds = record.get("rounds")
    post = record.get("post")

    # 1. The receipt names the work and the seat that did it.
    if not work_product:
        return fail(
            "work_product missing — the loop receipt must name the work "
            "that went through the loop",
            details,
        )
    if not seat:
        return fail(
            "seat missing — the loop receipt must name the builder seat; "
            "anonymous work carries no triple self-validation",
            details,
        )
    details["work_product"] = work_product
    details["seat"] = seat

    # 2. Three rounds minimum. The loop is not complete with fewer.
    if not isinstance(rounds, list):
        return fail(
            f"{work_product}: rounds is not a list — the loop receipt must "
            f"carry at least {MIN_ROUNDS} recorded scorecard rounds",
            details,
        )
    if len(rounds) < MIN_ROUNDS:
        return fail(
            f"{work_product}: only {len(rounds)} round(s) recorded — the "
            f"law requires at least {MIN_ROUNDS} honest rounds "
            "(BUILD -> SCORE -> FIX -> SCORE -> FIX -> SCORE) before MERGE",
            details,
        )
    details["rounds_recorded"] = len(rounds)
    reasons.append(f"{len(rounds)} scorecard rounds recorded "
                   f"(minimum {MIN_ROUNDS} met)")

    seen_changed: list[str] = []
    seen_moved: list[str] = []
    prev_at: datetime | None = None  # local only, never in details
    final_score: float | None = None

    for i, r in enumerate(rounds):
        label = f"round {i + 1}"

        # 3. Rounds run in order. The loop is not assembled after the fact.
        if not isinstance(r, dict):
            return fail(
                f"{work_product}: {label} is not a record object — a "
                "malformed round fails closed",
                details,
            )
        rn = r.get("round")
        if type(rn) is not int or rn != i + 1:
            return fail(
                f"{work_product}: {label} is numbered {rn!r}, not {i + 1} "
                "— rounds run in sequence (BUILD -> SCORE -> FIX -> SCORE "
                "-> FIX -> SCORE); skipped or renumbered rounds mean the "
                "loop was assembled after the fact, not run",
                details,
            )

        # 3b. When rounds carry timestamps, time must not run backwards.
        # A round dated before the previous round was written after it —
        # the receipt contradicts its own order.
        # (prev_at stays a local: a datetime in `details` would crash the
        # --json output, which must always serialize.)
        recorded_at = r.get("recorded_at")
        if recorded_at is not None:
            parsed = _parse_time(recorded_at)
            if parsed is None:
                return fail(
                    f"{work_product}: {label} recorded_at "
                    f"{recorded_at!r} is not a parseable ISO-8601 timestamp "
                    "— an unreadable timestamp is no timestamp",
                    details,
                )
            if prev_at is not None and parsed < prev_at:
                return fail(
                    f"{work_product}: {label} recorded_at "
                    f"{recorded_at!r} predates the previous round — rounds "
                    "run forward in time; a backdated round means the loop "
                    "was assembled after the fact, not run",
                    details,
                )
            prev_at = parsed
            reasons.append(f"{label}: recorded_at {recorded_at} in order")
        elif prev_at is not None:
            # Timestamps started, then stopped: the receipt is inconsistent.
            return fail(
                f"{work_product}: {label} has no recorded_at while an "
                "earlier round does — a loop receipt mixes timestamped and "
                "untimestamped rounds. Either all rounds carry recorded_at "
                "or none do",
                details,
            )

        # 4. Scores are finite numbers on the 0-10 scale.
        score = r.get("score")
        if not _is_number(score):
            return fail(
                f"{work_product}: {label} score is not a number — the 9.0 "
                "bar cannot be evaluated on a non-number",
                details,
            )
        if not math.isfinite(score) or not 0.0 <= score <= MAX_SCORE:
            return fail(
                f"{work_product}: {label} score {score!r} is not a finite "
                f"score on the 0-{MAX_SCORE:g} scale — Infinity, NaN, and "
                "out-of-range scores fail closed",
                details,
            )

        # 5. Nobody scores their own build perfect on first look.
        if i == 0 and score >= MAX_SCORE:
            return fail(
                f"{work_product}: round 1 scored {score} — a perfect "
                "self-score on first look is theater. The whole point of "
                "the loop is that the first look finds things; the first "
                "round must name what it found",
                details,
            )

        # 6. Each round's words must carry substance.
        what_changed = _nonempty_str(r.get("what_changed"))
        why_score_moved = _nonempty_str(r.get("why_score_moved"))
        if not _has_substance(what_changed):
            return fail(
                f"{work_product}: {label} what_changed has no substance "
                f"({what_changed!r}) — each round must say, in its own "
                "words, what was fixed since the previous state",
                details,
            )
        if not _has_substance(why_score_moved):
            return fail(
                f"{work_product}: {label} why_score_moved has no substance "
                f"({why_score_moved!r}) — each round must say why the score "
                "is what it is; scores move on evidence, never optimism",
                details,
            )

        # 7. Every round must name at least one gap ("why not 10?").
        gaps = r.get("gaps_found")
        if not isinstance(gaps, list) or not gaps:
            return fail(
                f"{work_product}: {label} gaps_found is empty — every round "
                'must answer "why not 10?" with at least one gap found. '
                "A round that found nothing learned nothing",
                details,
            )
        for g in gaps:
            if not _nonempty_str(g):
                return fail(
                    f"{work_product}: {label} gaps_found contains a blank "
                    'entry — each "why not 10?" answer must be a real gap',
                    details,
                )

        # 8. No two rounds may say the same thing. Copy-paste is theater.
        norm_changed = _normalize(what_changed)
        norm_moved = _normalize(why_score_moved)
        if norm_changed in seen_changed:
            return fail(
                f"{work_product}: {label} what_changed repeats an earlier "
                "round's change text — two rounds cannot claim the same "
                "fix. A faked round is detectable; this one was detected",
                details,
            )
        if norm_moved in seen_moved:
            return fail(
                f"{work_product}: {label} why_score_moved repeats an "
                "earlier round's explanation — each round must explain its "
                "own score in its own words",
                details,
            )
        seen_changed.append(norm_changed)
        seen_moved.append(norm_moved)

        reasons.append(
            f"{label}: score {score}, change stated, score movement "
            f"explained, {len(gaps)} gap(s) named"
        )
        final_score = float(score)

    # 9. The final round must be 9+. Below 9, the loop continues.
    assert final_score is not None
    details["final_score"] = final_score
    if final_score < MIN_SCORE_FOR_MERGE:
        return fail(
            f"{work_product}: final round scored {final_score} < "
            f"{MIN_SCORE_FOR_MERGE} — the law says: if work scores below 9, "
            "do the triple self-validation until it is 9+. The loop "
            "continues — more rounds, more fixing — or the merge still "
            "needs Shawn's word",
            details,
        )
    reasons.append(f"final round score {final_score} >= "
                   f"{MIN_SCORE_FOR_MERGE} — the loop's bar is met")

    # 10. The POST step: learning, never a gate.
    if post is None or (isinstance(post, dict) and post.get("posted") is False
                        and not _nonempty_str(post.get("venue"))
                        and not _nonempty_str(post.get("content"))):
        reasons.append(
            "post not yet recorded — the feed is for LEARNING, never for "
            "GATING; the merge is not held for it. Record the learning "
            "note after the merge."
        )
    else:
        if not isinstance(post, dict):
            return fail(
                f"{work_product}: post is not a record object — the "
                "learning note must name its venue and carry content",
                details,
            )
        if post.get("posted") is False:
            return fail(
                f"{work_product}: post says posted:false but names a venue "
                "— a learning note cannot be both unposted and posted. Say "
                "where it went, or leave post out until it is written",
                details,
            )
        venue = _nonempty_str(post.get("venue"))
        content = _nonempty_str(post.get("content"))
        if not venue:
            return fail(
                f"{work_product}: post.venue missing — the learning note "
                "must say where the team can read it",
                details,
            )
        if not _has_substance(content):
            return fail(
                f"{work_product}: post.content has no substance — the POST "
                "step is the team learning from the loop; a stub teaches "
                "nothing",
                details,
            )
        reasons.append(f"post recorded ({venue}) — the team learns from "
                       "this loop")

    reasons.append(
        f"{work_product}: the Builder-Scorer Loop is complete — BUILD -> "
        "SCORE -> FIX -> SCORE -> FIX -> SCORE is on the record, the bar is "
        "met, and POST is handled as learning, never as a gate"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Builder-Scorer Loop check")
    parser.add_argument("--record", required=True,
                        help="JSON loop receipt (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "BUILDER-SCORER-LOOP"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
