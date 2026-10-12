"""Anti-citogenesis claim-evidence gate (spec, parked).

Law: internal repetition is not independent corroboration (operating law:
DISCERN->DISTILL rule 7; D32 anti-cascade -- no claim exceeds its evidence).
A verification attestation ("independently verified", "proven", ...) must
resolve to admissible evidence. Evidence that merely repeats the claim -- a
same-seat note, a note citing a note -- is inadmissible as independent
corroboration.

This module is pure: claim text + structured evidence in, verdicts out. It
makes no network calls and reads no GitHub state. CI wiring (feeding it PR
bodies on pull_request) is a separate activation decision -- Shawn's word.

Evidence is POOLED across the attestations in one text: one admissible item
supports every attestation. This catches citogenesis (repetition, self-
citation, no-evidence claims) -- the gate's named purpose. It does not do
per-attestation linkage: a single real test cited once will also cover a
second bare attestation in the same text. That is overclaiming, not
repetition; per-attestation linkage is future work, documented here rather
than silently assumed.

What it does NOT claim: it does not parse PR bodies, resolve seat tags, or
fetch reviews. It adjudicates evidence items a caller supplies. The caller
owns provenance of the evidence list.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

# Attestation patterns: natural-language verification claims. Tight on purpose:
# every hit must be a claim a reader would act on, not a code identifier.
# Snake_case identifiers (outcome_verified) are excluded by the guard below.
ATTESTATION_PATTERNS = [
    r"independently\s+verified",
    r"independent\s+verification",
    r"verified\s+by\b",
    r"\bproven\b",
]

_IDENTIFIER_CHAR = re.compile(r"[A-Za-z0-9_]")


def _is_code_identifier(text: str, start: int, end: int) -> bool:
    before = text[start - 1] if start > 0 else " "
    after = text[end] if end < len(text) else " "
    return bool(_IDENTIFIER_CHAR.match(before) or _IDENTIFIER_CHAR.match(after))


def normalize_seat(seat: Optional[str]) -> str:
    """'Naya 5' / 'naya5' / 'NAYA 5' -> 'naya5'. Empty -> ''."""
    if not seat:
        return ""
    return re.sub(r"\s+", "", seat.strip().lower())


@dataclass
class Evidence:
    """One cited evidence item.

    kind: 'test' | 'ci_run' | 'seat_review' | 'commit' | 'note'
    seat: authoring seat of the evidence ('Naya 4'), '' if not a seat artifact.
    ref:  the pointer -- test path, run id, comment id, sha, note id.
    repeats: True if this item merely repeats the claim (or repeats another
        repetition). Repetition is never corroboration.
    """

    kind: str
    ref: str
    seat: str = ""
    repeats: bool = False


@dataclass
class Attestation:
    text: str
    start: int
    end: int


@dataclass
class Verdict:
    attestation: Attestation
    admissible: bool
    reasons: List[str] = field(default_factory=list)
    admissible_evidence: List[Evidence] = field(default_factory=list)


def find_attestations(text: str) -> List[Attestation]:
    """Find verification attestations in prose. Code identifiers excluded."""
    found: List[Attestation] = []
    for pattern in ATTESTATION_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            if _is_code_identifier(text, m.start(), m.end()):
                continue
            # Dedupe overlapping hits from multiple patterns.
            ms, me = m.start(), m.end()
            if any(a.start < me and ms < a.end for a in found):
                continue
            found.append(Attestation(text=m.group(0), start=m.start(), end=m.end()))
    return sorted(found, key=lambda a: a.start)


def _adjudicate_item(
    item: Evidence,
    author_seat: str,
    path_exists: Callable[[str], bool],
) -> tuple[bool, bool, str]:
    """Return (counts_as_independent, counts_as_supporting, reason)."""
    seat = normalize_seat(item.seat)
    author = normalize_seat(author_seat)

    if item.repeats:
        return False, False, (
            f"evidence {item.kind}:{item.ref} repeats the claim -- "
            "repetition is not corroboration (anti-citogenesis)"
        )

    if item.kind == "test":
        if path_exists(item.ref):
            return True, True, f"executable evidence: {item.ref} exists"
        return False, False, f"evidence test:{item.ref} does not exist"

    if item.kind == "ci_run":
        return True, True, f"external machine evidence: ci_run {item.ref}"

    if item.kind == "seat_review":
        if seat and seat != author:
            return True, True, f"independent seat review by {item.seat} ({item.ref})"
        if seat == author:
            return False, False, (
                f"seat_review by {item.seat} is the author's own seat -- "
                "self-attestation, not independent evidence"
            )
        return False, False, f"seat_review {item.ref} names no seat -- unattributable"

    if item.kind == "commit":
        # The change existing is evidence of existence, never of verification.
        return False, True, f"commit {item.ref} supports existence, not verification"

    if item.kind == "note":
        if seat == author:
            return False, False, (
                f"note {item.ref} is by the author's own seat ({item.seat}) -- "
                "self-attestation, not independent evidence"
            )
        return False, True, (
            f"note {item.ref} by {item.seat or 'unknown seat'} is supporting only -- "
            "notes document; verification must be executable or seat-attested in review"
        )

    return False, False, f"unknown evidence kind: {item.kind}"


def adjudicate(
    text: str,
    author_seat: str,
    evidence: List[Evidence],
    path_exists: Optional[Callable[[str], bool]] = None,
) -> Dict:
    """Adjudicate every verification attestation in `text`.

    Returns {'verdicts': [Verdict...], 'pass': bool}. Fail-closed: any
    attestation with no admissible *independent* evidence fails the run.
    Text with no attestations passes (nothing claimed, nothing to prove).
    """
    exists = path_exists or os.path.exists
    attestations = find_attestations(text)
    verdicts: List[Verdict] = []

    for att in attestations:
        independent: List[Evidence] = []
        reasons: List[str] = []
        for item in evidence:
            is_ind, is_sup, reason = _adjudicate_item(item, author_seat, exists)
            reasons.append(reason)
            if is_ind:
                independent.append(item)
        verdicts.append(
            Verdict(
                attestation=att,
                admissible=len(independent) > 0,
                reasons=reasons,
                admissible_evidence=independent,
            )
        )

    return {
        "verdicts": verdicts,
        "pass": all(v.admissible for v in verdicts),
    }
