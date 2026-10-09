#!/usr/bin/env python3
"""The Decision Receipt Law (Shawn, 2026-10-09).

"A decision without homework is guessing, not autonomy. Be fully aware of
the decision: you know it's right because you did the math."

Report format: "I chose X. I looked at A, B, C. X won because [evidence].
This is what I did." The scorecard is the receipt; correctness is the job.
Decisive on clear winners, honest on close calls. If the winner isn't
clear or evidence is missing, say so plainly instead of bluffing.

This is the REPORT half of decision governance. decision_log.py holds the
math half (options, scores, winner == argmax, authority gates). This
module holds the receipt half: the record must carry the alternatives that
were looked at, the evidence that made the winner win, and the
plain-words receipt naming both. A decision with no named alternatives
and no winning evidence is guessing, not a decision.

Input record:
    {
      "decision": "<what was decided>",
      "chosen": "opt-c",
      "alternatives": [
        {"id": "opt-a", "description": "..."},
        {"id": "opt-b", "description": "..."},
        {"id": "opt-c", "description": "..."}
      ],
      "winning_evidence": "<the evidence that made the winner win>",
      "receipt": "I chose opt-c. I looked at opt-a, opt-b, opt-c. opt-c won because <evidence>.",
      "seat": "<deciding seat>",
      "close_call": false,
      "uncertainty_declared": false   # required true when close_call is true
    }

Checks:
  1. decision and seat present and non-empty (anonymous decisions are void).
  2. alternatives is a list of >= 2, each with a non-empty id and description.
     One option is not a decision; a decision without homework is guessing.
     Every id must be a REAL IDENTIFIER, not an ordinary English word —
     an id like "a" or "the" occurs naturally in any prose receipt, so the
     name-check in (5) would pass on a receipt that never names the option.
     Dictionary-word ids fail closed.
  3. chosen is non-empty and is one of the alternatives' ids.
  4. winning_evidence is non-empty — "X won because [evidence]". Missing
     evidence is not a receipt; say so plainly instead of bluffing.
  5. receipt is non-empty and names the chosen id and every alternative id
     (the receipt must say what was chosen AND what was looked at).
  6. If close_call is true, uncertainty_declared must be true —
     "honest on close calls".

Honest bound: the dictionary-word boundary is ORDINARY_WORDS below — a
word NOT in that list but still common in prose is a residual risk the
name-check cannot see. The list is the extension point: when a new
prose-natural word is observed slipping through, add it with its evidence
instead of weakening the check. The law's own template vocabulary
("I chose X. I looked at A, B, C. X won because [evidence]." → chose,
looked, evidence, x, b, c) has been audited and is covered.

Usage:
    python3 tools/protocol/checks/decision_receipt.py \
        --record '{"decision": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402


# Ordinary English words. An alternative id that IS one of these words
# defeats the receipt name-check: any prose receipt contains words like
# "a", "the", "it", "this" naturally, so a receipt that never names the
# option still passes. Ids must be real identifiers (opt-a, plan-2,
# north-route) — things a receipt must deliberately write, never things
# prose writes by accident.
#
# Template-vocabulary closure (2026-10-09): the law's own report template
# ("I chose X. I looked at A, B, C. X won because [evidence].") writes
# "chose", "looked", "evidence", "x", "b", "c" BY CONSTRUCTION — every
# receipt written in the template names those ids without naming any
# option. Ghost options with those ids passed the full check end-to-end.
# They are banned with the same force as "a" and "the". The check is
# full-string equality, so honest ids like "opt-a" never collide with
# the banned bare letters "a", "b", "c", "x".
ORDINARY_WORDS = frozenset("""
a an the
i me my mine we us our ours you your yours he him his she her hers
it its they them their theirs this that these those who whom whose which what
where when why how
of in on at to for with by from as into through during before after above
below between among against about under over off per via within without upon
across along around behind beyond near toward towards onto except
and but or nor so yet because although though if while whereas whether unless
until since than then
am is are was were be been being have has had having do does did doing
will would shall should may might must can could ought
all any both each every either neither few many much most more less least
some such no not none only own same other another several enough
up down out just now there here well also very even back still too again once
ever never always often sometimes usually really quite rather almost already
ago away together soon today tomorrow yesterday
go goes went gone going get gets got getting make makes made making
take takes took taken taking know knows knew known knowing think thinks
thought thinking see sees saw seen seeing come comes came coming want wants
wanted use uses used using find finds found give gives gave given tell tells
told work works worked call calls called try tries tried ask asks asked
need needs needed feel feels felt become becomes became leave leaves left
put puts mean means meant keep keeps kept let lets begin begins began begun
seem seems seemed help helps helped talk talks talked turn turns turned
start starts started show shows showed shown hear hears heard play plays
played run runs ran move moves moved like likes liked live lives lived
believe believes believed hold holds held bring brings brought happen happens
happened write writes wrote written provide provides provided sit sits sat
stand stands stood lose loses lost pay pays paid meet meets met include
includes included continue continues continued set sets learn learns learned
change changes changed lead leads led understand understands understood
watch watches watched follow follows followed stop stops stopped create
creates created speak speaks spoke spoken read reads allow allows allowed
add adds added spend spends spent grow grows grew open opens opened walk
walks walked win wins won offer offers offered remember remembers remembered
love loves loved consider considers considered appear appears appeared buy
buys bought wait waits waited serve serves served send sends sent expect
expects expected build builds built stay stays stayed fall falls fell cut cuts
reach reaches reached remain remains remained suggest suggests suggested
raise raises raised pass passes passed sell sells sold require requires
required report reports reported decide decides decided pull pulls pulled
say says said
good better best new first last long great little old right big high
different small large next early young important public bad able sure clear
real true false whole free full strong hard easy major possible main current
worse worst minor
time day year way thing things man men woman women child children people
person world life hand part place case week company system program question
government number night point home water room mother father area money story
fact month lot study book eye job word business issue side kind head house
service friend power hour game line end member law car city community name
team minute idea kid body information parent face others level office door
health art war history party result morning reason research girl guy moment
air teacher force
one two three four five six seven eight nine ten eleven twelve thirteen
fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty
fifty sixty seventy eighty ninety hundred thousand million second third
yes no ok okay please thanks hello hi
chose looked
evidence
b c x
""".split())


def _is_dictionary_word(ident: str) -> bool:
    """True if ident is an ordinary English word. Such an id can never be
    genuinely 'named' by a prose receipt — the receipt contains it whether
    the option was named or not — so the id itself is the exploit."""
    return ident.lower() in ORDINARY_WORDS


def _names_id(text_lower: str, ident: str) -> bool:
    """True if ident appears in text_lower as a bounded token, not as a
    substring of a larger word. Substring matching lets 'c' pass inside
    'considered' and 'd' pass inside 'evidence' — that is the same
    absence-as-exploit class the fail-closed-shape law exists to kill."""
    return re.search(
        r"(?<![a-z0-9_])" + re.escape(ident) + r"(?![a-z0-9_])", text_lower
    ) is not None


def _nonempty_str(value) -> str:
    return str(value).strip() if isinstance(value, str) else ""


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "DECISION-RECEIPT-LAW", "law_status": "RATIFIED"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    decision = _nonempty_str(record.get("decision"))
    seat = _nonempty_str(record.get("seat"))
    chosen = _nonempty_str(record.get("chosen"))
    alternatives = record.get("alternatives")
    winning_evidence = _nonempty_str(record.get("winning_evidence"))
    receipt = _nonempty_str(record.get("receipt"))
    close_call = record.get("close_call", False)
    uncertainty_declared = record.get("uncertainty_declared", False)

    # 1. The decision and the decider must be named.
    if not decision:
        return fail(
            "decision missing or empty — a receipt for an unnamed decision "
            "is not a receipt",
            details,
        )
    if not seat:
        return fail(
            f"{decision}: seat unnamed — anonymous decisions are void; "
            "autonomy without a named decider is guessing with no owner",
            details,
        )
    details["decision"] = decision
    details["seat"] = seat

    # 2. Homework is mandatory: >= 2 alternatives, each identified.
    if not isinstance(alternatives, list):
        return fail(
            f"{decision}: alternatives is not a list — the law requires "
            "naming what was looked at (A, B, C); absence is the cheapest "
            "exploit, so a missing alternatives field fails closed",
            details,
        )
    if len(alternatives) < 2:
        return fail(
            f"{decision}: only {len(alternatives)} alternative(s) considered — "
            "one option is not a decision; a decision without homework is "
            "guessing, not autonomy",
            details,
        )
    alt_ids: list[str] = []
    for i, alt in enumerate(alternatives):
        if not isinstance(alt, dict):
            return fail(
                f"{decision}: alternative #{i} is not an object — every "
                "alternative must carry an id and a description",
                details,
            )
        alt_id = _nonempty_str(alt.get("id"))
        alt_desc = _nonempty_str(alt.get("description"))
        if not alt_id:
            return fail(
                f"{decision}: alternative #{i} has no id — an unnamed "
                "alternative was not really considered",
                details,
            )
        if _is_dictionary_word(alt_id):
            return fail(
                f"{decision}: alternative id {alt_id!r} is an ordinary "
                "English word, not a real identifier — any prose receipt "
                "contains words like 'a' or 'the' naturally, so the "
                "receipt name-check would pass on a receipt that never "
                "names the option. Use a real identifier (opt-a, plan-2) "
                "that a receipt must deliberately write.",
                details,
            )
        if not alt_desc:
            return fail(
                f"{decision}: alternative {alt_id!r} has no description — "
                "a listed-but-undescribed option is homework theater",
                details,
            )
        alt_ids.append(alt_id)
    reasons.append(f"homework done: looked at {', '.join(alt_ids)}")

    # 3. The choice must be one of the things that was looked at.
    if not chosen:
        return fail(
            f"{decision}: chosen missing — the receipt must say what was "
            "chosen (I chose X)",
            details,
        )
    if chosen not in alt_ids:
        return fail(
            f"{decision}: chosen {chosen!r} is not among the alternatives "
            f"considered ({', '.join(alt_ids)}) — choosing what you never "
            "looked at is guessing, not a decision",
            details,
        )
    reasons.append(f"chose {chosen}")

    # 4. X won because [evidence] — the scorecard is the receipt.
    if not winning_evidence:
        return fail(
            f"{decision}: winning_evidence missing — 'X won because "
            "[evidence]' is the law's load-bearing sentence. If the evidence "
            "is missing, say so plainly instead of bluffing.",
            details,
        )
    reasons.append("winning evidence cited")
    details["winning_evidence"] = winning_evidence

    # 5. The plain-words receipt names the choice AND the field.
    if not receipt:
        return fail(
            f"{decision}: receipt missing — the law's report format is "
            "'I chose X. I looked at A, B, C. X won because [evidence]. "
            "This is what I did.' A decision record without the receipt "
            "sentence is homework with no report.",
            details,
        )
    receipt_lower = receipt.lower()
    if not _names_id(receipt_lower, chosen.lower()):
        return fail(
            f"{decision}: receipt does not name the chosen option "
            f"{chosen!r} — 'I chose X' must say X",
            details,
        )
    missing_alts = [a for a in alt_ids if not _names_id(receipt_lower, a.lower())]
    if missing_alts:
        return fail(
            f"{decision}: receipt does not name every alternative looked at "
            f"(missing: {', '.join(missing_alts)}) — 'I looked at A, B, C' "
            "must name the field, not gesture at it",
            details,
        )
    reasons.append("receipt names the choice and the full field")

    # 6. Honest on close calls.
    if close_call is True and uncertainty_declared is not True:
        return fail(
            f"{decision}: close_call is true but uncertainty_declared is not "
            "— 'honest on close calls. If the winner isn't clear or evidence "
            "is missing, say so plainly instead of bluffing.'",
            details,
        )
    if close_call is True:
        reasons.append("close call declared honestly")

    reasons.append(f"{decision}: decision receipt complete — chosen, field, "
                   "evidence, report")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="Decision Receipt Law check")
    parser.add_argument("--record", required=True,
                        help="JSON decision-receipt record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}",
                         {"law": "DECISION-RECEIPT-LAW"}),
                    args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
