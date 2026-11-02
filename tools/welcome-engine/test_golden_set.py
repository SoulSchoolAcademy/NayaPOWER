#!/usr/bin/env python3
"""Golden Set as a pytest module (v1.5 hardening, item 2) — the 12 labeled
cases from golden_set.py, pinned individually so CI catches drift in any
single case instead of the set as a whole. Expectations live in
golden_set.py; this module only re-expresses them as tests.
Run: python3 -m pytest test_golden_set.py  (or python3 test_golden_set.py)"""
import golden_set as G
import smart_match as m


def _pair_test(a, b, expect):
    def run():
        assert m.score(a, b)["surface"] is expect
    return run


def _top1_test(entity, corpus, name):
    def run():
        rows = m.rank_matches(entity, corpus)
        assert rows and rows[0]["name"] == name
    return run


for _i, (_label, _a, _b, _expect) in enumerate(
        [p for p in G.PAIRS if p[3] is not None]):
    globals()[f"test_golden_pair_{_i:02d}"] = _pair_test(_a, _b, _expect)
for _i, (_label, _e, _corpus, _name) in enumerate(G.TOP1):
    globals()[f"test_golden_top1_{_i:02d}"] = _top1_test(_e, _corpus, _name)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
