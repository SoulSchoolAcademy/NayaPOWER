#!/usr/bin/env python3
"""Bench leg 2 (hardening item 6 follow-up, honestly labeled).

A) IDF precision/recall at n=200 on the bench_smart_match population
   (verbatim the leg the main bench script would have run last).
B) n=10,000 indexed per-entity cost on a 25-entity sample (the candidate
   set is degenerate on this population — see bench.txt — so this is the
   honest per-entity number, extrapolated and labeled).
C) Selective-token scenario, n=300: same generator WITHOUT the ubiquitous
   filler topic and with cross-theme picks removed, so signature tokens
   are selective — naive vs indexed, the regime the pre-filter is for.
"""
import sys, time
import smart_match as m
from bench_smart_match import make_population, full_rank, theme_pool
import random

print("== A) IDF evidence, n=200 (planted truth = same theme) ==")
pop, truth = make_population(200)
idf = m.compute_idf(list(pop.values()))
print(f"down-weighted tokens: {sorted(idf)}")
names = list(pop)
for label, kw in (("OFF", {}), ("ON", {"idf": idf})):
    tp = fp = fn_ = 0
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r = m.score(pop[names[i]], pop[names[j]], **kw)
            same = truth[names[i]] == truth[names[j]]
            if r["surface"] and same: tp += 1
            elif r["surface"] and not same: fp += 1
            elif not r["surface"] and same: fn_ += 1
    prec = tp / (tp + fp) if tp + fp else 0
    rec = tp / (tp + fn_) if tp + fn_ else 0
    print(f"IDF {label}: surfaced TP={tp} FP={fp} FN={fn_}  precision={prec:.2f} recall={rec:.2f}")
sys.stdout.flush()

print("== B) n=10,000 indexed, 25-entity sample ==")
pop, _ = make_population(10000)
index = m.build_index(pop)
t0 = time.perf_counter()
for name in list(pop)[:25]:
    m.rank_matches_indexed(pop[name], pop, index=index, self_name=name)
dt = time.perf_counter() - t0
print(f"indexed ranking: {dt / 25:.3f}s/entity -> extrapolated full 10,000: {dt / 25 * 10000 / 60:.0f} min")
print(f"naive full at 10,000 (extrapolated from 0.260 ms/score): {0.00026 * 10000 * 9999 / 60:.0f} min")
sys.stdout.flush()

print("== C) selective-token scenario, n=300 ==")
def make_selective(n, seed=20261024):
    rng = random.Random(seed)
    themes = list(theme_pool.__defaults__ or [])  # placeholder, replaced below
    from bench_smart_match import DOMAINS
    pop, truth = {}, {}
    for i in range(n):
        theme = DOMAINS[i % len(DOMAINS)]
        pool = theme_pool(theme)
        pick = lambda xs, k: [rng.choice(xs) for _ in range(k)]
        vec = {
            "topics": sorted(set(pick(pool["topics"], 3))),
            "goals": sorted(set(pick(pool["goals"], 2))),
            "offers": sorted(set(pick(pool["services"], 2))),
            "needs": sorted(set(pick(pool["services"], 2))),
            "wants": sorted(set(pick([f"{theme} people", f"{theme} learners"], 1))),
        }
        name = f"citizen-{i:05d}"
        pop[name] = vec
        truth[name] = theme
    return pop, truth

pop, _ = make_selective(300)
t_naive, naive_rows = full_rank(pop)
index = m.build_index(pop)
sizes = []
for name in list(pop)[:50]:
    sig = m.signature(pop[name])
    sizes.append(len(set().union(*[index.get(tok, set()) for tok in sig]) - {name}))
t_idx, idx_rows = full_rank(pop, indexed=True)
mism = sum(1 for n in pop if [(r['name'], r['score']) for r in naive_rows[n]] != [(r['name'], r['score']) for r in idx_rows[n]])
print(f"naive: {t_naive:.1f}s   indexed: {t_idx:.1f}s   speedup {t_naive / t_idx:.1f}x")
print(f"mean candidate set (50-entity sample): {sum(sizes) / len(sizes):.0f} of 299")
print(f"identity: {300 - mism}/300 identical, {mism} mismatches")
