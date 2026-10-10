"""naya.intent-matcher v1.0.0 — qualified Smart App.

Standalone intent-overlap scoring for lesson retrieval by a cold Naya.
Given a lesson's intent signature and a decision context's intent, returns
a 0.0–1.0 overlap score. Structured keyword/domain matching — not semantic
understanding; the score measures declared-intent overlap, nothing more.

Independent proof: 20 fixtures in tests/test_learn_smart_app_reuse.py
(fixture set INTENT_MATCHER_FIXTURES, all passing).
"""

from __future__ import annotations

from typing import Any


def normalize_terms(value: Any) -> set[str]:
    """Lowercased token set from a string or list of strings."""
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, (list, tuple)):
        items = [str(i) for i in value]
    else:
        return set()
    terms: set[str] = set()
    for item in items:
        for tok in item.lower().replace("/", " ").replace("-", " ").replace("_", " ").split():
            tok = "".join(c for c in tok if c.isalnum())
            if tok:
                terms.add(tok)
    return terms


def intent_match_score(lesson_signature: dict[str, Any], context_intent: dict[str, Any]) -> float:
    """Weighted intent overlap: 0.0 = none, 1.0 = full.

    Weights: domains 0.4, situations 0.4 (recall-oriented), decision_types 0.2.
    Returns 0.0 when either side carries no intent terms.
    """
    if not isinstance(lesson_signature, dict) or not isinstance(context_intent, dict):
        return 0.0

    score = 0.0
    weight_total = 0.0

    lesson_domains = normalize_terms(lesson_signature.get("domains"))
    context_domains = normalize_terms(context_intent.get("domains"))
    if lesson_domains or context_domains:
        weight_total += 0.4
        if lesson_domains and context_domains:
            overlap = lesson_domains & context_domains
            union = lesson_domains | context_domains
            score += 0.4 * (len(overlap) / len(union))

    lesson_situations = normalize_terms(lesson_signature.get("situations"))
    context_terms = normalize_terms(context_intent.get("situation")) | normalize_terms(
        context_intent.get("situation_keywords")
    )
    if lesson_situations or context_terms:
        weight_total += 0.4
        if lesson_situations and context_terms:
            overlap = lesson_situations & context_terms
            score += 0.4 * (len(overlap) / len(lesson_situations))

    lesson_decisions = normalize_terms(lesson_signature.get("decision_types"))
    context_decision = normalize_terms(context_intent.get("decision_type"))
    if lesson_decisions or context_decision:
        weight_total += 0.2
        if lesson_decisions and context_decision and (lesson_decisions & context_decision):
            score += 0.2

    if weight_total == 0.0:
        return 0.0
    return round(score / weight_total, 4)


def qualified_version() -> str:
    return "1.0.0"


def qualified_artifact_id() -> str:
    return "naya.intent-matcher"
