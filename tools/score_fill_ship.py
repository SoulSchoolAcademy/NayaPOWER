#!/usr/bin/env python3
"""NayaPOWER Score-Fill-Ship engine (Operating Code V2 §3.1).

The method, compiled to code:

    SCORE → FIND HOLES → FILL EVERY HOLE → RE-SCORE → SHIP

V2 §3.2: nothing below 9.0 ships, nothing below 9.0 reaches Shawn.
V2 §3.8: no one scores their own work — verification is independent or it
doesn't count. Three rounds, not two hundred: if it takes 200 rounds, the
scoring was dishonest or the holes weren't named.

Usage:
    python3 tools/score_fill_ship.py <work_state.json>

Reads a work-state JSON object (see build_work_state in tests), evaluates the
shipment decision, and prints a verdict.

Exit code 0: SHIP.  Exit code 1: NOT YET (reasons printed).
Exit code 2: usage / input error.

Fail-closed: any missing or unresolvable field fails its check. Self-scored
rounds fail the independent-verification gate.

Stdlib only. The engine functions are pure and importable for the test suite.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Mapping, Sequence

ENGINE_ID = "SCORE-FILL-SHIP-V1"
ENGINE_VERSION = "1.0.0"

# V2 §3.2 — the quality floor. V2 §3.1 — three rounds, not two hundred.
SHIP_FLOOR = 9.0
AAA_THRESHOLD = 9.5
MAX_ROUNDS = 3

SHIP = "SHIP"
NOT_YET = "NOT_YET"

# ---- Named failure reasons (fail closed) ------------------------------------
NOT_STARTED = "NOT_STARTED"                      # no scoring rounds at all
SHIP_BELOW_FLOOR = "SHIP_BELOW_FLOOR"            # latest score < 9.0
SHIP_ROUNDS_EXCEEDED = "SHIP_ROUNDS_EXCEEDED"    # > MAX_ROUNDS without reaching 10
SHIP_HOLES_UNNAMED = "SHIP_HOLES_UNNAMED"        # score < 10 with no holes named
SHIP_HOLES_OPEN = "SHIP_HOLES_OPEN"              # holes without fill evidence
SHIP_RESCORE_MISSING = "SHIP_RESCORE_MISSING"    # filled holes never re-scored
SHIP_SELF_VERIFIED = "SHIP_SELF_VERIFIED"        # scorer == verifier (V2 §3.8)
SHIP_SCORE_OUT_OF_RANGE = "SHIP_SCORE_OUT_OF_RANGE"
SHIP_ROUND_OUT_OF_ORDER = "SHIP_ROUND_OUT_OF_ORDER"


def _finite_score(value: object, round_no: int, reasons: list[str]) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        reasons.append(f"{SHIP_SCORE_OUT_OF_RANGE}: round {round_no} score must be numeric 0-10")
        return None
    if value < 0 or value > 10:
        reasons.append(f"{SHIP_SCORE_OUT_OF_RANGE}: round {round_no} score {value} out of range 0-10")
        return None
    return float(value)


@dataclass(frozen=True)
class Hole:
    """One named gap between the score and 10 (V2 §3.1 — holes must be NAMED)."""

    hole_id: str
    description: str
    fill_evidence: str = ""

    def is_filled(self) -> bool:
        return bool(self.fill_evidence and self.fill_evidence.strip())


@dataclass(frozen=True)
class ScoreRound:
    """One score → holes → fill → re-score cycle. scorer != verifier (V2 §3.8)."""

    round_no: int
    score: float
    holes: Sequence[Hole]
    scorer: str
    verifier: str

    def independently_verified(self) -> bool:
        return bool(self.scorer and self.verifier and self.scorer != self.verifier)


@dataclass(frozen=True)
class ShipVerdict:
    ship: bool
    grade: str  # "AAA" | "PASS" | "NOT_YET"
    reasons: Sequence[str]
    rounds_evaluated: int


def evaluate_shipment(rounds: Sequence[ScoreRound]) -> ShipVerdict:
    """Evaluate the shipment decision over the recorded rounds, latest last.

    Returns a ShipVerdict. ship is True only when: the latest score is >= 9.0,
    every named hole carries fill evidence, the fills were re-scored, the
    latest round was independently verified, and the work took at most three
    rounds to reach shippable state. Every refusal names its reason.
    """
    reasons: list[str] = []
    rounds = list(rounds)
    if not rounds:
        return ShipVerdict(False, NOT_YET, (NOT_STARTED,), 0)

    # Rounds must be ordered and numbered 1..n.
    for i, r in enumerate(rounds, 1):
        if r.round_no != i:
            reasons.append(f"{SHIP_ROUND_OUT_OF_ORDER}: expected round {i}, got {r.round_no}")
    if reasons:
        return ShipVerdict(False, NOT_YET, tuple(reasons), len(rounds))

    latest = rounds[-1]
    if not (0.0 <= latest.score <= 10.0):
        reasons.append(f"{SHIP_SCORE_OUT_OF_RANGE}: round {latest.round_no} score out of range 0-10")
        return ShipVerdict(False, NOT_YET, tuple(reasons), len(rounds))

    # V2 §3.8 — nobody grades their own homework.
    if not latest.independently_verified():
        reasons.append(
            f"{SHIP_SELF_VERIFIED}: round {latest.round_no} scorer '{latest.scorer}' "
            f"is also the verifier — verification is independent or it doesn't count"
        )

    # V2 §3.1 — score < 10 demands named holes.
    if latest.score < 10.0 and not latest.holes:
        reasons.append(f"{SHIP_HOLES_UNNAMED}: score {latest.score} < 10 with no holes named — name the gaps")

    # Every hole must be filled with evidence, and the fill must be re-scored.
    open_holes = [h.hole_id for h in latest.holes if not h.is_filled()]
    if open_holes:
        reasons.append(f"{SHIP_HOLES_OPEN}: holes without fill evidence: {open_holes}")
    if len(rounds) > 1:
        prev = rounds[-2]
        prev_open = [h.hole_id for h in prev.holes if not h.is_filled()]
        if prev_open and latest.score <= prev.score:
            reasons.append(
                f"{SHIP_RESCORE_MISSING}: previous round's holes {prev_open} were filled "
                f"but the re-score ({latest.score}) did not improve on {prev.score}"
            )

    # V2 §3.1 — three rounds, not two hundred.
    if len(rounds) > MAX_ROUNDS and latest.score < 10.0:
        reasons.append(
            f"{SHIP_ROUNDS_EXCEEDED}: {len(rounds)} rounds without reaching 10 — "
            "the scoring was dishonest or the holes weren't named; stop and re-score honestly"
        )

    # V2 §3.2 — nothing below 9.0 ships.
    if latest.score < SHIP_FLOOR:
        reasons.append(f"{SHIP_BELOW_FLOOR}: score {latest.score} < {SHIP_FLOOR} — fix it before anyone sees it")

    if reasons:
        return ShipVerdict(False, NOT_YET, tuple(reasons), len(rounds))
    grade = "AAA" if latest.score >= AAA_THRESHOLD else "PASS"
    return ShipVerdict(True, grade, (), len(rounds))


def parse_work_state(state: Mapping[str, object]) -> list[ScoreRound]:
    """Parse a work-state JSON object into ScoreRounds. Raises ValueError on defects."""
    if not isinstance(state, Mapping):
        raise ValueError("work_state must be an object")
    raw_rounds = state.get("rounds")
    if not isinstance(raw_rounds, list):
        raise ValueError("work_state.rounds must be a list")
    rounds: list[ScoreRound] = []
    reasons: list[str] = []
    for raw in raw_rounds:
        if not isinstance(raw, Mapping):
            raise ValueError("each round must be an object")
        round_no = raw.get("round_no")
        if not isinstance(round_no, int):
            raise ValueError("round.round_no must be an integer")
        score = _finite_score(raw.get("score"), round_no, reasons)
        if score is None:
            raise ValueError("; ".join(reasons))
        holes: list[Hole] = []
        for h in raw.get("holes") or []:
            if not isinstance(h, Mapping) or not h.get("hole_id"):
                raise ValueError(f"round {round_no}: each hole needs a hole_id")
            holes.append(
                Hole(
                    hole_id=str(h["hole_id"]),
                    description=str(h.get("description") or ""),
                    fill_evidence=str(h.get("fill_evidence") or ""),
                )
            )
        rounds.append(
            ScoreRound(
                round_no=round_no,
                score=score,
                holes=tuple(holes),
                scorer=str(raw.get("scorer") or ""),
                verifier=str(raw.get("verifier") or ""),
            )
        )
    return rounds


def main(argv: Sequence[str]) -> int:
    if len(argv) != 2:
        print("usage: python3 tools/score_fill_ship.py <work_state.json>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], "r", encoding="utf-8") as fh:
            state = json.load(fh)
        rounds = parse_work_state(state)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"engine": ENGINE_ID, "ship": False, "error": str(exc)}))
        return 2
    verdict = evaluate_shipment(rounds)
    print(
        json.dumps(
            {
                "engine": ENGINE_ID,
                "ship": verdict.ship,
                "grade": verdict.grade,
                "reasons": list(verdict.reasons),
                "rounds_evaluated": verdict.rounds_evaluated,
            },
            indent=2,
        )
    )
    return 0 if verdict.ship else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
