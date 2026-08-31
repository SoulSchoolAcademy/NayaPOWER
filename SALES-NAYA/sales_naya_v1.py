#!/usr/bin/env python3
"""Deterministic V1 Sales Naya intelligence engine.

No model, network call, vector store, or paid inference dependency is required.
The canonical knowledge JSON is the source of claims; this module only retrieves
and composes bounded responses from those entries.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_PATH = ROOT / "SALES-NAYA" / "NAYA-POWER-SALES-INTELLIGENCE-V1.json"


@dataclass(frozen=True)
class SalesAnswer:
    answer: str
    category: str
    support: str
    next_action: str
    cta_eligible: bool
    voice_text: str
    source_ids: tuple[str, ...]


def load_knowledge(path: Path = KNOWLEDGE_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") != "CANONICAL":
        raise ValueError("sales knowledge must be canonical")
    if not data.get("knowledge"):
        raise ValueError("sales knowledge is empty")
    return data


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(question: str, knowledge: dict[str, Any] | None = None) -> tuple[dict[str, Any], float]:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question is required")
    knowledge = knowledge or load_knowledge()
    q = _tokens(question)
    best: dict[str, Any] | None = None
    best_score = 0.0
    for entry in knowledge["knowledge"]:
        keys = set()
        for keyword in entry.get("keywords", []):
            keys |= _tokens(keyword)
        score = len(q & keys) / max(1, len(q | keys))
        # Exact phrase intent gets a small deterministic boost.
        if any(keyword.lower() in question.lower() for keyword in entry.get("keywords", [])):
            score += 0.25
        if score > best_score:
            best, best_score = entry, score
    if best is None or best_score < 0.10:
        best = next(x for x in knowledge["knowledge"] if x["id"] == "out_of_scope")
        return best, 0.0
    return best, min(best_score, 1.0)


def _cta(category: str, knowledge: dict[str, Any]) -> tuple[bool, str]:
    strong = {"challenge", "value", "activation"}
    eligible = category in strong
    if category == "boundary":
        eligible = True
    return eligible, knowledge["offer"]["promise"]


def compose(question: str, knowledge: dict[str, Any] | None = None) -> SalesAnswer:
    knowledge = knowledge or load_knowledge()
    entry, score = retrieve(question, knowledge)
    supported = score > 0 and entry["id"] != "out_of_scope"
    category = entry["intent"]
    cta_eligible, _ = _cta(category, knowledge)
    next_action = "Start the Five-Day Challenge." if cta_eligible else "Ask me what you want to understand next about Naya Power."
    answer = entry["answer"]
    if cta_eligible and entry["id"] != "five_day" and "Five-Day Challenge" not in answer:
        answer += " The easiest way to experience that difference is the Five-Day Challenge: 5 days, 5 lessons, 5 daily intelligence reports, zero risk."
    return SalesAnswer(
        answer=answer,
        category=category,
        support="SUPPORTED" if supported else "UNSUPPORTED",
        next_action=next_action,
        cta_eligible=cta_eligible,
        voice_text=answer,
        source_ids=tuple(entry.get("source_ids", [])),
    )


def answer(question: str, knowledge: dict[str, Any] | None = None) -> dict[str, Any]:
    result = compose(question, knowledge)
    return {
        "answer": result.answer,
        "category": result.category,
        "support": result.support,
        "recommended_next_action": result.next_action,
        "cta_eligible": result.cta_eligible,
        "voice_text": result.voice_text,
        "source_ids": list(result.source_ids),
    }


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:])
    print(json.dumps(answer(q), indent=2, ensure_ascii=False))
