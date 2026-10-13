"""Ratification gate — the math is the law (Naya 5, 2026-10-13).

Shawn's rule, mechanized. The incident: PR #2550's title claimed
"Shawn RATIFIED" on the strength of his encouragement ("The word! :)").
That is L316 — a legal act stamped from a thumbs-up.

The rule:
- Score < 9.5: NOT_RATIFIED. His "looks good" is ENCOURAGEMENT, never
  approval. The system states the score and what would qualify.
  His casual approval NEVER lowers the bar.
- Score >= 9.5 and protocol green: RATIFIED AUTOMATICALLY. His word is
  not needed. Asking for it anyway creates a bottleneck AND a backdoor.
- His explicit word is reserved for what the math can't decide: values,
  direction, genuine judgment calls — and must cite the exact content hash.
- A claimed "Shawn said" can NEVER upgrade a verdict. The claim is
  recorded as encouragement and ignored by the verdict. This protects him
  from the system ever saying "well Shawn said it was fine" about work
  that wasn't good enough.

Speech acts are typed: ENCOURAGEMENT (warm noise) vs DIRECTION (do X)
vs RATIFICATION (explicit, content-hashed). Only the third ratifies,
and only for non-scorable matters.
"""

RATIFICATION_BAR = 9.5

RATIFIED = "RATIFIED"
NOT_RATIFIED = "NOT_RATIFIED"
CANDIDATE = "CANDIDATE"
NEEDS_SHAWN = "NEEDS_SHAWN"


def ratify(score=None, protocol_green=False, claimed_word=None,
           explicit_override=False, content_hash=None, scorable=True):
    """Return (verdict, reasons) for a ratification question.

    score: honest 0-10 scorecard number, or None if unscored.
    protocol_green: independent review + green checks + feed receipt.
    claimed_word: anything Shawn said that someone cites as approval.
    explicit_override: True only when he EXPLICITLY invokes an override
        (deliberate, recorded — not casual encouragement).
    content_hash: the exact content being ratified/overridden.
    scorable: False for values/direction/genuine judgment calls.
    """
    reasons = []
    if claimed_word:
        reasons.append(
            f"encouragement noted ({claimed_word!r}); "
            "encouragement never ratifies")

    if not scorable:
        # Values, direction, judgment: only his explicit word decides.
        if claimed_word and content_hash:
            return (RATIFIED, reasons +
                    [f"explicit ratification of content {content_hash}"])
        return (NEEDS_SHAWN, reasons +
                ["not scorable by math; awaiting his explicit word"])

    if score is None:
        return (CANDIDATE, reasons +
                ["unscored: cannot ratify what was never measured"])

    if explicit_override and content_hash:
        return (RATIFIED, reasons +
                [f"EXPLICIT override of the {RATIFICATION_BAR} bar on "
                 f"{content_hash} — recorded, exceptional, not casual"])

    if score < RATIFICATION_BAR:
        return (NOT_RATIFIED, reasons +
                [f"score {score} < {RATIFICATION_BAR}: improve the work "
                 "or request an explicit override"])

    if protocol_green:
        return (RATIFIED, reasons +
                ["automatic: score >= 9.5 and protocol green; "
                 "his word was not needed"])

    return (CANDIDATE, reasons +
            ["score qualifies; awaiting protocol green"])


def describe(verdict_reasons):
    """One-line human rendering of a (verdict, reasons) pair."""
    verdict, reasons = verdict_reasons
    return f"{verdict} — " + "; ".join(reasons)
