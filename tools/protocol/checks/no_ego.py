#!/usr/bin/env python3
"""SN-NO-EGO — No-Ego Optimization.

"Decisions are not about what any individual wants. The standard is the
most valuable intelligent thing to do, determined by logic and math.
Optimization function: VALUE x INTELLIGENCE, maximized per moment."

This is the EGO half of decision governance:
  - decision_log.py holds the math half (options, scores, winner == argmax)
  - decision_receipt.py holds the report half (receipt format, evidence named)
  - wisest_choice.py holds the judgment contract (objective, basis type)
  - THIS module holds the ego half: the decider's want is not a basis.

A decision fails this gate when the record shows the decider substituted
personal preference for the math — ego-marker language in the rationale,
an override of the math's winner with no evidence, or a decision made
with no math consulted and no reason given for skipping it.

Input record:
    {
      "decision": "<what was decided>",
      "decider": "<seat or agent id>",
      "rationale": "<free-text reasoning>",
      "math_winner": "<option id the math picked>" | null,
      "chosen": "<option id actually chosen>",
      "override_evidence": "<evidence for overriding the math>" | "",
      "no_math_reason": "<why the math was not consulted>" | ""
    }

Checks:
  1. decision and decider present and non-empty — anonymous decisions are void.
  2. Rationale carries no ego markers — first-person preference signals
     ("I prefer", "my gut", "trust me", ...) fail, naming the matched
     phrases. Rewrite in evidence terms or cite the math.
  3. Math followed or honestly overridden: when math_winner is given,
     chosen must equal math_winner, or override_evidence must be non-empty
     and itself ego-marker-free. An override with no evidence is an ego
     override.
  4. Math consulted or honestly excused: when math_winner is null,
     no_math_reason must be non-empty — deciding without the math and
     without saying why is deciding on vibes.

Fail-closed: any malformed record fails with a specific reason.

Usage:
    python3 tools/protocol/checks/no_ego.py --record '{"decision": "...", ...}' [--json]
    python3 tools/protocol/checks/no_ego.py --record @record.json [--json]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

# First-person preference signals: the decider's want stated as the basis.
# Tight by design — honest uncertainty ("in my opinion", "I believe the
# evidence shows") is NOT here; only want-as-basis phrasing is.
EGO_MARKERS = [
    "i prefer",
    "i want",
    "i'd rather",
    "i would rather",
    "my gut",
    "gut feeling",
    "gut feel",
    "trust me",
    "just trust",
    "because i said so",
    "my call",
    "i feel like",
    "feels right",
    "i like this option",
    "i don't like",
    "i dont like",
]

_EGO_PATTERNS = [re.compile(r"\b" + re.escape(m) + r"\b") for m in EGO_MARKERS]


def find_ego_markers(text: str) -> list[str]:
    """Return the ego markers present in text (word-boundary matched)."""
    lowered = text.lower()
    return [m for m, p in zip(EGO_MARKERS, _EGO_PATTERNS) if p.search(lowered)]


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-NO-EGO"}
    subject = record.get("decision") or "(unnamed decision)"
    details["decision"] = subject

    if not _nonempty(record.get("decision")):
        return fail(f"{subject}: decision unnamed — nothing was decided", details)
    decider = record.get("decider")
    if not _nonempty(decider):
        return fail(f"{subject}: decider unnamed — anonymous decisions are void", details)
    details["decider"] = decider.strip()
    reasons.append(f"decider named: {decider.strip()}")

    rationale = record.get("rationale")
    if not isinstance(rationale, str):
        return fail(f"{subject}: rationale missing — a decision with no stated "
                    f"reasoning cannot be checked for ego", details)
    markers = find_ego_markers(rationale)
    if markers:
        details["ego_markers"] = markers
        return fail(
            f"{subject}: rationale states the decider's want as the basis "
            f"({', '.join(repr(m) for m in markers)}) — rewrite in evidence "
            f"terms or cite the math",
            details,
        )
    reasons.append("rationale carries no ego markers")

    math_winner = record.get("math_winner")
    chosen = record.get("chosen")
    if math_winner is not None:
        if not _nonempty(math_winner):
            return fail(f"{subject}: math_winner given but empty — name the "
                        f"math's winner or set it to null with a no_math_reason",
                        details)
        if not _nonempty(chosen):
            return fail(f"{subject}: chosen missing — the math picked "
                        f"{math_winner.strip()!r}; say what was chosen", details)
        details["math_winner"] = math_winner.strip()
        details["chosen"] = chosen.strip()
        if chosen.strip() != math_winner.strip():
            evidence = record.get("override_evidence")
            if not _nonempty(evidence):
                return fail(
                    f"{subject}: chose {chosen.strip()!r} over the math's winner "
                    f"{math_winner.strip()!r} with no override evidence — "
                    f"an override with no evidence is an ego override",
                    details,
                )
            ev_markers = find_ego_markers(evidence)
            if ev_markers:
                return fail(
                    f"{subject}: override evidence itself states the decider's "
                    f"want ({', '.join(repr(m) for m in ev_markers)}) — "
                    f"evidence, not preference",
                    details,
                )
            reasons.append(
                f"math overridden with evidence ({len(evidence.strip())} chars), "
                f"evidence ego-marker-free"
            )
        else:
            reasons.append(f"chosen == math's winner ({math_winner.strip()!r})")
    else:
        excuse = record.get("no_math_reason")
        if not _nonempty(excuse):
            return fail(
                f"{subject}: no math consulted (math_winner null) and no "
                f"no_math_reason given — deciding without the math and without "
                f"saying why is deciding on vibes",
                details,
            )
        reasons.append("math not consulted; reason stated")

    reasons.append(f"{subject}: no ego detected — the math (or evidence) decided")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-NO-EGO no-ego decision check")
    parser.add_argument("--record", required=True,
                        help="JSON decision record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-NO-EGO"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
