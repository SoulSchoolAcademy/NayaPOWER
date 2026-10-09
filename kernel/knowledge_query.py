"""KNOW intelligence lookup for ACT decisions (Phase 2 of the 9-node wiring).

Connects ``Kernel.decide()`` to KNOW's memory: before a governed decision is
returned, the kernel queries the Smart Note registry for intelligence
applicable to the pending decision and attaches what it found.

Design notes
------------
* The query reuses ``tools.smart_note_v2``'s proven scoring logic (field
  weights, phrase bonus, relevance-dominates-authority ordering) but operates
  on the registry directly so it can return the TOP N results instead of the
  single winner ``retrieve()`` returns. ``retrieve()`` also raises
  ``SystemExit("NO_RELEVANT_INTELLIGENCE")`` on empty results, which must
  never propagate out of a decision.
* Never raises on empty results: any failure (missing registry, unreadable
  file, empty corpus) yields ``[]``. The caller (``Kernel.decide``) must be
  able to decide with LAW alone when KNOW is unavailable.
* This module never calls ``retrieve()`` itself, so it is compatible with
  both the old ``retrieve(query)`` signature and the new one carrying the
  ``requester_context`` kwarg.
"""

from __future__ import annotations

import re

from tools.smart_note_v2 import (
    REGISTRY,
    TRUTH_STATE_RANK,
    _field_words,
    _nutshell_text,
    load_json,
)

# Lifecycle states that must never surface as applicable intelligence,
# mirrored from retrieve().
_INACTIVE_LIFECYCLE_STATES = {"SUPERSEDED", "ARCHIVED", "REVOKED"}

_SOURCE = "repository_projection_index"


def _scope_of(decision_context) -> str:
    """Best-effort scope string for a decision context.

    ``DecisionContext`` carries scope on ``authority.scope``; tolerate a
    direct ``.scope`` attribute too (duck-typed contexts).
    """
    scope = getattr(decision_context, "scope", None)
    if scope:
        return str(scope)
    authority = getattr(decision_context, "authority", None)
    authority_scope = getattr(authority, "scope", None) if authority else None
    return str(authority_scope) if authority_scope else ""


def retrieve_applicable_intelligence(
    decision_context, truth_floor: str = "VERIFIED", max_results: int = 5
) -> list:
    """Query KNOW for intelligence applicable to a pending decision.

    decision_context: object with ``.action`` (str) and ``.scope`` (str)
        attributes (scope may also come from ``.authority.scope``).
    truth_floor: minimum truth_state (``"VERIFIED"``, ``"RATIFIED"``,
        ``"ACTIVE"``, ``"LEARNED"``); compared via ``TRUTH_STATE_RANK``.
    max_results: cap on returned results.

    Returns: list of ``{"entry", "truth_state", "explanation", "provenance"}``
    dicts, best first. Never raises on empty results — returns ``[]``.
    """
    try:
        return _retrieve(decision_context, truth_floor, max_results)
    except SystemExit:
        # retrieve()'s NO_RELEVANT_INTELLIGENCE path must never escape.
        return []
    except Exception:
        # KNOW unavailable (missing registry, bad JSON, ...): decide() must
        # still work on LAW alone, so degrade to empty intelligence.
        return []


def _retrieve(decision_context, truth_floor: str, max_results: int) -> list:
    if max_results is None or max_results <= 0:
        return []
    action = str(getattr(decision_context, "action", "") or "")
    scope = _scope_of(decision_context)
    query_string = f"{action} {scope}".strip()

    registry = load_json(REGISTRY)
    entries = registry.get("entries", []) if isinstance(registry, dict) else []

    # Query tokenization mirrors retrieve() exactly: raw lowercase
    # alphanumeric tokens for the phrase bonus, stemmed set for field
    # matching.
    q_raw = re.findall(r"[a-z0-9]+", query_string.lower())
    q = _field_words(query_string)
    q_phrase = " ".join(q_raw)

    floor_rank = TRUTH_STATE_RANK.get(str(truth_floor).upper(), 0)

    ranked = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        if str(e.get("lifecycle_state", "ACTIVE")).upper() in _INACTIVE_LIFECYCLE_STATES:
            continue
        rank = TRUTH_STATE_RANK.get(str(e.get("truth_state", "")).upper(), 0)
        if rank < floor_rank:
            continue
        title = e.get("title", "")
        nutshell = _nutshell_text(e.get("projection_path", ""))
        keywords = " ".join(e.get("keywords", []) or [])
        taxonomy = " ".join(
            [e.get("category", "") or "", e.get("topic", "") or "", e.get("subtopic", "") or ""]
        )
        # Field weights mirror retrieve() (retrieval 10/10 track): title >
        # lesson content > keywords > taxonomy; phrase bonus for exact query
        # phrase; relevance dominates, authority breaks ties; zero relevance
        # never wins.
        score = 0.0
        score += len(q & _field_words(title)) * 3.0
        score += len(q & _field_words(nutshell)) * 2.0
        score += len(q & _field_words(keywords)) * 1.5
        score += len(q & _field_words(taxonomy)) * 1.0
        if q_phrase and (q_phrase in title.lower() or q_phrase in nutshell.lower()):
            score += 2.0
        if score <= 0:
            continue
        ranked.append((score, rank, e))

    ranked.sort(key=lambda z: (z[0], z[1], z[2].get("captured_at", "")), reverse=True)

    results = []
    for _score, _rank, e in ranked[:max_results]:
        results.append(
            {
                "entry": e,
                "truth_state": e.get("truth_state"),
                "explanation": _nutshell_text(e.get("projection_path", "")),
                "provenance": {"source": _SOURCE, "query": query_string},
            }
        )
    return results
