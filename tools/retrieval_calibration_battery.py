"""Retrieval relevance-floor calibration battery — RED-FIRST (Naya Narzan, 2026-10-13).

Finding it encodes (measured 2026-10-13 at live tip 582e5e5f, reproduced
identically at baseline e47a650e — NOT a tip regression):
  1. RETRIEVAL_RELEVANCE_FLOOR (40.0) sits above EVERY measured real-query
     top-1 score (18.8-33.5): retrieve() refuses 7/7 clearly-in-corpus queries.
  2. Positive and negative top-1 score classes OVERLAP: the best false
     positive ("how to bake sourdough bread" -> 23.95) outscores the weakest
     true positive ("fail closed index validation" -> 18.80). No single floor
     value can separate them. Lowering the floor alone is UNSAFE.
  3. The privacy-probe guard (_is_privacy_probe) is narrow-by-construction
     (store-enumeration phrasings only) and correctly does NOT fire on
     topic-queries like "the user's credit card number and password" — its
     winner is a lexically-plausible-but-irrelevant note (SN-0455, matched on
     "security"), a misdirection the floor must exclude, not a leak.

The contract this battery gates: a floor value is only admissible when the
labeled classes SEPARATE — min(positive top-1) > max(negative top-1) — so a
floor can live in the gap admitting true positives while refusing false
positives. Until then the battery is RED, and that redness is the receipt:
the fix is discrimination (applicability/relevance scoring), not a floor edit.

Run: python3 tools/retrieval_calibration_battery.py  (0 API; local corpus only)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tools.smart_note_v2 as sn2  # noqa: E402

# (query, expected winner id) — winner ids pinned from the 2026-10-13
# measurement; a ranking change must update these deliberately.
POSITIVE_CASES = [
    ("oath of the Naya", "SN-0199"),
    ("what is a Naya and how does she operate", "SN-0253"),
    ("brain index freshness validator", "SN-561"),
    ("cold retrieve applicability scoring", "SN-0497"),
    ("the merge law and five gates", "SN-0338"),
    ("scorecard law honest scoring", None),
    ("fail closed index validation", None),
]

# Queries that MUST refuse: either no candidates, a privacy-probe refusal,
# or a top-1 below any admissible floor.
NEGATIVE_CASES = [
    "asdf qzxw jklm vbnop",
    "purple elephant quantum banana",
    "the user's credit card number and password",
    "stock price of Tesla tomorrow",
    "how to bake sourdough bread",
    "weather in Tokyo next week",
]

MARGIN = 1.0  # required gap between classes, in score units


def top1(query):
    try:
        ranked = sn2._ranked_candidates(query)
    except SystemExit:
        return None, "REFUSED"
    if not ranked:
        return None, "NO_CANDIDATES"
    s, _, e = ranked[0]
    return s, (e.get("smart_note_id") or e.get("intelligent_block_id"))


def main():
    failures = []
    pos_scores, neg_scores = [], []
    lines = [f"floor={sn2.RETRIEVAL_RELEVANCE_FLOOR}"]

    for q, expected in POSITIVE_CASES:
        t0 = time.perf_counter()
        s, wid = top1(q)
        dt = (time.perf_counter() - t0) * 1000
        status = "REFUSED/EMPTY" if s is None else f"{s:.2f}"
        lines.append(f"POS {dt:7.1f}ms top1={status:>12} winner={wid}  q={q!r}")
        if s is None:
            failures.append(f"positive refused/empty: {q!r}")
        else:
            pos_scores.append(s)
            if expected and wid != expected:
                failures.append(f"positive winner drift: {q!r} -> {wid} (pinned {expected})")

    for q in NEGATIVE_CASES:
        s, wid = top1(q)
        status = "REFUSED/EMPTY" if s is None else f"{s:.2f}"
        lines.append(f"NEG {'':>10} top1={status:>12} winner={wid}  q={q!r}")
        if s is not None:
            neg_scores.append(s)

    if pos_scores and neg_scores:
        lo_pos, hi_neg = min(pos_scores), max(neg_scores)
        gap = lo_pos - hi_neg
        lines.append(f"min_pos={lo_pos:.2f} max_neg={hi_neg:.2f} gap={gap:+.2f} (need > {MARGIN})")
        if gap <= MARGIN:
            failures.append(
                f"classes overlap: no admissible floor — max_neg={hi_neg:.2f} >= min_pos - margin={lo_pos - MARGIN:.2f}"
            )
    elif pos_scores:
        lines.append("no scored negatives — separation holds trivially")
    else:
        failures.append("no scored positives at all — ranker produced nothing")

    print("\n".join(lines))
    if failures:
        print("\nRED — calibration failures:")
        for f in failures:
            print("  -", f)
        return 1
    print("\nGREEN — classes separate; a floor can live in the gap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
