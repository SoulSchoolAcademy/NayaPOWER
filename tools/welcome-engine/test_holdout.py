#!/usr/bin/env python3
"""Holdout accuracy pinned as tests (v1.5 hardening, item 8). The cases and
expectations live in holdout_set.py — hand-written, synthetic, NOT derived
from the declared population. This module asserts the set's accuracy bar:
every clear case must hold; a borderline miss must be investigated, never
silently re-labeled.
Run: python3 -m pytest test_holdout.py  (or python3 test_holdout.py)"""
import holdout_set as H
from smart_match import score, rank_matches


def _pair_test(a, b, expect):
    def run():
        assert score(a, b)["surface"] is expect
    return run


for _i, (_label, _a, _b, _expect) in enumerate(H.PAIRS):
    globals()[f"test_holdout_pair_{_i:02d}"] = _pair_test(_a, _b, _expect)


def test_holdout_orderings():
    for label, e, corpus, top1, beat in H.ORDERINGS:
        rows = rank_matches(e, corpus)
        assert rows and rows[0]["name"] == top1, label
        if beat:
            by_name = {r["name"]: r["score"] for r in rows}
            assert beat not in by_name or by_name[top1] > by_name[beat], label


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn(); print("PASS", fn.__name__)
    print(f"{len(fns)}/{len(fns)} tests passed")
