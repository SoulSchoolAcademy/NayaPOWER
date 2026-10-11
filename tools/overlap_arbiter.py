#!/usr/bin/env python3
"""UD-19 overlap arbiter — when work overlaps, the math decides.

No-ego merge protocol. When two lanes' work overlaps or conflicts, nobody
pulls rank: overlapping claims are decided by independent cross-scores
(doer != scorer != verifier), the value rule (highest verified value wins;
ties go to better evidence; a final tie is broken by a recorded
Intelligence-Question answer), and every decision lands in a receipt that
cites evidence, never rank. The receipt is the only authorization.

Built on: tools/scorecard.py (fixed-rubric scoring semantics) and
tools/no_self_cert.py (independence enforcement). This module is the
general protocol; the merge-consensus gate (PR #2196 and its fix) is a
separate, PR-specific gate.

Stdlib only.
"""
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

EPSILON_TIE = 0.5  # score gap below this is a tie
MIN_REASONING_CHARS = 20

RESOLUTIONS = ("ADVANCE_WINNER", "MERGE_BOTH", "COMPOSE_PARTS")

_RANK_PATTERNS = ("senior", "rank", "my authority", "because i'm",
                  "because i am", "outrank", "pull rank")


class OverlapError(Exception):
    """Machine-readable refusal. code is stable; detail explains."""

    def __init__(self, code, detail=""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class Claim:
    """One lane's overlapping work product."""
    claimant: str          # seat/lane making the claim
    artifact_id: str       # stable id for the work product
    work_key: str          # what work this is (overlap grouping key)
    artifact_hash: str     # content hash of the exact bytes judged
    location: str          # branch/PR/path where it lives (preservation)
    ts: str = ""


@dataclass
class CrossScore:
    """One independent scorer's evidenced score of someone else's artifact."""
    scorer: str
    artifact_id: str
    scores: dict           # dimension -> 0..10
    evidence: list         # evidence refs, each a source+pointer string
    ts: str = ""


def validate_evidence(evidence):
    """Evidence must exist, be descriptive, and be distinct."""
    if not evidence:
        raise OverlapError("SCORE_WITHOUT_EVIDENCE",
                           "a score with no cited evidence is inflation")
    seen = set()
    for ref in evidence:
        if not isinstance(ref, str) or len(ref.strip()) < 4:
            raise OverlapError("SCORE_WITHOUT_EVIDENCE",
                               f"evidence ref too thin to check: {ref!r}")
        key = ref.strip().lower()
        if key in seen:
            raise OverlapError("DUPLICATE_EVIDENCE",
                               f"same evidence cited twice: {ref!r}")
        seen.add(key)
    return [r.strip() for r in evidence]


def cross_score(claim, scorer, scores, evidence, ts=""):
    """Record one independent cross-score. The claimant may never judge
    their own overlap — that is refused, not warned."""
    if scorer == claim.claimant:
        raise OverlapError("SELF_JUDGE",
                           f"{scorer} may not score their own artifact "
                           f"{claim.artifact_id}")
    if not scores:
        raise OverlapError("SCORE_WITHOUT_EVIDENCE",
                           "empty scorecard decides nothing")
    for dim, val in scores.items():
        if not isinstance(val, (int, float)) or not (0 <= val <= 10):
            raise OverlapError("SCORE_WITHOUT_EVIDENCE",
                               f"dimension {dim!r} out of 0..10: {val!r}")
    clean = validate_evidence(evidence)
    return CrossScore(scorer=scorer, artifact_id=claim.artifact_id,
                      scores=dict(scores), evidence=clean, ts=ts or _now())


def find_overlaps(claims):
    """Group claims by work_key. Groups with 2+ distinct claimants are
    genuine overlaps needing arbitration. (tools/warn_overlapping_prs.py
    covers the advisory PR-file watch; this is the work-product trigger.)"""
    groups = {}
    for c in claims:
        groups.setdefault(c.work_key, []).append(c)
    return {k: v for k, v in groups.items()
            if len({c.claimant for c in v}) >= 2}


def _artifact_total(scores_for_artifact):
    """Mean of dimension-means across independent scorers."""
    per_scorer = [sum(s.scores.values()) / len(s.scores)
                  for s in scores_for_artifact]
    return sum(per_scorer) / len(per_scorer)


def _evidence_quality(scores_for_artifact):
    """Count of distinct evidence refs across scorers."""
    refs = set()
    for s in scores_for_artifact:
        refs.update(r.lower() for r in s.evidence)
    return len(refs)


def _check_reasoning(reasoning):
    if not reasoning or len(reasoning.strip()) < MIN_REASONING_CHARS:
        raise OverlapError("RANK_NOT_EVIDENCE",
                           "reasoning must explain the decision in words")
    low = reasoning.lower()
    for pat in _RANK_PATTERNS:
        if pat in low:
            raise OverlapError("RANK_NOT_EVIDENCE",
                               f"reasoning cites rank, not evidence: {pat!r}")


def arbitrate(claims, cross_scores, verifier, resolution, reasoning,
              iq_answer=""):
    """Decide one overlap set. Returns the decision receipt (dict).

    The verifier must be independent of every claimant. Every artifact
    needs at least one cross-score from a non-claimant. Highest verified
    value wins; ties go to better evidence; a remaining tie requires a
    recorded Intelligence-Question answer.
    """
    claimants = {c.claimant for c in claims}
    if verifier in claimants:
        raise OverlapError("SELF_VERIFY",
                           f"verifier {verifier} is a claimant in this overlap")
    if resolution not in RESOLUTIONS:
        raise OverlapError("RANK_NOT_EVIDENCE",
                           f"unknown resolution: {resolution!r}")
    _check_reasoning(reasoning)

    by_artifact = {}
    for s in cross_scores:
        by_artifact.setdefault(s.artifact_id, []).append(s)
    for c in claims:
        got = by_artifact.get(c.artifact_id, [])
        if not got:
            raise OverlapError("SCORE_WITHOUT_EVIDENCE",
                               f"artifact {c.artifact_id} has no cross-score")
        for s in got:
            if s.scorer == c.claimant:
                raise OverlapError("SELF_JUDGE",
                                   f"{s.scorer} scored their own artifact")

    totals = {c.artifact_id: _artifact_total(by_artifact[c.artifact_id])
              for c in claims}
    qualities = {c.artifact_id: _evidence_quality(by_artifact[c.artifact_id])
                 for c in claims}

    ranked = sorted(totals, key=lambda a: totals[a], reverse=True)
    winner, runner = ranked[0], ranked[1] if len(ranked) > 1 else (ranked[0], None)
    margin = totals[winner] - totals[runner] if runner else 0.0
    tiebreak = None
    if runner and margin < EPSILON_TIE:
        if qualities[winner] != qualities[runner]:
            winner = max(ranked[:2], key=lambda a: qualities[a])
            tiebreak = (f"score tie ({totals[ranked[0]]:.2f} vs "
                        f"{totals[ranked[1]]:.2f}); decided by evidence "
                        f"quality {qualities[winner]} vs "
                        f"{qualities[[a for a in ranked[:2] if a != winner][0]]}")
        else:
            if not iq_answer or len(iq_answer.strip()) < MIN_REASONING_CHARS:
                raise OverlapError("TIEBREAK_MISSING",
                                   "score and evidence tied; a recorded "
                                   "Intelligence-Question answer is required")
            tiebreak = f"score and evidence tied; Intelligence Question: {iq_answer.strip()}"

    # Flag evidence cited for two different artifacts by the same scorer.
    evidence_flags = []
    seen_refs = {}
    for s in cross_scores:
        for ref in s.evidence:
            key = (s.scorer, ref.lower())
            if key in seen_refs and seen_refs[key] != s.artifact_id:
                evidence_flags.append(
                    {"code": "DUPLICATE_EVIDENCE",
                     "detail": f"scorer {s.scorer} cited the same evidence "
                               f"for {seen_refs[key]} and {s.artifact_id}: "
                               f"{ref!r}"})
            else:
                seen_refs[key] = s.artifact_id

    losers = [c for c in claims if c.artifact_id != winner]
    receipt = {
        "protocol": "UD-19 no-ego merge",
        "work_key": claims[0].work_key,
        "decided_at": _now(),
        "verifier": verifier,
        "artifacts": [
            {"artifact_id": c.artifact_id, "claimant": c.claimant,
             "artifact_hash": c.artifact_hash,
             "cross_score_total": round(totals[c.artifact_id], 3),
             "evidence_quality": qualities[c.artifact_id],
             "scorers": sorted({s.scorer for s in by_artifact[c.artifact_id]})}
            for c in claims
        ],
        "winner": winner,
        "winner_claimant": next(c.claimant for c in claims
                                if c.artifact_id == winner),
        "margin": round(margin, 3),
        "tiebreak": tiebreak,
        "resolution": resolution,
        "reasoning": reasoning.strip(),
        "evidence_refs": sorted({r for s in cross_scores for r in s.evidence}),
        "evidence_flags": evidence_flags,
        "preserved_losers": [
            {"artifact_id": c.artifact_id, "claimant": c.claimant,
             "artifact_hash": c.artifact_hash, "location": c.location}
            for c in losers
        ],
        "does_not_claim": ("This receipt authorizes the stated resolution for "
                           "the stated artifact hashes only. It does not claim "
                           "the winner is perfect, the evidence is true, or "
                           "another verifier would agree."),
    }
    return receipt


def main(argv):
    print("UD-19 overlap arbiter. Import this module; see "
          "tools/overlap-arbiter-README.md. No CLI scoring — scores are "
          "entered by independent scorers via cross_score().")
    return 0


if __name__ == "__main__":
    raise SystemExit(main([]))
