#!/usr/bin/env python3
"""Match Derivation tests (B3). Run: python3 test_derive_matches.py (stdlib only).

Pins the derivation to the engine and to honesty: derivation rows are
IDENTICAL to direct rank_matches rows on the same corpus (the derivation
groups and names — it never re-scores); two runs are byte-identical; and
the four island spaces are named in insufficient_signal with their
per-field coverage, instead of vanishing silently.
"""
import json, os

import corpus as c
import derive_matches as d
from smart_match import WEIGHTS, rank_matches

HERE = os.path.dirname(os.path.abspath(__file__))
ISLANDS = {"space-smart-mail", "space-mirror", "space-one-flow", "space-voice"}


def _finished(alias, answers, ts):
    return {"session_id": f"s-{alias}", "flow": "welcome", "event": "finished",
            "step_key": None, "step_index": None, "owner_alias": alias,
            "via": "tap", "answers": answers, "created_at": ts}


def test_identity_with_direct_engine():
    store = c.build_corpus()
    out = d.derive(store)
    vectors = {a: e["vector"] for a, e in store["entities"].items()}
    by_kind = {}
    for a, e in store["entities"].items():
        by_kind.setdefault(e["kind"], {})[a] = vectors[a]
    for alias, sections in out["citizens"].items():
        for kind, label in d.SECTIONS:
            direct = rank_matches(vectors[alias], by_kind.get(kind, {}), self_name=alias)
            expected = [{"alias": r["name"], "kind": kind, "score": r["score"],
                         "reasons": r["reasons"],
                         "signal_coverage_percent": r["signal_coverage_percent"],
                         "calibrated": r["calibrated"]} for r in direct]
            assert sections[label] == expected, (alias, label)


def test_header_and_output_contract():
    store = c.build_corpus()
    out = d.derive(store)
    assert out["generated_from"] == c.corpus_hash(store)
    assert out["entity_count"] == 12 and out["weights"] == WEIGHTS
    assert "smart_match" in out["engine"]
    assert set(out["citizens"]) == {"naya-power", "nitro", "resolve"}
    for sections in out["citizens"].values():
        assert set(sections) == {"people", "spaces", "projects"}
        for label, rows in sections.items():
            for r in rows:
                assert set(r) == {"alias", "kind", "score", "reasons",
                                  "signal_coverage_percent", "calibrated"}
                assert r["calibrated"] is True and r["reasons"]
                assert r["kind"] == {"people": "citizen", "spaces": "space",
                                     "projects": "project"}[label]


def test_determinism_two_runs_byte_identical():
    store = c.build_corpus()
    a, b = d.derive(store), d.derive(c.build_corpus())
    assert d.matches_bytes(a) == d.matches_bytes(b)
    assert a["generated_from"] == b["generated_from"]


def test_island_honesty():
    store = c.build_corpus()
    out = d.derive(store)
    named = {e["alias"] for e in out["insufficient_signal"]}
    assert named == ISLANDS
    for e in out["insufficient_signal"]:
        vec = store["entities"][e["alias"]]["vector"]
        assert e["surfaced_pairs"] == 0
        assert e["empty_fields"] == [f for f in ("topics", "goals", "offers", "needs", "wants")
                                     if not vec[f]]
        assert e["field_term_counts"] == {f: len(vec[f]) for f in vec}
        for sections in out["citizens"].values():
            for rows in sections.values():
                assert all(r["alias"] != e["alias"] for r in rows)


def test_citizen_top_matches():
    out = d.derive(c.build_corpus())
    nitro_spaces = out["citizens"]["nitro"]["spaces"]
    assert nitro_spaces[0]["alias"] == "space-team-nitro" and nitro_spaces[0]["score"] == 62
    power_spaces = out["citizens"]["naya-power"]["spaces"]
    assert power_spaces[0]["alias"] == "space-nayapower" and power_spaces[0]["score"] == 57
    resolve = out["citizens"]["resolve"]
    assert resolve["spaces"] == [] and resolve["projects"] == []
    assert resolve["people"][0]["alias"] == "naya-power" and resolve["people"][0]["score"] == 14


def test_end_to_end_intake_to_derivation():
    rows = [_finished("ada", {"into": "urban gardening", "offers": "garden design",
                              "needs": "accounting help"}, "2026-10-25T02:00:00Z"),
            _finished("bob", {"into": "urban gardening", "offers": "accounting help",
                              "needs": "garden design"}, "2026-10-25T02:01:00Z"),
            _finished("nul", {"motto": "just a motto"}, "2026-10-25T02:02:00Z")]
    store = c.build_corpus(intake_rows=rows)
    assert "ada" in store["entities"] and "bob" in store["entities"]
    assert "nul" not in store["entities"]  # no signal -> never a zero-vector citizen
    out = d.derive(store)
    bob_row = [r for r in out["citizens"]["ada"]["people"] if r["alias"] == "bob"]
    assert bob_row and any(x.startswith("offer/need fit") for x in bob_row[0]["reasons"])


def test_new_entry_changes_only_affected_citizens():
    pages = {"space-paper-arts": {"kind": "space",
                                  "vector": {"topics": ["execution", "testing"],
                                             "goals": ["ship fast"],
                                             "offers": ["scheduling"],
                                             "needs": ["testing"], "wants": []}}}
    before = d.derive(c.build_corpus())
    after = d.derive(c.build_corpus(page_declarations=pages))
    assert before["citizens"]["resolve"] == after["citizens"]["resolve"]
    assert before["citizens"]["naya-power"] == after["citizens"]["naya-power"]
    assert before["citizens"]["nitro"] != after["citizens"]["nitro"]
    assert any(r["alias"] == "space-paper-arts" for r in after["citizens"]["nitro"]["spaces"])
    assert before["insufficient_signal"] == after["insufficient_signal"]


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
