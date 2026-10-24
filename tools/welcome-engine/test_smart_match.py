#!/usr/bin/env python3
"""Smart Match tests — behavior pinned so the math can't drift silently.
Run: python3 test_smart_match.py (stdlib only)."""
import smart_match as m

V = lambda **kw: kw  # tiny vector builder

def test_perfectly_complementary_is_100():
    # 100 means every signal family aligns — a COMPLEMENTARY pair, not an
    # identical one (nobody's offers need to match their own needs).
    a = V(topics=["voice"], goals=["sing"], offers=["songs"], needs=["amps"], wants=["voice"])
    b = V(topics=["voice"], goals=["sing"], offers=["amps"], needs=["songs"], wants=["songs"])
    assert m.score(a, b)["score"] == 100

def test_disjoint_is_0_and_not_surfaced():
    a = V(topics=["voice"], goals=["sing"], offers=["songs"], needs=["amps"], wants=["fans"])
    b = V(topics=["tax law"], goals=["file"], offers=["audits"], needs=["forms"], wants=["clients"])
    r = m.score(a, b)
    assert r["score"] == 0 and r["surface"] is False

def test_two_signal_bar():
    a = V(topics=["voice"], goals=["x"], offers=[], needs=[], wants=[])
    b = V(topics=["voice"], goals=["y"], offers=[], needs=[], wants=[])
    assert m.score(a, b)["surface"] is False  # one signal only: held back

def test_taxonomy_bridges_synonyms():
    a = V(topics=["ship"], goals=[], offers=[], needs=[], wants=[])
    b = V(topics=["delivery"], goals=[], offers=[], needs=[], wants=[])
    assert m.score(a, b)["parts"]["topics"] > 0  # SHIPPING concept bridges ship/delivery

def test_resolve_case_is_visible():
    # The v1 blindness: a resolver must see the distillation program via THINKING.
    resolver = V(topics=["root cause", "critical thinking", "risk"], goals=[], offers=["analysis"], needs=[], wants=[])
    mirror = V(topics=["distillation", "essence", "learning"], goals=[], offers=[], needs=[], wants=[])
    assert m.score(resolver, mirror)["parts"]["topics"] > 0

def test_percent_is_relevance_not_value():
    a = V(topics=["voice"], goals=["go"], offers=[], needs=[], wants=[])
    b = V(topics=["voice"], goals=["go"], offers=[], needs=[], wants=[])
    plain = m.score(a, b)
    valued = m.score(a, b, value_b=1.0)
    assert plain["score"] == valued["score"]       # % never moves with value
    assert valued["rank"] >= plain["rank"]          # only the ranking does

def test_deterministic_order():
    e = V(topics=["systems", "building"], goals=["prove outcomes"], offers=["builders"], needs=[], wants=["builders"])
    cands = {"B proj": V(topics=["systems"], goals=["prove outcomes"], offers=[], needs=["builders"], wants=[]),
             "A proj": V(topics=["building"], goals=["prove outcomes"], offers=[], needs=["builders"], wants=[])}
    r1 = [r["name"] for r in m.rank_matches(e, cands)]
    r2 = [r["name"] for r in m.rank_matches(e, cands)]
    assert r1 == r2  # same input, same order, every run

def test_empty_vectors_never_crash():
    assert m.score({}, {})["score"] == 0

def test_word_tier_bridges_free_vocabulary():
    a = V(topics=["urban gardening"], goals=[], offers=[], needs=[], wants=[])
    b = V(topics=["gardening"], goals=[], offers=[], needs=[], wants=[])
    assert m.score(a, b)["parts"]["topics"] > 0


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
