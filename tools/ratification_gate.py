"""Ratification gate — the math is the law (Naya 5, 2026-10-13;
repaired 2026-10-14 after Naya 3's adversarial finding).

Shawn's rule, mechanized. The incident: PR #2550's title claimed
"Shawn RATIFIED" on the strength of his encouragement ("The word! :)").
That is L316 — a legal act stamped from a thumbs-up.

The repair (Naya 3, P0, reproduced 2026-10-14): the first version of this
gate still minted RATIFIED from two unauthenticated inputs — a claimed
word plus content hash on the non-scorable path, and an explicit_override
flag on the scored path. Three adversarial inputs proved it. That is the
L316 hole wearing a new hat: the gate was built so a claimed "Shawn said"
could never upgrade a verdict, and it did exactly that.

The root cause is structural, not a missing check: a pure function cannot
authenticate that Shawn said something. ANY parameter that converts a
string into RATIFIED is the hole. So the gate no longer traffics in words
at all — the word parameters are removed, not guarded.

The rule, final form:
- Score < 9.5: NOT_RATIFIED. Nothing anyone claims he said can upgrade it.
- Score >= 9.5 and protocol green: RATIFIED AUTOMATICALLY. His word is
  not needed. Asking for it anyway creates a bottleneck AND a backdoor.
- Not scorable by math (values, direction, genuine judgment): NEEDS_SHAWN.
  The gate cannot resolve this — resolving it requires a human who checked
  checkable evidence. See attest_ratification().
- attest_ratification() is the separate human step. It records an
  attestation: exact content hash + a CHECKABLE evidence ref (a GitHub
  comment ID or message ID — never a quoted string) + the identity of the
  human who verified it. It returns an auditable record, not a verdict.
  Trust rests on the attester and the ref; a different seat can
  independently verify the ref against the live source.
"""

RATIFICATION_BAR = 9.5

RATIFIED = "RATIFIED"
NOT_RATIFIED = "NOT_RATIFIED"
CANDIDATE = "CANDIDATE"
NEEDS_SHAWN = "NEEDS_SHAWN"


def ratify(score=None, protocol_green=False, scorable=True):
    """Return (verdict, reasons) for a ratification question.

    Pure math plus protocol. There are deliberately NO word parameters:
    code cannot authenticate a human, so the gate refuses to convert
    claimed speech into verdicts.

    score: honest 0-10 scorecard number, or None if unscored.
    protocol_green: independent review + green checks + feed receipt.
    scorable: False for values/direction/genuine judgment calls —
        the math has no standing there.
    """
    if not scorable:
        # Values, direction, judgment: the math has no standing, and a
        # score has no standing either. Only a human attestation resolves.
        return (NEEDS_SHAWN,
                ["not scorable by math; resolvable only by "
                 "attest_ratification() with an exact content_hash, a "
                 "checkable evidence_ref (comment/message ID, never a "
                 "quoted string), and the attested_by identity of the "
                 "human who verified it"])

    if score is None:
        return (CANDIDATE,
                ["unscored: cannot ratify what was never measured"])

    if score < RATIFICATION_BAR:
        return (NOT_RATIFIED,
                [f"score {score} < {RATIFICATION_BAR}: improve the work; "
                 "claimed approval can never upgrade a verdict"])

    if protocol_green:
        return (RATIFIED,
                ["automatic: score >= 9.5 and protocol green; "
                 "his word was not needed"])

    return (CANDIDATE,
            ["score qualifies; awaiting protocol green"])


def attest_ratification(content_hash, evidence_ref, attested_by):
    """Record a human's ratification attestation for non-scorable matters.

    This is the ONLY path by which NEEDS_SHAWN resolves, and it lives
    outside the gate on purpose: the gate types verdicts from math; only
    a human can authenticate Shawn's word, and only against checkable
    evidence.

    content_hash: SHA/ID of the EXACT content ratified. Required —
        ratification binds to exact content, never to a vibe.
    evidence_ref: checkable artifact proving he said it — a GitHub
        comment ID, message ID, or URL. A quoted string is NOT evidence;
        anyone can type quotes. Required.
    attested_by: identity of the human/seat who verified the ref against
        the live source. Required — someone stands behind the check.

    Returns an attestation record (a dict), NOT a verdict. The dock weighs
    the record with its evidence; ratify() never consumes it.
    """
    if not content_hash:
        raise ValueError(
            "content_hash is required — ratification binds to exact "
            "content, never to a vibe")
    if not evidence_ref:
        raise ValueError(
            "evidence_ref is required — a checkable comment/message ID, "
            "never a quoted string")
    if not attested_by:
        raise ValueError(
            "attested_by is required — someone stands behind the check")
    return {
        "attestation": "RATIFICATION_ATTESTED",
        "content_hash": content_hash,
        "evidence_ref": evidence_ref,
        "attested_by": attested_by,
    }


def describe(verdict_reasons):
    """One-line human rendering of a (verdict, reasons) pair."""
    verdict, reasons = verdict_reasons
    return f"{verdict} — " + "; ".join(reasons)
