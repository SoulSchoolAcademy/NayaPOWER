#!/usr/bin/env python3
"""Calibration harness — sweeps the weight grid against the Golden Set.
Question it answers with evidence: are the Lock Packet's v1 weights
(40/25/20/15) at or near the best this labeled evidence supports?
It changes NOTHING by itself — its output is the evidence packet.
Run: python3 calibrate.py"""
import itertools
import golden_set as G
import smart_match as m

def evaluate(weights):
    m.WEIGHTS.update(weights)
    ok = bad = 0
    margins = []
    for label, a, b, expect in G.PAIRS:
        if expect is None:
            continue
        r = m.score(a, b)
        if r["surface"] == expect:
            ok += 1
        else:
            bad += 1
    for label, e, corpus, name in G.TOP1:
        rows = m.rank_matches(e, corpus)
        if rows and rows[0]["name"] == name:
            ok += 1
            runner = rows[1]["score"] if len(rows) > 1 else 0
            margins.append(rows[0]["score"] - runner)
        else:
            bad += 1
    return ok, bad, (sum(margins) / len(margins) if margins else 0)

if __name__ == "__main__":
    base = dict(m.WEIGHTS)
    ok, bad, margin = evaluate(base)
    print(f"current weights {base}: {ok} right, {bad} wrong, mean top-1 margin {margin:.1f}")
    best = []
    for t in (0.30, 0.35, 0.40, 0.45, 0.50):
        for g in (0.15, 0.20, 0.25, 0.30):
            for o in (0.10, 0.15, 0.20, 0.25):
                w = round(1.0 - t - g - o, 2)
                if w < 0.05 or w > 0.30:
                    continue
                ok2, bad2, margin2 = evaluate({"topics": t, "goals": g, "offers_needs": o, "wants": w})
                best.append((ok2, margin2, {"topics": t, "goals": g, "offers_needs": o, "wants": w}))
    m.WEIGHTS.update(base)
    best.sort(key=lambda x: (-x[0], -x[1]))
    print("top grid points (right, margin, weights):")
    for row in best[:3]:
        print("  ", row)
    cur = [b for b in best if b[2] == {"topics": 0.40, "goals": 0.25, "offers_needs": 0.20, "wants": 0.15}]
    print("current weights appear in grid:", bool(cur), cur[:1])
