#!/usr/bin/env python3
"""Bench leg C2 (labeled scenario): disjoint-vocabulary population, n=300.
Each theme owns a private vocabulary (no shared suffix words, no global
pools) — the regime real free-text citizen declarations approximate, where
signature tokens are selective. Naive vs indexed + identity proof."""
import random, time
import smart_match as m
from bench_smart_match import full_rank

THEMES = {
    "garden": ["roses", "soil", "pruning", "compost", "seedlings", "herbs"],
    "chess": ["openings", "gambit", "endgame", "tactics", "blitz", "notation"],
    "astro": ["telescopes", "nebula", "orbits", "starlight", "planets", "comets"],
    "bakery": ["sourdough", "croissants", "ovens", "kneading", "frosting", "yeast"],
    "surf": ["waves", "boards", "tides", "paddling", "wetsuits", "breakers"],
    "code": ["compilers", "debugging", "algorithms", "databases", "keyboards", "syntax"],
    "bees": ["hives", "honey", "apiary", "smokers", "queens", "pollen"],
    "pottery": ["kilns", "glazing", "clay", "wheels", "firing", "earthenware"],
}

def make(n, seed=7):
    rng = random.Random(seed)
    themes = list(THEMES)
    pop, truth = {}, {}
    for i in range(n):
        t = themes[i % len(themes)]
        w = THEMES[t]
        pick = lambda k: sorted(rng.sample(w, k))
        vec = {"topics": pick(3), "goals": pick(2), "offers": pick(2),
               "needs": pick(2), "wants": pick(1)}
        name = f"citizen-{i:05d}"
        pop[name] = vec
        truth[name] = t
    return pop, truth

pop, _ = make(300)
t_naive, naive_rows = full_rank(pop)
index = m.build_index(pop)
sizes = []
for name in list(pop)[:50]:
    sig = m.signature(pop[name])
    sizes.append(len(set().union(*[index.get(tok, set()) for tok in sig]) - {name}))
t_idx, idx_rows = full_rank(pop, indexed=True)
mism = sum(1 for n in pop if [(r['name'], r['score']) for r in naive_rows[n]] != [(r['name'], r['score']) for r in idx_rows[n]])
print(f"disjoint-vocabulary n=300: naive {t_naive:.1f}s  indexed {t_idx:.2f}s  speedup {t_naive / t_idx:.1f}x")
print(f"mean candidate set (50-entity sample): {sum(sizes) / len(sizes):.0f} of 299")
print(f"identity: {300 - mism}/300 identical, {mism} mismatches")
