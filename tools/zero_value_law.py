"""NAYA-ZERO-VALUE-LAW-V1 — executable machinery (PROPOSED, NOT RATIFIED).

Status: DRAFT. Ratification is Shawn's gate. This module implements the *machinery*
described in the seat's 2026-10-10 proposal as additive clarification of Smart
Ledger V2.1 — it does not replace the V2.1 receipt schema or create a second
ledger.

The law in one line: Naya must never confuse "we measured zero" with
"we don't know." Unknown, unmeasured, delayed, and inconclusive are not zero,
and the schema must refuse to let anyone record them as zero.

Null discipline: null means NOT ESTABLISHED. A numeric zero is an actual
assertion. This module never coerces null -> 0, and the validator refuses any
receipt that does.

Reconciliation note (+-9 vs +-10): the signed-value fix on branch
naya4/value-calculus-signed removed the clamp from build_decision_receipt —
d_verified now carries the verified actual unclamped. The +-9 anchors are
reference vocabulary (display), not clipping bounds. This module does not
reimpose any clamp and does not re-litigate that decision; it documents it.
"""

LAW_ID = "NAYA-ZERO-VALUE-LAW-V1"
LAW_STATUS = "PROPOSED — draft machinery; ratification is Shawn's gate"

# ---------------------------------------------------------------------------
# Interpretations
# ---------------------------------------------------------------------------
TRUE_ZERO = "TRUE_ZERO"                     # exact zero established, deterministic
PRACTICALLY_NEUTRAL = "PRACTICALLY_NEUTRAL"  # measured within justified tolerance
UNKNOWN = "UNKNOWN"                         # cannot currently be determined
UNMEASURED = "UNMEASURED"                    # measurement not performed
DELAYED = "DELAYED"                          # consequences pending; window open
INCONCLUSIVE = "INCONCLUSIVE"                # evidence spans signs; unresolved
BASELINE_ZERO = "BASELINE_ZERO"              # self-comparison; zero by definition
ROUNDED_DISPLAY_ZERO = "ROUNDED_DISPLAY_ZERO"  # display rounding of nonzero raw
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"

ZERO_INTERPRETATIONS = frozenset(
    {TRUE_ZERO, PRACTICALLY_NEUTRAL, BASELINE_ZERO, ROUNDED_DISPLAY_ZERO}
)
NONZERO_UNKNOWN_INTERPRETATIONS = frozenset({UNKNOWN, UNMEASURED, DELAYED, INCONCLUSIVE})

ASSESSMENT_STATES = ("UNASSESSED", "ASSESSED", "VERIFIED_VALUE")
VERIFICATION_STATES = ("UNVERIFIED", "PASS_PENDING_WINDOW", "VERIFIED_PASS", "FAIL", "ESCALATE")

# Verification states under which a verified ladder value may exist.
VERIFIED_VALUE_ALLOWED = frozenset({"VERIFIED_PASS", "FAIL"})


# ---------------------------------------------------------------------------
# Refusal codes (machine-readable)
# ---------------------------------------------------------------------------
NULL_ACTUAL_WITH_VERIFIED_VALUE = "NULL_ACTUAL_WITH_VERIFIED_VALUE"
VERIFIED_VALUE_WITHOUT_VERIFICATION = "VERIFIED_VALUE_WITHOUT_VERIFICATION"
ZERO_WITHOUT_ESTABLISHMENT = "ZERO_WITHOUT_ESTABLISHMENT"
PRACTICAL_NEUTRALITY_NEEDS_EPSILON = "PRACTICAL_NEUTRALITY_NEEDS_EPSILON"
INTERPRETATION_VALUE_MISMATCH = "INTERPRETATION_VALUE_MISMATCH"
ROUNDED_ZERO_NEEDS_RAW = "ROUNDED_ZERO_NEEDS_RAW"
PREDICTED_IS_NOT_VERIFIED = "PREDICTED_IS_NOT_VERIFIED"
HARM_UNRESOLVED_BLOCKS_NEUTRAL = "HARM_UNRESOLVED_BLOCKS_NEUTRAL"
INVALID_INTERVAL = "INVALID_INTERVAL"


def _epsilon_declared(epsilon):
    """An epsilon counts only if declared, versioned, and justified."""
    return (
        isinstance(epsilon, dict)
        and isinstance(epsilon.get("value"), (int, float))
        and bool(epsilon.get("version"))
        and bool(epsilon.get("justification"))
    )


def classify_zero(
    *,
    assessment_state,
    verification=None,
    interval=None,
    epsilon=None,
    evidence_refs=(),
    deterministic=False,
    actual_value=None,
    baseline_self_compare=False,
    display_rounded=False,
    raw_value=None,
    observation_window=None,
    measurement_performed=True,
    unresolved_harm=False,
):
    """Classify what a value outcome means — never confusing unknown with zero.

    Returns {"interpretation", "refusal", "reasons"}. A refusal is never silent:
    the interpretation falls back to the honest state (usually INCONCLUSIVE or
    UNKNOWN) and the refusal code names exactly what was missing.
    """
    reasons = []

    # 1. Unresolved critical harm overrides everything. LAW first.
    if unresolved_harm:
        return {
            "interpretation": INCONCLUSIVE,
            "refusal": HARM_UNRESOLVED_BLOCKS_NEUTRAL,
            "reasons": ["unresolved critical harm: no zero/neutral classification permitted"],
        }

    # 2. No assessment at all: unknown is not zero.
    if assessment_state == "UNASSESSED":
        interp = UNMEASURED if not measurement_performed else UNKNOWN
        reasons.append("no established value assessment; null is not zero")
        return {"interpretation": interp, "refusal": None, "reasons": reasons}

    # 3. Delayed consequences: the window decides, not the point estimate.
    if isinstance(observation_window, dict) and observation_window.get("status") == "OPEN":
        reasons.append("observation window open: assessment stays provisional")
        return {"interpretation": DELAYED, "refusal": None, "reasons": reasons}

    # 4. Self-comparison: zero by definition, says nothing about goodness.
    if baseline_self_compare:
        reasons.append("comparing the current course against itself: exactly zero by definition")
        return {"interpretation": BASELINE_ZERO, "refusal": None, "reasons": reasons}

    # 5. Display rounding: the raw value is preserved and governs.
    if display_rounded:
        if raw_value is None or raw_value == 0:
            return {
                "interpretation": INCONCLUSIVE,
                "refusal": ROUNDED_ZERO_NEEDS_RAW,
                "reasons": ["rounded display zero requires a stored nonzero raw value"],
            }
        reasons.append("display rounds to 0; raw nonzero value preserved and governs")
        return {
            "interpretation": ROUNDED_DISPLAY_ZERO,
            "refusal": None,
            "reasons": reasons,
            "raw_value": raw_value,
        }

    # 6. Interval classification — the width matters as much as the center.
    if interval is not None:
        try:
            L, U = float(interval[0]), float(interval[1])
        except (TypeError, ValueError, IndexError):
            return {
                "interpretation": INCONCLUSIVE,
                "refusal": INVALID_INTERVAL,
                "reasons": ["interval must be a [L, U] pair of numbers"],
            }
        if L > U:
            return {
                "interpretation": INCONCLUSIVE,
                "refusal": INVALID_INTERVAL,
                "reasons": ["interval lower bound exceeds upper bound"],
            }
        eps_declared = _epsilon_declared(epsilon)
        eps = float(epsilon["value"]) if eps_declared else None
        if eps is not None and L > eps:
            return {"interpretation": POSITIVE, "refusal": None,
                    "reasons": ["interval entirely above +tolerance"]}
        if eps is not None and U < -eps:
            return {"interpretation": NEGATIVE, "refusal": None,
                    "reasons": ["interval entirely below -tolerance"]}
        if eps is not None and L >= -eps and U <= eps:
            reasons.append("interval inside justified tolerance: practically neutral, not exact zero")
            return {"interpretation": PRACTICALLY_NEUTRAL, "refusal": None, "reasons": reasons}
        if not eps_declared:
            reasons.append("cannot claim practical neutrality without a declared, versioned tolerance")
            return {
                "interpretation": INCONCLUSIVE,
                "refusal": PRACTICAL_NEUTRALITY_NEEDS_EPSILON,
                "reasons": reasons,
            }
        reasons.append("interval spans signs or exceeds tolerance: inconclusive")
        return {"interpretation": INCONCLUSIVE, "refusal": None, "reasons": reasons}

    # 7. Point zero: exact only by deterministic proof; otherwise needs tolerance.
    if actual_value == 0:
        if deterministic:
            if evidence_refs:
                reasons.append("deterministic count establishes exactly zero for the stated metric")
                return {"interpretation": TRUE_ZERO, "refusal": None, "reasons": reasons}
            return {
                "interpretation": INCONCLUSIVE,
                "refusal": ZERO_WITHOUT_ESTABLISHMENT,
                "reasons": ["exact zero asserted without the evidence that establishes it"],
            }
        if _epsilon_declared(epsilon) and evidence_refs:
            reasons.append("point zero inside declared tolerance with evidence: practically neutral")
            return {"interpretation": PRACTICALLY_NEUTRAL, "refusal": None, "reasons": reasons}
        reasons.append("point zero without deterministic proof or justified tolerance: inconclusive")
        return {
            "interpretation": INCONCLUSIVE,
            "refusal": PRACTICAL_NEUTRALITY_NEEDS_EPSILON,
            "reasons": reasons,
        }

    # 8. Nothing established a zero: stay honest.
    reasons.append("no established zero; outcome remains as assessed")
    return {"interpretation": INCONCLUSIVE, "refusal": None, "reasons": reasons}


def validate_receipt(receipt):
    """Cross-field validator for V2.1 decision receipts. Additive to the schema.

    Returns {"ok": bool, "refusals": [...], "notes": [...]}. Never coerces null.
    """
    refusals = []
    notes = []
    r = dict(receipt)

    verification = r.get("verification")
    actual = r.get("delta_v_actual")
    d_verified = r.get("d_verified")
    predicted = r.get("delta_v_predicted")
    interp = r.get("value_interpretation")
    evidence_refs = r.get("evidence_refs") or []
    epsilon = r.get("epsilon")

    # R1: the exact gap case — verified value with no verified actual.
    if d_verified is not None and actual is None:
        refusals.append(NULL_ACTUAL_WITH_VERIFIED_VALUE)
        notes.append("d_verified is numeric while delta_v_actual is null: null means not established")

    # R2: a verified ladder value needs a verifying state.
    if d_verified is not None and verification not in VERIFIED_VALUE_ALLOWED:
        refusals.append(VERIFIED_VALUE_WITHOUT_VERIFICATION)
        notes.append("d_verified set while verification=%r cannot carry a verified value" % (verification,))

    # R8: a prediction is not a verification.
    if actual is None and d_verified is not None and predicted is not None and d_verified == predicted:
        refusals.append(PREDICTED_IS_NOT_VERIFIED)
        notes.append("d_verified equals the prediction with no actual: predicted value became verified value")

    # R3: a numeric zero is an assertion — it needs establishment.
    if isinstance(d_verified, (int, float)) and d_verified == 0:
        if interp not in ZERO_INTERPRETATIONS:
            refusals.append(ZERO_WITHOUT_ESTABLISHMENT)
            notes.append("zero asserted without a zero interpretation (TRUE_ZERO/BASELINE_ZERO/"
                         "PRACTICALLY_NEUTRAL/ROUNDED_DISPLAY_ZERO)")
        elif not evidence_refs:
            refusals.append(ZERO_WITHOUT_ESTABLISHMENT)
            notes.append("zero asserted without evidence refs")

    # R4: practical neutrality needs its declared, versioned tolerance on the receipt.
    if interp == PRACTICALLY_NEUTRAL and not _epsilon_declared(epsilon):
        refusals.append(PRACTICAL_NEUTRALITY_NEEDS_EPSILON)
        notes.append("PRACTICALLY_NEUTRAL without a declared, versioned, justified epsilon")

    # R5: unknown-family interpretations must not carry a verified value.
    if interp in NONZERO_UNKNOWN_INTERPRETATIONS and d_verified is not None:
        refusals.append(INTERPRETATION_VALUE_MISMATCH)
        notes.append("interpretation %s is not a zero; it must not carry d_verified" % interp)

    # R6: rounded display preserves the raw value; the raw governs.
    if interp == ROUNDED_DISPLAY_ZERO:
        raw = r.get("delta_v_actual_raw", r.get("raw_value"))
        if raw is None or raw == 0:
            refusals.append(ROUNDED_ZERO_NEEDS_RAW)
            notes.append("ROUNDED_DISPLAY_ZERO requires the stored nonzero raw value")
        else:
            notes.append("raw value preserved; raw governs over display")

    # R7: null discipline — the validator never coerces; it only checks.
    if actual is None and d_verified is None:
        notes.append("null discipline holds: not established stays null, never 0")

    return {"ok": not refusals, "refusals": refusals, "notes": notes}


def reconsider_prior(prior_receipt, new_evidence_refs, contradicts=False, delayed_harm=False):
    """Material new evidence triggers reconsideration — never a silent keep.

    Returns a reopened assessment; the prior PASS is never quietly retained.
    """
    if not contradicts and not delayed_harm:
        return {
            "reopened": False,
            "prior_verification": prior_receipt.get("verification"),
            "note": "new evidence does not contradict the prior result; no reopen required",
        }
    window = prior_receipt.get("observation_window") or {}
    interp = DELAYED if window.get("status") == "OPEN" else INCONCLUSIVE
    return {
        "reopened": True,
        "prior_verification": prior_receipt.get("verification"),
        "new_verification": "ESCALATE",
        "value_interpretation": interp,
        "new_evidence_refs": list(new_evidence_refs),
        "reason": "delayed-harm evidence contradicts an earlier PASS" if delayed_harm
                  else "material new evidence contradicts the prior result",
        "note": "prior result corrected/reopened, never silently retained",
    }


def annotate_historical(row):
    """Annotate historical UNASSESSED rows carrying placeholder zeros.

    History is preserved, never rewritten. The annotation explains the old zero
    meant 'unassessed', not 'measured zero'. Returns an annotated copy.
    """
    annotated = dict(row)
    assessment = row.get("assessment_state", row.get("assessment"))
    has_placeholder_zero = (
        row.get("d_verified") == 0 or row.get("delta_v_actual") == 0
    )
    if assessment in (None, "UNASSESSED") and has_placeholder_zero:
        annotated["value_interpretation"] = UNKNOWN
        annotated["historical_annotation"] = (
            "HISTORICAL_PLACEHOLDER_ZERO: recorded before value assessment existed; "
            "the zero meant 'unassessed', not 'measured zero'. History preserved; "
            "meaning annotated, never silently rewritten."
        )
    return annotated


def audit_null_discipline(source_text):
    """Scan source for null->0 coercion patterns on value fields.

    Returns a list of findings; a clean module returns []. This is the
    executable form of 'never silently replace null with 0': the coercion is
    detectable, not just prohibited.
    """
    import re

    patterns = [
        (r"\bor\s+0\b", "OR_ZERO_DEFAULT"),
        (r"\.get\(\s*[\"'](?:d_verified|delta_v_actual|delta_v_predicted)[\"']\s*,\s*0\s*\)",
         "GET_WITH_ZERO_DEFAULT"),
        (r"(?:d_verified|delta_v_actual)\s*=\s*(?:d_verified|delta_v_actual)\s+or\s+0",
         "VALUE_OR_ZERO"),
    ]
    findings = []
    for i, line in enumerate(source_text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for pat, code in patterns:
            if re.search(pat, line):
                findings.append({"line": i, "code": code, "text": stripped})
                break
    return findings


# What this does NOT claim: this module judges the classifications it is given;
# it does not perform measurements, run observation windows, or verify evidence
# itself. A TRUE_ZERO verdict is only as good as the deterministic proof cited.
# The law is PROPOSED — nothing here is ratified until Shawn ratifies it.
