"""Applicability-metadata layer tests (Naya Beta, KNOW lane, 2026-10-11).

GRAND-TODO P1: retrieval must know WHICH knowledge applies to WHICH context.
The ground-truth table below is hand-labeled by reading the real registry
entries (.naya/memory/smart-notes/index.json); the tagger must reproduce it.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


applicability = _load("applicability", "tools/applicability.py")


def _registry_entries():
    reg = json.loads(
        (ROOT / ".naya" / "memory" / "smart-notes" / "index.json")
        .read_text(encoding="utf-8"))
    return reg["entries"]


# index -> expected (areas, confidence). Hand-labeled from the real corpus.
GROUND_TRUTH = {
    0:   ({"LEARN", "KNOW"}, 0.7),             # Official Smart Note Format & Lifecycle (topic SMART_NOTE_SYSTEM; generic capture stamps are not signal)
    2:   ({"SUCCESSOR", "KNOW"}, 0.7),          # Naya Continuation Engine
    4:   ({"LAW", "HUMAN_VALUE"}, 0.7),         # Internal Morality
    7:   ({"HUMAN_VALUE"}, 0.7),                # Human Reconstruction Is an Architectural Failure
    50:  ({"LAW", "TEAM"}, 0.9),                # Iteration Law (subtopic GOVERNANCE)
    120: ({"TEAM"}, 0.9),                       # Lane-seam reporting (subtopic OPERATING-MODE)
    300: ({"INFRA"}, 0.9),                      # Sibling-gap hardening (subtopic CI-TRIAGE)
    396: ({"SUCCESSOR", "KNOW"}, 0.9),          # Canonical persistence (subtopic INTELLIGENCE-CONTINUITY)
    413: ({"KNOW", "LEARN"}, 0.9),             # Direct-commit capture bypass (subtopic MEMORY-DISCIPLINE; title is about the capture pipeline)
    600: ({"VERIFY", "KNOW"}, 0.9),             # Retain the UNKNOWN (subtopic ENGINEERING-PROOF)
    620: ({"INFRA"}, 0.9),                      # Byte-identical CI green (subtopic CI-TRIAGE)
    247: ({"ACT", "KNOW"}, 0.9),                # Canary learning-loop proof (subtopic ACTIVE-INTELLIGENCE)
}


class TestTaggerOnRealUnits:
    @pytest.mark.parametrize("idx,expected", list(GROUND_TRUTH.items()))
    def test_sample_tag_matches_hand_label(self, idx, expected):
        areas, confidence = expected
        entry = _registry_entries()[idx]
        tag = applicability.tag_entry(entry)
        assert set(tag["areas"]) == areas, (
            f"entry {idx} ({entry.get('title','')[:50]}): "
            f"got {tag['areas']}, want {sorted(areas)}")
        assert tag["confidence"] == confidence
        assert tag["source"] == "heuristic"
        assert tag["schema_version"] == applicability.SCHEMA_VERSION
        assert not tag["needs_review"]
        # areas must come from the 12-area vocabulary
        assert set(tag["areas"]) <= set(applicability.AREAS)
        # every area must map to at least one task context
        assert tag["task_contexts"], f"entry {idx}: no task contexts derived"


class TestSchemaContract:
    def test_full_corpus_tags_are_valid(self):
        entries = _registry_entries()
        rules = applicability.load_rules()
        tags = applicability.tag_corpus(entries, rules)
        assert len(tags) == len(entries)
        review = [t for t in tags if t["needs_review"]]
        for t in tags:
            assert set(t["areas"]) <= set(applicability.AREAS)
            assert set(t["task_contexts"]) <= set(applicability.TASK_CONTEXTS)
            assert 0.0 <= t["confidence"] <= 1.0
            assert t["source"] == "heuristic"
            assert isinstance(t["law_refs"], list)
            if not t["needs_review"]:
                assert t["areas"] and t["task_contexts"]
            if not t["areas"]:
                assert t["needs_review"] and t["confidence"] == 0.0
        # recorded coverage floor: >90% of the live corpus must tag without review
        assert len(review) / len(tags) < 0.10, (
            f"{len(review)}/{len(tags)} entries need review")

    def test_no_false_law_refs_on_bare_titles(self):
        entry = _registry_entries()[413]
        assert applicability.extract_law_refs(entry) == []


class TestLawRefExtraction:
    def test_extracts_sn_and_directive_refs(self):
        entry = {
            "title": "Judgment Rule SN-016 and Directive D29 on Cold Successor",
            "keywords": ["SN-0522 self-governing intelligence"],
            "category": "SYSTEM_INTELLIGENCE", "topic": "X", "subtopic": "Y",
        }
        refs = applicability.extract_law_refs(entry)
        assert "SN-016" in refs
        assert "SN-0522" in refs
        assert "D29" in refs
        assert len(refs) == len(set(refs))  # deduped


class TestFilter:
    def _entries(self):
        return _registry_entries()

    def test_identity_when_no_dimensions(self):
        entries = self._entries()
        assert applicability.filter_entries(entries) == list(entries)

    def test_area_filter_is_exact(self):
        entries = self._entries()
        kept = applicability.filter_entries(entries, areas=["SUCCESSOR"])
        assert kept, "SUCCESSOR filter returned nothing on the live corpus"
        cache = {}
        for e in kept:
            tag = applicability._entry_tag(e, cache)
            assert "SUCCESSOR" in tag["areas"]

    def test_context_filter(self):
        entries = self._entries()
        kept = applicability.filter_entries(
            entries, task_contexts=["successor-handoff"])
        assert kept
        cache = {}
        for e in kept:
            assert "successor-handoff" in applicability._entry_tag(e, cache)["task_contexts"]

    def test_mode_all_requires_both_dimensions(self):
        entries = self._entries()
        kept = applicability.filter_entries(
            entries, areas=["KNOW"], task_contexts=["capture"], mode="all")
        cache = {}
        for e in kept:
            tag = applicability._entry_tag(e, cache)
            assert "KNOW" in tag["areas"] and "capture" in tag["task_contexts"]

    def test_mode_any_widens(self):
        entries = self._entries()
        any_kept = applicability.filter_entries(
            entries, areas=["INFRA"], task_contexts=["successor-handoff"], mode="any")
        all_kept = applicability.filter_entries(
            entries, areas=["INFRA"], task_contexts=["successor-handoff"], mode="all")
        assert len(any_kept) >= len(all_kept)

    def test_law_refs_dimension(self):
        entry = {
            "smart_note_id": "SN-TEST-1",
            "title": "Self-Governing Intelligence SN-0522 ratified",
            "category": "SYSTEM_INTELLIGENCE", "topic": "DOCTRINE",
            "subtopic": "DOCTRINE", "keywords": [],
        }
        entries = [entry] + self._entries()
        kept = applicability.filter_entries(entries, law_refs=["SN-0522"])
        assert entry in kept
        assert len(kept) < len(entries)

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError):
            applicability.filter_entries(self._entries(), areas=["KNOW"], mode="bogus")

    def test_filter_does_not_mutate_entries(self):
        entries = self._entries()
        before = [json.dumps(e, sort_keys=True, default=str) for e in entries[:20]]
        applicability.filter_entries(entries[:20], areas=["KNOW"])
        after = [json.dumps(e, sort_keys=True, default=str) for e in entries[:20]]
        assert before == after

    def test_precomputed_tag_is_honored(self):
        entries = self._entries()
        e = dict(entries[0])
        e["applicability"] = {
            "entry_id": "manual", "schema_version": "1.0",
            "areas": ["HUMAN_VALUE"], "task_contexts": ["human-value"],
            "law_refs": [], "confidence": 1.0, "source": "manual",
            "needs_review": False,
        }
        kept = applicability.filter_entries([e], areas=["HUMAN_VALUE"])
        assert kept == [e]


class TestRetrievalWiring:
    def _retrieve(self):
        tools_dir = str(ROOT / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        return _load("smart_note_v2_wired", "tools/smart_note_v2.py")

    def test_retrieve_accepts_area_scope(self):
        snv2 = self._retrieve()
        ranked = snv2._ranked_candidates("cold retrieve drill", areas=["RETRIEVAL"])
        # every scored candidate must carry the RETRIEVAL tag
        assert ranked, "area-scoped candidate pool is empty"
        cache = {}
        for score, rank, e in ranked:
            assert "RETRIEVAL" in applicability._entry_tag(e, cache)["areas"]

    def test_unscoped_retrieve_unchanged(self):
        snv2 = self._retrieve()

        def ids(ranked):
            return [(e.get("smart_note_id"), e.get("intelligent_block_id"))
                    for _, _, e in ranked]

        scoped = ids(snv2._ranked_candidates("smart note format"))
        unscoped = ids(snv2._ranked_candidates("smart note format", areas=None))
        assert scoped == unscoped

    def test_cli_flags_exist(self):
        import subprocess
        out = subprocess.run(
            [sys.executable, "tools/smart_note_v2.py", "retrieve", "--help"],
            cwd=ROOT, capture_output=True, text=True, timeout=30)
        assert "--area" in out.stdout and "--context" in out.stdout
