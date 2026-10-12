#!/usr/bin/env python3
"""Applicability metadata v2.0 tests (Naya Beta, KNOW lane, 2026-10-12).

Contract vectors: these are the exact expectations the retrieval-side port
(Naya Theta, THETA-NEXT-1) must reproduce verbatim.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from applicability import (
    apply_ranking,
    freshness_for,
    load_rules,
    produce,
    rank_adjust,
    stamp_entry,
    supersession_for,
    supersession_head,
    tag_corpus,
    validate,
    MULT_EXPIRED,
    MULT_LOW_CONFIDENCE,
    MULT_OUT_OF_SCOPE,
    MULT_SUPERSEDED,
    MULT_UNREVIEWED,
    SCHEMA_VERSION,
)


def _entry(eid="IB-TEST-1", **kw):
    e = {
        "intelligent_block_id": eid,
        "title": "Decision value calculus weights for dispatch",
        "captured_at": "2026-10-01",
        "category": "SYSTEM_INTELLIGENCE",
        "topic": "VALUE_CALCULUS",
        "subtopic": "",
        "truth_state": "CANDIDATE",
        "keywords": ["dispatch", "value calculus", "weights"],
    }
    e.update(kw)
    return e


def _tag(eid="IB-TEST-1", **kw):
    t = produce(_entry(eid, **kw))
    assert validate(t) == [], f"fixture tag invalid: {validate(t)}"
    # Pin the heuristic ladder: contract vectors isolate the ranking rule.
    t["confidence"] = 0.9
    t["needs_review"] = False
    return t


class TestProducerStamping:
    def test_schema_version_is_v2(self):
        assert produce(_entry())["schema_version"] == SCHEMA_VERSION == "2.0"

    def test_freshness_derived_from_captured_at(self):
        fr = produce(_entry(captured_at="2026-09-01"))["freshness"]
        assert fr["valid_from"] == "2026-09-01"
        assert fr["valid_until"] is not None  # CANDIDATE is not timeless

    def test_timeless_truth_states_never_expire(self):
        for state in ("VERIFIED", "DISTILLED", "APPLIED", "LEARNED"):
            fr = produce(_entry(truth_state=state))["freshness"]
            assert fr["valid_until"] is None, state

    def test_topic_ttl_rule_applies(self):
        rules = load_rules()
        fr = freshness_for(_entry(topic="DAILY_NOTE"), rules=rules)
        assert fr["ttl_days"] == 30
        fr = freshness_for(_entry(topic="VALUE_CALCULUS"), rules=rules)
        assert fr["ttl_days"] == 365  # default

    def test_stamp_is_non_mutating_and_persisted(self):
        e = _entry()
        stamped = stamp_entry(e)
        assert "applicability" not in e
        assert stamped["applicability"]["entry_id"] == "IB-TEST-1"
        assert validate(stamped["applicability"]) == []

    def test_supersession_registry_empty_by_default(self):
        su = supersession_for(_entry())
        assert su == {"superseded_by": None, "supersedes": []}

    def test_validate_rejects_bad_areas(self):
        t = produce(_entry())
        t["areas"] = ["NOT_AN_AREA"]
        errs = validate(t)
        assert any("vocabulary" in x for x in errs)

    def test_validate_rejects_missing_freshness(self):
        t = produce(_entry())
        del t["freshness"]
        assert validate(t) != []

    def test_full_corpus_tags_validate(self):
        import json
        entries = json.loads(
            (ROOT / ".naya" / "memory" / "smart-notes" / "index.json")
            .read_text(encoding="utf-8"))["entries"]
        bad = 0
        for e in entries[:50]:
            if validate(produce(e)):
                bad += 1
        assert bad == 0


class TestRankingReference:
    """Contract vectors. Retrieval's port must reproduce these multipliers."""

    def test_fresh_in_scope_full_score(self):
        t = _tag()
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00",
                          requested_areas=["DECISION"])
        assert adj["servable"] is True
        assert adj["multiplier"] == 1.0, adj

    def test_expired_demotes_hard(self):
        t = _tag()
        t["freshness"]["valid_until"] = "2026-01-01"
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00")
        assert adj["multiplier"] == MULT_EXPIRED == 0.1
        assert any(r.startswith("expired:") for r in adj["reasons"])

    def test_timeless_never_expires(self):
        t = _tag(truth_state="VERIFIED")
        adj = rank_adjust(t, now="2030-01-01T00:00:00+00:00")
        assert adj["multiplier"] == 1.0

    def test_out_of_scope_demotes(self):
        t = _tag()
        t["areas"] = ["LEARN"]
        t["task_contexts"] = []
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00",
                          requested_areas=["DECISION"])
        assert adj["multiplier"] == MULT_OUT_OF_SCOPE == 0.25
        assert "out_of_scope" in adj["reasons"]

    def test_no_caller_scope_no_out_of_scope_penalty(self):
        t = _tag()
        t["areas"] = ["LEARN"]
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00")
        assert adj["multiplier"] == 1.0

    def test_unknown_metadata_fails_closed(self):
        adj = rank_adjust(None, now="2026-10-12T00:00:00+00:00")
        assert adj["multiplier"] == MULT_UNREVIEWED == 0.5
        assert "metadata_unknown:fail_closed" in adj["reasons"]

    def test_unreviewed_tag_demotes(self):
        t = _tag()
        t["needs_review"] = True
        t["areas"] = []
        t["task_contexts"] = []
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00")
        assert adj["multiplier"] == MULT_UNREVIEWED == 0.5

    def test_low_confidence_demotes(self):
        t = _tag()
        t["needs_review"] = False
        t["confidence"] = 0.3
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00")
        assert adj["multiplier"] == MULT_LOW_CONFIDENCE == 0.8

    def test_superseded_never_served_as_current(self):
        t = _tag()
        t["supersession"]["superseded_by"] = "IB-TEST-2"
        adj = rank_adjust(t, now="2026-10-12T00:00:00+00:00")
        assert adj["servable"] is False
        assert adj["multiplier"] == MULT_SUPERSEDED == 0.0
        assert "superseded_by:IB-TEST-2" in adj["reasons"]


class TestSupersessionResolution:
    def _index(self, *entries):
        return {(e.get("smart_note_id") or e.get("intelligent_block_id")): e
                for e in entries}

    def test_two_hop_chain_resolves(self):
        a = stamp_entry(_entry("IB-A", truth_state="CANDIDATE"))
        b = stamp_entry(_entry("IB-B", truth_state="VERIFIED"))
        c = stamp_entry(_entry("IB-C", truth_state="VERIFIED"))
        a["applicability"]["supersession"]["superseded_by"] = "IB-B"
        b["applicability"]["supersession"]["superseded_by"] = "IB-C"
        head, lineage = supersession_head(a, self._index(a, b, c))
        assert (head.get("smart_note_id") or head.get("intelligent_block_id")) == "IB-C"
        assert lineage == ["IB-B", "IB-C"]

    def test_cycle_stops(self):
        a = stamp_entry(_entry("IB-A"))
        b = stamp_entry(_entry("IB-B"))
        a["applicability"]["supersession"]["superseded_by"] = "IB-B"
        b["applicability"]["supersession"]["superseded_by"] = "IB-A"
        head, lineage = supersession_head(a, self._index(a, b))
        assert lineage == ["IB-B"]  # stops before looping

    def test_missing_head_stops_at_last_resolvable(self):
        a = stamp_entry(_entry("IB-A"))
        a["applicability"]["supersession"]["superseded_by"] = "IB-GHOST"
        head, lineage = supersession_head(a, self._index(a))
        assert lineage == []
        assert (head.get("smart_note_id") or head.get("intelligent_block_id")) == "IB-A"

    def test_apply_ranking_aggregates_at_head(self):
        a = stamp_entry(_entry("IB-A", title="dispatch weights old"))
        b = stamp_entry(_entry("IB-B", title="dispatch weights revised",
                               truth_state="VERIFIED"))
        a["applicability"]["supersession"]["superseded_by"] = "IB-B"
        rows = apply_ranking([a, b], {"IB-A": 2.0, "IB-B": 1.0},
                             now="2026-10-12T00:00:00+00:00")
        assert len(rows) == 1  # members never ranked separately
        row = rows[0]
        assert row["entry_id"] == "IB-B"
        assert row["base_score"] == 2.0  # head inherits best member score
        assert row["via_lineage"] == ["IB-B"]
        assert row["servable"] is True


class TestSmartNoteV2Wiring:
    def test_default_behavior_unchanged(self):
        sys.path.insert(0, str(ROOT / "tools"))
        import smart_note_v2 as sn
        off = sn._ranked_candidates("decision value calculus dispatch")
        on = sn._ranked_candidates("decision value calculus dispatch",
                                   apply_applicability_ranking=True)
        off_ids = [(e.get("smart_note_id") or e.get("intelligent_block_id"))
                   for _, _, e in off]
        on_ids = [e.get("smart_note_id") or e.get("intelligent_block_id")
                  for _, _, e in (r[:3] for r in on)]
        # Same candidate pool; ranking may reorder but nothing vanishes
        assert set(off_ids) == set(on_ids)
        # tuples from the contract pass carry the breakdown row
        assert all(len(r) == 4 and isinstance(r[3], dict) for r in on)


class TestV1Upgrade:
    def test_v1_tag_upgraded_not_recomputed(self):
        from applicability import _upgrade_tag, validate, SCHEMA_VERSION
        e = _entry("IB-V1")
        v1 = {
            "entry_id": "IB-V1", "schema_version": "1.0",
            "areas": ["HUMAN_VALUE"], "task_contexts": ["human-value"],
            "law_refs": [], "confidence": 1.0, "source": "manual",
            "needs_review": False,
        }
        up = _upgrade_tag(v1, e)
        assert up["schema_version"] == SCHEMA_VERSION
        assert up["areas"] == ["HUMAN_VALUE"]  # manual stamp honored
        assert validate(up) == []
        assert "freshness" in up and "supersession" in up

    def test_unknown_schema_recomputed(self):
        from applicability import _upgrade_tag, SCHEMA_VERSION
        e = _entry("IB-X")
        weird = {"schema_version": "9.9", "areas": ["BOGUS"]}
        up = _upgrade_tag(weird, e)
        assert up["schema_version"] == SCHEMA_VERSION
        assert up["entry_id"] == "IB-X"
