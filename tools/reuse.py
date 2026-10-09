"""REUSE lifecycle step: attach ACTIVE+ learnings to a pending decision.

Scans the smart-notes registry for learnings applicable to a pending
decision's action/scope and returns the top matches for the decider to
consider BEFORE acting — that is the reuse arc: intelligence earned by past
executions re-enters the next decision.

Self-contained by design: the tokenize/stem/weighted-scoring pattern follows
tools/smart_note_v2.py::retrieve() but is re-implemented here — no
cross-worker imports. Scoring pattern: title 3.0, keywords 1.5,
category/topic/subtopic 1.0, exact-phrase-in-title bonus 2.0. Relevance
dominates; truth-state rank only breaks ties; zero-relevance never attaches.

Truth-state filter: only entries with truth_state at or above truth_floor
(default ACTIVE) attach. Rank map: LEARNED 4 > ACTIVE 3 > RATIFIED 2 >
VERIFIED 1; unknown/missing ranks 0.

Never raises on empty input or a missing registry — returns attached_count 0.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / ".naya" / "memory" / "smart-notes" / "index.json"

# Own copy of the truth-state rank (self-contained, no cross-worker imports).
# Higher = more authoritative. Full ladder:
# CANDIDATE < TESTING < VERIFIED < RATIFIED < ACTIVE < LEARNED.
TRUTH_STATE_RANK = {"LEARNED": 4, "ACTIVE": 3, "RATIFIED": 2, "VERIFIED": 1}

_INACTIVE_LIFECYCLE = {"SUPERSEDED", "ARCHIVED", "REVOKED"}


def _registry_path() -> Path:
    env = os.environ.get("NAYA_SMART_NOTES_REGISTRY")
    return Path(env) if env else DEFAULT_REGISTRY


def _stem(word: str) -> str:
    """Normalize common English inflections (same conservative pattern as
    smart_note_v2._stem: never shortens below 4 chars)."""
    if len(word) <= 4:
        return word
    for suffix in ("ing", "ed", "es", "ly", "ion"):
        if word.endswith(suffix) and len(word) > len(suffix) + 3:
            return word[:-len(suffix)]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 5:
        return word[:-1]
    return word


def _field_words(text: str) -> set:
    """Tokenize text into a set of stemmed lowercase words."""
    return set(_stem(w) for w in re.findall(r"[a-z0-9]+", (text or "").lower()))


def _score_entry(query_words: set, query_phrase: str, entry: dict) -> float:
    """Weighted relevance score (the retrieve() pattern, minimal form)."""
    title = entry.get("title", "") or ""
    keywords = " ".join(entry.get("keywords", []) or [])
    taxonomy = " ".join([
        entry.get("category", "") or "",
        entry.get("topic", "") or "",
        entry.get("subtopic", "") or "",
    ])
    score = 0.0
    score += len(query_words & _field_words(title)) * 3.0
    score += len(query_words & _field_words(keywords)) * 1.5
    score += len(query_words & _field_words(taxonomy)) * 1.0
    if query_phrase and query_phrase in title.lower():
        score += 2.0
    return score


def _entry_id(entry: dict) -> str:
    return str(entry.get("intelligent_block_id") or entry.get("id") or "")


def reuse_for_decision(decision_context, truth_floor: str = "ACTIVE",
                       max_results: int = 3) -> dict:
    """Attach ACTIVE+ learnings applicable to a pending decision.

    decision_context: object with .action (str) and .scope (str).
    Returns {"learnings": [...], "attached_count": N, "log_entry": {...}}.
    Each learning: {"entry": {...}, "truth_state": ..., "provenance": {...}}.
    The log_entry records decision action + attached learning IDs + timestamp
    (for the later PROVE step). Never raises on empty — attached_count 0.
    """
    action = str(getattr(decision_context, "action", "") or "")
    scope = str(getattr(decision_context, "scope", "") or "")
    query = f"{action} {scope}".strip()
    floor_rank = TRUTH_STATE_RANK.get(str(truth_floor or "ACTIVE").upper(), 3)
    log_entry = {
        "decision_action": action,
        "decision_scope": scope,
        "truth_floor": str(truth_floor or "ACTIVE").upper(),
        "attached_learning_ids": [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    def empty():
        return {"learnings": [], "attached_count": 0, "log_entry": log_entry}

    if not query:
        return empty()
    try:
        limit = max(0, int(max_results))
    except (TypeError, ValueError):
        limit = 3
    try:
        registry = json.loads(_registry_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return empty()
    entries = registry.get("entries", []) or []

    q_raw = re.findall(r"[a-z0-9]+", query.lower())
    q = set(_stem(w) for w in q_raw)
    q_phrase = " ".join(q_raw)

    ranked = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        if str(e.get("lifecycle_state", "ACTIVE")).upper() in _INACTIVE_LIFECYCLE:
            continue
        rank = TRUTH_STATE_RANK.get(str(e.get("truth_state", "")).upper(), 0)
        if rank < floor_rank:
            continue
        score = _score_entry(q, q_phrase, e)
        if score <= 0:
            # Authority never promotes irrelevance.
            continue
        ranked.append((score, rank, e))
    # Relevance dominates; truth-state rank breaks ties.
    ranked.sort(key=lambda z: (z[0], z[1], z[2].get("captured_at", "")),
                reverse=True)

    learnings = []
    for _score, _rank, e in ranked[:limit]:
        entry_id = _entry_id(e)
        learnings.append({
            "entry": {
                "id": entry_id,
                "title": e.get("title", "") or "",
                "keywords": e.get("keywords", []) or [],
                "category": e.get("category", "") or "",
                "topic": e.get("topic", "") or "",
            },
            "truth_state": str(e.get("truth_state", "")).upper(),
            "provenance": {
                "entry_id": entry_id,
                "source": "smart-notes-registry",
                "captured_at": e.get("captured_at", "") or "",
                "registry_provenance": e.get("provenance", {}) or {},
            },
        })
    log_entry["attached_learning_ids"] = [l["entry"]["id"] for l in learnings]
    return {"learnings": learnings, "attached_count": len(learnings),
            "log_entry": log_entry}
