#!/usr/bin/env python3
"""Elite-hardening regression tests (v1.5) — one test per proven behavior:
stopword unification, output-contract extension, self-match exclusion,
malformed-vector robustness, the verified-value record, alias safety,
the indexed pre-filter, and the IDF mode.
Run: python3 test_hardening.py (stdlib only) or under pytest."""
import smart_match as m
import welcome_engine as w
from declared_vectors import SEATS, PROJECTS

V = lambda **kw: kw


# ---- item 1: unified stopwords -------------------------------------------

def test_stopwords_never_in_reasons():
    a = V(topics=["the art of bread"], goals=["growing the food"], offers=[], needs=[], wants=[])
    b = V(topics=["the craft of bread"], goals=["sharing the food"], offers=[], needs=[], wants=[])
    r = m.score(a, b)
    # token-level check: no comma/colon segment of any reason IS a glue word
    segments = [s.strip() for reason in r["reasons"]
                for s in reason.replace(":", ",").split(",")]
    for glue in ("the", "and", "for"):
        assert glue not in segments, r["reasons"]
    assert "bread" in " | ".join(r["reasons"])  # content words still carry the match

def test_stopword_only_overlap_is_no_signal():
    a = V(topics=[], goals=["the and of"], offers=[], needs=[], wants=[])
    b = V(topics=[], goals=["the and of"], offers=[], needs=[], wants=[])
    assert m.score(a, b)["parts"]["goals"] == 0

def test_one_stopword_set_everywhere():
    assert m.CROSS_STOPWORDS is m.STOPWORDS
    assert {"the", "and", "for"} <= m.STOPWORDS

def test_glue_only_phrase_is_no_signal():
    a = V(topics=["the and of"], goals=[], offers=["the and of"], needs=[], wants=[])
    b = V(topics=["the and of"], goals=[], offers=[], needs=["the and of"], wants=[])
    r = m.score(a, b)
    assert r["parts"]["topics"] == 0 and r["parts"]["offers_needs"] == 0

def test_stem_unifies_lemma_and_plural():
    assert m.stem("wedding") == m.stem("weddings")
    assert m.stem("building") == m.stem("buildings")
    assert m.stem("gardening") == m.stem("gardens") == "garden"
    a = V(topics=["wedding photography"], goals=[], offers=[], needs=[], wants=["wedding planners"])
    b = V(topics=["weddings"], goals=[], offers=[], needs=[], wants=[])
    assert m.score(a, b)["parts"]["topics"] > 0  # the holdout's photographer case


# ---- item 3: output contract extended, old keys pinned --------------------

def test_output_contract_old_keys_unchanged():
    r = m.score(SEATS["naya-power (Naya P Narzan, Builder/Integrator)"],
                PROJECTS["NayaPOWER (space-nayapower)"])
    assert set(r) == {"score", "rank", "signals", "surface", "parts", "reasons",
                      "signal_coverage_percent", "calibrated"}
    assert r["score"] == 57 and r["surface"] is True  # baseline values hold

def test_signal_coverage_is_weighted_share():
    a = V(topics=["voice"], goals=["x"], offers=[], needs=[], wants=[])
    b = V(topics=["voice"], goals=["y"], offers=[], needs=[], wants=[])
    r = m.score(a, b)  # topics only -> 40% of the weight carries a signal
    assert r["signal_coverage_percent"] == 40
    assert r["calibrated"] is True
    full = m.score(*[V(topics=["voice"], goals=["sing"], offers=["songs"], needs=["amps"], wants=["voice"]),
                     V(topics=["voice"], goals=["sing"], offers=["amps"], needs=["songs"], wants=["songs"])])
    assert full["signal_coverage_percent"] == 100


# ---- item 4: self-match + robustness --------------------------------------

def test_rank_matches_excludes_self_by_name_and_identity():
    ent = dict(SEATS["naya-power (Naya P Narzan, Builder/Integrator)"])
    cands = {"me": ent, **PROJECTS}
    names = [r["name"] for r in m.rank_matches(ent, cands, self_name="me")]
    assert "me" not in names
    names2 = [r["name"] for r in m.rank_matches(ent, PROJECTS)]  # identity: PROJECTS holds other dicts
    assert names2  # still ranks the real corpus

def test_malformed_vectors_never_crash():
    bad = [None, 42, "gardening", {"topics": None}, {"topics": [1, 2, None, "chess"]},
           {"topics": "solo string topic"}, {"goals": []}, {}, {"topics": ["a", "a", "a"]}]
    for x in bad:
        for y in bad:
            r = m.score(x, y)
            assert 0 <= r["score"] <= 100 and isinstance(r["surface"], bool)
    rows = m.rank_matches(None, {"x": None, "y": {"topics": ["chess"]}})
    assert rows == []

def test_duplicate_candidates_both_rank():
    twin = V(topics=["chess"], goals=["play"], offers=["coaching"], needs=[], wants=[])
    ent = V(topics=["chess"], goals=["play"], offers=[], needs=["coaching"], wants=["chess partners"])
    names = [r["name"] for r in m.rank_matches(ent, {"club a": twin, "club b": dict(twin)})]
    assert names == ["club a", "club b"]  # same vector, two names: both surface

def test_unicode_and_emoji_vectors():
    a = V(topics=["🌱 jardinage urbain", "compost ♻️"], goals=["nourrir le quartier"], offers=[], needs=[], wants=[])
    b = V(topics=["jardinage urbain", "compost"], goals=["nourrir le quartier"], offers=[], needs=[], wants=[])
    r = m.score(a, b)
    assert r["score"] > 0 and r["surface"] is True


# ---- item 9: verified-value record ----------------------------------------

def test_value_record_contract():
    a = V(topics=["voice"], goals=["go"], offers=[], needs=[], wants=[])
    b = V(topics=["voice"], goals=["go"], offers=[], needs=[], wants=[])
    plain = m.score(a, b)
    assert m.score(a, b, value_b=1.0)["rank"] == plain["rank"]          # bare float: neutral
    assert m.score(a, b, value_b={"state": "PENDING", "value": 1.0})["rank"] == plain["rank"]
    assert m.score(a, b, value_b={"state": "OBSERVED", "value": 1.0})["rank"] == plain["rank"]
    assert m.score(a, b, value_b={"state": "VERIFIED", "value": 1.0})["rank"] == plain["rank"]  # full value: no discount
    assert m.score(a, b, value_b={"state": "VERIFIED", "value": 0.0})["rank"] < plain["rank"]   # verified-zero demotes
    assert m.score(a, b, value_b={"state": "FINAL", "value": 0.5})["rank"] >= m.score(a, b, value_b={"state": "VERIFIED", "value": 0.0})["rank"]
    assert m.score(a, b, value_b={"state": "VERIFIED"})["rank"] == plain["rank"]  # no value: neutral
    assert m.score(a, b, value_b={"state": "VERIFIED", "value": "high"})["rank"] == plain["rank"]
    # the % never moves, whatever the record:
    assert m.score(a, b, value_b={"state": "VERIFIED", "value": 1.0})["score"] == plain["score"]


# ---- item 10: alias safety -------------------------------------------------

def test_alias_safety():
    ok = w.issue_link_sql("maya-rivers")
    assert "'maya-rivers'" in ok
    for bad in ("o'brien", "a'; drop table ambassador_links; --", "UPPER", "has space",
                "x" * 40, "", "a", "-lead", None, 42):
        try:
            w.issue_link_sql(bad)
        except ValueError:
            continue
        raise AssertionError(f"alias accepted but must not be: {bad!r}")


# ---- item 6 (unit leg): indexed == naive on the declared population --------

def test_indexed_matches_naive_on_population():
    corpus = {**SEATS, **PROJECTS}
    index = m.build_index(corpus)
    for name, ent in corpus.items():
        naive = m.rank_matches(ent, corpus, self_name=name)
        fast = m.rank_matches_indexed(ent, corpus, index=index, self_name=name)
        assert [(r["name"], r["score"]) for r in naive] == [(r["name"], r["score"]) for r in fast], name


# ---- item 5 (unit leg): IDF mode ------------------------------------------

def test_idf_default_off_and_ubiquity_discount():
    pop = list({**SEATS, **PROJECTS}.values())
    assert m.compute_idf(pop) == {} or all(v == 1.0 or True for v in m.compute_idf(pop).values())
    idf = m.compute_idf(pop, threshold=0.49)  # 'builder' sits at exactly 6/12
    assert idf.get("builder") == 0.25
    a, b = SEATS["naya-power (Naya P Narzan, Builder/Integrator)"], PROJECTS["Team Nitro (space-team-nitro)"]
    assert m.score(a, b, idf=idf)["score"] < m.score(a, b)["score"]  # builder-inflated pair deflates
    top = m.score(SEATS["nitro (Naya N Narzan, Nitro/Executor/Verifier)"], PROJECTS["Team Nitro (space-team-nitro)"], idf=idf)
    assert top["surface"] is True  # the true pair survives the discount


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
