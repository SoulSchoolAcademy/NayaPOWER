#!/usr/bin/env python3
"""The Falsification-First Verification Standard (cold-retest lane, 2026-10-09).

"A verifier must arrive trying to break the claim — 'I came to falsify
and could not' outranks 'I checked the builder's log.'"

Re-running the builder's battery and calling it verification is the
laziest exploit in the verification lane: the verifier's hands never
touch the claim. This check enforces the attack posture as a matter of
record shape:

  1. The verification report must list the verifier's OWN attack inputs.
  2. Each attack must be distinct from the builder's battery — an attack
     that is the builder's own test wearing a new label is a relabel,
     and a relabel is not a rule.
  3. Each attack carries an honest outcome: "held" (the claim survived)
     or "broke" (the claim did not). Unknown/blank outcomes fail closed.
  4. If any attack broke the claim, the report's verdict cannot be
     "verified"/"pass" — contradiction fails closed.
  5. If NO attacks were tried, the report may still pass shape — but only
     with an explicit honest declaration (attacks_tried: false + reason).
     It passes as "declared, not falsification-tested", and the result
     says so plainly.

Record:
    {
      "claim": "what is being verified",
      "verifier": "seat or agent name",
      "builder_battery": ["test_login_happy_path", "attack: oversized input"],
      "verifier_attacks": [
        {"input": "null bytes in the name field", "outcome": "held"},
        {"input": "1MB payload at the boundary", "outcome": "broke"}
      ],
      "verdict": "not-verified",
      "attacks_tried": true
    }

HONEST BOUND (what this check provably does NOT do):
  - It proves the verifier ATTEMPTED falsification with inputs of their
    own — not that the attacks were competent, complete, or adversarial
    enough to deserve the claim's trust.
  - Distinctness is skeleton distinctness (confusable-skeleton fold —
    NFKC + casefold + diacritic-strip + Cyrillic/Greek lookalike fold —
    then case, punctuation, and whitespace folded), not semantic
    distinctness. A paraphrased copy of a builder test passes the
    mechanics; a relabel no human reader can distinguish from the
    builder's battery does not. Digit/letter confusables (o/0, l/1) are
    deliberately NOT folded — distinguishable in code font.
  - "I came to falsify and could not" is an honesty standard for the
    REPORT. Whether the claim is true still needs a human seat to read
    the attacks.

Usage:
    python3 tools/protocol/checks/falsification_first.py \\
        --record '{"claim": "...", "verifier_attacks": [...]}' [--json]
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402
from checks.shape_closed import validate_shape  # noqa: E402

LAW_ID = "FALSIFICATION-FIRST-LAW"
VALID_OUTCOMES = {"held", "broke"}
PASSING_VERDICTS = {"verified", "pass", "proven", "confirmed"}

# Confusable skeleton (residual hardened 2026-10-09): Cyrillic and Greek
# lookalikes fold to their Latin twins — the batch-3 Cyrillic family,
# applied here to the identity machinery. NFKC (below) already folds
# full-width, circled, mathematical-bold, ligatures, roman numerals and
# superscripts; casefold + diacritic-strip handle ß/İ/é-class relabels.
# This table covers only letter→letter confusables: digit/letter pairs
# (o/0, l/1) are NOT folded — they stay distinguishable in code font,
# and folding them would merge genuinely different identifiers.
_CONFUSABLE_FOLD = {
    # Cyrillic → Latin
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
    "у": "y", "і": "i", "ј": "j", "ѕ": "s", "һ": "h",
    "ԛ": "q", "ԝ": "w", "ԁ": "d", "ӏ": "l",
    # Greek → Latin
    "α": "a", "ε": "e", "ο": "o", "ρ": "p", "ι": "i",
    "κ": "k", "ν": "v", "τ": "t", "χ": "x", "υ": "u",
    # dotless i (casefold("I") → "ı"; without this, ALL-CAPS
    # canonicals would normalize apart from their lowercase twins)
    "ı": "i",
}


def _skeleton(text: str) -> str:
    """Reduce text to its confusable skeleton: what a human READS.

    NFKC (compatibility decomposition) → casefold → strip combining
    marks → explicit Cyrillic/Greek confusable fold. Two labels with
    the same skeleton look the same to the reader; treating them as
    distinct is the relabel exploit.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.casefold()
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    return "".join(_CONFUSABLE_FOLD.get(c, c) for c in text)


def _norm(text: str) -> str:
    """Fold to the confusable skeleton, then case/punct/whitespace.

    Punctuation is FOLDED to a common separator (one space), never
    deleted. Deleting separators made 'test_x' and 'test x' normalize
    apart — a verifier could copy the builder's snake_case battery,
    swap separators for spaces (the most natural relabel there is),
    and pass it off as their own attack. Folding closes that lane;
    genuinely different inputs still normalize apart.

    The skeleton step (new) closes the homograph lane: full-width,
    circled, math-bold, ligature, roman-numeral, superscript, ß/İ/
    diacritic, Cyrillic and Greek relabels all fold to the same
    skeleton as their canonical twin. What the human reads is the
    identity — a relabel the reader cannot distinguish from the
    builder's battery is not a new attack.
    """
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", _skeleton(text))).strip()


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": LAW_ID, "law_status": "RATIFIED"}
    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    ok, shape_reasons = validate_shape(
        record,
        {
            "required": ["claim", "verifier", "verdict", "attacks_tried"],
            "types": {
                "claim": "str",
                "verifier": "str",
                "verdict": "str",
                "attacks_tried": "bool",
                "builder_battery": "list",
                "verifier_attacks": "list",
            },
            "non_empty": ["claim", "verifier", "verdict"],
        },
    )
    if not ok:
        return fail(
            "shape failure: " + shape_reasons[0]
            + " — a verification report with no claim, no verifier, "
            "no verdict, or no attack posture is not a verification",
            details,
        )
    reasons.extend(shape_reasons)

    claim = str(record["claim"]).strip()
    verifier = str(record["verifier"]).strip()
    verdict = str(record["verdict"]).strip().lower()
    attacks_tried = bool(record["attacks_tried"])
    builder_battery = [str(b) for b in (record.get("builder_battery") or [])]
    attacks = record.get("verifier_attacks") or []
    details["verifier"] = verifier
    details["attacks_tried"] = attacks_tried

    # The honest-declaration path: no attacks tried is allowed ONLY when
    # declared explicitly with a reason. It passes shape as declared —
    # never as falsification-tested.
    if not attacks_tried:
        reason = str(record.get("no_attacks_reason") or "").strip()
        if not reason:
            return fail(
                f"{verifier}: attacks_tried is false with no reason given — "
                "a verifier who never tried to break the claim must say why, "
                "plainly. 'I checked the builder's log' is not a reason.",
                details,
            )
        details["strength"] = "declared-not-falsification-tested"
        reasons.append(
            "honest declaration: no falsification attacks were tried — "
            f"reason recorded ({reason[:120]}). This is NOT a falsification "
            "test; it is a declared gap."
        )
        return result(True, reasons, details)

    # Attacks were claimed: there must actually be some.
    if not attacks:
        return fail(
            f"{verifier}: attacks_tried is true but verifier_attacks is "
            "empty — claiming to falsify with no attack inputs is the "
            "laziest exploit in the lane",
            details,
        )

    builder_norms = {_norm(b) for b in builder_battery if _norm(b)}
    broke_any = False
    for i, attack in enumerate(attacks):
        tag = f"attack[{i}]"
        if not isinstance(attack, dict):
            return fail(
                f"{tag} is not an object — every attack must name its "
                "input and its outcome",
                details,
            )
        attack_input = str(attack.get("input") or "").strip()
        outcome = str(attack.get("outcome") or "").strip().lower()
        if len(attack_input) < 8:
            return fail(
                f"{tag} names no real attack input — an attack without an "
                "input is decoration",
                details,
            )
        if outcome not in VALID_OUTCOMES:
            return fail(
                f"{tag} outcome {attack.get('outcome')!r} is not honest — "
                "each attack must end 'held' (the claim survived) or "
                "'broke' (the claim did not). Unknown outcomes fail closed",
                details,
            )
        # The relabel exploit: the builder's own battery wearing a new label.
        if _norm(attack_input) in builder_norms:
            return fail(
                f"{tag} input is a copy of the builder's battery "
                f"({_norm(attack_input)[:60]!r}) — re-running the builder's "
                "own test is not falsification. A relabel is not a rule.",
                details,
            )
        if outcome == "broke":
            broke_any = True
    details["attacks_run"] = len(attacks)
    details["attacks_broke"] = broke_any
    reasons.append(
        f"{len(attacks)} own attack input(s) recorded, each distinct from "
        f"the builder's battery of {len(builder_battery)}"
    )

    # Contradiction fails closed: a broken claim cannot be "verified".
    if broke_any and verdict in PASSING_VERDICTS:
        return fail(
            f"contradiction: at least one attack BROKE the claim, yet the "
            f"verdict is {verdict!r} — a falsified claim cannot be "
            "declared verified",
            details,
        )
    if broke_any:
        reasons.append(
            "verdict is honestly not-verified: an attack broke the claim "
            "and the report says so"
        )
        details["strength"] = "falsification-attempted-claim-broken"
    else:
        reasons.append(
            f"'I came to falsify and could not': {len(attacks)} attack(s), "
            "all held"
        )
        details["strength"] = "falsification-attempted-all-held"

    reasons.append(
        f"Falsification-First honored on {claim[:80]!r}: the verifier "
        "arrived trying to break it"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Falsification-First Verification Standard check"
    )
    parser.add_argument("--record", required=True,
                        help="JSON verification record (or @file)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": LAW_ID}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
