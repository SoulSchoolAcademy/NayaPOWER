#!/usr/bin/env python3
"""Corpus Store tests (B2). Run: python3 test_corpus.py (stdlib only).

Pins the store's contract: the declared population lands whole, with
aliases extracted and provenance naming exactly which source fed each
field; merges UNION (a later source never deletes), and the artifact is
byte-deterministic — the same inputs regenerate the same store, because
B3's header binds to its hash.
"""
import json, os

import corpus as c
from smart_match import FIELDS
from welcome_engine import ALIAS_RE

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_ALIASES = {
    "naya-power", "nitro", "resolve",
    "space-nayapower", "space-ask-naya", "space-smart-mail",
    "space-team-nitro", "space-mirror", "space-one-flow",
    "space-one-hub", "space-smart-factory", "space-voice",
}


def _finished(alias, answers, ts):
    return {"session_id": f"s-{alias}", "flow": "welcome", "event": "finished",
            "step_key": None, "step_index": None, "owner_alias": alias,
            "via": "tap", "answers": answers, "created_at": ts}


def test_declared_population_is_the_corpus():
    store = c.build_corpus()
    assert store["artifact"] == "welcome-engine-corpus/v1"
    assert store["sources"] == ["declared"]
    assert store["entity_count"] == 12
    assert set(store["entities"]) == EXPECTED_ALIASES
    kinds = {}
    for e in store["entities"].values():
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    assert kinds == {"citizen": 3, "space": 9}


def test_entity_shape_and_provenance_names_coverage():
    store = c.build_corpus()
    for alias, e in store["entities"].items():
        assert set(e) == {"alias", "name", "kind", "vector", "provenance", "value"}
        assert e["alias"] == alias and ALIAS_RE.match(alias)
        assert set(e["vector"]) == set(FIELDS) and set(e["provenance"]) == set(FIELDS)
        assert e["value"] is None  # no source declares a value record today
        for f in FIELDS:
            terms = e["vector"][f]
            assert terms == sorted(set(terms))  # canonical: sorted, unique
            # provenance names a field's source exactly when it carries terms
            assert e["provenance"][f] == (["declared"] if terms else [])


def test_alias_of_shapes():
    assert c.alias_of("nitro (Naya N Narzan, Nitro/Executor/Verifier)") == "nitro"
    assert c.alias_of("NayaPOWER (space-nayapower)") == "space-nayapower"
    assert c.alias_of("bare-alias") == "bare-alias"


def test_intake_merge_unions_and_names_provenance():
    rows = [_finished("nitro",
                      {"flow": "welcome", "owner_alias": "nitro",
                       "offers": "proofreading", "needs": "quiet focus time"},
                      "2026-10-25T02:00:00Z"),
            _finished("ada-new",
                      {"flow": "welcome", "owner_alias": "ada-new",
                       "into": "urban gardening", "offers": "garden design"},
                      "2026-10-25T02:01:00Z")]
    store = c.build_corpus(intake_rows=rows)
    assert store["sources"] == ["declared", "intake"]
    assert store["entity_count"] == 13
    nitro = store["entities"]["nitro"]
    # union: every declared offer survives, the walked offer joins it
    assert "proofreading" in nitro["vector"]["offers"]
    assert "execution" in nitro["vector"]["offers"]
    assert "quiet focus time" in nitro["vector"]["needs"]
    assert nitro["provenance"]["offers"] == ["declared", "intake"]
    assert nitro["provenance"]["needs"] == ["declared", "intake"]
    assert nitro["provenance"]["topics"] == ["declared"]  # untouched stays single-source
    ada = store["entities"]["ada-new"]
    assert ada["kind"] == "citizen"
    assert ada["provenance"]["topics"] == ["intake"]
    assert ada["provenance"]["offers"] == ["intake"]
    assert ada["provenance"]["goals"] == []  # no signal, named as none


def test_page_source_merges_last():
    pages = {"space-paper-arts": {"kind": "space", "name": "Paper Arts (space-paper-arts)",
                                  "vector": {"topics": ["origami"], "goals": [],
                                             "offers": ["paper folding"], "needs": [],
                                             "wants": []}},
             "resolve": {"kind": "citizen",
                         "vector": {"topics": ["origami"], "goals": [], "offers": [],
                                    "needs": [], "wants": []}},
             "junk": {"kind": "space", "vector": "not-a-dict"},
             "junk2": "not-a-dict"}
    store = c.build_corpus(page_declarations=pages)
    assert store["sources"] == ["declared", "page"]
    assert "junk" not in store["entities"] and "junk2" not in store["entities"]
    spa = store["entities"]["space-paper-arts"]
    assert spa["kind"] == "space" and spa["provenance"]["topics"] == ["page"]
    res = store["entities"]["resolve"]
    assert "origami" in res["vector"]["topics"] and "blockers" in res["vector"]["topics"]
    assert res["provenance"]["topics"] == ["declared", "page"]


def test_value_slot_holds_records_only():
    pages = {"space-valued": {"kind": "space",
                              "vector": {"topics": ["ledgers"], "goals": [], "offers": [],
                                         "needs": [], "wants": []},
                              "value": {"state": "VERIFIED", "value": 0.5}},
             "space-bare": {"kind": "space",
                            "vector": {"topics": ["ledgers"], "goals": [], "offers": [],
                                       "needs": [], "wants": []},
                            "value": 0.5}}  # a bare float is NOT a record (engine contract)
    store = c.build_corpus(page_declarations=pages)
    assert store["entities"]["space-valued"]["value"] == {"state": "VERIFIED", "value": 0.5}
    assert store["entities"]["space-bare"]["value"] is None


def test_determinism_bytes_and_hash():
    rows = [_finished("ada-new", {"into": "urban gardening", "offers": "garden design"},
                      "2026-10-25T02:01:00Z"),
            _finished("bob-new", {"into": "chess", "wants": "chess partners"},
                      "2026-10-25T02:02:00Z")]
    a = c.build_corpus(intake_rows=rows)
    b = c.build_corpus(intake_rows=list(reversed(rows)))  # fold is by created_at
    assert c.corpus_bytes(a) == c.corpus_bytes(b)
    assert c.corpus_hash(a) == c.corpus_hash(b)
    assert c.corpus_hash(c.build_corpus()) == c.corpus_hash(c.build_corpus())


def test_store_roundtrip():
    store = c.build_corpus()
    path = os.path.join(HERE, ".test-corpus-roundtrip.json")
    try:
        c.write_corpus(store, path)
        back = c.read_corpus(path)
        assert back == store and c.corpus_hash(back) == c.corpus_hash(store)
    finally:
        if os.path.exists(path):
            os.remove(path)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
