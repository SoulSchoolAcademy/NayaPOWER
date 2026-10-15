"""Claim-check + dedup addon for tools/post_checker.py (Zeta w195/w201).

Pre-post hygiene: a confident quantitative claim without a live receipt
must not ship. Division of labor with Gamma's CI-side claim_reconcile.py:

  post_checker (text in hand)  -> receipt PRESENCE: every claim carries one
  claim_reconcile (live state) -> receipt TRUTH: SHA freshness, named-check
      binding, cherry-pick ordering, ambiguity fails closed

This addon never adjudicates. It only requires that a claim is anchored.

WHAT THIS DOES NOT CLAIM (D32)
- It does not verify a cited SHA equals any live head (that's STALE, the
  CI gate's job). A cited receipt may still be wrong — just not absent.
- It does not bind a named check ("Team gate green") to the real check
  or fail ambiguous names closed — claim_reconcile does.
- It does not verify a check-run id belongs to the PR under discussion.

Vocabulary alignment (w201): the claim families and receipt anchors mirror
Gamma's claim_reconcile.py parse vocabulary — proven against its 8 claim
fixtures in tests. An unwired gate protects nobody: wire check_claim into
post_checker.check_post.

ITEM-9 VERDICT (registered w218; decided with Gamma): a bare #NNNN issue
reference does NOT bind a green-CI claim. Binding anchors are an asserted
head SHA (+ check-run id) observed THIS mission — "green at <sha>", the
bare 40-char sha, or check-run/run id (see _RECEIPT_PATTERNS). Code
landing is the BARE_ISSUE_BINDS flag flip plus the claim-conflict fixture
test update — pending; until it lands the gate still binds bare issues and
this docstring names the decided rule, not the current behavior.
"""

import re
import difflib

# Verdict boundary (item 9 — decided WITH Gamma; verdict registered in the
# module docstring w218): whether a bare #NNNN issue reference counts as a
# live receipt for a green-CI claim. The flip of this ONE constant (plus the
# claim-conflict fixture test update) is the pending code landing.
BARE_ISSUE_BINDS = True

# Confident quantitative claims that need a live receipt to ship.
# X/10 scores are EXCLUDED — check_score owns them (meaning rule).
# Named-green forms parse wide like claim_reconcile (adjudication, with
# strict matching, stays on the CI side).
_CLAIM_PATTERNS = [
    # green claims (broad)
    re.compile(r"(?i)\ball\s+green\b"),
    re.compile(r"(?i)\bgreen\s+ci\b"),
    re.compile(r"(?i)\bci\s+(is\s+)?green\b"),
    re.compile(r"(?i)\ball\s+checks?\s+(are\s+)?green\b"),
    re.compile(r"(?i)\bchecks?\s+(are\s+)?all\s+green\b"),
    re.compile(r"(?i)\bci\s+passed\b"),
    re.compile(r"(?i)\bchecks?\s+pass(?:ed|ing)?\b"),
    # green claims (named — parse wide, adjudicate elsewhere)
    re.compile(r"(?i)([^\W\d_][\w][\w \-/]{1,48}?)\s+"
               r"(gate|check)\s+(?:is\s+|came\s+back\s+)?green\b"),
    re.compile(r"(?im)^[\s>*\-]*([^\W\d_][\w][\w \-/]{1,48}?)"
               r"\s*[:\u2013\u2014-]\s*green\b"),
    # N/N counts
    re.compile(r"\b\d+\s*/\s*\d+\s*(?:checks?|tests?|runs?|jobs?)?\b"),
    # zero-failure claims
    re.compile(r"(?i)\bno\s+(failures?|errors?|objections?)\b"),
    re.compile(r"(?i)\bzero\s+(failures?|errors?)\b"),
]

# Live-receipt anchors: observed THIS mission, not from memory.
# Same vocabulary Gamma's claim_reconcile.py binds on — including the bare
# full-length SHA written as "green at <sha>" (its fixtures' canonical form).
_RECEIPT_PATTERNS = [
    re.compile(r"(?:@\s*|\b(?:sha|commit|tree|tip|head|ref)\s*[:=]?\s*)"
               r"([0-9a-f]{7,40})\b", re.IGNORECASE),
    re.compile(r"\b[0-9a-f]{40}\b"),  # bare full-length SHA, "at <sha>" style
    re.compile(r"(?i)(?:check[- ]?run|run)\s*(?:id\s*)?[:#]?\s*(\d{6,})"),
    re.compile(r"(?i)\bobserved\s+(in\s+)?this\s+mission\b"),
]
if BARE_ISSUE_BINDS:
    _RECEIPT_PATTERNS.append(re.compile(r"#\d{3,5}"))


def _unquoted_lines(body):
    """Author's own lines: reuse post_checker._unquoted when available,
    else a minimal local copy."""
    try:
        import post_checker as pc
        return pc._unquoted(body)
    except Exception:
        kept, in_fence = [], False
        for line in body.splitlines():
            s = line.lstrip()
            if s.startswith("```") or s.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence or s.startswith(">"):
                continue
            kept.append(line)
        return "\n".join(kept)


def check_claim(body):
    """Every confident quantitative claim must carry a live receipt.

    Returns (ok, detail). FLAG when a claim pattern fires but no
    receipt anchor is present — the claim ships on memory, not
    measurement. Vacuous PASS when no quantitative claim exists.

    Does NOT judge whether the receipt is true or fresh; it only
    requires one to be present. Truth/freshness is claim_reconcile's
    job at the CI gate.
    """
    body = _unquoted_lines(body)
    # Scores are check_score's territory (the meaning rule), not ours:
    # strip X/10 spans so "9.5/10" never reads as an N/N count claim.
    body = re.sub(r"\d+(?:\.\d+)?\s*/\s*10\b", " ", body)
    claims = sorted({p.pattern for p in _CLAIM_PATTERNS
                     if p.search(body)})
    if not claims:
        return True, "no quantitative claim — nothing to bind"
    receipts = [p.pattern for p in _RECEIPT_PATTERNS
                if p.search(body)]
    if receipts:
        return True, f"{len(claims)} claim(s) bound to live receipt"
    return False, (f"confident claim without live receipt: "
                   f"{claims[0][:48]}… — cite @ <head-sha> or the 40-char "
                   f"sha + check-run id observed THIS mission")


def _norm(body):
    """Normalize for dedup: lowercase, drop schema labels, punctuation,
    numbers that are ids/timestamps (not content words)."""
    text = _unquoted_lines(body).lower()
    text = re.sub(r"(?m)^\s*(state|verdict|next|owner|evidence|score|"
                  r"win_why|blocker|lesson|drift|emit_feedback)\s*[:|]",
                  " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\b\d{4,}\b", " ", text)   # ids, timestamps, shas
    return re.sub(r"\s+", " ", text).strip()


def check_dedup(body, recent_bodies, threshold=0.85):
    """FLAG when this post is a near-duplicate of a recent one.

    Caller passes only in-window bodies (e.g. last 20 board comments,
    6h window — the three-level protocol's DEDUP rule). Similarity is
    token-sequence ratio on normalized text; >= threshold = repost,
    link the original instead."""
    me = _norm(body)
    if not me:
        return True, "empty post — nothing to dedup"
    best = 0.0
    for other in recent_bodies:
        them = _norm(other)
        if not them:
            continue
        r = difflib.SequenceMatcher(None, me, them).ratio()
        best = max(best, r)
        if best >= threshold:
            return False, (f"near-duplicate of a recent post "
                           f"(similarity {best:.2f} >= {threshold}) — "
                           f"link it, don't repost")
    return True, f"no duplicate in {len(recent_bodies)} recent (best {best:.2f})"
