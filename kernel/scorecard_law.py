"""NayaPOWER Scorecard Law engine (Operating Code V2 §1.1).

The supreme decision procedure, compiled to code:

    ENUMERATE → SCORE → GATE → DECIDE → RECEIPT

Deterministic, dependency-free, stdlib-only. Gates run BEFORE scores are read
(V2 §1.3): a gate failure kills the option regardless of score, and a score
never grants permission — authority is checked independently of optimality.

V2 §1.1 score dimensions: mission alignment, value produced, consequences
(pros and cons), collective impact, risk, reversibility.
V2 §1.1 hard-stop gates: reversible, no major damage, positive forward effect.

Every failure is a named reason; the engine fails closed and never raises on
valid input shapes (malformed input raises ValueError naming the defect, so
callers can distinguish "bad input" from "decision refused").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

ENGINE_ID = "SCORECARD-LAW-V2"
ENGINE_VERSION = "2.0.0"

# V2 §1.1 — the five steps, in order. No exceptions. No shortcuts.
STEPS = ("enumerate", "score", "gate", "decide", "receipt")

# V2 §1.1 — the six honest-score dimensions.
SCORE_DIMENSIONS = (
    "mission_alignment",
    "value_produced",
    "consequences",
    "collective_impact",
    "risk",
    "reversibility",
)

# V2 §1.1 — the three hard-stop gates.
GATE_FIELDS = (
    "reversible",
    "no_major_damage",
    "positive_forward_effect",
)

# V2 §1.4 / §5.1 — human-only gates. A score never grants permission: when any
# of these is attested true, the decision needs Shawn regardless of the math.
HUMAN_ONLY_GATES = (
    "constitutional_ratification",
    "production_dispatch",
    "production_db",
    "workflows",
    "credentials_money",
    "destructive_irreversible",
    "authority_consent_security",
)

# Decision verdicts.
PROCEED = "PROCEED"
NEEDS_AUTHORITY = "NEEDS_AUTHORITY"
NO_DECISION = "NO_DECISION"

# ---- Named failure reasons (fail closed) ------------------------------------
# Enumerate
ENUMERATE_OPTIONS_NOT_LIST = "ENUMERATE_OPTIONS_NOT_LIST"
ENUMERATE_TOO_FEW_OPTIONS = "ENUMERATE_TOO_FEW_OPTIONS"
ENUMERATE_MISSING_ID = "ENUMERATE_MISSING_ID"
ENUMERATE_DUPLICATE_ID = "ENUMERATE_DUPLICATE_ID"
# Score
SCORE_OPTION_NOT_SCORED = "SCORE_OPTION_NOT_SCORED"
SCORE_DIMENSIONS_NOT_OBJECT = "SCORE_DIMENSIONS_NOT_OBJECT"
SCORE_MISSING_DIMENSION = "SCORE_MISSING_DIMENSION"
SCORE_NON_NUMERIC_DIMENSION = "SCORE_NON_NUMERIC_DIMENSION"
SCORE_DIMENSION_OUT_OF_RANGE = "SCORE_DIMENSION_OUT_OF_RANGE"
# Gate
GATE_ASSESSMENT_MISSING = "GATE_ASSESSMENT_MISSING"
GATE_NOT_BOOLEAN = "GATE_NOT_BOOLEAN"
GATE_FAILED = "GATE_FAILED"
# Authority (V2 §1.3 — a score never grants permission)
AUTHORITY_HUMAN_ONLY_GATE = "AUTHORITY_HUMAN_ONLY_GATE"
# Decide
DECIDE_NO_GATE_PASSERS = "DECIDE_NO_GATE_PASSERS"
DECIDE_NO_CLEAR_WINNER = "DECIDE_NO_CLEAR_WINNER"
DECIDE_WINNER_NOT_ENUMERATED = "DECIDE_WINNER_NOT_ENUMERATED"
DECIDE_WINNER_FAILED_GATE = "DECIDE_WINNER_FAILED_GATE"
DECIDE_WINNER_NOT_HIGHEST = "DECIDE_WINNER_NOT_HIGHEST"
# Receipt (V2 §1.1 — no receipt, no action)
RECEIPT_NOT_OBJECT = "RECEIPT_NOT_OBJECT"
RECEIPT_MISSING_STEP = "RECEIPT_MISSING_STEP"
RECEIPT_NOT_POSTED = "RECEIPT_NOT_POSTED"


def _dim_value(dims: Mapping[str, object], option_id: str, dim: str, reasons: list[str]) -> float | None:
    """Validate one score dimension; append a named reason and return None on failure."""
    if dim not in dims:
        reasons.append(f"{SCORE_MISSING_DIMENSION}: option '{option_id}' missing dimension '{dim}'")
        return None
    v = dims[dim]
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        reasons.append(f"{SCORE_NON_NUMERIC_DIMENSION}: option '{option_id}' dimension '{dim}' must be numeric 0-10")
        return None
    if v < 0 or v > 10:
        reasons.append(f"{SCORE_DIMENSION_OUT_OF_RANGE}: option '{option_id}' dimension '{dim}' out of range 0-10")
        return None
    return float(v)


@dataclass(frozen=True)
class OptionScore:
    """One option's six-dimension honest score."""

    option_id: str
    dimensions: Mapping[str, float]

    def total(self) -> float:
        return sum(float(self.dimensions[d]) for d in SCORE_DIMENSIONS)


@dataclass(frozen=True)
class GateAssessment:
    """One option's three hard-stop gates. A failure here kills the option."""

    option_id: str
    gates: Mapping[str, bool]

    def failed_gates(self) -> list[str]:
        return [g for g in GATE_FIELDS if self.gates.get(g) is not True]

    def passes(self) -> bool:
        return not self.failed_gates()


@dataclass(frozen=True)
class ScorecardResult:
    """The five steps, executed. verdict ∈ {PROCEED, NEEDS_AUTHORITY, NO_DECISION}."""

    verdict: str
    winner_id: str | None
    totals: Mapping[str, float]
    killed_by_gate: Mapping[str, Sequence[str]]
    reasons: Sequence[str]
    receipt: Mapping[str, object]


def _enumerate(option_ids: Sequence[str], reasons: list[str]) -> list[str]:
    """Step 1 — ENUMERATE. Every real option, each with a unique non-empty id."""
    if not isinstance(option_ids, (list, tuple)):
        reasons.append(ENUMERATE_OPTIONS_NOT_LIST)
        return []
    ids = [o for o in option_ids if isinstance(o, str) and o.strip()]
    if len(ids) != len(option_ids):
        reasons.append(ENUMERATE_MISSING_ID)
    if len(ids) < 2:
        reasons.append(ENUMERATE_TOO_FEW_OPTIONS)
        return []
    seen: set[str] = set()
    dupes = sorted({o for o in ids if o in seen or seen.add(o)})
    if dupes:
        reasons.append(f"{ENUMERATE_DUPLICATE_ID}: {dupes}")
        return []
    return ids


def _score(
    option_ids: Sequence[str],
    scores: Mapping[str, Mapping[str, float]],
    reasons: list[str],
) -> dict[str, OptionScore]:
    """Step 2 — SCORE. Every option scored honestly on all six dimensions."""
    scored: dict[str, OptionScore] = {}
    if not isinstance(scores, Mapping):
        for oid in option_ids:
            reasons.append(f"{SCORE_OPTION_NOT_SCORED}: option '{oid}' has no score entry")
        return scored
    for oid in option_ids:
        dims = scores.get(oid)
        if not isinstance(dims, Mapping):
            reasons.append(f"{SCORE_OPTION_NOT_SCORED}: option '{oid}' has no score entry")
            continue
        values: dict[str, float] = {}
        ok = True
        for dim in SCORE_DIMENSIONS:
            v = _dim_value(dims, oid, dim, reasons)
            if v is None:
                ok = False
                break
            values[dim] = v
        if ok:
            scored[oid] = OptionScore(option_id=oid, dimensions=values)
    return scored


def _gate(
    option_ids: Sequence[str],
    gates: Mapping[str, Mapping[str, bool]],
    reasons: list[str],
) -> tuple[dict[str, GateAssessment], dict[str, list[str]]]:
    """Step 3 — GATE. Hard stops; a gate failure kills the option regardless of score.

    Gates run BEFORE scores are read (V2 §1.3): killed options are recorded
    with the gates they failed, whether or not they hold the highest total.
    """
    assessed: dict[str, GateAssessment] = {}
    killed: dict[str, list[str]] = {}
    for oid in option_ids:
        entry = gates.get(oid) if isinstance(gates, Mapping) else None
        if not isinstance(entry, Mapping):
            reasons.append(f"{GATE_ASSESSMENT_MISSING}: option '{oid}' has no gate assessment")
            killed[oid] = ["assessment_missing"]
            continue
        values: dict[str, bool] = {}
        ok = True
        for g in GATE_FIELDS:
            v = entry.get(g)
            if v is not True and v is not False:
                reasons.append(f"{GATE_NOT_BOOLEAN}: option '{oid}' gate '{g}' must be a boolean")
                ok = False
                break
            values[g] = v
        if not ok:
            killed[oid] = ["assessment_invalid"]
            continue
        assessment = GateAssessment(option_id=oid, gates=values)
        assessed[oid] = assessment
        failed = assessment.failed_gates()
        if failed:
            killed[oid] = failed
            reasons.append(f"{GATE_FAILED}: option '{oid}' failed gate(s) {failed} — killed regardless of score")
    return assessed, killed


def _decide(
    scored: Mapping[str, OptionScore],
    killed: Mapping[str, Sequence[str]],
    reasons: list[str],
) -> tuple[str, str | None]:
    """Step 4 — DECIDE. Highest valid (gate-passing) total wins. Act without asking.

    A tie at the top is not decided by coin flip: uncertainty means no
    decision until the evidence discriminates (V2 §1.2 — the calculator, not
    escalation; more scoring, not a guess).
    """
    eligible = {oid: s for oid, s in scored.items() if oid not in killed}
    if not eligible:
        reasons.append(DECIDE_NO_GATE_PASSERS)
        return NO_DECISION, None
    best = max(s.total() for s in eligible.values())
    leaders = sorted(oid for oid, s in eligible.items() if s.total() == best)
    if len(leaders) > 1:
        reasons.append(f"{DECIDE_NO_CLEAR_WINNER}: tied at {best} among {leaders} — score further, do not guess")
        return NO_DECISION, None
    return PROCEED, leaders[0]


def _check_authority(
    authority_flags: Mapping[str, bool] | None, reasons: list[str]
) -> bool:
    """V2 §1.3 — a score never grants permission. Authority is separate from optimality."""
    if not authority_flags:
        return False
    triggered = sorted(g for g in HUMAN_ONLY_GATES if authority_flags.get(g) is True)
    if triggered:
        reasons.append(f"{AUTHORITY_HUMAN_ONLY_GATE}: human-only gate(s) {triggered} — needs Shawn regardless of score")
        return True
    return False


def build_receipt(
    decision_id: str,
    option_ids: Sequence[str],
    scored: Mapping[str, OptionScore],
    assessed: Mapping[str, GateAssessment],
    verdict: str,
    winner_id: str | None,
    reasons: Sequence[str],
    decided_by: str,
    decided_at: str,
    receipt_posted_comment_id: int | None = None,
) -> dict:
    """Step 5 — RECEIPT. The five steps written as one object, ready to post.

    V2 §1.1: no receipt, no action. The receipt is posted by the caller; the
    posted comment id is what makes it checkable by an independent seat.
    """
    return {
        "engine": ENGINE_ID,
        "engine_version": ENGINE_VERSION,
        "decision_id": decision_id,
        "decided_by": decided_by,
        "decided_at": decided_at,
        "step1_enumerate": {"options": [{"id": oid} for oid in option_ids]},
        "step2_score": {
            "scores": {
                oid: {d: s.dimensions[d] for d in SCORE_DIMENSIONS} for oid, s in scored.items()
            },
            "totals": {oid: s.total() for oid, s in scored.items()},
        },
        "step3_gate": {
            oid: {g: assessed[oid].gates[g] for g in GATE_FIELDS}
            for oid in assessed
        },
        "step4_decide": {
            "winner": winner_id,
            "verdict": verdict,
            "reasons": list(reasons),
        },
        "step5_receipt": {
            "posted": receipt_posted_comment_id is not None,
            "receipt_posted_comment_id": receipt_posted_comment_id,
        },
    }


def run_scorecard(
    option_ids: Sequence[str],
    scores: Mapping[str, Mapping[str, float]],
    gates: Mapping[str, Mapping[str, bool]],
    *,
    decision_id: str = "",
    decided_by: str = "",
    decided_at: str = "",
    authority_flags: Mapping[str, bool] | None = None,
    receipt_posted_comment_id: int | None = None,
) -> ScorecardResult:
    """Run the five steps in order and return the result with its receipt.

    Malformed input raises ValueError naming the defect (callers distinguish
    "bad input" from "decision refused": refused decisions are returned with
    verdict NO_DECISION or NEEDS_AUTHORITY plus named reasons, never raised).
    """
    reasons: list[str] = []
    ids = _enumerate(option_ids, reasons)
    if not ids:
        receipt = build_receipt(
            decision_id, [], {}, {}, NO_DECISION, None, reasons,
            decided_by, decided_at, receipt_posted_comment_id,
        )
        return ScorecardResult(NO_DECISION, None, {}, {}, reasons, receipt)

    scored = _score(ids, scores, reasons)
    assessed, killed = _gate(ids, gates, reasons)

    # Structural integrity: every enumerated option must be scored AND
    # gate-assessed. A missing score or a malformed gate assessment is not a
    # "failed gate" — it is untrustworthy evidence, and the decision is refused
    # (fail closed) rather than decided on a partial board.
    structurally_sound = set(scored) == set(ids) and set(assessed) == set(ids)
    if not structurally_sound:
        receipt = build_receipt(
            decision_id, ids, scored, assessed, NO_DECISION, None, reasons,
            decided_by, decided_at, receipt_posted_comment_id,
        )
        return ScorecardResult(
            NO_DECISION, None,
            {oid: s.total() for oid, s in scored.items()},
            killed, tuple(reasons), receipt,
        )

    verdict, winner = _decide(scored, killed, reasons)

    # V2 §1.3 — gates ran before scores were read; now authority overrides score.
    if verdict == PROCEED and _check_authority(authority_flags, reasons):
        verdict, winner = NEEDS_AUTHORITY, None

    receipt = build_receipt(
        decision_id, ids, scored, assessed, verdict, winner, reasons,
        decided_by, decided_at, receipt_posted_comment_id,
    )
    return ScorecardResult(
        verdict=verdict,
        winner_id=winner,
        totals={oid: s.total() for oid, s in scored.items()},
        killed_by_gate=killed,
        reasons=tuple(reasons),
        receipt=receipt,
    )


def validate_receipt(receipt: Mapping[str, object]) -> tuple[bool, list[str]]:
    """Validate a SCORECARD-LAW-V2 receipt mechanically, re-deriving the decision.

    Returns (ok, reasons). ok is True only when all five steps hold:
    enumerated ids are unique; every option scored on all six dimensions in
    0-10; every gate is a boolean; the winner is an enumerated id that passes
    all gates and holds the highest total; the receipt is posted
    (receipt_posted_comment_id present — V2 §1.1: no receipt, no action).

    This is the canonical receipt validator used by the auto-merge gate's
    V2 path (tools/auto_merge_gate.py): one mechanism for the receipt, not two.
    """
    reasons: list[str] = []
    if not isinstance(receipt, Mapping):
        return False, [RECEIPT_NOT_OBJECT]

    for step in ("step1_enumerate", "step2_score", "step3_gate", "step4_decide", "step5_receipt"):
        if not isinstance(receipt.get(step), Mapping):
            reasons.append(f"{RECEIPT_MISSING_STEP}: '{step}' missing or not an object")

    # Re-derive steps 1-4 from the receipt's own data.
    s1 = receipt.get("step1_enumerate")
    option_ids: list[str] = []
    if isinstance(s1, Mapping):
        options = s1.get("options")
        if isinstance(options, list):
            option_ids = [o.get("id") for o in options if isinstance(o, Mapping) and o.get("id")]

    tmp: list[str] = []
    ids = _enumerate(option_ids, tmp) if option_ids else []
    reasons.extend(tmp)

    s2 = receipt.get("step2_score")
    scored: dict[str, OptionScore] = {}
    if isinstance(s2, Mapping) and ids:
        scored = _score(ids, s2.get("scores"), reasons)

    s3 = receipt.get("step3_gate")
    assessed: dict[str, GateAssessment] = {}
    killed: dict[str, Sequence[str]] = {}
    if isinstance(s3, Mapping) and ids:
        assessed, killed = _gate(ids, s3, reasons)

    s4 = receipt.get("step4_decide")
    claimed_winner: str | None = None
    claimed_verdict: str | None = None
    if isinstance(s4, Mapping):
        claimed_winner = s4.get("winner")
        claimed_verdict = s4.get("verdict")

    # The winner claim is re-derived, not trusted.
    re_verdict, re_winner = _decide(scored, killed, [])
    if claimed_winner not in ids:
        reasons.append(f"{DECIDE_WINNER_NOT_ENUMERATED}: winner '{claimed_winner}' is not an enumerated option id")
    elif claimed_winner in killed:
        reasons.append(f"{DECIDE_WINNER_FAILED_GATE}: winner '{claimed_winner}' failed gate(s) {list(killed.get(claimed_winner, []))}")
    elif re_verdict == PROCEED and claimed_winner != re_winner:
        reasons.append(
            f"{DECIDE_WINNER_NOT_HIGHEST}: winner '{claimed_winner}' does not hold the highest "
            f"valid total (re-derived winner '{re_winner}') — the math decides, not the author"
        )
    if claimed_verdict not in (PROCEED, NEEDS_AUTHORITY, NO_DECISION):
        reasons.append(f"{RECEIPT_MISSING_STEP}: step4_decide.verdict must be PROCEED, NEEDS_AUTHORITY, or NO_DECISION")

    # Step 5 — written AND posted. A private scorecard is not a gate.
    s5 = receipt.get("step5_receipt")
    if not isinstance(s5, Mapping) or not isinstance(s5.get("receipt_posted_comment_id"), int):
        reasons.append(f"{RECEIPT_NOT_POSTED}: receipt_posted_comment_id missing — no receipt, no action")

    return (len(reasons) == 0, reasons)


def receipt_summary(result: ScorecardResult) -> str:
    """One-line plain-meaning summary of a scorecard result (V2 §2 — plain words)."""
    if result.verdict == PROCEED:
        total = result.totals.get(result.winner_id or "", 0.0)
        return f"DECIDE {result.winner_id} (score {total:.1f}/{6 * 10}); gates passed; receipt ready to post."
    if result.verdict == NEEDS_AUTHORITY:
        return "NEEDS SHAWN — a human-only gate applies; the score does not grant permission."
    first = result.reasons[0] if result.reasons else "unknown"
    return f"NO DECISION — {first}"
