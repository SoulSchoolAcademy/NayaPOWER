#!/usr/bin/env python3
"""IDF Decision Harness tests (B6). Run: python3 test_idf_eval.py
(stdlib only) or under pytest.

Pins the harness to the engine and to its honesty contract: indexed
rankings are EXACTLY the naive rankings on the real corpus; the golden
set and the holdout are each scored in both modes (OFF and ON, at both
thresholds) with every case present; the decision artifact is valid
JSON carrying the required sections; and running the harness changes
no engine default — it informs the flip decision, it never makes it.
No empirical pair value from any run is asserted here: measurements
belong to the harness output, not to the tests."""
import inspect, json, os, tempfile

import golden_set
import holdout_set
import idf_eval as h
import smart_match as m

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(HERE, "corpus.json")

REPORT = None  # built once, shared by the read-only tests


def _report():
    global REPORT
    if REPORT is None:
        REPORT = h.build_report(CORPUS_PATH)
    return REPORT


def _real_vectors():
    store, _path = h.load_real_corpus(CORPUS_PATH)
    return {a: e["vector"] for a, e in store["entities"].items()}


# ---- the scale guard: indexed == naive on the real corpus ------------------

def test_indexed_identical_to_naive_on_real_corpus():
    vectors = _real_vectors()
    index = m.build_index(vectors)
    legs = {"off": None, **h._idf_legs(list(vectors.values()))}
    for leg, idf in legs.items():
        for alias, vec in vectors.items():
            naive = m.rank_matches(vec, vectors, self_name=alias, idf=idf)
            fast = m.rank_matches_indexed(vec, vectors, index=index,
                                          self_name=alias, idf=idf)
            assert fast == naive, (leg, alias)  # exact row equality


def test_identity_check_recorded_and_true():
    ic = _report()["real_corpus"]["identity_check"]
    assert ic["identical"] is True
    assert ic["rankings_match_pair_matrix"] is True
    assert ic["entities_checked"] == len(_real_vectors())
    for leg in ("off", "on_default", "on_ge50"):
        assert ic["legs"][leg]["identical"] is True
        assert ic["legs"][leg]["rows_compared"] > 0


# ---- labeled sets: both modes, every case ----------------------------------

def test_golden_and_holdout_scored_in_both_modes():
    labeled = _report()["labeled_sets"]
    expected = {
        "golden": len(golden_set.PAIRS) + len(golden_set.TOP1),
        "holdout": len(holdout_set.PAIRS) + len(holdout_set.ORDERINGS),
    }
    for name, count in expected.items():
        s = labeled[name]
        assert s["total_cases"] == count, name
        assert len(s["cases"]) == count, name
        for case in s["cases"]:
            for leg in ("off", "on_default", "on_ge50"):
                assert leg in case, (name, case["label"], leg)
                assert f"passed_{leg}" in case, (name, case["label"], leg)
        for leg in ("off", "on_default", "on_ge50"):
            assert s[f"accuracy_{leg}"] is not None
            assert s[f"passed_{leg}"] <= s["scored_cases"]
    # the golden set's one informational case is scored, never counted
    golden = labeled["golden"]
    assert golden["scored_cases"] == golden["total_cases"] - 1


def test_idf_on_does_not_crash_on_real_corpus():
    real = _report()["real_corpus"]
    assert real["entity_count"] > 0 and real["pairs"]
    for row in real["pairs"]:
        for key in ("score_off", "score_on", "score_on_default",
                    "score_on_ge50"):
            assert isinstance(row[key], int) and 0 <= row[key] <= 100
        assert row["delta"] == row["score_on"] - row["score_off"]
        assert isinstance(row["survived_at_ge50"], bool)


# ---- the decision artifact --------------------------------------------------

def test_decision_artifact_structure():
    report = _report()
    blob = json.loads(h.report_bytes(report).decode("utf-8"))  # valid JSON
    assert blob["artifact"] == "welcome-engine-idf-decision/v1"
    assert set(blob) >= {"artifact", "engine", "generated_from", "idf",
                         "labeled_sets", "real_corpus", "summary"}
    assert set(blob["labeled_sets"]) == {"golden", "holdout"}
    real = blob["real_corpus"]
    assert set(real) >= {"identity_check", "pairs", "aggregates",
                         "ubiquity_table", "ubiquity_summary"}
    for row in real["pairs"]:
        assert set(row) >= {"pair", "a", "b", "score_off", "score_on",
                            "delta", "survived_at_ge50",
                            "surfaced_off", "surfaced_on_ge50"}
    agg = real["aggregates"]
    assert set(agg) >= {"pairs_surfaced_off", "pairs_surfaced_on_default",
                        "pairs_surfaced_on_ge50", "pairs_lost_ge50",
                        "pairs_gained_ge50", "top2_off", "top2_on_ge50",
                        "top2_set_stable_on_ge50", "most_deflated_ge50"}
    assert agg["pairs_surfaced_off"] == sum(
        1 for r in real["pairs"] if r["surfaced_off"])
    summary = blob["summary"]
    assert summary["facts"] and summary["recommendation_rule"]
    assert summary["decision_made"] is False
    assert summary["default_changed"] is False


def test_cli_writes_valid_json_artifact(tmp_path=None):
    out = os.path.join(tempfile.mkdtemp(), "idf_decision.json")
    assert h.main([CORPUS_PATH, out]) == 0
    with open(out) as fh:
        blob = json.load(fh)
    assert blob["artifact"] == "welcome-engine-idf-decision/v1"
    assert blob["summary"]["default_changed"] is False


# ---- the harness informs; it does not flip ---------------------------------

def test_engine_defaults_untouched_after_run():
    _report()
    assert inspect.signature(m.compute_idf).parameters["threshold"].default == 0.5
    assert inspect.signature(m.compute_idf).parameters["factor"].default == 0.25
    assert inspect.signature(m.rank_matches).parameters["idf"].default is None
    assert inspect.signature(m.rank_matches_indexed).parameters["idf"].default is None
    assert inspect.signature(m.score).parameters["idf"].default is None


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
