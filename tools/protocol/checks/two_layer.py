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

The carve-out is NARROW: it covers one-line pings only. A record that
carries substantive consequential content VOIDS the exemption — content
decides the path, not the label (a relabel is not a rule). Substantive =
any report-shaped field present and non-blank (technical, plain_human,
full_text, blocker_x, unblock_action — a one-line ping never carries
these), or PING_MAX_CHARS (300) total chars of text accounted IN
AGGREGATE across ALL fields, whatever their names or types: splitting
text across fields cannot dodge the accounting, and non-str payloads
(lists, nested dicts) count as content. The voided record is then
checked as a consequential report: it can still pass, but only by
actually honoring the two layers.

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
  6. plain_human carries at least one plain-words signal (cheap screen —
     the law's own markers), AND reads short: Flesch Reading Ease >= 50.
     Sprinkling one signal phrase into jargon, or paraphrasing the jargon,
     keeps the long words and long sentences, so Flesch stays low and the
     wall kills the lazy attacks. HONEST LIMIT, measured live 2026-10-09:
     Flesch rewards SHORTNESS, not plainness — choppy jargon in short
     fragments scores 62.8 and passes, while a genuine flowing explanation
     that must name technical things scores 46-47 and fails. No Flesch
     threshold separates the two (the bands overlap), so this wall is a
     laziness screen, not a plainness test. See HONEST BOUND below.
  7. If full_text is provided, it must contain a TECHNICAL marker followed
     by a PLAIN-WORDS marker. Order is the law: technicals-first-then-literal.

HONEST BOUND (what this check provably does NOT do):
  - It proves READABILITY, not truthfulness. A readable-but-vacuous layer
    ("In other words, think of it like a car. For example, it drives.")
    passes the mechanics while explaining nothing.
  - JARGON-READABLE PASSES (admitted 2026-10-09, measured live by the
    independent re-validator): choppy jargon in short fragments
    ("In other words: the CSI driver choked. PVs stuck. Kubelet flapped.
    Restarts looped. Nodes drained.") scores Flesch 62.8 and PASSES.
    Flesch measures short words in short sentences — shortness, not
    plainness. No threshold on this axis separates jargon-short from
    plain-long; the bands overlap.
  - FALSE NEGATIVES EXIST (admitted 2026-10-09, measured live): a genuine
    plain explanation that must name technical things, written in flowing
    sentences, scores 46-47 and FAILS at threshold 50 — including the
    prior round's own honoring fixture at 46.1. Real two-layer reports on
    #1354 (n=6, 2026-10-09) score Flesch 62.8-73.6 and clear the wall with
    margin; the wall is calibrated for real reports, not against every
    genuine sentence shape.
  - It does not grade comprehension, intent, or whether the plain layer
    faithfully represents the technical layer.
  - High-stakes reports still need a human seat to actually read them.
The check is a cheap screen against laziness and decoration — missing
layer, verbatim copy, marker-free jargon, jargon wearing one plain-words
phrase as camouflage. It is not a comprehension test, and it never
claims to be. It does not claim to be a plainness test either.

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

# --- Hardening 2 (2026-10-09) + Round 2 (2026-10-09): the exempt
# carve-out is one-line pings only, and CONTENT DECIDES — accounted in
# aggregate, not per enumerated field (round-1's per-field list left
# three same-class residuals: split-across-fields, non-str payloads,
# uncovered report-shaped fields).
#
# Fields that ARE the consequential report shape. A one-line ping never
# carries these; their non-blank presence voids the exemption on sight.
REPORT_SHAPED_FIELDS = (
    "technical",
    "plain_human",
    "full_text",
    "blocker_x",
    "unblock_action",
)
# Everything else is content-accounted IN AGGREGATE across ALL fields,
# whatever their names: str or nested containers (a 600-word list payload
# is content, not a type loophole; dict keys count too). Non-text scalars
# (numbers, bools, None) carry no prose and are not counted. The
# report_type label itself is not content.
# At/over PING_MAX_CHARS total chars it is a report, not a one-line ping —
# spreading 400 chars across two fields cannot dodge the accounting.
# Judgment call, tested at the boundary (299 total chars passes, 300 voids).
PING_MAX_CHARS = 300


def _content_chars(value) -> int:
    """Text chars in a value, recursing into containers."""
    if isinstance(value, str):
        return len(value)
    if isinstance(value, dict):
        return sum(_content_chars(k) + _content_chars(v)
                   for k, v in value.items())
    if isinstance(value, (list, tuple, set, frozenset)):
        return sum(_content_chars(v) for v in value)
    return 0


def _aggregate_content(record: dict) -> tuple[int, list[tuple[str, int]]]:
    """(total content chars, per-field breakdown) over every field except
    the report_type label — largest contributor first."""
    breakdown: list[tuple[str, int]] = []
    total = 0
    for key, val in record.items():
        if key == "report_type":
            continue
        n = _content_chars(val)
        total += n
        if n:
            breakdown.append((str(key), n))
    breakdown.sort(key=lambda kv: kv[1], reverse=True)
    return total, breakdown


def _exemption_voided_reason(record: dict) -> str | None:
    """Why the exempt-type carve-out is voided, or None for a genuine
    one-line ping. Content decides the path, not the label — and content
    is accounted IN AGGREGATE, so neither splitting text across fields
    nor hiding it in non-str payloads changes the verdict."""
    for field in REPORT_SHAPED_FIELDS:
        val = record.get(field)
        if isinstance(val, str) and val.strip():
            return (
                f"carries report field {field!r} — a one-line ping never "
                "carries one"
            )
    total, breakdown = _aggregate_content(record)
    if total >= PING_MAX_CHARS:
        top = ", ".join(f"{k}={v}" for k, v in breakdown[:3])
        return (
            f"carries {total} chars of text across {len(breakdown)} "
            f"field(s) (>= {PING_MAX_CHARS}) — a report, not a one-line "
            f"ping (largest: {top})"
        )
    return None


# --- Hardening 3 (2026-10-09) + Round 2 (2026-10-09): the shortness wall.
# Minimum Flesch Reading Ease for the plain-words layer.
# What it IS: a laziness screen. The 8 battery attacks (signal phrase
# sprinkled into jargon, paraphrased jargon) measured -0-43 and all die
# here; real two-layer reports on #1354 (n=6, 2026-10-09) measured
# 62.8-73.6 and clear 50 with margin.
# What it IS NOT: a plainness test. Choppy jargon in short fragments
# measured 62.8 live and PASSES — Flesch rewards shortness, not plainness.
# A genuine flowing explanation that must name technical things measured
# 46-47 and FAILS (false negatives, admitted). The bands overlap, so no
# threshold on this axis separates jargon-short from plain-long: 50 is the
# documented judgment call that kills the lazy attacks while clearing
# real reports, not a wall against all jargon.
MIN_FLESCH = 50.0


def _syllables(word: str) -> int:
    word = word.lower().strip("'")
    if not word:
        return 0
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e"):
        count -= 1
    if word.endswith("le") and len(word) > 2 and word[-3] not in "aeiouy":
        count += 1
    return max(count, 1)


def _flesch_reading_ease(text: str) -> float:
    """Flesch Reading Ease: 206.835 - 1.015*(words/sentences)
    - 84.6*(syllables/words). Higher = plainer. Deterministic, no word
    list, no model — short sentences in short common words score high."""
    words = re.findall(r"[a-zA-Z']+", text)
    sentences = [s for s in re.split(r"[.!?;]+", text) if s.strip()]
    n_words = len(words)
    n_sent = max(len(sentences), 1)
    n_syl = sum(_syllables(w) for w in words)
    if n_words == 0:
        return 0.0
    return 206.835 - 1.015 * (n_words / n_sent) - 84.6 * (n_syl / n_words)


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
        void_reason = _exemption_voided_reason(record)
        if void_reason is None:
            reasons.append(
                f"{title}: {rtype!r} is explicitly exempt — one-line pings "
                "stay cheap, the law deliberately skips them"
            )
            return result(True, reasons, details)
        # Exemption voided: a relabel is not a rule. The record is checked
        # as a consequential report — it can still pass, but only by
        # actually honoring the two layers.
        reasons.append(
            f"{title}: labeled {rtype!r} but {void_reason} — the one-line-ping "
            "exemption is voided; content decides the path, not the label"
        )
        details["exemption_voided"] = void_reason
        # fall through to the consequential path below

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

    # Shortness wall: the layer must read SHORT, not just wear one
    # plain-words phrase as camouflage. Sprinkling "in other words" into
    # jargon, or paraphrasing the jargon, keeps the long words and long
    # sentences — Flesch stays low and the lazy attack dies. Honest bounds
    # (measured live 2026-10-09, pinned in tests): choppy jargon in short
    # fragments scores 62.8 and PASSES — Flesch rewards shortness, not
    # plainness; and a genuine flowing explanation can score 46-47 and
    # FAIL. This wall kills laziness, not all jargon.
    ease = _flesch_reading_ease(plain)
    details["plain_flesch"] = round(ease, 1)
    if ease < MIN_FLESCH:
        return fail(
            f"{title}: plain_human reads at Flesch {ease:.1f} "
            f"(< {MIN_FLESCH:g}) — it may carry a plain-words marker, but "
            "it still reads like technicals. Plain human words, like "
            "explaining to a child: short sentences, short common words.",
            details,
        )
    reasons.append(f"plain layer reads plain (Flesch {ease:.1f})")

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
