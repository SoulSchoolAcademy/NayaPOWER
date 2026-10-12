#!/usr/bin/env python3
"""Applicability metadata for the KNOW retrieval layer (Naya Beta, KNOW lane).

The gap (GRAND-TODO P1, Beta/Theta): retrieval returns what MATCHES; it must
return what APPLIES. This module is the KNOW-side producer + schema, plus the
reference ranking implementation that the retrieval side (Naya Theta) ports.

Schema v2.0 — everything v1 had, plus the three missing dimensions:
    "entry_id":        <smart_note_id or intelligent_block_id>,
    "schema_version":  "2.0",
    "areas":           [12 Team Naya area codes the unit serves, ordered],
    "task_contexts":   [domain tags for retrieval: cold-retrieve, briefing,
                        scorecard, merge-gate, dispatch, capture, verify,
                        trial, successor-handoff, human-value],
    "law_refs":        [standing-law / Smart Note refs from title+keywords,
                        e.g. "SN-0522", "D29"],
    "freshness":       {"valid_from":  <ISO date the knowledge starts applying>,
                        "valid_until": <ISO date it stops applying | null>,
                        "ttl_days":    <int window the stamp was derived from>,
                        "assessed_at": <ISO UTC ts of the stamp>},
    "supersession":    {"superseded_by": <entry_id that replaces this | null>,
                        "supersedes":    [<entry_ids this replaces>]},
    "confidence":      0.0..1.0 for the heuristic tag,
    "source":          "heuristic" | "manual",
    "needs_review":    True when no rule matched the unit.

Confidence ladder:
    0.9  subtopic rule matched (most specific)
    0.7  topic rule matched (no subtopic rule)
    0.5  keyword rule only
    0.0  nothing matched -> areas empty, needs_review True

Producer (KNOW side): produce()/stamp_entry() attach entry["applicability"]
deterministically from the registry taxonomy + the supersession registry.
Nothing is deleted: supersession is lineage, not removal.

Ranking reference (retrieval side): rank_adjust() is the exact rule the
retrieval layer must apply. Ported one-to-one into TypeScript by Naya Theta;
see BRAIN/11-KNOWLEDGE/0005-APPLICABILITY-CONSUMER-CONTRACT-V1.md.

Rule tables live in tools/applicability_rules.json and
tools/applicability_supersession.json so other lanes can tune without
touching code.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

RULES_PATH = Path(__file__).with_name("applicability_rules.json")
SUPERSESSION_PATH = Path(__file__).with_name("applicability_supersession.json")

SCHEMA_VERSION = "2.0"
SCHEMA_VERSION_V1 = "1.0"

# The 12 Team Naya area codes (TEAM-STRUCTURE.md, 2026-10-11).
AREAS = [
    "LEARN", "KNOW", "ACT", "LAW", "VERIFY", "BLOCKS",
    "DECISION", "RETRIEVAL", "SUCCESSOR", "TEAM", "INFRA", "HUMAN_VALUE",
]

# Retrieval-facing task contexts = the domain tag vocabulary.
# Must match area_contexts keys in the rules file.
TASK_CONTEXTS = [
    "cold-retrieve", "briefing", "scorecard", "merge-gate", "dispatch",
    "capture", "verify", "trial", "successor-handoff", "human-value",
]

DEFAULT_TTL_DAYS = 365
MAX_SUPERSESSION_HOPS = 3

# Ranking multipliers (the contract; retrieval ports these verbatim).
MULT_SUPERSEDED = 0.0   # superseded record: never served as current
MULT_EXPIRED = 0.1      # valid_until < now: knowledge no longer applies
MULT_OUT_OF_SCOPE = 0.25  # caller named a scope and this record matches none of it
MULT_UNREVIEWED = 0.5   # no rule matched: tag is unreliable
MULT_LOW_CONFIDENCE = 0.8  # heuristic confidence below 0.5

_LAW_SN = re.compile(r"\bSN-\d{3,4}\b")
_LAW_DIRECTIVE = re.compile(r"\bD\d{2}\b")
_LAW_LAWNUM = re.compile(r"\bLAW[- ]?0*\d{1,4}\b", re.I)


def load_rules(path=RULES_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_supersession(path=SUPERSESSION_PATH):
    p = Path(path)
    if not p.exists():
        return {"schema_version": "1.0", "superseded_by": {}, "supersedes": {}}
    return json.loads(p.read_text(encoding="utf-8"))


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


def _utcnow_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_date(value):
    """Parse an ISO date or datetime to a date; None in -> None out."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value)).date()
    except ValueError:
        try:
            return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
        except ValueError:
            return None


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
    """Tag one registry entry with v1 dimensions. Deterministic, non-mutating."""
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


def freshness_for(entry, rules=None, now=None):
    """Derive the freshness window for one entry.

    valid_from = captured_at (or created_at). ttl_days comes from
    freshness_rules.topic_rules[topic], else the default 365. valid_until =
    valid_from + ttl_days, unless the entry is DURA-class (truth_state in
    DURABLE-class states or a 'permanent' law_ref), which gets valid_until
    None (no expiry).
    """
    rules = rules or load_rules()
    now = now or _utcnow_iso()
    fr = rules.get("freshness_rules", {})
    topic = (entry.get("topic") or "").strip()
    ttl = fr.get("topic_rules", {}).get(topic, fr.get("default_ttl_days", DEFAULT_TTL_DAYS))
    valid_from = (_parse_date(entry.get("captured_at"))
                  or _parse_date(entry.get("created_at"))
                  or _parse_date(now))
    timeless = set(fr.get("timeless_truth_states", []))
    valid_until = None
    if entry.get("truth_state") not in timeless:
        valid_until = (valid_from + timedelta(days=int(ttl))).isoformat() if ttl else None
    return {
        "valid_from": valid_from.isoformat(),
        "valid_until": valid_until,
        "ttl_days": int(ttl) if ttl else None,
        "assessed_at": now,
    }


def supersession_for(entry, supersede_map=None):
    """Supersession links for one entry, from the explicit registry."""
    supersede_map = supersede_map or load_supersession()
    eid = _entry_id(entry)
    by = supersede_map.get("superseded_by", {})
    to = supersede_map.get("supersedes", {})
    return {
        "superseded_by": by.get(eid),
        "supersedes": list(to.get(eid, [])),
    }


def produce(entry, rules=None, supersede_map=None, now=None):
    """PRODUCER: full v2.0 applicability metadata for one registry entry.

    Deterministic and non-mutating; callers persist it via stamp_entry().
    """
    tag = tag_entry(entry, rules=rules)
    tag["freshness"] = freshness_for(entry, rules=rules, now=now)
    tag["supersession"] = supersession_for(entry, supersede_map=supersede_map)
    return tag


def stamp_entry(entry, rules=None, supersede_map=None, now=None):
    """Return a COPY of the entry with entry['applicability'] stamped (v2.0)."""
    stamped = dict(entry)
    stamped["applicability"] = produce(
        entry, rules=rules, supersede_map=supersede_map, now=now)
    return stamped


def stamp_corpus(entries, rules=None, supersede_map=None, now=None):
    """Stamp every entry; returns the stamped list in entry order."""
    rules = rules or load_rules()
    supersede_map = supersede_map or load_supersession()
    return [stamp_entry(e, rules=rules, supersede_map=supersede_map, now=now)
            for e in entries]


# Schema validation -------------------------------------------------------------

REQUIRED_V2_KEYS = {
    "entry_id", "schema_version", "areas", "task_contexts", "law_refs",
    "freshness", "supersession", "confidence", "source", "needs_review",
}
REQUIRED_FRESHNESS_KEYS = {"valid_from", "valid_until", "ttl_days", "assessed_at"}
REQUIRED_SUPERSESSION_KEYS = {"superseded_by", "supersedes"}


def validate(tag):
    """Validate a v2.0 tag. Returns a list of error strings (empty = valid)."""
    errors = []
    if not isinstance(tag, dict):
        return ["tag is not a dict"]
    missing = REQUIRED_V2_KEYS - set(tag)
    if missing:
        errors.append(f"missing keys: {sorted(missing)}")
    if tag.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    bad_areas = [a for a in tag.get("areas", []) if a not in AREAS]
    if bad_areas:
        errors.append(f"areas outside vocabulary: {bad_areas}")
    bad_ctx = [c for c in tag.get("task_contexts", []) if c not in TASK_CONTEXTS]
    if bad_ctx:
        errors.append(f"task_contexts outside vocabulary: {bad_ctx}")
    conf = tag.get("confidence")
    if not isinstance(conf, (int, float)) or not (0.0 <= conf <= 1.0):
        errors.append(f"confidence out of range: {conf!r}")
    fr = tag.get("freshness")
    if isinstance(fr, dict):
        fmissing = REQUIRED_FRESHNESS_KEYS - set(fr)
        if fmissing:
            errors.append(f"freshness missing keys: {sorted(fmissing)}")
        elif _parse_date(fr.get("valid_from")) is None:
            errors.append(f"freshness.valid_from unparseable: {fr.get('valid_from')!r}")
        vu = fr.get("valid_until")
        if vu is not None and _parse_date(vu) is None:
            errors.append(f"freshness.valid_until unparseable: {vu!r}")
    else:
        errors.append("freshness must be a dict")
    su = tag.get("supersession")
    if isinstance(su, dict):
        if REQUIRED_SUPERSESSION_KEYS - set(su):
            errors.append("supersession missing keys")
        elif not isinstance(su.get("supersedes"), list):
            errors.append("supersession.supersedes must be a list")
    else:
        errors.append("supersession must be a dict")
    return errors


# Supersession resolution ---------------------------------------------------------

def supersession_head(entry, index, max_hops=MAX_SUPERSESSION_HOPS):
    """Resolve a record to its current head by following superseded_by links.

    `index` maps entry_id -> entry (entries carry entry['applicability'] or a
    plain superseded_by key). Cycle-safe, capped at max_hops. Returns
    (head_entry, lineage_ids) where lineage_ids is the followed chain.
    Missing head -> stop at the last resolvable entry.
    """
    seen = set()
    lineage = []
    current = entry
    if isinstance(current, dict):
        seen.add(_entry_id(current))  # seed: a cycle back to self stops
    for _ in range(max_hops):
        app = current.get("applicability") if isinstance(current, dict) else None
        if isinstance(app, dict):
            nxt = (app.get("supersession") or {}).get("superseded_by")
        else:
            nxt = current.get("superseded_by") if isinstance(current, dict) else None
        if not nxt or nxt in seen:
            break
        nxt_entry = index.get(nxt)
        if nxt_entry is None:
            break
        seen.add(nxt)
        lineage.append(nxt)
        current = nxt_entry
    return current, lineage


# Ranking reference (the contract) --------------------------------------------------

def rank_adjust(tag, now=None, requested_areas=None, requested_contexts=None):
    """Reference implementation of the consumer ranking rule.

    Returns {"servable": bool, "multiplier": float, "reasons": [str]}.

    Retrieval computes final_score = base_score * multiplier, then sorts.
    Records with multiplier 0.0 are never served as current knowledge.

    - Missing/unknown metadata is fail-closed: treated as needs_review
      (multiplier *= 0.5), never as fresh.
    - superseded_by set -> servable False; the consumer must resolve to the
      lineage head via supersession_head() instead of serving this record.
    - Expired (valid_until < now) -> *= 0.1. Stale knowledge demotes hard.
    - Caller named areas/contexts and the record matches none -> *= 0.25.
    """
    reasons = []
    multiplier = 1.0
    servable = True

    if not isinstance(tag, dict):
        return {"servable": True, "multiplier": MULT_UNREVIEWED,
                "reasons": ["metadata_unknown:fail_closed"]}

    sup = tag.get("supersession") or {}
    if sup.get("superseded_by"):
        servable = False
        multiplier = MULT_SUPERSEDED
        reasons.append(f"superseded_by:{sup['superseded_by']}")
        return {"servable": servable, "multiplier": multiplier, "reasons": reasons}

    fr = tag.get("freshness") or {}
    vu = _parse_date(fr.get("valid_until"))
    now_d = _parse_date(now or _utcnow_iso())
    if vu is not None and now_d is not None and vu < now_d:
        multiplier *= MULT_EXPIRED
        reasons.append(f"expired:{fr['valid_until']}")

    want = set(requested_areas or []) | set(requested_contexts or [])
    if want:
        have = set(tag.get("areas", [])) | set(tag.get("task_contexts", []))
        if not (have & want):
            multiplier *= MULT_OUT_OF_SCOPE
            reasons.append("out_of_scope")

    if tag.get("needs_review"):
        multiplier *= MULT_UNREVIEWED
        reasons.append("unreviewed_tag")
    elif isinstance(tag.get("confidence"), (int, float)) and tag["confidence"] < 0.5:
        multiplier *= MULT_LOW_CONFIDENCE
        reasons.append(f"low_confidence:{tag['confidence']}")

    return {"servable": servable, "multiplier": round(multiplier, 4),
            "reasons": reasons}


def tag_corpus(entries, rules=None):
    """Tag every entry (v2.0 full produce); returns the tag list in entry order.
    Non-mutating."""
    rules = rules or load_rules()
    supersede_map = load_supersession()
    return [produce(e, rules=rules, supersede_map=supersede_map) for e in entries]


def _upgrade_tag(tag, entry, rules=None, supersede_map=None, now=None):
    """Upgrade a v1 tag to v2.0 in place-safe fashion: keep the stamped
    areas/task_contexts/law_refs/confidence/source (the human/manual signal
    is honored), backfill freshness + supersession from the entry. Unknown
    schema versions are NOT upgraded — they are recomputed."""
    if tag.get("schema_version") == SCHEMA_VERSION:
        return tag
    if tag.get("schema_version") != SCHEMA_VERSION_V1:
        return produce(entry, rules=rules, supersede_map=supersede_map, now=now)
    upgraded = dict(tag)
    upgraded["schema_version"] = SCHEMA_VERSION
    upgraded["freshness"] = freshness_for(entry, rules=rules, now=now)
    upgraded["supersession"] = supersession_for(entry, supersede_map=supersede_map)
    return upgraded


def _entry_tag(entry, cache):
    """Use a precomputed 'applicability' tag on the entry if present,
    otherwise compute (and memoize) it. Cache is keyed by object identity
    because entry ids are not unique in the live corpus (the retrieval
    audit tracks duplicate smart_note_id as a defect class).
    A v1 tag is upgraded to v2.0 (manual stamps honored, freshness +
    supersession backfilled); unknown schema versions are recomputed, never
    trusted."""
    tag = entry.get("applicability")
    if isinstance(tag, dict):
        return _upgrade_tag(tag, entry)
    key = id(entry)
    if key not in cache:
        cache[key] = produce(entry)
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


def apply_ranking(entries, query_scores, now=None, requested_areas=None,
                  requested_contexts=None):
    """Apply the contract ranking to a scored candidate list.

    entries: candidate registry entries (stamped or not).
    query_scores: dict entry_id -> base match score (float).
    Returns a list of dicts sorted by final_score desc:
      {"entry_id", "base_score", "multiplier", "final_score",
       "servable", "reasons", "via_lineage"}.
    Superseded records resolve to their lineage head; the head inherits
    the base score of the best-scoring lineage member.
    """
    now = now or _utcnow_iso()
    index = {_entry_id(e): e for e in entries}
    cache = {}
    by_head = {}
    for e in entries:
        head, lineage = supersession_head(e, index)
        hid = _entry_id(head)
        agg = by_head.setdefault(hid, {"head": head, "lineage": set(),
                                       "base": 0.0, "members": []})
        agg["base"] = max(agg["base"], float(query_scores.get(_entry_id(e), 0.0)))
        agg["lineage"].update(lineage)
        agg["members"].append(_entry_id(e))
    ranked = []
    for hid, agg in by_head.items():
        tag = _entry_tag(agg["head"], cache)
        adj = rank_adjust(tag, now=now, requested_areas=requested_areas,
                          requested_contexts=requested_contexts)
        ranked.append({
            "entry_id": hid,
            "base_score": round(agg["base"], 4),
            "multiplier": adj["multiplier"],
            "final_score": round(agg["base"] * adj["multiplier"], 4),
            "servable": adj["servable"],
            "reasons": adj["reasons"],
            "via_lineage": sorted(agg["lineage"]),
        })
    ranked.sort(key=lambda r: (-r["final_score"], r["entry_id"]))
    return ranked


def _repo_root():
    return Path(__file__).resolve().parents[1]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Applicability-metadata layer for KNOW retrieval (v2.0).")
    ap.add_argument("--root", default=str(_repo_root()))
    ap.add_argument("--sample", type=int, default=0,
                    help="tag the first N registry entries and print a summary")
    ap.add_argument("--stats", action="store_true",
                    help="print coverage stats over the full registry")
    ap.add_argument("--validate", action="store_true",
                    help="validate produced v2.0 tags for the full registry")
    args = ap.parse_args(argv)

    registry = json.loads(
        (Path(args.root) / ".naya" / "memory" / "smart-notes" / "index.json")
        .read_text(encoding="utf-8"))
    entries = registry.get("entries", [])
    rules = load_rules()

    if args.validate:
        bad = 0
        for e in entries:
            errs = validate(produce(e, rules=rules))
            if errs:
                bad += 1
                print(f"{_entry_id(e)}: {errs}")
        print(json.dumps({"entries": len(entries), "invalid": bad}))
        return 1 if bad else 0

    if args.stats:
        tags = tag_corpus(entries, rules)
        from collections import Counter
        area_c = Counter()
        review = expired = superseded = 0
        for t in tags:
            for a in t["areas"]:
                area_c[a] += 1
            if t["needs_review"]:
                review += 1
            if t["supersession"]["superseded_by"]:
                superseded += 1
            fr = t["freshness"]
            if fr["valid_until"] and _parse_date(fr["valid_until"]) < _parse_date(_utcnow_iso()):
                expired += 1
        print(json.dumps({
            "entries": len(entries),
            "needs_review": review,
            "superseded": superseded,
            "expired": expired,
            "coverage": {a: area_c.get(a, 0) for a in AREAS},
        }, indent=2))
        return

    n = args.sample or min(5, len(entries))
    for e in entries[:n]:
        t = produce(e, rules=rules)
        fr = t["freshness"]
        su = t["supersession"]
        print(f"{t['entry_id']}: areas={t['areas']} ctx={t['task_contexts']} "
              f"laws={t['law_refs']} conf={t['confidence']} "
              f"valid_until={fr['valid_until']} superseded_by={su['superseded_by']}")


if __name__ == "__main__":
    main()
