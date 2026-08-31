#!/usr/bin/env python3
"""Acceptance + deliberate-negative tests for Sales Naya V1."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from sales_naya_v1 import answer, load_knowledge, retrieve


REQUIRED_KNOWLEDGE_IDS = {
    "what_is_nayapower", "why_chatgpt", "superbrain", "smart_notes", "pis",
    "cis", "daily_intelligence", "activation", "five_day", "who_for",
    "privacy_control", "personal_naya_boundary", "out_of_scope",
}


def validate_knowledge(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("status") != "CANONICAL":
        errors.append("knowledge status must be CANONICAL")
    entries = data.get("knowledge")
    if not isinstance(entries, list) or not entries:
        return errors + ["knowledge entries are required"]
    ids = {e.get("id") for e in entries if isinstance(e, dict)}
    missing = REQUIRED_KNOWLEDGE_IDS - ids
    if missing:
        errors.append(f"missing canonical knowledge: {sorted(missing)}")
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("knowledge entry must be an object")
            continue
        for field in ("id", "intent", "answer", "source_ids"):
            if not entry.get(field):
                errors.append(f"knowledge entry missing {field}")
    return errors


def validate_boundaries(data: dict) -> list[str]:
    errors: list[str] = []
    required = [
        "Never claim the sales-page interface is the visitor's personal Naya Power.",
        "Never claim personal Superbrain, personal memory, or personal PIS access for a visitor.",
        "Never imply that chatting on the sales page activates Naya Power.",
        "Never invent pricing, privacy terms, technical requirements, integrations, or features not in verified knowledge.",
    ]
    actual = set(data.get("boundaries", []))
    for item in required:
        if item not in actual:
            errors.append(f"missing boundary: {item}")
    return errors


def validate_offer(data: dict) -> list[str]:
    promise = data.get("offer", {}).get("promise", [])
    expected = {"5 days", "5 lessons", "5 daily intelligence reports", "Zero risk"}
    return [] if set(promise) == expected else ["Five-Day Challenge promise is incomplete or contradictory"]


def acceptance() -> None:
    data = load_knowledge()
    assert validate_knowledge(data) == []
    assert validate_boundaries(data) == []
    assert validate_offer(data) == []

    checks = [
        ("What is Naya Power?", "what_is_it"),
        ("Why do I need this if I already have ChatGPT?", "differentiation"),
        ("What is the Superbrain?", "how_it_works"),
        ("What are Smart Notes?", "how_it_works"),
        ("What is PIS?", "how_it_works"),
        ("How does intelligence compound?", "how_it_works"),
        ("How does activation work?", "activation"),
        ("What is the Five-Day Challenge?", "challenge"),
        ("Who is Naya Power for?", "value"),
        ("Are you my personal Naya Power?", "boundary"),
        ("Why would I pay when ChatGPT is free?", "differentiation"),
    ]
    for question, category in checks:
        result = answer(question, data)
        assert result["category"] == category, (question, result)
        assert result["support"] == "SUPPORTED", (question, result)
        assert result["answer"].strip()
        assert result["source_ids"]
        assert result["recommended_next_action"].strip()

    boundary = answer("Are you my personal Naya Power?", data)
    assert boundary["cta_eligible"] is True
    assert "not your activated personal Naya Power" in boundary["answer"]
    assert "personal Superbrain" in boundary["answer"]

    unknown = answer("Can you guarantee my taxes will be correct?", data)
    assert unknown["support"] == "UNSUPPORTED"
    assert "don't have a verified answer" in unknown["answer"]

    challenge = answer("Is the five day challenge really five days?", data)
    assert challenge["cta_eligible"] is True
    for phrase in ("5 days", "5 lessons", "5 daily intelligence reports", "zero risk"):
        assert phrase in challenge["answer"].lower()

    print("PRODUCT UNDERSTANDING → GREEN")
    print("DIFFERENTIATION → GREEN")
    print("SUPERBRAIN → GREEN")
    print("SMART NOTES → GREEN")
    print("PIS → GREEN")
    print("COMPOUNDING → GREEN")
    print("ACTIVATION → GREEN")
    print("FIVE-DAY CHALLENGE → GREEN")
    print("PERSONAL NAYA BOUNDARY → GREEN")
    print("UNSUPPORTED QUESTION SAFETY → GREEN")
    print("CTA DECISION → GREEN")


def deliberate_failures() -> None:
    original = load_knowledge()

    missing = copy.deepcopy(original)
    missing["knowledge"] = [e for e in missing["knowledge"] if e["id"] != "smart_notes"]
    assert any("missing canonical knowledge" in e for e in validate_knowledge(missing))
    print("MISSING CANONICAL KNOWLEDGE → RED (EXPECTED)")

    false_claim = copy.deepcopy(original)
    false_claim["knowledge"].append({
        "id": "false_claim", "intent": "value", "keywords": ["magic"],
        "answer": "Naya Power guarantees every business will double revenue tomorrow.",
        "source_ids": [],
    })
    assert any(e for e in validate_knowledge(false_claim) if "source_ids" in e)
    print("UNSUPPORTED CLAIM WITHOUT SOURCE → RED (EXPECTED)")

    contradictory = copy.deepcopy(original)
    contradictory["offer"]["promise"] = ["7 days", "7 lessons"]
    assert validate_offer(contradictory)
    print("CONTRADICTORY OFFER → RED (EXPECTED)")

    no_boundary = copy.deepcopy(original)
    no_boundary["boundaries"] = [b for b in no_boundary["boundaries"] if "personal Superbrain" not in b]
    assert validate_boundaries(no_boundary)
    print("MISSING PERSONAL-ACCESS BOUNDARY → RED (EXPECTED)")

    no_cta = copy.deepcopy(original)
    no_cta["offer"]["promise"] = []
    assert validate_offer(no_cta)
    print("MISSING CTA/OFFER CONTRACT → RED (EXPECTED)")

    # Engine must remain bounded even when canonical data is malformed.
    try:
        bad = copy.deepcopy(original)
        bad["status"] = "DRAFT"
        load_path = Path("/definitely/not/a/file")
        del load_path
        from sales_naya_v1 import load_knowledge as _load
        # _load reads the real file; malformed-data safety is enforced by validate_knowledge.
        assert validate_knowledge(bad)
    except Exception as exc:
        raise AssertionError(f"unexpected test harness failure: {exc}")
    print("MALFORMED KNOWLEDGE STATUS → RED (EXPECTED)")


if __name__ == "__main__":
    acceptance()
    deliberate_failures()
    print("PASS — Sales Naya V1 acceptance + deliberate-negative tests GREEN")
