"""Rule-based claim candidate splitter.

Splits source text into atomic claim candidates, each carrying its meaning
envelope. Deterministic and testable — no model calls. The splitter is
conservative: it would rather emit a claim marked AMBIGUOUS than silently
drop a qualifier.

Minimum sufficient claim rule: split independent assertions; preserve
inseparable qualifiers with their nucleus.
"""
from __future__ import annotations

import re

from .claim import Claim, MeaningEnvelope

# --- Qualifier detectors (each must EARN its value from explicit text) -------

_NEGATION_RES = [
    r"\bnot\b", r"\bnever\b", r"\bno\b", r"\bn't\b", r"\bwithout\b",
    r"\bneither\b", r"\bnone\b", r"\bn't\b",
]
_NEGATION_SCOPE_RES = {
    "not-all": r"\bnot all\b",
    "not-every": r"\bnot every\b",
}

_QUANTIFIER_RES = {
    "all": r"\b(all|every|each)\b",
    "3-of-5": r"\bthree of five\b",
    "only": r"\bonly\b",
}

_TEMPORAL_RES = {
    "AFTER": r"\bafter\b",
    "BEFORE": r"\bbefore\b",
}

_CONDITIONAL_RES = [r"\bif\b", r"\bwhen\b", r"\bunless\b", r"\bprovided\b"]

_EXCEPTION_RES = [r"\bexcept\b", r"\bexcept for\b", r"\bother than\b"]

_MODALITY_RES = {
    "POSSIBLE": [r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bpossibly\b"],
    "NECESSARY": [r"\bmust\b", r"\bnecessarily\b"],
    "PERMITTED": [r"\bmay\b(?=.*\b(execute|use|apply|proceed)\b)"],
    "CONDITIONAL": [r"\bif\b", r"\bwhen\b.*\b(holds|true)\b"],
    "REPORTED": [r"\bclaims?\b", r"\breported\b", r"\bsays?\b", r"\baccording to\b"],
}

_ATTRIBUTION_RES = [
    (r"\b(agent [A-Z0-9]+)\b.*\b(claims?|reported|says?)\b", "AGENT_REPORT"),
    (r"\b(naya [0-9])\b.*\b(claims?|reported|says?|brief)\b", "NAYA_REPORT"),
    (r"\baccording to\b", "THIRD_PARTY_REPORT"),
]

_CAUSATION_RES = [r"\bcaused?\b", r"\bbecause\b", r"\bled to\b", r"\bresulted in\b"]
_CORRELATION_RES = [r"\bobserved together\b", r"\bcorrelated\b", r"\balongside\b"]


def _find(patterns, text):
    if isinstance(patterns, str):
        patterns = [patterns]
    return any(re.search(p, text, re.I) for p in patterns)


def detect_envelope(sentence: str) -> MeaningEnvelope:
    """Extract the meaning envelope from explicit textual markers."""
    low = sentence.lower()

    # Polarity: negation present and scoping the nucleus
    polarity = "NEGATIVE" if _find(_NEGATION_RES, low) else "POSITIVE"

    # Quantifier / scope markers
    quantifier = "UNSPECIFIED"
    for name, pat in _QUANTIFIER_RES.items():
        if re.search(pat, low, re.I):
            quantifier = name
            break
    for name, pat in _NEGATION_SCOPE_RES.items():
        if re.search(pat, low, re.I):
            quantifier = name
            polarity = "NEGATIVE"
            break

    # Temporal
    time_relation = "UNSPECIFIED"
    for name, pat in _TEMPORAL_RES.items():
        if re.search(pat, low, re.I):
            time_relation = name
            break

    # Condition
    condition = "PRESENT" if _find(_CONDITIONAL_RES, low) else "NONE"

    # Exceptions
    exceptions = tuple(
        m.group(0) for pat in _EXCEPTION_RES
        for m in re.finditer(pat, low, re.I)
    )

    # Modality — most specific wins
    modality = "OBSERVED"
    if _find(_MODALITY_RES["REPORTED"], low):
        modality = "REPORTED"
    elif _find([r"\bmust\b", r"\bnecessarily\b"], low):
        modality = "NECESSARY"
    elif _find(_CONDITIONAL_RES, low):
        modality = "CONDITIONAL"
    elif _find(_MODALITY_RES["POSSIBLE"], low):
        modality = "POSSIBLE"

    # Attribution
    attribution = "NONE"
    epistemic = "OBSERVED"
    for pat, label in _ATTRIBUTION_RES:
        if re.search(pat, low, re.I):
            attribution = label
            epistemic = "REPORTED"
            break
    if re.search(r"\bno evidence\b", low, re.I):
        epistemic = "UNPROVEN"

    return MeaningEnvelope(
        polarity=polarity, quantifier=quantifier, scope="UNSPECIFIED",
        time_relation=time_relation, condition=condition,
        exceptions=exceptions, modality=modality,
        attribution=attribution, epistemic=epistemic,
    )


def detect_relation_markers(sentence: str) -> tuple:
    """Relationship markers present in the sentence (edge-type hints)."""
    low = sentence.lower()
    out = []
    if _find(_CAUSATION_RES, low):
        out.append("CAUSED")
    elif _find(_CORRELATION_RES, low):
        out.append("CO_OCCURRENCE")
    if _find([r"\bdepends on\b", r"\brequires\b"], low):
        out.append("REQUIRES")
    if _find([r"\bcontradicts?\b", r"\bhowever\b", r"\balthough\b"], low):
        out.append("CONTRADICTS_HINT")
    return tuple(out)


_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])")

# Clause boundaries that must NOT split a claim (qualifier carriers)
_PROTECTED_CLAUSES = [
    r"\bif\b.*?,",          # conditional clause
    r"\bwhen\b.*?,",
    r"\bunless\b.*?,",
    r"\bexcept\b[^.]*",     # exception phrase
    r"\balthough\b.*?,",
]


def split_candidates(source_text: str, source_id: str) -> list:
    """Split source into claim candidates, each with envelope + span.

    Returns list[Claim]. Sentences split on terminal punctuation; clauses
    carrying qualifiers (if/when/unless/except/although) are never detached
    from their nucleus — they travel inside the same candidate.
    """
    content_hash = Claim.content_hash(source_text)
    claims = []
    offset = 0
    # Strip markdown headers: they are structure, not claims
    clean = re.sub(r"^#{1,6}\s+.*$", "", source_text, flags=re.M)
    sentences = _SENTENCE_SPLIT.split(clean.strip())
    idx = 0
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        start = source_text.find(sent, offset)
        end = start + len(sent)
        offset = end
        envelope = detect_envelope(sent)
        rels = detect_relation_markers(sent)
        claims.append(Claim(
            claim_id=f"{source_id}:C-{idx:03d}",
            parent_source_id=source_id,
            source_content_hash=content_hash,
            text_span=(start, end),
            nucleus=sent,
            envelope=envelope,
            relations=tuple((r, "") for r in rels),
        ))
        idx += 1
    return claims
