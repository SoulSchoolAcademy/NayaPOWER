#!/usr/bin/env python3
"""Applicability metadata for the KNOW retrieval layer (Naya Beta, KNOW lane).

The gap (GRAND-TODO P1, Beta/Theta): brain-index freshness is green, but
retrieval does not know WHICH knowledge applies to WHICH context. This module
adds the applicability-metadata layer WITHOUT creating a second store — tags
are computed deterministically from the existing registry taxonomy
(category/topic/subtopic/keywords) and cached per entry id.

APPLICABILITY_SCHEMA (v1):
    {
        "entry_id":        <smart_note_id or intelligent_block_id>,
        "areas":           [12 Team Naya area codes the unit serves, ordered],
        "task_contexts":   [retrieval-facing contexts: cold-retrieve, briefing,
                            scorecard, merge-gate, dispatch, capture, verify,
                            trial, successor-handoff, human-value],
        "law_refs":        [standing-law / Smart Note refs extracted from the
                            entry title+keywords, e.g. "SN-0522", "D29"],
        "confidence":      0.0..1.0 for the heuristic tag,
        "source":          "heuristic" | "manual",
        "needs_review":    True when no rule matched the unit,
    }

Confidence ladder:
    0.9  subtopic rule matched (most specific)
    0.7  topic rule matched (no subtopic rule)
    0.5  keyword rule only
    0.0  nothing matched -> areas empty, needs_review True

Wiring: tools/smart_note_v2.py retrieve(query, areas=..., task_contexts=...)
applies filter_entries() to the candidate pool before scoring, so retrieval
can be scoped to the caller's context without changing default behavior.

Rule table lives in tools/applicability_rules.json so other lanes (Theta)
can tune rules without touching code.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RULES_PATH = Path(__file__).with_name("applicability_rules.json")

SCHEMA_VERSION = "1.0"

# The 12 Team Naya area codes (TEAM-STRUCTURE.md, 2026-10-11).
AREAS = [
    "LEARN", "KNOW", "ACT", "LAW", "VERIFY", "BLOCKS",
    "DECISION", "RETRIEVAL", "SUCCESSOR", "TEAM", "INFRA", "HUMAN_VALUE",
]

# Retrieval-facing task contexts. Must match area_contexts keys in the rules file.
TASK_CONTEXTS = [
    "cold-retrieve", "briefing", "scorecard", "merge-gate", "dispatch",
    "capture", "verify", "trial", "successor-handoff", "human-value",
]

_LAW_SN = re.compile(r"\bSN-\d{3,4}\b")
_LAW_DIRECTIVE = re.compile(r"\bD\d{2}\b")
_LAW_LAWNUM = re.compile(r"\bLAW[- ]?0*\d{1,4}\b", re.I)


def load_rules(path=RULES_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


# Capture stamps every note with the same generic keywords, so the metadata
# haystack cannot distinguish lessons (retrieval track, 2026-10-06). These
# stamps are excluded from keyword-rule matching; they are pipeline
# fingerprint, not topical signal.
GENERIC_STAMP_KEYWORDS = frozenset({
    "smart note", "capture", "intelligent block", "future naya",
    "superbrain", "intent", "memory", "reusable intelligence",
})


def _entry_id(entry):
    return entry.get("smart_note_id") or entry.get("intelligent_block_id") or "UNKNOWN"


def _haystack(entry):
    keywords = [k for k in (entry.get("keywords", []) or [])
                if k.lower() not in GENERIC_STAMP_KEYWORDS]
    parts = [
        entry.get("title", ""),
        entry.get("category", ""),
        entry.get("topic", ""),
        entry.get("subtopic", ""),
        " ".join(keywords),
    ]
    return "\n".join(parts)


def extract_law_refs(entry):
    """Standing-law / Smart Note refs cited by the entry (title + keywords)."""
    text = "\n".join([entry.get("title", ""),
                      " ".join(entry.get("keywords", []) or [])])
    refs = []
    for pat in (_LAW_SN, _LAW_DIRECTIVE, _LAW_LAWNUM):
        for m in pat.findall(text):
            ref = m.upper().replace("LAW ", "LAW-")
            if ref not in refs:
                refs.append(ref)
    return refs


def tag_entry(entry, rules=None):
    """Tag one registry entry. Deterministic, non-mutating."""
    rules = rules or load_rules()
    areas = []
    confidence = 0.0
    subtopic = (entry.get("subtopic") or "").strip()
    topic = (entry.get("topic") or "").strip()

    if subtopic and subtopic in rules.get("subtopic_rules", {}):
        areas = list(rules["subtopic_rules"][subtopic])
        confidence = 0.9
    elif topic and topic in rules.get("topic_rules", {}):
        areas = list(rules["topic_rules"][topic])
        confidence = 0.7

    # Keyword rules are ADDITIVE to taxonomy rules.
    haystack = _haystack(entry).lower()
    kw_hit = False
    for rule in rules.get("keyword_rules", []):
        if rule.get("match", "").lower() in haystack:
            kw_hit = True
            for a in rule.get("areas", []):
                if a not in areas:
                    areas.append(a)
    if not areas and kw_hit:
        confidence = 0.5

    # Drop anything outside the 12-area vocabulary; preserve order.
    areas = [a for a in areas if a in AREAS]

    area_contexts = rules.get("area_contexts", {})
    task_contexts = []
    for a in areas:
        for c in area_contexts.get(a, []):
            if c in TASK_CONTEXTS and c not in task_contexts:
                task_contexts.append(c)

    needs_review = not areas
    return {
        "entry_id": _entry_id(entry),
        "schema_version": SCHEMA_VERSION,
        "areas": areas,
        "task_contexts": task_contexts,
        "law_refs": extract_law_refs(entry),
        "confidence": confidence,
        "source": "heuristic",
        "needs_review": needs_review,
    }


def tag_corpus(entries, rules=None):
    """Tag every entry; returns the tag list in entry order. Non-mutating."""
    rules = rules or load_rules()
    return [tag_entry(e, rules) for e in entries]


def _entry_tag(entry, cache):
    """Use a precomputed 'applicability' tag on the entry if present,
    otherwise compute (and memoize) it. Cache is keyed by object identity
    because entry ids are not unique in the live corpus (the retrieval
    audit tracks duplicate smart_note_id as a defect class)."""
    if isinstance(entry.get("applicability"), dict):
        return entry["applicability"]
    key = id(entry)
    if key not in cache:
        cache[key] = tag_entry(entry)
    return cache[key]


def filter_entries(entries, areas=None, task_contexts=None, law_refs=None,
                   mode="any"):
    """Filter entries by applicability dimensions. Non-mutating.

    mode="any": keep entries matching at least one requested value across
        all specified dimensions.
    mode="all": keep entries matching at least one requested value in EACH
        specified dimension.
    No dimensions -> identity (returns the list as-is).
    """
    if mode not in ("any", "all"):
        raise ValueError(f"unknown filter mode: {mode!r}")
    dims = [("areas", areas), ("task_contexts", task_contexts),
            ("law_refs", law_refs)]
    dims = [(name, set(v)) for name, v in dims if v]
    if not dims:
        return list(entries)
    cache = {}
    kept = []
    for e in entries:
        tag = _entry_tag(e, cache)
        hits = [bool(set(tag.get(name, [])) & want) for name, want in dims]
        if (any(hits) if mode == "any" else all(hits)):
            kept.append(e)
    return kept


def _repo_root():
    return Path(__file__).resolve().parents[1]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Applicability-metadata layer for KNOW retrieval.")
    ap.add_argument("--root", default=str(_repo_root()))
    ap.add_argument("--sample", type=int, default=0,
                    help="tag the first N registry entries and print a summary")
    ap.add_argument("--stats", action="store_true",
                    help="print coverage stats over the full registry")
    args = ap.parse_args(argv)

    registry = json.loads(
        (Path(args.root) / ".naya" / "memory" / "smart-notes" / "index.json")
        .read_text(encoding="utf-8"))
    entries = registry.get("entries", [])
    rules = load_rules()

    if args.stats:
        tags = tag_corpus(entries, rules)
        from collections import Counter
        area_c = Counter()
        review = 0
        for t in tags:
            for a in t["areas"]:
                area_c[a] += 1
            if t["needs_review"]:
                review += 1
        print(json.dumps({
            "entries": len(entries),
            "needs_review": review,
            "coverage": {a: area_c.get(a, 0) for a in AREAS},
        }, indent=2))
        return

    n = args.sample or min(5, len(entries))
    for e in entries[:n]:
        t = tag_entry(e, rules)
        print(f"{t['entry_id']}: areas={t['areas']} ctx={t['task_contexts']} "
              f"laws={t['law_refs']} conf={t['confidence']}")


if __name__ == "__main__":
    main()
