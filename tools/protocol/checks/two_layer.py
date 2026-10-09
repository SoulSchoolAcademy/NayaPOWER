#!/usr/bin/env python3
"""The Two-Layer Communication Law (Shawn, 2026-10-09 — his explicit ask).

"Never hand Shawn technicals alone. He should never have to decode.
Technicals-first-then-literal is the format."

Every CONSEQUENTIAL update comes in TWO layers, back to back:
  1. THE TECHNICAL: what happened, honestly, real terms.
  2. LITERALLY WHAT I'M SAYING: what it means in plain human words —
     like explaining to a child. Allegories welcome.

Consequential types (the law applies — these are things Shawn reads):
  verdict, completion, deliverable_report, briefing, decision_receipt,
  scorecard, blocker_post.

Exempt types (one-line pings stay cheap — the law deliberately skips):
  status_ping, ack, coordination_note.

Anything else fails CLOSED: an unknown report_type is never silently
defaulted to exempt. (Fail-closed on shape, not just syntax — the
validator's meta-law.)

Record:
    {
      "report_type": "deliverable_report",
      "title": "<short title>",
      "technical": "<the technical layer, real terms>",
      "plain_human": "<the plain-words layer, human words>",
      "full_text": "(optional) the rendered report; layer marker order is enforced here",
      "audience": "shawn",
      "seat": "naya-5"
    }

Checks (fail-closed: shape first via shape_closed.validate_shape):
  1. report_type present, known. Unknown -> FAIL.
  2. Exempt type -> PASS (layers not required).
  3. technical present, non-empty, >= 40 chars.
  4. plain_human present, non-empty, >= 40 chars.
  5. plain_human is not a copy of technical (token Jaccard < 0.7).
     Copy-pasting the jargon into the second field is the laziest exploit.
  6. plain_human carries at least one plain-words signal. Heuristic, documented
     as approximate — but fail-closed: no signal, no pass.
  7. If full_text is provided, it must contain a TECHNICAL marker followed
     by a PLAIN-WORDS marker. Order is the law: technicals-first-then-literal.

LITERAL-FIRST REFINEMENT (Shawn, 2026-10-09 — the law's root-cause fix):
  "Write the literal layer FIRST. Think in plain human words before the
   technicals." The literal layer is for HIM, not for the log — so it must
   contain NO machine exhaust, ever:
  8. plain_human contains no SHA-like hex ([0-9a-f]{7,40} with at least one
     hex letter — pure numbers stay legal), no #NNNN PR/issue refs, no
     test-count patterns (NNN passed/failed/skipped, N/M ratios), and no
     CI-state markers (CI, GitHub Actions, green/red build language).
     A SHA in the literal layer is the law's named failure mode: "speak it
     in words that I can't understand."
  9. If full_text is provided, the literal portion (after the plain-words
     marker) gets the same purity screen — the rule is about the LAYER,
     wherever it appears, not the field.

HONEST BOUND (what this check provably does NOT do):
  - It proves the literal layer is free of machine exhaust, not that it is
    true, complete, or faithful to the technical layer.
  - Readability (Flesch >= 50, checks 5-6) plus purity (checks 8-9) is a
    cheap screen against laziness and decoration, not a comprehension test.

Usage:
    python3 tools/protocol/checks/two_layer.py \\
        --record '{"report_type": "deliverable_report", ...}' [--json]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402
from checks.shape_closed import validate_shape  # noqa: E402

CONSEQUENTIAL = {
    "verdict",
    "completion",
    "deliverable_report",
    "briefing",
    "decision_receipt",
    "scorecard",
    "blocker_post",
}
EXEMPT = {"status_ping", "ack", "coordination_note"}
MIN_LAYER_CHARS = 40
MAX_JACCARD = 0.7

# Signals that the plain-words layer is actually plain. The law says
# "like explaining to a child — allegories welcome": plain speech leaves
# markers. This is a documented approximation, not a comprehension test —
# but absence fails closed.
PLAIN_SIGNALS = [
    "in other words",
    "in plain words",
    "literally what i'm saying",
    "what this means",
    "what i'm saying",
    "think of it",
    "imagine",
    "like a ",
    "like the ",
    "picture this",
    "for example",
    "basically",
    "simply put",
    "in plain terms",
    "means that",
    "an analogy",
    "plainly",
]

TECH_MARKERS = ["the technical", "technical:"]
PLAIN_MARKERS = [
    "literally what i'm saying",
    "in plain words",
    "plain words:",
    "plainly put",
]

# LITERAL-FIRST refinement (Shawn, 2026-10-09): the literal layer is written
# for HIM, not the log — no machine exhaust, ever. Each pattern is a named
# failure mode from his correction. The SHA pattern requires at least one
# hex letter so plain numbers stay legal; the law bans SHAs, not counts.
LITERAL_PURITY_PATTERNS = [
    (
        "sha_like",
        re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b"),
        "SHA-like hex string",
    ),
    (
        "pr_ref",
        re.compile(r"(?:#\d{3,}|PR[\s#-]*\d+|pull request\s*#?\s*\d+|issue\s*#\s*\d+)", re.IGNORECASE),
        "PR/issue number",
    ),
    (
        "test_count",
        re.compile(
            r"\b\d+\s*(?:passed|failed|skipped|errored|passing|failing)\b"
            r"|\b\d+\s+tests?\s+(?:passed|failed|skipped|errored|passing|failing)\b"
            r"|\b\d+\s*/\s*\d+\b"
            r"|\b\d+\s+of\s+\d+\s+tests?\b",
            re.IGNORECASE,
        ),
        "test count",
    ),
    (
        "ci_state",
        re.compile(
            r"\bCI\b"
            r"|github actions"
            r"|\b(?:green|red)\s+(?:build|suite|pipeline|CI)\b"
            r"|\bbuild\s+(?:passed|failed|green|red)\b",
            re.IGNORECASE,
        ),
        "CI-state marker",
    ),
]


def _literal_impurities(text: str) -> list[str]:
    """Return human-readable hits of machine exhaust in the literal layer."""
    hits: list[str] = []
    for _name, pattern, label in LITERAL_PURITY_PATTERNS:
        m = pattern.search(text)
        if m:
            hits.append(f"{label} {m.group(0)!r}")
    return hits


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9']+", text.lower()))


def _jaccard(a: str, b: str) -> float:
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    return len(ta & tb) / len(ta | tb)


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "TWO-LAYER-LAW", "law_status": "RATIFIED"}
    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    # Shape first: report_type must exist, be a str, and be KNOWN.
    ok, shape_reasons = validate_shape(
        record,
        {
            "required": ["report_type"],
            "types": {"report_type": "str"},
            "non_empty": ["report_type"],
            "allowed": {"report_type": sorted(CONSEQUENTIAL | EXEMPT)},
        },
    )
    if not ok:
        for r in shape_reasons:
            if "ABSENT" in r or "not in" in r or "empty" in r or "None" in r:
                details["shape_failed"] = True
        return fail(
            "shape failure: " + shape_reasons[0]
            + " — absence is the cheapest exploit; unknown types fail closed",
            details,
        )
    reasons.extend(shape_reasons)

    rtype = str(record.get("report_type")).strip().lower()
    title = str(record.get("title") or "(untitled)").strip()
    details["report_type"] = rtype
    details["title"] = title

    if rtype in EXEMPT:
        reasons.append(
            f"{title}: {rtype!r} is explicitly exempt — one-line pings "
            "stay cheap, the law deliberately skips them"
        )
        return result(True, reasons, details)

    # Consequential: both layers are required, with substance.
    ok, layer_reasons = validate_shape(
        record,
        {
            "required": ["technical", "plain_human"],
            "types": {"technical": "str", "plain_human": "str"},
            "non_empty": ["technical", "plain_human"],
            "min_length": {
                "technical": MIN_LAYER_CHARS,
                "plain_human": MIN_LAYER_CHARS,
            },
        },
    )
    if not ok:
        return fail(
            f"{title}: consequential {rtype!r} report with a missing, empty, "
            "or too-thin layer — " + layer_reasons[0]
            + ". Never hand Shawn technicals alone.",
            details,
        )
    reasons.append("technical and plain_human layers present with substance")

    technical = str(record["technical"])
    plain = str(record["plain_human"])

    # The copy-paste exploit: same jargon, both fields.
    similarity = _jaccard(technical, plain)
    if similarity >= MAX_JACCARD:
        return fail(
            f"{title}: plain_human is a near-copy of technical "
            f"(token Jaccard {similarity:.2f} >= {MAX_JACCARD}) — "
            "pasting the jargon into the second field is not plain words",
            details,
        )
    reasons.append(f"plain layer is genuinely distinct (Jaccard {similarity:.2f})")

    # Plain-words signal: the layer must sound like plain speech.
    lowered = plain.lower()
    if not any(sig in lowered for sig in PLAIN_SIGNALS):
        return fail(
            f"{title}: plain_human carries no plain-words signal — it reads "
            "like more technicals. The law demands plain human words, like "
            "explaining to a child; allegories welcome",
            details,
        )
    reasons.append("plain_human carries plain-words signal")

    # Order, when the rendered text is provided: technicals FIRST, then literal.
    full = str(record.get("full_text") or "").strip()
    if full:
        low = full.lower()
        tech_pos = min(
            (low.find(m) for m in TECH_MARKERS if m in low), default=-1
        )
        plain_pos = min(
            (low.find(m) for m in PLAIN_MARKERS if m in low), default=-1
        )
        if tech_pos < 0:
            return fail(
                f"{title}: full_text has no TECHNICAL layer marker — "
                "the technical layer must be labeled and present",
                details,
            )
        if plain_pos < 0:
            return fail(
                f"{title}: full_text has no plain-words marker "
                "('literally what i'm saying' / 'in plain words') — "
                "the second layer must be labeled and present",
                details,
            )
        if tech_pos > plain_pos:
            return fail(
                f"{title}: plain-words layer appears BEFORE the technical "
                "layer — the law is technicals-first-then-literal, back to back",
                details,
            )
        reasons.append("full_text: TECHNICAL marker precedes plain-words marker")

        # Literal-first refinement, check 9: the literal PORTION of full_text
        # gets the same purity screen. The rule is about the layer, wherever
        # it appears — not the field.
        literal_portion = full[plain_pos:].strip()
        full_impurities = _literal_impurities(literal_portion)
        if full_impurities:
            return fail(
                f"{title}: full_text's literal portion carries machine "
                f"exhaust ({'; '.join(full_impurities)}) — the literal "
                "layer is written for Shawn, not the log. Write it first, "
                "in plain human words.",
                details,
            )
        reasons.append("full_text: literal portion free of machine exhaust")

    # Literal-first refinement, check 8: no machine exhaust in plain_human.
    # This is the named failure mode — "speak it in words I can't understand."
    impurities = _literal_impurities(plain)
    if impurities:
        return fail(
            f"{title}: plain_human carries machine exhaust "
            f"({'; '.join(impurities)}) — the literal layer is for Shawn, "
            "not the log. Think in plain human words FIRST, then attach "
            "technicals as the evidence appendix.",
            details,
        )
    reasons.append("plain_human: literal layer free of machine exhaust")

    reasons.append(
        f"Two-Layer Law honored on {rtype!r}: technicals first, "
        "literally-what-I'm-saying second"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Two-Layer Communication Law check")
    parser.add_argument("--record", required=True,
                        help="JSON report record (or @file)")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "TWO-LAYER-LAW"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
