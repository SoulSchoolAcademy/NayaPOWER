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
any of technical/plain_human/full_text present and non-blank, or any
other text field at/over PING_MAX_CHARS (300) chars. The voided record
is then checked as a consequential report: it can still pass, but only
by actually honoring the two layers.

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
  6. plain_human carries at least one plain-words signal (the law's own
     markers), AND reads like plain human words: abstraction density
     below MAX_ABSTRACTION. The wall measures DICTION — the register of
     the words — not word or sentence length. Choppy jargon built from
     short buzzwords ("synergy is key. We leverage core competencies.")
     sails past length-based readability scores while staying unreadable
     to a human; genuine plain writing with flowing sentences fails them.
     Flesch was disproved on live probes 2026-10-09 and removed. To beat
     the abstraction wall you must write in concrete, everyday words —
     which IS the law's demand ("like explaining to a child"). The exploit
     collapses into compliance.
  7. If full_text is provided, it must contain a TECHNICAL marker followed
     by a PLAIN-WORDS marker. Order is the law: technicals-first-then-literal.

HONEST BOUND (what this check provably does NOT do):
  - It proves PLAINNESS OF DICTION, not truthfulness. A plain-but-vacuous
    layer ("In other words, think of it like a car. For example, it
    drives.") passes the mechanics while explaining nothing.
  - It does not grade comprehension, intent, or whether the plain layer
    faithfully represents the technical layer.
  - High-stakes reports still need a human seat to actually read them.
The check is a cheap screen against laziness and decoration — missing
layer, verbatim copy, marker-free jargon, jargon wearing one plain-words
phrase as camouflage. It is not a comprehension test, and it never
claims to be.

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

# --- Hardening 2 (2026-10-09): the exempt carve-out is one-line pings only.
# Fields that ARE the consequential report shape. A ping never carries
# these; their presence means this is a report wearing a ping's label.
CONSEQUENTIAL_FIELDS = ("technical", "plain_human", "full_text")
# Other free-text payload fields a ping may legitimately carry — but only
# as a one-liner. At/over this length it is a report, not a ping.
# Judgment call, tested at the boundary (299 passes, 300 voids).
PING_MAX_CHARS = 300
PING_TEXT_FIELDS = (
    "title",
    "message",
    "body",
    "content",
    "note",
    "summary",
    "details",
    "description",
    "text",
)


def _exemption_voided_reason(record: dict) -> str | None:
    """Why the exempt-type carve-out is voided, or None for a genuine
    one-line ping. Content decides the path, not the label."""
    for field in CONSEQUENTIAL_FIELDS:
        val = record.get(field)
        if isinstance(val, str) and val.strip():
            return f"carries report field {field!r}"
    for field in PING_TEXT_FIELDS:
        val = record.get(field)
        if isinstance(val, str) and len(val) >= PING_MAX_CHARS:
            return (
                f"text field {field!r} is {len(val)} chars "
                f"(>= {PING_MAX_CHARS}) — a report, not a one-line ping"
            )
    return None


# --- Rewrite (2026-10-09): the plain-diction wall replaces Flesch.
# Round-2 hardening DISPROVED Flesch Reading Ease as the plain-words proxy
# on live probes: choppy jargon scored 54.7–62.8 (PASSES the old >= 50
# gate — short buzzwords are short words in short sentences) while
# genuinely plain human writing scored 41.6–47 (FAILS — flowing sentences
# with ordinary multi-syllable words). Flesch measures word/sentence
# LENGTH, but the law demands a REGISTER: concrete, everyday human words.
# The replacement measures abstraction density = (jargon-lexicon hits +
# nominalization hits) / words. Calibrated on the probe corpus
# (tools/protocol/probes/clarity_probes.json) 2026-10-09: honoring and
# bound probes measured 0.000, attacks measured 0.229–0.429. The wall sits
# between them with margin on both sides. Deterministic, no model; every
# hit is named in the result details, so the number has provenance.
MAX_ABSTRACTION = 0.10

# Corporate/consultant jargon and the techno-abstract register of the
# paraphrase attacks. Words that are never needed in plain human speech.
# Multi-word entries are matched as phrases. This list is the documented
# approximation — reviewable in the open, unlike a formula's hidden bias.
JARGON = {
    # corporate fluff
    "synergy", "synergies", "synergy-driven", "paradigm", "holistic",
    "robust", "scalable", "scalability", "granular", "granularity",
    "utilize", "utilizes", "utilized", "utilizing", "utilization",
    "facilitate", "facilitates", "facilitated", "facilitating",
    "facilitation", "bandwidth", "deliverable", "deliverables",
    "stakeholder", "stakeholders", "ecosystem", "ecosystems", "ideate",
    "ideation", "operationalize", "operationalization", "monetize",
    "incentivize", "incentivise", "impactful", "learnings", "uplevel",
    "cross-functional", "silo", "silos", "siloed", "unpack",
    "double-click", "kpi", "kpis", "okr", "okrs", "takeaway",
    "takeaways", "net-net", "thought leadership", "bleeding edge",
    "cutting edge", "game changer", "game-changer", "secret sauce",
    "pivot", "pivoting", "disruption", "disruptive",
    "leverage", "leverages", "leveraged", "leveraging",
    "optimize", "optimizes", "optimized", "optimizing", "optimization",
    "throughput",
    # techno-abstract register (the paraphrase-attack vocabulary)
    "propagation", "delegation", "retrieval", "redirection", "validation",
    "authorization", "authentication", "configuration", "reconfiguration",
    "traversal", "traverse", "traverses", "surrogate", "surrogates",
    "mechanism", "mechanisms", "subsystem", "subsystems", "endpoint",
    "endpoints", "infrastructure", "credential", "credentials",
    "continuity", "systemic", "necessitating", "initiative",
}

# Nominalization suffixes: abstract nouns built from verbs ("implementation"
# instead of "implement") are the fingerprint of the technical register in
# plain-words clothing. Plain everyday words that happen to end this way
# are excepted so ordinary speech never trips the wall. Entry rule: a word
# is excepted ONLY if it is genuinely ordinary in plain civic/business
# prose — never a corporate-abstraction term. Seeded from the suffix hits
# of real plain sentences (never guesswork): 2026-10-09, a re-validator
# measured a dense-but-plain sentence at 0.160 (false FAIL from
# government/payment/department/agreement); the exceptions below return it
# under the wall while the attack probes still fail.
NOMINAL_SUFFIXES = ("tion", "sion", "ment", "ance", "ence", "ity")
PLAIN_EXCEPTIONS = {
    "moment", "moments", "comment", "comments", "question", "questions",
    "station", "stations", "nation", "nations", "section", "sections",
    "sentence", "sentences", "evidence", "presence", "science", "silence",
    "patience", "distance", "distances", "audience", "instance",
    "instances", "experience", "experiences", "difference", "differences",
    "apartment", "apartments", "clarity", "explanation", "explanations",
    "quality", "community", "communities", "activity", "activities",
    "security", "priority", "priorities", "reality",
    # ordinary civic/business nominalizations (2026-10-09 audit):
    "government", "governments", "payment", "payments", "agreement",
    "agreements", "department", "departments", "statement", "statements",
    "development", "developments", "management", "treatment", "treatments",
    "movement", "movements", "settlement", "settlements", "improvement",
    "improvements", "arrangement", "arrangements",
}


def _abstraction_hits(text: str) -> tuple[list[str], int]:
    """(named hits, word count). A hit is a JARGON word/phrase or a
    nominalization-suffix word not in PLAIN_EXCEPTIONS. Suffix hits are
    marked with a trailing '*' in the named list so the provenance shows
    which rule fired."""
    words = re.findall(r"[a-zA-Z']+", text.lower())
    hits: list[str] = []
    for w in words:
        if w in JARGON:
            hits.append(w)
        elif (
            w not in PLAIN_EXCEPTIONS
            and any(w.endswith(s) and len(w) > len(s) + 2
                    for s in NOMINAL_SUFFIXES)
        ):
            hits.append(w + "*")
    # multi-word jargon phrases: match on normalized spacing
    norm = " " + re.sub(r"[^a-z0-9 ]+", " ", text.lower()) + " "
    for j in JARGON:
        if " " in j and f" {j} " in norm:
            hits.append(j)
    return hits, len(words)


def _abstraction_density(text: str) -> tuple[float, list[str]]:
    """Abstraction density of the text: hits per word. Higher = more jargon."""
    hits, n_words = _abstraction_hits(text)
    if n_words == 0:
        return 0.0, hits
    return len(hits) / n_words, hits


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

    # Plain-diction wall: the layer must READ like plain human words, not
    # just wear one plain-words phrase as camouflage. Sprinkling "in other
    # words" into jargon, paraphrasing the jargon, or chopping the jargon
    # into short buzzword sentences all keep the abstract register — the
    # abstraction density stays high. Beating the wall requires writing in
    # concrete, everyday words: the exploit collapses into compliance.
    # (Honest bound: this proves plainness of diction, not truthfulness —
    # a plain-but-vacuous layer still passes.)
    density, hits = _abstraction_density(plain)
    details["plain_abstraction"] = round(density, 3)
    details["abstraction_hits"] = sorted(set(hits))
    if density >= MAX_ABSTRACTION:
        shown = ", ".join(sorted(set(hits))[:8])
        return fail(
            f"{title}: plain_human reads like jargon, not plain human words "
            f"(abstraction density {density:.2f} >= {MAX_ABSTRACTION:g}; "
            f"hits: {shown}) — it may carry a plain-words marker, but it "
            "still speaks in abstractions. Plain human words, like "
            "explaining to a child: concrete, everyday words.",
            details,
        )
    reasons.append(
        f"plain layer reads like human words (abstraction {density:.3f})"
    )

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
